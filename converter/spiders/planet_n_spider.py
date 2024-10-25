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
    friendlyName = "Planet N"
    version = "0.0.2"
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 4,
        "WEB_TOOLS": WebEngine.Playwright,
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
        # ToDo: DocString
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
        # ToDo: DocString
        # e.g.: https://www.planet-n.de/wp-json/wp/v2/module/2093
        _module_api_endpoint: str = f"https://www.planet-n.de/wp-json/wp/v2/module/{module_id}"
        return _module_api_endpoint

    def parse_api_results(self, response: scrapy.http.TextResponse, **kwargs: Any):
        # ToDo: DocString
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
        # ToDo: DocString
        if response.status == 200:
            _response_dict: dict = response.json()
            item_url: str = _response_dict["link"]
            yield scrapy.Request(
                url=item_url,
                callback=self.parse,
                cb_kwargs={"wp_item": _response_dict},  # we'll read metadata from this dict in the parser() method
            )
        else:
            self.logger.warning(
                f"Unexpected API response for URL {response.url} . " f"Response status: {response.status}"
            )
            return None

    def getId(self, response=None, wp_item: dict = None) -> str:
        # ToDo: DocString
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
        # ToDo: DocString
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
        # ToDo: DocString
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
        # ToDo: DocString
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
        if og_image:
            base_itemloader.add_value("thumbnail", og_image)
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

        license_itemloader: LicenseItemLoader = LicenseItemLoader()
        license_itemloader.add_value("author", meta_author)

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
