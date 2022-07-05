import json

import requests
import scrapy

from converter.constants import *
from converter.items import *
from .base_classes import JSONBase
from .base_classes import LomBase
# Spider to fetch RSS from planet schule
from .. import env


class SodixSpider(scrapy.Spider, LomBase, JSONBase):
    name = "sodix_spider"
    friendlyName = "Sodix"
    url = "https://sodix.de/"
    version = "0.1.7"
    apiUrl = "https://api.sodix.de/gql/graphql"
    page_size = 2500
    custom_settings = {
        "ROBOTSTXT_OBEY": False  # returns an 401-error anyway, we might as well skip this scrapy.Request
    }

    MAPPING_LRT = {
        "APP": "application",
        "ARBEITSBLATT": "worksheet",
        "AUDIO": "audio",
        "AUDIOVISUELLES": "audiovisual medium",
        "BILD": "image",
        "DATEN": "data",
        "ENTDECKENDES": "exploration",
        "EXPERIMENT": "experiment",
        "FALLSTUDIE": "case_study",
        "GLOSSAR": "glossary",
        "HANDBUCH": "guide",
        # "INTERAKTION": "",
        "KARTE": "map",
        "KURS": "course",
        "LERNKONTROLLE": "assessment",
        "LERNSPIEL": "educational Game",
        "MODELL": "model",
        "OFFENE": "open activity",
        "PRESENTATION": "presentation",
        "PROJECT": "project",
        "QUELLE": "reference",
        "RADIO": "broadcast",
        "RECHERCHE": "enquiry-oriented activity",
        "RESSOURCENTYP": "other",  # "Anderer Ressourcentyp"
        "ROLLENSPIEL": "role play",
        "SIMULATION": "simulation",
        "SOFTWARE": "application",
        "SONSTIGES": "other",
        "TEST": "assessment",
        "TEXT": "text",
        "UBUNG": "drill and practice",
        "UNTERRICHTSBAUSTEIN": "teaching module",
        "UNTERRICHTSPLANUNG": "lesson plan",
        "VERANSCHAULICHUNG": "demonstration",
        "VIDEO": "video",
        "WEBSEITE": "web page",
        "WEBTOOL": ["web page", "tool"],

    }
    MAPPING_EDUCONTEXT = {
        "Primarbereich": "Primarstufe",
        "Fort- und Weiterbildung": "Fortbildung"
    }

    MAPPING_INTENDED_END_USER_ROLE = {
        "pupils": "learner",
    }

    MAPPING_LICENSE_NAMES = {
        'CC BY': Constants.LICENSE_CC_BY_40,
        'CC BY-NC': Constants.LICENSE_CC_BY_NC_40,
        'CC BY-NC-ND': Constants.LICENSE_CC_BY_NC_ND_40,
        'CC BY-NC-SA': Constants.LICENSE_CC_BY_NC_SA_40,
        'CC BY-ND': Constants.LICENSE_CC_BY_ND_40,
        'CC BY-SA': Constants.LICENSE_CC_BY_SA_40,
        'CC0': Constants.LICENSE_CC_ZERO_10,
        'Copyright, freier Zugang': Constants.LICENSE_COPYRIGHT_LAW,
        'Copyright, lizenzpflichtig': Constants.LICENSE_COPYRIGHT_LAW,
        'Gemeinfrei / Public Domain': Constants.LICENSE_PDM,
        'freie Lizenz': Constants.LICENSE_CUSTOM,
        'keine Angaben (gesetzliche Regelung)': Constants.LICENSE_CUSTOM,
    }

    # DEBUG_SUBJECTS = set()

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def mapResponse(self, response):
        r = LomBase.mapResponse(self, response, fetchData=False)
        r.replace_value("text", "")
        r.replace_value("html", "")
        r.replace_value("url", response.meta["item"].get("media").get("url"))
        return r

    def getId(self, response):
        return response.meta["item"].get("id")

    def getHash(self, response):
        return f"{response.meta['item'].get('updated')}v{self.version}"

    def getUri(self, response=None) -> str:
        # or media.originalUrl?
        return self.get("media.url", json=response.meta["item"])

    def startRequest(self, page=0):
        access_token = requests.post(
            "https://api.sodix.de/gql/auth/login",
            None,
            {
                "login": env.get("SODIX_SPIDER_USERNAME"),
                "password": env.get("SODIX_SPIDER_PASSWORD"),
            }
        ).json()['access_token']
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
                "Authorization": "Bearer " + access_token
            },
            meta={"page": page},
        )

    def start_requests(self):
        yield self.startRequest()

    def parse_request(self, response):
        results = json.loads(response.body)
        if results:
            metadata_items: dict = results['data']['findAllMetadata']
            # if len(metadata_items) == 0:
            #     return
            if metadata_items:
                # lists and dictionaries only become True if they have >0 entries, empty lists are considered False
                for item in metadata_items:
                    response_copy = response.copy()
                    response_copy.meta["item"] = item
                    if self.hasChanged(response_copy):
                        yield self.handleEntry(response_copy)
                # ToDo: links to binary files (.jpeg) cause errors while building the BaseItem, we might have to filter
                #  specific media types / URLs
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
        if "keywords" in response.meta["item"]:
            keywords: list = self.get("keywords", json=response.meta["item"])
            if keywords:
                # making sure that we're not receiving an empty list
                for individual_keyword in keywords:
                    if individual_keyword.strip():
                        # we're only adding valid keywords, none of the empty (whitespace) strings
                        general.add_value('keyword', individual_keyword)
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
        original = self.get("media.originalUrl", json=response.meta["item"])
        if original:
            technical.add_value(
                "location", original
            )
        duration: str = self.get("media.duration", json=response.meta["item"])
        if duration and duration != 0:
            # the API response contains "null"-values, we're making sure to only add valid duration values to our item
            technical.add_value("duration", duration)
        technical.add_value(
            "size", self.get("media.size", json=response.meta["item"])
        )
        return technical

    def getLicense(self, response):
        license_loader = LomBase.getLicense(self, response)

        author: str = self.get('author', json=response.meta['item'])
        if author:
            license_loader.add_value('author', author)
        license_description: str = self.get("license.text", json=response.meta["item"])
        if license_description:
            license_loader.add_value('description', license_description)
        license_name: str = self.get("license.name", json=response.meta["item"])
        if license_name:
            if license_name in self.MAPPING_LICENSE_NAMES:
                license_internal_mapped = self.MAPPING_LICENSE_NAMES.get(license_name)
                if license_name.startswith("CC"):
                    # ToDo: for CC-licenses the actual URL is more precise than our 'internal' license mapping
                    # (you will see differences between the 'internal' value and the actual URL from the API,
                    # e.g. a license pointing to v3.0 and v4.0 at the same time)
                    pass
                else:
                    license_loader.add_value('internal', license_internal_mapped)
                    if not license_description:
                        # "name"-fields with the "Copyright, freier Zugang"-value don't have "text"-fields, therefore
                        # we're carrying over the custom description, just in case
                        license_loader.replace_value('description', license_name)

        license_url: str = self.get("license.url", json=response.meta["item"])
        # license_urls_sorted = ['https://creativecommons.org/licenses/by-nc-nd/2.0/de/',
        #                        'https://creativecommons.org/licenses/by-nc-nd/3.0/de/',
        #                        'https://creativecommons.org/licenses/by-nc-nd/3.0/deed.de',
        #                        'https://creativecommons.org/licenses/by-nc-nd/4.0/deed.de',
        #                        'https://creativecommons.org/licenses/by-nc-sa/2.0/deed.de',
        #                        'https://creativecommons.org/licenses/by-nc-sa/2.5/deed.de',
        #                        'https://creativecommons.org/licenses/by-nc-sa/3.0/de/',
        #                        'https://creativecommons.org/licenses/by-nc-sa/3.0/deed.de',
        #                        'https://creativecommons.org/licenses/by-nc-sa/4.0/deed.de',
        #                        'https://creativecommons.org/licenses/by-nc/3.0/de/',
        #                        'https://creativecommons.org/licenses/by-nc/3.0/deed.de',
        #                        'https://creativecommons.org/licenses/by-nc/4.0/deed.de',
        #                        'https://creativecommons.org/licenses/by-nd/2.0/de/',
        #                        'https://creativecommons.org/licenses/by-nd/3.0/de/',
        #                        'https://creativecommons.org/licenses/by-nd/3.0/deed.de',
        #                        'https://creativecommons.org/licenses/by-nd/4.0/deed.de',
        #                        'https://creativecommons.org/licenses/by-sa/2.0/de/',
        #                        'https://creativecommons.org/licenses/by-sa/2.0/deed.de',
        #                        'https://creativecommons.org/licenses/by-sa/2.0/fr/deed.de',
        #                        'https://creativecommons.org/licenses/by-sa/2.5/deed.de',
        #                        'https://creativecommons.org/licenses/by-sa/3.0/de/',
        #                        'https://creativecommons.org/licenses/by-sa/3.0/deed.de',
        #                        'https://creativecommons.org/licenses/by-sa/4.0/deed.de',
        #                        'https://creativecommons.org/licenses/by/2.0/deed.de',
        #                        'https://creativecommons.org/licenses/by/2.5/deed.de',
        #                        'https://creativecommons.org/licenses/by/3.0/de/',
        #                        'https://creativecommons.org/licenses/by/3.0/deed.de',
        #                        'https://creativecommons.org/licenses/by/4.0/',
        #                        'https://creativecommons.org/publicdomain/mark/1.0/deed.de',
        #                        'https://creativecommons.org/publicdomain/zero/1.0/deed.de']
        # ToDo: our constants.py doesn't have entries for v2.0 or 2.5 values of CC licenses
        if license_url:
            # making sure to only handle valid license urls, since the API result can be NoneType or empty string ('')
            if license_url.endswith("deed.de"):
                license_url = license_url[:-len("deed.de")]
            if license_url.endswith("/de/"):
                license_url = license_url[:-len("de/")]
                # cutting off the "de/"-part of the URL while leaving the rest intact
            elif license_url.endswith("/fr/"):
                license_url = license_url[:-len("fr/")]
            license_loader.replace_value('url', license_url)
        return license_loader

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
        if "subject" in response.meta['item'] is not None:
            # the "subject"-field does not exist in every item returned by the sodix API
            subjects = self.get('subject', json=response.meta['item'])
            if subjects:
                # the "subject"-key might exist in the API, but still be 'none'
                for subject in subjects:
                    # ToDo: there are (currently) 837 unique subjects across all 50.697 Items
                    #  - these values would be suitable as additional keywords
                    subject_name = subject['name']
                    # self.DEBUG_SUBJECTS.add(subject_name)
                    # print(f"Amount of Subjects: {len(self.DEBUG_SUBJECTS)} // SUBJECT SET: \n {self.DEBUG_SUBJECTS}")
                    valuespaces.add_value('discipline', subject_name)

        educational_context_list = self.get('educationalLevels', json=response.meta['item'])
        if educational_context_list:
            for potential_edu_context in educational_context_list:
                if potential_edu_context in self.MAPPING_EDUCONTEXT:
                    potential_edu_context = self.MAPPING_EDUCONTEXT.get(potential_edu_context)
                valuespaces.add_value('educationalContext', potential_edu_context)
        target_audience_list = self.get('targetAudience', json=response.meta['item'])
        if target_audience_list:
            for target_audience_item in target_audience_list:
                if target_audience_item in self.MAPPING_INTENDED_END_USER_ROLE:
                    target_audience_item = self.MAPPING_INTENDED_END_USER_ROLE.get(target_audience_item)
                valuespaces.add_value('intendedEndUserRole', target_audience_item)

        if self.get('cost', json=response.meta['item']) == "FREE":
            valuespaces.add_value("price", "no")
        potential_lrts = self.get('learnResourceType', json=response.meta['item'])
        # attention: sodix calls their LRT "learnResourceType"
        if potential_lrts:
            for potential_lrt in potential_lrts:
                if potential_lrt in self.MAPPING_LRT:
                    potential_lrt = self.MAPPING_LRT.get(potential_lrt)
                    valuespaces.add_value('learningResourceType', potential_lrt)
                else:
                    # ToDo: lrt values that can't get mapped should be put into "keywords" to avoid losing them
                    pass
        return valuespaces
