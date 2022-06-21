from scrapy import Request

from .base_classes import LomBase, RSSBase


class IRightsSpider(RSSBase):
    name = "irights_spider"
    friendlyName = "iRights.info"
    start_urls = ["https://irights.info/feed"]
    version = "0.1.1"   # last update: 2022-02-21

    def __init__(self, **kwargs):
        RSSBase.__init__(self, **kwargs)

    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse)

    def getLOMGeneral(self, response):
        general = RSSBase.getLOMGeneral(self, response)
        general.add_value(
            "keyword", response.meta["item"].xpath("category//text()").getall()
        )
        return general

    def getLOMLifecycle(self, response):
        lifecycle = RSSBase.getLOMLifecycle(self, response)
        name = response.meta["item"].xpath("creator//text()").get().split(" ")
        lifecycle.add_value("role", "author")
        lifecycle.add_value("firstName", name[0])
        del name[0]
        lifecycle.add_value("lastName", " ".join(name))
        return lifecycle

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.add_value("educationalContext", "sekundarstufe_2")
        valuespaces.add_value("educationalContext", "berufliche_bildung")
        valuespaces.add_value("educationalContext", "erwachsenenbildung")
        valuespaces.add_value("discipline", "700")  # Wirtschaftskunde
        valuespaces.add_value("discipline", "48005")  # Gesellschaftskunde
        return valuespaces
