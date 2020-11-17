from converter.items import *
from datetime import datetime
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base_no_parse import LomBase
from converter.spiders.json_base import JSONBase
import json
import time
import logging
from html.parser import HTMLParser
import html

# base spider mapping data via LRMI inside the html pages
# Please override the lrmi_path if necessary and add your sitemap_urls
class LrmiBase(LomBase, JSONBase):
    friendlyName = "LRMI-Header Based spider"
    lrmi_path = '//script[@type="application/ld+json"]//text()'
    sitemap_urls = []

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def getLRMI(self, *params, response):
        try:
            lrmi = list(
                map(
                    lambda x: json.loads(x.replace("\r", "").replace("\n", " ")),
                    response.xpath(self.lrmi_path).getall(),
                )
            )
        except:
            logging.warning(
                "failed parsing lrmi at " + response.url + ", please check source"
            )
            return None
        for l in lrmi:
            value = JSONBase.get(self, *params, json=l)
            if value != None:
                return html.unescape(value)
        return None

    # def parse(self, response):
    #     return LomBase.parse(self, response)

    # def getId(self, response):
    #     return self.getLRMI("identifier", "url", "name", response=response)

    def getHash(self, response):
        if self.get("version") != None:
            return self.getLRMI("version", response=response)
        return time.time()

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        base.add_value("thumbnail", self.getLRMI("thumbnailUrl", response=response))
        base.add_value(
            "lastModified",
            self.getLRMI("dateModified", "datePublished", response=response),
        )
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("identifier", self.getLRMI("identifier", response=response))
        general.add_value("title", self.getLRMI("name", response=response))
        general.add_value("keyword", self.getLRMI("keywords", response=response))
        general.add_value("language", self.getLRMI("inLanguage", response=response))
        general.add_value(
            "description", self.getLRMI("description", "about", response=response)
        )
        return general

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.add_value(
            "intendedEndUserRole",
            self.getLRMI("audience.educationalRole", response=response),
        )
        return valuespaces

    def getLOMEducational(self, response):
        educational = LomBase.getLOMEducational(self, response)
        educational.add_value(
            "typicalLearningTime", self.getLRMI("timeRequired", response=response)
        )
        return educational


    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        license.add_value("url", self.getLRMI("license", response=response))
        return license

    def getLOMTechnical(self, response):
        print("get LRMI technical")
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", self.getLRMI("fileFormat", response=response))
        technical.add_value("size", self.getLRMI("ContentSize", response=response))
        url = self.getLRMI("url", response=response)
        if not url:
            url = response.url
        technical.add_value("location", url)
        return technical
