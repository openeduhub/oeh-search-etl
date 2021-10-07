import logging

import scrapy
import w3lib.html
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, ResponseItemLoader, \
    PermissionItemLoader
from converter.spiders.base_classes import LomBase


class UmweltImUnterrichtSpider(CrawlSpider, LomBase):
    """
    Crawler for Umwelt-im-Unterricht.de
    (Bundesministerium für Umwelt, Naturschutz und nukleare Sicherheit)
    """
    name = "umwelt_im_unterricht_spider"
    friendlyName = "Umwelt im Unterricht"
    start_urls = [
        # "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Atopics",
        # # Typ: Thema der Woche
        # "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Alessons",
        # # Typ: Unterrichtsvorschlag
        # "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Acontexts",
        # # Typ: Hintergrund (Kontext)
        # "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Amaterials",
        # # Typ: Arbeitsmaterial
        "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Amaterials_video",
        # Typ: Video
        # "https://www.umwelt-im-unterricht.de/suche/?tx_solr%5Bfilter%5D%5B0%5D=type%3Amaterials_images",
        # # Typ: Bilderserie
    ]
    version = "0.0.1"   # last update: 2021-10-07
    topic_urls = set()  # urls that need to be parsed will be added here
    topic_urls_already_parsed = set()   # this set is used for 'checking off' already parsed urls

    EDUCATIONAL_CONTEXT_MAPPING: dict = {
        # There's only 2 "Zielgruppen": 'Grundschule' and 'Sekundarstufe'
        # ToDo: either map Sekundarstufe to both or neither
        'Sekundarstufe': ['Sekundarstufe I', 'Sekundarstufe II']
    }
    DISCIPLINE_MAPPING: dict = {
        'Arbeit, Wirtschaft, Technik': 'Arbeitslehre',
        'Ethik, Philosophie, Religion': ['Ethik', 'Philosophie', 'Religion'],
        # 'Fächerübergreifend',   # ToDo: no mapping available
        'Politik, SoWi, Gesellschaft': ['Politik', 'Sozialkunde', 'Gesellschaftskunde'],
        # 'Verbraucherbildung'    # ToDo: no mapping available
    }

    def getId(self, response=None) -> str:
        return response.url

    def getHash(self, response=None) -> str:
        date_raw = response.xpath('//div[@class="b-cpsuiu-show-info"]/span/text()').get()
        date_cleaned_up = w3lib.html.strip_html5_whitespace(date_raw)
        hash_temp = str(date_cleaned_up + self.version)
        return hash_temp

    def parse_start_url(self, response, **kwargs):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_category_overview_for_individual_topic_urls)

    def parse_category_overview_for_individual_topic_urls(self, response, **kwargs):
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
        base = BaseItemLoader()
        # ALL possible keys for the different Item and ItemLoader-classes can be found inside converter/items.py

        # TODO: fill "base"-keys with values for
        #  - thumbnail          recommended (let splash handle it)
        #  - publisher          optional
        base.add_value('sourceId', response.url)
        date_raw = response.xpath('//div[@class="b-cpsuiu-show-info"]/span/text()').get()
        date_cleaned_up = w3lib.html.strip_html5_whitespace(date_raw)
        base.add_value('lastModified', date_cleaned_up)
        base.add_value('type', Constants.TYPE_MATERIAL)
        # base.add_value('thumbnail', thumbnail_url)

        lom = LomBaseItemloader()

        general = LomGeneralItemloader()
        # TODO: fill "general"-keys with values for
        #  - coverage                       optional
        #  - structure                      optional
        #  - aggregationLevel               optional
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
        # TODO: fill "technical"-keys with values for
        #  - size                           optional
        #  - requirement                    optional
        #  - installationRemarks            optional
        #  - otherPlatformRequirements      optional
        technical.add_value('format', 'text/html')
        technical.add_value('location', response.url)
        lom.add_value('technical', technical.load_item())

        lifecycle = LomLifecycleItemloader()
        # TODO: fill "lifecycle"-keys with values for
        #  - url                            recommended
        #  - email                          optional
        #  - uuid                           optional
        lifecycle.add_value('role', 'publisher')
        lifecycle.add_value('date', date_cleaned_up)
        lifecycle.add_value('organization', 'Bundesministerium für Umwelt, Naturschutz und nukleare Sicherheit (BMU)')
        lom.add_value('lifecycle', lifecycle.load_item())

        educational = LomEducationalItemLoader()
        # TODO: fill "educational"-keys with values for
        #  - description                    recommended (= "Comments on how this learning object is to be used")
        #  - interactivityType              optional
        #  - interactivityLevel             optional
        #  - semanticDensity                optional
        #  - typicalAgeRange                optional
        #  - difficulty                     optional
        #  - typicalLearningTime            optional
        educational.add_value('language', 'de')
        lom.add_value('educational', educational.load_item())

        # once you've filled "general", "technical", "lifecycle" and "educational" with values,
        # the LomBaseItem is loaded into the "base"-BaseItemLoader
        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()
        # for possible values, either consult https://vocabs.openeduhub.de
        # or take a look at https://github.com/openeduhub/oeh-metadata-vocabs
        # TODO: fill "valuespaces"-keys with values for
        #  - discipline                     recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/discipline.ttl)
        #  - intendedEndUserRole            recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/intendedEndUserRole.ttl)
        #  - learningResourceType           recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/learningResourceType.ttl)
        #  - conditionsOfAccess             recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/conditionsOfAccess.ttl)
        #  - containsAdvertisement          recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/containsAdvertisement.ttl)
        #  - price                          recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/price.ttl)
        #  - educationalContext             optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/educationalContext.ttl)
        #  - sourceContentType              optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/sourceContentType.ttl)
        #  - toolCategory                   optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/toolCategory.ttl)
        #  - accessibilitySummary           optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/accessibilitySummary.ttl)
        #  - dataProtectionConformity       optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/dataProtectionConformity.ttl)
        #  - fskRating                      optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/fskRating.ttl)
        #  - oer                            optional
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/oer.ttl)
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
        # TODO: fill "license"-keys with values for
        #  - oer                            recommended ('oer' is automatically set if the 'url'-field above
        #  is recognized in LICENSE_MAPPINGS: for possible url-mapping values, please take a look at
        #  LICENSE_MAPPINGS in converter/constants.py)
        #  - author                         recommended
        #  - internal                       optional
        #  - expirationDate                 optional (for content that expires, e.g. ÖR-Mediatheken)
        license_url = response.xpath('//div[@class="cc-licence-info"]/p/a[@rel="license"]/@href').get()
        if license_url is not None:
            lic.add_value('url', license_url)

        license_description_raw = response.xpath('//div[@class="cc-licence-info"]').get()
        if license_description_raw is not None:
            license_description_raw = w3lib.html.remove_tags(license_description_raw)
            license_description_raw = w3lib.html.replace_escape_chars(license_description_raw, which_ones="\n",
                                                                      replace_by=" ")
            license_description_raw = w3lib.html.replace_escape_chars(license_description_raw)
            license_description = " ".join(license_description_raw.split())
            lic.add_value('description', license_description)
        base.add_value('license', lic.load_item())

        # Either fill the PermissionItemLoader manually (not necessary most of the times)
        permissions = PermissionItemLoader()
        # or (preferably) call the inherited getPermissions(response)-method
        #   from converter/spiders/base_classes/lom_base.py by using super().:
        # permissions = super().getPermissions(response)
        # TODO: if necessary, add/replace values for the following "permissions"-keys
        #  - public                         optional
        #  - groups                         optional
        #  - mediacenters                   optional
        #  - autoCreateGroups               optional
        #  - autoCreateMediacenters         optional
        base.add_value('permissions', permissions.load_item())

        # Either fill the ResponseItemLoader manually (not necessary most of the time)
        # response_loader = ResponseItemLoader()
        # or (preferably) call the inherited mapResponse(response)-method
        #   from converter/spiders/base_classes/lom_base.py by using super().:
        response_loader = super().mapResponse(response)
        # TODO: if necessary, add/replace values for the following "response"-keys
        #  - url                            required
        #  - status                         optional
        #  - html                           optional
        #  - text                           optional
        #  - headers                        optional
        #  - cookies                        optional
        #  - har                            optional
        base.add_value('response', response_loader.load_item())

        # once all scrapy.Item are loaded into our "base", we yield the BaseItem by calling the .load_item() method
        yield base.load_item()
