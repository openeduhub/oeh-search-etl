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
    version = "0.1.4"
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
        return response.meta["item"].get("updated") + "v" + self.version

    def getUri(self, response=None) -> str:
        # or media.originalUrl?
        return self.get("media.url", json=response.meta["item"])

    def startRequest(self, page=0):
        return scrapy.Request(
            url=self.apiUrl,
            callback=self.parse_request,
            body=json.dumps({
                "query": f"""{{
                    findAllMetadata(page: {page}, pageSize: {self.page_size}) {{
                        id
                        identifier
                        title
                        description
                        keywords
                        language
                        creationDate
                        updated
                        publishedTime
                        availableTo
                        recordStatus
                        author
                        authorWebsite
                        producer
                        publishers {{
                            id
                            title
                            description
                            imageDetails
                            imagePreview
                            officialWebsite
                            linkToGeneralUseRights
                        }}
                        source {{
                            id
                            name
                            description
                            imageUrl
                            termsOfUse
                            generalUseRights
                            website
                            sourceStatus
                            created
                            edited
                        }}
                        media {{
                            size
                            dataType
                            duration
                            thumbDetails
                            thumbPreview
                            url
                            originalUrl
                        }}
                        targetAudience
                        learnResourceType
                        educationalLevels
                        classLevel
                        schoolTypes
                        eafCode
                        subject {{
                            id
                            name
                            level
                            path
                        }}
                        competencies {{
                            id
                            level
                            name
                            path
                        }}
                        license {{
                        name
                        version
                        country
                        url
                        text
                        }}
                        additionalLicenseInformation
                        downloadRight
                        cost
                        linkedObjects
                        }}
                    }}""",
                "operationName": None
            }),
            method="POST",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.access_token
            },
            meta={"page": page},
        )

    def start_requests(self):
        yield self.startRequest()

    def parse_request(self, response):
        results = json.loads(response.body)
        if results:
            list = results['data']['findAllMetadata']
            if len(list) == 0:
                return
            for item in list:
                copyResponse = response.copy()
                copyResponse.meta["item"] = item
                if self.hasChanged(copyResponse):
                    yield self.handleEntry(copyResponse)
            yield self.startRequest(response.meta["page"] + 1)

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

    def getLOMLifecycle(self, response=None) -> LomLifecycleItemloader:
        lifecycle = LomBase.getLOMLifecycle(response)

        return lifecycle

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
        licenseUrl = self.get("license.url", json=response.meta["item"])
        # @TODO: add mappings for the sodix names
        # {None, 'CC BY-NC-SA', 'Copyright, lizenzpflichtig', 'CC BY-SA', 'CC BY-ND', 'CC BY', 'CC0', 'freie Lizenz', 'CC BY-NC-ND', 'keine Angaben (gesetzliche Regelung)', 'CC BY-NC', 'Gemeinfrei / Public Domain', 'Copyright, freier Zugang'}
        url = None
        # {'', 'https://creativecommons.org/licenses/by-nd/4.0/deed.de', 'https://creativecommons.org/licenses/by-sa/3.0/deed.de', 'https://creativecommons.org/licenses/by/3.0/deed.de', 'https://creativecommons.org/licenses/by-nc-sa/4.0/deed.de', 'https://creativecommons.org/licenses/by-nc-nd/4.0/deed.de', 'https://creativecommons.org/licenses/by/2.0/deed.de', 'https://creativecommons.org/licenses/by/4.0/', 'https://creativecommons.org/licenses/by-nc-nd/2.0/de/', 'https://creativecommons.org/licenses/by-nc-nd/3.0/de/', 'https://creativecommons.org/licenses/by-sa/2.0/deed.de', 'https://creativecommons.org/licenses/by-nd/3.0/deed.de', 'https://creativecommons.org/licenses/by-nd/2.0/de/', 'https://creativecommons.org/licenses/by-nc-sa/3.0/deed.de', 'https://creativecommons.org/licenses/by-sa/4.0/deed.de', 'https://creativecommons.org/licenses/by/2.5/deed.de', 'https://creativecommons.org/licenses/by-sa/2.0/de/', 'https://creativecommons.org/licenses/by/3.0/de/', 'https://creativecommons.org/licenses/by-nc-nd/3.0/deed.de', 'https://creativecommons.org/licenses/by-nc/3.0/de/', 'https://creativecommons.org/licenses/by-nd/3.0/de/', 'https://creativecommons.org/licenses/by-sa/2.5/deed.de', 'https://creativecommons.org/publicdomain/mark/1.0/deed.de', 'https://creativecommons.org/licenses/by-nc-sa/2.0/deed.de', 'https://creativecommons.org/licenses/by-sa/2.0/fr/deed.de', 'https://creativecommons.org/licenses/by-nc/3.0/deed.de', None, 'https://creativecommons.org/licenses/by-nc-sa/2.5/deed.de', 'https://creativecommons.org/licenses/by-nc/4.0/deed.de', 'https://creativecommons.org/publicdomain/zero/1.0/deed.de', 'https://creativecommons.org/licenses/by-sa/3.0/de/', 'https://creativecommons.org/licenses/by-nc-sa/3.0/de/'}
        license.add_value("url", url)
        return license

    def getLOMEducational(self, response=None) -> LomEducationalItemLoader:
        educational = LomBase.getLOMEducational(response)
        class_level = self.get('classLevel', json=response.meta['item'])
        if class_level and len(class_level.split("-")) == 2:
            split = class_level.split("-")
            tar = LomAgeRangeItemLoader()
            # mapping from classLevel to ageRange
            tar.add_value(
                "fromRange",
                int(split[0]) + 5
            )
            tar.add_value(
                "toRange",
                int(split[1]) + 5
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

