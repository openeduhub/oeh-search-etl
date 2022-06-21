import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from .base_classes import LomBase, JSONBase


class TutorySpider(CrawlSpider, LomBase, JSONBase):
    name = "tutory_spider"
    friendlyName = "tutory"
    url = "https://www.tutory.de/"
    objectUrl = "https://www.tutory.de/bereitstellung/dokument/"
    baseUrl = "https://www.tutory.de/api/v1/share/"
    version = "0.1.2"  # last update: 2022-05-23
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_DEBUG": True
    }

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self):
        url = self.baseUrl + "worksheet?groupSlug=entdecken&pageSize=999999"
        yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response: scrapy.http.TextResponse):
        data = response.json()
        for j in data["worksheets"]:
            response_copy = response.replace(url=self.objectUrl + j["id"])
            response_copy.meta["item"] = j
            if self.hasChanged(response_copy):
                yield self.parse(response_copy)

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

        # valuespaces.add_value("learningResourceType", "worksheet")  # remove this value when reaching crawler v0.1.3
        valuespaces.add_value("new_lrt", "36e68792-6159-481d-a97b-2c00901f4f78")  # Arbeitsblatt
        return valuespaces

    def getLicense(self, response=None):
        license_loader = LomBase.getLicense(self, response)
        license_loader.add_value("internal", Constants.LICENSE_COPYRIGHT_LAW)
        return license_loader

    def getLOMGeneral(self, response=None):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("title", response.meta["item"]["name"])
        if 'description' in response.meta["item"]:
            general.add_value("description", response.meta["item"]["description"])
        else:
            html = self.getUrlData(response.url)["html"]
            if html:
                data = (
                    Selector(text=html).xpath('//ul[contains(@class,"worksheet-pages")]//text()').getall()
                )
                cutoff = 4
                if len(data) > cutoff:
                    for i in range(cutoff):
                        del data[0]

                text = " ".join(data)
                text = text[:1000]
                general.add_value("description", text)
        return general

    def getLOMTechnical(self, response=None):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("location", response.url)
        technical.add_value("format", "text/html")
        technical.add_value("size", len(response.body))
        return technical
