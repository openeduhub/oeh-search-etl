import json
from typing import Iterator

import requests
import scrapy

from converter.constants import *
from converter.items import *
from .base_classes import JSONBase
from .base_classes import LomBase
from .. import env
from ..items import LomLifecycleItemloader


def extract_eaf_codes_to_set(eaf_code_list: list[str]) -> set:
    """
    This helper method extracts (only valid) entries from a list of strings and returns a set.
    """
    temporary_set = set()
    for eaf_code in eaf_code_list:
        if eaf_code:
            # while this might be (theoretically) unnecessary, we're make sure to never grab empty strings
            temporary_set.add(eaf_code)
    return temporary_set


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
    version = "0.2.9"  # last update: 2022-01-10
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
        "RECHERCHE": "enquiry_oriented_activity",
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

    def __init__(self, oer_filter: str = "False", **kwargs):
        if oer_filter.lower() == "true" or env.get_bool(key='SODIX_SPIDER_OER_FILTER', default=False) is True:
            # Scrapy arguments are always handled as Strings, even if you try to set a boolean
            # see: https://docs.scrapy.org/en/latest/topics/spiders.html#spider-arguments
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
                    if self.OER_FILTER is True or env.get_bool('SODIX_SPIDER_OER_FILTER', default=False):
                        # Since DropItem exceptions can only be raised from within the pipeline, the filtering of items
                        # that aren't strictly OER-licenses needs to happen here.
                        #  - controlling the OER-Filter via spider arguments is useful for debugging, but we also need
                        #   an easy way to control the spider via the .env file (while running it as a Docker container)
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
        # for publisher in self.get("publishers", json=response.meta["item"]):
        #     base.add_value(
        #         "publisher", publisher['title']
        #     )
        # ToDo: the 'publisher'-field in BaseItem will be removed in the future
        base.add_value("status", self.get("recordStatus", json=response.meta["item"]))
        last_modified = self.get("updated", json=response.meta["item"])
        if last_modified:
            base.add_value('lastModified', last_modified)
        source_id: str = self.get("source.id", json=response.meta["item"])
        # ToDo: the crawler can't write description text to subfolder names yet
        #  'source.name' or 'source.description' could be used here to make the subfolders more human-readable
        if source_id:
            base.add_value('origin', source_id)
        self.extract_and_save_eaf_codes_to_custom_field(base, response)
        return base

    def extract_and_save_eaf_codes_to_custom_field(self, base: BaseItemLoader, response):
        """
        Extracts eafCodes as a String from two Sodix API fields ('eafCode', 'competencies.id') and saves them to
        'base.custom' as a dictionary.
        (The dictionary-key 'ccm:taxonentry' is (later on) used by es_connector.py to transmit the collected values
        into edu-sharing.)
        """
        eaf_code_subjects = set()
        eaf_code_competencies = set()
        eaf_code_subjects_list = self.get("eafCode", json=response.meta["item"])
        # Extracting eafCodes from 'subject.id':
        if eaf_code_subjects_list:
            eaf_code_subjects: set = extract_eaf_codes_to_set(eaf_code_subjects_list)
            # attention: eafCodes from Sodix field 'eafCode' and 'subject.id' carry the same information
        eaf_code_competencies_list: list[dict] = self.get("competencies", json=response.meta["item"])
        # eafCodes from Sodix field 'competencies.id' are not listed within the 'eafCode' field, therefore we're
        # gathering them separately and merge them with the other collected eafCodes if necessary
        if eaf_code_competencies_list:
            for competency_item in eaf_code_competencies_list:
                if "id" in competency_item:
                    competency_eaf_code: str = competency_item.get("id")
                    eaf_code_competencies.add(competency_eaf_code)
        # after collecting eafCodes from both Sodix fields, we're merging the sets (if possible) and saving them:
        if eaf_code_subjects and eaf_code_competencies:
            # subjects and competencies can be independently available from each other. If both fields are available
            # in Sodix, we merge the sets and save them to a list
            eaf_code_subjects.update(eaf_code_competencies)
            eaf_code_combined = list(eaf_code_subjects)
            eaf_code_combined.sort()
            base.add_value('custom', {
                'ccm:taxonentry': eaf_code_combined
            })
        elif eaf_code_subjects or eaf_code_competencies:
            if eaf_code_subjects:
                eaf_code_subjects_list: list = list(eaf_code_subjects)
                eaf_code_subjects_list.sort()
                base.add_value('custom', {
                    'ccm:taxonentry': eaf_code_subjects_list
                })
            if eaf_code_competencies:
                eaf_code_competencies_list: list = list(eaf_code_competencies)
                eaf_code_competencies_list.sort()
                base.add_value('custom', {
                    'ccm:taxonentry': eaf_code_competencies_list
                })

    def get_lom_lifecycle_author(self, response=None) -> LomLifecycleItemloader | None:
        lifecycle = LomBase.getLOMLifecycle(response)
        # the Sodix 'author'-field returns a wild mix of agencies, persons, usernames and project-names
        # therfore all author-strings from Sodix are treated as "organization"-values
        author = self.get("author", json=response.meta["item"])
        author_website = self.get("authorWebsite", json=response.meta["item"])
        if author and author_website:
            # edge-case: Some Sodix Items can have a "authorWebsite", but no valid "author"-value (e.g. null).
            # saving only the authorWebsite would lead to an empty author-symbol in the edu-sharing workspace view,
            # which is why the current workaround is to only save this field if BOTH values are available and valid.
            lifecycle.add_value('role', 'author')
            lifecycle.add_value('organization', author)
            lifecycle.add_value('url', author_website)
            return lifecycle
        else:
            return None

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
                        # this uuid is used by Sodix to differentiate publishers
                        lifecycle.add_value('uuid', publisher_sodix_uuid)
                if "officialWebsite" in publisher:
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

    def get_lom_lifecycle_metadata_provider(self, response=None) -> LomLifecycleItemloader:
        """
        Collects metadata from Sodix 'source'-field with the purpose of saving it to edu-sharing's
        'ccm:metadatacontributer_provider'-field.
        """
        lifecycle = LomBase.getLOMLifecycle(response)
        source: dict = self.get('source', json=response.meta["item"])
        if source:
            lifecycle.add_value('role', 'metadata_provider')
            # all 'source'-subfields are of Type: String
            if source.get('id'):
                lifecycle.add_value('uuid', source.get('id'))
            if source.get('name'):
                lifecycle.add_value('organization', source.get('name'))
            if source.get('created'):
                # LocalDateTime within the String, e.g.: "2022-10-17T11:42:49.198"
                lifecycle.add_value('date', source.get('created'))
            # ToDo: Sodix 'source.edited'-field also carries a LocalDateTime, but we currently can't make a distinction
            #  between lifecycle metadata_provider dates (e.g. between a creationDate <-> lastModified)
            if source.get('website'):
                lifecycle.add_value('url', source.get('website'))
        return lifecycle

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
            subjects = self.get_subject_dictionary(response)
            if subjects:
                subject_names = list(subjects.values())
                subject_names.sort()
                keywords_cleaned_up.extend(subject_names)
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

        # Sodix has TWO distinct identifiers (uuids) for their objects:
        # the Sodix field 'identifier' carries a prefix, e.g. "SODIX-<uuid>", "BY-<uuid>" etc.
        # the Sodix field 'id' is an uuid without further explanation
        # If both are available, they're saved as a [String] to 'cclom:general_identifier' (this might be necessary to
        # identify duplicates later in edu-sharing)
        sodix_identifier: str = self.get("identifier", json=response.meta["item"])
        if sodix_identifier:
            general.add_value('identifier', sodix_identifier)
        sodix_id: str = self.get("id", json=response.meta["item"])
        if sodix_id:
            general.add_value('identifier', sodix_id)
        return general

    def getLOMTechnical(self, response) -> LomTechnicalItemLoader:
        technical = LomBase.getLOMTechnical(self, response)
        technical.replace_value("format", self.get("media.dataType", json=response.meta["item"]))
        technical.replace_value(
            "location", self.getUri(response)
        )
        original = self.get("media.originalUrl", json=response.meta["item"])
        if original and self.getUri(response) != original:
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
                    Constants.LICENSE_CC_BY_20,
                    Constants.LICENSE_CC_BY_25,
                    Constants.LICENSE_CC_BY_30,
                    Constants.LICENSE_CC_BY_40,
                    Constants.LICENSE_CC_BY_SA_20,
                    Constants.LICENSE_CC_BY_SA_25,
                    Constants.LICENSE_CC_BY_SA_30,
                    Constants.LICENSE_CC_BY_SA_40,
                    Constants.LICENSE_CC_ZERO_10,
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
                license_mapped_url = self.MAPPING_LICENSE_NAMES.get(license_name)
                # if mapping was successful, license_mapped_url contains a license URL
                if license_name.startswith("CC"):
                    # for CC-licenses the actual URL is more precise than our 'internal' license mapping
                    # (you would see differences between the 'internal' value and the actual URL from the API,
                    # e.g. a license pointing to v3.0 and v4.0 at the same time)
                    pass
                else:
                    if license_mapped_url in [Constants.LICENSE_COPYRIGHT_LAW]:
                        license_loader.add_value('internal', license_mapped_url)
                    else:
                        license_loader.add_value('url', license_mapped_url)
                    if not license_description:
                        # "name"-fields with the "Copyright, freier Zugang"-value don't have "text"-fields, therefore
                        # we're carrying over the custom description, just in case
                        license_loader.replace_value('description', license_name)

        license_url: str = self.get("license.url", json=response.meta["item"])
        # possible license URL values returned by the Sodix API:
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

    def get_subject_dictionary(self, response) -> dict[str, str] | None:
        """
        Parses the Sodix API field 'subject' and returns a dictionary consisting of:
        Sodix 'subject.id' (= the eafCode of a "Schulfach") and its human-readable counterpart
        Sodix 'subject.name' as its value.
        """
        subject_dictionary = dict()
        if "subject" in response.meta['item'] is not None:
            # the "subject"-field does not exist in every item returned by the sodix API
            subjects_list: list = self.get('subject', json=response.meta['item'])
            if subjects_list:
                # the "subject"-key might exist in the API, but still be of 'None'-value
                for subject in subjects_list:
                    subject_name: str = subject['name']
                    subject_id: str = subject['id']
                    subject_dictionary.update({subject_id: subject_name})
                return subject_dictionary
            else:
                return None

    def getValuespaces(self, response) -> ValuespaceItemLoader:
        valuespaces = LomBase.getValuespaces(self, response)
        subjects = self.get_subject_dictionary(response)
        if subjects:
            subject_ids = list(subjects.keys())
            if subject_ids:
                subject_ids.sort()
                valuespaces.add_value('discipline', subject_ids)
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
        # attention: Sodix calls their LRT "learnResourceType", not "learningResourceType"
        if potential_lrts:
            for potential_lrt in potential_lrts:
                if potential_lrt in self.MAPPING_LRT:
                    potential_lrt = self.MAPPING_LRT.get(potential_lrt)
                valuespaces.add_value('learningResourceType', potential_lrt)
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

        # "UNTERRICHTSBAUSTEIN"-Materials need to handled as aggregationLevel = 2 (according to LOM-DE)
        potential_lrts = self.get('learnResourceType', json=response.meta['item'])
        if potential_lrts:
            if "UNTERRICHTSBAUSTEIN" in potential_lrts:
                general.add_value('aggregationLevel', 2)

        technical = self.getLOMTechnical(response)
        if self.get("author", json=response.meta["item"]):
            lifecycle_author = self.get_lom_lifecycle_author(response)
            if lifecycle_author:
                lom.add_value('lifecycle', lifecycle_author.load_item())
        if self.get("publishers", json=response.meta["item"]):
            # theoretically, there can be multiple publisher fields per item, but in reality this doesn't occur (yet).
            lifecycle_iterator: Iterator[LomLifecycleItemloader] = self.get_lom_lifecycle_publisher(response)
            for lifecycle_publisher in lifecycle_iterator:
                lom.add_value('lifecycle', lifecycle_publisher.load_item())
        if self.get("source", json=response.meta["item"]):
            lifecycle_metadata_provider = self.get_lom_lifecycle_metadata_provider(response)
            lom.add_value('lifecycle', lifecycle_metadata_provider.load_item())
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
