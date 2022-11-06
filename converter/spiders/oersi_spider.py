import datetime
import logging
from typing import Optional

import requests
import scrapy

from converter.constants import Constants
from converter.es_connector import EduSharing
from converter.items import (
    BaseItemLoader,
    LomBaseItemloader,
    LomGeneralItemloader,
    LomTechnicalItemLoader,
    LomLifecycleItemloader,
    LomEducationalItemLoader,
    LomClassificationItemLoader,
    ValuespaceItemLoader,
    LicenseItemLoader,
    ResponseItemLoader,
)
from converter.spiders.base_classes import LomBase
from converter.web_tools import WebEngine, WebTools


class OersiSpider(scrapy.Spider, LomBase):
    """
    Crawls OERSI.org for metadata from different OER providers.

    You can control which metadata provider should be crawled by commenting/uncommenting their name within the
    ELASTIC_PROVIDERS_TO_CRAWL list.
    """

    name = "oersi_spider"
    # start_urls = ["https://oersi.org/"]
    friendlyName = "OERSI"
    version = "0.0.2"   # last update: 2022-11-06
    allowed_domains = "oersi.org"
    custom_settings = {
        "CONCURRENT_REQUESTS": 32,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 3,
        "WEB_TOOLS": WebEngine.Playwright,
    }

    ELASTIC_PARAMETER_KEEP_ALIVE: str = "1m"
    # for reference: https://www.elastic.co/guide/en/elasticsearch/reference/current/api-conventions.html#time-units
    ELASTIC_PARAMETER_REQUEST_SIZE: int = 1000  # maximum: 10.000, but responses for bigger request sizes take significantly longer

    ELASTIC_PIT_ID: dict = dict()
    # the provider-filter at https://oersi.org/resources/ shows you which String values can be used as a provider-name
    # ToDo: regularly check if new providers need to be added to the list below (and insert/sort them alphabetically!)
    ELASTIC_PROVIDERS_TO_CRAWL: list = [
        # "detmoldMusicTools",
        # "digiLL",
        # "DuEPublico",
        # "eaDNURT",
        # "eGov-Campus",
        # "HessenHub",
        # "HHU Mediathek",
        # "HOOU",
        # "iMoox",
        # "KI Campus",
        # "oncampus",
        # "openHPI",
        # "OpenLearnWare",
        "Open Music Academy"
        # "OpenRub",
        # "ORCA.nrw",
        # "RWTH Aachen GitLab",
        # "twillo",
        # "TIB AV-Portal",
        # "TU Delft OpenCourseWare",
        # "vhb",
        # "Virtual Linguistics Campus",
        # "ZOERR"
    ]
    # ToDo: DO NOT activate other providers until 'Hochschulfaechersystematik'-values are possible within edu-sharing!
    ELASTIC_ITEMS_ALL = list()

    MAPPING_HCRT_TO_NEW_LRT = {
        "diagram": "f7228fb5-105d-4313-afea-66dd59b1b6f8",  # "Graph, Diagramm und Charts"
        "portal": "d8c3ef03-b3ab-4a5e-bcc9-5a546fefa2e9",  # "Webseite und Portal (stabil)"
        "questionnaire": "d31a5b68-611f-4015-8be9-56bd5eb44c64",  # "Fragebogen und Umfragen"
        "reference_work": "c022c920-c236-4234-bae1-e264a3e2bdf6",  # "Nachschlagewerk und Glossar"
        "script": "6a15628c-0e59-43e3-9fc5-9a7f7fa261c4",  # "Skript, Handout und Handreichung"
        "sheet_music": "f7e92628-4132-4985-bcf5-93c285e300a8",  # "Noten"
        "textbook": "a5897142-bf57-4cd0-bcd9-7d0f1932e87a",  # "Lehrbuch und Grundlagenwerk (auch E-Book)"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Fetching a "point in time"-id for the subsequent ElasticSearch queries
        self.ELASTIC_PIT_ID = self.elastic_pit_get_id(self.elastic_pit_create())
        # querying the ElasticSearch API for metadata-sets of specific providers, this allows us to control which
        # providers we want to include/exclude by using the "ELASTIC_PROVIDERS_TO_CRAWL"-list
        self.ELASTIC_ITEMS_ALL = self.elastic_fetch_all_provider_pages()
        # after all items have been collected, delete the ElasticSearch PIT
        json_response = self.elastic_pit_delete()
        if json_response:
            logging.info(
                f"ElasticSearch API response (upon PIT delete): {json_response}"
            )

    def start_requests(self):
        for elastic_item in self.ELASTIC_ITEMS_ALL:
            main_entity_of_page: list[dict] = elastic_item.get("_source").get(
                "mainEntityOfPage"
            )
            if main_entity_of_page:
                item_url = main_entity_of_page[0].get("id")
                yield scrapy.Request(
                    url=item_url, cb_kwargs={"elastic_item": elastic_item}
                )

    def elastic_pit_create(self) -> dict:
        """
        Creates an ElasticSearch PIT (point-in-time), which is needed for iterating through the API results.
        See: https://www.elastic.co/guide/en/elasticsearch/reference/current/point-in-time-api.html
        """
        url = (
            f"https://oersi.org/resources/api-internal/search/oer_data/_pit?keep_alive="
            f"{self.ELASTIC_PARAMETER_KEEP_ALIVE}&pretty"
        )
        headers = {"accept": "application/json"}
        request = requests.post(
            url=url,
            headers=headers,
        )
        return request.json()

    @staticmethod
    def elastic_pit_get_id(pit_json_response) -> dict:
        response_json: dict = pit_json_response
        return response_json

    def elastic_pit_delete(self) -> dict:
        """
        Deletes the ElasticSearch PIT once it's no longer needed for page iteration. See:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/point-in-time-api.html#close-point-in-time-api
        """
        url = f"https://oersi.org/resources/api-internal/search/_pit"
        delete_request = requests.delete(url=url, json=self.ELASTIC_PIT_ID)
        logging.debug(f"Deleting ElasticSearch PIT: {self.ELASTIC_PIT_ID}")
        return delete_request.json()

    def elastic_query_provider_metadata(self, provider_name, search_after=None):
        """
        Queries OERSI's ElasticSearch API for a metadata from a specific provider.
        See: https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#paginate-search-results
        """
        url = "https://oersi.org/resources/api-internal/search/_search"
        if search_after is None:
            payload = {
                "size": self.ELASTIC_PARAMETER_REQUEST_SIZE,
                "query": {
                    "match": {"mainEntityOfPage.provider.name": f"{provider_name}"}
                },
                "pit": {
                    "id": self.ELASTIC_PIT_ID.get("id"),
                    "keep_alive": self.ELASTIC_PARAMETER_KEEP_ALIVE,
                },
                "sort": [{"id": "asc"}],
                "track_total_hits": f"true",
            }
        else:
            payload = {
                "size": self.ELASTIC_PARAMETER_REQUEST_SIZE,
                "query": {
                    "match": {"mainEntityOfPage.provider.name": f"{provider_name}"}
                },
                "pit": {
                    "id": self.ELASTIC_PIT_ID.get("id"),
                    "keep_alive": self.ELASTIC_PARAMETER_KEEP_ALIVE,
                },
                "sort": [{"id": "asc"}],
                "track_total_hits": f"true",
                "search_after": search_after,
            }
        headers = {"Content-Type": "application/json", "accept": "application/json"}
        response = requests.post(url=url, json=payload, headers=headers)
        # logging.debug(response.text)
        return response.json()

    def elastic_fetch_all_provider_pages(self):
        """
        Iterates through ElasticSearch result pages and collects each item within a list for further parsing. See:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#search-after
        """
        all_items: list = list()
        has_next_page = True
        for provider_name in self.ELASTIC_PROVIDERS_TO_CRAWL:
            pagination_parameter = None
            while has_next_page:
                current_page_json_response: dict = self.elastic_query_provider_metadata(
                    provider_name=provider_name, search_after=pagination_parameter
                )
                if "pit_id" in current_page_json_response:
                    if current_page_json_response.get(
                        "pit_id"
                    ) != self.ELASTIC_PIT_ID.get("id"):
                        self.ELASTIC_PIT_ID = current_page_json_response.get("pit_id")
                        logging.info(
                            f"ElasticSearch: pit_id changed between queries, using the new pit_id "
                            f"{current_page_json_response.get('pit_id')} for subsequent queries."
                        )
                if "hits" in current_page_json_response:
                    total_count = (
                        current_page_json_response.get("hits").get("total").get("value")
                    )
                    logging.info(f"Expecting {total_count} items for {provider_name}")
                if "hits" in current_page_json_response.get("hits"):
                    provider_items: list = current_page_json_response.get("hits").get(
                        "hits"
                    )
                    if provider_items:
                        logging.info(
                            f"The provider_items list has {len(provider_items)} entries"
                        )
                        all_items.extend(provider_items)
                        last_entry: dict = provider_items[-1]
                        # ToDo: pagination documentation
                        if "sort" in last_entry:
                            last_sort_result: list = last_entry.get("sort")
                            if last_sort_result:
                                logging.info(
                                    f"The last_sort_result is {last_sort_result}"
                                )
                                has_next_page = True
                                pagination_parameter = last_sort_result
                            else:
                                has_next_page = False
                                break
                    else:
                        logging.info(
                            f"reached the end of the ElasticSearch results for {provider_name} // "
                            f"Total amount of items collected: {len(all_items)}"
                        )
                        break
        return all_items

    def getId(self, response=None, elastic_item: dict = dict) -> str:
        """
        Uses OERSI's ElasticSearch "_id"-field to collect an uuid. See:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-id-field.html
        """
        return elastic_item["_id"]

    def getHash(self, response=None, elastic_item: dict = dict) -> str:
        """
        Creates a hash-value by combining a date + the crawler version number within a string.
        Since OERSI's date-fields are not always available, this method has several fallbacks:
        1) OERSI "datePublished"-field
        2) OERSI "dateCreated"-field
        3) if neither of the above are available: combine the current datetime + crawler version
        """
        date_published: str = elastic_item["_source"]["datePublished"]
        date_created: str = elastic_item["_source"]["dateCreated"]
        if date_published:
            hash_temp: str = f"{date_published}{self.version}"
        elif date_created:
            hash_temp: str = f"{date_created}{self.version}"
        else:
            hash_temp: str = f"{datetime.datetime.now().isoformat()}{self.version}"
        return hash_temp

    def hasChanged(self, response=None, elastic_item: dict = dict) -> bool:
        elastic_item = elastic_item
        if self.forceUpdate:
            return True
        if self.uuid:
            if self.getUUID(response) == self.uuid:
                logging.info(f"matching requested id: {self.uuid}")
                return True
            return False
        if self.remoteId:
            if str(self.getId(response, elastic_item=elastic_item)) == self.remoteId:
                logging.info(f"matching requested id: {self.remoteId}")
                return True
            return False
        db = EduSharing().findItem(
            self.getId(response, elastic_item=elastic_item), self
        )
        changed = db is None or db[1] != self.getHash(
            response, elastic_item=elastic_item
        )
        if not changed:
            logging.info(
                f"Item {self.getId(response, elastic_item=elastic_item)} (uuid: {db[0]}) has not changed"
            )
        return changed

    def get_lifecycle_author(
        self,
        lom_base_item_loader: LomBaseItemloader,
        elastic_item_source: dict,
        date_created: Optional[str] = None,
        date_published: Optional[str] = None,
    ):
        """
        If a "creator"-field is available in the OERSI API for a specific '_source'-item, creates an 'author'-specific
        LifecycleItemLoader and fills it up with available metadata.

        :param lom_base_item_loader: LomBaseItemLoader where the collected metadata should be saved to
        :param elastic_item_source: the '_source'-field of the currently parsed OERSI elastic item
        :param date_created: OERSI 'dateCreated' value (if available)
        :param date_published: OERSI 'datePublished' value (if available)
        :returns: list[str] - list of authors (names) for later usage in the LicenseItemLoader
        """
        authors: list[str] = list()
        if "creator" in elastic_item_source:
            creators: list[dict] = elastic_item_source.get("creator")
            # creator.honorificPrefix might appear in a future version of the API within a "creator"-array;
            # doesn't seem to be implemented in OERSI (yet)
            for creator_item in creators:
                lifecycle_author = LomLifecycleItemloader()
                if date_published:
                    lifecycle_author.add_value("date", date_published)
                elif date_created:
                    lifecycle_author.add_value("date", date_created)
                if "affiliation" in creator_item:
                    affiliation_item = creator_item.get("affiliation")
                    # ToDo: affiliation.type (e.g. Organization)
                    if "name" in affiliation_item:
                        affiliation_name = affiliation_item.get("name")
                        lifecycle_author.add_value("organization", affiliation_name)
                    if "id" in affiliation_item:
                        affiliation_url = affiliation_item.get("id")
                        lifecycle_author.add_value("url", affiliation_url)
                if creator_item.get("type") == "Person":
                    lifecycle_author.add_value(
                        "role", "author"
                    )  # supported roles: "author" / "editor" / "publisher"
                    author_name: str = creator_item.get("name")
                    authors.append(
                        author_name
                    )  # this string is going to be used in the license field "author"
                    self.split_names_if_possible_and_add_to_lifecycle(
                        name_string=author_name, lifecycle_item_loader=lifecycle_author
                    )
                    self.lifecycle_save_oersi_identifier_to_url_or_uuid(
                        person_dictionary=creator_item,
                        lifecycle_item_loader=lifecycle_author,
                    )
                    lom_base_item_loader.add_value(
                        "lifecycle", lifecycle_author.load_item()
                    )
                elif creator_item.get("type") == "Organization":
                    creator_organization_name = creator_item.get("name")
                    lifecycle_author.add_value("role", "author")
                    lifecycle_author.add_value(
                        "organization", creator_organization_name
                    )
                    lom_base_item_loader.add_value(
                        "lifecycle", lifecycle_author.load_item()
                    )
        return authors

    def get_lifecycle_contributor(
        self,
        lom_base_item_loader: LomBaseItemloader,
        elastic_item_source: dict,
        author_list: Optional[list[str]] = None,
    ):
        """
        Collects metadata from the OERSI "contributor"-field and stores it within a LomLifecycleItemLoader.
        """
        if "contributor" in elastic_item_source:
            contributors: list[dict] = elastic_item_source.get("contributor")
            # the OERSI field 'contributor' is OPTIONAL: https://dini-ag-kim.github.io/amb/draft/#contributor and might
            # contain several Persons or Organizations
            for contributor_item in contributors:
                lifecycle_contributor = LomLifecycleItemloader()
                lifecycle_contributor.add_value("role", "unknown")
                contributor_name: str = contributor_item.get("name")
                if contributor_name:
                    if author_list:
                        if contributor_name in author_list:
                            # OMA lists one author, but also lists the same person as a "contributor",
                            # therefore causing the same person to appear both as author and unknown contributor in
                            continue
                    # removing trailing whitespaces before further processing of the string
                    contributor_name = contributor_name.strip()
                if "type" in contributor_item:
                    if contributor_item.get("type") == "Person":
                        self.split_names_if_possible_and_add_to_lifecycle(
                            name_string=contributor_name,
                            lifecycle_item_loader=lifecycle_contributor,
                        )
                    elif contributor_item.get("type") == "Organization":
                        lifecycle_contributor.add_value(
                            "organization", contributor_name
                        )
                if "id" in contributor_item:
                    # id points to a URI reference of ORCID, GND, WikiData or ROR
                    # (while this isn't necessary for OMA items yet (as they have no 'id'-field), it will be necessary
                    # for other metadata providers once we extend the crawler)
                    self.lifecycle_save_oersi_identifier_to_url_or_uuid(
                        person_dictionary=contributor_item,
                        lifecycle_item_loader=lifecycle_contributor,
                    )
                if "affiliation" in contributor_item:
                    # ToDo: in future versions of the crawler, this field needs to be handled
                    # (the 'affiliation'-field currently ONLY appears in items from provider "ORCA.nrw")
                    #  - affiliation
                    #   - id
                    #   - name
                    #   - type
                    pass
                lom_base_item_loader.add_value(
                    "lifecycle", lifecycle_contributor.load_item()
                )

    @staticmethod
    def get_lifecycle_metadata_provider(
        lom_base_item_loader: LomBaseItemloader, oersi_main_entity_of_page_item: dict
    ):
        """
        Collects metadata from OERSI's "provider"-field and stores it within a LomLifecycleItemLoader.
        """
        # each provider-item has 3 fields:
        # - 'id'    (= URL of the Metadata provider, e.g. 'https://openmusic.academy')
        # - 'name'  (= human readable name, e.g. "Open Music Academy")
        # - 'type'  (= String 'Service' in 100% of cases)
        provider_dict: dict = oersi_main_entity_of_page_item.get("provider")
        if "name" in provider_dict:
            lifecycle_metadata_provider = LomLifecycleItemloader()
            lifecycle_metadata_provider.add_value("role", "metadata_provider")
            metadata_provider_name: str = oersi_main_entity_of_page_item.get(
                "provider"
            ).get("name")
            lifecycle_metadata_provider.add_value(
                "organization", metadata_provider_name
            )
            if "id" in provider_dict:
                # unique URL to the landing-page of the metadata, e.g.: "id"-value for a typical
                # 'Open Music Academy'-item looks like: "https://openmusic.academy/docs/26vG1SR17Zqf5LXpVLULqb"
                metadata_provider_url: str = oersi_main_entity_of_page_item.get(
                    "provider"
                ).get("id")
                lifecycle_metadata_provider.add_value("url", metadata_provider_url)
            lom_base_item_loader.add_value(
                "lifecycle", lifecycle_metadata_provider.load_item()
            )

    def get_lifecycle_publisher(
        self, lom_base_item_loader: LomBaseItemloader, elastic_item_source: dict
    ):
        """
        Collects metadata from OERSI's "publisher"-field and stores it within a LomLifecycleItemLoader.
        """
        if "publisher" in elastic_item_source:
            # see: https://dini-ag-kim.github.io/amb/draft/#publisher
            publisher_list: list[dict] = elastic_item_source.get("publisher")
            if publisher_list:
                for publisher_item in publisher_list:
                    lifecycle_publisher = LomLifecycleItemloader()
                    lifecycle_publisher.add_value("role", "publisher")
                    publisher_type: str = publisher_item.get("type")
                    publisher_name: str = publisher_item.get("name")
                    if publisher_type == "Organization":
                        lifecycle_publisher.add_value("organization", publisher_name)
                    elif publisher_type == "Person":
                        self.split_names_if_possible_and_add_to_lifecycle(
                            name_string=publisher_name,
                            lifecycle_item_loader=lifecycle_publisher,
                        )
                    if "id" in publisher_item:
                        publisher_url = publisher_item.get("id")
                        if publisher_url:
                            lifecycle_publisher.add_value("url", publisher_url)
                    lom_base_item_loader.add_value(
                        "lifecycle", lifecycle_publisher.load_item()
                    )

    @staticmethod
    def lifecycle_save_oersi_identifier_to_url_or_uuid(
        person_dictionary: dict, lifecycle_item_loader: LomLifecycleItemloader
    ):
        """
        OERSI's author 'id'-field delivers both URLs and uuids in the same field. Since edu-sharing expects URLs and
        uuids to be saved in separate fields, this method checks if the 'id'-field is available at all, and if it is,
        determines if the string should be saved to the 'url' or 'uuid'-field of LomLifecycleItemLoader.
        """
        if "id" in person_dictionary:
            author_uuid_or_url = person_dictionary.get("id")
            # ToDo: If this "lazy" approach yields messy results, RegEx differentiate between uuids and URLs
            if (
                "orcid.org" in author_uuid_or_url
                or "dnb.de" in author_uuid_or_url
                or "wikidata.org" in author_uuid_or_url
                or "ror.org" in author_uuid_or_url
            ):
                lifecycle_item_loader.add_value("url", author_uuid_or_url)
            else:
                lifecycle_item_loader.add_value("uuid", author_uuid_or_url)

    @staticmethod
    def split_names_if_possible_and_add_to_lifecycle(
        name_string: str, lifecycle_item_loader: LomLifecycleItemloader
    ):
        """
        Splits a string containing a person's name - if there's a whitespace within that string -
        into two parts: first_name and last_name.
        Afterwards saves the split-up values to their respective 'lifecycle'-fields or saves the string as a whole.
        """
        if " " in name_string:
            name_parts = name_string.split(maxsplit=1)
            first_name = name_parts[0]
            last_name = name_parts[1]
            lifecycle_item_loader.add_value("firstName", first_name)
            lifecycle_item_loader.add_value("lastName", last_name)
        else:
            lifecycle_item_loader.add_value("firstName", name_string)

    def parse(self, response: scrapy.http.Response, **kwargs):
        elastic_item: dict = kwargs.get("elastic_item")
        elastic_item_source: dict = elastic_item.get("_source")
        # _source is the original JSON body passed for the document at index time
        # see: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html
        if self.shouldImport(response) is False:
            logging.debug(
                "Skipping entry {} because shouldImport() returned false".format(
                    str(self.getId(response))
                )
            )
            return None
        if (
            self.getId(response=response, elastic_item=elastic_item) is not None
            and self.getHash(response=response, elastic_item=elastic_item) is not None
        ):
            if not self.hasChanged(response, elastic_item=elastic_item):
                return None

        # ToDo: look at these (sometimes available) properties later:
        #  - encoding (see: https://dini-ag-kim.github.io/amb/draft/#encoding - OPTIONAL field)

        # ToDo: The following keys DON'T EXIST (yet?) in the OERSI ElasticSearch API,
        #   but could appear in the future as possible metadata fields according to the AMB metadata draft:
        #  - affiliation            (OERSI uses their own 'sourceOrganization'-field instead)
        #  - assesses
        #  - audience               (might be suitable for "valuespaces.intendedEndUserRole")
        #  - conditionsOfAccess     (would be suitable for "valuespaces.conditionsOfAccess")
        #  - competencyRequired
        #  - duration               (for audio/video: will be suitable for "technical.location")
        #  - educationalLevel       (might be suitable for 'valuespaces.educationalContext')
        #  - hasPart
        #  - isBasedOn
        #  - isPartOf
        #  - teaches

        # noinspection DuplicatedCode
        base = BaseItemLoader()
        lom = LomBaseItemloader()
        general = LomGeneralItemloader()

        provider_name = str()
        if "mainEntityOfPage" in elastic_item_source:
            main_entity_of_page: list[dict] = elastic_item_source.get(
                "mainEntityOfPage"
            )
            if main_entity_of_page:
                if "provider" in main_entity_of_page[0]:
                    provider_name: str = (
                        main_entity_of_page[0].get("provider").get("name")
                    )
                    # the first provider_name is used for saving individual items to edu-sharing sub-folders
                    # via 'base.origin' later
                for maeop_item in main_entity_of_page:
                    # ToDo: according to the AMB spec, there could be a 'dateCreated'-field and 'dateModified'-field
                    #   appearing in the future. Regularly check the API if it was implemented (this could be used for
                    #   'lifecycle.date')
                    # a random sample showed that there can be multiple "mainEntityOfPage"-objects
                    # this only occurred once within 55438 items in the API, but might happen more often in the future
                    if "provider" in maeop_item:
                        self.get_lifecycle_metadata_provider(
                            lom_base_item_loader=lom,
                            oersi_main_entity_of_page_item=maeop_item,
                        )

        # if "about" in elastic_item_source:
        #     about = elastic_item_source.get("about")
        #     # about is OPTIONAL
        #     for about_item in about:
        #         # ToDo: disciplines are available as a list (according to the 'Hochschulfaechersystematik')
        #         #  - 'de'-field: human-readable German String
        #         #  - 'id'-field: URL of the entry (e.g. "https://w3id.org/kim/hochschulfaechersystematik/n78")
        #         pass
        #     # see: https://dini-ag-kim.github.io/amb/draft/#about
        #     # ToDo: DISCIPLINES!
        #     #  - prefLabel
        #     #   - de: German description (Schulfach / Studienfach)
        #     #   - en: English ...
        #     #   - uk: Ukrainian ...
        #     #   - etc. (depending on the provider, several more languages + descriptions are listed)
        #     #  - id

        date_created = str()
        if "dateCreated" in elastic_item_source:
            date_created: str = elastic_item_source.get("dateCreated")
        date_published = str()
        if "datePublished" in elastic_item_source:
            date_published: str = elastic_item_source.get("datePublished")

        base.add_value("sourceId", self.getId(response, elastic_item=elastic_item))
        base.add_value("hash", self.getHash(response, elastic_item=elastic_item))
        if "image" in elastic_item_source:
            thumbnail_url = elastic_item_source.get("image")  # thumbnail
            if thumbnail_url:
                base.add_value("thumbnail", thumbnail_url)
        if provider_name:
            # every item gets sorted into a /<provider_name>/-subfolder to make QA more feasable
            base.add_value("origin", provider_name)

        general.add_value("identifier", response.url)
        if "keywords" in elastic_item_source:
            keywords: list = elastic_item_source.get("keywords")
            if keywords:
                general.add_value("keyword", keywords)
        if "description" in elastic_item_source:
            description: str = elastic_item_source.get("description")
            general.add_value("description", description)
        title: str = elastic_item_source.get("name")
        general.add_value("title", title)

        in_languages = list()
        if "inLanguage" in elastic_item_source:
            in_languages: list[str] = elastic_item_source.get("inLanguage")
            # list of language codes, e.g. ["de", "en"]. (even if it's just a single language)
            if in_languages:
                for language_value in in_languages:
                    general.add_value("language", language_value)

        # noinspection DuplicatedCode
        lom.add_value("general", general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value(
            "format", "text/html"
        )  # e.g. if the learning object is a web-page
        if "id" in elastic_item_source:
            identifier_url: str = elastic_item_source.get(
                "id"
            )  # this URL REQUIRED and should always be available
            # see https://dini-ag-kim.github.io/amb/draft/#id
            if identifier_url:
                technical.add_value("location", identifier_url)
                # the identifier_url should be more stable/robust than the current response.url
                # navigated by the crawler
            else:
                technical.add_value("location", response.url)
        lom.add_value("technical", technical.load_item())

        authors = self.get_lifecycle_author(
            lom_base_item_loader=lom,
            elastic_item_source=elastic_item_source,
            date_created=date_created,
            date_published=date_published,
        )

        self.get_lifecycle_contributor(
            lom_base_item_loader=lom,
            elastic_item_source=elastic_item_source,
            author_list=authors,
        )

        self.get_lifecycle_publisher(
            lom_base_item_loader=lom, elastic_item_source=elastic_item_source
        )

        # ToDo: 'sourceOrganization' doesn't appear in OMA results, but will be available for other providers
        #   each item can have multiple 'soureOrganization' dictionaries attached to it, which typically look like
        # {
        #         "type": "Organization",
        #         "name": "Universität Innsbruck"
        #  }
        # if "sourceOrganization" in elastic_item_source:
        #     # attention: the "sourceOrganization"-field is not part of the AMB draft
        #     # see: https://github.com/dini-ag-kim/amb/issues/110
        #     # it is used by OERSI to express affiliation to an organization (instead of the AMB 'affiliation'-field)
        #     lifecycle_org = LomLifecycleItemloader()
        #     source_organizations: list = elastic_item_source.get('sourceOrganization')
        #     for source_org_item in source_organizations:
        #         if "id" in source_org_item:
        #             source_org_url = source_org_item.get('id')
        #             lifecycle_org.add_value('url', source_org_url)
        #         if "name" in source_org_item:
        #             source_org_name = source_org_item.get('name')
        #             lifecycle_org.add_value('organization', source_org_name)
        #         # source_org_type = source_org_item.get('type')  # e.g.: "Organization", "CollegeOrUniversity" etc.
        #     lom.add_value('lifecycle', lifecycle_org.load_item())

        educational = LomEducationalItemLoader()
        if in_languages:
            for language_value in in_languages:
                educational.add_value("language", language_value)
        # noinspection DuplicatedCode
        lom.add_value("educational", educational.load_item())

        classification = LomClassificationItemLoader()
        lom.add_value("classification", classification.load_item())

        base.add_value("lom", lom.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value("discipline", "420")  # Musik
        # ToDo: remove this hardcoded value in the future! (oersi_spider v0.0.1 is hardcoded for 'Open Music Academy')
        # ToDo: future versions of the crawler need to use 'Hochschulfaechersystematik'-values!
        vs.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)
        is_accessible_for_free: bool = elastic_item_source.get("isAccessibleForFree")
        if is_accessible_for_free:
            vs.add_value("price", "no")
        else:
            vs.add_value("price", "yes")

        hcrt_types = dict()
        oeh_lrt_types = dict()
        learning_resource_types = list()
        if "learningResourceType" in elastic_item_source:
            learning_resource_types: list[dict] = elastic_item_source.get(
                "learningResourceType"
            )
            # see: https://dini-ag-kim.github.io/amb/draft/#learningresourcetype - a typical LRT-dict looks like this:
            # 		{
            # 			"prefLabel": {
            # 				"nl": "Webpagina",
            # 				"fr": "Page Web",
            # 				"da": "Hjemmeside",
            # 				"de": "Webseite",
            # 				"en": "Web Page",
            # 				"es": "Página Web",
            # 				"fi": "Verkkosivu",
            # 				"uk": "Веб-сайт"
            # 			},
            # 			"id": "https://w3id.org/kim/hcrt/web_page"
            # 		}
        if learning_resource_types:
            # while the AMB specification allows vocabularies from either HCRT or OEH,
            # currently the OERSI API only serves HCRT LRTs
            for lrt_item in learning_resource_types:
                if "id" in lrt_item:
                    if "/hcrt/" in lrt_item.get("id"):
                        hcrt_type_url = lrt_item.get("id")
                        hcrt_type = lrt_item.get("prefLabel").get("en")
                        hcrt_types.update({hcrt_type: hcrt_type_url})
                    elif "/openeduhub/" in lrt_item.get("id"):
                        oeh_lrt_url = lrt_item.get("id")
                        oeh_lrt_type = lrt_item.get("prefLabel").get("en")
                        oeh_lrt_types.update({oeh_lrt_type: oeh_lrt_url})
        if hcrt_types:
            for hcrt_url in hcrt_types.values():
                # hcrt_urls will typically look like this: "https://w3id.org/kim/hcrt/drill_and_practice"
                hcrt_key: str = hcrt_url.split("/")[-1]
                if hcrt_key in self.MAPPING_HCRT_TO_NEW_LRT:
                    # some values in the HCRT Vocab don't exist in the (old) learningResourceType
                    # therefore they get mapped directly to a new_lrt
                    # ToDo: we are setting learningResourceType and new_lrt at the same time here!
                    #  - while Open Music Academy only uses a single LRT per item (100% of cases are "web_page")
                    #  - this might not be desired crawler behaviour in later versions of the crawler!
                    hcrt_key = self.MAPPING_HCRT_TO_NEW_LRT.get(hcrt_key)
                    vs.add_value("new_lrt", hcrt_key)
                else:
                    vs.add_value("learningResourceType", hcrt_key)
        if oeh_lrt_types:
            vs.add_value("learningResourceType", list(oeh_lrt_types.keys()))

        base.add_value("valuespaces", vs.load_item())

        license_loader = LicenseItemLoader()
        if "license" in elastic_item_source:
            license_url: str = elastic_item_source.get("license").get("id")
            if license_url:
                # ToDo: from some providers (e.g. twillo) license URLs end with "deed.de", confirm if licenses get
                #  properly recognized in edu-sharing
                license_loader.add_value("url", license_url)
        if authors:
            license_loader.add_value("author", authors)
        # noinspection DuplicatedCode
        base.add_value("license", license_loader.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader = ResponseItemLoader(response=response)
        # for future maintenance, during debugging the following problems occurred one day,
        # but disappeared the next day:
        #  - OMA URLs cause HTTP Error 400 in Splash
        response_loader.add_value("status", response.status)
        url_data = WebTools.getUrlData(
            url=response.url, engine=WebEngine.Playwright
        )
        if "html" in url_data:
            response_loader.add_value("html", url_data["html"])
        if "text" in url_data:
            response_loader.add_value("text", url_data["text"])
        if "cookies" in url_data:
            response_loader.add_value("cookies", url_data["cookies"])
        if "har" in url_data:
            response_loader.add_value("har", url_data["har"])
        if "screenshot_bytes" in url_data:
            # ToDo: optional thumbnail feature (toggleable via a list?)
            # -> OMA serves generic thumbnails, which is why a screenshot of the
            #  website will always be more interesting to users than the same generic image across ~650 materials
            base.add_value("screenshot_bytes", url_data["screenshot_bytes"])
        response_loader.add_value("headers", response.headers)
        response_loader.add_value("url", response.url)
        base.add_value("response", response_loader.load_item())

        yield base.load_item()
