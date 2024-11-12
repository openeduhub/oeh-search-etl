from __future__ import annotations

import datetime
import json
import logging
import os
import re
import sqlite3
from typing import Optional, cast

import openai
import scrapy.http
import scrapy.signals
import trafilatura  # type: ignore
from bs4 import BeautifulSoup
from scrapy.http.response import Response
from scrapy.http.response.text import TextResponse
from scrapy.spiders import Spider
from scrapy.spiders.crawl import Rule

import z_api
import z_api.exceptions
from converter.util.sitemap import find_generate_sitemap
from valuespace_converter.app.valuespaces import Valuespaces

from .. import env
from ..items import (AiPromptItemLoader, BaseItemLoader, KIdraItemLoader,
                     LicenseItemLoader, LomBaseItemloader,
                     LomClassificationItemLoader, LomEducationalItemLoader,
                     LomGeneralItemloader, LomLifecycleItemloader,
                     LomTechnicalItemLoader, ResponseItemLoader,
                     ValuespaceItemLoader)
from ..util.generic_crawler_db import fetch_urls_passing_filterset
from ..util.license_mapper import LicenseMapper
from ..web_tools import WebEngine, WebTools
from .base_classes import LrmiBase

log = logging.getLogger(__name__)


class GenericSpider(Spider, LrmiBase):
    name = "generic_spider"
    friendlyName = "generic_spider"  # name as shown in the search ui
    version = "0.1.4"
    start_urls = []
    rules = [Rule(callback="parse")]
    custom_settings = { "WEB_TOOLS": WebEngine.Playwright, "ROBOTSTXT_OBEY": False }

    clean_tags = ["nav", "header", "footer"]
    prompts = {
        "description": "Fasse folgenden Text in 3 Sätzen zusammen: %(text)s",
        "keyword": "Liefere 4 Schlagworte für folgenden Text: %(text)s",
        "discipline": "Für welche Schul bzw. Fachgebiete eignet sich folgender Text: %(text)s",
        "educationalContext": "Für welche Bildungsstufe eignet sich folgender Text: %(text)s",
        "new_lrt": "Welche Materialart im schulischen Kontext ist folgender Text: %(text)s",
        "intendedEndUserRole": "Für welche Zielgruppen eignet sich folgender Text: %(text)s",
    }
    valuespaces: Valuespaces
    ai_enabled: bool
    z_api_text: z_api.AITextPromptsApi
    z_api_kidra: z_api.KidraApi
    llm_client: Optional[openai.OpenAI] = None
    use_llm_api: bool = False
    llm_model: str = ""

    def __init__(self, urltocrawl="", validated_result="", ai_enabled="True", find_sitemap="False",
                 max_urls="3", filter_set_id="", **kwargs):
        super().__init__(**kwargs)

        log.info("Initializing GenericSpider")
        log.info("Arguments:")
        log.info("  urltocrawl: %r", urltocrawl)
        log.info("  validated_result: %r", validated_result)
        log.info("  ai_enabled: %r", ai_enabled)
        log.info("  find_sitemap: %r", find_sitemap)
        log.info("  max_urls: %r", max_urls)
        log.info("  filter_set_id: %r", filter_set_id)

        if urltocrawl and filter_set_id:
            raise ValueError("You must set either 'urltocrawl' or 'filter_set_id', not both.")

        if not urltocrawl and not filter_set_id:
            raise ValueError("You must set either 'urltocrawl' or 'filter_set_id'.")

        if filter_set_id != "":
            self.filter_set_id = int(filter_set_id)
        else:
            self.filter_set_id = None

        self.max_urls = int(max_urls)

        self.results_dict = {}
        if urltocrawl != "":
            urls = [url.strip() for url in urltocrawl.split(",")]
            if find_sitemap == "True" and len(urls) == 1:
                sitemap_urls = find_generate_sitemap(
                    urls[0], max_entries=self.max_urls)
                self.start_urls = sitemap_urls
            else:
                self.start_urls = urls[:self.max_urls]

        if validated_result != "":
            self.results_dict = json.loads(validated_result)
            urltocrawl = self.results_dict["url"]
            self.start_urls = [urltocrawl]

        # logging.warning("self.start_urls=" + self.start_urls[0])
        self.valuespaces = Valuespaces()

        try:
            self.ai_enabled = to_bool(ai_enabled)
        except ValueError:
            log.error("Invalid value for ai_enabled: %s", ai_enabled)
            raise

        if self.ai_enabled:
            log.info("Starting generic_spider with ai_enabled flag!")
            z_api_config = z_api.Configuration.get_default_copy()
            z_api_config.api_key = {
                "ai-prompt-token": env.get("Z_API_KEY", False)}
            z_api_client = z_api.ApiClient(configuration=z_api_config)
            self.z_api_text = z_api.AITextPromptsApi(z_api_client)
            self.z_api_kidra = z_api.KidraApi(z_api_client)
        else:
            log.info(
                "Starting generic_spider with MINIMAL settings. AI Services are DISABLED!")
            # this optional flag allows us to control if we want to use
            # AI-suggested metadata. We can compare the items gathered
            # by the "generic_spider_minimal" against the (AI-enabled)
            # "generic_spider"
            self.name = "generic_spider_minimal"
            self.friendlyName = "generic_spider_minimal"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(
            spider.spider_opened, signal=scrapy.signals.spider_opened)  # pylint: disable=no-member
        return spider

    def spider_opened(self, spider: GenericSpider):
        """ Run when the spider is opened, before the crawl begins.
            Open the database and get the list of URLs to crawl. """

        log.info("Opened spider %s", spider.name)
        db_path = self.settings.get('GENERIC_CRAWLER_DB_PATH')
        log.info("Using database at %s", db_path)
        if db_path is not None:
            log.info("File exists? %s", os.path.exists(db_path))
        if db_path is None or not os.path.exists(db_path):
            log.error(
                "No database set or database not found. Please set GENERIC_CRAWLER_DB_PATH.")
            return

        if not self.filter_set_id:
            return

        log.info("Filter set ID: %s", self.filter_set_id)
        # List filter rules in this filter set
        connection = sqlite3.connect(db_path)

        matches = fetch_urls_passing_filterset(connection, self.filter_set_id, limit=self.max_urls)

        log.info("Adding %d URLs to start_urls", len(matches))
        for row in matches:
            log.info("Adding URL to start_urls: %s", row.url)
            self.start_urls.append(row.url)

        self.setup_llm_client()

    def setup_llm_client(self):
        self.use_llm_api = self.settings.get('GENERIC_CRAWLER_USE_LLM_API', False)
        log.info("GENERIC_CRAWLER_USE_LLM_API: %r", self.use_llm_api)
        if not self.use_llm_api:
            return

        api_key = self.settings.get('GENERIC_CRAWLER_LLM_API_KEY', '')
        if not api_key:
            raise RuntimeError(
                "No API key set for LLM API. Please set GENERIC_CRAWLER_LLM_API_KEY.")

        base_url = self.settings.get('GENERIC_CRAWLER_LLM_API_BASE_URL', '')
        if not base_url:
            raise RuntimeError(
                "No base URL set for LLM API. Please set GENERIC_CRAWLER_LLM_API_BASE_URL.")

        self.llm_model = self.settings.get('GENERIC_CRAWLER_LLM_MODEL', '')
        if not self.llm_model:
            raise RuntimeError(
                "No model set for LLM API. Please set GENERIC_CRAWLER_LLM_MODEL.")
        
        log.info("Using LLM API with the following settings:")
        log.info("GENERIC_CRAWLER_LLM_API_KEY: <set>")
        log.info("GENERIC_CRAWLER_LLM_API_BASE_URL: %r", base_url)
        log.info("GENERIC_CRAWLER_LLM_MODEL: %r", self.llm_model)
        self.llm_client = openai.OpenAI(api_key=api_key, base_url=base_url)

    def getId(self, response: Optional[Response] = None) -> str:
        """Return a stable identifier (URI) of the crawled item"""
        assert response
        return response.url

    def getHash(self, response: Optional[Response] = None) -> str:
        """
        Return a stable hash to detect content changes (for future crawls).
        """
        return f"{datetime.datetime.now().isoformat()}v{self.version}"

    async def parse(self, response: Response):
        if not self.hasChanged(response):
            return

        url_data = await WebTools.getUrlData(response.url, engine=WebEngine.Playwright)
        if not url_data:
            log.warning("Playwright failed to fetch data for %s", response.url)
            return

        response = response.copy()
        assert isinstance(response, TextResponse)

        # ToDo: validate "trafilatura"-fulltext-extraction from playwright
        # (compared to the html2text approach)
        playwright_text: str = url_data["html"] or ""
        playwright_bytes: bytes = playwright_text.encode()
        trafilatura_text = url_data["text"]
        log.info("trafilatura_text: %s", trafilatura_text)
        # ToDo: implement text extraction .env toggle: default / advanced / basic?
        #  - default: use trafilatura by default?
        #  - advanced: which trafilatura parameters could be used to improve text extraction for
        #    "weird" results?
        #  - basic: fallback to html2text extraction (explicit .env setting)
        # trafilatura_meta_scrapy = trafilatura.extract_metadata(response.body).as_dict()
        trafilatura_meta_playwright = trafilatura.extract_metadata(
            playwright_bytes)
        parsed_html = BeautifulSoup(url_data["html"] or "", features="lxml")
        for tag in self.clean_tags:
            tags = parsed_html.find_all(
                tag) if parsed_html.find_all(tag) else []
            for t in tags:
                t.clear()
        crawler_ignore = parsed_html.find_all(
            name=None, attrs={"data-crawler": "ignore"})
        for t in crawler_ignore:
            t.clear()
        html = parsed_html.prettify()
        text_html2text = WebTools.html2Text(html)
        if trafilatura_meta_playwright:
            trafilatura_meta = trafilatura_meta_playwright.as_dict()
        else:
            trafilatura_meta = {}

        response.meta["data"] = {
            # legacy, do we need these fields?
            "content": url_data["html"],
            "parsed_html": parsed_html,
            "text": text_html2text,
            "trafilatura_text": trafilatura_text,
            "trafilatura_meta": trafilatura_meta,
        }

        selector_playwright = scrapy.Selector(text=playwright_text)
        robot_meta_tags: list[str] = selector_playwright.xpath(
            "//meta[@name='robots']/@content").getall()
        respect_robot_meta_tags = env.get_bool(
            key="RESPECT_ROBOT_META_TAGS", allow_null=True, default=True)
        if robot_meta_tags and respect_robot_meta_tags:
            # There are 3 Robot Meta Tags (<meta name="robots" content="VALUE">) that we need to
            # respect:
            # - "noindex"       (= don't index the current URL)
            # - "nofollow"      (= don't follow any links on this site)
            # - "none"          (= shortcut for combined value "noindex, nofollow")
            # by default, we try to respect the webmaster's wish to not be indexed/crawled
            if "noindex" in robot_meta_tags:
                log.info(
                    "Robot Meta Tag 'noindex' identified. Aborting further parsing of item: %s .",
                    response.url)
                return
            if "nofollow" in robot_meta_tags:
                # ToDo: don't follow any links, but parse the current response
                #  -> yield response with 'nofollow'-setting in cb_kwargs
                log.info(
                    "Robot Meta Tag 'nofollow' identified. Parsing item %s , but WILL NOT "
                    "follow any links found within.", response.url
                )
            if "none" in robot_meta_tags:
                log.info(
                    "Robot Meta Tag 'none' identified (= 'noindex, nofollow'). "
                    "Aborting further parsing of item: %s itself and any links within it.",
                    response.url
                )
                return

        base_loader = BaseItemLoader(selector=selector_playwright)
        base_loader.add_value("sourceId", self.getId(response))
        base_loader.add_value("hash", self.getHash(response))
        base_loader.add_value("thumbnail", self.getLRMI(
            "thumbnailUrl", response=response))
        base_loader.add_xpath(
            "thumbnail", '//meta[@property="og:image"]/@content')
        base_loader.add_xpath(
            "lastModified", '//meta[@name="last-modified"]/@content')

        # Creating the nested ItemLoaders according to our items.py data model
        lom_loader = LomBaseItemloader()
        general_loader = LomGeneralItemloader(response=response)
        technical_loader = LomTechnicalItemLoader(selector=selector_playwright)
        educational_loader = LomEducationalItemLoader()
        classification_loader = LomClassificationItemLoader()
        valuespace_loader = ValuespaceItemLoader()
        license_loader = LicenseItemLoader(selector=selector_playwright)
        permissions_loader = self.getPermissions(response)
        response_loader = ResponseItemLoader()
        kidra_loader = KIdraItemLoader()

        # ToDo: rework LRMI JSON-LD extraction
        #  - so it can handle websites when there are several JSON-LD containers within a single DOM
        # ToDo: try to grab as many OpenGraph metadata properties as possible (for reference, see:
        # https://ogp.me)

        # general_loader.add_xpath("title", '//meta[@property="og:title"]/@content')
        general_loader.add_xpath("title", '//title/text()')
        # HTML language and locale properties haven proven to be pretty inconsistent, but they might
        # be useful as fallback values.
        # ToDo: websites might return languagecodes as 4-char values (e.g. "de-DE") instead of the
        # 2-char value "de"
        # -> we will have to detect/clean up languageCodes to edu-sharing's expected 2-char format
        general_loader.add_value("language", self.getLRMI(
            "inLanguage", response=response))
        general_loader.add_xpath("language", "//html/@lang")
        general_loader.add_xpath(
            "language", '//meta[@property="og:locale"]/@content')
        general_loader.add_value("description", self.getLRMI(
            "description", "about", response=response))
        general_loader.add_value(
            "keyword", self.getLRMI("keywords", response=response))

        if self.ai_enabled:
            excerpt = text_html2text[:4000]
            self.query_llm(excerpt, general_loader, base_loader, valuespace_loader)

            kidra_loader.add_value(
                "curriculum", self.zapi_get_curriculum(excerpt))
            classification, reading_time = self.zapi_get_statistics(excerpt)
            kidra_loader.add_value("text_difficulty", classification)
            kidra_loader.add_value("text_reading_time", reading_time)
            kidra_loader.add_value(
                "kidraDisciplines", self.zapi_get_disciplines(excerpt))
            # ToDo: map/replace the previously set 'language'-value by AI suggestions from Z-API?
            base_loader.add_value("kidra_raw", kidra_loader.load_item())
        else:
            if trafilatura_description := trafilatura_meta.get("description"):
                general_loader.add_value(
                    "description", trafilatura_description)
            if trafilatura_title := trafilatura_meta.get("title"):
                general_loader.replace_value("title", trafilatura_title)

        lom_loader.add_value("general", general_loader.load_item())

        technical_loader.add_value(
            "format", self.getLRMI("fileFormat", response=response))
        # ToDo: do we really want to hard-code this?
        technical_loader.replace_value("format", "text/html")
        technical_loader.add_value("size", self.getLRMI(
            "ContentSize", response=response))
        technical_loader.add_value(
            "location", self.getLRMI("url", response=response))
        technical_loader.add_value("location", response.url)
        technical_loader.replace_value("size", len(response.body))
        # ToDo: 'size' should probably use the length of our playwright response, not scrapy's
        # response.body
        technical_loader.add_xpath(
            "location", '//meta[@property="og:url"]/@content')

        self.get_lifecycle_author(
            lom_loader=lom_loader, selector=selector_playwright, response=response)

        self.get_lifecycle_publisher(
            lom_loader=lom_loader, selector=selector_playwright, response=response)

        # we might be able to extract author/publisher information from typical <meta> or <head>
        # fields in the DOM
        lom_loader.add_value("educational", educational_loader.load_item())
        lom_loader.add_value(
            "classification", classification_loader.load_item())
        lom_loader.add_value("technical", technical_loader.load_item())
        # after LomBaseItem is filled with nested metadata, we build the LomBaseItem and add it to
        # our BaseItem:
        base_loader.add_value("lom", lom_loader.load_item())

        # Todo: does this deal with multiple authors correctly?
        license_loader.add_xpath("author", '//meta[@name="author"]/@content')
        # trafilatura offers a license detection feature as part of its "extract_metadata()"-method

        if trafilatura_license_detected := trafilatura_meta.get("license"):
            license_mapper = LicenseMapper()
            license_url_mapped = license_mapper.get_license_url(
                license_string=trafilatura_license_detected
            )
            # ToDo: this is a really risky assignment! Validation of trafilatura's license detection
            #  will be necessary! (this is a metadata field that needs to be confirmed by a human!)
            license_loader.add_value("url", license_url_mapped)

        # lrmi_intended_end_user_role = self.getLRMI("audience.educationalRole", response=response)
        # if lrmi_intended_end_user_role:
        #     valuespace_loader.add_value("intendedEndUserRole", lrmi_intended_end_user_role)
        # ToDo: rework
        # # attention: serlo URLs will break the getLRMI() Method because JSONBase cannot extract
        # the JSON-LD properly
        # # ToDo: maybe use the 'jmespath' Python package to retrieve this value more reliably
        valuespace_loader.add_value("learningResourceType", self.getLRMI(
            "learningResourceType", response=response))

        # loading all nested ItemLoaders into our BaseItemLoader:
        base_loader.add_value("license", license_loader.load_item())
        base_loader.add_value("valuespaces", valuespace_loader.load_item())
        base_loader.add_value("permissions", permissions_loader.load_item())
        base_loader.add_value("response", response_loader.load_item())

        if self.results_dict:
            base_loader = self.modify_base_item(base_loader)
        log.info("New URL processed:------------------------------------------")
        log.info(base_loader.load_item())
        log.info("------------------------------------------------------------")

        yield base_loader.load_item()

    def get_lifecycle_publisher(self, lom_loader: LomBaseItemloader, selector: scrapy.Selector,
                                response: Response):
        meta_publisher = selector.xpath(
            '//meta[@name="publisher"]/@content').get()
        if meta_publisher:
            lifecycle_publisher_loader = LomLifecycleItemloader()
            lifecycle_publisher_loader.add_value("role", "publisher")
            lifecycle_publisher_loader.add_value(
                "organization", meta_publisher)
            self.get_lifecycle_date(
                lifecycle_loader=lifecycle_publisher_loader, selector=selector, response=response)

            lom_loader.add_value(
                "lifecycle", lifecycle_publisher_loader.load_item())

    def get_lifecycle_author(self, lom_loader: LomBaseItemloader, selector: scrapy.Selector,
                             response: Response):
        meta_author = selector.xpath('//meta[@name="author"]/@content').get()
        if meta_author:
            lifecycle_author_loader = LomLifecycleItemloader()
            lifecycle_author_loader.add_value("role", "author")
            # author strings could be one or several names or organizations.
            # The license loader expects a 'firstName'.
            lifecycle_author_loader.add_value("firstName", meta_author)
            # ToDo: (optional) try determining if names need to be sorted into
            # 'firstName', 'lastName' or 'organization'-field-values
            # ToDo: shoving the whole string into 'firstName' is a hacky approach that will cause
            # organizations to appear as persons within the "lifecycle"-metadata. fine-tune this
            # approach later.
            self.get_lifecycle_date(
                lifecycle_loader=lifecycle_author_loader, selector=selector, response=response)

            lom_loader.add_value(
                "lifecycle", lifecycle_author_loader.load_item())

    @staticmethod
    def get_lifecycle_date(lifecycle_loader: LomLifecycleItemloader, selector: scrapy.Selector,
                           response: Response):
        if "date" in response.meta["data"]["trafilatura_meta"]:
            # trafilatura's metadata extraction scans for dates within
            # <meta name="date" content"..."> Elements
            date = selector.xpath('//meta[@name="date"]/@content').get()
            date_trafilatura: str = response.meta["data"]["trafilatura_meta"]["date"]
            if date_trafilatura:
                lifecycle_loader.add_value("date", date_trafilatura)
            elif date:
                lifecycle_loader.add_value("date", date)

    def zapi_get_curriculum(self, text: str) -> list[str]:
        """ Determines the curriculum topic (Lehrplanthema) using the z-API. """
        try:
            result = cast(z_api.TopicAssistantKeywordsResult,
                        self.z_api_kidra.topics_flat_topics_flat_post({"text": text}))
        except z_api.exceptions.ApiException:
            log.error("Failed to get curriculum topics from z-API")
            return []

        n_topics = 3
        if result.topics:
            topics = result.topics[:n_topics]
            topic_names = [topic.uri for topic in topics]
            return topic_names
        else:
            return []

    def zapi_get_statistics(self, text: str) -> tuple[str, float]:
        """ Queries the z-API to get the text difficulty and reading time. """
        params = {"text": text, "reading_speed": 200,
                  "generate_embeddings": False}
        try:
            result = cast(z_api.TextStatisticsResult,
                        self.z_api_kidra.text_stats_analyze_text_post(params))
        except z_api.exceptions.ApiException:
            log.error("Failed to get text statistics from z-API")
            return "", 0.0

        return result.classification, round(result.reading_time, 2)  # type: ignore

    def zapi_get_disciplines(self, text: str) -> list[str]:
        """ Gets the disciplines for a given text using the z-API. """
        try:
            result = self.z_api_kidra.predict_subjects_kidra_predict_subjects_post({"text": text})
        except z_api.exceptions.ApiException:
            log.error("Failed to get disciplines from z-API")
            return []

        min_score = 0.3
        uri_discipline = 'http://w3id.org/openeduhub/vocabs/discipline/'
        discipline_names = [
            uri_discipline + d.id for d in result.disciplines if d.score > min_score  # type: ignore
        ]

        return discipline_names

    def query_llm(self, excerpt: str, general_loader: LomGeneralItemloader,
                  base_loader: BaseItemLoader, valuespace_loader: ValuespaceItemLoader):
        """ Performs the LLM queries for the given text, and fills the
            corresponding ItemLoaders. """

        general_loader.add_value(
            "description", self.resolve_z_api(
                "description", excerpt, base_itemloader=base_loader)
        )
        keyword_str = self.resolve_z_api(
            "keyword", excerpt, base_itemloader=base_loader)
        if keyword_str:
            keywords = [s.strip()
                        for s in re.split(r"[,|\n]", keyword_str)]
            # TODO: does it work to pass a list to add_value?
            general_loader.add_value("keyword", keywords)

        # ToDo: keywords will (often) be returned as a list of bullet points by the AI
        #  -> we might have to detect & clean up the string first
        for v in ["educationalContext", "discipline", "intendedEndUserRole", "new_lrt"]:
            ai_response = self.resolve_z_api(
                v, excerpt, base_itemloader=base_loader)
            if ai_response:
                valuespace_loader.add_value(
                    v, self.valuespaces.findInText(v, ai_response))


    def resolve_z_api(self, field: str, text: str,
                      base_itemloader: BaseItemLoader) -> Optional[str]:
        ai_prompt_itemloader = AiPromptItemLoader()
        ai_prompt_itemloader.add_value("field_name", field)
        prompt = self.prompts[field] % {"text": text}
        # ToDo: figure out a reasonable cutoff-length
        # (prompts which are too long get thrown out by the AI services)
        ai_prompt_itemloader.add_value("ai_prompt", prompt)

        if self.llm_client:
            chat_completion = self.llm_client.chat.completions.create(
                messages=[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":prompt}],
                model=self.llm_model
            )
            log.info("LLM API response: %s", chat_completion)
            result = chat_completion.choices[0].message.content or ""
        else:
            # TODO: add error checking
            api_result = cast(z_api.TextPromptEntity,
                            self.z_api_text.prompt(body=prompt))
            if not api_result.responses:
                log.error("No valid response from AI service for prompt: %s", prompt)
                return None
            result: str = api_result.responses[0].strip()
        ai_prompt_itemloader.add_value("ai_response_raw", result)
        ai_prompt_itemloader.add_value("ai_response", result)
        base_itemloader.add_value(
            "ai_prompts", ai_prompt_itemloader.load_item())
        return result

    def modify_base_item(self, base_loader):
        title = self.results_dict['title']
        description = self.results_dict['description']
        if len(self.results_dict['disciplines']) != 0:
            disciplines = self.results_dict['disciplines']
            base_loader.load_item()['valuespaces']['discipline'] = disciplines
        educational_context = self.results_dict['educational_context']
        intendedEndUserRole = self.results_dict['intendedEndUserRole']
        keywords = self.results_dict['keywords']
        license = self.results_dict['license']
        new_lrt = self.results_dict['new_lrt']
        curriculum = self.results_dict['curriculum']
        if len(self.results_dict['text_difficulty']) != 0:
            text_difficulty = self.results_dict['text_difficulty']
            base_loader.load_item()[
                'kidra_raw']['text_difficulty'] = text_difficulty
        if len(self.results_dict['text_reading_time']) != 0:
            text_reading_time = self.results_dict['text_reading_time']
            base_loader.load_item()[
                'kidra_raw']['text_reading_time'] = text_reading_time

        # TODO: this looks wrong
        base_loader.load_item()['lom']['general']['title'] = title
        base_loader.load_item()['lom']['general']['description'] = description
        base_loader.load_item()['lom']['general']['keyword'] = keywords
        base_loader.load_item()['valuespaces']['new_lrt'] = new_lrt
        base_loader.load_item()[
            'valuespaces']['educationalContext'] = educational_context
        base_loader.load_item()[
            'valuespaces']['intendedEndUserRole'] = intendedEndUserRole
        base_loader.load_item()['license'] = license
        # base_loader.load_item()['valuespaces']['curriculum'] = curriculum
        base_loader.load_item()['kidra_raw']['curriculum'] = curriculum

        return base_loader


def to_bool(value: str) -> bool:
    """ Converts a string to a bool. Yes, true, t, 1 is True.
        No, false, f, 0 is False. The function is case insensitive.
        Returns a ValueError if the argument is something else.
    """

    if value.lower() in ("yes", "true", "t", "1"):
        return True
    if value.lower() in ("no", "false", "f", "0"):
        return False
    raise ValueError(f"Invalid boolean value: {value}")
