from converter.items import *
from .base_classes import LomBase
from .base_classes import JSONBase
import json
import logging
import requests
import html
from converter.constants import *
import scrapy

# Spider to fetch RSS from planet schule
class WirLernenOnlineSpider(scrapy.Spider, LomBase, JSONBase):
    name = "wirlernenonline_spider"
    friendlyName = "WirLernenOnline"
    url = "https://wirlernenonline.de/"
    version = "0.1.3"
    apiUrl = "https://wirlernenonline.de/wp-json/wp/v2/%type/?per_page=50&page=%page"
    keywords = {}

    mappings = {
        'conditionsOfAccess': {
            '20': 'no_login',
            '21': 'login_for_additional_features',
            '22': 'login'
        },
        'price': {
            '30': 'no',
            '31': 'yes_for_additional',
            '32': 'yes'
        },
        'accessibilitySummary': {
            '60':  'a',
            '61': 'none',
            '62': 'invalid_value'
        },
        'dataProtectionConformity': {
            '50': 'generalDataProtectionRegulation',
            '51': 'noGeneralDataProtectionRegulation',
            '52': 'invalid_value',
        },
        'oer' : {
            '10': '0',
            '11': '1',
            '12': '2',
        }
    }

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

    def startRequest(self, type, page=1):
        return scrapy.Request(
            url=self.apiUrl.replace("%page", str(page)).replace("%type", type),
            callback=self.parseRequest,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            meta={"page": page, "type": type},
        )

    def start_requests(self):
        keywords = json.loads(
            requests.get(
                "https://wirlernenonline.de/wp-json/wp/v2/tags/?per_page=100"
            ).content.decode("UTF-8")
        )
        for keyword in keywords:
            self.keywords[keyword["id"]] = keyword["name"]

        yield self.startRequest("edusource")
        yield self.startRequest("edutool")

    def parseRequest(self, response):
        results = json.loads(response.body)
        if results:
            for item in results:
                copyResponse = response.copy()
                copyResponse.meta["item"] = item
                if self.hasChanged(copyResponse):
                    yield self.handleEntry(copyResponse)
            yield self.startRequest(response.meta["type"], response.meta["page"] + 1)

    def handleEntry(self, response):
        return LomBase.parse(self, response)

    def getType(self, response):
        if response.meta["type"] == "edusource":
            return Constants.NEW_LRT_MATERIAL
        elif response.meta["type"] == "edutool":
            return Constants.NEW_LRT_TOOL
        return None

    # thumbnail is always the same, do not use the one from rss
    def getBase(self, response):
        base = LomBase.getBase(self, response)
        base.replace_value(
            "thumbnail", self.get("acf.thumbnail.url", json=response.meta["item"])
        )
        fulltext = self.get("acf.long_text", json=response.meta["item"])
        base.replace_value("fulltext", html.unescape(fulltext))
        try:
            notes = '\n'.join(list(map(lambda x: x['notes'], self.get('acf.notizen', json=response.meta["item"]))))
            base.replace_value('notes', notes)
        except:
            pass
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.replace_value(
            "title",
            html.unescape(
                self.get("title.rendered", json=response.meta["item"])
            ),
        )
        keywords = self.get("tags", json=response.meta["item"])
        if keywords:
            keywords = list(map(lambda x: self.keywords[x], keywords))
            general.add_value("keyword", keywords)
        general.add_value(
            "description",
            html.unescape(
                self.get("acf.short_text", json=response.meta["item"])
            ),
        )
        return general

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.replace_value("format", "text/html")
        technical.replace_value(
            "location", self.get("acf.url", json=response.meta["item"])
        )
        return technical

    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        try:
            licenseId = self.get("acf.licence", json=response.meta["item"])[0]["value"]
            if licenseId == "10":
                license.add_value("oer", OerType.ALL)
            elif licenseId == "11":
                license.add_value("oer", OerType.MIXED)
            elif licenseId == "12":
                license.add_value("oer", OerType.NONE)
        except:
            pass
        return license

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.replace_value("new_lrt", self.getType(response))
        discipline = list(
            map(
                lambda x: x["value"],
                self.get("acf.fachgebiet", json=response.meta["item"]),
            )
        )
        valuespaces.add_value("discipline", discipline)
        lernresourcentyp = self.get("acf.lernresourcentyp", json=response.meta["item"])
        if lernresourcentyp:
            lernresourcentyp = list(map(lambda x: x["value"], lernresourcentyp))
            valuespaces.add_value("sourceContentType", lernresourcentyp)
        category = self.get("acf.category", json=response.meta["item"])
        if category:
            category = list(map(lambda x: x["value"], category))
            valuespaces.add_value("toolCategory", category)

        context = list(
            map(
                lambda x: x["value"],
                self.get("acf.schulform", json=response.meta["item"]),
            )
        )
        valuespaces.add_value("educationalContext", context)
        role = list(
            map(lambda x: x["value"], self.get("acf.role", json=response.meta["item"]))
        )
        valuespaces.add_value("intendedEndUserRole", role)

        self.addValuespace(valuespaces, 'conditionsOfAccess', 'acf.nutzung', response)
        valuespaces.add_value("containsAdvertisement", 'yes' if self.get('acf.advertisment', json=response.meta['item']) else 'no')
        self.addValuespace(valuespaces, 'price', 'acf.costs', response)
        self.addValuespace(valuespaces, 'accessibilitySummary', 'acf.accessibility', response)
        self.addValuespace(valuespaces, 'dataProtectionConformity', 'acf.dsgvo', response)

        self.addValuespace(valuespaces, 'oer', 'acf.licence', response)

        return valuespaces

    def addValuespace(self, valuespaces, key, key_wp, response):
        try:
            apiData = self.get(key_wp, json=response.meta['item'])
            if not isinstance(apiData, list):
                apiData = [apiData]
            data = list(
                map(lambda x: self.mappings[key][x['value']], apiData)
            )
            valuespaces.add_value(key, data)
        except:
            logging.info('Could not map ' + key_wp + ' to ' + key + ' for item ' + str(self.getId(response)))
            pass
