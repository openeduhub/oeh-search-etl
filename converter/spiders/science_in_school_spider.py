import datetime

import dateparser
import scrapy
import w3lib.html

from converter.constants import Constants
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
    LomAgeRangeItemLoader,
)
from converter.spiders.base_classes import LomBase
from converter.util.license_mapper import LicenseMapper


class ScienceInSchoolSpider(scrapy.Spider, LomBase):
    name = "science_in_school_spider"
    friendlyName = "Science in School"
    start_urls = ["https://www.scienceinschool.org/issue/"]
    version = "0.0.5"  # last update: 2023-08-02
    custom_settings = {"AUTOTHROTTLE_ENABLED": True, "AUTOTHROTTLE_DEBUG": True}
    allowed_domains = ["scienceinschool.org"]
    ALL_ARTICLE_URLS = set()

    TOPICS_TO_DISCIPLINES_MAPPING = {
        "Astronomy / space": "Astronomy",
        "Biology": "Biology",
        "Chemistry": "Chemistry",
        "Health": "Health education",
        "Mathematics": "Mathematics",
        "Physics": "Physics",
        "Sustainability": "Sustainability",
    }
    KEYWORD_EXCLUSION_LIST = ["Not applicable", "not applicable"]

    def __init__(self, **kwargs):
        LomBase.__init__(self=self, **kwargs)

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse_issue_overview)

    def parse_issue_overview(self, response: scrapy.http.Response) -> scrapy.Request:
        """
        Crawls the overview-page of all published issues and extracts URLs to the individual issue numbers

        :param response: scrapy.http.Response
        :return: scrapy.Request

        Scrapy Contracts:
        @url https://www.scienceinschool.org/issue/
        @returns requests 51
        """
        issue_urls = response.xpath('//h3[@class="vf-card__heading"]/a[@class="vf-card__link"]/@href').getall()
        if issue_urls:
            # self.logger.info(f"Found {len(issue_urls)} Issues in the overview")
            for issue_url in issue_urls:
                yield scrapy.Request(url=issue_url, callback=self.parse_article_overview)
        pass

    def parse_article_overview(self, response: scrapy.http.Response) -> scrapy.Request:
        """
        Crawls an issue (e.g. Issue #3) for all individual article URLs within that publication. Afterwards yields the
        URLs to the parse()-method.

        :param response: scrapy.http.Response
        :return: scrapy.Request

        Scrapy Contracts:
        @url https://www.scienceinschool.org/issue/issue-3/
        @returns requests 20
        """
        article_urls = response.xpath('//h3[@class="vf-card__heading"]/a[@class="vf-card__link"]/@href').getall()
        # self.logger.info(f"Currently on {response.url} // Found {len(article_urls)} individual articles")
        self.ALL_ARTICLE_URLS.update(article_urls)
        # self.logger.info(f"Total URLs gathered so far: {len(self.ALL_ARTICLE_URLS)}")
        for article_url in article_urls:
            yield scrapy.Request(url=article_url, callback=self.parse)
        pass

    def getId(self, response=None) -> str:
        return response.url

    def getHash(self, response=None) -> str:
        date_published: str = self.extract_and_parse_date(response)
        hash_value: str = f"{date_published}v{self.version}"
        return hash_value

    @staticmethod
    def extract_and_parse_date(response):
        date_published_raw: str = response.xpath('//p[@class="vf-meta__date"]/text()').get()
        date_published = str()
        if date_published_raw:
            # using dateparser to get a reusable ISO-format from strings like 'January 28, 2016'
            # dateparser will show warnings in Python 3.10 (we're waiting for a new dateparser version)
            date_parsed = dateparser.parse(date_string=date_published_raw)
            if date_parsed:
                # the dateparser library can't parse all languages reliably, throws errors with serbian articles
                date_published = date_parsed.isoformat()
            else:
                date_published = datetime.datetime.now()
        return date_published

    async def parse(self, response: scrapy.http.Response, **kwargs) -> BaseItemLoader:
        """
        Crawls an individual article and extracts metadata. Afterward creates a BaseItem by filling up metadata-fields
        by calling .load_item() on the respective ItemLoaders.

        :param response: scrapy.http.Response
        :param kwargs:
        :return: BaseItem via .load_item()

        Scrapy Contracts:
        @url https://www.scienceinschool.org/article/2006/birdflu/
        @returns item 1
        """
        multilanguage_article_list: list = response.xpath(
            '//ul[@class="vf-links__list vf-links__list--secondary | ' 'vf-list"]/li/a/@href'
        ).getall()
        # on the left side of each article is a list of "Available languages", which holds URLs to all available
        # versions of the (currently visited) article, including its own URL. We need to make sure that we're only
        # gathering URLs that haven't been parsed before:
        # self.logger.info(f"Before gathering article translations: {len(self.ALL_ARTICLE_URLS)}")
        if multilanguage_article_list:
            for article_translation_url in multilanguage_article_list:
                if article_translation_url not in self.ALL_ARTICLE_URLS:
                    # making sure we're not parsing translated articles more than once or causing loops
                    if article_translation_url.endswith(".pdf"):
                        # skipping direct-links to .pdf files because scrapy / splash can't handle these
                        continue
                    elif "/sr/" in article_translation_url or article_translation_url.endswith("-sr/"):
                        # Articles that are translated to Serbian currently aren't supported by the dateparser.
                        # Since we don't want to deal with ~40 errors from these URLs, we skip them altogether.
                        continue
                    else:
                        yield scrapy.Request(url=article_translation_url, callback=self.parse)
            self.ALL_ARTICLE_URLS.update(multilanguage_article_list)
        # self.logger.info(f"This message should still be appearing after fetching article translations. URLs gathered "
        #                  f"so far: {len(self.ALL_ARTICLE_URLS)}")

        title: str = response.xpath('//meta[@property="og:title"]/@content').get()
        if title is None:
            title = response.xpath("//head/title/text()").get()
        description: str = response.xpath('//meta[@property="og:description"]/@content').get()
        thumbnail_url: str = response.xpath('//meta[@property="og:image"]/@content').get()
        language: list = response.xpath("//html/@lang").getall()

        date_published = self.extract_and_parse_date(response)

        authors_raw: list = response.xpath('//div[@class="vf-author | vf-article-meta-info__author"]/p/text()').getall()
        authors_clean = list()
        if authors_raw:
            for author_raw in authors_raw:
                possible_authors: str = w3lib.html.strip_html5_whitespace(author_raw)
                if possible_authors:
                    if "," in possible_authors:
                        possible_authors_list: list[str] = possible_authors.split(", ")
                        for author in possible_authors_list:
                            authors_clean.append(author)
                    else:
                        authors_clean.append(possible_authors)

        # selector for the whole metadata container, in case you want to try it out with Scrapy Shell:
        # response.xpath('//aside[@class="vf-article-meta-information"]').getall()
        metadata_container_ages_topics_keywords: list = response.xpath('//p[@class="vf-meta__topics"]').getall()
        # this metadata container doesn't have individual CSS Selectors for the different types of metadata
        # therefore we have to analyze it line-by-line:
        age_ranges = list()
        disciplines = set()
        keywords = set()
        if metadata_container_ages_topics_keywords:
            for metadata_container_item in metadata_container_ages_topics_keywords:
                current_selector = scrapy.Selector(text=metadata_container_item)
                current_selector_description = current_selector.xpath("//span/text()").get()
                if current_selector_description:
                    if "Ages:" in current_selector_description:
                        age_ranges_raw_string: str = current_selector.xpath("//p/text()").get()
                        # a typical string value can be ' 14-16, 16-19' (including the whitespace around single values)
                        if age_ranges_raw_string:
                            # therefore we're splitting up the string by its commas and removing the whitespace around
                            # each value
                            potential_age_ranges: list = age_ranges_raw_string.split(",")
                            if potential_age_ranges:
                                for age_range_item in potential_age_ranges:
                                    if age_range_item in self.KEYWORD_EXCLUSION_LIST:
                                        # filtering out the 'not applicable' string (which can also appear in topics)
                                        pass
                                    else:
                                        age_range_clean = age_range_item.strip()
                                        age_ranges.append(age_range_clean)
                    if "Topics:" in current_selector_description:
                        # there can be several topics per article
                        topic_description_list_raw = current_selector.xpath("//a/text()").getall()
                        topic_description_urls = current_selector.xpath("//a/@href").getall()
                        if topic_description_list_raw and topic_description_urls:
                            # topic_dict = dict(zip(topic_description_list_raw, topic_description_urls))
                            for potential_topic in topic_description_list_raw.copy():
                                # topics can either be real disciplines or will be treated as additional keywords
                                if potential_topic in self.TOPICS_TO_DISCIPLINES_MAPPING:
                                    disciplines.add(self.TOPICS_TO_DISCIPLINES_MAPPING.get(potential_topic))
                                elif potential_topic in self.KEYWORD_EXCLUSION_LIST:
                                    topic_description_list_raw.remove(potential_topic)
                                else:
                                    keywords.add(potential_topic)
                    if "Keywords:" in current_selector_description:
                        keyword_description_list_raw: list = current_selector.xpath("//a/text()").getall()
                        keyword_description_urls: list = current_selector.xpath("//a/@href").getall()
                        if keyword_description_list_raw and keyword_description_urls:
                            # keyword_dict = dict(zip(keyword_description_list_raw, keyword_description_urls))
                            for potential_keyword in keyword_description_list_raw:
                                keywords.add(potential_keyword)

        # supporting_materials_selector = response.xpath('//article[@class="sis-materials"]/p/a')
        supporting_materials_descriptions: list = response.xpath(
            '//article[@class="sis-materials"]/p/a/text()'
        ).getall()
        supporting_materials_urls: list = response.xpath('//article[@class="sis-materials"]/p/a/@href').getall()
        # on the right-hand side of an article there can (sometimes) be downloadable, additional materials:
        # - supporting materials (teachers guides etc.)
        # - "Download this article as a PDF"-button
        # ToDo: these materials would be suitable as "Serienobjekte" in a future crawler-version, see below
        if supporting_materials_descriptions and supporting_materials_urls:
            supporting_materials_dict = dict(zip(supporting_materials_descriptions, supporting_materials_urls))
            if "Download this article as a PDF" in supporting_materials_dict.keys():
                # first, we're extracting the PDF Download URL and remove it from the dictionary
                article_pdf_download_url = supporting_materials_dict.pop("Download this article as a PDF")
                if article_pdf_download_url:
                    # ToDo: if PDF download is available -> add it to our binary field?
                    pass
            if supporting_materials_dict:
                # before we look for "supporting materials", we need to make sure that our dict isn't empty after
                # removing the "Download this article as a PDF"-URL
                # supporting_materials_url_list = supporting_materials_dict.values()
                # ToDo: put these urls into an "edu-sharing"-Serienobjekt as soon as our environment supports it
                pass

        base = BaseItemLoader()
        base.add_value("sourceId", self.getId(response))
        base.add_value("hash", self.getHash(response))
        if thumbnail_url:
            base.add_value("thumbnail", thumbnail_url)
        lom = LomBaseItemloader()

        general = LomGeneralItemloader()
        general.add_value("identifier", response.url)
        if title:
            general.add_value("title", title)
        if keywords:
            general.add_value("keyword", keywords)
        if description:
            general.add_value("description", description)
        if language:
            for language_item in language:
                # edu-sharing expects the base.language value to be using underscores
                language_underscore: str = language_item.replace("-", "_")
                general.add_value("language", language_underscore)
            # depending on the article language, we're creating sub-folders within edu-sharing:
            # SYNC_OBJ/science_in_school_spider/<language_code>/
            base.add_value("origin", language)
        else:
            # if no language code is detected, the main part of the website is always available in English
            general.add_value("language", "en")
        # noinspection DuplicatedCode
        lom.add_value("general", general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value("format", "text/html")
        technical.add_value("location", response.url)
        lom.add_value("technical", technical.load_item())

        if authors_clean:
            for author in authors_clean:
                author_single_split = author.split(sep=" ", maxsplit=1)
                if author_single_split:
                    lifecycle_author = LomLifecycleItemloader()
                    lifecycle_author.add_value("role", "author")
                    if len(author_single_split) >= 1:
                        lifecycle_author.add_value("firstName", author_single_split[0])
                        if len(author_single_split) == 2:
                            lifecycle_author.add_value("lastName", author_single_split[1])
                    lom.add_value("lifecycle", lifecycle_author.load_item())

        lifecycle_publisher = LomLifecycleItemloader()
        lifecycle_publisher.add_value("role", "publisher")
        lifecycle_publisher.add_value("organization", "EIROforum")  # EIROforum is the intergovernmental
        # organization/publisher behind scienceinschool.org
        lifecycle_publisher.add_value("url", "https://www.scienceinschool.org/about-eiroforum/")
        lifecycle_publisher.add_value("email", "info@eiroforum.org")
        lifecycle_publisher.add_value("date", date_published)
        lom.add_value("lifecycle", lifecycle_publisher.load_item())

        educational = LomEducationalItemLoader()
        if language:
            educational.add_value("language", language)
        # ToDo: the primary website language is always English, but sometimes additional languages are available as well
        lom_age_range_loader = LomAgeRangeItemLoader()
        # since we already prepared age_ranges above to only hold valid, already whitespace-stripped strings, we can use
        # these values to fill our typicalAgeRange. According to the "Filter"-function on scienceinschool.org there
        # could be these possible values in our list: "< 11", "11-14", "14-16", "16-19"
        age_range_total = set()
        if age_ranges:
            for age_range_item in age_ranges:
                if "<" in age_range_item:
                    # "< 11"
                    from_range = 0
                    to_range = age_range_item.replace("<", "")
                    to_range = int(to_range)
                    age_range_total.add(from_range)
                    age_range_total.add(to_range)
                elif "-" in age_range_item:
                    from_range = int(min(age_range_item.split("-")))
                    to_range = int(max(age_range_item.split("-")))
                    age_range_total.add(from_range)
                    age_range_total.add(to_range)
            if age_range_total:
                lom_age_range_loader.add_value("fromRange", min(age_range_total))
                lom_age_range_loader.add_value("toRange", max(age_range_total))
                educational.add_value("typicalAgeRange", lom_age_range_loader.load_item())

        lom.add_value("educational", educational.load_item())

        classification = LomClassificationItemLoader()
        lom.add_value("classification", classification.load_item())

        base.add_value("lom", lom.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value("discipline", disciplines)
        vs.add_value("intendedEndUserRole", "teacher")
        vs.add_value("dataProtectionConformity", "generalDataProtectionRegulation")
        # see: https://www.embl.de/aboutus/privacy_policy/
        vs.add_value(
            "new_lrt",
            [
                Constants.NEW_LRT_MATERIAL,
                "b98c0c8c-5696-4537-82fa-dded7236081e",
                "0f519bd5-069c-4d32-b6d3-a373ac96724c",
            ],
        )
        # "Artikel und Einzelpublikation", "Fachliche News"
        vs.add_value("containsAdvertisement", "no")
        vs.add_value("conditionsOfAccess", "no_login")
        vs.add_value("price", "no")
        base.add_value("valuespaces", vs.load_item())

        license_loader = LicenseItemLoader()
        if authors_clean:
            license_loader.add_value("author", authors_clean)
        license_raw: str = response.xpath('//a[@href="/copyright"]/text()').get()
        # see: https://www.scienceinschool.org/copyright/
        # the possible string patterns seem to be either "CC-BY", "CC-BY-NC-SA" or "CC-BY-NC-ND"
        if license_raw:
            license_mapper = LicenseMapper()
            license_internal_mapped: str | None = license_mapper.get_license_internal_key(license_string=license_raw)
            if license_internal_mapped:
                license_loader.add_value("internal", license_internal_mapped)
            # sometimes there is an additional license description available, which always seems to be in the next
            # <div>-container after the copyright <a>-element:
            license_description = response.xpath(
                '//div[child::a[@href="/copyright"]]/following-sibling::div' "/text()"
            ).get()
            if license_description:
                license_description_stripped = w3lib.html.strip_html5_whitespace(license_description)
                if license_description_stripped:
                    license_description_mapped: str | None = license_mapper.get_license_internal_key(
                        license_description_stripped
                    )
                    if license_description_mapped and not license_internal_mapped:
                        license_loader.replace_value("internal", license_description_mapped)
                    license_loader.add_value("description", license_description)
            else:
                # as a fallback, we try to set the raw license string
                license_loader.add_value("description", license_raw)
        # noinspection DuplicatedCode
        base.add_value("license", license_loader.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader = await super().mapResponse(response)
        base.add_value("response", response_loader.load_item())

        yield base.load_item()
