import asyncio
import logging
import re
from typing import Any

import scrapy.http
import trafilatura
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import Rule, Spider

import z_api
from util.license_mapper import LicenseMapper
from valuespace_converter.app.valuespaces import Valuespaces
from .base_classes import LrmiBase
from .. import env
from ..items import LicenseItemLoader
from ..web_tools import WebEngine, WebTools


# class GenericSpider(CrawlSpider, LrmiBase):


class GenericSpider(Spider, LrmiBase):
    name = "generic_spider"
    friendlyName = "generic_spider"  # name as shown in the search ui
    version = "0.1.2"
    start_urls = [
        "https://www.planet-schule.de/schwerpunkt/total-phaenomenal-energie/sonnenenergie-film-100.html",  # the original Hackathon example URL
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

    def __init__(self, **kwargs):
        # CrawlSpider.__init__(self, **kwargs)

        LrmiBase.__init__(self, **kwargs)

        self.valuespaces = Valuespaces()
        # ToDo: optional .env Feature: "generic_spider" (AI=enabled) <-> "generic_minimal_spider" (AI=disabled)?
        ai_enabled: bool = env.get_bool(key="GENERIC_SPIDER_AI_ENABLED", allow_null=True, default=True)
        if ai_enabled:
            self.AI_ENABLED = True
            logging.info(f"Starting generic_spider with AI_ENABLED flag!")
            z_api_config = z_api.Configuration.get_default_copy()
            z_api_config.api_key = {"ai-prompt-token": env.get("Z_API_KEY", False)}
            z_api_client = z_api.ApiClient(configuration=z_api_config)
            self.z_api_text = z_api.AITextPromptsApi(z_api_client)
        elif ai_enabled is False:
            logging.info(f"Starting generic_spider with MINIMAL settings. AI Services are DISABLED!")
            self.AI_ENABLED = False
            # this optional flag allows us to control if we want to use AI-suggested metadata. We can compare the
            # items gathered by the "generic_spider_minimal" against the (AI-enabled) "generic_spider"
            self.name = "generic_spider_minimal"
            self.friendlyName = "generic_spider_minimal"

    def start_requests(self):
        url_from_dot_env = env.get(key="GENERIC_SPIDER_URL_TARGET", allow_null=True, default=None)
        if url_from_dot_env:
            logging.info(f"Recognized URL to crawl from '.env'-Setting 'GENERIC_SPIDER_URL_TARGET': {url_from_dot_env}")
            yield Request(url_from_dot_env, callback=self.parse)
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response: scrapy.http.Response, **kwargs) -> Any | None:
        if not self.hasChanged(response):
            return
        data_playwright = asyncio.run(WebTools.fetchDataPlaywright(response.url))
        response = response.copy()
        # ToDo: validate "trafilatura"-fulltext-extraction from playwright (compared to the html2text approach)
        playwright_text: str = data_playwright["content"]
        playwright_bytes: bytes = playwright_text.encode()
        text_trafilatura = trafilatura.extract(playwright_text)
        trafilatura_meta_scrapy = trafilatura.extract_metadata(response.body).as_dict()
        trafilatura_meta_playwright = trafilatura.extract_metadata(playwright_bytes).as_dict()
        parsed_html = BeautifulSoup(data_playwright["content"], features="lxml")
        for tag in self.clean_tags:
            tags = parsed_html.find_all(tag) if parsed_html.find_all(tag) else []
            for t in tags:
                t.clear()
        crawler_ignore = parsed_html.find_all(name=None, attrs={"data-crawler": "ignore"})
        for t in crawler_ignore:
            t.clear()
        html = parsed_html.prettify()
        data_playwright["parsed_html"] = parsed_html
        data_playwright["text"] = WebTools.html2Text(html)
        data_playwright["text_trafilatura"] = text_trafilatura
        data_playwright["trafilatura_meta"] = trafilatura_meta_playwright
        response.meta["data"] = data_playwright

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
                    logging.info(
                        f"Robot Meta Tag 'noindex' identified. Aborting further parsing of item: " f"{response.url} ."
                    )
                    return None
                if "nofollow" in robot_meta_tags:
                    # ToDo: don't follow any links, but parse the current response
                    #  -> yield response with 'nofollow'-setting in cb_kwargs
                    logging.info(
                        f"Robot Meta Tag 'nofollow' identified. Parsing item {response.url} , but WILL NOT "
                        f"follow any links found within."
                    )
                    pass
                if "none" in robot_meta_tags:
                    logging.info(
                        f"Robot Meta Tag 'none' identified (= 'noindex, nofollow'). "
                        f"Aborting further parsing of item: {response.url} itself and any links within it."
                    )
                    return None

        return LrmiBase.parse(self, response)

    # return a (stable) id of the source
    def getId(self, response):
        return response.url

    # return a stable hash to detect content changes
    # if there is no hash available, may use the current time as "always changing" info
    # Please include your crawler version as well
    def getHash(self, response):
        # ToDo: append the current date to the hash?
        return self.version

    def getBase(self, response):
        base = LrmiBase.getBase(self, response)
        # optionally provide thumbnail. If empty, it will tried to be generated from the getLOMTechnical 'location' (if format is 'text/html')
        # base.add_value('thumbnail', 'https://url/to/thumbnail')
        return base

    def mapResponse(self, response):
        return LrmiBase.mapResponse(self, response, False)

    def getLOMGeneral(self, response):
        general = LrmiBase.getLOMGeneral(self, response)
        general.add_value("title", response.meta["data"]["title"])
        # TODO: Map language based on z-api
        html_language: str = response.xpath("//html/@lang").get()
        meta_locale: str = response.xpath('//meta[@property="og:locale"]/@content').get()
        # HTML language and locale properties haven proven to be pretty inconsistent, but they might be useful as
        # fallback values.
        # ToDo: websites might return languagecodes as 4-char values (e.g. "de-DE") instead of the 2-char value "de"
        #       -> we will have to detect/clean up languageCodes to edu-sharing's expected 2-char format
        if html_language:
            general.add_value("language", html_language)
        elif meta_locale:
            general.add_value("language", meta_locale)
        else:
            # ToDo: replace this fallback value when using the AI_enabled flag
            general.add_value("language", "de")
        if self.AI_ENABLED:
            general.add_value("description", self.resolve_z_api("description", response))
            general.add_value("keyword", self.resolve_z_api("keyword", response, split=True))
            # ToDo: keywords will (often) be returned as a list of bullet points by the AI -> clean up the string first
        elif self.AI_ENABLED is False:
            if response.meta["data"]:
                if "trafilatura_meta" in response.meta["data"]:
                    if "description" in response.meta["data"]["trafilatura_meta"]:
                        trafilatura_description = response.meta["data"]["trafilatura_meta"]["description"]
                        general.add_value("description", trafilatura_description)
                    if "title" in response.meta["data"]["trafilatura_meta"]:
                        trafilatura_title: str = response.meta["data"]["trafilatura_meta"]["title"]
                        general.replace_value("title", trafilatura_title)
        return general

    def getLicense(self, response) -> LicenseItemLoader:
        license = LrmiBase.getLicense(self, response)
        author = response.meta["data"]["parsed_html"].find("meta", {"name": "author"})
        if author:
            license.add_value("author", author.get_text())
        # trafilatura offers a license detection feature as part of its "extract_metadata()"-method
        if response.meta["data"]:
            if "trafilatura_meta" in response.meta["data"]:
                if "license" in response.meta["data"]["trafilatura_meta"]:
                    trafilatura_license_detected: str = response.meta["data"]["trafilatura_meta"]["license"]
                    if trafilatura_license_detected:
                        license_mapper = LicenseMapper()
                        license_url_mapped: str = license_mapper.get_license_url(
                            license_string=trafilatura_license_detected
                        )
                        if license_url_mapped:
                            # ToDo: this is a really risky assignment! Validation of trafilatura's license detection
                            #  will be necessary! (this is a metadata field that needs to be confirmed by a human!)
                            license.add_value("url", license_url_mapped)
        return license

    def getLOMTechnical(self, response):
        technical = LrmiBase.getLOMTechnical(self, response)
        technical.replace_value("location", response.url)
        technical.replace_value("format", "text/html")
        technical.replace_value("size", len(response.body))
        return technical

    def getValuespaces(self, response):
        valuespaces = LrmiBase.getValuespaces(self, response)
        if self.AI_ENABLED:
            for v in ["educationalContext", "discipline", "educationalContext", "intendedEndUserRole", "new_lrt"]:
                valuespaces.add_value(v, self.valuespaces.findInText(v, self.resolve_z_api(v, response)))
        return valuespaces

    def resolve_z_api(self, field, response, split=False):
        prompt = self.prompts[field] % {"text": response.meta["data"]["text"][:4000]}
        # ToDo: figure out a reasonable cutoff-length
        # (prompts which are too long get thrown out by the AI services)
        result = self.z_api_text.prompt(body=prompt)
        logging.info(result)
        result = result.responses[0].strip()
        # fix utf-8 chars
        # result = codecs.decode(result, 'unicode-escape')
        # data['text'] = data['text'].encode().decode('unicode-escape').encode('latin1').decode('utf-8')
        # ToDo: (.csv or .json) pipeline to store the (raw) AI Prompts and answers we received for an item
        if split:
            result = list(map(lambda x: x.strip(), re.split(r"[,|\n]", result)))
        return result
