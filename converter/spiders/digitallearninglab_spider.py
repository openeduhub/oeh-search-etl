from converter.items import *
import time
from .base_classes import LrmiBase
import json
import html
from converter.valuespace_helper import ValuespaceHelper
from converter.constants import Constants
import scrapy

# Spider to fetch RSS from planet schule
class DigitallearninglabSpider(scrapy.Spider, LrmiBase):
    name = "digitallearninglab_spider"
    friendlyName = "digital.learning.lab"
    url = "https://digitallearninglab.de"
    version = "0.1.1"
    apiUrl = "https://digitallearninglab.de/api/%type?q=&sorting=latest&page=%page"

    def __init__(self, **kwargs):
        LrmiBase.__init__(self, **kwargs)

    def mapResponse(self, response):
        return LrmiBase.mapResponse(self, response)

    def getId(self, response):
        return response.meta["item"].get("id")

    def getHash(self, response):
        modified = self.getLRMI("dateModified", response=response)
        if modified:
            return modified + self.version
        # fallback if lrmi was unparsable
        return time.time()

    def startRequest(self, type, page):
        return scrapy.Request(
            url=self.apiUrl.replace("%page", str(page)).replace("%type", type),
            callback=self.parseRequest,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            meta={"page": page, "type": type},
        )

    def start_requests(self):
        yield self.startRequest("unterrichtsbausteine", 1)
        yield self.startRequest("tools", 1)

    def parseRequest(self, response):
        data = json.loads(response.body_as_unicode())
        results = data.get("results")
        if results:
            for item in results:
                copyResponse = response.replace(url=self.url + item.get("url"))
                copyResponse.meta["item"] = item
                if self.hasChanged(copyResponse):
                    yield scrapy.Request(
                        url=copyResponse.url,
                        callback=self.handleEntry,
                        meta={"item": item, "type": response.meta["type"]},
                    )
                yield self.startRequest(
                    response.meta["type"], response.meta["page"] + 1
                )

    def handleEntry(self, response):
        return LrmiBase.parse(self, response)

    def getType(self, response):
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
        base.replace_value("type", self.getType(response))
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
            toolType = list(
                map(
                    lambda x: x.strip(),
                    response.xpath(
                        '//ul[@class="sidebar__information"]/li[@class="sidebar__information-item"]/*[contains(@class,"icon-settings")]/parent::*//text()'
                    ).getall(),
                )
            )
            # @TODO: proper mapping, maybe specialised tool field?
            valuespaces.add_value("learningResourceType", toolType)
        except:
            pass
        return valuespaces
