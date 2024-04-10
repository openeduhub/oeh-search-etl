import html
import logging
import time

import scrapy
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.valuespace_helper import ValuespaceHelper
from .base_classes import LrmiBase, LomBase
from ..items import (
    LicenseItemLoader,
    LomLifecycleItemloader,
    ResponseItemLoader,
    BaseItemLoader,
    LomGeneralItemloader,
    LomTechnicalItemLoader,
    ValuespaceItemLoader,
    LomBaseItemloader,
)
from ..util.license_mapper import LicenseMapper
from ..web_tools import WebEngine


class DigitallearninglabSpider(CrawlSpider, LrmiBase):
    name = "digitallearninglab_spider"
    friendlyName = "digital.learning.lab"
    url = "https://digitallearninglab.de"
    version = "0.1.4"  # last update: 2024-02-09
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        # Digital Learning Lab recognizes and blocks crawlers that are too fast:
        # without the Autothrottle we'll be seeing HTTP Errors 503 (and therefore missing out on lots of items)
        # "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 2,
        "AUTOTHROTTLE_START_DELAY": 0.25,
        "WEB_TOOLS": WebEngine.Playwright,
    }
    apiUrl = "https://digitallearninglab.de/api/%type?q=&sorting=latest&page=%page"
    # API Counts (as of 2023-03-08)
    # type 'unterrichtsbausteine':              234
    # type 'tool':                              184
    # therefore we expect (in total):           418 items after a successful crawl
    # under the assumption that there are no duplicates across types

    def __init__(self, **kwargs):
        LrmiBase.__init__(self, **kwargs)

    async def mapResponse(self, response, **kwargs):
        return await LrmiBase.mapResponse(self, response)

    def getId(self, response):
        return response.meta["item"].get("id")

    def getHash(self, response):
        modified = self.getLRMI("dateModified", response=response)
        if modified:
            return f"{modified}v{self.version}"
        # fallback if LRMI was not parsable
        return time.time()

    def start_request(self, type: str, page: int) -> scrapy.Request:
        return scrapy.Request(
            url=self.apiUrl.replace("%page", str(page)).replace("%type", type),
            callback=self.parse_request,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            meta={"page": page, "type": type},
        )

    def build_initial_api_requests(self, response: scrapy.http.Response):
        # the previous approach of simply having two yield requests after each other caused Scrapy to stop
        # after the first request, basically skipping half the items.
        # see: https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy.Spider.start_requests
        api_material_type_starting_points: list[str] = ["unterrichtsbausteine", "tools"]
        for material_type in api_material_type_starting_points:
            yield self.start_request(type=material_type, page=1)

    def start_requests(self):
        # Dummy request: check if Digital Learning Lab is online/available, then start building the actual API requests
        yield scrapy.Request(url=self.url, callback=self.build_initial_api_requests)

    def parse_request(self, response: scrapy.http.TextResponse):
        data: dict = response.json()
        results = data.get("results")
        if results:
            for item in results:
                copy_response = response.replace(url=self.url + item.get("url"))
                copy_response.meta["item"] = item
                yield scrapy.Request(
                    url=copy_response.url,
                    callback=self.parse,
                    meta={"item": item, "type": response.meta["type"]},
                )
            yield self.start_request(type=response.meta["type"], page=response.meta["page"] + 1)

    @staticmethod
    def get_new_lrt(response):
        if response.meta["type"] == "tool":
            return Constants.NEW_LRT_TOOL
        else:
            return Constants.NEW_LRT_MATERIAL

    # thumbnail is always the same, do not use the one from rss
    def getBase(self, response):
        base: BaseItemLoader = LrmiBase.getBase(self, response)
        # base.replace_value('thumbnail', self.url + '/media/' + response.meta['item'].get('image'))
        base.replace_value(
            "thumbnail",
            response.xpath('//img[@class="content-info__image"]/@src').get(),
        )
        return base

    def getLOMGeneral(self, response):
        general: LomGeneralItemloader = LrmiBase.getLOMGeneral(self, response)
        general.replace_value("title", html.unescape(response.meta["item"].get("name").strip()))
        json_ld_description = self.getLRMI("description", response=response)
        if json_ld_description:
            general.add_value("description", json_ld_description)
        else:
            # fallback via DLL API: shorter "teaser"-description
            general.add_value("description", html.unescape(response.meta["item"].get("teaser")))
        # general.add_value('keyword', list(filter(lambda x: x,map(lambda x: x.strip(), response.xpath('//*[@id="ContentModuleApp"]//*[@class="topic-name"]//text()').getall()))))
        return general

    def getLOMTechnical(self, response):
        technical: LomTechnicalItemLoader = LrmiBase.getLOMTechnical(self, response)
        technical.replace_value("format", "text/html")
        technical.replace_value("location", response.url)
        return technical

    def get_lifecycle_author(self, response):
        lifecycle_loader: LomLifecycleItemloader = LomLifecycleItemloader()
        json_ld_authors: list[dict] = self.getLRMI("author", response=response)
        if json_ld_authors:
            for author_item in json_ld_authors:
                if "@type" in author_item:
                    author_type = author_item["@type"]
                    if author_type == "Person":
                        if "name" in author_item:
                            lifecycle_loader.add_value("role", "author")
                            lifecycle_loader.add_value("firstName", author_item["name"])
                        if "sameAs" in author_item:
                            lifecycle_loader.add_value("url", author_item["sameAs"])
                    elif author_type == "Organization":
                        if "name" in author_item:
                            lifecycle_loader.add_value("role", "publisher")
                            lifecycle_loader.add_value("organization", author_item["name"])
                        if "sameAs" in author_item:
                            lifecycle_loader.add_value("url", author_item["sameAs"])
        return lifecycle_loader

    def get_lifecycle_metadata_provider(self, response, provider_item: dict = None):
        if provider_item:
            lifecycle_loader: LomLifecycleItemloader = LomLifecycleItemloader()
            provider_name: str = provider_item.get("name")
            provider_url: str = provider_item.get("sameAs")
            date_published: str = self.getLRMI("datePublished", response=response)
            if provider_name:
                lifecycle_loader.add_value("role", "metadata_provider")
                lifecycle_loader.add_value("organization", provider_name)
            if provider_url:
                lifecycle_loader.add_value("url", provider_url)
            if date_published:
                lifecycle_loader.add_value("date", date_published)
            return lifecycle_loader

    def getLicense(self, response):
        license_loader: LicenseItemLoader = LomBase.getLicense(self, response)
        license_raw: str = self.getLRMI("license", response=response)
        json_ld_authors: list[dict] = self.getLRMI("author", response=response)
        authors = set()  # by adding all authors to a set, we're making sure to only save unique author names
        if json_ld_authors:
            # if available, the second (there are two!) json_ld container contains a single author, while the DLL API
            # itself provides a "co_author"-field (which will be used later on in lifecycle 'role' -> 'unknown')
            for author_item in json_ld_authors:
                if "name" in author_item:
                    author_name: str = author_item["name"]
                    authors.add(author_name)
        if authors:
            license_loader.add_value("author", authors)
        if license_raw:
            license_mapper = LicenseMapper()
            license_url = license_mapper.get_license_url(license_string=license_raw)
            license_internal = license_mapper.get_license_internal_key(license_string=license_raw)
            if license_url:
                license_loader.replace_value("url", license_url)
            elif license_internal:
                license_loader.add_value("internal", license_internal)
        else:
            # Footer: "Inhalte der Seite stehen unter CC BY-SA 4.0 Lizenz, wenn nicht anders angegeben."
            logging.debug(
                f"DigitalLearningLabs did not provide a valid license for {response.url} . Setting fallback "
                f"value CC-BY-SA 4.0."
            )
            license_loader.add_value("url", Constants.LICENSE_CC_BY_SA_40)  # default for every item
        return license_loader

    def getValuespaces(self, response):
        vs_loader: ValuespaceItemLoader = LrmiBase.getValuespaces(self, response)
        vs_loader.replace_value("new_lrt", self.get_new_lrt(response))
        # ToDo: scrape DOM (left bar) for additional metadata:
        #  - 'conditionsOfAccess'
        #  - dataProtectionConformity?
        try:
            range = (
                response.xpath(
                    '//ul[@class="sidebar__information"]/li[@class="sidebar__information-item"]/*[contains(@class,"icon-level")]/parent::*//text()'
                )
                .get()
                .replace("Stufe", "")
                .strip()
                .split(" - ")
            )
            if len(range):
                vs_loader.add_value(
                    "educationalContext",
                    ValuespaceHelper.educationalContextByGrade(range),
                )
        except:
            pass
        try:
            discipline = response.xpath(
                '//ul[@class="sidebar__information"]/li[@class="sidebar__information-item"]/*[contains(@class,"icon-subject")]/parent::*//text()'
            ).getall()
            vs_loader.add_value("discipline", discipline)
            # ToDo: implement a proper 'discipline'-mapping with the 'digitalCompetencies'-update of the crawler
        except:
            pass
        item_type = response.meta["item"].get("type")
        # the DLL API currently provides only 3 values for "type": 'teaching-module', 'tool', 'trend'
        vs_loader.add_value("new_lrt", item_type)
        if item_type == "teaching-module":
            vs_loader.replace_value("new_lrt", "5098cf0b-1c12-4a1b-a6d3-b3f29621e11d")  # Unterrichtsbaustein
        try:
            tool_type = list(
                map(
                    lambda x: x.strip(),
                    response.xpath(
                        '//ul[@class="sidebar__information"]/li[@class="sidebar__information-item"]/*[contains(@class,"icon-settings")]/parent::*//text()'
                    ).getall(),
                )
            )
            # @TODO: proper mapping, maybe specialised tool field?
            vs_loader.add_value("new_lrt", tool_type)
        except:
            pass
        # ToDo: fix above PEP8:E722 warnings (too broad 'except' clauses) asap
        return vs_loader

    async def parse(self, response: scrapy.http.HtmlResponse, **kwargs):
        if self.shouldImport(response) is False:
            logging.debug("Skipping entry {} because shouldImport() returned false".format(str(self.getId(response))))
            return None
        if self.getId(response) is not None and self.getHash(response) is not None:
            if not self.hasChanged(response):
                return None
        base: BaseItemLoader = self.getBase(response)
        # ToDo: educational -> competencies ("ccm:competencies")?
        lom: LomBaseItemloader = self.getLOM(response)

        if self.getLRMI("author", response=response):
            lom.add_value("lifecycle", self.get_lifecycle_author(response).load_item())
        provider_list: list[dict] = self.getLRMI("provider", response=response)
        # there might be multiple providers within the "provider"-field of the json_ld
        if provider_list:
            for provider_item in provider_list:
                lom.add_value(
                    "lifecycle", self.get_lifecycle_metadata_provider(response, provider_item=provider_item).load_item()
                )
        if "co_authors" in response.meta["item"]:
            co_authors: list[str] = response.meta["item"]["co_authors"]
            if co_authors:
                for co_author in co_authors:
                    lifecycle_unknown_item_loader = LomLifecycleItemloader()
                    if co_author:
                        lifecycle_unknown_item_loader.add_value("role", "unknown")
                        lifecycle_unknown_item_loader.add_value("firstName", co_author)
                    lom.add_value("lifecycle", lifecycle_unknown_item_loader.load_item())
        base.add_value("lom", lom.load_item())
        base.add_value("license", self.getLicense(response).load_item())
        base.add_value("permissions", self.getPermissions(response).load_item())

        response_itemloader: ResponseItemLoader = await self.mapResponse(response)
        base.add_value("response", response_itemloader.load_item())
        base.add_value("valuespaces", self.getValuespaces(response).load_item())

        return base.load_item()
