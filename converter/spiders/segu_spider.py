import json

import requests
import scrapy
from scrapy.spiders import CrawlSpider

from converter.constants import *
from .base_classes import LomBase, JSONBase


class SeguSpider(CrawlSpider, LomBase, JSONBase):
    name = "segu_spider"
    friendlyName = "segu"
    url = "https://segu-geschichte.de/"
    version = "0.1.1"  # last update: 2022-05-20
    apiUrl = "https://segu-geschichte.de/wp-json/wp/v2/pages?page=%page"
    categories = {}

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    async def mapResponse(self, response, **kwargs):
        r = await LomBase.mapResponse(self, response, fetchData=False)
        r.replace_value("text", "")
        r.replace_value("html", "")
        r.replace_value("url", response.meta["item"].get("link"))
        return r

    def getId(self, response=None) -> str:
        return response.meta["item"].get("id")

    def getHash(self, response=None):
        return response.meta["item"].get("modified") + self.version

    def start_requests(self):
        categories = json.loads(
            requests.get(
                "https://segu-geschichte.de/wp-json/wp/v2/categories/?per_page=100"
            ).content.decode("UTF-8")
        )
        for cat in categories:
            self.categories[cat["id"]] = cat["name"]

        yield self.fetch_page()

    def fetch_page(self, page=1):
        return scrapy.Request(
            url=self.apiUrl.replace("%page", str(page)),
            callback=self.parse_request,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            meta={"page": page, "type": type},
        )

    def parse_request(self, response: scrapy.http.TextResponse):
        results = response.json()
        if results:
            for item in results:
                response_copy = response.copy()
                response_copy.meta["item"] = item
                if self.hasChanged(response_copy):
                    yield self.handle_entry(response_copy)
            yield self.fetch_page(response.meta["page"] + 1)

    def handle_entry(self, response):
        return LomBase.parse(self, response)

    def getBase(self, response=None):
        base = LomBase.getBase(self, response)
        # thumbnail is always the same, do not use the one from rss
        base.replace_value(
            "thumbnail", self.get("acf.thumbnail.url", json=response.meta["item"])
        )
        base.replace_value(
            "fulltext",
            self.html2Text(
                self.get("content.rendered", json=response.meta["item"])
            ),
        )
        return base

    def getLOMGeneral(self, response=None):
        general = LomBase.getLOMGeneral(self, response)
        general.replace_value(
            "title",
            self.html2Text(
                self.get("title.rendered", json=response.meta["item"])
            ),
        )

        general.add_value(
            "description",
            self.html2Text(
                self.get("excerpt.rendered", json=response.meta["item"])
            ).replace("… weiterlesen …", ""),
        )
        cat = self.get("categories", json=response.meta["item"])
        if cat:
            general.add_value("keyword", list(map(lambda x: self.categories[x], cat)))
        return general

    def getLOMTechnical(self, response=None):
        technical = LomBase.getLOMTechnical(self, response)
        technical.replace_value("format", "text/html")
        technical.replace_value(
            "location", self.get("link", json=response.meta["item"])
        )
        return technical

    def getLicense(self, response=None):
        license_loader = LomBase.getLicense(self, response)
        license_loader.add_value("url", Constants.LICENSE_CC_BY_SA_40)
        return license_loader

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.add_value("discipline", "Geschichte")
        return valuespaces

    def parse(self, response, **kwargs):
        super().parse(response)
