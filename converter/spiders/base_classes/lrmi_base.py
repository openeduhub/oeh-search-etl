import re

from .lom_base import LomBase
from .json_base import JSONBase
import json
import time
import html
import logging

# base spider mapping data via LRMI inside the html pages
# Please override the lrmi_path if necessary and add your sitemap_urls
from ...constants import Constants
from ...items import LicenseItemLoader


class LrmiBase(LomBase, JSONBase):
    friendlyName = "LRMI-Header Based spider"
    lrmi_path = '//script[@type="application/ld+json"]//text()'

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

    def parse(self, response):
        return LomBase.parse(self, response)

    def getId(self, response):
        return self.getLRMI("identifier", "url", "name", response=response)

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
        general.add_value("title", self.getLRMI("name", "headline", response=response))
        general.add_value("keyword", self.getLRMI("keywords", response=response))
        general.add_value("language", self.getLRMI("inLanguage", response=response))
        general.add_value(
            "description", self.getLRMI("description", "about", response=response)
        )
        return general

    def getLOMEducational(self, response):
        educational = LomBase.getLOMEducational(self, response)
        educational.add_value(
            "typicalLearningTime", self.getLRMI("timeRequired", response=response)
        )
        return educational

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.add_value(
            "learningResourceType",
            self.getLRMI("learningResourceType", response=response),
        )
        valuespaces.add_value(
            "intendedEndUserRole",
            self.getLRMI("audience.educationalRole", response=response),
        )
        return valuespaces

    def getLicense(self, response):
        license_loader: LicenseItemLoader = LomBase.getLicense(self, response)
        license_raw = self.getLRMI("license", response=response)
        if license_raw:
            if license_raw.startswith("http"):
                # the "license" field holds a valid URL -> use it directly as is
                license_loader.add_value("url", license_raw)
            else:
                logging.warning(f"Could not map the received 'license'-value {license_raw} within LrmiBase. "
                                f"Please check Constants.py and LrmiBase for missing mappings/values.")
        else:
            logging.warning("LrmiBase: The 'license'-field returned within the JSON_LD doesn't seem to be a URL.\n"
                            "Please check if additional license-mapping is necessary within the spider itself.")
        return license_loader

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", self.getLRMI("fileFormat", response=response))
        technical.add_value("size", self.getLRMI("ContentSize", response=response))
        url = self.getLRMI("url", response=response)
        if not url:
            url = response.url
        technical.add_value("location", url)
        return technical
