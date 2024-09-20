from __future__ import annotations

import datetime
import json
import logging
import os
import re
import sqlite3

import scrapy.http
import trafilatura  # type: ignore
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import Rule, Spider

import z_api
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
    start_urls = [
        # "https://www.planet-schule.de/schwerpunkt/total-phaenomenal-energie/sonnenenergie-film-100.html",  # the original Hackathon example URL
        # "https://de.serlo.org/informatik/158541/definitionen-von-%E2%80%9Ebig-data%E2%80%9C",
        # "https://de.serlo.org/mathe/62630/aufgaben-zum-volumen-eines-quaders",
        # "https://www.planet-schule.de/schwerpunkt/dichter-dran/fontane-film-100.html",
        # "https://www.planet-schule.de/thema/fridays-for-future-was-steckt-hinter-den-klima-streiks-film-100.html",
        # "https://www.dilertube.de/englisch/oer-video/algeria-in-a-nutshell.html",
        # "https://www.dilertube.de/alltagskultur-ernaehrung-soziales-aes/oer-video/erklaerfilm-medikamente-richtig-entsorgen.html",
        # "https://www.umwelt-im-unterricht.de/unterrichtsvorschlaege/der-mensch-hauptursache-fuer-den-rueckgang-der-biologischen-vielfalt",
        # "https://www.umwelt-im-unterricht.de/hintergrund/die-endlagerung-hochradioaktiver-abfaelle",
        # "https://editor.mnweg.org/mnw/sammlung/das-menschliche-skelett-m-78",
        # "https://editor.mnweg.org/mnw/sammlung/bruchrechnen-m-10",
        # "https://www.bpb.de/themen/migration-integration/laenderprofile/277555/afghanistan-geschichte-politik-gesellschaft/",
        # "https://www.bpb.de/themen/kolonialismus-imperialismus/postkolonialismus-und-globalgeschichte/236617/kolonialismus-und-postkolonialismus-schluesselbegriffe-der-aktuellen-debatte/",
        # "https://www.geschichtsquellen.de/werk/3402",
        # "https://www.geschichtsquellen.de/werk/4799",
        # "https://www.weltderphysik.de/gebiet/teilchen/quanteneffekte/",
        # "https://www.weltderphysik.de/mediathek/podcast/geothermie/",
        # "https://histomania.com/app/Saralee_Thungthongkam_W468573",
        # "https://histomania.com/app/Anna_Maria_von_Anhalt_W527486",
        # "https://medienportal.siemens-stiftung.org/de/design-thinking#examples",
        # "https://medienportal.siemens-stiftung.org/portal/main.php?todo=metadata_search&searcharea=portal&crits%5Bmedialang%5D=de&options%5BsearchAndOr%5D=1&crits%5Bfree%5D=Bl%C3%A4tterwald&crits%5Bmedialang%5D=de&options%5Bsort%5D=mediatype%2Ctimepublish+DESC",
        # "https://medienportal.siemens-stiftung.org/de/service-learning-in-den-mint-faechern-109145",
        # "https://apps.zum.de/apps/25726",
        # "https://apps.zum.de/apps/25532",
        # "https://www.inf-schule.de/datenbanksysteme/terra/relationaledb/konzept_tabelle",
        # "https://www.inf-schule.de/rechner/bonsai/murmelrechner/universellermurmelrechner",
        # "https://weltverbessern-lernen.de/materialupload/dirk-ehnts-modern-monetary-theory-erklaert/",
        # "https://weltverbessern-lernen.de/materialupload/mehr-oder-weniger-wachstumskritik-von-links/",
        # "https://weltverbessern-lernen.de/materialupload/5707/",
        # "https://lernen.schule.de/das-notensystem/",
        # "https://lernen.schule.de/das-menschliche-skelett/",
        # "https://www.schulebewegt.ch/de/aufgaben/Streckung",
        # "https://www.schulebewegt.ch/de/aufgaben/Hampelmann",
    ]
    rules = [
        Rule(callback="parse"),
    ]
    custom_settings = {"WEB_TOOLS": WebEngine.Playwright, "ROBOTSTXT_OBEY": False}

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
    AI_ENABLED: bool = True  # optional .env setting to turn off AI services (-> generic_spider_minimal)
    z_api_text: z_api.AITextPromptsApi
    z_api_kidra: z_api.KidraApi

    def __init__(self, urltocrawl="", validated_result="", ai_enabled="True", find_sitemap="False", max_urls="3", filter_set_id="", **kwargs):
        super().__init__(**kwargs)

        # self.validated_result = validated_result
        # validated_result = '{"curriculum":["http://w3id.org/openeduhub/vocabs/oeh-topics/66e5911e-ba75-4521-adb6-cbe24569500b"], "url": "https://blog.bitsrc.io/how-to-store-data-on-the-browser-with-javascript-9c57fc0f91b0", "title": "Test 2 How to Store Data in the Browser with JavaScript | Bits and Pieces", "description": "Test How to store data with localStorage and sessionStorage. The benefits of each, and when you should use one instead of the other", "keywords": ["Test JavaScript"], "disciplines": ["http://w3id.org/openeduhub/vocabs/discipline/320"], "educational_context": ["http://w3id.org/openeduhub/vocabs/educationalContext/fortbildung"], "license": {"author": ["Pedro Henrique"]}, "new_lrt": ["http://w3id.org/openeduhub/vocabs/new_lrt/1846d876-d8fd-476a-b540-b8ffd713fedb"], "intendedEndUserRole":["http://w3id.org/openeduhub/vocabs/intendedEndUserRole/counsellor"]}'
        # logging.warning("self.validated_result="+self.validated_result)

        if filter_set_id != "":
            self.filter_set_id = int(filter_set_id)
        else:
            self.filter_set_id = None

        # temp hack
        ai_enabled = "False"

        self.results_dict = {}
        if urltocrawl != "":
            urls = get_urls_from_string(urltocrawl)
            if find_sitemap == "True" and len(urls) == 1:
                max_sitemap_urls = int(max_urls)
                sitemap_urls = find_generate_sitemap(urls[0], max_entries=max_sitemap_urls)
                self.start_urls = sitemap_urls
            else:
                self.start_urls = urls
        if validated_result != "":
            self.results_dict = json.loads(validated_result)
            urltocrawl = self.results_dict["url"]
            self.start_urls = [urltocrawl]

        # logging.warning("self.start_urls=" + self.start_urls[0])
        self.valuespaces = Valuespaces()
        # ToDo: optional .env Feature: "generic_spider" (AI=enabled) <-> "generic_minimal_spider" (AI=disabled)?
        if ai_enabled == "True":
            self.AI_ENABLED = True
            log.info("Starting generic_spider with AI_ENABLED flag!")
            z_api_config = z_api.Configuration.get_default_copy()
            z_api_config.api_key = {"ai-prompt-token": env.get("Z_API_KEY", False)}
            z_api_client = z_api.ApiClient(configuration=z_api_config)
            self.z_api_text = z_api.AITextPromptsApi(z_api_client)
            self.z_api_kidra = z_api.KidraApi(z_api_client)
        elif ai_enabled == "False":
            log.info("Starting generic_spider with MINIMAL settings. AI Services are DISABLED!")
            self.AI_ENABLED = False
            # this optional flag allows us to control if we want to use AI-suggested metadata. We can compare the
            # items gathered by the "generic_spider_minimal" against the (AI-enabled) "generic_spider"
            self.name = "generic_spider_minimal"
            self.friendlyName = "generic_spider_minimal"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=scrapy.signals.spider_opened)  # pylint: disable=no-member
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
            log.error("No database set or database not found. Please set GENERIC_CRAWLER_DB_PATH.")
            return

        if not self.filter_set_id:
            return

        log.info("Filter set ID: %s", self.filter_set_id)
        # List filter rules in this filter set
        connection = sqlite3.connect(db_path)

        matches = fetch_urls_passing_filterset(connection, self.filter_set_id)

        for row in matches:
            log.info("Adding URL to start_urls: %s", row.url)
            self.start_urls.append(row.url)

    def start_requests(self):
        url_from_dot_env = env.get(key="GENERIC_SPIDER_URL_TARGET", allow_null=True, default=None)
        if url_from_dot_env:
            log.info("Recognized URL to crawl from '.env'-Setting 'GENERIC_SPIDER_URL_TARGET': %s", url_from_dot_env)
            yield Request(url_from_dot_env, callback=self.parse)
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def getId(self, response=None) -> str:
        """Return a stable identifier (URI) of the crawled item"""
        return response.url

    def getHash(self, response=None) -> str:
        """
        Return a stable hash to detect content changes (for future crawls).
        """
        return f"{datetime.datetime.now().isoformat()}v{self.version}"

    async def parse(self, response: scrapy.http.Response, **kwargs):
        if not self.hasChanged(response):
            return

        # data_playwright = run_async(WebTools.fetchDataPlaywright, response.url)
        # this is playwrite_dict with 'content', 'screenshot_bytes' and so on
        

        url_data = await WebTools.getUrlData(response.url, engine=WebEngine.Playwright)

        # data_playwright = asyncio.run(WebTools.fetchDataPlaywright(response.url))
        response = response.copy()
        # ToDo: validate "trafilatura"-fulltext-extraction from playwright (compared to the html2text approach)
        # if data_playwright is None:
        #     log.warning("Playwright failed to fetch data for %s", response.url)
        #     data_playwright = {"content": ""}
        playwright_text: str = url_data["html"]
        playwright_bytes: bytes = playwright_text.encode()
        # trafilatura_text = trafilatura.extract(playwright_text)
        trafilatura_text = url_data["text"]
        log.info("trafilatura_text: %s", trafilatura_text)
        # ToDo: implement text extraction .env toggle: default / advanced / basic?
        #  - default: use trafilatura by default?
        #  - advanced: which trafilatura parameters could be used to improve text extraction for "weird" results?
        #  - basic: fallback to html2text extraction (explicit .env setting)
        # trafilatura_meta_scrapy = trafilatura.extract_metadata(response.body).as_dict()
        trafilatura_meta_playwright = trafilatura.extract_metadata(playwright_bytes)
        parsed_html = BeautifulSoup(url_data["html"], features="lxml")
        for tag in self.clean_tags:
            tags = parsed_html.find_all(tag) if parsed_html.find_all(tag) else []
            for t in tags:
                t.clear()
        crawler_ignore = parsed_html.find_all(name=None, attrs={"data-crawler": "ignore"})
        for t in crawler_ignore:
            t.clear()
        html = parsed_html.prettify()
        data = {
            # legacy, do we need these fields?
            "content": url_data["html"],
        }
        data["parsed_html"] = parsed_html
        data["text"] = WebTools.html2Text(html)
        data["trafilatura_text"] = trafilatura_text
        if trafilatura_meta_playwright:
            data["trafilatura_meta"] = trafilatura_meta_playwright.as_dict()
        response.meta["data"] = data

        selector_playwright = scrapy.Selector(text=playwright_text)
        robot_meta_tags: list[str] = selector_playwright.xpath("//meta[@name='robots']/@content").getall()
        respect_robot_meta_tags = env.get_bool(key="RESPECT_ROBOT_META_TAGS", allow_null=True, default=True)
        if robot_meta_tags:
            # There are 3 Robot Meta Tags (<meta name="robots" content="VALUE">) that we need to respect:
            # - "noindex"       (= don't index the current URL)
            # - "nofollow"      (= don't follow any links on this site)
            # - "none"          (= shortcut for combined value "noindex, nofollow")
            if respect_robot_meta_tags:
                # by default, we try to respect the webmaster's wish to not be indexed/crawled
                if "noindex" in robot_meta_tags:
                    log.info("Robot Meta Tag 'noindex' identified. Aborting further parsing of item: %s .", response.url)
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
                        "Aborting further parsing of item: %s itself and any links within it.", response.url
                    )
                    return

        base_loader = BaseItemLoader()
        base_loader.add_value("sourceId", self.getId(response))
        base_loader.add_value("hash", self.getHash(response))
        lrmi_thumbnail = self.getLRMI("thumbnailUrl", response=response)
        if lrmi_thumbnail:
            base_loader.add_value("thumbnail", lrmi_thumbnail)
        meta_og_image = selector_playwright.xpath('//meta[@property="og:image"]/@content').get()
        if meta_og_image:
            base_loader.add_value("thumbnail", meta_og_image)
        meta_last_modified = selector_playwright.xpath('//meta[@name="last-modified"]/@content').get()
        if meta_last_modified:
            base_loader.add_value("lastModified", meta_last_modified)

        # Creating the nested ItemLoaders according to our items.py data model
        lom_loader = LomBaseItemloader()
        general_loader = LomGeneralItemloader()
        technical_loader = LomTechnicalItemLoader()
        educational_loader = LomEducationalItemLoader()
        classification_loader = LomClassificationItemLoader()
        valuespace_loader = ValuespaceItemLoader()
        license_loader = LicenseItemLoader()
        permissions_loader = self.getPermissions(response)
        response_loader = ResponseItemLoader()
        kidra_loader = KIdraItemLoader()

        # ToDo: rework LRMI JSON-LD extraction
        #  - so it can handle websites when there are several JSON-LD containers within a single DOM
        # ToDo: try to grab as many OpenGraph metadata properties as possible (for reference, see: https://ogp.me)

        general_loader.add_value('title', response.xpath('/html/head/title/text()').get())
        # general_loader.add_value("title", response.meta["data"]["title"])
        html_language = selector_playwright.xpath("//html/@lang").get()
        meta_locale = selector_playwright.xpath('//meta[@property="og:locale"]/@content').get()
        # HTML language and locale properties haven proven to be pretty inconsistent, but they might be useful as
        # fallback values.
        # ToDo: websites might return languagecodes as 4-char values (e.g. "de-DE") instead of the 2-char value "de"
        #       -> we will have to detect/clean up languageCodes to edu-sharing's expected 2-char format
        lrmi_language = self.getLRMI("inLanguage", response=response)
        if lrmi_language:
            general_loader.add_value("language", lrmi_language)
        elif html_language:
            general_loader.add_value("language", html_language)
        elif meta_locale:
            general_loader.add_value("language", meta_locale)
        lrmi_description = self.getLRMI("description", "about", response=response)
        if lrmi_description:
            general_loader.add_value("description", lrmi_description)
        lrmi_keywords: list[str] = self.getLRMI("keywords", response=response)
        if lrmi_keywords:
            general_loader.add_value("keyword", lrmi_keywords)

        if self.AI_ENABLED:
            general_loader.add_value(
                "description", self.resolve_z_api("description", response, base_itemloader=base_loader)
            )
            general_loader.add_value(
                "keyword", self.resolve_z_api("keyword", response, base_itemloader=base_loader, split=True)
            )
            curriculum = self.resolve_z_api("curriculum", response, base_itemloader=base_loader, split=True)
            kidra_loader.add_value("curriculum", curriculum)
            # valuespace_loader.add_value(
            #     "curriculum", self.valuespaces.findInText("curriculum", curriculum)
            # )
            classification, reading_time = self.resolve_z_api("textStatistics", response, base_itemloader=base_loader, split=True)
            kidra_loader.add_value("text_difficulty", classification)
            kidra_loader.add_value("text_reading_time", reading_time)
            ki_disciplines = self.resolve_z_api("kidraDisciplines", response, base_itemloader=base_loader, split=True)
            kidra_loader.add_value("kidraDisciplines", ki_disciplines)
            # ToDo: map/replace the previously set 'language'-value by AI suggestions from Z-API?

            # ToDo: keywords will (often) be returned as a list of bullet points by the AI
            #  -> we might have to detect & clean up the string first
        else:
            if response.meta["data"]:
                if "trafilatura_meta" in response.meta["data"]:
                    if "description" in response.meta["data"]["trafilatura_meta"]:
                        trafilatura_description = response.meta["data"]["trafilatura_meta"]["description"]
                        general_loader.add_value("description", trafilatura_description)
                    if "title" in response.meta["data"]["trafilatura_meta"]:
                        trafilatura_title: str = response.meta["data"]["trafilatura_meta"]["title"]
                        general_loader.replace_value("title", trafilatura_title)

        lom_loader.add_value("general", general_loader.load_item())

        lrmi_file_format = self.getLRMI("fileFormat", response=response)
        if lrmi_file_format:
            technical_loader.add_value("format", lrmi_file_format)
        lrmi_content_size = self.getLRMI("ContentSize", response=response)
        if lrmi_content_size:
            technical_loader.add_value("size", lrmi_content_size)
        lrmi_url = self.getLRMI("url", response=response)
        if lrmi_url:
            technical_loader.add_value("location", lrmi_url)
        technical_loader.add_value("location", response.url)
        technical_loader.replace_value("format", "text/html")  # ToDo: do we really want to hard-code this?
        technical_loader.replace_value("size", len(response.body))
        # ToDo: 'size' should probably use the length of our playwright response, not scrapy's response.body
        meta_og_url = selector_playwright.xpath('//meta[@property="og:url"]/@content').get()
        if meta_og_url != response.url:
            technical_loader.add_value("location", meta_og_url)

        self.get_lifecycle_author(lom_loader=lom_loader, selector=selector_playwright, response=response)

        self.get_lifecycle_publisher(lom_loader=lom_loader, selector=selector_playwright, response=response)

        # we might be able to extract author/publisher information from typical <meta> or <head> fields in the DOM
        lom_loader.add_value("educational", educational_loader.load_item())
        lom_loader.add_value("classification", classification_loader.load_item())
        lom_loader.add_value("technical", technical_loader.load_item())
        # after LomBaseItem is filled with nested metadata, we build the LomBaseItem and add it to our BaseItem:
        base_loader.add_value("lom", lom_loader.load_item())

        meta_author = selector_playwright.xpath('//meta[@name="author"]/@content').getall()
        if meta_author:
            license_loader.add_value("author", meta_author)
        # trafilatura offers a license detection feature as part of its "extract_metadata()"-method
        if response.meta["data"]:
            if "trafilatura_meta" in response.meta["data"]:
                if "license" in response.meta["data"]["trafilatura_meta"]:
                    trafilatura_license_detected: str = response.meta["data"]["trafilatura_meta"]["license"]
                    if trafilatura_license_detected:
                        license_mapper = LicenseMapper()
                        license_url_mapped = license_mapper.get_license_url(
                            license_string=trafilatura_license_detected
                        )
                        if license_url_mapped:
                            # ToDo: this is a really risky assignment! Validation of trafilatura's license detection
                            #  will be necessary! (this is a metadata field that needs to be confirmed by a human!)
                            license_loader.add_value("url", license_url_mapped)

        lrmi_lrt = self.getLRMI("learningResourceType", response=response)
        if lrmi_lrt:
            valuespace_loader.add_value("learningResourceType", lrmi_lrt)
        # lrmi_intended_end_user_role = self.getLRMI("audience.educationalRole", response=response)  # ToDo: rework
        # # attention: serlo URLs will break the getLRMI() Method because JSONBase cannot extract the JSON-LD properly
        # # ToDo: maybe use the 'jmespath' Python package to retrieve this value more reliably
        # if lrmi_intended_end_user_role:
        #     valuespace_loader.add_value("intendedEndUserRole", lrmi_intended_end_user_role)
        if self.AI_ENABLED:
            for v in ["educationalContext", "discipline", "intendedEndUserRole", "new_lrt"]:
                valuespace_loader.add_value(
                    v, self.valuespaces.findInText(v, self.resolve_z_api(v, response, base_itemloader=base_loader))
                )
            base_loader.add_value("kidra_raw", kidra_loader.load_item())

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
        # once all scrapy.Items are loaded into our "base", we yield the BaseItem by calling the .load_item() method
        yield base_loader.load_item()

    def get_lifecycle_publisher(
        self, lom_loader: LomBaseItemloader, selector: scrapy.Selector, response: scrapy.http.Response
    ):
        meta_publisher = selector.xpath('//meta[@name="publisher"]/@content').get()
        if meta_publisher:
            lifecycle_publisher_loader = LomLifecycleItemloader()
            lifecycle_publisher_loader.add_value("role", "publisher")
            lifecycle_publisher_loader.add_value("organization", meta_publisher)
            self.get_lifecycle_date(lifecycle_loader=lifecycle_publisher_loader, selector=selector, response=response)

            lom_loader.add_value("lifecycle", lifecycle_publisher_loader.load_item())

    def get_lifecycle_author(
        self, lom_loader: LomBaseItemloader, selector: scrapy.Selector, response: scrapy.http.Response
    ):
        meta_author = selector.xpath('//meta[@name="author"]/@content').get()
        if meta_author:
            lifecycle_author_loader = LomLifecycleItemloader()
            lifecycle_author_loader.add_value("role", "author")
            # author strings could be one or several names or organizations. The license loader expects a 'firstName'.
            lifecycle_author_loader.add_value("firstName", meta_author)
            # ToDo: (optional) try determining if names need to be sorted into
            #  'firstName', 'lastName' or 'organization'-field-values
            # ToDo: shoving the whole string into 'firstName' is a hacky approach that will cause organizations
            #  to appear as persons within the "lifecycle"-metadata. fine-tune this approach later.
            self.get_lifecycle_date(lifecycle_loader=lifecycle_author_loader, selector=selector, response=response)

            lom_loader.add_value("lifecycle", lifecycle_author_loader.load_item())

    @staticmethod
    def get_lifecycle_date(lifecycle_loader: LomLifecycleItemloader, selector: scrapy.Selector, response):
        if "date" in response.meta["data"]["trafilatura_meta"]:
            # trafilatura's metadata extraction scans for dates within <meta name="date" content"..."> Elements
            date = selector.xpath('//meta[@name="date"]/@content').get()
            date_trafilatura: str = response.meta["data"]["trafilatura_meta"]["date"]
            if date_trafilatura:
                lifecycle_loader.add_value("date", date_trafilatura)
            elif date:
                lifecycle_loader.add_value("date", date)

    def resolve_z_api(self, field: str, response: scrapy.http.Response, base_itemloader: BaseItemLoader, split=False):
        if field == "curriculum":
            text = {"text": response.meta["data"]["text"][:4000]}
            result = self.z_api_kidra.topics_flat_topics_flat_post(text)
            result_dict = result.to_dict()
            result = self.parse_topics(result_dict)
            return result
        elif field == "textStatistics":
            text = response.meta["data"]["text"][:4000]
            body = {"text": text, "reading_speed": 200, "generate_embeddings": False}
            result = self.z_api_kidra.text_stats_analyze_text_post(body)
            result_dict = result.to_dict()
            classification, reading_time = self.parse_text_statistics(result_dict)
            return classification, reading_time
        elif field == "kidraDisciplines":
            text = response.meta["data"]["text"][:4000]
            body = {"text": text}
            result = self.z_api_kidra.predict_subjects_kidra_predict_subjects_post(body)
            result_dict = result.to_dict()
            result = self.parse_kidra_disciplines(result_dict, score_threshold=0.3)
            return result
        else:
            ai_prompt_itemloader = AiPromptItemLoader()
            ai_prompt_itemloader.add_value("field_name", field)
            prompt = self.prompts[field] % {"text": response.meta["data"]["text"][:4000]}
            # ToDo: figure out a reasonable cutoff-length
            # (prompts which are too long get thrown out by the AI services)
            ai_prompt_itemloader.add_value("ai_prompt", prompt)

            result = self.z_api_text.prompt(body=prompt)
            result = result.responses[0].strip()
            ai_prompt_itemloader.add_value("ai_response_raw", result)
            # ToDo: error-handling when there is no valid response that we could return as a result

            # fix utf-8 chars
            # result = codecs.decode(result, 'unicode-escape')
            # data['text'] = data['text'].encode().decode('unicode-escape').encode('latin1').decode('utf-8')
            if split:
                result = list(map(lambda x: x.strip(), re.split(r"[,|\n]", result)))
                # ToDo: fix 'split'-parameter:
                #  - keyword-strings need to be split up in a cleaner way, this approach isn't precise enough for Serlo URLs
            ai_prompt_itemloader.add_value("ai_response", result)
            base_itemloader.add_value("ai_prompts", ai_prompt_itemloader.load_item())
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
            base_loader.load_item()['kidra_raw']['text_difficulty'] = text_difficulty
        if len(self.results_dict['text_reading_time']) != 0:
            text_reading_time = self.results_dict['text_reading_time']
            base_loader.load_item()['kidra_raw']['text_reading_time'] = text_reading_time

        base_loader.load_item()['lom']['general']['title'] = title
        base_loader.load_item()['lom']['general']['description'] = description
        base_loader.load_item()['lom']['general']['keyword'] = keywords
        base_loader.load_item()['valuespaces']['new_lrt'] = new_lrt
        base_loader.load_item()['valuespaces']['educationalContext'] = educational_context
        base_loader.load_item()['valuespaces']['intendedEndUserRole'] = intendedEndUserRole
        base_loader.load_item()['license'] = license
        # base_loader.load_item()['valuespaces']['curriculum'] = curriculum
        base_loader.load_item()['kidra_raw']['curriculum'] = curriculum

        return base_loader

    def parse_topics(self, topics_result, n_topics = 3):
        topics = topics_result["topics"][:n_topics]
        topic_names = [topic['uri'] for topic in topics]
        return topic_names

    def parse_text_statistics(self, statistics_result):
        classification = statistics_result["classification"]
        reading_time = statistics_result["reading_time"]
        reading_time = "{:.2f}".format( reading_time )
        return classification, float(reading_time)

    def parse_kidra_disciplines(self, disciplines_result, score_threshold=0.6):
        uri_discipline = 'http://w3id.org/openeduhub/vocabs/discipline/'
        disciplines = disciplines_result["disciplines"]
        discipline_names = []
        for discipline in disciplines:
            score = discipline['score']
            if score > score_threshold:
                discipline_names.append( uri_discipline+discipline['id'] )

        return discipline_names

# class RunThread(threading.Thread):
#     def __init__(self, func, args, kwargs):
#         self.func = func
#         self.args = args
#         self.kwargs = kwargs
#         self.result = None
#         super().__init__()

#     def run(self):
#         self.result = asyncio.run(self.func(*self.args, **self.kwargs))

# def run_async(func, *args, **kwargs):
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = None
#     if loop and loop.is_running():
#         thread = RunThread(func, args, kwargs)
#         thread.start()
#         thread.join()
#         return thread.result
#     else:
#         return asyncio.run(func(*args, **kwargs))

def get_urls_from_string(urls_string):
    urls = urls_string.split(",")
    urls_list = []
    for url in urls:
        urls_list.append( url.strip() )
    return urls_list
