import html
import re
from typing import Any, Iterable

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.http import Response

from converter.constants import Constants
from converter.es_connector import EduSharing
from converter.items import (
    BaseItemLoader,
    LomBaseItemloader,
    LomGeneralItemloader,
    LomTechnicalItemLoader,
    LomLifecycleItemloader,
    LomEducationalItemLoader,
    ValuespaceItemLoader,
    LicenseItemLoader,
    PermissionItemLoader,
    ResponseItemLoader,
)
from converter.spiders.base_classes import LomBase
from converter.web_tools import WebEngine


class PlanetNSpider(scrapy.Spider, LomBase):
    name = "planet_n_spider"
    friendlyName = "Planet-N"
    version = "0.0.4"
    playwright_cookies: list[dict] = [
        {
            "name": "SimpleCookieControl",
            "value": "deny"
        }
    ]
    # see: https://wordpress.com/plugins/simple-cookie-control
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 4,
        "WEB_TOOLS": WebEngine.Playwright,
        "PLAYWRIGHT_COOKIES": playwright_cookies,
        "PLAYWRIGHT_ADBLOCKER": True,
    }

    MODULE_SUBJECT_TO_DISCIPLINE_MAPPING = {
        "bildende-kunst": "060",  # Kunst
        "biologie": "080",  # Biologie
        "chemie": "100",  # Chemie
        "deutsch": "120",  # Deutsch
        "englisch": "20001",  # Englisch
        "erdkunde-geographie-weltkunde": "220",  # Geografie
        "ethik-religion-werte": ["160", "520"],  # Ethik / Religion
        "franzoesisch": "20002",  # Französisch
        "gemeinschaft-gesellschaft-politik-sozialkunde": [
            "48005",
            "480",
            "44007",
        ],  # Gesellschaftskunde / Politik / Sozialpädagogik (Sozialkunde)
        "geschichte": "240",  # Geschichte
        "latein": "20005",  # Latein
        "mathematik": "380",  # Mathematik
        "philosophie": "450",  # Philosophie
        "physik": "460",  # Physik
        "russisch": "20006",  # Russisch
        "spanisch": "20007",  # Spanisch
        "sport": "600",  # Sport
        # "verbraucherkunde": "",  # ToDo: mapping not possible -> no equivalent discipline available
        "wirtschaft": "700",  # Wirtschaftskunde
    }

    TAG_TO_NEW_LRT = {
        "aktion": "68a43516-889e-4ce9-8e03-248307bd99ff",  # offene und kreative Aktivität (Lehr- und Lernmaterial)
        "allgemein": "1846d876-d8fd-476a-b540-b8ffd713fedb",  # Material
        "audio": "ec2682af-08a9-4ab1-a324-9dca5151e99f",  # Audio
        "bild": "a6d1ac52-c557-4151-bc6f-0d99b0b96fb9",  # Bild
        "diagramm": "f7228fb5-105d-4313-afea-66dd59b1b6f8",  # Graph, Diagramm und Charts
        "schaubild": "1dc4ed81-718c-4b76-86cb-947a86875973",  # Veranschaulichung, Schaubild und Tafelbild
        "slideshow": "92c7a50c-6243-45d9-8b11-e79cbbda6305",  # Präsentation
        "spiel": "a120ce77-59f5-4564-8d49-73f4a0de1594",  # Lernen, Quiz und Spiel
        "statistik": "345cba59-9fa0-4ec8-ba93-2c75f4a40003",  # Daten
        "tabelle": "933ceef8-c7ae-4af3-9229-4bd86334dfea",  # Tabellen
        "text": "0cef3ce9-e106-47ae-836a-48f9ed04384e",  # Dokumente und textbasierte Inhalte
        "video": "7a6e9608-2554-4981-95dc-47ab9ba924de",  # Video (Material)
    }

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self) -> Iterable[Request]:
        _api_first_page: str = self.build_wp_json_module_list_request_url()
        yield scrapy.Request(
            url=_api_first_page,
            callback=self.parse_api_results,
        )

    @staticmethod
    def build_wp_json_module_list_request_url(page: int = 1, results_per_page: int = 100) -> str:
        """
        Build the URLs for iterating through all result pages of Planet-N's WordPress JSON API.

        :param page: page parameter (valid from: 1 to X)
        :param results_per_page: the number of items that should be returned per query
        :return: the "complete" URL for a single API request
        """
        # the WP-JSON API endpoint pagination begins at 1, e.g.:
        # https://www.planet-n.de/wp-json/wp/v2/module?per_page=50&page=1
        _planet_n_wp_json_api: str = "https://www.planet-n.de/wp-json/wp/v2/module?"
        _results_per_page: int = results_per_page  # the API only supports values between 1 and 100
        _results_per_page_parameter: str = f"per_page={_results_per_page}"
        _page_parameter: str = f"page={page}"
        api_endpoint: str = f"{_planet_n_wp_json_api}{_results_per_page_parameter}&{_page_parameter}"
        return api_endpoint

    @staticmethod
    def build_wp_json_individual_module_request_url(module_id: str | int) -> str:
        """
        Build the URL to request individual "module" items from Planet-N's WordPress JSON API.

        :param module_id: the "module" id (a WordPress item ``id``)
        :return: the "complete" URL to request a single item from the API
        """
        # e.g.: https://www.planet-n.de/wp-json/wp/v2/module/2093
        _module_api_endpoint: str = f"https://www.planet-n.de/wp-json/wp/v2/module/{module_id}"
        return _module_api_endpoint

    def parse_api_results(self, response: scrapy.http.TextResponse, **kwargs: Any):
        """
        Try to parse the API response for individual "modules" and:
        1) yield those "module" items as an individual ``scrapy.Request``
        2) paginate to the next API results (if available)

        :param response: WordPress JSON API response containing several "module" items
        :param kwargs:
        :return: yield ``scrapy.Request`` for each contained item of the API response that should be parsed
        and yield another ``scrapy.Request`` to query the next API page (hopefully containing results)
        """
        if response.status == 200:
            response_json: list[dict] = response.json()
            # if the response is valid, the JSON should contain up to 50 elements that we need to (individually) parse
            for _item in response_json:
                _module_id: int = _item["id"]
                request_url_for_individual_item: str = self.build_wp_json_individual_module_request_url(_module_id)
                yield scrapy.Request(url=request_url_for_individual_item, callback=self.parse_api_item)
            # --- request the next API page:
            page_pattern: re.Pattern = re.compile(r"&page=(?P<page>\d+)")
            page_match: re.Match = page_pattern.search(response.url)
            if page_match:
                _current_page: str = page_match.group("page")
                _current_page_number: int = int(_current_page)
                _next_page = _current_page_number + 1
                _next_page_api_url: str = self.build_wp_json_module_list_request_url(page=_next_page)
                yield scrapy.Request(
                    url=_next_page_api_url,
                    callback=self.parse_api_results,
                )
        else:
            self.logger.warning(f"Unexpected API response for URL {response.url} received. Status: {response.status}")
        pass

    def parse_api_item(self, response: scrapy.http.TextResponse, **kwargs: Any):
        """
        Try to parse the API response for an individual "module"-request from Planet-N's WordPress JSON API
        and yield the URL to scrapy's ``parse()``-method.

        :param response: the WP-JSON API response of an individual item
        :param kwargs:
        :return: yield a ``scrapy.Request`` if the API response could be parsed to a ``dict``,
        otherwise return ``None``.
        """
        if response.status == 200:
            _response_dict: dict = response.json()
            item_url: str = _response_dict["link"]
            yield scrapy.Request(
                url=item_url,
                callback=self.parse,
                cb_kwargs={"wp_item": _response_dict},  # we'll read metadata from this dict in the parse() method
            )
        else:
            self.logger.warning(
                f"Unexpected API response for URL {response.url} . " f"Response status: {response.status}"
            )
            return None

    def getId(self, response=None, wp_item: dict = None) -> str:
        """
        Read the ``id`` (Type: ``int``) property from the WordPress item and return it as a string.

        :param response: not used in this method (but typically an HTML ``scrapy.http.Response`` object)
        :param wp_item: the WordPress item from Planet-N
        :return: the WordPress item ``id`` (Type: ``str``)
        """
        if wp_item:
            # WordPress identifiers are Integer values, e.g.:
            # the API request https://www.planet-n.de/wp-json/wp/v2/module/1596 ("id"-value: 1596)
            # leads to the URL
            # https://www.planet-n.de/module/gaia-geographie-und-geschichte/
            _item_id: int = wp_item["id"]
            return str(_item_id)
        else:
            self.logger.error(f"Could not read 'id' from API response for item {response.url} !")

    def getHash(self, response=None, wp_item: dict = None) -> str:
        """
        Read the ``hash`` property from the WordPress item and build a hash string.

        :param response: not used in this method (but typically an HTML ``scrapy.http.Response`` object)
        :param wp_item: the WordPress item from Planet-N
        :return: a hash string in this pattern: ``"<hash_value>v<crawler_version>"``
        """
        if wp_item:
            _hash: str = wp_item["hash"]
            return f"{_hash}v{self.version}"
        else:
            self.logger.error(f"Could not read 'hash' from API response for item {response.url} !")

    def hasChanged(self, response=None, **kwargs) -> bool:
        try:
            wp_item: dict = kwargs["wp_item"]
            identifier: str = self.getId(response, wp_item)
            hash_str: str = self.getHash(response, wp_item)
            uuid_str: str = self.getUUID(response=response)
        except KeyError:
            self.logger.error(f"Failed to read necessary metadata in hasChanged() method for item {response.url} !")
            return False
        if self.forceUpdate:
            return True
        if self.uuid:
            if uuid_str == self.uuid:
                self.logger.info(f"matching requested id: {self.uuid}")
                return True
            return False
        if self.remoteId:
            if identifier == self.remoteId:
                self.logger.info(f"matching requested id: {self.remoteId}")
                return True
            return False
        db = EduSharing().find_item(identifier, self)
        changed = db is None or db[1] != hash_str
        if not changed:
            self.logger.info(f"Item {identifier} (uuid: {db[0]}) has not changed")
        return changed

    def check_if_item_should_be_dropped(self, response: scrapy.http.Response, wp_item: dict):
        """
        Determine if the provided WordPress item from Planet-N should be dropped by checking for three conditions:
        1) are there any robot meta tags in the DOM header that indicate a wish against webcrawling of this URL?
        2) is the crawler attribute "shouldImport" set to False?
        (-> item should be skipped)
        3) has the item's hash value changed?
        (-> if the hash value has not changed -> item should be skipped)

        :param response: the scrapy.http.Response object (HTML)
        :param wp_item: the corresponding WordPress item
        :return: ``True`` if the item should be dropped, ``False`` otherwise
        """
        _drop_item_flag: bool = False  # we assume that items should be crawled
        robot_meta_tags: list[str] = response.xpath("//meta[@name='robots']/@content").get()
        # checking if items should be crawled or not: if we detect "noindex" or "none" in the robot meta tags,
        # we'll skip the item altogether.
        if robot_meta_tags:
            # see: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
            if "noindex" in robot_meta_tags or "none" in robot_meta_tags:
                self.logger.info(
                    f"Robot Meta Tag {robot_meta_tags} identified! (Robot Meta Tags 'noindex' or 'none' should "
                    f"be skipped by the crawler.) Dropping item {response.url} ."
                )
                _drop_item_flag = True
        if self.shouldImport(response) is False:
            self.logger.debug(
                f"Skipping entry {self.getId(response=response, wp_item=wp_item)} because shouldImport() returned false"
            )
            _drop_item_flag = True
        if not self.hasChanged(response=response, wp_item=wp_item):
            _drop_item_flag = True
        return _drop_item_flag

    def clean_up_string(self, text: str) -> str | None:
        """
        Strips the provided string from HTML entities and unnecessary whitespaces or newlines.

        :param text: the "raw" input string
        :return: the "cleaned up" string (or None if the wrong input type was detected)
        """
        _text_clean: str | None = None
        if text and isinstance(text, str):
            # strings from Planet-N will contain HTML entities
            _soup = BeautifulSoup(text, "html.parser")
            _text_soup: str = _soup.get_text()
            if _text_soup:
                # Planet-N's strings contain trailing whitespaces or newlines, which we have to strip first:
                _text_clean = _text_soup.strip()
                return _text_clean
        else:
            self.logger.warning(f"Received unhandled input: provided 'text'-parameter was of type '{type(text)}'")
            return None

    def parse(self, response: Response, **kwargs: Any):
        try:
            # the JSON response from Planet-N's WordPress API:
            wp_item: dict = kwargs.get("wp_item")
        except KeyError:
            self.logger.warning(
                f"The WordPress API item (dict) for {response.url} could not be read. "
                f"Metadata might be missing! Dropping item..."
            )
            return None
        # check if item should be skipped / dropped during this crawl:
        drop_item_flag: bool = self.check_if_item_should_be_dropped(response=response, wp_item=wp_item)
        if drop_item_flag:
            return None

        # Reading metadata from the WP JSON API item:
        wp_item_id: str = self.getId(response=response, wp_item=wp_item)
        wp_item_hash: str = self.getHash(response=response, wp_item=wp_item)
        wp_class: list[str] | None = None
        if "class_list" in wp_item:
            # the "class_list" property contains several prefixed values:
            # "tag-<value>" contains a non-descriptive mix of keywords, disciplines and WordPress-internal status information
            # "module_subject-<value>" can contain disciplines (Schulfächer)
            # "module_topic-<value>" contains keywords
            wp_class = wp_item["class_list"]
        wp_date: str | None = None
        if "date" in wp_item:
            wp_date: str = wp_item["date"]
        wp_date_modified: str | None = None
        if "modified" in wp_item:
            wp_date_modified: str = wp_item["modified"]
        wp_description_long: str | None = None
        if "description" in wp_item:
            # description text will contain HTML entities
            wp_description_long: str = wp_item["description"]
            wp_description_long_clean: str | None = self.clean_up_string(text=wp_description_long)
            if wp_description_long_clean:
                wp_description_long = wp_description_long_clean
        wp_description_excerpt: str | None = None
        if "excerpt" in wp_item and "rendered" in wp_item["excerpt"]:
            wp_description_excerpt: str = wp_item["excerpt"]["rendered"]
            wp_description_excerpt_clean: str | None = self.clean_up_string(text=wp_description_excerpt)
            if wp_description_excerpt_clean:
                wp_description_excerpt = wp_description_excerpt_clean
        wp_keywords: list[str] | None = None
        if "keywords" in wp_item:
            wp_keywords: list[str] = wp_item["keywords"]
        wp_title: str | None = None
        if "title" in wp_item:
            wp_title: str = wp_item["title"]
            if wp_title and isinstance(wp_title, str):
                # titles will contain HTML entities (long dashes, "&" etc.)
                wp_title = html.unescape(wp_title)
        wp_location_url: str | None = None
        if "location" in wp_item:
            wp_location_url: str = wp_item["location"]
        wp_fulltext: str | None = None
        if "content" in wp_item and "rendered" in wp_item["content"]:
            wp_fulltext: str = wp_item["content"]["rendered"]

        # scraping DOM Metadata for additional properties:
        og_image: str = response.xpath("//meta[@property='og:image']/@content").get()
        og_locale: str = response.xpath("//meta[@property='og:locale']/@content").get()
        meta_author: str = response.xpath("//meta[@name='author']/@content").get()

        base_itemloader: BaseItemLoader = BaseItemLoader()

        base_itemloader.add_value("sourceId", wp_item_id)
        base_itemloader.add_value("hash", wp_item_hash)
        if wp_date_modified:
            base_itemloader.add_value("lastModified", wp_date_modified)
        # if og_image:
        #     base_itemloader.add_value("thumbnail", og_image)
        if wp_fulltext:
            base_itemloader.add_value("fulltext", wp_fulltext)

        lom_base_itemloader: LomBaseItemloader = LomBaseItemloader()

        lom_general_itemloader: LomGeneralItemloader = LomGeneralItemloader()
        lom_general_itemloader.add_value("identifier", wp_item_id)  # saving the module id to the 1st position
        lom_general_itemloader.add_value("identifier", wp_location_url)  # saving the location URL as the 2nd identifier
        if wp_title:
            lom_general_itemloader.add_value("title", wp_title)
        if wp_keywords:
            lom_general_itemloader.add_value("keyword", wp_keywords)
        if wp_description_long:
            lom_general_itemloader.add_value("description", wp_description_long)
        elif wp_description_excerpt:
            lom_general_itemloader.add_value("description", wp_description_excerpt)
        if og_image:
            # we assume that the OpenGraph locale attribute is correct and tells us the language of the learning object
            lom_general_itemloader.add_value("language", og_locale)

        lom_technical_itemloader: LomTechnicalItemLoader = LomTechnicalItemLoader()
        lom_technical_itemloader.add_value("location", wp_location_url)
        if wp_location_url != response.url:
            # in case the resolved URL differs from the API-provided URL of the item, we save both
            lom_technical_itemloader.add_value("location", response.url)

        if meta_author:
            # since the API provides no author metadata, we check the HTML Header for the DOM meta property "author"
            # and fill a (minimal) LifecycleItem with it
            lifecycle_publisher_itemloader: LomLifecycleItemloader = LomLifecycleItemloader()
            lifecycle_publisher_itemloader.add_value("role", "author")
            lifecycle_publisher_itemloader.add_value("organization", meta_author)
            if wp_date:
                lifecycle_publisher_itemloader.add_value("date", wp_date)
            lom_base_itemloader.add_value("lifecycle", lifecycle_publisher_itemloader.load_item())

        lom_educational_itemloader: LomEducationalItemLoader = LomEducationalItemLoader()
        if og_locale:
            lom_educational_itemloader.add_value("language", og_locale)

        valuespace_itemloader: ValuespaceItemLoader = ValuespaceItemLoader()
        valuespace_itemloader.add_value("discipline", "64018")  # Nachhaltigkeit
        valuespace_itemloader.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)
        # this crawler uses a crawler source template (Quellen-Datensatz) to inherit values from:
        # - intendedEndUserRole
        # - educationalContext
        _tags: list[str] = []
        _modules: list[str] = []
        if wp_class and isinstance(wp_class, list):
            for _class_entry in wp_class:
                # individual entries of the "class-list"-property can look like this:
                # "module_subject-gemeinschaft-gesellschaft-politik-sozialkunde",
                # "tag-bild"
                if "tag-" in _class_entry:
                    # we'll try to map these values to our "new_lrt"-vocab, but need to clean up the strings first
                    _tag_cleaned = _class_entry.replace("tag-", "")
                    _tags.append(_tag_cleaned)
                if "module_subject-" in _class_entry:
                    # we'll try to map these values to our "discipline"-vocab, but need to clean up the strings first
                    _module_cleaned = _class_entry.replace("module_subject-", "")
                    _modules.append(_module_cleaned)
        new_lrts_mapped: set[str] = set()
        if _tags and isinstance(_tags, list):
            for _tag in _tags:
                if _tag in self.TAG_TO_NEW_LRT:
                    _new_lrt_mapped: str | list[str] = self.TAG_TO_NEW_LRT[_tag]
                    if _new_lrt_mapped and isinstance(_new_lrt_mapped, str):
                        new_lrts_mapped.add(_new_lrt_mapped)
                    if _new_lrt_mapped and isinstance(_new_lrt_mapped, list):
                        new_lrts_mapped.update(_new_lrt_mapped)
        if new_lrts_mapped:
            new_lrt_list: list[str] = list(new_lrts_mapped)
            valuespace_itemloader.add_value("new_lrt", new_lrt_list)
        else:
            # as discussed with Jan on 2024-12-11:
            # each item can be considered to be a teaching module ("Unterrichtsbaustein")
            valuespace_itemloader.add_value("new_lrt", "5098cf0b-1c12-4a1b-a6d3-b3f29621e11d")

        disciplines_mapped: set[str] = set()
        if _modules and isinstance(_modules, list):
            for _module in _modules:
                if _module in self.MODULE_SUBJECT_TO_DISCIPLINE_MAPPING:
                    _discipline_mapped: str | list[str] = self.MODULE_SUBJECT_TO_DISCIPLINE_MAPPING[_module]
                    if _discipline_mapped and isinstance(_discipline_mapped, str):
                        disciplines_mapped.add(_discipline_mapped)
                    if _discipline_mapped and isinstance(_discipline_mapped, list):
                        disciplines_mapped.update(_discipline_mapped)
        if disciplines_mapped:
            discipline_list: list[str] = list(disciplines_mapped)
            valuespace_itemloader.add_value("discipline", discipline_list)

        license_itemloader: LicenseItemLoader = LicenseItemLoader()
        license_itemloader.add_value("author", meta_author)
        license_itemloader.add_value("internal", Constants.LICENSE_CUSTOM)
        custom_license_description: str = (
            "Vorbehaltlich der verlinkten externen Inhalte, "
            "sind die Inhalte dieser Website lizenziert unter einer CC BY-NC-SA 4.0 Lizenz. "
            "Als Namensnennung genügt die Angabe „Planet-N“."
        )
        # as discussed with Jan on 2024-12-11 we're hard-coding the license description according to
        # https://www.planet-n.de/info/ -> Headline: "Nutzung der Website"
        license_itemloader.add_value("description", custom_license_description)

        permission_itemloader: PermissionItemLoader = super().getPermissions(response=response)

        response_itemloader: ResponseItemLoader = ResponseItemLoader()
        response_itemloader.add_value("headers", response.headers)
        response_itemloader.add_value("url", response.url)
        response_itemloader.add_value("status", response.status)
        response_itemloader.add_value("text", wp_fulltext)

        lom_base_itemloader.add_value("general", lom_general_itemloader.load_item())
        lom_base_itemloader.add_value("technical", lom_technical_itemloader.load_item())
        lom_base_itemloader.add_value("educational", lom_educational_itemloader.load_item())

        base_itemloader.add_value("lom", lom_base_itemloader.load_item())
        base_itemloader.add_value("license", license_itemloader.load_item())
        base_itemloader.add_value("valuespaces", valuespace_itemloader.load_item())
        base_itemloader.add_value("permissions", permission_itemloader.load_item())
        base_itemloader.add_value("response", response_itemloader.load_item())

        yield base_itemloader.load_item()
