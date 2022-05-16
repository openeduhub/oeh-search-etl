import re
from datetime import datetime

import scrapy
import w3lib.html
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, LomClassificationItemLoader, ValuespaceItemLoader, \
    LicenseItemLoader
from converter.spiders.base_classes import LomBase
from converter.util.sitemap import from_xml_response


class DiLerTubeSpider(CrawlSpider, LomBase):
    name = "dilertube_spider"
    friendlyName = "DiLerTube"
    start_urls = ["https://www.dilertube.de/sitemap.xml"]
    version = "0.0.1"  # last update: 2022-05-16
    custom_settings = {
        "ROBOTSTXT_OBEY": False
    }

    # debug_video_url_set = set()

    LICENSE_MAPPING = {
        "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0",
        "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0",
        "CC BY-ND 4.0": "https://creativecommons.org/licenses/by-nd/4.0",
        "CC BY-NC 4.0": "https://creativecommons.org/licenses/by-nc/4.0",
        "CC BY-NC-SA 4.0": "https://creativecommons.org/licenses/by-nc-sa/4.0",
        "CC BY-NC-ND 4.0": "https://creativecommons.org/licenses/by-nc-nd/4.0"
    }
    # ToDo: we're missing several licenses in converter.Constants (either keep using this mapping or update Constants)
    DISCIPLINE_MAPPING = {
        "Alltagskultur, Ernährung, Soziales (AES)": "Ernährung und Hauswirtschaft",
        # ToDo: AES discipline exists since 2016 in BaWü, probably needs its own entry in the "disciplines.ttl"-Vocab
        "Berufsorientierung": "Berufliche Bildung",
        "Bildende Kunst": "Kunst",
        # "Biologie": "Biologie",
        # "Chemie": "Chemie",
        # "Deutsch": "Deutsch",
        # "Englisch": "Englisch",
        "Ethik": "Ethik",
        # "Französisch": "Französisch",
        "Gemeinschaftskunde": "",
        "Geographie": "Geografie",
        # "Geschichte": "Geschichte",
        "Gesundheit und Soziales": "",
        "Informatik und Medienbildung": "",
        "Lateinisch": "Latein",
        "Materie Natur Technik (MNT)": "",
        # "Mathematik": "Mathematik",
        # "Musik": "Musik",
        # "Pädagogik": "Pädagogik",
        # "Philosophie": "Philosophie",
        # "Religion": "Religion",
        # "Sachunterricht": "Sachunterricht",
        # "Spanisch": "Spanisch",
        # "Sport": "Sport",
        "Technik": "Arbeitslehre",
        # "Wirtschaftskunde": "Wirtschaftskunde",
    }
    CATEGORY_IS_ACTUALLY_A_KEYWORD = [
        "DiLer Tutorials", "Führerscheine", "Imagefilme von Schulen", "Kanäle", "Methoden", "Naturphänomene",
        "Sonstige", "Schülerprojekte", "Technik"
    ]

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
            yield scrapy.Request(url=sitemap_item.loc, callback=self.parse_video_overview)

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

        # logging.debug(f"Video-links from {response.url}: \n {url_list}")
        for url in url_list:
            video_url: str = str("https://www.dilertube.de" + url)
            # self.debug_video_url_set.add(video_url)
            yield scrapy.Request(url=video_url, callback=self.parse)

    def getId(self, response=None) -> str:
        pass

    def getHash(self, response=None) -> str:
        pass

    def parse(self, response: scrapy.http.Response, **kwargs) -> BaseItemLoader:
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
        date_string_raw, date_string = str(), str()
        date_regex = re.compile(r'((?P<day>\d{2})\.)?'
                                r'((?<=\.)(?P<month>\d{2})\.)?'
                                r'(?P<year>\d{4})')
        channel_info_box: list = response.xpath('//div[@class="jv-channel"]/small/text()').getall()
        for channel_info_item in channel_info_box:
            if "Veröffentlicht am" in channel_info_item:
                date_string_raw: str = channel_info_item
        if date_string_raw is not None:
            date_string_raw = w3lib.html.strip_html5_whitespace(date_string_raw)
            if date_regex.search(date_string_raw):
                date_string = date_regex.search(date_string_raw).group()
        if date_string is not None:
            # ToDo RegEx discerning between Year-only and proper dates
            date_parsed: datetime = datetime.strptime(date_string, "%d.%m.%Y")
            if date_parsed is not None:
                date_string = date_parsed.isoformat()
            else:
                # fallback value: current time (in case we can't gather the published_date ("Veröffentlicht am: ...")
                # from the DOM)
                date_string = datetime.now().isoformat()
        published_date = date_string

        # Below a video, these possible metadata fields might be available in the video-information-box:
        # "Lizenz"                                  always?         (freeform text, set by the video-uploader)
        # "Autor"                                   optional        (freeform text)
        # "Quelle"                                  optional        (= the original source of the video, freeform text)
        # "Produktionsjahr des Videos (ca.)"        optional        (year, e.g. "2020")
        # "Produktionsdatum"                        optional        (date, e.g. "09.03.2021")
        license_description_raw = response.xpath('//div[@class="customFieldValue license"]/text()').get()
        video_info_dict = dict()
        if license_description_raw is not None:
            license_description = w3lib.html.strip_html5_whitespace(license_description_raw)
            video_info_dict.update({'license_description': license_description})
            if license_description is not None:
                cc_pattern = re.compile(r'\((?P<CC>C{2})\)\s'
                                        r'(?P<CC_TYPE>\D{2}(-\D{2})*)'
                                        r'.*'
                                        r'(?<=\s)(?P<CC_VERSION>\d\.\d)?(?=\s)'
                                        )
                if cc_pattern.search(license_description) is not None:
                    cc_pattern_result_dict = cc_pattern.search(license_description).groupdict()
                    # cc_string_ready_for_mapping = str(cc_pattern_result_dict.get("CC") + "_"
                    #                                   + cc_pattern_result_dict.get("CC_TYPE").replace("-", "_") + "_"
                    #                                   + cc_pattern_result_dict.get("CC_VERSION").replace(".", ""))
                    # ToDo map license url with converter.Constants instead? (some licenses are missing there)
                    cc_string = str(cc_pattern_result_dict.get("CC") + " " + cc_pattern_result_dict.get("CC_TYPE")
                                    + " " + cc_pattern_result_dict.get("CC_VERSION"))
                    if cc_string in self.LICENSE_MAPPING.keys():
                        cc_url = self.LICENSE_MAPPING.get(cc_string)
                        video_info_dict.update({'cc_url': cc_url})

        video_info_box = \
            response.xpath('//ul[@class="list-group mx-0 my-0"]//div[@class="card-body"]/div[@class="mb-2"]').getall()
        for video_info_field in video_info_box:
            selector_item = scrapy.Selector(text=video_info_field)
            video_info_field_description = selector_item.xpath('//h4[@class="customFieldLabel "]/text()').get()
            # the class-name "customFieldLabel " needs to come with that trailing whitespace! this is NOT A TYPO!
            if video_info_field_description is not None:
                if "Autor" in video_info_field_description:
                    author_string = selector_item.xpath('//div[@class="customFieldValue "]/text()').get()
                    if author_string is not None:
                        author_string = w3lib.html.strip_html5_whitespace(author_string)
                        video_info_dict.update({'author': author_string})
                if "Quelle" in video_info_field_description:
                    source_string = selector_item.xpath('//div[@class="customFieldValue "]/text()').get()
                    if source_string is not None:
                        source_string = w3lib.html.strip_html5_whitespace(source_string)
                        video_info_dict.update({'source': source_string})
                if "Produktionsjahr" in video_info_field_description:
                    production_year: str = selector_item.xpath('//div[@class="customFieldValue "]/text()').get()
                    if production_year is not None:
                        production_year = w3lib.html.strip_html5_whitespace(production_year)
                        video_info_dict.update({'production_year': production_year})
                if "Produktionsdatum" in video_info_field_description:
                    production_date: str = selector_item.xpath('//div[@class="customFieldValue "]/text()').get()
                    if production_date is not None:
                        production_date = w3lib.html.strip_html5_whitespace(production_date)
                        video_info_dict.update({'production_date': production_date})

        base = BaseItemLoader()

        base.add_value('sourceId', response.url)
        hash_temp: str = published_date + self.version
        base.add_value('hash', hash_temp)
        last_modified = published_date
        # while this is not strictly the last_modified date, it is the only date we can gather from the OOM
        base.add_value('lastModified', last_modified)
        base.add_value('type', Constants.TYPE_MATERIAL)
        # thumbnail_url: str = response.xpath('//meta[@property="og:image"]/@content').get()
        # ToDo: DiLerTube provides thumbnails, but they are locked behind an error 423 when directly accessing the link
        # if thumbnail_url is not None:
        #     base.add_value('thumbnail', thumbnail_url)

        if "source" in video_info_dict.keys():
            base.add_value('publisher', video_info_dict.get("source"))

        categories = list()
        keywords = list()
        categories_and_keywords_list: list = response.xpath('//ul[@class="list-group mx-0 my-0"]/li['
                                                            '@class="list-group-item"]').getall()
        # categories and keywords both use the same generic class names for its elements, therefore we try to identify
        # the description-text and use its <a href>-siblings to extract the text-values:
        for category_or_keyword_item in categories_and_keywords_list:
            selector_item = scrapy.Selector(text=category_or_keyword_item)
            category_or_keyword_description = selector_item.xpath('//span[@class="title"]/text()').get()
            if "Kategorie" in category_or_keyword_description:
                categories_temp = selector_item.xpath('//a[@class="badge-primary badge-pill"]/text()').getall()
                if len(categories_temp) >= 1:
                    for category_potential_candidate in categories_temp:
                        if category_potential_candidate.startswith("||| "):
                            # there are some categories which are not school-disciplines but rather keywords
                            # e.g. "||| Methoden": https://www.dilertube.de/sonstige/oer-videos/methoden.html
                            category_potential_candidate: str = category_potential_candidate.replace("||| ", "")
                        if category_potential_candidate in self.CATEGORY_IS_ACTUALLY_A_KEYWORD:
                            keywords.append(category_potential_candidate)
                        else:
                            categories.append(category_potential_candidate)
            if "Schlagwörter" in category_or_keyword_description:
                keywords_temp = selector_item.xpath('//a[@class="badge-primary badge-pill"]/text()').getall()
                if len(keywords_temp) >= 1:
                    keywords.extend(keywords_temp)

        lom = LomBaseItemloader()

        general = LomGeneralItemloader()
        general.add_value('identifier', response.url)
        general.add_value('title', response.xpath('//meta[@property="og:title"]/@content').get())
        general.add_value('description', response.xpath('//meta[@property="og:description"]/@content').get())
        general.add_value('language', response.xpath('/html/@lang').get())
        # grabs the language from the html language; there seem to be additional translations of DiLerTube in the works:
        # the german URLs use 'de-DE' by default,
        # while the english translations use 'en-GB', so this looks like a suitable indicator
        general.add_value('keyword', keywords)
        lom.add_value('general', general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value('format', 'text/html')
        technical.add_value('location', response.url)
        lom.add_value('technical', technical.load_item())

        lifecycle = LomLifecycleItemloader()
        if "production_year" in video_info_dict.keys():
            # this is a necessary workaround because dateparser.parse() would mis-calculate year-only representations of
            # the date
            datetime_production_year: datetime = datetime.strptime(video_info_dict.get("production_year"), "%Y")
            datetime_production_year: str = datetime_production_year.isoformat()
            lifecycle.add_value('date', datetime_production_year)
        if "production_date" in video_info_dict.keys():
            # this is a necessary workaround because dateparser.parse() would confuse de-DE time-formats as en-US
            datetime_production_date: datetime = datetime.strptime(video_info_dict.get("production_date"), "%d.%m.%Y")
            datetime_production_date: str = datetime_production_date.isoformat()
            lifecycle.add_value('date', datetime_production_date)
        lom.add_value('lifecycle', lifecycle.load_item())

        educational = LomEducationalItemLoader()
        lom.add_value('educational', educational.load_item())

        classification = LomClassificationItemLoader()
        lom.add_value('classification', classification.load_item())

        # once you've filled "general", "technical", "lifecycle" and "educational" with values,
        # the LomBaseItem is loaded into the "base"-BaseItemLoader
        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()
        for category_item in categories:
            if category_item in self.DISCIPLINE_MAPPING.keys():
                discipline = self.DISCIPLINE_MAPPING.get(category_item)
                vs.add_value('discipline', discipline)
            else:
                vs.add_value('discipline', category_item)
        vs.add_value('new_lrt', "7a6e9608-2554-4981-95dc-47ab9ba924de")  # Video (Material)
        vs.add_value('intendedEndUserRole', ["learner", "teacher"])
        vs.add_value('conditionsOfAccess', "no login")
        vs.add_value('containsAdvertisement', "no")
        vs.add_value('dataProtectionConformity', "Datensparsam")
        # see https://www.dilertube.de/datenschutz.html
        vs.add_value('price', "no")
        base.add_value('valuespaces', vs.load_item())

        lic = LicenseItemLoader()
        if "license_description" in video_info_dict.keys():
            # DiLerTube allows the uploaders to enter freeform text into the license field
            lic.add_value('description', video_info_dict.get("license_description"))
            if "cc_url" in video_info_dict.keys():
                lic.add_value('url', video_info_dict.get("cc_url"))
        if "author" in video_info_dict.keys():
            lic.add_value('author', video_info_dict.get("author"))
        base.add_value('license', lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value('permissions', permissions.load_item())

        response_loader = super().mapResponse(response)
        base.add_value('response', response_loader.load_item())

        yield base.load_item()
