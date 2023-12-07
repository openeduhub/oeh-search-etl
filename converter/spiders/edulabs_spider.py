import datetime
import json

import scrapy
import w3lib.html

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, LomClassificationItemLoader, ValuespaceItemLoader, \
    LicenseItemLoader, ResponseItemLoader
from converter.spiders.base_classes import LomBase


class EdulabsSpider(scrapy.Spider, LomBase):
    name = "edulabs_spider"
    start_urls = ["https://edulabs.de/oer/"]
    friendlyName = "edulabs"
    version = "0.0.1"
    allowed_domains = ["edulabs.de"]

    MAPPING_DISCIPLINES = {
        "Erdkunde/Geografie": "Erdkunde",
        "Mathe": "Mathematik",
        "Sachkunde": "Sachunterricht",
        "SoWi": "Social education",
    }
    MAPPING_EDUCATIONAL_CONTEXT = {
        "KITA/VORSCHULE": "Elementarbereich",
        "GRUNDSTUFE (1-3)": "Primarstufe",
        "SEKUNDARSTUFE 1": "Sekundarstufe 1",
        "SEKUNDARSTUFE 2": "Sekundarstufe 2"
    }

    def start_requests(self) -> scrapy.Request:
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse_overview)

    def parse_overview(self, response: scrapy.http.Response) -> scrapy.Request:
        """

        :param response: scrapy.http.Response
        :return: scrapy.Request

        Scrapy Contracts:
        @url https://edulabs.de/oer/
        @returns requests 48
        """
        url_list = response.xpath('//a[@class="teaser-inner"]/@href').getall()
        for url in url_list:
            # ToDo: "/blog/"-entries have a different structure than materials
            yield response.follow(url=url, callback=self.parse)

    def getId(self, response=None) -> str:
        pass

    def getHash(self, response=None) -> str:
        pass

    async def parse(self, response: scrapy.http.Response, **kwargs) -> BaseItemLoader:
        """

        Scrapy Contracts:
        @url https://edulabs.de/oer/30utp/
        @returns item 1
        """
        disciplines = list()
        educational_context = list()
        keywords = list()
        typical_learning_time = list()
        digital_competencies: list = response.xpath('//h4[@class="filter-items-headline"][contains(text(),"DIGITALE '
                                                    'KOMPETENZEN")]/following-sibling::div/div/text()').getall()

        target_age_group: list = response.xpath('//div[@class="col-xs-24 col-md-12 edusprint-zielgruppe '
                                                'edusprint-grey filter-items"]/div/a/span/text()').getall()
        if target_age_group:
            # mapping "Zielgruppe" from edulabs to educational_context
            for potential_educontext in target_age_group:
                if potential_educontext.startswith("GRUNDSTUFE"):
                    keywords.append(potential_educontext)
                if potential_educontext in self.MAPPING_EDUCATIONAL_CONTEXT:
                    educontext_mapped = self.MAPPING_EDUCATIONAL_CONTEXT.get(potential_educontext)
                    educational_context.append(educontext_mapped)

        school_subject_groups: list = response.xpath('//h4[@class="filter-items-headline"][contains(text(),'
                                                     '"FÄCHERGRUPPEN")]/following-sibling::div/div/text()').getall()
        if school_subject_groups:
            # school subject groups are different from the individual disciplines, but still useful information that we
            # can use as additional keywords
            keywords.extend(school_subject_groups)

        school_subjects: list = response.xpath('//h4[@class="filter-items-headline"][contains(text(),'
                                               '"FACH")]/following-sibling::div/div/text()').getall()
        if school_subjects:
            for school_subject in school_subjects:
                if school_subject in self.MAPPING_DISCIPLINES:
                    if "SoWi" in school_subject:
                        keywords.append(school_subject)
                    subject_temp = self.MAPPING_DISCIPLINES.get(school_subject)
                    disciplines.append(subject_temp)
                else:
                    disciplines.append(school_subject)
        if disciplines:
            pass

        time_required: list = response.xpath('//h4[@class="filter-items-headline"][contains(text(),'
                                             '"ZEITBEDARF")]/following-sibling::div/a/span/text()').getall()
        if time_required:
            # there can be up to three "time required"-values per crawled item
            # our pipeline expects only one value (in seconds), though, which is why we need to prioritize which value
            # should actually be saved as typical_learning_time: the longest or shortest duration?
            for time_item in time_required:
                if "DOPPELSTUNDE" in time_item:
                    time_string = str(datetime.timedelta(minutes=90))
                    typical_learning_time.append(time_string)
                if "45 MINUTEN" in time_item:
                    time_string = str(datetime.timedelta(minutes=45))
                    typical_learning_time.append(time_string)
                if "ÜBUNG" in time_item:
                    # exercises are typically < 20 minutes
                    time_string = str(datetime.timedelta(minutes=20))
                    typical_learning_time.append(time_string)
        if typical_learning_time:
            typical_learning_time.sort()
            # we're using the longest duration of all available learning times
            typical_learning_time = typical_learning_time.pop()

        json_ld = str()
        if "/mkifa/" in response.url or "/tnh8i/" in response.url or "/p78kq/" in response.url:
            # there are exactly 3 materials that have malformed "json+ld"-containers which would cause errors
            # we skip trying to parse these containers and use fallback metadata instead
            pass
        else:
            json_ld: str = response.xpath('//script[@type="application/ld+json"]/text()').get()
            json_ld: dict = json.loads(json_ld)

        # og_type: str = response.xpath('//head/meta[@property="og:type"]/@content').get()
        date_published: str = response.xpath('//head/meta[@property="article:published_time"]/@content').get()

        language: str = response.xpath('//head/meta[@property="og:locale"]/@content').get()

        # building our BaseItem by filling up the BaseItemLoader starts here:
        base: BaseItemLoader = BaseItemLoader()

        base.add_value('sourceId', response.url)
        hash_temp: str = f"{date_published}v{self.version}"
        base.add_value('hash', hash_temp)
        if "dateModified" in json_ld:
            date_modified: str = json_ld.get("dateModified")
            if date_modified:
                base.add_value('lastModified', date_modified)
        lom: LomBaseItemloader = LomBaseItemloader()

        general = LomGeneralItemloader()
        general.add_value('identifier', response.url)
        title: str = response.xpath('//head/meta[@property="og:title"]/@content').get()
        if title:
            general.add_value('title', title)
        if keywords:
            general.add_value('keyword', keywords)
        description: str = response.xpath('//head/meta[@property="og:description"]/@content').get()
        if description:
            general.add_value('description', description)
        if language:
            general.add_value('language', language)
        lom.add_value('general', general.load_item())

        technical: LomTechnicalItemLoader = LomTechnicalItemLoader()
        technical.add_value('format', 'text/html')
        technical.add_value('location', response.url)
        media_required: list = response.xpath('//h4[@class="filter-items-headline"][contains(text(),'
                                              '"MEDIENEINSATZ")]/following-sibling::div/a/span/text()').getall()
        if media_required:
            technical.add_value('requirement', str(media_required))
        # noinspection DuplicatedCode
        lom.add_value('technical', technical.load_item())

        lifecycle: LomLifecycleItemloader = LomLifecycleItemloader()
        lifecycle.add_value('role', 'publisher')  # supported roles: "author" / "editor" / "publisher"
        author_edulabs: str = response.xpath('//head/meta[@name="author"]/@content').get()
        if author_edulabs:
            lifecycle.add_value('organization', author_edulabs)
        if date_published:
            lifecycle.add_value('date', date_published)
        # noinspection DuplicatedCode
        lom.add_value('lifecycle', lifecycle.load_item())

        educational = LomEducationalItemLoader()
        if language:
            educational.add_value('language', language)
        if typical_learning_time:
            educational.add_value('typicalLearningTime', typical_learning_time)
        lom.add_value('educational', educational.load_item())

        classification: LomClassificationItemLoader = LomClassificationItemLoader()
        if digital_competencies:
            classification.add_value('description', str(digital_competencies))
        lom.add_value('classification', classification.load_item())

        # once you've filled "general", "technical", "lifecycle" and "educational" with values,
        # the LomBaseItem is loaded into the "base"-BaseItemLoader
        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value('conditionsOfAccess', 'no login')
        vs.add_value('containsAdvertisement', 'No')
        vs.add_value('dataProtectionConformity', 'generalDataProtectionRegulation')
        if disciplines:
            vs.add_value('discipline', disciplines)
        if educational_context:
            vs.add_value('educationalContext', educational_context)
        vs.add_value('intendedEndUserRole', 'teacher')
        vs.add_value('new_lrt', 'd8c3ef03-b3ab-4a5e-bcc9-5a546fefa2e9')  # Webseite und Portal (stabil)
        # by default, every item is considered to be a web-page; some materials have additional identifiers that can be
        # used for the 'new_lrt'-value
        if "UNTERRICHTSREIHE" in time_required:
            vs.add_value('new_lrt', '962560fe-d8d0-43e2-ad60-97f070b935c6')  # Unterrichtsreihe
        if "/blog/" in response.url:
            vs.add_value('new_lrt', ['5204fc81-5dac-4cc4-a28b-aad5c241fa19', 'b98c0c8c-5696-4537-82fa-dded7236081e'])
            # "Webblog (dynamisch)", "Artikel"
        vs.add_value('price', 'no')
        base.add_value('valuespaces', vs.load_item())

        license_loader: LicenseItemLoader = LicenseItemLoader()
        if json_ld:
            if "author" in json_ld.keys():
                author_name = json_ld.get("author")
                if author_name:
                    license_loader.add_value('author', author_name)
        else:
            author_name_fallback = response.xpath('//div[@class="edusprint-author-row"]'
                                                  '//*[@class="author-name"]/text()').getall()
            license_loader.add_value('author', author_name_fallback)
        license_default = Constants.LICENSE_CC_BY_SA_40
        license_url: str = response.xpath('//a[@rel="license"]/@href').get()
        if license_url:
            if license_url.startswith('http://'):
                license_url = license_url.replace('http://', "https://")
            license_loader.add_value('url', license_url)
            if license_url.endswith("/cc0/"):
                license_loader.add_value('internal', Constants.LICENSE_CC_ZERO_10)
                license_loader.replace_value('url', Constants.LICENSE_CC_ZERO_10)
        else:
            # edulabs.de footer: "Inhalte dieser Webseite sind, sofern nicht anders angegeben, nach Creative Commons 4.0
            # Attribution lizenziert." - we're  using this string as a license description fallback
            license_loader.add_value('url', license_default)
            license_description_clean: list = list()
            license_description: list = response.xpath('//li[@class="cc-info"]//text()').getall()
            if license_description:
                for temp_str in license_description:
                    temp = w3lib.html.strip_html5_whitespace(temp_str)
                    license_description_clean.append(temp)
                license_description_clean: str = str(license_description)
                license_loader.add_value('description', license_description_clean)
        # noinspection DuplicatedCode
        base.add_value('license', license_loader.load_item())

        permissions = super().getPermissions(response)
        base.add_value('permissions', permissions.load_item())

        response_loader: ResponseItemLoader = await super().mapResponse(response)
        base.add_value('response', response_loader.load_item())

        yield base.load_item()
