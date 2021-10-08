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
    topic_urls_already_parsed = set()  # this set is used for 'checking off' already parsed urls

    EDUCATIONAL_CONTEXT_MAPPING: dict = {
        'Sekundarstufe': ['Sekundarstufe I', 'Sekundarstufe II']
    }
    DISCIPLINE_MAPPING: dict = {
        'Arbeit, Wirtschaft, Technik': 'Arbeitslehre',
        'Ethik, Philosophie, Religion': ['Ethik', 'Philosophie', 'Religion'],
        'Fächerübergreifend': 'Allgemein',   # ToDo: no mapping available
        'Politik, SoWi, Gesellschaft': ['Politik', 'Sozialkunde', 'Gesellschaftskunde']
    }

    def getId(self, response=None) -> str:
        pass

    def getHash(self, response=None) -> str:
        pass

    def parse_start_url(self, response, **kwargs):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_category_overview_for_individual_topic_urls)

    def parse_category_overview_for_individual_topic_urls(self, response):
        # logging.debug(f"INSIDE PARSE CATEGORY METHOD: {response.url}")
        topic_urls_raw: list = response.xpath('//a[@class="internal-link readmore"]/@href').getall()
        # logging.debug(f"TOPIC URLS (RAW) ={topic_urls_raw}")

        for url_ending in topic_urls_raw:
            self.topic_urls.add(response.urljoin(url_ending))
        # logging.debug(f"TOPIC URLS ({len(self.topic_urls)}) = {self.topic_urls}")

        # if there's a "Letzte"-Button in the overview, there's more topic_urls to be gathered than the initially
        # displayed 10 elements
        last_page_button_url = response.xpath('//li[@class="tx-pagebrowse-last last"]/a/@href').get()
        if last_page_button_url is not None:
            last_page_button_url = response.urljoin(last_page_button_url)
            # Using the "next page"-button until we reach the last page:
            if last_page_button_url != response.url:
                next_page_button_url = response.xpath('//li[@class="tx-pagebrowse-last next"]/a/@href').get()
                if next_page_button_url is not None:
                    next_url_to_parse = response.urljoin(next_page_button_url)
                    yield scrapy.Request(url=next_url_to_parse,
                                         callback=self.parse_category_overview_for_individual_topic_urls)
            # if last_page_button_url == response.url:
            #     logging.debug(f"Reached the last page: {response.url}")
            #     logging.debug(f"{len(self.topic_urls)} individual topic_urls were found: {self.topic_urls}")
        for url in self.topic_urls:
            # making sure that we don't accidentally crawl individual pages more than once
            if url not in self.topic_urls_already_parsed:
                yield scrapy.Request(url=url, callback=self.parse)
                self.topic_urls_already_parsed.add(url)
        # logging.debug(f"topic_urls after yielding them: {len(self.topic_urls)} --- "
        #               f"topic_urls_already_parsed: {len(self.topic_urls_already_parsed)}")

    def parse(self, response, **kwargs):
        current_url: str = response.url
        base = BaseItemLoader()

        base.add_value('sourceId', response.url)
        date_raw = response.xpath('//div[@class="b-cpsuiu-show-info"]/span/text()').get()
        date_cleaned_up = w3lib.html.strip_html5_whitespace(date_raw)
        hash_temp = str(date_cleaned_up + self.version)
        base.add_value('hash', hash_temp)
        base.add_value('lastModified', date_cleaned_up)
        base.add_value('type', Constants.TYPE_MATERIAL)
        # base.add_value('thumbnail', thumbnail_url)

        lom = LomBaseItemloader()

        general = LomGeneralItemloader()
        general.add_value('identifier', response.url)
        title = response.xpath('//div[@class="tx-cps-uiu"]/article/h1/text()').get()
        general.add_value('title', title)
        keywords = response.xpath('//div[@class="b-cpsuiu-show-keywords"]/ul/li/a/text()').getall()
        if len(keywords) >= 1:
            general.add_value('keyword', keywords)
        description = response.xpath('/html/head/meta[@name="description"]/@content').get()
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
                    # the button-description of the expandable info-box ends up in the string, therefore removing it:
                    didactic_comment = didactic_comment.replace("mehr lesenweniger lesen", "")
                # ToDo: make sure which string format looks best in edu-sharing (cleaned up <-> with escape chars)
                educational.add_value('description', didactic_comment)

        lom.add_value('educational', educational.load_item())

        classification = LomClassificationItemLoader()
        if "/unterrichtsvorschlaege/" in current_url:
            classification.add_value('purpose', 'competency')
            competency_description: list = response.xpath('//div[@class="b-cpsuiu-show-description"]/*[not('
                                                          '@class="cc-licence-info")]').getall()
            # competency_description will grab the whole div-element, but EXCLUDE the "license"-container
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
        vs.add_value('accessibilitySummary', 'Not tested')
        # see: https://www.umwelt-im-unterricht.de/erklaerung-zur-barrierefreiheit/
        vs.add_value('dataProtectionConformity', 'Sensible data collection')
        # see: https://www.umwelt-im-unterricht.de/datenschutz/
        # see: https://www.umwelt-im-unterricht.de/ueber-umwelt-im-unterricht/
        disciplines_raw = response.xpath('//div[@class="b-cpsuiu-show-subjects"]/ul/li/a/text()').getall()
        if len(disciplines_raw) >= 1:
            disciplines = list()
            for discipline_value in disciplines_raw:
                # self.debug_discipline_values.add(discipline_value)
                if discipline_value in self.DISCIPLINE_MAPPING.keys():
                    discipline_value = self.DISCIPLINE_MAPPING.get(discipline_value)
                if type(discipline_value) is list:
                    disciplines.extend(discipline_value)
                else:
                    disciplines.append(discipline_value)
            if len(disciplines) >= 1:
                vs.add_value('discipline', disciplines)

        educational_context_raw = response.xpath('//div[@class="b-cpsuiu-show-targets"]/ul/li/a/text()').getall()
        if len(educational_context_raw) >= 1:
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
                license_url = license_url.replace("http://", "https://")
            lic.add_value('url', license_url)

        license_description_raw = response.xpath('//div[@class="cc-licence-info"]').get()
        if license_description_raw is not None:
            license_description_raw = w3lib.html.remove_tags(license_description_raw)
            license_description_raw = w3lib.html.replace_escape_chars(license_description_raw, which_ones="\n",
                                                                      replace_by=" ")
            # if we would replace_escape_chars() straight away, there would be words stuck together that don't belong
            # together. just replacing \n with a whitespace is enough to keep the structure of the string intact.
            license_description_raw = w3lib.html.replace_escape_chars(license_description_raw)
            license_description = " ".join(license_description_raw.split())
            # making sure that there's only 1 whitespace between words, not 4+ when the original string had serveral \t
            lic.add_value('description', license_description)
        base.add_value('license', lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value('permissions', permissions.load_item())

        response_loader = super().mapResponse(response)
        base.add_value('response', response_loader.load_item())

        # once all scrapy.Item are loaded into our "base", we yield the BaseItem by calling the .load_item() method
        yield base.load_item()
