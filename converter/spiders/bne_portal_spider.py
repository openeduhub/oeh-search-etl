import datetime
import re
from typing import Iterable

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


class BnePortalSpider(scrapy.Spider, LomBase):
    """
    Crawler for "Lernmaterialien" from BNE-Portal.de. ("Infothek" -> "Lernmaterialien":
    https://www.bne-portal.de/SiteGlobals/Forms/bne/lernmaterialien/suche_formular.html?nn=140004)
    """

    name = "bne_portal_spider"
    friendlyName = "BNE-Portal"
    version = "0.0.3"  # last update: 2024-08-08
    playwright_cookies: list[dict] = [
        {
            "name": "gsbbanner",
            "value": "closed"
        }
    ]
    current_session_cookie: dict = dict()
    # By using two cookie attributes ("gsbbanner" and "AL_SESS-S"), we enable playwright to skip the rendering of
    # cookie banners while taking website screenshots (e.g., when no thumbnail was provided by BNE).
    # While we can hard-code the "gsbbanner"-cookie,
    # we need to dynamically parse the current session cookie ("AL_SESS-S") from the first HTTP response.
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 2,
        "AUTOTHROTTLE_MAX_DELAY": 120,
        "WEB_TOOLS": WebEngine.Playwright,
        "ROBOTSTXT_OBEY": False,
        # "COOKIES_DEBUG": True,
        "PLAYWRIGHT_COOKIES": playwright_cookies,
        "PLAYWRIGHT_ADBLOCKER": True,
        "USER_AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }
    # NOTICE: Custom Settings
    # We need to disobey the robots.txt in this case because the crawler would not be able to parse the learning
    # materials in a timely manner (and requests to the required search form would be disallowed).
    # We also NEED to spoof the User Agent, because Scrapy Requests without a User Agent always return a "403"-Response.

    # Spider-specific Mappings:
    # to see a list of possible strings that need to be mapped, check the drop-down menus at:
    # https://www.bne-portal.de/SiteGlobals/Forms/bne/lernmaterialien/suche_formular.html?nn=140004
    FORMAT_TO_NEW_LRT: dict = {
        "Artikel": "b98c0c8c-5696-4537-82fa-dded7236081e",  # Artikel und Einzelpublikation
        "Broschüre/ Buch/ Zeitschrift": "0cef3ce9-e106-47ae-836a-48f9ed04384e",  # Dokumente und textbasierte Inhalte
        "Datenbank/ Materialsammlung": "04693b11-8b39-42aa-964f-578be063a851",  # Kollektion, Sammlung oder Kanal
        "Datenbank-Webseite": "d8c3ef03-b3ab-4a5e-bcc9-5a546fefa2e9",  # Webseite
        "Digitale Lehr-/ Lerneinheit": ["588efe4f-976f-48eb-84aa-8bcb45679f85", "0d23ff13-9d92-4944-92fa-2b5fe1dde80b"],
        # Lehr- und Lernmaterial; Stundenentwurf
        "Film": "7a6e9608-2554-4981-95dc-47ab9ba924de",  # Video (Material)
        "Poster": "c382a478-74e0-42f1-96dd-fcfb5c27f746",  # Poster und Plakat
        "Spiel": "b0495f44-b05d-4bde-9dc5-34d7b5234d76",  # Lernspiel
        "Spiel/ Aktion": "68a43516-889e-4ce9-8e03-248307bd99ff",  # offene und kreative Aktivität
    }

    BILDUNGSBEREICH_TO_EDUCATIONAL_CONTEXT: dict = {
        # "bildungsbereichübergreifend": "",  # will be added to keywords due to impossible mapping
        "Frühkindliche Bildung": "elementarbereich",
        # "non-formale/ informelle Bildung": "",  # will be added to keywords due to impossible mapping
        "Primarbereich": "grundschule",
        "Sekundarbereich I": "sekundarstufe_1",
        "Sekundarbereich II": "sekundarstufe_2",
    }

    THEMEN_TO_DISCIPLINE: dict = {
        "Ernährung": "04006",  # Ernährung und Hauswirtschaft
        "Gesellschaftslehre": "48005",  # Gesellschaftskunde
        "Interkulturelles Lernen": "340",  # Interkulturelle Bildung
    }

    def start_requests(self) -> Iterable[Request]:
        start_url_lernmaterialien: str = (
            "https://www.bne-portal.de/SiteGlobals/Forms/bne/lernmaterialien/suche_formular.html"
        )
        start_url_publikationen: str = (
            "https://www.bne-portal.de/SiteGlobals/Forms/bne/publikationen/suche_formular.html?nn=139986"
        )
        start_urls: list[str] = [start_url_lernmaterialien, start_url_publikationen]
        for start_url in start_urls:
            yield scrapy.Request(
                url=start_url,
                callback=self.gather_urls_from_first_page_of_search_results,
            )

    def gather_urls_from_first_page_of_search_results(self, response: scrapy.http.HtmlResponse, **kwargs):
        # https://www.bne-portal.de/SiteGlobals/Forms/bne/lernmaterialien/suche_formular.html
        # at the bottom of the search results should be a page navigation element ("Seite 1 ... X")
        # we're looking for the last page number to build the list of available URLs
        last_page_link: str | None = response.xpath("//nav[@class='c-nav-index']/ul/li[last()]/a/@href").get()
        last_page_number: int | None = None
        page_number_pattern = re.compile(r"""D(?P<page_number>\d+)#searchResults""")
        if last_page_link:
            # the relative URl of the last page currently looks like this:
            # "SiteGlobals/Forms/bne/lernmaterialien/suche_formular.html?gtp=33528_list%253D59#searchResults"
            # the page number is controlled via the "D<page_number>#searchResults" part of the URL
            page_number_result = page_number_pattern.search(string=last_page_link)
            if page_number_result and "page_number" in page_number_result.groupdict():
                last_page_str: str = page_number_result.groupdict()["page_number"]
                last_page_number: int = int(last_page_str)
        else:
            self.logger.warning(
                f"Failed to retrieve last page URL from response {response.url} . "
                f"Cannot proceed with page iteration. (Please debug the XPath Expression!)"
            )
        if last_page_number:
            overview_relative_url_without_page_param = re.sub(
                pattern=page_number_pattern, repl="", string=last_page_link
            )
            for overview_page_nr in range(2, last_page_number + 1):
                # since we are already on page 1, we iterate from page 2 to the last page
                overview_relative_url: str = (
                    f"{overview_relative_url_without_page_param}" f"D{overview_page_nr}#searchResults"
                )
                overview_absolute_url: str = response.urljoin(overview_relative_url)
                yield scrapy.Request(
                    url=overview_absolute_url, callback=self.yield_request_for_each_search_result, priority=1
                )
        if response.headers and not self.current_session_cookie:
            # we want to grab the first session cookie exactly ONCE and forward it to playwright,
            # because it allows us to skip the rendering of the cookie-banner when falling back to website-screenshots
            self.save_session_cookie_to_spider_custom_settings(response)
        # the first page should contain 15 search results that need to be yielded to the parse()-method
        yield from self.yield_request_for_each_search_result(response)

    def save_session_cookie_to_spider_custom_settings(self, response: scrapy.http.HtmlResponse):
        """
        Parses the HTML header for a specific cookie attribute ("AL_SESS-S") and saves the key-value pair to the
        spider's custom_settings.
        This allows us to skip the rendering of the (obtrusive) cookie banner when a thumbnail was not available,
        and our pipeline needs to fall back to taking a screenshot with playwright.
        """
        cookies_raw: list[bytes] | None = response.headers.getlist("Set-Cookie")
        if cookies_raw:
            for cookie_bytes_object in cookies_raw:
                if cookie_bytes_object and isinstance(cookie_bytes_object, bytes):
                    # cookie example:
                    # b'AL_SESS-S=AVHw!yeRm5uXQNxe3FM!nbN33IjG7EMgCO2CipHfxK1Iv34ESuTGarlWWhYFBecs0e3b;
                    # Path=/; Secure; HttpOnly; SameSite=Lax'
                    cookie = cookie_bytes_object.decode("utf-8")
                    # we need to decode the cookie into a string object first
                    if "AL_SESS-S" in cookie:
                        # we want to pass the session cookie to playwright, in order to not rely on hard-coding a
                        # session cookie (which might become invalid at any future moment).
                        cookie_attributes: list[str] | None = cookie.split(";")
                        # first, we need to split the cookie bytes object into the individual cookie attributes
                        if cookie_attributes:
                            for cookie_attribute in cookie_attributes:
                                if "AL_SESS-S=" in cookie_attribute:
                                    # We're only interested in the session cookie. The other attributes don't seem
                                    # to be necessary to skip the cookie-banner
                                    cookie_split = cookie_attribute.split("=")
                                    cookie_name: str = cookie_split[0]
                                    cookie_value: str = cookie_split[1]
                                    session_cookie = {"name": cookie_name, "value": cookie_value}
                                    self.current_session_cookie.update(session_cookie)
            if self.current_session_cookie:
                self.logger.info(
                    f"Saving current session cookie to 'PLAYWRIGHT_COOKIES'-custom-settings. "
                    f"Session cookie: {self.current_session_cookie}"
                )
                # we expect the current sesison cookie to look like this:
                # {
                #     "name": "AL_SESS-S",
                #     "value": "AUiJVd4i8sXlsq6ZEHfjlvfvCBhnub4_TNyxnydq1cpcuRk8EvO5ryyD9643seQ742AB",
                # },
                self.playwright_cookies.append(self.current_session_cookie)
                self.custom_settings.update({"PLAYWRIGHT_COOKIES": self.playwright_cookies})

    def yield_request_for_each_search_result(self, response: scrapy.http.HtmlResponse):
        search_result_relative_urls: list[str] = response.xpath(
            "//div[@class='c-pub-teaser__text-wrapper']/h2/a[@class='c-pub-teaser__title-link']/@href"
        ).getall()
        if search_result_relative_urls and isinstance(search_result_relative_urls, list):
            self.logger.debug(f"Detected {len(search_result_relative_urls)} search results on {response.url}")
            for url_item in search_result_relative_urls:
                search_result_absolute_url: str = response.urljoin(url_item)
                yield scrapy.Request(url=search_result_absolute_url, callback=self.parse)

    @staticmethod
    def clean_up_and_split_list_of_strings(raw_list_of_strings: list[str]):
        """
        Cleans up a (raw) list of strings by
        1) removing whitespace chars from the beginning / end of strings
        2) removing empty strings (that only consist of newlines / whitespaces)
        3) splitting multiple string values (which are separated by comma on BNE-Portal) into individual strings
        and returns the result as a list[str] if successful.

        @param raw_list_of_strings: a list of strings that might contain unnecessary whitespace chars or empty strings
        @return: cleaned up list[str] if successful, otherwise None.
        """
        temporary_list_of_strings: list[str] = list()
        clean_list_of_strings: list[str] = list()
        if raw_list_of_strings and isinstance(raw_list_of_strings, list):
            for raw_string in raw_list_of_strings:
                if isinstance(raw_string, str):
                    cleaned_string: str | None = raw_string.strip()
                    if cleaned_string:
                        temporary_list_of_strings.append(cleaned_string)
        if temporary_list_of_strings:
            for temp_str in temporary_list_of_strings:
                if ", " in temp_str:
                    individual_strings: list[str] = temp_str.split(", ")
                    if individual_strings:
                        clean_list_of_strings.extend(individual_strings)
                else:
                    clean_list_of_strings.append(temp_str)
        if clean_list_of_strings:
            return clean_list_of_strings
        else:
            return None

    def getId(self, response=None) -> str:
        # BNE-Portal.de does not provide an identifier for their items, therefore we resort to the URL
        return response.url

    def getHash(self, response=None) -> str:
        # BNE-Portal.de does not provide a publication or modification date,
        # therefore we need to resort to the timestamp of the crawl
        now = datetime.datetime.now().isoformat()
        hash_str: str = f"{now}v{self.version}"
        return hash_str

    def parse(self, response=None, **kwargs):
        trafilatura_text: str | None = trafilatura.extract(response.body)

        if self.shouldImport(response) is False:
            self.logger.debug(f"Skipping entry {self.getId(response)} because shouldImport() returned False")
            return None
        if self.getId(response) is not None and self.getHash(response) is not None:
            if not self.hasChanged(response):
                return None

        # Metadata (Header)
        title: str | None = response.xpath("//meta[@name='title']/@content").get()
        og_title: str = response.xpath("//meta[@property='og:title']/@content").get()
        description: str | None = response.xpath("//meta[@name='description']/@content").get()
        og_description: str | None = response.xpath("//meta[@property='og:description']/@content").get()

        keywords_from_header: str | None = response.xpath("//meta[@name='keywords']/@content").get()
        keyword_set: set[str] = set()
        if keywords_from_header and isinstance(keywords_from_header, str) and ", " in keywords_from_header:
            # keyword values are typically split by comma in the DOM header
            keyword_list: list[str] = keywords_from_header.split(", ")
            if keyword_list:
                keyword_set.update(keyword_list)
        elif keywords_from_header and isinstance(keywords_from_header, str):
            # this case should only happen if there is only a single keyword available in the header
            keyword_set.add(keywords_from_header)

        # og_type: str | None = response.xpath("//meta[@property='og:type']/@content").get()
        og_image: str | None = response.xpath("//meta[@property='og:image']/@content").get()
        # attention: a big amount of (older) learning materials do not have a thumbnail!
        # og_image_type: str | None = response.xpath("//meta[@property='og:image:type']/@content").get()
        og_locale: str | None = response.xpath("//meta[@property='og:locale']/@content").get()
        og_url: str | None = response.xpath("//meta[@property='og:url']/@content").get()

        # metadata (DOM)
        #  - optional: "Mehr Informationen" should contain the URL to source website
        bne_format_raw: list[str] | None = response.xpath("//strong[contains(text(),'Format')]/../text()").getall()
        # this XPath Expression looks for the bold text "Format", which shares the same <p>-element as the desired
        # strings. Therefore, we select its parent with ".." and grab all text strings for further metadata extraction.
        bne_thema_raw: list[str] | None = response.xpath("//strong[contains(text(),'Thema')]/../text()").getall()
        bne_bildungsbereich_raw: list[str] | None = response.xpath(
            "//strong[contains(text(),'Bildungsbereich')]/../text()"
        ).getall()
        bne_kosten_raw: list[str] | None = response.xpath("//strong[contains(text(),'Kosten')]/../text()").getall()

        bne_format_clean: list[str] | None = self.clean_up_and_split_list_of_strings(bne_format_raw)
        bne_thema_clean: list[str] | None = self.clean_up_and_split_list_of_strings(bne_thema_raw)
        bne_bildungsbereich_clean: list[str] | None = self.clean_up_and_split_list_of_strings(bne_bildungsbereich_raw)
        bne_kosten_clean: list[str] | None = self.clean_up_and_split_list_of_strings(bne_kosten_raw)

        bne_guetesiegel: list | None = response.xpath("//div[@class='c-pub-teaser__stamp']").getall()
        # the "BNE Gütesiegel" is displayed at the bottom right of curated materials.
        # (as of 2024-08-02 there are 6 of those materials in total)
        # If this <div>-container shows up, we'll add the "erfüllt BNE-Gütekriterien" keyword to our list.
        if bne_guetesiegel:
            keyword_set.add("erfüllt BNE-Gütekriterien")

        new_lrt_set: set[str] = set()
        if bne_format_clean and isinstance(bne_format_clean, list):
            for format_str in bne_format_clean:
                if format_str in self.FORMAT_TO_NEW_LRT:
                    # manually mapping BNE "Format"-strings (e.g. 'Film', 'Poster') to our new_lrt Vocab for those cases
                    # where the raw strings would not match with our vocab
                    new_lrt_mapped: list[str] | str = self.FORMAT_TO_NEW_LRT.get(format_str)
                    if isinstance(new_lrt_mapped, str):
                        new_lrt_set.add(new_lrt_mapped)
                    if isinstance(new_lrt_mapped, list):
                        for mapped_value in new_lrt_mapped:
                            new_lrt_set.add(mapped_value)
                elif format_str:
                    # this case typically happens for perfect matches (e.g. "Arbeitsblatt") or uncovered edge-cases
                    new_lrt_set.add(format_str)

        if "/Publikationen/" in response.url:
            new_lrt_set.add("b98c0c8c-5696-4537-82fa-dded7236081e")  # Artikel und Einzelpublikation

        disciplines: set[str] = set()
        if bne_thema_clean and isinstance(bne_thema_clean, list):
            for thema_str in bne_thema_clean:
                if thema_str in self.THEMEN_TO_DISCIPLINE:
                    thema_mapped: str = self.THEMEN_TO_DISCIPLINE.get(thema_str)
                    disciplines.add(thema_mapped)
                elif thema_str:
                    # at this point we cannot know if the "Thema"-string is a discipline or not, therefore we treat it
                    # as additional keywords because the majority of values that we receive from "Thema" are keywords.
                    disciplines.add(thema_str)
                    keyword_set.add(thema_str)

        educational_context_set: set[str] = set()
        if bne_bildungsbereich_clean and isinstance(bne_bildungsbereich_clean, list):
            # Mapping BNE "Bildungsbereich" values to educationalContext
            for bb_str in bne_bildungsbereich_clean:
                if bb_str in self.BILDUNGSBEREICH_TO_EDUCATIONAL_CONTEXT:
                    bb_mapped: str = self.BILDUNGSBEREICH_TO_EDUCATIONAL_CONTEXT.get(bb_str)
                    educational_context_set.add(bb_mapped)
                elif bb_str:
                    educational_context_set.add(bb_str)
                    if "bildungsbereichübergreifend" in bb_str or "non-formale/ informelle Bildung" in bb_str:
                        # these two edge-cases can't be mapped to educationalContext. To not lose out on these values,
                        # we save them to the keywords instead.
                        keyword_set.add(bb_str)

        price: str | None = None
        if bne_kosten_clean and isinstance(bne_kosten_clean, list):
            # there should be exactly 1 string value in this list by now
            if len(bne_kosten_clean) == 1:
                for cost_str in bne_kosten_clean:
                    if cost_str and isinstance(cost_str, str):
                        cost_str: str = cost_str.lower()
                        if "kostenfrei" in cost_str:
                            price = "no"
                            pass
                        elif "kostenpflichtig" in cost_str:
                            price = "yes"
                        elif "€" in cost_str:
                            # there is currently (as of 2024-08-01) one single item that has an actual price string.
                            # example:
                            # https://www.bne-portal.de/bne/shareddocs/lernmaterialien/de/praxisbuch-mobilitaetsbildung.html#searchFacets
                            price = "yes"
                        elif "null" in cost_str:
                            # observed 5 edge-cases where free materials carried the "Kosten"-string: "null"
                            # this might be a typo in their CMS, but handling these edge-cases as free seems reasonable.
                            # example:
                            # https://www.bne-portal.de/bne/shareddocs/lernmaterialien/de/nachhaltige-stadtentwicklung.html#searchFacets
                            price = "no"
                        else:
                            self.logger.warning(
                                f"Failed to map BNE 'Kosten'-value to 'price'-vocab. Please update the mapping "
                                f"for this edge-case: '{cost_str}'"
                            )
            else:
                # if BNE-Portal starts using more than two values in the future, we need to update our mapping
                self.logger.warning(
                    f"Mapping edge-case for BNE 'Kosten' detected: Expected exactly 1 value in "
                    f"{bne_kosten_clean}, but received {len(bne_kosten_clean)}. "
                    f"Values received: {bne_kosten_clean}"
                )

        base_itemloader: BaseItemLoader = BaseItemLoader()
        base_itemloader.add_value("sourceId", self.getId(response))
        base_itemloader.add_value("hash", self.getHash(response))
        if og_image:
            base_itemloader.add_value("thumbnail", og_image)
        if trafilatura_text:
            base_itemloader.add_value("fulltext", trafilatura_text)

        lom_base_itemloader: LomBaseItemloader = LomBaseItemloader()

        lom_classification_itemloader: LomClassificationItemLoader = LomClassificationItemLoader()

        lom_general_itemloader: LomGeneralItemloader = LomGeneralItemloader()
        lom_general_itemloader.add_value("identifier", response.url)
        if title:
            lom_general_itemloader.add_value("title", title)
        elif og_title:
            lom_general_itemloader.add_value("title", og_title)
        if description:
            lom_general_itemloader.add_value("description", description)
        elif og_description:
            lom_general_itemloader.add_value("description", og_description)
        if og_locale:
            lom_general_itemloader.add_value("language", og_locale)
        if keyword_set:
            keyword_list = list(keyword_set)
            lom_general_itemloader.add_value("keyword", keyword_list)

        lom_educational_itemloader: LomEducationalItemLoader = LomEducationalItemLoader()

        lom_technical_itemloader: LomTechnicalItemLoader = LomTechnicalItemLoader()
        if og_url and og_url != response.url:
            lom_technical_itemloader.add_value("location", og_url)
            lom_technical_itemloader.add_value("location", response.url)
        else:
            lom_technical_itemloader.add_value("location", response.url)

        lom_lifecycle_itemloader: LomLifecycleItemloader = LomLifecycleItemloader()
        lom_lifecycle_itemloader.add_value("role", "publisher")
        lom_lifecycle_itemloader.add_value("organization", "Bundesministerium für Bildung und Forschung")
        lom_lifecycle_itemloader.add_value(
            "url", "https://www.bne-portal.de/bne/de/services/impressum/impressum_node.html"
        )
        lom_base_itemloader.add_value("lifecycle", lom_lifecycle_itemloader.load_item())

        license_itemloader: LicenseItemLoader = LicenseItemLoader()
        license_itemloader.add_value("author", "Bundesministerium für Bildung und Forschung")
        license_itemloader.add_value("internal", Constants.LICENSE_COPYRIGHT_FREE)
        license_description: str = (
            "Das Copyright für Texte liegt, soweit nicht anders vermerkt, "
            "beim Bundesministerium für Bildung und Forschung (nachfolgend BMBF). Das "
            "Copyright für Bilder liegt, soweit nicht anders vermerkt, beim Bundesministerium "
            "für Bildung und Forschung oder bei der Bundesbildstelle des Presse- und "
            "Informationsamtes der Bundesregierung. Auf den BMBF-Webseiten zur Verfügung "
            "gestellte Texte, Textteile, Grafiken, Tabellen oder Bildmaterialien dürfen ohne "
            "vorherige Zustimmung des BMBF nicht vervielfältigt, nicht verbreitet und nicht "
            "ausgestellt werden."
        )
        # see: https://www.bne-portal.de/bne/de/services/impressum/impressum_node.html
        license_itemloader.add_value("description", license_description)

        permission_itemloader: PermissionItemLoader = self.getPermissions(response=response)

        valuespace_itemloader: ValuespaceItemLoader = ValuespaceItemLoader()
        valuespace_itemloader.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)
        disciplines.add("64018")  # Nachhaltigkeit is hard-coded for all BNE materials
        if disciplines:
            discipline_list: list[str] = list(disciplines)
            valuespace_itemloader.add_value("discipline", discipline_list)
        if educational_context_set:
            edu_context_list: list[str] = list(educational_context_set)
            valuespace_itemloader.add_value("educationalContext", edu_context_list)
        if new_lrt_set:
            new_lrt_list: list[str] = list(new_lrt_set)
            valuespace_itemloader.add_value("new_lrt", new_lrt_list)
        if price:
            valuespace_itemloader.add_value("price", price)

        response_itemloader: ResponseItemLoader = ResponseItemLoader()
        response_itemloader.add_value("headers", response.headers)
        response_itemloader.add_value("status", response.status)
        response_itemloader.add_value("text", trafilatura_text)
        response_itemloader.add_value("url", response.url)

        lom_base_itemloader.add_value("classification", lom_classification_itemloader.load_item())
        lom_base_itemloader.add_value("educational", lom_educational_itemloader.load_item())
        lom_base_itemloader.add_value("general", lom_general_itemloader.load_item())
        lom_base_itemloader.add_value("technical", lom_technical_itemloader.load_item())

        base_itemloader.add_value("lom", lom_base_itemloader.load_item())
        base_itemloader.add_value("license", license_itemloader.load_item())
        base_itemloader.add_value("valuespaces", valuespace_itemloader.load_item())
        base_itemloader.add_value("permissions", permission_itemloader.load_item())
        base_itemloader.add_value("response", response_itemloader.load_item())
        yield base_itemloader.load_item()
