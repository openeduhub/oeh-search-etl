from converter.items import *
from .base_classes import LomBase, JSONBase
import json
import requests
from converter.constants import *

# Spider to fetch RSS from planet schule
class SeguSpider(scrapy.Spider, LomBase, JSONBase):
    name = "segu_spider"
    friendlyName = "segu"
    url = "https://segu-geschichte.de/"
    version = "0.1.0"
    apiUrl = "https://segu-geschichte.de/wp-json/wp/v2/pages?page=%page"
    categories = {}
    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def mapResponse(self, response):
        r = LomBase.mapResponse(self, response, fetchData=False)
        r.replace_value("text", "")
        r.replace_value("html", "")
        r.replace_value("url", response.meta["item"].get("link"))
        return r

    def getId(self, response):
        return response.meta["item"].get("id")

    def getHash(self, response):
        return response.meta["item"].get("modified") + self.version

    def start_requests(self):
        categories = json.loads(
            requests.get(
                "https://segu-geschichte.de/wp-json/wp/v2/categories/?per_page=100"
            ).content.decode("UTF-8")
        )
        for cat in categories:
            self.categories[cat["id"]] = cat["name"]

        yield self.fetchPage()

    def fetchPage(self, page = 1):
        return scrapy.Request(
            url=self.apiUrl.replace("%page", str(page)),
            callback=self.parseRequest,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            meta={"page": page, "type": type},
        )
    def parseRequest(self, response):
        results = json.loads(response.body_as_unicode())
        if results:
            for item in results:
                copyResponse = response.copy()
                copyResponse.meta["item"] = item
                if self.hasChanged(copyResponse):
                    yield self.handleEntry(copyResponse)
            yield self.fetchPage(response.meta["page"] + 1)

    def handleEntry(self, response):
        return LomBase.parse(self, response)

    # thumbnail is always the same, do not use the one from rss
    def getBase(self, response):
        base = LomBase.getBase(self, response)
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

    def getLOMGeneral(self, response):
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

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.replace_value("format", "text/html")
        technical.replace_value(
            "location", self.get("link", json=response.meta["item"])
        )
        return technical

    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        license.add_value("url", Constants.LICENSE_CC_BY_SA_40)
        return license

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.add_value("discipline", "Geschichte")
        return valuespaces
