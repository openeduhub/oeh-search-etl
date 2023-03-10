import logging
import re
import urllib.parse

import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider

from .base_classes import LomBase, JSONBase
from ..web_tools import WebEngine, WebTools


class TutorySpider(CrawlSpider, LomBase, JSONBase):
    name = "tutory_spider"
    friendlyName = "tutory"
    url = "https://www.tutory.de/"
    objectUrl = "https://www.tutory.de/bereitstellung/dokument/"
    baseUrl = "https://www.tutory.de/api/v1/share/"
    version = "0.1.4"  # last update: 2022-03-11
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_DEBUG": True,
        "WEB_TOOLS": WebEngine.Playwright,
    }

    api_pagesize_limit = 5000

    # the old API pageSize of 999999 (which was used in 2021) doesn't work anymore and throws a 502 Error (Bad Gateway).
    # Setting the pageSize to 5000 appears to be a reasonable value with an API response time of 12-15s

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self):
        first_url: str = self.assemble_tutory_api_url(api_page=0)
        yield scrapy.Request(url=first_url, callback=self.parse_api_page)

    def parse_api_page(self, response: scrapy.http.TextResponse):
        """
        This method tries to parse the current pagination parameter from response.url and yields two types of
        scrapy.Requests:
        1) if the "worksheets"-list isn't empty, try to crawl the next API page
        2) if there are "worksheets" in the current JSON Response, try to crawl the individual items
        """
        json_data: dict = response.json()
        page_regex = re.compile(r"&page=(?P<page>\d+)")
        pagination_parameter = page_regex.search(response.url)
        pagination_current_page: int = 0
        if pagination_parameter:
            pagination_current_page: int = pagination_parameter.groupdict().get("page")
        if "total" in json_data:
            total_items = json_data.get("total")
            logging.info(
                f"Currently crawling Tutory API page {pagination_current_page} -> {response.url} // "
                f"Expected items (in total): {total_items}"
            )
        pagination_next_page: int = int(pagination_current_page) + 1
        url_next_page = self.assemble_tutory_api_url(pagination_next_page)
        if "worksheets" in json_data:
            worksheets_data: list = json_data.get("worksheets")
            if worksheets_data:
                # only crawl the next page if the "worksheets"-dict isn't empty
                yield scrapy.Request(url=url_next_page, callback=self.parse_api_page)
                logging.info(
                    f"Tutory API page {pagination_current_page} is expected to yield " f"{len(worksheets_data)} items."
                )
                for j in worksheets_data:
                    response_copy = response.replace(url=self.objectUrl + j["id"])
                    response_copy.meta["item"] = j
                    if self.hasChanged(response_copy):
                        yield self.parse(response_copy)

    def assemble_tutory_api_url(self, api_page: int):
        url_current_page = (
            f"{self.baseUrl}worksheet?groupSlug=entdecken&pageSize={str(self.api_pagesize_limit)}"
            f"&page={str(api_page)}"
        )
        return url_current_page

    def getId(self, response=None):
        return str(response.meta["item"]["id"])

    def getHash(self, response=None):
        return response.meta["item"]["updatedAt"] + self.version

    def parse(self, response, **kwargs):
        return LomBase.parse(self, response)

    def getBase(self, response=None):
        base = LomBase.getBase(self, response)
        base.add_value("lastModified", response.meta["item"]["updatedAt"])
        base.add_value(
            "thumbnail",
            self.objectUrl + response.meta["item"]["id"] + ".jpg?width=1000",
        )
        return base

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        discipline = list(
            map(
                lambda x: x["code"],
                filter(
                    lambda x: x["type"] == "subject",
                    response.meta["item"]["metaValues"],
                ),
            )
        )
        valuespaces.add_value("discipline", discipline)
        valuespaces.add_value("new_lrt", "36e68792-6159-481d-a97b-2c00901f4f78")  # Arbeitsblatt
        return valuespaces

    def getLicense(self, response=None):
        license_loader = LomBase.getLicense(self, response)
        if "user" in response.meta["item"]:
            user_dict: dict = response.meta["item"]["user"]
            if "publishName" in user_dict:
                # the 'publishName'-field seems to indicate whether the username or the full name appears on top of a
                # worksheet as author metadata.
                publish_decision: str = user_dict["publishName"]
                if publish_decision == "username":
                    if "username" in user_dict:
                        username: str = user_dict["username"]
                        if username:
                            license_loader.add_value("author", username)
                elif publish_decision == "name":
                    # ToDo: this information could also be used for lifecycle role 'author' in a future crawler update
                    firstname = None
                    lastname = None
                    if "firstname" in user_dict:
                        firstname = user_dict.get("firstname")
                    if "lastname" in user_dict:
                        lastname = user_dict.get("lastname")
                    if firstname and lastname:
                        full_name = f"{firstname} {lastname}"
                        license_loader.add_value("author", full_name)
        return license_loader

    def getLOMGeneral(self, response=None):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("title", response.meta["item"]["name"])
        item_description = None
        if "description" in response.meta["item"]:
            item_description = response.meta["item"]["description"]
        meta_description = response.xpath("//meta[@property='description']/@content").get()
        meta_og_description = response.xpath("//meta[@property='og:description']/@content").get()
        if item_description:
            general.add_value("description", item_description)
        elif meta_description:
            # 1st fallback: trying to parse a description string from the header
            general.add_value("description", meta_description)
        elif meta_og_description:
            # 2nd fallback: <meta property="og:description">
            general.add_value("description", meta_og_description)
        else:
            html = WebTools.getUrlData(response.url, engine=WebEngine.Playwright)["html"]
            if html:
                # apparently, the human-readable text is nested within
                # <div class="eduMark"> OR <div class="noEduMark"> elements
                edumark_combined: list[str] = (
                    Selector(text=html)
                    .xpath("//div[contains(@class,'eduMark')]//text()|//div[contains(@class,'noEduMark')]//text()")
                    .getall()
                )
                if edumark_combined:
                    text_combined: str = " ".join(edumark_combined)
                    text_combined = urllib.parse.unquote(text_combined)
                    text_combined = f"{text_combined[:1000]} [...]"
                    general.add_value("description", text_combined)
        return general

    def getLOMTechnical(self, response=None):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("location", response.url)
        technical.add_value("format", "text/html")
        technical.add_value("size", len(response.body))
        return technical
