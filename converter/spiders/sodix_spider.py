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
from .. import env


class SodixSpider(scrapy.Spider, LomBase, JSONBase):
    name = "sodix_spider"
    friendlyName = "Sodix"
    url = "https://sodix.de/"
    version = "0.1.3"
    apiUrl = "https://api.sodix.de/gql/graphql"
    access_token: str = None
    page_size = 2500

    def __init__(self, **kwargs):
        self.access_token = requests.post(
            "https://api.sodix.de/gql/auth/login",
            None,
            {
                "login": env.get("SODIX_SPIDER_USERNAME"),
                "password": env.get("SODIX_SPIDER_PASSWORD"),
            }
        ).json()['access_token']
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
        return response.meta["item"].get("updated") + self.version

    def getUri(self, response=None) -> str:
        # or media.originalUrl?
        return self.get("media.url", json=response.meta["item"])

    def startRequest(self, offset=0):
        return scrapy.Request(
            url=self.apiUrl,
            callback=self.parseRequest,
            body=json.dumps({
                "query": "{\n    findAllMetadata(page: " + str(offset) + ", pageSize: " + str(
                    self.page_size) + ") {\n        id\n        identifier\n        title\n        description\n        keywords\n        language\n        creationDate\n        updated\n        publishedTime\n        availableTo\n        recordStatus\n        author\n        authorWebsite\n        producer\n        publishers{\n            id\n            title\n            description\n            imageDetails\n            imagePreview\n            officialWebsite\n            linkToGeneralUseRights       \n        }\n        source{\n            id\n            name\n            description\n            imageUrl\n            termsOfUse\n            generalUseRights\n            website\n            sourceStatus\n            created\n            edited            \n        }\n        media {\n            size\n            dataType\n            duration\n            thumbDetails\n            thumbPreview\n            url\n            originalUrl           \n        }\n        targetAudience\n        learnResourceType\n        educationalLevels\n        classLevel\n        schoolTypes\n        eafCode\n        subject{\n            id\n            name\n            level\n            path\n        }        \n        competencies{\n            id\n            level\n            name\n            path            \n        }\n        license{\n            name\n            version\n            country\n            url\n            text            \n        }\n        additionalLicenseInformation\n        downloadRight\n        cost\n        linkedObjects             \n    }\n}\n\n",
                "operationName": None
            }),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.access_token
            },
            meta={"offset": offset},
        )

    def start_requests(self):
        yield self.startRequest()

    def parseRequest(self, response):
        results = json.loads(response.body)
        if results:
            for item in results['data']['findAllMetadata']:
                copyResponse = response.copy()
                copyResponse.meta["item"] = item
                if self.hasChanged(copyResponse):
                    yield self.handleEntry(copyResponse)
            yield self.startRequest(response.meta["offset"] + self.page_size)

    def handleEntry(self, response):
        return LomBase.parse(self, response)

    # thumbnail is always the same, do not use the one from rss
    def getBase(self, response):
        base = LomBase.getBase(self, response)
        base.replace_value(
            "thumbnail", self.get("media.thumbPreview", json=response.meta["item"])
        )
        for publisher in self.get("publishers", json=response.meta["item"]):
            base.add_value(
                "publisher", publisher['title']
            )
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.replace_value(
            "title",
            self.get("title", json=response.meta["item"])
        )
        general.add_value(
            "keyword",
            self.get("keywords", json=response.meta["item"])
        )
        general.add_value(
            "description",
            self.get("description", json=response.meta["item"])
        )
        return general

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.replace_value("format", self.get("media.dataType", json=response.meta["item"]))
        technical.replace_value(
            "location", self.getUri(response)
        )
        technical.add_value(
            "duration", self.get("media.duration", json=response.meta["item"])
        )
        technical.add_value(
            "size", self.get("media.size", json=response.meta["item"])
        )
        return technical

    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        licenseId = self.get("license.name", json=response.meta["item"])
        # @TODO: add mappings for the sodix names
        url = None
        license.add_value("url", url)
        return license

    def getLOMEducational(self, response=None) -> LomEducationalItemLoader:
        educational = LomBase.getLOMEducational(response)
        class_level = self.get('classLevel', json=response.meta['item'])
        if class_level and len(class_level.split("-")) == 2:
            split = class_level.split("-")
            tar = LomAgeRangeItemLoader()
            tar.add_value(
                "fromRange",
                split[0]
            )
            tar.add_value(
                "toRange",
                split[1]
            )
            educational.add_value("typicalAgeRange", tar.load_item())
        return educational

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        subjects = self.get('subject', json=response.meta['item'])
        for subject in subjects if subjects else []:
            valuespaces.add_value("discipline", subject['name'])
        valuespaces.add_value("educationalContext", self.get('educationalLevels', json=response.meta['item']))
        # @TODO: add mappings!
        valuespaces.add_value("intendedEndUserRole", self.get('targetAudience', json=response.meta['item']))
        if self.get('cost', json=response.meta['item']) == "FREE":
            valuespaces.add_value("price", "no")

        # @TODO: mapping required:
        # enum LRT {
        #     APP
        # ARBEITSBLATT
        # AUDIO
        # AUDIOVISUELLES
        # BILD
        # DATEN
        # ENTDECKENDES
        # EXPERIMENT
        # FALLSTUDIE
        # GLOSSAR
        # HANDBUCH
        # INTERAKTION
        # KARTE
        # KURS
        # LERNKONTROLLE
        # LERNSPIEL
        # MODELL
        # OFFENE
        # PRESENTATION
        # PROJECT
        # QUELLE
        # RADIO
        # RECHERCHE
        # RESSOURCENTYP
        # ROLLENSPIEL
        # SIMULATION
        # SOFTWARE
        # SONSTIGES
        # TEST
        # TEXT
        # UBUNG
        # UNTERRICHTSBAUSTEIN
        # UNTERRICHTSPLANUNG
        # VERANSCHAULICHUNG
        # VIDEO
        # WEBSEITE
        # WEBTOOL
        # }
        valuespaces.add_value("learningResourceType", self.get('learnResourceType', json=response.meta['item']))
        return valuespaces

