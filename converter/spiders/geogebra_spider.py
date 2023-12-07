from scrapy.spiders import CrawlSpider
from converter.items import *
from converter.constants import Constants
from .base_classes import LomBase, JSONBase
from scrapy import Request
import json
import logging


# spider for GeoGebra
class GeoGebraSpider(CrawlSpider, LomBase, JSONBase):
    name = "geogebra_spider"
    friendlyName = "GeoGebra"
    url = "https://www.geogebra.org"
    version = "0.1.1"
    start_urls = [
        "https://www.geogebra.org/m-sitemap-1.xml",
        "https://www.geogebra.org/m-sitemap-2.xml",
        "https://www.geogebra.org/m-sitemap-3.xml",
        "https://www.geogebra.org/m-sitemap-4.xml",
        "https://www.geogebra.org/m-sitemap-5.xml",
        "https://www.geogebra.org/m-sitemap-6.xml",
        "https://www.geogebra.org/m-sitemap-7.xml",
        "https://www.geogebra.org/m-sitemap-8.xml",
        "https://www.geogebra.org/m-sitemap-9.xml",
        "https://www.geogebra.org/m-sitemap-10.xml",
        "https://www.geogebra.org/m-sitemap-11.xml",
    ]

    apiUrl = "https://api.geogebra.org/v1.0/materials/%id?scope=extended&embed=creator,tags,topics"

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)
        CrawlSpider.__init__(self, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url = url, callback = self.parse)

    def get(self, *params, response):
        data = json.loads(response.body_as_unicode())
        return JSONBase.get(self, *params, json=data)

    def parse(self, response):
        i = 0
        for url in response.xpath('//*[name()="url"]/*[name()="loc"]//text()').getall():
            split = url.split("/")
            id = split[len(split) - 1]
            apiCall = self.apiUrl.replace("%id", id)
            yield Request(
                url=apiCall, callback=self.parseEntry, meta={"url": url}
            )
            i += 1

    async def parseEntry(self, response):
        if self.get("language", response=response) == "de":
            return await LomBase.parse(self, response)
        logging.info(
            "Skpping entry with language " + self.get("language", response=response)
        )
        return None

    def getId(self, response):
        return self.get("id", response=response)

    def getHash(self, response):
        return self.version + str(self.get("date_modified", response=response))

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        # print(response.url)
        # print(self.get('thumbUrl', response = response))
        # print(self.get('thumbUrl', response = response).replace('$1', '@l'))
        base.add_value(
            "thumbnail",
            str(self.get("thumbUrl", response=response)).replace("$1", "@l"),
        )
        base.add_value("lastModified", self.get("date_modified", response=response))
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("identifier", self.get("id", response=response))
        general.add_value("title", self.get("title", response=response))
        general.add_value("keyword", self.get("keywords", response=response))
        general.add_value("language", self.get("language", response=response))
        general.add_value("description", self.get("description", response=response))
        return general

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.add_value("discipline", self.get("topics", response=response))
        t = self.get("type", response=response)
        if t == "ws":
            valuespaces.add_value("learningResourceType", "worksheet")
        if t == "book":
            valuespaces.add_value("learningResourceType", "text")
        c = self.get("categories", response=response)
        if "game" in c:
            valuespaces.add_value("learningResourceType", "educational_game")
        if "practice" in c:
            valuespaces.add_value("learningResourceType", "drill_and_practice")
        return valuespaces

    def getLOMEducational(self, response):
        educational = LomBase.getLOMEducational(self, response)
        # educational.add_value('typicalLearningTime', self.get('timeRequired'))
        return educational

    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        license.add_value("url", Constants.LICENSE_CC_BY_NC_SA_30)
        return license

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", self.get("fileFormat", response=response))
        technical.add_value("size", self.get("ContentSize", response=response))
        technical.add_value("location", response.meta["url"])
        return technical
