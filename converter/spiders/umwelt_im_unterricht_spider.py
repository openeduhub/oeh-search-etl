import re

import scrapy
import w3lib.html
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, \
    LomClassificationItemLoader
from converter.spiders.base_classes import LomBase


class UmweltImUnterrichtSpider(CrawlSpider, LomBase):
    """
    Crawler for Umwelt-im-Unterricht.de
    (Bundesministerium für Umwelt, Naturschutz und nukleare Sicherheit)
    """
    name = "umwelt_im_unterricht_spider"
    friendlyName = "Umwelt im Unterricht"
    start_urls = [
        "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Atopics",
        # Typ: Thema der Woche
        "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Alessons",
        # Typ: Unterrichtsvorschlag
        "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Acontexts",
        # Typ: Hintergrund (Kontext)
        "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Amaterials",
        # Typ: Arbeitsmaterial
        "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Amaterials_video",
        # Typ: Video
        "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Amaterials_images",
        # Typ: Bilderserie
    ]
    version = "0.0.2"  # last update: 2021-10-08
    topic_urls = set()  # urls that need to be parsed will be added here
    topic_urls_parsed = set()  # this set is used for 'checking off' already parsed (individual) topic urls
    overview_urls_already_parsed = set()  # this set is used for 'checking off' already parsed overview_pages

    EDUCATIONAL_CONTEXT_MAPPING: dict = {
        'Sekundarstufe': ['Sekundarstufe I', 'Sekundarstufe II']
    }
    DISCIPLINE_MAPPING: dict = {
        'Arbeit, Wirtschaft, Technik': 'Arbeitslehre',
        'Ethik, Philosophie, Religion': ['Ethik', 'Philosophie', 'Religion'],
        'Fächerübergreifend': 'Allgemein',
        'Politik, SoWi, Gesellschaft': ['Politik', 'Sozialkunde', 'Gesellschaftskunde']
    }

    def getId(self, response=None) -> str:
        pass

    def getHash(self, response=None) -> str:
        pass

    def parse_start_url(self, response, **kwargs):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_category_overview_for_topics_and_subpages)

    def parse_category_overview_for_topics_and_subpages(self, response: scrapy.http.Response):
        """
        Crawls an overview page of a "type"-category (e.g. "Hintergrund", "Bilderserie" etc.) for subpages and topics.
        If the overview has subpages, it will recursively yield additional scrapy.Requests to the overview-subpages.
        Afterwards it yields the (10) individual topic_urls (per overview page) to the parse()-method.

        Scrapy Contracts:
        @url https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Alessons
        @returns requests 10
        """
        topic_urls_raw: list = response.xpath('//a[@class="internal-link readmore"]/@href').getall()

        for url_ending in topic_urls_raw:
            self.topic_urls.add(response.urljoin(url_ending))

        # if there's a "Letzte"-Button in the overview, there's more topic_urls to be gathered than the initially
        # displayed 10 elements
        last_page_button_url: str = response.xpath('//li[@class="tx-pagebrowse-last last"]/a/@href').get()
        # the string last_page_button_url typically looks like this:
        # "/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Amaterials_images&tx_solr%5Bpage%5D=8"
        page_number_regex = re.compile(r'(?P<url_with_parameters>.*&tx_solr%5Bpage%5D=)(?P<nr>\d+)')

        overview_urls_parsed: set = set()   # temporary set used for checking off already visited URLs
        if last_page_button_url is not None:
            page_number_dict: dict = page_number_regex.search(last_page_button_url).groupdict()
            url_without_page_parameter: str = response.urljoin(page_number_dict.get('url_with_parameters'))
            last_page_number = int(page_number_dict.get('nr'))
            for i in range(2, last_page_number + 1):
                # the initial url from start_urls already counts as page 1, therefore we're iterating
                # from page 2 to the last page
                next_overview_subpage_to_crawl = str(url_without_page_parameter + str(i))
                if next_overview_subpage_to_crawl not in self.overview_urls_already_parsed:
                    yield scrapy.Request(url=next_overview_subpage_to_crawl,
                                         callback=self.parse_category_overview_for_topics_and_subpages)
                    overview_urls_parsed.add(next_overview_subpage_to_crawl)
            self.overview_urls_already_parsed.update(overview_urls_parsed)  # checking off the (10) URLs that we yielded

        parsed_urls: set = set()    # temporary set used for checking off already visited topics
        for url in self.topic_urls:
            if url not in self.topic_urls_parsed:
                # making sure that we don't accidentally crawl individual pages more than once
                yield scrapy.Request(url=url, callback=self.parse)
                parsed_urls.add(url)
        self.topic_urls_parsed.update(parsed_urls)

    def parse(self, response: scrapy.http.Response, **kwargs):
        """
        Parses an individual topic url for metadata and yields a BaseItem.

        Scrapy Contracts:
        @url https://www.umwelt-im-unterricht.de/hintergrund/generationengerechtigkeit-klimaschutz-und-eine-lebenswerte-zukunft/
        @returns item 1
        """
        current_url: str = response.url
        base = BaseItemLoader()

        base.add_value('sourceId', response.url)
        date_raw: str = response.xpath('//div[@class="b-cpsuiu-show-info"]/span/text()').get()
        date_cleaned_up: str = w3lib.html.strip_html5_whitespace(date_raw)
        hash_temp = str(date_cleaned_up + self.version)
        base.add_value('hash', hash_temp)
        base.add_value('lastModified', date_cleaned_up)
        base.add_value('type', Constants.TYPE_MATERIAL)
        # base.add_value('thumbnail', thumbnail_url)

        lom = LomBaseItemloader()

        general = LomGeneralItemloader()
        general.add_value('identifier', response.url)
        title: str = response.xpath('//div[@class="tx-cps-uiu"]/article/h1/text()').get()
        general.add_value('title', title)
        keywords: list = response.xpath('//div[@class="b-cpsuiu-show-keywords"]/ul/li/a/text()').getall()
        if len(keywords) >= 1:
            # only add keywords if the list isn't empty
            general.add_value('keyword', keywords)
        description: str = response.xpath('/html/head/meta[@name="description"]/@content').get()
        general.add_value('description', description)
        general.add_value('language', 'de')

        lom.add_value('general', general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value('format', 'text/html')
        technical.add_value('location', response.url)
        lom.add_value('technical', technical.load_item())

        lifecycle = LomLifecycleItemloader()
        lifecycle.add_value('role', 'publisher')
        lifecycle.add_value('date', date_cleaned_up)
        lifecycle.add_value('url', "https://www.umwelt-im-unterricht.de/impressum/")
        lifecycle.add_value('organization', 'Bundesministerium für Umwelt, Naturschutz und nukleare Sicherheit (BMU)')
        lom.add_value('lifecycle', lifecycle.load_item())

        educational = LomEducationalItemLoader()
        educational.add_value('language', 'de')

        # TODO: a didactic comment could fit into either one of these:
        #  - educational.description
        #  - classification.description (with classification.purpose set to 'educational objective')
        if "/wochenthemen/" in current_url:
            # didactic comments are only part of "Thema der Woche"
            didactic_comment = response.xpath('//div[@class="c-collapse-content js-collapse-content"]').get()
            if didactic_comment is not None:
                didactic_comment = w3lib.html.remove_tags(didactic_comment)
                # didactic_comment = w3lib.html.replace_escape_chars(didactic_comment, which_ones='\t', replace_by=" ")
                # didactic_comment = w3lib.html.replace_escape_chars(didactic_comment)
                didactic_comment = " ".join(didactic_comment.split())
                if didactic_comment.endswith("mehr lesenweniger lesen"):
                    # the button-description of the expandable info-box ends up in the string,
                    # therefore we are manually removing it:
                    didactic_comment = didactic_comment.replace("mehr lesenweniger lesen", "")
                # since there's currently no way to confirm how the string looks in the web-interface:
                # ToDo: make sure which string format looks best in edu-sharing (cleaned up <-> with escape chars)
                educational.add_value('description', didactic_comment)

        lom.add_value('educational', educational.load_item())

        classification = LomClassificationItemLoader()
        if "/unterrichtsvorschlaege/" in current_url:
            classification.add_value('purpose', 'competency')
            competency_description: list = response.xpath('//div[@class="b-cpsuiu-show-description"]/*[not('
                                                          '@class="cc-licence-info")]').getall()
            # the xpath-expression for competency_description will grab the whole div-element,
            # but EXCLUDE the "license"-container (if the license-description exists, it's always part of the same div)
            if len(competency_description) >= 1:
                # only if the list of strings is not empty, we'll try to type-convert it to a string (and clean its
                # formatting up)
                competency_description: str = " ".join(competency_description)
                competency_description = w3lib.html.remove_tags(competency_description)
                classification.add_value('description', competency_description)

        lom.add_value('classification', classification.load_item())
        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()

        # depending on the website-category, we need to set a specific learningResourceType
        # because the value 'website' for all crawled items would not be helpful enough
        if "/wochenthemen/" in current_url or "/unterrichtsvorschlaege/" in current_url:
            vs.add_value('learningResourceType', 'lesson plan')
        if "/hintergrund/" in current_url:
            vs.add_value('learningResourceType', 'Text')
        if "/medien/dateien/" in current_url:
            # topics categorized as "Arbeitsmaterial" offer customizable worksheets to teachers
            vs.add_value('learningResourceType', 'worksheet')
        if "/medien/videos/" in current_url:
            vs.add_value('learningResourceType', 'video')
        if "/medien/bilder/" in current_url:
            # topics categorized as "Bilderserie" hold several images in a gallery (with individual licenses)
            vs.add_value('learningResourceType', 'image')

        vs.add_value('price', 'no')
        vs.add_value('containsAdvertisement', 'no')
        vs.add_value('conditionsOfAccess', 'no login')
        vs.add_value('intendedEndUserRole', 'teacher')
        # see: https://www.umwelt-im-unterricht.de/ueber-umwelt-im-unterricht/
        vs.add_value('accessibilitySummary', 'Not tested')
        # see: https://www.umwelt-im-unterricht.de/erklaerung-zur-barrierefreiheit/
        vs.add_value('dataProtectionConformity', 'Sensible data collection')
        # see: https://www.umwelt-im-unterricht.de/datenschutz/

        disciplines_raw: list = response.xpath('//div[@class="b-cpsuiu-show-subjects"]/ul/li/a/text()').getall()
        if len(disciplines_raw) >= 1:
            disciplines = list()
            for discipline_value in disciplines_raw:
                # self.debug_discipline_values.add(discipline_value)
                if discipline_value in self.DISCIPLINE_MAPPING.keys():
                    discipline_value = self.DISCIPLINE_MAPPING.get(discipline_value)
                # since the mapping value can either be a single string OR a list of strings, we need to make sure that
                # our 'disciplines'-list is a list of strings (not a list with nested lists):
                if type(discipline_value) is list:
                    disciplines.extend(discipline_value)
                else:
                    disciplines.append(discipline_value)
            if len(disciplines) >= 1:
                vs.add_value('discipline', disciplines)

        educational_context_raw = response.xpath('//div[@class="b-cpsuiu-show-targets"]/ul/li/a/text()').getall()
        if len(educational_context_raw) >= 1:
            # the educationalContext-mapping is only done when there's at least one educational_context found
            educational_context = list()
            for educational_context_value in educational_context_raw:
                # self.debug_educational_context_values.add(educational_context_value)
                if educational_context_value in self.EDUCATIONAL_CONTEXT_MAPPING.keys():
                    educational_context_value = self.EDUCATIONAL_CONTEXT_MAPPING.get(educational_context_value)
                if type(educational_context_value) is list:
                    educational_context.extend(educational_context_value)
                else:
                    educational_context.append(educational_context_value)
            if len(educational_context) >= 1:
                vs.add_value('educationalContext', educational_context)

        base.add_value('valuespaces', vs.load_item())

        lic = LicenseItemLoader()
        license_url: str = response.xpath('//div[@class="cc-licence-info"]/p/a[@rel="license"]/@href').get()
        if license_url is not None:
            if license_url.startswith("http://"):
                # the license-mapper expects urls that are in https:// format, but UIU uses http:// links to CC-licenses
                license_url = license_url.replace("http://", "https://")
            lic.add_value('url', license_url)

        license_description_raw: str = response.xpath('//div[@class="cc-licence-info"]').get()
        if license_description_raw is not None:
            license_description_raw = w3lib.html.remove_tags(license_description_raw)
            license_description_raw = w3lib.html.replace_escape_chars(license_description_raw, which_ones="\n",
                                                                      replace_by=" ")
            # if we would replace_escape_chars() straight away, there would be words stuck together that don't belong
            # together. just replacing \n with a whitespace is enough to keep the structure of the string intact.
            license_description_raw = w3lib.html.replace_escape_chars(license_description_raw)
            license_description = " ".join(license_description_raw.split())
            # making sure that there's only 1 whitespace between words
            lic.add_value('description', license_description)
        base.add_value('license', lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value('permissions', permissions.load_item())

        response_loader = super().mapResponse(response)
        base.add_value('response', response_loader.load_item())

        yield base.load_item()
