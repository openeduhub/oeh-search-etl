import html
import os
import pathlib

import requests
import scrapy

from converter.constants import Constants
from converter.items import *
from converter.valuespace_helper import Valuespaces
from .base_classes import LomBase


class LeifiSpider(scrapy.Spider, LomBase):
    """
    LeifiSpider uses a local .xml file (which contains the RSS feed of leifiphysik.de) to crawl its elements.

    This crawler can only be run or locally debugged if you have the "leifi_feed_rss.xml" file
    in the correct directory, either locally or on your HTTP-Server in "/sources/leifi_feed_rss.xml".
    """
    name = "leifi_spider"
    friendlyName = "LEIFIphysik"
    url = "https://www.leifiphysik.de/"
    version = "0.1.1"   # last update: 2022-03-04
    # ToDo: enable the localhost rssUrl
    # rssUrl = "http://localhost/sources/leifi_feed_rss.xml"

    # For local testing/debugging ONLY:
    # first create a folder in this project root folder called 'sources' and add the 'leifi_feed_rss.xml'
    # ToDo: don't forget to enable the localhost rssUrl before commiting your changes!
    rssUrl = pathlib.Path(os.path.abspath('sources/leifi_feed_rss.xml')).as_uri()

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)
        self.valuespacesMapping = Valuespaces()

    def getUri(self, response):
        return response.meta["item"].xpath("url_datensatz//text()").get()

    def start_requests(self):
        yield scrapy.Request(url=self.rssUrl, callback=self.parse_xml)

    def parse_xml(self, response):
        ids = []
        for item in response.xpath("//elixier/datensatz"):
            item_id = item.xpath("id_local//text()").get()
            if item_id not in ids:
                ids.append(item_id)
                copy_response = response.copy()
                copy_response.meta["item"] = item
                yield self.parse(copy_response)

    async def parse(self, response):
        return await LomBase.parse(self, response)

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
            html.unescape(response.meta["item"].xpath("titel//text()").get()),
        )
        general.add_value(
            "language", response.meta["item"].xpath("sprache//text()").get()
        )
        general.add_value(
            "keyword",
            html.unescape(response.meta["item"].xpath("schlagwort//text()").get()).split("; "),
        )
        desc = response.meta["item"].xpath("beschreibung//text()").get().strip()
        # dirty cleaning of invalid descriptions
        # not perfect yet, these objects also appear inside the content
        if not desc.startswith("swiffyobject_"):
            general.add_value("description", html.unescape(desc))
        return general

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", "text/html")
        technical.add_value(
            "location", response.meta["item"].xpath("url_datensatz//text()").get()
        )
        return technical

    def getLicense(self, response):
        license_loader = LomBase.getLicense(self, response)
        if (
                response.meta["item"].xpath("rechte//text()").get()
                == "Keine Angabe, es gilt die gesetzliche Regelung"
        ):
            license_loader.add_value("internal", Constants.LICENSE_COPYRIGHT_LAW)
        return license_loader
