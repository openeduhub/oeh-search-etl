import datetime
import logging
import random
from typing import Optional

import requests
import scrapy

from converter import env
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
from converter.util.license_mapper import LicenseMapper
from converter.web_tools import WebEngine


class OersiSpider(scrapy.Spider, LomBase):
    """
    Crawls OERSI.org for metadata from different OER providers.

    You can control which metadata provider should be crawled by commenting/uncommenting their name within the
    ELASTIC_PROVIDERS_TO_CRAWL list. Alternatively, you can set the optional '.env'-variable 'OERSI_METADATA_PROVIDER'
    to control which provider should be crawled individually.
    """

    name = "oersi_spider"
    # start_urls = ["https://oersi.org/"]
    friendlyName = "OERSI"
    version = "0.1.8"  # last update: 2023-12-20
    allowed_domains = "oersi.org"
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 60,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 6,
        "DUPEFILTER_DEBUG": True,
        "WEB_TOOLS": WebEngine.Playwright,
        "ROBOTSTXT_OBEY": False,
    }
    # if robots.txt is obeyed, the thumbnail downloads fail on some metadata-providers (e.g., DuEPublico)

    ELASTIC_PARAMETER_KEEP_ALIVE: str = "1m"
    # for reference: https://www.elastic.co/guide/en/elasticsearch/reference/current/api-conventions.html#time-units
    ELASTIC_PARAMETER_REQUEST_SIZE: int = (
        5000  # maximum: 10.000, but responses for bigger request sizes take significantly longer
    )

    ELASTIC_PIT_ID: dict = dict()
    # the provider-filter at https://oersi.org/resources/ shows you which String values can be used as a provider-name
    # ToDo: regularly check if new providers need to be added to the list below (and insert/sort them alphabetically!)
    ELASTIC_PROVIDERS_TO_CRAWL: list = [
        "BC Campus",  # BC Campus website cannot be crawled at the moment, needs further investigation
        # "ComeIn",  # should not be crawled, datasets were exported to OERSI from WLO
        "detmoldMusicTools",
        "digiLL",
        "DuEPublico",
        "eaDNURT",
        "eCampusOntario",
        "eGov-Campus",
        "Finnish Library of Open Educational Resources",  # URLs of this metadata-provider cannot be resolved
        "GitHub",
        "GitLab",
        "Helmholtz Codebase",
        "HessenHub",
        "HHU Mediathek",
        "HOOU",
        "iMoox",
        "KI Campus",
        "langSci Press",  # new provider as of 2023-04-27
        "lecture2go (Hamburg)",  # new provider as of 2023-12-14
        "MIT OpenCourseWare",
        # "OEPMS",  # new provider as of 2023-04-27 # ToDo: cannot be crawled
        "OER Portal Uni Graz",
        "oncampus",  # (temporarily) not available? (2023-12-14)
        "Open Music Academy",
        "Open Textbook Library",
        "Opencast Universität Osnabrück",
        "openHPI",
        "OpenLearnWare",
        "OpenRub",
        "ORCA.nrw",
        "Phaidra Uni Wien",
        "Pressbooks Directory",  # new provider as of 2023-12-14
        "RWTH Aachen GitLab",
        "TIB AV-Portal",
        "TU Delft OpenCourseWare",
        "twillo",
        "Universität Innsbruck OER Repositorium",
        "VCRP",
        "vhb",
        "Virtual Linguistics Campus",
        "ZOERR",
    ]
    ELASTIC_ITEMS_ALL = list()

    MAPPING_HCRT_TO_NEW_LRT = {
        "diagram": "f7228fb5-105d-4313-afea-66dd59b1b6f8",  # "Graph, Diagramm und Charts"
        "portal": "d8c3ef03-b3ab-4a5e-bcc9-5a546fefa2e9",  # "Webseite und Portal (stabil)"
        "questionnaire": "d31a5b68-611f-4015-8be9-56bd5eb44c64",  # "Fragebogen und Umfragen"
        "script": "6a15628c-0e59-43e3-9fc5-9a7f7fa261c4",  # "Skript, Handout und Handreichung"
        "sheet_music": "f7e92628-4132-4985-bcf5-93c285e300a8",  # "Noten"
        "textbook": "a5897142-bf57-4cd0-bcd9-7d0f1932e87a",  # "Lehrbuch und Grundlagenwerk (auch E-Book)"
    }
    MAPPING_AUDIENCE_TO_INTENDED_END_USER_ROLE = {
        # Mapping from https://www.dublincore.org/vocabs/educationalAudienceRole.ttl
        # to https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/intendedEndUserRole.ttl
        "administrator": "manager",
        # "generalPublic": "",  # ToDo: find mapping
        "mentor": "counsellor",
        # "peerTutor": "",  # ToDo: find mapping
        # "professional": "",  # ToDo: find mapping
    }

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)
        # Fetching a "point in time"-id for the subsequent ElasticSearch queries
        self.ELASTIC_PIT_ID = self.elastic_pit_get_id(self.elastic_pit_create())
        # querying the ElasticSearch API for metadata-sets of specific providers, this allows us to control which
        # providers we want to include/exclude by using the "ELASTIC_PROVIDERS_TO_CRAWL"-list
        self.ELASTIC_ITEMS_ALL = self.elastic_fetch_all_provider_pages()
        # after all items have been collected, delete the ElasticSearch PIT
        json_response = self.elastic_pit_delete()
        if json_response:
            logging.info(f"ElasticSearch API response (upon PIT delete): {json_response}")

    def start_requests(self):
        # yield dummy request, so that Scrapy's start_item method requirement is satisfied,
        # then use callback method to crawl all items
        yield scrapy.Request(url="https://oersi.org", callback=self.handle_collected_elastic_items)

    def handle_collected_elastic_items(self, response: scrapy.http.Response):
        random.shuffle(self.ELASTIC_ITEMS_ALL)  # shuffling the list of ElasticSearch items to improve concurrency and
        # distribute the load between several target domains.
        for elastic_item in self.ELASTIC_ITEMS_ALL:
            yield from self.check_item_and_yield_to_parse_method(elastic_item)

    def check_item_and_yield_to_parse_method(self, elastic_item: dict) -> scrapy.Request | None:
        """
        Checks if the item already exists in the edu-sharing repository and yields a Request to the parse()-method.
        If the item already exists, it will be updated (if its hash has changed).
        Otherwise, creates a new item in the edu-sharing repository.
        """
        item_url: str = self.get_item_url(elastic_item)
        if item_url:
            if self.shouldImport(response=None) is False:
                logging.debug(
                    "Skipping entry {} because shouldImport() returned false".format(
                        str(self.getId(response=None, elastic_item=elastic_item))
                    )
                )
                return None
            if (
                self.getId(response=None, elastic_item=elastic_item) is not None
                and self.getHash(response=None, elastic_item_source=elastic_item["_source"]) is not None
            ):
                if not self.hasChanged(None, elastic_item=elastic_item):
                    return None
            # ToDo: implement crawling mode toggle?
            #  (online) crawl vs. "offline"-import (without making requests to the item urls)
            # by omitting the callback parameter, individual requests are yielded to the parse-method
            # yield scrapy.Request(url=item_url, cb_kwargs={"elastic_item": elastic_item}, dont_filter=True)
            yield from self.parse(elastic_item=elastic_item)

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
                "query": {"match": {"mainEntityOfPage.provider.name": f"{provider_name}"}},
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
                "query": {"match": {"mainEntityOfPage.provider.name": f"{provider_name}"}},
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
        # the OERSI_METADATA_PROVIDER '.env'-variable controls which metadata-provider should be crawled:
        # e.g. set: OERSI_METADATA_PROVIDER="eGov-Campus" within your .env file if you only want to crawl items from
        # 'eGov-Campus'. Since this string is used within ElasticSearch queries as a parameter, it needs to be
        # 1:1 identical to the metadata-provider string values on OERSI.org.
        provider_target_from_env: str = env.get(key="OERSI_METADATA_PROVIDER", allow_null=True, default=None)
        if provider_target_from_env:
            logging.info(f"Recognized OERSI_METADATA_PROVIDER .env setting. Value: {provider_target_from_env}")
            self.ELASTIC_PROVIDERS_TO_CRAWL = [provider_target_from_env]
            if ";" in provider_target_from_env:
                provider_list: list[str] = provider_target_from_env.split(";")
                logging.info(
                    f"Recognized multiple providers within OERSI_METADATA_PROVIDER .env setting:" f"{provider_list}"
                )
                self.ELASTIC_PROVIDERS_TO_CRAWL = provider_list

        has_next_page = True
        for provider_name in self.ELASTIC_PROVIDERS_TO_CRAWL:
            pagination_parameter = None
            while has_next_page:
                current_page_json_response: dict = self.elastic_query_provider_metadata(
                    provider_name=provider_name, search_after=pagination_parameter
                )
                if "pit_id" in current_page_json_response:
                    if current_page_json_response.get("pit_id") != self.ELASTIC_PIT_ID.get("id"):
                        self.ELASTIC_PIT_ID = current_page_json_response.get("pit_id")
                        logging.info(
                            f"ElasticSearch: pit_id changed between queries, using the new pit_id "
                            f"{current_page_json_response.get('pit_id')} for subsequent queries."
                        )
                if "hits" in current_page_json_response:
                    total_count = current_page_json_response.get("hits").get("total").get("value")
                    logging.debug(f"Expecting {total_count} items for the current API Pagination of {provider_name}")
                if "hits" in current_page_json_response.get("hits"):
                    provider_items: list = current_page_json_response.get("hits").get("hits")
                    if provider_items:
                        logging.debug(f"The provider_items list has {len(provider_items)} entries")
                        all_items.extend(provider_items)
                        last_entry: dict = provider_items[-1]
                        # ToDo: pagination documentation
                        if "sort" in last_entry:
                            last_sort_result: list = last_entry.get("sort")
                            if last_sort_result:
                                has_next_page = True
                                pagination_parameter = last_sort_result
                            else:
                                has_next_page = False
                                break
                    else:
                        logging.info(
                            f"Reached the end of the ElasticSearch results for '{provider_name}' // "
                            f"Total amount of items collected (across all metadata-providers): {len(all_items)}"
                        )
                        break
        return all_items

    def getId(self, response=None, elastic_item: dict = dict) -> str:
        """
        Uses OERSI's ElasticSearch "_id"-field to collect an uuid. See:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-id-field.html
        """
        return elastic_item["_id"]

    def getHash(self, response=None, elastic_item_source: dict = dict) -> str:
        """
        Creates a hash-value by combining a date + the crawler version number within a string.
        Since OERSI's date-fields are not always available, this method has several fallbacks:
        1) OERSI "datePublished"-field
        2) OERSI "dateCreated"-field
        3) if neither of the above are available: combine the current datetime + crawler version
        """
        date_published = str()
        date_created = str()
        if "datePublished" in elastic_item_source:
            date_published: str = elastic_item_source["datePublished"]
        if "dateCreated" in elastic_item_source:
            date_created: str = elastic_item_source["dateCreated"]
        if date_published:
            hash_temp: str = f"{date_published}{self.version}"
        elif date_created:
            hash_temp: str = f"{date_created}{self.version}"
        else:
            hash_temp: str = f"{datetime.datetime.now().isoformat()}{self.version}"
        return hash_temp

    @staticmethod
    def get_uuid(elastic_item: dict):
        """
        Builds a UUID string from the to-be-parsed target URL and returns it.
        """
        # The "getUUID"-method of LomBase couldn't be cleanly overridden because at the point of time when we do this
        # check, there is no "Response"-object available yet.
        item_url = OersiSpider.get_item_url(elastic_item=elastic_item)
        return EduSharing.build_uuid(item_url)

    @staticmethod
    def get_item_url(elastic_item: dict) -> str | None:
        """
        Retrieves the to-be-parsed URL from OERSI's '_source.id'-field.
        If that (REQUIRED) field was not available, returns None.
        """
        item_url: str = elastic_item["_source"]["id"]
        if item_url:
            return item_url
        else:
            logging.warning(f"OERSI Item {elastic_item['_id']} did not provide a URL string. Dropping item.")
            return None

    def hasChanged(self, response=None, elastic_item: dict = dict) -> bool:
        elastic_item = elastic_item
        if self.forceUpdate:
            return True
        if self.uuid:
            if self.get_uuid(elastic_item=elastic_item) == self.uuid:
                logging.info(f"matching requested id: {self.uuid}")
                return True
            return False
        if self.remoteId:
            if str(self.getId(response, elastic_item=elastic_item)) == self.remoteId:
                logging.info(f"matching requested id: {self.remoteId}")
                return True
            return False
        db = EduSharing().find_item(self.getId(response, elastic_item=elastic_item), self)
        changed = db is None or db[1] != self.getHash(response, elastic_item_source=elastic_item["_source"])
        if not changed:
            logging.info(f"Item {self.getId(response, elastic_item=elastic_item)} (uuid: {db[0]}) has not changed")
        return changed

    def get_lifecycle_author(
        self,
        lom_base_item_loader: LomBaseItemloader,
        elastic_item_source: dict,
        organization_fallback: set[str],
        date_created: Optional[str] = None,
        date_published: Optional[str] = None,
    ):
        """
        If a "creator"-field is available in the OERSI API for a specific '_source'-item, creates an 'author'-specific
        LifecycleItemLoader and fills it up with available metadata.

        :param lom_base_item_loader: LomBaseItemLoader where the collected metadata should be saved to
        :param elastic_item_source: the '_source'-field of the currently parsed OERSI elastic item
        :param organization_fallback: a temporary set of strings containing all affiliation 'name'-values
        :param date_created: OERSI 'dateCreated' value (if available)
        :param date_published: OERSI 'datePublished' value (if available)
        :returns: list[str] - list of authors (author names will be used for "contributor"-duplicate-mitigation)
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
                if creator_item.get("type") == "Person":
                    lifecycle_author.add_value("role", "author")
                    author_name: str = creator_item.get("name")
                    academic_title: str = str()
                    if "honorificPrefix" in creator_item:
                        # the 'honorificPrefix'-field is described in the 'creator'-json-scheme:
                        # https://dini-ag-kim.github.io/amb/draft/schemas/creator.json
                        honorific_prefix = creator_item["honorificPrefix"]
                        if honorific_prefix:
                            academic_title = self.validate_academic_title_string(honorific_prefix)
                            if academic_title:
                                lifecycle_author.add_value("title", academic_title)
                                author_name_prefixed_with_academic_title = f"{academic_title} {author_name}"
                                authors.append(author_name_prefixed_with_academic_title)
                    if not academic_title:
                        authors.append(author_name)  # this string is going to be used in the license field "author"
                    self.split_names_if_possible_and_add_to_lifecycle(
                        name_string=author_name, lifecycle_item_loader=lifecycle_author
                    )
                    self.lifecycle_determine_type_of_identifier_and_save_uri(
                        item_dictionary=creator_item,
                        lifecycle_item_loader=lifecycle_author,
                    )
                    lom_base_item_loader.add_value("lifecycle", lifecycle_author.load_item())
                elif creator_item.get("type") == "Organization":
                    creator_organization_name = creator_item.get("name")
                    organization_fallback.add(creator_organization_name)
                    lifecycle_author.add_value("role", "author")
                    lifecycle_author.add_value("organization", creator_organization_name)
                    self.lifecycle_determine_type_of_identifier_and_save_uri(
                        item_dictionary=creator_item, lifecycle_item_loader=lifecycle_author
                    )
                    lom_base_item_loader.add_value("lifecycle", lifecycle_author.load_item())
                if "affiliation" in creator_item:
                    affiliation_item = creator_item.get("affiliation")
                    self.get_affiliation_and_save_to_lifecycle(
                        affiliation_dict=affiliation_item,
                        lom_base_item_loader=lom_base_item_loader,
                        organization_fallback=organization_fallback,
                        lifecycle_role="author",
                    )
        return authors

    def get_affiliation_and_save_to_lifecycle(
        self,
        affiliation_dict: dict,
        lom_base_item_loader: LomBaseItemloader,
        organization_fallback: set[str],
        lifecycle_role: str,
    ):
        """
        Retrieves metadata from OERSI's "affiliation"-field (which is typically found within a "creator"- or
        "contributor"-item) and tries to save it within a new LOM Lifecycle Item.

        See: https://dini-ag-kim.github.io/amb/draft/#affiliation
        """
        # affiliation.type is always "Organization" according to
        # see: https://dini-ag-kim.github.io/amb/draft/schemas/affiliation.json // example dict:
        # [
        # 		{
        # 			"affiliation": {
        # 				"name": "RWTH Aachen",
        # 				"id": "https://ror.org/04xfq0f34",
        # 				"type": "Organization"
        # 			},
        # 			"name": "OMB+-Konsortium",
        # 			"type": "Organization"
        # 		}
        # 	],
        # the vCard standard 4.0 provides a "RELATED"-property which could be suitable for this edge-case,
        # but both edu-sharing and the currently used "vobject"-package only support vCard standard v3.0
        # (for future reference:
        # vCard v3: https://datatracker.ietf.org/doc/html/rfc2426
        # vCard v4: https://www.rfc-editor.org/rfc/rfc6350.html#section-6.6.6 )
        if "name" in affiliation_dict:
            affiliation_name = affiliation_dict.get("name")
            lifecycle_affiliated_org = LomLifecycleItemloader()
            if affiliation_name:
                if affiliation_name not in organization_fallback:
                    # checking to make sure we don't add the same organization several times to the same role
                    # (e.g. 5 different authors could be affiliated to the same university, but we most definitely don't
                    # want to have the organization entry 5 times)
                    lifecycle_affiliated_org.add_value("role", lifecycle_role)
                    lifecycle_affiliated_org.add_value("organization", affiliation_name)
                    organization_fallback.add(affiliation_name)
                if "id" in affiliation_dict:
                    # according to the AMB spec, the affiliation.id is OPTIONAL, but should always be a
                    # reference to GND, Wikidata or ROR
                    self.lifecycle_determine_type_of_identifier_and_save_uri(
                        affiliation_dict, lifecycle_item_loader=lifecycle_affiliated_org
                    )
                lom_base_item_loader.add_value("lifecycle", lifecycle_affiliated_org.load_item())

    @staticmethod
    def validate_academic_title_string(honorific_prefix: str) -> str:
        """
        Some metadata-providers provide weird values for the 'honorificPrefix'-attribute within a "creator"- or
        "contributor"-item. This method checks for known edge-cases and drops the string if necessary.
        See: https://dini-ag-kim.github.io/amb/draft/#dfn-creator
        Check for truthiness after using this method! If a known edge-case was detected, it will return an empty string.
        """
        # Typical edge-cases for the 'honorificPrefix'-field that have been noticed so far:
        #   ORCA.nrw: "http://hbz-nrw.de/regal#academicDegree/unkown", "unknown",
        #   Open Textbook Library: single backticks
        if "unknown" in honorific_prefix or "unkown" in honorific_prefix or len(honorific_prefix) == 1:
            logging.debug(
                f"'honorificPrefix'-validation: The string {honorific_prefix} was recognized as an invalid "
                f"edge-case value. Deleting string..."
            )
            honorific_prefix = ""
        return honorific_prefix.strip()

    def get_lifecycle_contributor(
        self,
        lom_base_item_loader: LomBaseItemloader,
        elastic_item_source: dict,
        organization_fallback: set[str],
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
                    if "honorificPrefix" in contributor_item:
                        honorific_prefix: str = contributor_item["honorificPrefix"]
                        if honorific_prefix:
                            academic_title: str = self.validate_academic_title_string(honorific_prefix)
                            if academic_title:
                                lifecycle_contributor.add_value("title", academic_title)
                                # contributor_name_prefixed_with_academic_title = f"{academic_title} {contributor_name}"
                    if author_list:
                        for author_string in author_list:
                            if contributor_name in author_string:
                                # OMA lists one author, but also lists the same person as a "contributor",
                                # therefore causing the same person to appear both as author and unknown contributor
                                continue
                    contributor_name = contributor_name.strip()
                    # removing trailing whitespaces before further processing of the string
                if "type" in contributor_item:
                    if contributor_item.get("type") == "Person":
                        self.split_names_if_possible_and_add_to_lifecycle(
                            name_string=contributor_name,
                            lifecycle_item_loader=lifecycle_contributor,
                        )
                    elif contributor_item.get("type") == "Organization":
                        lifecycle_contributor.add_value("organization", contributor_name)
                        organization_fallback.add(contributor_name)
                if "id" in contributor_item:
                    # id points to a URI reference of ORCID, GND, WikiData or ROR
                    # (while this isn't necessary for OMA items yet (as they have no 'id'-field), it will be necessary
                    # for other metadata providers once we extend the crawler)
                    self.lifecycle_determine_type_of_identifier_and_save_uri(
                        item_dictionary=contributor_item,
                        lifecycle_item_loader=lifecycle_contributor,
                    )
                if "affiliation" in contributor_item:
                    # the 'affiliation'-field currently ONLY appears in items from provider "ORCA.nrw"
                    # the 'affiliation.type' is always 'Organization'
                    affiliation_dict: dict = contributor_item["affiliation"]
                    # if the dictionary exists, it might contain the following fields:
                    #   - id        (= URL to GND / ROR / Wikidata)
                    #   - name      (= string containing the name of the affiliated organization)
                    self.get_affiliation_and_save_to_lifecycle(
                        affiliation_dict=affiliation_dict,
                        lom_base_item_loader=lom_base_item_loader,
                        organization_fallback=organization_fallback,
                        lifecycle_role="unknown",
                    )
                lom_base_item_loader.add_value("lifecycle", lifecycle_contributor.load_item())

    @staticmethod
    def get_lifecycle_metadata_provider(lom_base_item_loader: LomBaseItemloader, oersi_main_entity_of_page_item: dict):
        """
        Collects metadata from OERSI's "provider"-field and stores it within a LomLifecycleItemLoader.
        """
        # mainEntityofPage structure -> 'id' is the only REQUIRED field, all other fields are OPTIONAL:
        # 'id'              (= URL of the Metadata Landing Page)
        # 'dateCreated'     (= creation date of the metadata)
        # 'dateModified'    (= last modified date of the metadata)
        # 'provider':
        #   - 'id'            (= URL of the Metadata provider, e.g. 'https://openmusic.academy')
        #   - 'name'          (= human readable name, e.g. "Open Music Academy")
        #   - 'type'          (= String 'Service' in 100% of cases)
        provider_dict: dict = oersi_main_entity_of_page_item.get("provider")
        if "name" in provider_dict:
            lifecycle_metadata_provider = LomLifecycleItemloader()
            lifecycle_metadata_provider.add_value("role", "metadata_provider")
            metadata_provider_name: str = provider_dict.get("name")
            lifecycle_metadata_provider.add_value("organization", metadata_provider_name)
            if "id" in oersi_main_entity_of_page_item:
                # unique URL to the landing-page of the metadata, e.g.: "id"-value for a typical
                # 'Open Music Academy'-item looks like: "https://openmusic.academy/docs/26vG1SR17Zqf5LXpVLULqb"
                maeop_id_url: str = oersi_main_entity_of_page_item["id"]
                if maeop_id_url:
                    lifecycle_metadata_provider.add_value("url", maeop_id_url)
            if "dateCreated" in oersi_main_entity_of_page_item:
                maeop_date_created: str = oersi_main_entity_of_page_item["dateCreated"]
                if maeop_date_created:
                    lifecycle_metadata_provider.add_value("date", maeop_date_created)
            elif "dateModified" in oersi_main_entity_of_page_item:
                # if no creation date of the metadata is available, we use dateModified as a fallback (if available)
                maeop_date_modified: str = oersi_main_entity_of_page_item["dateModified"]
                if maeop_date_modified:
                    lifecycle_metadata_provider.add_value("date", maeop_date_modified)
            if "id" in provider_dict:
                # the 'provider.id' URL will always point to a more generic URL
                metadata_provider_url: str = oersi_main_entity_of_page_item.get("provider").get("id")
                lifecycle_metadata_provider.add_value("url", metadata_provider_url)
            lom_base_item_loader.add_value("lifecycle", lifecycle_metadata_provider.load_item())

    def get_lifecycle_publisher(
        self,
        lom_base_item_loader: LomBaseItemloader,
        elastic_item_source: dict,
        organizations_from_publisher_fields: set[str],
        date_published: Optional[str] = None,
    ):
        """
        Collects metadata from OERSI's "publisher"-field and stores it within a LomLifecycleItemLoader. Successfully
        collected 'publisher.name'-strings are added to an organizations set for duplicate detection in the
        'sourceOrganization' field.
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
                        # to avoid duplicate entries in 'publisher'-lifecycle items, we need to keep a set of previously
                        # collected publisher names to compare them later in the 'sourceOrganization'-method for the
                        # WLO-BIRD-Connector v2
                        organizations_from_publisher_fields.add(publisher_name)
                    elif publisher_type == "Person":
                        self.split_names_if_possible_and_add_to_lifecycle(
                            name_string=publisher_name,
                            lifecycle_item_loader=lifecycle_publisher,
                        )
                    if "id" in publisher_item:
                        publisher_url = publisher_item.get("id")
                        if publisher_url:
                            lifecycle_publisher.add_value("url", publisher_url)
                    if date_published:
                        lifecycle_publisher.add_value("date", date_published)
                    lom_base_item_loader.add_value("lifecycle", lifecycle_publisher.load_item())

    def get_lifecycle_organization_from_source_organization_fallback(
        self, elastic_item_source: dict, lom_item_loader: LomBaseItemloader, organization_fallback: set[str]
    ):
        # ATTENTION: the "sourceOrganization"-field is not part of the AMB draft, therefore this method is currently
        # used a fallback, so we don't lose any useful metadata (even if that metadata is not part of the AMB spec).
        # see: https://github.com/dini-ag-kim/amb/issues/110
        # 'sourceOrganization' is an OERSI-specific (undocumented) field: it is used by OERSI to express an affiliation
        # to an organization (which is normally covered by the AMB 'affiliation'-field).
        # it appears to be implemented in two distinct ways:
        #  1) For metadata providers which use the "affiliation"-field within "creator" or "contributor", the
        #   'sourceOrganization'-field does not contain any useful (additional) data. It's basically a set of all
        #   "affiliation"-values (without any duplicate entries). -> In this case we SKIP it completely!
        #  2) For metadata-providers which DON'T provide any "affiliation"-values, the 'sourceOrganization'-field will
        #   contain metadata about organizations without being attached to a person. (Therefore it can only be
        #   interpreted as lifecycle role 'unknown' (= contributor in unknown capacity).
        # ToDo: periodically confirm if this fallback is still necessary (check the OERSI API / AMB spec!)
        source_organizations: list = elastic_item_source.get("sourceOrganization")
        for source_org_item in source_organizations:
            if "name" in source_org_item:
                source_org_name = source_org_item.get("name")
                if source_org_name in organization_fallback:
                    # if the 'sourceOrganization' name is already in our organization list, skip this loop
                    continue
                lifecycle_org = LomLifecycleItemloader()
                lifecycle_org.add_value("role", "unknown")
                lifecycle_org.add_value("organization", source_org_name)
                if "id" in source_org_item:
                    # the "id"-field is used completely different between metadata-providers:
                    # for some providers ("HOOU") it contains just the URL to their website (= not a real identifier),
                    # but other metadata-providers provide an actual identifier (e.g. to ror.org) within this field.
                    # Therefore, we're checking which type of URI it is first before saving it to a specific field
                    self.lifecycle_determine_type_of_identifier_and_save_uri(
                        item_dictionary=source_org_item, lifecycle_item_loader=lifecycle_org
                    )
                # ToDo: sometimes there are more possible fields within a 'sourceOrganization', e.g.:
                #  - image  (-> ?)
                #  - logo   (-> ?)
                if "url" in source_org_item:
                    org_url: str = source_org_item.get("url")
                    lifecycle_org.add_value("url", org_url)
                lom_item_loader.add_value("lifecycle", lifecycle_org.load_item())

    def get_lifecycle_publisher_from_source_organization(
        self, lom_item_loader: LomBaseItemloader, elastic_item_source: dict, previously_collected_publishers: set[str]
    ):
        source_organizations: list[dict] = elastic_item_source.get("sourceOrganization")
        for so in source_organizations:
            if "name" in so:
                source_org_name: str = so.get("name")
                if source_org_name not in previously_collected_publishers:
                    lifecycle_org = LomLifecycleItemloader()
                    lifecycle_org.add_value("role", "publisher")
                    lifecycle_org.add_value("organization", source_org_name)
                    if "id" in so:
                        self.lifecycle_determine_type_of_identifier_and_save_uri(
                            item_dictionary=so, lifecycle_item_loader=lifecycle_org
                        )
                    if "url" in so:
                        org_url: str = so.get("url")
                        if org_url:
                            lifecycle_org.add_value("url", org_url)
                    lom_item_loader.add_value("lifecycle", lifecycle_org.load_item())

    @staticmethod
    def lifecycle_determine_type_of_identifier_and_save_uri(
        item_dictionary: dict, lifecycle_item_loader: LomLifecycleItemloader
    ):
        """
        OERSI's "creator"/"contributor"/"affiliation" items might contain an 'id'-field which (optionally) provides
        URI-identifiers that reference GND / ORCID / Wikidata / ROR.
        This method checks if the 'id'-field is available at all, and if it is, determines if the string should be
        saved to an identifier-specific field of LomLifecycleItemLoader.
        If the URI string of "id" could not be recognized, it will save the value to 'lifecycle.url' as a fallback.
        """
        if "id" in item_dictionary:
            uri_string: str = item_dictionary.get("id")
            if (
                "orcid.org" in uri_string
                or "/gnd/" in uri_string
                or "wikidata.org" in uri_string
                or "ror.org" in uri_string
            ):
                if "/gnd/" in uri_string:
                    lifecycle_item_loader.add_value("id_gnd", uri_string)
                if "orcid.org" in uri_string:
                    lifecycle_item_loader.add_value("id_orcid", uri_string)
                if "ror.org" in uri_string:
                    lifecycle_item_loader.add_value("id_ror", uri_string)
                if "wikidata.org" in uri_string:
                    lifecycle_item_loader.add_value("id_wikidata", uri_string)
            else:
                logging.info(
                    f"The URI identifier '{uri_string}' was not recognized. "
                    f"Fallback: Saving its value to 'lifecycle.url'."
                )
                # lifecycle_item_loader.add_value("url", uri_string)

    @staticmethod
    def split_names_if_possible_and_add_to_lifecycle(name_string: str, lifecycle_item_loader: LomLifecycleItemloader):
        """
        Splits a string containing a person's name - if there's a whitespace within that string -
        into two parts: first_name and last_name.
        Afterward saves the split values to their respective 'lifecycle'-fields or saves the string as a whole.
        """
        if " " in name_string:
            # clean up empty / erroneous whitespace-only strings before trying to split the string
            name_string = name_string.strip()
        if " " in name_string:
            name_parts = name_string.split(maxsplit=1)
            first_name = name_parts[0]
            last_name = name_parts[1]
            lifecycle_item_loader.add_value("firstName", first_name)
            lifecycle_item_loader.add_value("lastName", last_name)
        elif name_string:
            lifecycle_item_loader.add_value("firstName", name_string)

    def parse(self, response=None, **kwargs):
        elastic_item: dict = kwargs.get("elastic_item")
        elastic_item_source: dict = elastic_item.get("_source")
        # _source is the original JSON body passed for the document at index time
        # see: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html

        # ToDo: look at these (sometimes available) properties later:
        #  - encoding (see: https://dini-ag-kim.github.io/amb/draft/#encoding - OPTIONAL field)

        # ToDo: The following keys DON'T EXIST (yet?) in the OERSI ElasticSearch API,
        #   but could appear in the future as possible metadata fields according to the AMB metadata draft:
        #  - assesses
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
            main_entity_of_page: list[dict] = elastic_item_source.get("mainEntityOfPage")
            if main_entity_of_page:
                if "provider" in main_entity_of_page[0]:
                    provider_name: str = main_entity_of_page[0].get("provider").get("name")
                    # the first provider_name is used for saving individual items to edu-sharing sub-folders
                    # via 'base.origin' later
                for maeop_item in main_entity_of_page:
                    # a random sample showed that there can be multiple "mainEntityOfPage"-objects
                    # this only occurred once within 55438 items in the API, but might happen more often in the future
                    if "provider" in maeop_item:
                        self.get_lifecycle_metadata_provider(
                            lom_base_item_loader=lom,
                            oersi_main_entity_of_page_item=maeop_item,
                        )

        date_created = str()
        if "dateCreated" in elastic_item_source:
            date_created: str = elastic_item_source.get("dateCreated")
        date_published = str()
        if "datePublished" in elastic_item_source:
            date_published: str = elastic_item_source.get("datePublished")

        base.add_value("sourceId", self.getId(response, elastic_item=elastic_item))
        base.add_value("hash", self.getHash(response, elastic_item_source=elastic_item_source))
        try:
            thumbnail_url: str = elastic_item_source.get("image")
            # see: https://dini-ag-kim.github.io/amb/draft/#image
            if thumbnail_url:
                base.add_value("thumbnail", thumbnail_url)
        except KeyError:
            logging.debug(f"OERSI Item {elastic_item['_id']} "
                          f"(name: {elastic_item_source['name']}) did not provide a thumbnail.")
        if "image" in elastic_item_source:
            thumbnail_url = elastic_item_source.get("image")  # thumbnail
            if thumbnail_url:
                base.add_value("thumbnail", thumbnail_url)
        if provider_name:
            # every item gets sorted into a /<provider_name>/-subfolder to make QA more feasable
            base.add_value("origin", provider_name)

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
        try:
            identifier_url: str = self.get_item_url(elastic_item=elastic_item)
            # this URL is REQUIRED and should always be available
            # see https://dini-ag-kim.github.io/amb/draft/#id
        except KeyError:
            logging.warning(f"Item {elastic_item['_id']} did not have an item URL (AMB 'id' was missing)!")
            return
        if identifier_url:
            general.replace_value("identifier", identifier_url)
            technical.add_value("location", identifier_url)
        lom.add_value("technical", technical.load_item())

        organizations_from_affiliation_fields: set[str] = set()
        # this (temporary) set of strings is used to make a decision for OERSI's "sourceOrganization" field:
        # we only store metadata about organizations from this field if an organization didn't appear previously in
        # an "affiliation" field of a "creator" or "contributor". If we didn't do this check, we would have duplicate
        # entries for organizations in our lifecycle items.

        authors = self.get_lifecycle_author(
            lom_base_item_loader=lom,
            elastic_item_source=elastic_item_source,
            date_created=date_created,
            date_published=date_published,
            organization_fallback=organizations_from_affiliation_fields,
        )

        self.get_lifecycle_contributor(
            lom_base_item_loader=lom,
            elastic_item_source=elastic_item_source,
            organization_fallback=organizations_from_affiliation_fields,
            author_list=authors,
        )

        organizations_from_publisher_fields: set[str] = set()
        self.get_lifecycle_publisher(
            lom_base_item_loader=lom,
            elastic_item_source=elastic_item_source,
            organizations_from_publisher_fields=organizations_from_publisher_fields,
            date_published=date_published,
        )

        if "sourceOrganization" in elastic_item_source:
            # # ToDo: this fallback might no longer be necessary:
            # self.get_lifecycle_organization_from_source_organization_fallback(
            #     elastic_item_source=elastic_item_source,
            #     lom_item_loader=lom,
            #     organization_fallback=organizations_from_affiliation_fields,
            # )

            # WLO-BIRD-Connector v2 REQUIREMENT:
            # 'sourceOrganization' -> 'ccm:lifecyclecontributer_publisher'
            self.get_lifecycle_publisher_from_source_organization(
                lom_item_loader=lom,
                elastic_item_source=elastic_item_source,
                previously_collected_publishers=organizations_from_publisher_fields,
            )

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
        vs.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)
        is_accessible_for_free: bool = elastic_item_source.get("isAccessibleForFree")
        if is_accessible_for_free:
            vs.add_value("price", "no")
        else:
            vs.add_value("price", "yes")
        if "conditionsOfAccess" in elastic_item_source:
            conditions_of_access: dict = elastic_item_source.get("conditionsOfAccess")
            if "id" in conditions_of_access:
                conditions_of_access_id: str = conditions_of_access["id"]
                # the "id"-field can hold one of two URLs. Either:
                # https://w3id.org/kim/conditionsOfAccess/login or https://w3id.org/kim/conditionsOfAccess/no_login
                # which is equal to our OEH vocab:
                # https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/conditionsOfAccess.ttl
                if "/conditionsOfAccess/" in conditions_of_access_id:
                    conditions_of_access_value = conditions_of_access_id.split("/")[-1]
                    if conditions_of_access_value:
                        vs.add_value("conditionsOfAccess", conditions_of_access_value)

        hcrt_types = dict()
        oeh_lrt_types = dict()
        learning_resource_types = list()
        if "learningResourceType" in elastic_item_source:
            learning_resource_types: list[dict] = elastic_item_source.get("learningResourceType")
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

        if "about" in elastic_item_source:
            about: list[dict] = elastic_item_source.get("about")
            # see: https://dini-ag-kim.github.io/amb/draft/#about
            # "about" is an OPTIONAL field.
            # The equivalent edu-sharing field will be "ccm:oeh_taxonid_university".
            # each about-field is a list of dictionaries. Here's an example from Open Music Academy:
            # [
            # 		{
            # 			"prefLabel": {
            # 				"de": "Musik, Musikwissenschaft",
            # 				"uk": "Музика, музикознавство",
            # 				"en": "Music, Musicology"
            # 			},
            # 			"id": "https://w3id.org/kim/hochschulfaechersystematik/n78"
            # 		},
            # 		{
            # 			"prefLabel": {
            # 				"de": "Kunst, Kunstwissenschaft",
            # 				"uk": "Мистецтво, мистецтвознавство",
            # 				"en": "Art, Art Theory"
            # 			},
            # 			"id": "https://w3id.org/kim/hochschulfaechersystematik/n9"
            # 		}
            # 	],
            for about_item in about:
                if "id" in about_item:
                    about_id: str = about_item.get("id")
                    # According to the AMB spec, the 'id'-field: can either contain a URL from the
                    # "Destatis-Systematik der Fächergrppen, Studienbereiche und Studienfächer"
                    # (= hochschulfaechersystematik)
                    # e.g.: "https://w3id.org/kim/hochschulfaechersystematik/n78")
                    # or alternatively "Schulfächer" (e.g. http://w3id.org/kim/schulfaecher/)
                    if about_id:
                        # at the moment OERSI exclusively provides university-specific URL values,
                        # but might start providing "schulfaecher"-URLs as well in the future (-> mapping
                        # to 'discipline' will be necessary)
                        if about_id.startswith("https://w3id.org/kim/hochschulfaechersystematik/"):
                            about_id_key = about_id.split("/")[-1]
                            if about_id_key:
                                vs.add_value("hochschulfaechersystematik", about_id_key)
                        else:
                            logging.debug(
                                f"The value of OERSI 'about.id' was not recognized during mapping to "
                                f"valuespaces 'hochschulfaechersystematik': {about_id} ."
                            )
                # if "prefLabel" in about_item:
                #     # ToDo: the 'prefLabel'-strings might be used as fallback values in the future
                #     # Hochschulfächer are available as a list of prefLabel strings in several languages (according to
                #     # the 'Hochschulfaechersystematik')
                #     # - 'de'-field: human-readable German string
                #     # - 'en'-field: human-readable English string
                #     if "de" in about_item:
                #         about_preflabel_de: str = about_item["prefLabel"]["de"]
                #     if "en" in about_item:
                #         about_preflabel_en: str = about_item["prefLabel"]["en"]

        vs.add_value("educationalContext", "hochschule")
        # according to https://oersi.org/resources/pages/en/about/ all Materials indexed by OERSI are in the context of
        # higher education
        # ToDo: remove this hard-coded educationalContext value as soon as OERSI provides metadata for this field

        if "audience" in elastic_item_source:
            # "audience" is an OPTIONAL field in OERSI and is currently only provided for materials from
            # the "Finnish Library of Open Educational Resources"
            audience_dicts: list[dict] = elastic_item_source["audience"]
            # one "audience"-dictionary might look like this:
            # {
            # 			"prefLabel": {
            # 				"de": "Lehrer",
            # 				"fi": "Opettaja",
            # 				"uk": "вчитель",
            # 				"en": "teacher",
            # 				"fr": "enseignant",
            # 				"da": "lærer",
            # 				"es": "profesor",
            # 				"nl": "onderwijzer"
            # 			},
            # 			"id": "http://purl.org/dcx/lrmi-vocabs/educationalAudienceRole/teacher"
            # 		},
            if audience_dicts:
                for audience in audience_dicts:
                    # ToDo: we could use prefLabel values of "de" or "en" as fallbacks in the future (if necessary)
                    if "id" in audience:
                        audience_id_url: str = audience["id"]
                        if audience_id_url:
                            audience_key: str = audience_id_url.split("/")[-1]
                            if audience_key:
                                if audience_key in self.MAPPING_AUDIENCE_TO_INTENDED_END_USER_ROLE:
                                    audience_key = self.MAPPING_AUDIENCE_TO_INTENDED_END_USER_ROLE.get(audience_key)
                                vs.add_value("intendedEndUserRole", audience_key)

        base.add_value("valuespaces", vs.load_item())

        license_loader = LicenseItemLoader()
        if "license" in elastic_item_source:
            license_url: str = elastic_item_source.get("license").get("id")
            if license_url:
                license_mapper = LicenseMapper()
                license_url_mapped = license_mapper.get_license_url(license_string=license_url)
                if license_url_mapped:
                    license_loader.add_value("url", license_url_mapped)
        # noinspection DuplicatedCode
        base.add_value("license", license_loader.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader = ResponseItemLoader()
        response_loader.add_value("url", identifier_url)
        base.add_value("response", response_loader.load_item())

        yield base.load_item()
