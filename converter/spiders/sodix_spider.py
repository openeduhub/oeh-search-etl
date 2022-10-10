import json
from typing import Iterator

import requests
import scrapy

from converter.constants import *
from converter.items import *
from .base_classes import JSONBase
from .base_classes import LomBase
from .. import env


class SodixSpider(scrapy.Spider, LomBase, JSONBase):
    """
    Crawler for learning materials from SODIX GraphQL API.
    This crawler cannot run without login-data. Please make sure that you have the necessary settings saved
    to your .env file:
    SODIX_SPIDER_USERNAME="your_username"
    SODIX_SPIDER_PASSWORD="your_password"
    SODIX_SPIDER_OER_FILTER=True/False
    """
    name = "sodix_spider"
    friendlyName = "Sodix"
    url = "https://sodix.de/"
    version = "0.2.0"  # last update: 2022-10-06
    apiUrl = "https://api.sodix.de/gql/graphql"
    page_size = 2500
    custom_settings = {
        "ROBOTSTXT_OBEY": False  # returns an 401-error anyway, we might as well skip this scrapy.Request
    }
    OER_FILTER = False  # flag used for controlling the crawling process between two modes
    # - by default (OER_FILTER=False), ALL entries from the GraphQL API are crawled.
    # - If OER_FILTER=TRUE, only materials with OER-compatible licenses are crawled (everything else gets skipped)
    # control the modes either
    # - via spider arguments: "scrapy crawl sodix_spider -a oer_filter=true"
    # - or by setting SODIX_SPIDER_OER_FILTER=True in your .env file
    NOT_OER_THROWAWAY_COUNTER = 0  # counts the amount of skipped items, in case that the OER-Filter is enabled

    MAPPING_LRT = {
        "APP": "application",
        "ARBEITSBLATT": "worksheet",
        "AUDIO": "audio",
        "AUDIOVISUELLES": "audiovisual medium",
        "BILD": "image",
        "BROSCHUERE": "text",
        "DATEN": "data",
        "ENTDECKENDES": "exploration",
        "EXPERIMENT": "experiment",
        "FALLSTUDIE": "case_study",
        "GLOSSAR": "glossary",
        "HANDBUCH": "guide",
        # "INTERAKTION": "",  # ToDo: find a fitting value or leave empty?
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

    MAPPING_SCHOOL_TYPES_TO_EDUCONTEXT = {
        "Berufsschule": "Berufliche Bildung",
        "Fachoberschule": "Sekundarstufe II",
        # "Förderschule": "Förderschule",
        "Gesamtschule": "Sekundarstufe I",
        "Grundschule": "Primarstufe",
        "Gymnasium": "Sekundarstufe II",
        "Kindergarten": "Elementarbereich",
        "Mittel- / Hauptschule": "Sekundarstufe I",
        "Realschule": "Sekundarstufe I"
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

    def __init__(self, oer_filter=False, **kwargs):
        if oer_filter == "True" or oer_filter == "true":
            # scrapy arguments are handled as strings
            self.OER_FILTER = True
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
        if self.OER_FILTER is True:
            recordstatus_parameter = ", recordStatus: ACTIVATED"
            # by using the recordStatus parameter during the GraphQL query, only a subset of available items is returned
            # by the Sodix API: OER-only items carry the recordStatus: ACTIVATED
        else:
            recordstatus_parameter = ""
            # if OER-Filter is off (default), the GraphQL query will return all items (including non-OER materials)
        return scrapy.Request(
            url=self.apiUrl,
            callback=self.parse_request,
            body=json.dumps({
                "query": f"""{{
                    findAllMetadata(page: {page}, pageSize: {self.page_size}{recordstatus_parameter}) {{
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
                    # ToDo: don't handle an entry if the license is not OER-compatible?
                    # (DropItem exceptions can only be raised from the pipeline)
                    if self.OER_FILTER is True or env.get_bool('SODIX_SPIDER_OER_FILTER', default=False):
                        # controlling the OER-Filter via spider arguments is useful for debugging, but we also need
                        # an easy way to control the spider via the .env file (while running as a Docker container)
                        if self.license_is_oer(response_copy) is False:
                            self.NOT_OER_THROWAWAY_COUNTER += 1
                            self.logger.info(f"Item dropped due to OER-incompatibility. \n"
                                             f"Total amount of items dropped so far: "
                                             f"{self.NOT_OER_THROWAWAY_COUNTER}")
                            continue
                    if self.hasChanged(response_copy):
                        yield self.handleEntry(response_copy)
                # ToDo: links to binary files (.jpeg) cause errors while building the BaseItem, we might have to filter
                #  specific media types / URLs
                yield self.startRequest(response.meta["page"] + 1)

    def handleEntry(self, response):
        return self.parse(response=response)

    # thumbnail is always the same, do not use the one from rss
    def getBase(self, response) -> BaseItemLoader:
        base = LomBase.getBase(self, response)
        # thumbnail-priority from different fields:
        # 1) media.thumbDetails (480x360) 2) media.thumbPreview (256x256) 3) source.imageUrl (480x360)
        media_thumb_details = self.get("media.thumbDetails", json=response.meta["item"])
        media_thumb_preview = self.get("media.thumbPreview", json=response.meta["item"])
        source_image_url = self.get("source.imageUrl", json=response.meta["item"])
        if media_thumb_details:
            base.replace_value("thumbnail", media_thumb_details)
        elif media_thumb_preview:
            base.replace_value("thumbnail", media_thumb_preview)
        elif source_image_url:
            base.replace_value("thumbnail", source_image_url)
        for publisher in self.get("publishers", json=response.meta["item"]):
            base.add_value(
                "publisher", publisher['title']
            )
        # ToDo: use 'source'-field from the GraphQL item for 'origin'?
        return base

    def get_lom_lifecycle_author(self, response=None) -> LomLifecycleItemloader:
        lifecycle = LomBase.getLOMLifecycle(response)
        # the Sodix 'author'-field returns a wild mix of agencies, persons, usernames and project-names
        # which would inevitably lead to bad metadata in this field. It is therefore only used in license.author
        author_website = self.get("authorWebsite", json=response.meta["item"])
        if author_website:
            lifecycle.add_value('role', 'author')
            lifecycle.add_value('url', author_website)
        return lifecycle

    def get_lom_lifecycle_publisher(self, response=None) -> Iterator[LomLifecycleItemloader]:
        lifecycle = LomBase.getLOMLifecycle(response)
        publishers: list[dict] = self.get("publishers", json=response.meta["item"])
        # Sodix 'publishers'-field is a list of Publishers, therefore we need to iterate through them
        if publishers:
            for publisher in publishers:
                lifecycle.add_value('role', 'publisher')
                if "title" in publisher:
                    publisher_name = publisher.get("title")
                    if publisher_name:
                        lifecycle.add_value('organization', publisher_name)
                if "id" in publisher:
                    publisher_sodix_uuid: str = publisher.get("id")
                    if publisher_sodix_uuid:
                        lifecycle.add_value('uuid', publisher_sodix_uuid)
                if "officialWebsite" in publishers:
                    publisher_url: str = publisher.get("officialWebsite")
                    if publisher_url:
                        lifecycle.add_value('url', publisher_url)
            published_time = self.get("publishedTime", json=response.meta["item"])
            creation_date = self.get("creationDate", json=response.meta["item"])
            source: dict = self.get("source", json=response.meta["item"])
            if published_time:
                # the 'publishedTime'-field is 95% null or empty, which is why several fallbacks are needed
                lifecycle.add_value('date', published_time)
            elif creation_date:
                lifecycle.add_value('date', creation_date)
            elif source:
                if "created" in source:
                    # Sodix field 'source.created' is of type LocalDateTime and available most of the time. Its usage
                    # and meaning is undocumented, though, which is why we use this field only as the last fallback
                    # in case the other fields aren't available
                    created_date = source.get("created")
                    if created_date:
                        lifecycle.add_value('date', created_date)
            yield lifecycle

    def getLOMGeneral(self, response) -> LomGeneralItemloader:
        general = LomBase.getLOMGeneral(self, response)
        general.replace_value(
            "title",
            self.get("title", json=response.meta["item"])
        )
        if "keywords" in response.meta["item"]:
            keywords: list = self.get("keywords", json=response.meta["item"])
            keywords_cleaned_up: list = list()
            if keywords:
                # making sure that we're not receiving an empty list
                for individual_keyword in keywords:
                    if individual_keyword.strip():
                        # we're only adding valid keywords, none of the empty (whitespace) strings
                        keywords_cleaned_up.append(individual_keyword)
                        general.add_value('keyword', individual_keyword)
            subjects = self.get_subjects(response)
            if subjects:
                keywords_cleaned_up.extend(subjects)
                general.replace_value('keyword', keywords_cleaned_up)
        if "language" in response.meta["item"]:
            languages: list = self.get("language", json=response.meta["item"])
            if languages and isinstance(languages, list):
                # Sodix returns empty lists and 'null' occasionally
                for language in languages:
                    general.add_value('language', language)
        if "description" in response.meta["item"]:
            description: str = self.get("description", json=response.meta["item"])
            if description:
                # Sodix sometimes returns the 'description'-field as null
                general.add_value("description", description)
        return general

    def getLOMTechnical(self, response) -> LomTechnicalItemLoader:
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

    def license_is_oer(self, response) -> bool:
        """
        Checks if the Item is licensed under an OER-compatible license.
        Returns True if license is OER-compatible. (CC-BY/CC-BY-SA/CC0/PublicDomain)
        Otherwise returns False.
        """
        license_name: str = self.get("license.name", json=response.meta["item"])
        if license_name:
            if license_name in self.MAPPING_LICENSE_NAMES:
                license_internal_mapped = self.MAPPING_LICENSE_NAMES.get(license_name)
                return license_internal_mapped in [
                    Constants.LICENSE_CC_BY_30,
                    Constants.LICENSE_CC_BY_40,
                    Constants.LICENSE_CC_BY_SA_30,
                    Constants.LICENSE_CC_BY_SA_40,
                    Constants.LICENSE_CC_ZERO_10,
                    # ToDo: confirm if 'public domain' should be included in the OER-filter or not
                    Constants.LICENSE_PDM]

    def getLicense(self, response) -> LicenseItemLoader:
        license_loader = LomBase.getLicense(self, response)

        author: str = self.get('author', json=response.meta['item'])
        if author:
            license_loader.add_value('author', author)
        license_description: str = self.get("license.text", json=response.meta["item"])
        additional_license_information: str = self.get("additionalLicenseInformation")
        # the Sodix field 'additionalLicenseInformation' is empty 95% of the time, but sometimes it might serve as a
        # fallback for the license description
        if license_description:
            license_loader.add_value('description', license_description)
        elif additional_license_information:
            license_loader.add_value('description', additional_license_information)
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

    def get_subjects(self, response) -> list[Any] | None:
        # there are (currently) 837 unique subjects across all 50.697 Items, which are suitable to be used as additional
        # keyword values.
        subject_set = set()
        if "subject" in response.meta['item'] is not None:
            # the "subject"-field does not exist in every item returned by the sodix API
            subjects = self.get('subject', json=response.meta['item'])
            if subjects:
                # the "subject"-key might exist in the API, but still be of 'None'-value
                for subject in subjects:
                    subject_name = subject['name']
                    subject_set.add(subject_name)
                return list(subject_set)
            else:
                return None

    def getValuespaces(self, response) -> ValuespaceItemLoader:
        valuespaces = LomBase.getValuespaces(self, response)
        subjects = self.get_subjects(response)
        # ToDo: if subjects can't be mapped to SKOS, save them to the keywords field
        #   - this needs to happen during ValuespacePipeline mapping
        if subjects:
            for subject in subjects:
                valuespaces.add_value('discipline', subject)
        educational_context_list = self.get('educationalLevels', json=response.meta['item'])
        school_types_list = self.get('schoolTypes', json=response.meta['item'])
        educational_context_set = set()
        if educational_context_list:
            # the Sodix field 'educationalLevels' is directly mappable to our 'educationalContext'
            for potential_edu_context in educational_context_list:
                if potential_edu_context in self.MAPPING_EDUCONTEXT:
                    potential_edu_context = self.MAPPING_EDUCONTEXT.get(potential_edu_context)
                educational_context_set.add(potential_edu_context)
        elif school_types_list:
            # if 'educationalLevels' isn't available, fallback to: map 'schoolTypes'-field to 'educationalContext'
            for school_type in school_types_list:
                if school_type in self.MAPPING_SCHOOL_TYPES_TO_EDUCONTEXT:
                    school_type = self.MAPPING_SCHOOL_TYPES_TO_EDUCONTEXT.get(school_type)
                educational_context_set.add(school_type)
        educational_context_list = list(educational_context_set)
        educational_context_list.sort()
        if educational_context_list:
            valuespaces.add_value("educationalContext", educational_context_list)

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
                    pass
        # ToDo: Lisum special use-case: use 'ccm:taxonentry' to store eafCodes
        return valuespaces

    def parse(self, response, **kwargs):
        if LomBase.shouldImport(response) is False:
            self.logger.debug(
                f"Skipping entry {str(self.getId(response))} because shouldImport() returned false"
            )
            return None
        if self.getId(response) is not None and self.getHash(response) is not None:
            if not self.hasChanged(response):
                return None

        base = self.getBase(response)

        lom = LomBaseItemloader()
        general = self.getLOMGeneral(response)
        technical = self.getLOMTechnical(response)
        if self.get("author", json=response.meta["item"]):
            lifecycle_author = self.get_lom_lifecycle_author(response)
            lom.add_value('lifecycle', lifecycle_author.load_item())
        if self.get("publishers", json=response.meta["item"]):
            # theoretically, there can be multiple publisher fields per item, but in reality this doesn't occur (yet).
            lifecycle_iterator: Iterator[LomLifecycleItemloader] = self.get_lom_lifecycle_publisher(response)
            for lifecycle_publisher in lifecycle_iterator:
                lom.add_value('lifecycle', lifecycle_publisher.load_item())
        educational = self.getLOMEducational(response)
        classification = self.getLOMClassification(response)

        lom.add_value('general', general.load_item())
        lom.add_value('technical', technical.load_item())
        lom.add_value('educational', educational.load_item())
        lom.add_value('classification', classification.load_item())
        base.add_value("lom", lom.load_item())

        base.add_value("valuespaces", self.getValuespaces(response).load_item())
        base.add_value("license", self.getLicense(response).load_item())
        base.add_value("permissions", self.getPermissions(response).load_item())
        base.add_value("response", self.mapResponse(response).load_item())

        return base.load_item()
