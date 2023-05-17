import html
import json
import logging
import time

from .json_base import JSONBase
from .lom_base import LomBase

# base spider mapping data via LRMI inside the html pages
# Please override the lrmi_path if necessary and add your sitemap_urls
from ...items import LicenseItemLoader


class LrmiBase(LomBase, JSONBase):
    friendlyName = "LRMI-Header Based spider"
    lrmi_path = '//script[@type="application/ld+json"]//text()'

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def getLRMI(self, *params, response):
        lrmi: list[dict] = list()
        if response:
            if response.selector.type == "html":
                # this check is necessary because querying a selector of type 'json' would result in an ValueError and
                # throw warnings
                lrmi_raw: list[str] = response.xpath(self.lrmi_path).getall()
                for lrmi_item in lrmi_raw:
                    lrmi_item = lrmi_item.replace("\r", "")
                    lrmi_item = lrmi_item.replace("\n", " ")
                    lrmi_item = lrmi_item.replace("\t", " ")
                    # after these steps there might still be multiple whitespaces within a json-ld object
                    lrmi_item = " ".join(lrmi_item.split())
                    if lrmi_item:
                        lrmi_object: dict = json.loads(lrmi_item)
                        lrmi.append(lrmi_object)
                    else:
                        logging.warning(
                            f"Failed parsing LRMI at {response.url} : After trying to sanitize the JSON string object, "
                            f"the final string was invalid."
                        )
            else:
                logging.warning(
                    f"Failed parsing lrmi at {response.url} , please check source (if there was an JSON-LD available)"
                )
                return None
        if lrmi and isinstance(lrmi, list):
            for lrmi_dict in lrmi:
                value = JSONBase.get(self, *params, json=lrmi_dict)
                if value is not None:
                    return html.unescape(value)
        return None

    async def parse(self, response):
        return await LomBase.parse(self, response)

    def getId(self, response):
        return self.getLRMI("identifier", "url", "name", response=response)

    def getHash(self, response):
        if self.get("version") is not None:
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
        general.add_value("description", self.getLRMI("description", "about", response=response))
        return general

    def getLOMEducational(self, response):
        educational = LomBase.getLOMEducational(self, response)
        educational.add_value("typicalLearningTime", self.getLRMI("timeRequired", response=response))
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
                logging.warning(
                    f"Could not map the received 'license'-value {license_raw} within LrmiBase. "
                    f"Please check Constants.py and LrmiBase for missing mappings/values."
                )
        else:
            logging.warning(
                "LrmiBase: The 'license'-field returned within the JSON_LD doesn't seem to be a URL.\n"
                "Please check if additional license-mapping is necessary within the spider itself."
            )
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
