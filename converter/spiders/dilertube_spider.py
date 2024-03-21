import logging
import re
from datetime import datetime

import scrapy
import w3lib.html
from scrapy.spiders import CrawlSpider

from converter.items import (
    BaseItemLoader,
    LomBaseItemloader,
    LomGeneralItemloader,
    LomTechnicalItemLoader,
    LomLifecycleItemloader,
    LomEducationalItemLoader,
    LomClassificationItemLoader,
    ValuespaceItemLoader,
    LicenseItemLoader,
    ResponseItemLoader,
    PermissionItemLoader,
)
from converter.spiders.base_classes import LomBase
from converter.util.license_mapper import LicenseMapper
from converter.util.sitemap import from_xml_response
from converter.web_tools import WebEngine

logger = logging.getLogger(__name__)


class DiLerTubeSpider(CrawlSpider, LomBase):
    name = "dilertube_spider"
    friendlyName = "DiLerTube"
    start_urls = ["https://www.dilertube.de/sitemap.xml"]
    version = "0.0.5"  # last update: 2024-03-21
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 4,
        "WEB_TOOLS": WebEngine.Playwright,
    }

    DISCIPLINE_MAPPING = {
        "Alltagskultur, Ernährung, Soziales (AES)": "04006",  # "Ernährung und Hauswirtschaft"
        # ToDo: AES discipline exists since 2016 in BaWü, probably needs its own entry in the "disciplines.ttl"-Vocab
        "Berufsorientierung": "040",  # "Berufliche Bildung"
        "Bildende Kunst": "060",  # Kunst
        "Gemeinschaftskunde": "48005",  # Gesellschaftskunde / Sozialkunde
        "Geographie": "220",  # Geografie  # ToDo: remove this temporary mapping as soon as the vocabs are updated
        "Gesundheit und Soziales (GuS)": "260",  # Gesundheit
        "Informatik & Medienbildung": ["320", "900"],  # Informatik; Medienbildung
        "Lateinisch": "20005",  # Latein
        # "Materie Natur Technik (MNT)": "",  # ToDo: cannot be mapped
        "Technik": "020",  # Arbeitslehre
    }
    CATEGORY_IS_ACTUALLY_A_KEYWORD = [
        "DiLer Tutorials",
        "Führerscheine",
        "Imagefilme von Schulen",
        "Kanäle",
        "Methoden",
        "Naturphänomene",
        "Sonstige",
        "Schülerprojekte",
    ]

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self) -> scrapy.Request:
        """

        :return: scrapy.Request

        Scrapy Contracts:
        @url https://www.dilertube.de/sitemap.xml
        @returns item 1
        """
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse_sitemap)

    def parse_sitemap(self, response) -> scrapy.Request:
        """
        Iterates through the sitemap and yields a scrapy.Request for every url found inside a <loc>-element.
        :param response:
        :return: scrapy.Request

        Scrapy Contracts:
        @url https://www.dilertube.de/sitemap.xml
        @returns requests 30
        """
        sitemap_items = from_xml_response(response)
        # the sitemap contains the urls to all video categories (currently: 37); a single sitemap_item looks like this:
        # <url>
        # 		<loc>https://www.dilertube.de/bildende-kunst.html</loc>
        # 		<changefreq>weekly</changefreq>
        # 		<priority>0.5</priority>
        # 	</url>
        for sitemap_item in sitemap_items:
            yield scrapy.Request(url=sitemap_item.loc, callback=self.parse_video_overview, priority=1)

    def parse_video_overview(self, response) -> scrapy.Request:
        """
        Gathers individual video urls from a category overview (e.g. "Englisch") and yields individual video_urls to the
        parse()-method.
        :param response:
        :return: a scrapy.Request for every available video_url

        Scrapy Contracts:
        @url https://wwww.dilertube.de/bildende-kunst.html
        @returns requests 13
        """
        url_list = response.xpath('//*[@class="card-title m-0 mb-2"]/a/@href').getall()
        # the individual links from the video-overview look like this:
        # '/bildende-kunst/oer-video/kudivi-geschichte-der-kunstpaedagogik-03-bauhaus.html'

        for url in url_list:
            video_url: str = str("https://www.dilertube.de" + url)
            yield scrapy.Request(url=video_url, callback=self.parse)

    def getId(self, response=None) -> str:
        return response.url

    def getHash(self, response=None) -> str:
        date_str: str = self.get_published_date_from_dom(response=response)
        hash_str: str = f"{date_str}v{self.version}"
        return hash_str

    @staticmethod
    def get_published_date_from_dom(response: scrapy.http.Response) -> str:
        """
        Try to parse the published date directly from the DOM and return it as a string.
        If no "veröffentlicht am"-date is found in the DOM, build a date string from datetime now as a fallback.

        :param response: scrapy.http.Response
        :return: a string containing the published date or the current time
        """
        date_string_raw, date_string = str(), str()
        date_regex: re.Pattern = re.compile(r"((?P<day>\d{2})\.)?" r"((?<=\.)(?P<month>\d{2})\.)?" r"(?P<year>\d{4})")
        channel_info_box: list[str] = response.xpath('//div[@class="jv-channel"]/small/text()').getall()
        for channel_info_item in channel_info_box:
            if "Veröffentlicht am" in channel_info_item:
                date_string_raw: str = channel_info_item
        if date_string_raw and isinstance(date_string_raw, str):
            date_string_raw = w3lib.html.strip_html5_whitespace(date_string_raw)
            if date_regex.search(date_string_raw):
                date_string = date_regex.search(date_string_raw).group()
        if date_string and isinstance(date_string, str):
            # ToDo RegEx distinction between Year-only and proper dates
            date_parsed: datetime = datetime.strptime(date_string, "%d.%m.%Y")
            if date_parsed:
                date_string = date_parsed.isoformat()
            else:
                # fallback value: current time (in case we can't gather the published_date ("Veröffentlicht am: ...")
                # from the DOM)
                date_string = datetime.now().isoformat()
        published_date = date_string
        return published_date

    async def parse(self, response: scrapy.http.Response, **kwargs) -> BaseItemLoader:
        """
        Gathers metadata from a video-url, nests the metadata within a BaseItemLoader and yields a complete BaseItem by
        calling the .load_item()-method.
        :param response: scrapy.http.Response
        :param kwargs:
        :return: yields a converter.items.BaseItem by calling the ".load_item()"-method on its scrapy.ItemLoader

        Scrapy Contracts:
        @url https://www.dilertube.de/ethik/oer-video/solidaritaet.html
        @returns item 1
        """
        if self.shouldImport(response) is False:
            logger.info(f"Skipping item {self.getId(response)} because shouldImport() returned False.")
            return
        if self.getId(response) is not None and self.getHash(response) is not None:
            if not self.hasChanged(response):
                return

        # Below a video, these possible metadata fields might be available in the video-information-box:
        # "Lizenz"                                  always?         (freeform text, set by the video-uploader)
        # "Autor"                                   optional        (freeform text)
        # "Quelle"                                  optional        (= the original source of the video, freeform text)
        # "Produktionsjahr des Videos (ca.)"        optional        (year, e.g. "2020")
        # "Produktionsdatum"                        optional        (date, e.g. "09.03.2021")
        license_description_raw: str = response.xpath('//div[@class="customFieldValue license"]/text()').get()
        video_info_dict = dict()
        if license_description_raw and isinstance(license_description_raw, str):
            license_description: str = w3lib.html.strip_html5_whitespace(license_description_raw)
            video_info_dict.update({"license_description": license_description})
            if license_description and isinstance(license_description, str):
                # a typical license description string might look like this:
                # 'Creative Commons (CC) BY-NC-ND Namensnennung-Nicht kommerziell-Keine Bearbeitungen 4.0 International'
                cc_pattern: re.Pattern = re.compile(
                    r"\((?P<CC>C{2})\)\s" r"(?P<CC_TYPE>\D{2}(-\D{2})*)" r".*" r"(?<=\s)(?P<CC_VERSION>\d\.\d)?(?=\s)"
                )
                license_mapper = LicenseMapper()
                if cc_pattern.search(license_description):
                    # the LicenseMapper does not recognize this string yet, which is why we need to trim it down in the
                    # crawler first and then let the LicenseMapper do the rest
                    cc_pattern_result_dict = cc_pattern.search(license_description).groupdict()
                    cc_string_prepared_for_mapping: str = (
                        f"{cc_pattern_result_dict.get('CC')} "
                        f"{cc_pattern_result_dict.get('CC_TYPE')} "
                        f"{cc_pattern_result_dict.get('CC_VERSION')}"
                    )
                    mapped_license_url: str | None = license_mapper.get_license_url(cc_string_prepared_for_mapping)
                    if mapped_license_url:
                        video_info_dict.update({"cc_url": mapped_license_url})
                else:
                    # fallback to string recognition by our license mapper for edge-cases where the above RegEx fails
                    # e.g. "Creative Commons (CC) CC0 gemeinfrei (public domain - no rights reserved)"
                    license_internal_mapped = license_mapper.get_license_internal_key(license_description)
                    if license_internal_mapped:
                        video_info_dict.update({"license_internal": license_internal_mapped})

        video_info_box: list[str] = response.xpath(
            '//ul[@class="list-group mx-0 my-0"]//div[@class="card-body"]/div[@class="mb-2"]'
        ).getall()
        for video_info_field in video_info_box:
            selector_item = scrapy.Selector(text=video_info_field)
            video_info_field_description = selector_item.xpath('//h4[@class="customFieldLabel "]/text()').get()
            # the class-name "customFieldLabel " needs to come with that trailing whitespace! this is NOT A TYPO!
            if video_info_field_description:
                if "Autor" in video_info_field_description:
                    author_string: str = selector_item.xpath('//div[@class="customFieldValue "]/text()').get()
                    if author_string:
                        author_string = w3lib.html.strip_html5_whitespace(author_string)
                        video_info_dict.update({"author": author_string})
                if "Quelle" in video_info_field_description:
                    source_string: str = selector_item.xpath('//div[@class="customFieldValue "]/text()').get()
                    if source_string:
                        source_string = w3lib.html.strip_html5_whitespace(source_string)
                        video_info_dict.update({"source": source_string})
                if "Produktionsjahr" in video_info_field_description:
                    production_year: str = selector_item.xpath('//div[@class="customFieldValue "]/text()').get()
                    if production_year:
                        production_year = w3lib.html.strip_html5_whitespace(production_year)
                        video_info_dict.update({"production_year": production_year})
                if "Produktionsdatum" in video_info_field_description:
                    production_date: str = selector_item.xpath('//div[@class="customFieldValue "]/text()').get()
                    if production_date:
                        production_date = w3lib.html.strip_html5_whitespace(production_date)
                        video_info_dict.update({"production_date": production_date})

        base: BaseItemLoader = BaseItemLoader()
        base.add_value("sourceId", self.getId(response=response))
        base.add_value("hash", self.getHash(response=response))
        thumbnail_url: str = response.xpath('//meta[@property="og:image"]/@content').get()
        if thumbnail_url and isinstance(thumbnail_url, str):
            base.add_value("thumbnail", thumbnail_url)

        categories = list()
        keywords = list()
        categories_and_keywords_list: list[str] = response.xpath(
            '//ul[@class="list-group mx-0 my-0"]/li[' '@class="list-group-item"]'
        ).getall()
        # categories and keywords both use the same generic class names for its elements, therefore we try to identify
        # the description-text and use its <a href>-siblings to extract the text-values:
        if categories_and_keywords_list and isinstance(categories_and_keywords_list, list):
            for category_or_keyword_item in categories_and_keywords_list:
                selector_item = scrapy.Selector(text=category_or_keyword_item)
                category_or_keyword_description = selector_item.xpath('//span[@class="title"]/text()').get()
                if "Kategorie" in category_or_keyword_description:
                    categories_raw = selector_item.xpath('//a[@class="badge-primary badge-pill"]/text()').getall()
                    if categories_raw and isinstance(categories_raw, list) and len(categories_raw) >= 1:
                        for category_potential_candidate in categories_raw:
                            if category_potential_candidate.startswith("||| "):
                                # there are some categories which are not school-disciplines but rather keywords
                                # e.g. "||| Methoden": https://www.dilertube.de/sonstige/oer-videos/methoden.html
                                category_potential_candidate: str = category_potential_candidate.replace("||| ", "")
                            if category_potential_candidate in self.CATEGORY_IS_ACTUALLY_A_KEYWORD:
                                keywords.append(category_potential_candidate)
                            else:
                                categories.append(category_potential_candidate)
                if "Schlagwörter" in category_or_keyword_description:
                    keywords_raw: list[str] = selector_item.xpath(
                        '//a[@class="badge-primary badge-pill"]/text()'
                    ).getall()
                    if keywords_raw and isinstance(keywords_raw, list) and len(keywords_raw) >= 1:
                        keywords.extend(keywords_raw)

        lom: LomBaseItemloader = LomBaseItemloader()

        general: LomGeneralItemloader = LomGeneralItemloader()
        general.add_value("identifier", response.url)
        general.add_value("title", response.xpath('//meta[@property="og:title"]/@content').get())
        general.add_value("description", response.xpath('//meta[@property="og:description"]/@content').get())
        general.add_value("language", response.xpath("/html/@lang").get())
        # grabs the language from the html language; there seem to be additional translations of DiLerTube in the works:
        # the german URLs use 'de-DE' by default,
        # while the english translations use 'en-GB', so this looks like a suitable indicator
        general.add_value("keyword", keywords)
        lom.add_value("general", general.load_item())

        technical: LomTechnicalItemLoader = LomTechnicalItemLoader()
        technical.add_value("format", "text/html")
        technical.add_value("location", response.url)
        lom.add_value("technical", technical.load_item())

        date_production_year: str | None = None
        date_of_production: str | None = None
        if "production_year" in video_info_dict:
            # this is a necessary workaround because dateparser.parse() would mis-calculate year-only representations of
            # the date
            dt_production_year: datetime = datetime.strptime(video_info_dict.get("production_year"), "%Y")
            date_production_year: str = dt_production_year.isoformat()
        if "production_date" in video_info_dict:
            # this is a necessary workaround because dateparser.parse() would confuse de-DE time-formats as en-US
            dt_production_date: datetime = datetime.strptime(video_info_dict.get("production_date"), "%d.%m.%Y")
            date_of_production: str = dt_production_date.isoformat()

        if "source" in video_info_dict:
            lifecycle_publisher: LomLifecycleItemloader = LomLifecycleItemloader()
            lifecycle_publisher.add_value("role", "publisher")
            lifecycle_publisher.add_value("organization", video_info_dict.get("source"))
            if date_of_production:
                lifecycle_publisher.add_value("date", date_of_production)
            elif date_production_year:
                lifecycle_publisher.add_value("date", date_production_year)
            lom.add_value("lifecycle", lifecycle_publisher.load_item())

        if "author" in video_info_dict:
            lifecycle_author: LomLifecycleItemloader = LomLifecycleItemloader()
            lifecycle_author.add_value("role", "author")
            lifecycle_author.add_value("firstName", video_info_dict.get("author"))
            # dumping the whole author string into "firstName" is a temporary solution so we don't lose author metadata
            # ToDo (optional):
            #  - refine author information by splitting author names into firstName and lastName?
            if date_of_production:
                lifecycle_author.add_value("date", date_of_production)
            elif date_production_year:
                lifecycle_author.add_value("date", date_production_year)
            lom.add_value("lifecycle", lifecycle_author.load_item())

        educational: LomEducationalItemLoader = LomEducationalItemLoader()
        lom.add_value("educational", educational.load_item())

        classification: LomClassificationItemLoader = LomClassificationItemLoader()
        lom.add_value("classification", classification.load_item())

        base.add_value("lom", lom.load_item())

        vs: ValuespaceItemLoader = ValuespaceItemLoader()
        if keywords and isinstance(keywords, list):
            # the complete list of keywords (called "tags" on DiLerTube) can be seen here:
            # https://www.dilertube.de/component/tags/
            # (attention: DiLerTube tags are freetext strings that can be set by the individual video uploader)
            keywords_lc: list[str] = [kw.lower() for kw in keywords]
            # first, we need to cast keywords to lowercase to make mapping individual parts of a string more robust
            for keyword_lowercase in keywords_lc:
                if "grundschule" in keyword_lowercase:
                    vs.add_value("educationalContext", "grundschule")
                if "erklärvideo" in keyword_lowercase:
                    vs.add_value("new_lrt", "a0218a48-a008-4975-a62a-27b1a83d454f")  # Erklärvideo und
                    # gefilmtes Experiment
        for category_item in categories:
            if category_item in self.DISCIPLINE_MAPPING.keys():
                discipline_mapped: str | list[str] = self.DISCIPLINE_MAPPING.get(category_item)
                if isinstance(discipline_mapped, list):
                    for discipline in discipline_mapped:
                        vs.add_value("discipline", discipline)
                if isinstance(discipline_mapped, str):
                    vs.add_value("discipline", discipline_mapped)
            else:
                vs.add_value("discipline", category_item)
        vs.add_value("new_lrt", "7a6e9608-2554-4981-95dc-47ab9ba924de")  # Video (Material)
        vs.add_value("intendedEndUserRole", ["learner", "teacher"])
        vs.add_value("conditionsOfAccess", "no_login")
        vs.add_value("containsAdvertisement", "no")
        vs.add_value("dataProtectionConformity", "generalDataProtectionRegulation")  # Datensparsam
        # see https://www.dilertube.de/datenschutz.html
        vs.add_value("price", "no")
        base.add_value("valuespaces", vs.load_item())

        lic: LicenseItemLoader = LicenseItemLoader()
        if "license_description" in video_info_dict:
            # DiLerTube allows the uploaders to enter freeform text into the license field
            lic.add_value("description", video_info_dict.get("license_description"))
            if "cc_url" in video_info_dict:
                lic.add_value("url", video_info_dict.get("cc_url"))
            elif "license_internal" in video_info_dict:
                # fallback for edge-cases when no CC license could be parsed
                lic.add_value("internal", video_info_dict.get("license_internal"))
        if "author" in video_info_dict:
            lic.add_value("author", video_info_dict.get("author"))
        base.add_value("license", lic.load_item())

        permissions: PermissionItemLoader = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader: ResponseItemLoader = await super().mapResponse(response, fetchData=False)
        base.add_value("response", response_loader.load_item())

        yield base.load_item()
