import datetime
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
    version = "0.0.4"  # last update: 2022-04-26
    topic_urls = set()  # urls that need to be parsed will be added here
    topic_urls_parsed = set()  # this set is used for 'checking off' already parsed (individual) topic urls
    overview_urls_already_parsed = set()  # this set is used for 'checking off' already parsed overview_pages

    EDUCATIONAL_CONTEXT_MAPPING: dict = {
        'Grundschule': "Primarstufe",
        # ToDo: find out why the pipeline doesn't map altLabels by itself
        # while "Grundschule" is the altLabel for "Primarstufe" in our educationalContext Vocab,
        # the valuespaces converter / pipeline only seems to map to 'prefLabel' entries?
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
        for url in self.topic_urls.copy():
            if url not in self.topic_urls_parsed:
                # making sure that we don't accidentally crawl individual pages more than once
                yield scrapy.Request(url=url, callback=self.parse)
                parsed_urls.add(url)
        self.topic_urls_parsed.update(parsed_urls)

    async def parse(self, response: scrapy.http.Response, **kwargs):
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
        if date_cleaned_up is not None:
            # converting the german date format "DD.MM.YYYY" to YYYY-MM-DD
            date_iso = datetime.datetime.strptime(date_cleaned_up, "%d.%m.%Y")
            date_cleaned_up = date_iso.isoformat()
        hash_temp = str(date_cleaned_up + self.version)
        base.add_value('hash', hash_temp)
        base.add_value('lastModified', date_cleaned_up)
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
        lifecycle.add_value('url', "https://www.umwelt-im-unterricht.de/")
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

        vs.add_value('new_lrt', "d8c3ef03-b3ab-4a5e-bcc9-5a546fefa2e9")
        # 'Webseite und Portal (stabil)'
        # depending on the website-category, we need to set a specific learningResourceType
        # because just the value 'website' for all crawled items would not be helpful enough
        if "/wochenthemen/" in current_url or "/unterrichtsvorschlaege/" in current_url:
            # vs.add_value('learningResourceType', 'lesson plan') # ToDo
            vs.add_value('new_lrt', '7381f17f-50a6-4ce1-b3a0-9d85a482eec0')  # Unterrichtsplanung
        if "/hintergrund/" in current_url:
            # vs.add_value('learningResourceType', 'Text')    # ToDo
            vs.add_value('new_lrt', ['b98c0c8c-5696-4537-82fa-dded7236081e', '7381f17f-50a6-4ce1-b3a0-9d85a482eec0'])
            # "Artikel und Einzelpublikation", "Unterrichtsplanung"
        if "/medien/dateien/" in current_url:
            # topics categorized as "Arbeitsmaterial" offer customizable worksheets to teachers, most of the time
            # consisting of both an "Unterrichtsvorschlag" and a worksheet
            # vs.add_value('learningResourceType', 'worksheet')   # ToDo
            vs.add_value('new_lrt', ['36e68792-6159-481d-a97b-2c00901f4f78', '7381f17f-50a6-4ce1-b3a0-9d85a482eec0'])
            # "Arbeitsblatt", "Unterrichtsplanung"
        if "/medien/videos/" in current_url:
            # each video is served together with one or several "Unterrichtsvorschlag"-documents
            # vs.add_value('learningResourceType', 'video')   # ToDo
            vs.add_value('new_lrt', ['7a6e9608-2554-4981-95dc-47ab9ba924de', '7381f17f-50a6-4ce1-b3a0-9d85a482eec0'])
            # "Video (Material)", "Unterrichtsplanung"
        if "/medien/bilder/" in current_url:
            # topics categorized as "Bilderserie" hold several images in a gallery (with individual licenses),
            # they also come with one or several "Unterrichtsvorschlag"-documents that are linked to further below
            # vs.add_value('learningResourceType', 'image')   # ToDo
            vs.add_value('new_lrt', ["a6d1ac52-c557-4151-bc6f-0d99b0b96fb9", "7381f17f-50a6-4ce1-b3a0-9d85a482eec0"])
            # "Bild (Material)", "Unterrichtsplanung"
        # ToDo: once new_lrt goes live:
        #  - remove the old learningResourceType with the next crawler update
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
            educational_context = set()
            for educational_context_value in educational_context_raw:
                # self.debug_educational_context_values.add(educational_context_value)
                if educational_context_value in self.EDUCATIONAL_CONTEXT_MAPPING.keys():
                    educational_context_value = self.EDUCATIONAL_CONTEXT_MAPPING.get(educational_context_value)
                if type(educational_context_value) is list:
                    for educational_context_list_item in educational_context_value:
                        educational_context.add(educational_context_list_item)
                if type(educational_context_value) is str:
                    educational_context.add(educational_context_value)
            if len(educational_context) >= 1:
                vs.add_value('educationalContext', list(educational_context))

        base.add_value('valuespaces', vs.load_item())

        lic = LicenseItemLoader()
        license_url: str = response.xpath('//div[@class="cc-licence-info"]/p/a[@rel="license"]/@href').get()
        if license_url is not None:
            if license_url.startswith("http://"):
                # the license-mapper expects urls that are in https:// format, but UIU uses http:// links to CC-licenses
                license_url = license_url.replace("http://", "https://")
            lic.replace_value('url', license_url)
        else:
            lic.add_value('url', Constants.LICENSE_CC_BY_SA_40)
            # since there are a lot of articles with missing license-information (especially "Thema der Woche",
            # "Bilderserien" and other mixed forms of articles), we're setting the default license to CC-BY-SA 4.0
            # EMail-Confirmation from Umwelt-im-Unterricht (2022-04-26):
            # this license is covering the texts that were produced by UIU! (teasers, intro-texts, summaries)
            # individual pictures from "Bilderserie"-type of topics still carry their own respective licenses (which we
            # currently don't crawl individually)

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

        response_loader = await super().mapResponse(response)
        base.add_value('response', response_loader.load_item())

        yield base.load_item()
