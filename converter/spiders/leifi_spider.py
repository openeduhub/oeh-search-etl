from converter.items import *
from .base_classes import LomBase
from converter.valuespace_helper import Valuespaces
import requests
import html
from converter.constants import Constants
import scrapy

# LEIFIphysik spider for xml data file
class LeifiSpider(scrapy.Spider, LomBase):
    name = "leifi_spider"
    friendlyName = "LEIFIphysik"
    url = "https://www.leifiphysik.de/"
    rssUrl = "http://localhost/sources/leifi_feed_rss.xml"

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)
        self.valuespacesMapping = Valuespaces()

    def getUri(self, response):
        return response.meta["item"].xpath("url_datensatz//text()").get()

    def start_requests(self):
        yield scrapy.Request(url=self.rssUrl, callback=self.parseList)

    def parseList(self, response):
        ids = []
        for item in response.xpath("//elixier/datensatz"):
            id = item.xpath("id_local//text()").get()
            if not id in ids:
                ids.append(id)
                copyResponse = response.copy()
                copyResponse.meta["item"] = item
                yield self.parse(copyResponse)

    def parse(self, response):
        return LomBase.parse(self, response)

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        text = response.meta["item"].xpath("systematikpfad//text()").get()
        for entry in self.valuespacesMapping.data["discipline"]:
            if entry["prefLabel"]["de"].casefold() in text.casefold():
                valuespaces.add_value("discipline", entry["id"])
        return valuespaces

    def mapResponse(self, response):
        r = ResponseItemLoader()
        r.add_value("url", self.getUri(response))
        r.add_value(
            "text",
            requests.get(
                response.meta["item"].xpath("url_datensatz//text()").get()
            ).content.decode("UTF-8"),
        )
        return r

    def getId(self, response):
        return response.meta["item"].xpath("id_local//text()").get()

    def getHash(self, response):
        return response.meta["item"].xpath("letzte_aenderung//text()").get()

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        base.add_value(
            "lastModified",
            response.meta["item"].xpath("letzte_aenderung//text()").get(),
        )
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value(
            "title",
            HTMLParser().unescape(response.meta["item"].xpath("titel//text()").get()),
        )
        general.add_value(
            "language", response.meta["item"].xpath("sprache//text()").get()
        )
        general.add_value(
            "keyword",
            HTMLParser()
            .unescape(response.meta["item"].xpath("schlagwort//text()").get())
            .split("; "),
        )
        desc = response.meta["item"].xpath("beschreibung//text()").get().strip()
        # dirty cleaning of invalid descriptions
        # not perfect yet, these objects also appear inside the content
        if not desc.startswith("swiffyobject_"):
            general.add_value("description", HTMLParser().unescape(desc))
        return general

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", "text/html")
        technical.add_value(
            "location", response.meta["item"].xpath("url_datensatz//text()").get()
        )
        return technical

    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        if (
            response.meta["item"].xpath("rechte//text()").get()
            == "Keine Angabe, es gilt die gesetzliche Regelung"
        ):
            license.add_value("internal", Constants.LICENSE_COPYRIGHT_LAW)
        return license
