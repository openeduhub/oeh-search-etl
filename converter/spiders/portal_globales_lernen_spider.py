import datetime
import re
from typing import Any, Iterable

import scrapy
import trafilatura
from scrapy import Request

from converter.constants import Constants
from converter.items import (
    BaseItemLoader,
    LomBaseItemloader,
    LomGeneralItemloader,
    LomTechnicalItemLoader,
    LomLifecycleItemloader,
    LomEducationalItemLoader,
    ValuespaceItemLoader,
    LicenseItemLoader,
    ResponseItemLoader,
    PermissionItemLoader,
    LomClassificationItemLoader,
)
from converter.spiders.base_classes import LomBase
from converter.web_tools import WebEngine


class PortalGlobalesLernenSpider(scrapy.Spider, LomBase):
    """
    Crawler for "Portal Globales Lernen" (https://www.globaleslernen.de)
    """

    name = "portal_globales_lernen_spider"
    friendlyName = "Portal für Globales Lernen"
    version = "0.0.5"  # last update: 2025-01-10

    playwright_cookies: list[dict] = [
        {
            "name": "cookiesjsr",
            "value": "%7B%22functional%22%3Afalse%2C%22recaptcha%22%3Afalse%2C%22analytics%22%3Afalse%7D",
        }
    ]
    # Portal für Globales Lernen uses "Drupal 10" as their CMS and the "COOKiES Consent Management"-Module.
    # see: https://www.drupal.org/project/cookies & https://github.com/jfeltkamp/cookiesjsr
    # When clicking the "reject all"-button, a "callback.json"-payload is sent and all subsequent HTTP requests
    # send along the above "cookiesjsr"-cookie to hide the consent management banner from popping up again.
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 2,
        "WEB_TOOLS": WebEngine.Playwright,
        "PLAYWRIGHT_COOKIES": playwright_cookies,
        # "ROBOTSTXT_OBEY": False,
        # "COOKIES_DEBUG": True,
    }

    BILDUNGSBEREICH_TO_EDUCATIONAL_CONTEXT: dict = {
        "frühkindliche bildung": "elementarbereich",
    }

    FORMAT_TO_NEW_LRT: dict = {
        "bildungsmaterial": "1846d876-d8fd-476a-b540-b8ffd713fedb",  # Material
        "aktion": "955590ae-5f06-4513-98e9-91dfa8d5a05e",  # "Termin, Event und Veranstaltung"
        "app": "cefccf75-cba3-427d-9a0f-35b4fedcbba1",  # Tool
        "außerschulischer lernort": "92dcc3ec-fe94-451c-95ac-ea305e0e7597",  # "außerschulisches Angebot"
        "ausstellung": "c903a62a-17b0-4646-b2b8-a1a02a84e8cc",  # "außerschulisches Angebot (Bildungsangebot)"
        "austauschprogramm": "c903a62a-17b0-4646-b2b8-a1a02a84e8cc",  # "außerschulisches Angebot (Bildungsangebot)"
        "beratungsangebot": "c903a62a-17b0-4646-b2b8-a1a02a84e8cc",  # "außerschulisches Angebot (Bildungsangebot)"
        "bericht": "b98c0c8c-5696-4537-82fa-dded7236081e",  # "Artikel und Einzelpublikation"
        "beschluss": "0f519bd5-069c-4d32-b6d3-a373ac96724c",  # "Fachliche News"
        "bildungsserver": "3869b453-d3c1-4b34-8f25-9127e9d68766",  # "Quelle"
        "broschüre/handreichung": "6a15628c-0e59-43e3-9fc5-9a7f7fa261c4",  # "Skript, Handout und Handreichung"
        "datenbank": "ac0ad1e8-d1a2-42f2-961e-5aa9b8157fa5",  # "Datenbank"
        "evaluierung/wirkungsbeobachtung": "0f519bd5-069c-4d32-b6d3-a373ac96724c",  # "Fachliche News"
        "fachpublikation": "b98c0c8c-5696-4537-82fa-dded7236081e",  # "Artikel und Einzelpublikation"
        "fachpublikation globales lernen / bne": "b98c0c8c-5696-4537-82fa-dded7236081e",  # "Artikel und Einzelpublikation"
        "film mit begleitmaterial": "7a6e9608-2554-4981-95dc-47ab9ba924de",  # "Video (Material)"
        "fortbildung/weiterbildung": "4fe167ea-1f40-44b7-8c17-355f256b4fc9",  # "Fortbildungsangebot"
        "freiwilligendienst": "c903a62a-17b0-4646-b2b8-a1a02a84e8cc",  # "außerschulisches Angebot (Bildungsangebot)"
        "informations- und lernplattform": "d8c3ef03-b3ab-4a5e-bcc9-5a546fefa2e9",  # "Webseite"
        "kampagne": "c903a62a-17b0-4646-b2b8-a1a02a84e8cc",  # "außerschulisches Angebot (Bildungsangebot)"
        "lernkiste/-koffer": "5098cf0b-1c12-4a1b-a6d3-b3f29621e11d",  # "Unterrichtsbaustein"
        "methodensammlung/-handbuch": "5098cf0b-1c12-4a1b-a6d3-b3f29621e11d",  # "Unterrichtsbaustein"
        "multimediales": [
            "ec2682af-08a9-4ab1-a324-9dca5151e99f",  # Audio
            "7a6e9608-2554-4981-95dc-47ab9ba924de",  # Video
        ],
        "online-spiel/online-kurs": "4e16015a-7862-49ed-9b5e-6c1c6e0ffcd1",  # Kurs
        # "open educational resource – oer": "",
        "plan- und gesellschaftsspiel": "a120ce77-59f5-4564-8d49-73f4a0de1594",  # "Lernen, Quiz und Spiel"
        "podcast": "6e821748-ad12-4ac1-bb14-9b54493e2c50",  # "Radio, Podcastfolge und Interview"
        "poster": "c382a478-74e0-42f1-96dd-fcfb5c27f746",  # "Poster und Plakat"
        "projektfinanzierung": "0f519bd5-069c-4d32-b6d3-a373ac96724c",  # "fachliche News"
        "projekttage/-wochen": "22823ca9-7175-4b24-892e-19ebbf5fe0e7",  # "Projekt (Lehr- und Lernmaterial)"
        "rahmenvereinbarungen": "0f519bd5-069c-4d32-b6d3-a373ac96724c",  # "Fachliche News"
        # "referentinnenvermittlung": "",
        "schulauszeichnung/schulprofilbildung": "0f519bd5-069c-4d32-b6d3-a373ac96724c",  # "Fachliche News"
        "schulentwicklung": "0f519bd5-069c-4d32-b6d3-a373ac96724c",  # "Fachliche News"
        "schulpartnerschaften": "0f519bd5-069c-4d32-b6d3-a373ac96724c",  # Fachliche News
        "studie": "b98c0c8c-5696-4537-82fa-dded7236081e",  # "Artikel und Einzelpublikation"
        "studiengang": "337eb29c-1ea8-41dc-9caf-e469eea29177",  # "Studiengang"
        "umsetzungsprojekt / länderinitiative (OR)": "0f519bd5-069c-4d32-b6d3-a373ac96724c",  # "Fachliche News"
        "veranstaltung": "955590ae-5f06-4513-98e9-91dfa8d5a05e",  # "Termin, Event und Veranstaltung"
        "videoclip/erklärvideo": "a0218a48-a008-4975-a62a-27b1a83d454f",  # "Erklärvideo und gefilmtes Experiment"
        "wettbewerb": "81578410-73df-4320-83fd-2e6e0c0fd189",  # Wettbewerbe
    }

    SCHULFACH_TO_DISCIPLINE: dict = {
        "fächerübergreifend": "720",  # "Allgemein"
        "politische bildung": "480",  # Politik
        "religion / ethik": ["520", "160"],  # Religion / Ethik
        "wirtschaft": "700",
    }

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self) -> Iterable[Request]:
        url_suche_bildungsmaterialien: str = (
            "https://www.globaleslernen.de/de/suche?combine="
            "&field_media_types_target_id%5B0%5D=2636"
            "&field_media_types_target_id%5B1%5D=2636"
            "&field_media_types_target_id%5B2%5D=2636"
            "&field_media_types_target_id%5B3%5D=2636"
        )
        url_suche: str = "https://www.globaleslernen.de/de/suche"
        yield scrapy.Request(
            url=url_suche_bildungsmaterialien, callback=self.gather_urls_from_first_page_of_search_results
        )

    def gather_urls_from_first_page_of_search_results(self, response: scrapy.http.HtmlResponse):
        last_page_link: str | None = response.xpath(
            "//nav[@class='pager']/ul/li[@class='pager__item pager__item--last']/a/@href"
        ).get()
        last_page_number: int | None = None
        page_number_pattern = re.compile(r"""page=(?P<page_number>\d+)$""")
        if last_page_link:
            regex_result = page_number_pattern.search(last_page_link)
            if regex_result and "page_number" in regex_result.groupdict():
                last_page_str: str = regex_result.groupdict()["page_number"]
                last_page_number: int = int(last_page_str)
            else:
                self.logger.error(
                    f"Failed to retrieve 'Last Page'-number via RegEx. Please check if the page parameter"
                    f" is still available within the relative URL: {last_page_link}"
                )
        else:
            self.logger.error(
                f"Failed to retrieve 'Last Page'-Button href from search overview at {response.url} . "
                f"(The crawler cannot navigate through the search results without this href element, "
                f"please check the XPath-expression with a debugger!)"
            )
        overview_urls: list[str] = list()
        if last_page_number:
            overview_url_without_page_param = re.sub(pattern=page_number_pattern, repl="", string=last_page_link)
            for overview_page_number in range(1, last_page_number + 1):
                # result iteration starts at page 0
                overview_relative_url: str = f"{overview_url_without_page_param}page={overview_page_number}"
                overview_absolute_url: str = response.urljoin(overview_relative_url)
                overview_urls.append(overview_absolute_url)
                yield scrapy.Request(
                    url=overview_absolute_url, callback=self.gather_item_urls_from_search_result_overview, priority=1
                )
        yield from self.gather_item_urls_from_search_result_overview(response)

    def gather_item_urls_from_search_result_overview(self, response: scrapy.http.HtmlResponse):
        search_results: list[str] | None = response.xpath("//div[@class='edu-tit']//a/@href").getall()
        if search_results:
            # each complete page of search results typically contains 6 items
            for search_result_relative_url in search_results:
                item_url: str = response.urljoin(search_result_relative_url)
                yield scrapy.Request(url=item_url, callback=self.parse)

    def getId(self, response=None) -> str:
        # PGL does not provide an identifier for their items; therefore, we resort to the URL
        return response.url

    def getHash(self, response=None) -> str:
        # PGL does not provide 'datePublished' or 'dateModified' metadata in their DOM.
        now = datetime.datetime.now().isoformat()
        hash_value: str = f"{now}v{self.version}"
        return hash_value

    def parse(self, response: scrapy.http.HtmlResponse, **kwargs: Any) -> Any:
        trafilatura_fulltext = trafilatura.extract(filecontent=response.body)

        if self.shouldImport(response) is False:
            self.logger.debug(f"Skipping entry {self.getId(response)} because shouldImport() returned False")
            return None
        if self.getId(response) is not None and self.getHash(response) is not None:
            if not self.hasChanged(response):
                return None

        keyword_set: set[str] = set()
        # DOM (Header) metadata
        meta_description: str | None = response.xpath("//meta[@name='description']/@content").get()
        html_language: str | None = response.xpath("//html/@lang").get()
        # DOM (body) metadata:
        pgl_bildungsbereich: list[str] | None = response.xpath("//div[@class='edu-field2 edu-tar']/text()").getall()
        educontext_set: set[str] | None = set()
        if pgl_bildungsbereich and isinstance(pgl_bildungsbereich, list):
            for bb_item in pgl_bildungsbereich:
                if bb_item and isinstance(bb_item, str):
                    if "außerschulische" in bb_item or "bildungsübergreifende" in bb_item:
                        # adding these values to the keyword set before the string is transformed to lowercase
                        keyword_set.add(bb_item)
                    bb_item = bb_item.lower()
                    if bb_item in self.BILDUNGSBEREICH_TO_EDUCATIONAL_CONTEXT:
                        bb_mapped: str = self.BILDUNGSBEREICH_TO_EDUCATIONAL_CONTEXT.get(bb_item)
                        educontext_set.add(bb_mapped)
                    else:
                        educontext_set.add(bb_item)
        pgl_thema: list[str] | None = response.xpath("//div[@class='edu-field2 edu-top']/text()").getall()
        if pgl_thema and isinstance(pgl_thema, list):
            keyword_set.update(pgl_thema)
        pgl_format: list[str] | None = response.xpath("//div[@class='edu-field2 edu-typ']/text()").getall()
        new_lrt_mapped: set[str] = set()
        if pgl_format and isinstance(pgl_format, list):
            for pgl_format_item in pgl_format:
                if pgl_format_item and isinstance(pgl_format_item, str):
                    # since most "Format" values are specific enough to provide their own semantic context,
                    # we save all strings to our keywords, no matter if they can be mapped or not:
                    keyword_set.add(pgl_format_item)
                    # to increase the long-term reliability of our mapping, we cast all strings to lowercase chars:
                    pgl_format_item = pgl_format_item.lower()
                if pgl_format_item in self.FORMAT_TO_NEW_LRT:
                    pgl_format_mapped: str | list[str] = self.FORMAT_TO_NEW_LRT.get(pgl_format_item)
                    if pgl_format_mapped and isinstance(pgl_format_mapped, str):
                        new_lrt_mapped.add(pgl_format_mapped)
                    if pgl_format_mapped and isinstance(pgl_format_mapped, list):
                        new_lrt_mapped.update(pgl_format_mapped)
        pgl_land: list[str] | None = response.xpath("//div[@class='edu-field2 edu-cou']/text()").getall()
        if pgl_land and isinstance(pgl_land, list):
            keyword_set.update(pgl_land)
        pgl_sdg: list[str] | None = response.xpath("//div[@class='edu-field2 edu-sdg']/text()").getall()
        if pgl_sdg and isinstance(pgl_sdg, list):
            keyword_set.update(pgl_sdg)
        pgl_author: str | None = response.xpath("//div[@class='edu-field2 edu-aut']/text()").get()
        pgl_erscheinungsjahr: str | None = response.xpath("//div[@class='edu-field2 edu-dat']/text()").get()
        pgl_schulfach: list[str] | None = response.xpath("//div[@class='edu-field2 edu-sub']/text()").getall()
        disciplines: set[str] | None = set()
        if pgl_schulfach and isinstance(pgl_schulfach, list):
            for schulfach_item in pgl_schulfach:
                if schulfach_item and isinstance(schulfach_item, str):
                    schulfach_item = schulfach_item.lower()
                if schulfach_item in self.SCHULFACH_TO_DISCIPLINE:
                    schulfach_mapped: str | list[str] = self.SCHULFACH_TO_DISCIPLINE.get(schulfach_item)
                    if schulfach_mapped and isinstance(schulfach_mapped, list):
                        # example: the PGL value "Religion / Ethik" needs to be mapped to two separate values
                        disciplines.update(schulfach_mapped)
                    elif schulfach_mapped and isinstance(schulfach_mapped, str):
                        disciplines.add(schulfach_mapped)
                else:
                    # this case should be the most common one (since there are only a few mappings necessary)
                    disciplines.add(schulfach_item)
        pgl_thumbnail: str | None = response.xpath("//div[@class='edu-mat']/a/img/@src").get()

        # Loading up the item with metadata starts here:
        base_itemloader: BaseItemLoader = BaseItemLoader()
        base_itemloader.add_value("sourceId", self.getId(response=response))
        base_itemloader.add_value("hash", self.getHash(response=response))
        if pgl_thumbnail:
            thumbnail_url: str = response.urljoin(pgl_thumbnail)
            base_itemloader.add_value("thumbnail", thumbnail_url)
        base_itemloader.add_value("fulltext", trafilatura_fulltext)

        lom_base_itemloader: LomBaseItemloader = LomBaseItemloader()

        lom_general_itemloader: LomGeneralItemloader = LomGeneralItemloader()
        lom_general_itemloader.add_value("identifier", self.getId(response=response))
        pgl_title: str | None = response.xpath("//title/text()").get()
        if pgl_title:
            lom_general_itemloader.add_value("title", pgl_title)
        if meta_description:
            lom_general_itemloader.add_value("description", meta_description)
        if html_language:
            lom_general_itemloader.add_value("language", html_language)
        if keyword_set:
            keyword_list: list[str] = list(keyword_set)
            if keyword_list:
                keyword_list.sort()
                lom_general_itemloader.add_value("keyword", keyword_list)

        lom_classification_itemloader: LomClassificationItemLoader = LomClassificationItemLoader()
        lom_educational_itemloader: LomEducationalItemLoader = LomEducationalItemLoader()

        if pgl_author and isinstance(pgl_author, str):
            # PGL provides exactly one organization text string per item
            lifecycle_publisher: LomLifecycleItemloader = LomLifecycleItemloader()
            lifecycle_publisher.add_value("role", "author")
            lifecycle_publisher.add_value("organization", pgl_author)
            if pgl_erscheinungsjahr:
                # PGL provides only incomplete "YYYY"-dates, which the pipeline will transform to YYYY-01-01
                pgl_erscheinungsjahr = pgl_erscheinungsjahr.strip()
                lifecycle_publisher.add_value("date", pgl_erscheinungsjahr)
            lom_base_itemloader.add_value("lifecycle", lifecycle_publisher.load_item())

        lifecycle_metadata_provider: LomLifecycleItemloader = LomLifecycleItemloader()
        # see: https://www.globaleslernen.de/de/die-ewik/impressum
        lifecycle_metadata_provider.add_value("role", "metadata_provider")
        lifecycle_metadata_provider.add_value("organization", "World University Service (WUS) Deutsches Komitee e.V.")
        lifecycle_metadata_provider.add_value("url", response.url)
        if pgl_erscheinungsjahr:
            lifecycle_metadata_provider.add_value("date", pgl_erscheinungsjahr)
        lom_base_itemloader.add_value("lifecycle", lifecycle_metadata_provider.load_item())

        lom_technical_itemloader: LomTechnicalItemLoader = LomTechnicalItemLoader()
        # lom_technical_itemloader.add_value("format", "text/html")
        # ToDo: debug the crawler results first without setting "format" to text/html
        lom_technical_itemloader.add_value("location", response.url)

        license_itemloader: LicenseItemLoader = LicenseItemLoader()
        if pgl_author and isinstance(pgl_author, str):
            license_itemloader.add_value("author", pgl_author)
        license_itemloader.add_value("internal", Constants.LICENSE_COPYRIGHT_FREE)

        valuespace_itemloader: ValuespaceItemLoader = ValuespaceItemLoader()
        valuespace_itemloader.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)  # default for all crawled items
        if new_lrt_mapped:
            new_lrt_list: list[str] = list(new_lrt_mapped)
            valuespace_itemloader.add_value("new_lrt", new_lrt_list)
        if educontext_set:
            edu_context: list[str] = list(educontext_set)
            valuespace_itemloader.add_value("educationalContext", edu_context)
        # 2024-11-28: as suggested by Jan and the editors,
        # all PGL items should be considered as part of the "Nachhaltigkeit"-discipline
        disciplines.add("64018")  # Nachhaltigkeit
        if disciplines:
            discipline_list: list[str] = list(disciplines)
            valuespace_itemloader.add_value("discipline", discipline_list)

        permission_itemloader: PermissionItemLoader = self.getPermissions(response=response)
        response_itemloader: ResponseItemLoader = ResponseItemLoader()
        response_itemloader.add_value("headers", response.headers)
        response_itemloader.add_value("status", response.status)
        response_itemloader.add_value("text", trafilatura_fulltext)
        response_itemloader.add_value("url", response.url)

        lom_base_itemloader.add_value("general", lom_general_itemloader.load_item())
        lom_base_itemloader.add_value("classification", lom_classification_itemloader.load_item())
        lom_base_itemloader.add_value("educational", lom_educational_itemloader.load_item())
        lom_base_itemloader.add_value("technical", lom_technical_itemloader.load_item())

        base_itemloader.add_value("lom", lom_base_itemloader.load_item())
        base_itemloader.add_value("license", license_itemloader.load_item())
        base_itemloader.add_value("valuespaces", valuespace_itemloader.load_item())
        base_itemloader.add_value("permissions", permission_itemloader.load_item())
        base_itemloader.add_value("response", response_itemloader.load_item())

        yield base_itemloader.load_item()
