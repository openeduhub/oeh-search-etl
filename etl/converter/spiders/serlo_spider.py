from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase
from converter.spiders.json_base import JSONBase
import json
import logging
from html.parser import HTMLParser
from converter.pipelines import ProcessValuespacePipeline
import re
from converter.constants import Constants

# Spider to fetch API from Serlo
class SerloSpider(scrapy.Spider, LomBase, JSONBase):
    name = "serlo_spider"
    friendlyName = "Serlo"
    url = "https://de.serlo.org"
    version = "0.1.0"

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self):
        url = self.url + "/entity/api/json/export/article"
        # current dummy fallback since the Serlo API is basically down
        # url = "http://localhost/sources/serlo.json"

        yield scrapy.Request(url=url, callback=self.parseList)

    # some fields are having xml entities (for whatever reason), we will unescape them here
    def get(self, *params, response):
        data = JSONBase.get(self, *params, json=response.meta["json"])
        try:
            return HTMLParser().unescape(data)
        except:
            try:
                result = []
                for p in data:
                    result.append(HTMLParser().unescape(p))
                return result
            except:
                return data

    def parseList(self, response):
        data = json.loads(response.body)
        for j in data:
            responseCopy = response.replace(url=self.url + j["link"] + "?contentOnly")
            responseCopy.meta["json"] = j
            if self.hasChanged(responseCopy):
                yield scrapy.Request(
                    url=responseCopy.url,
                    callback=self.parse,
                    meta={"json": j, "url": responseCopy.url},
                )

    def getId(self, response=None):
        return self.get("guid", response=response)

    def getHash(self, response=None):
        return self.version + self.get("lastModified.date", response=response)

    def parse(self, response):
        if not self.get("description", response=response):
            logging.info("skipping empty entry in serlo")
            return None
        return LomBase.parse(self, response)

    def mapResponse(self, response):
        r = LomBase.mapResponse(self, response)
        text = r.load_item()["text"].split(
            "Dieses Werk steht unter der freien Lizenz CC BY-SA 4.0 Information"
        )[0]
        r.replace_value("text", text)
        return r

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        base.add_value("lastModified", self.get("lastModified.date", response=response))
        base.add_value(
            "ranking",
            0.9
            + (
                float(self.get("revisionsCount", response=response)) / 2
                + float(self.get("authorsCount", response=response))
            )
            / 50,
        )
        return base

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response=response)
        text = self.get("categories", response=response)[0].split("/")[0]
        # manual mapping to Mathematik
        if text == "Mathe":
            text = "Mathematik"
        valuespaces.add_value("discipline", text)
        # for entry in ProcessValuespacePipeline.valuespaces['discipline']:
        #  if len(list(filter(lambda x:x['@value'].casefold() == text.casefold(), entry['label']))):
        #    valuespaces.add_value('discipline',entry['id'])

        primarySchool = re.compile("Klasse\s[1-4]$", re.IGNORECASE)
        if len(
            list(filter(lambda x: primarySchool.match(x), self.getKeywords(response)))
        ):
            valuespaces.add_value("educationalContext", "Grundschule")
        sek1 = re.compile("Klasse\s([5-9]|10)$", re.IGNORECASE)
        if len(list(filter(lambda x: sek1.match(x), self.getKeywords(response)))):
            valuespaces.add_value("educationalContext", "Sekundarstufe 1")
        sek2 = re.compile("Klasse\s1[1-2]", re.IGNORECASE)
        if len(list(filter(lambda x: sek2.match(x), self.getKeywords(response)))):
            valuespaces.add_value("educationalContext", "Sekundarstufe 2")
        return valuespaces

    def getKeywords(self, response):
        try:
            keywords = list(self.get("keywords", response=response).values())
        except:
            keywords = self.get("keywords", response=response)
        for c in self.get("categories", response=response):
            keywords += c.split("/")
        return set(keywords)

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response=response)
        general.add_value("title", self.get("title", response=response))
        general.add_value("keyword", self.getKeywords(response))
        general.add_value("description", self.get("description", response=response))
        return general

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("location", response.url)
        technical.add_value("format", "text/html")
        technical.add_value("size", len(response.body))
        return technical

    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        license.add_value("url", Constants.LICENSE_CC_BY_SA_40)
        return license
