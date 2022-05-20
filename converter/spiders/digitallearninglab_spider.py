import html
import time

import scrapy
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.valuespace_helper import ValuespaceHelper
from .base_classes import LrmiBase


class DigitallearninglabSpider(CrawlSpider, LrmiBase):
    name = "digitallearninglab_spider"
    friendlyName = "digital.learning.lab"
    url = "https://digitallearninglab.de"
    version = "0.1.2"  # last update: 2022-05-20
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        # Digital Learning Lab recognizes and blocks crawlers that are too fast:
        # without the Autothrottle we'll be seeing HTTP Errors 503 (and therefore missing out on lots of items)
        # "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1,
        "AUTOTHROTTLE_START_DELAY": 0.25
    }
    apiUrl = "https://digitallearninglab.de/api/%type?q=&sorting=latest&page=%page"
    # Unterrichtsbausteine (API "count" value):     228
    # tools:                                        182
    # therefore we expect                           410 items after a successful crawl

    def __init__(self, **kwargs):
        LrmiBase.__init__(self, **kwargs)

    def mapResponse(self, response, **kwargs):
        return LrmiBase.mapResponse(self, response)

    def getId(self, response):
        return response.meta["item"].get("id")

    def getHash(self, response):
        modified = self.getLRMI("dateModified", response=response)
        if modified:
            return modified + self.version
        # fallback if LRMI was not parsable
        return time.time()

    def start_request(self, type, page):
        return scrapy.Request(
            url=self.apiUrl.replace("%page", str(page)).replace("%type", type),
            callback=self.parse_request,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            meta={"page": page, "type": type},
        )

    def start_requests(self):
        yield self.start_request("unterrichtsbausteine", 1)
        yield self.start_request("tools", 1)

    def parse_request(self, response: scrapy.http.TextResponse):
        data = response.json()
        results = data.get("results")
        if results:
            for item in results:
                copy_response = response.replace(url=self.url + item.get("url"))
                copy_response.meta["item"] = item
                if self.hasChanged(copy_response):
                    yield scrapy.Request(
                        url=copy_response.url,
                        callback=self.handle_entry,
                        meta={"item": item, "type": response.meta["type"]},
                    )
                yield self.start_request(
                    response.meta["type"], response.meta["page"] + 1
                )

    def handle_entry(self, response):
        return LrmiBase.parse(self, response)

    @staticmethod
    def get_type(response):
        if response.meta["type"] == "tools":
            return Constants.TYPE_TOOL
        else:
            return Constants.TYPE_MATERIAL

    # thumbnail is always the same, do not use the one from rss
    def getBase(self, response):
        base = LrmiBase.getBase(self, response)
        # base.replace_value('thumbnail', self.url + '/media/' + response.meta['item'].get('image'))
        base.replace_value(
            "thumbnail",
            response.xpath('//img[@class="content-info__image"]/@src').get(),
        )
        base.replace_value("type", self.get_type(response))
        return base

    def getLOMGeneral(self, response):
        general = LrmiBase.getLOMGeneral(self, response)
        general.replace_value(
            "title", html.unescape(response.meta["item"].get("name").strip())
        )
        general.add_value(
            "description", html.unescape(response.meta["item"].get("teaser"))
        )
        # general.add_value('keyword', list(filter(lambda x: x,map(lambda x: x.strip(), response.xpath('//*[@id="ContentModuleApp"]//*[@class="topic-name"]//text()').getall()))))
        return general

    def getLOMTechnical(self, response):
        technical = LrmiBase.getLOMTechnical(self, response)
        technical.replace_value("format", "text/html")
        technical.replace_value("location", response.url)
        return technical

    def getLicense(self, response):
        license = LrmiBase.getLicense(self, response)
        return license

    def getValuespaces(self, response):
        valuespaces = LrmiBase.getValuespaces(self, response)
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
                valuespaces.add_value(
                    "educationalContext",
                    ValuespaceHelper.educationalContextByGrade(range),
                )
        except:
            pass
        try:
            discipline = response.xpath(
                '//ul[@class="sidebar__information"]/li[@class="sidebar__information-item"]/*[contains(@class,"icon-subject")]/parent::*//text()'
            ).getall()
            valuespaces.add_value("discipline", discipline)
        except:
            pass
        lrt = response.meta["item"].get("type")
        valuespaces.add_value("learningResourceType", lrt)
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
            valuespaces.add_value("learningResourceType", tool_type)
        except:
            pass
        return valuespaces
