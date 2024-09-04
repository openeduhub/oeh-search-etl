import copy
import datetime
import random
import re
from collections import Counter
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
    CourseItemLoader,
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
    version = "0.2.7"  # last update: 2024-07-30
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

    # the "Provider"-filter in the frontend of https://oersi.org/resources/ shows you which string values
    # can be used as a query-parameter for ElasticSearch (names are case-sensitive and need to be matches!)
    # You can use the ELASTIC_PROVIDERS_TO_CRAWL list to manually override the crawling targets. If the list is empty,
    # the crawler will query the ElasticSearch API and fill the list at the beginning of a crawl!
    ELASTIC_PROVIDERS_TO_CRAWL: list = [
        # "BC Campus",  # BC Campus website cannot be crawled at the moment, needs further investigation
        # "ComeIn",  # should not be crawled, datasets were exported to OERSI from WLO
        # "detmoldMusicTools",
        # "digiLL",
        # "DuEPublico",
        # "eaDNURT",
        # "eCampusOntario",
        # "eGov-Campus",
        # "Finnish Library of Open Educational Resources",  # URLs of this metadata-provider cannot be resolved
        # "GitHub",
        # "GitLab",
        # "Helmholtz Codebase",
        # "HessenHub",
        # "HHU Mediathek",
        # "HOOU",
        # "iMoox",
        # "KI Campus",
        # "langSci Press",  # new provider as of 2023-04-27
        # "lecture2go (Hamburg)",  # new provider as of 2023-12-14
        # "MIT OpenCourseWare",
        # "OEPMS",  # new provider as of 2023-04-27 # ToDo: cannot be crawled
        # "OER Portal Uni Graz",
        # "oncampus",  # (temporarily) not available? (2023-12-14)
        # "Open Music Academy",
        # "Open Textbook Library",
        # "Opencast Universität Osnabrück",
        # "openHPI",
        # "OpenLearnWare",
        # "OpenRub",
        # "ORCA.nrw",
        # "Phaidra Uni Wien",
        # "Pressbooks Directory",  # new provider as of 2023-12-14
        # "RWTH Aachen GitLab",
        # "TIB AV-Portal",
        # "TU Delft OpenCourseWare",
        # "twillo",
        # "Universität Innsbruck OER Repositorium",
        # "VCRP",
        # "vhb",
        # "Virtual Linguistics Campus",
        # "ZOERR",
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
    # BIRD-related: "vhb" response dict (from https://open.vhb.org/oersi.json)
    vhb_oersi_json: dict | None = None
    # BIRD-related "iMoox" response dict (from https://imoox.at/mooc/local/moochubs/classes/webservice.php)
    imoox_json: dict | None = None

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)
        # Fetching a "point in time"-id for the subsequent ElasticSearch queries
        self.ELASTIC_PIT_ID = self.elastic_pit_get_id(self.elastic_pit_create())
        # querying the ElasticSearch API for metadata-sets of specific providers, this allows us to control which
        # providers we want to include/exclude by using the "ELASTIC_PROVIDERS_TO_CRAWL"-list
        if not self.ELASTIC_PROVIDERS_TO_CRAWL:
            # if no crawling targets were set (e.g. during debugging), the default behavior is to query all
            # metadata providers from OERSI's ElasticSearch
            self.elastic_fetch_list_of_provider_names()
        self.ELASTIC_ITEMS_ALL = self.elastic_fetch_all_provider_pages()
        # after all items have been collected, delete the ElasticSearch PIT
        json_response = self.elastic_pit_delete()
        if json_response:
            self.logger.info(f"ElasticSearch API response (upon PIT delete): {json_response}")

    def start_requests(self):
        # yield dummy request, so that Scrapy's start_item method requirement is satisfied,
        # then use callback method to crawl all items
        yield scrapy.Request(url="https://oersi.org", callback=self.handle_collected_elastic_items)

    def handle_collected_elastic_items(self, response: scrapy.http.Response):
        random.shuffle(self.ELASTIC_ITEMS_ALL)  # shuffling the list of ElasticSearch items to improve concurrency and
        # distribute the load between several target domains.

        # counting duplicates across "metadata provider"-queries:
        urls_all: list = [x["_source"]["id"] for x in self.ELASTIC_ITEMS_ALL]
        urls_counted = Counter(urls_all)
        duplicates: set = set()
        for item in urls_counted:
            # if items occur more than once, we'll add their URL to the duplicate set (to compare it later)
            if urls_counted[item] > 1:
                duplicates.add(item)
        duplicate_dict = dict()
        for elastic_item in self.ELASTIC_ITEMS_ALL:
            _source_id: str = elastic_item["_source"]["id"]
            if _source_id in duplicates:
                # if an object appears in more than one "MetadataProvider"-query response, we'll create a dictionary,
                # where the "key" is the URL and the "value" is a list of duplicate objects (Type: list[dict])
                if _source_id in duplicate_dict:
                    duplicate_list: list = duplicate_dict[_source_id]
                    duplicate_list.append(elastic_item)
                    duplicate_dict.update({_source_id: duplicate_list})
                else:
                    duplicate_dict.update({_source_id: [elastic_item]})
        # Dumping duplicates to local .json for further analysis:
        # with open("oersi_duplicates.json", "w") as fp:
        #     json.dump(duplicate_dict, fp)
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
                self.logger.debug(
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
            f"https://oersi.org/resources/api/search/oer_data/_pit?keep_alive="
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
        url = f"https://oersi.org/resources/api/search/_pit"
        delete_request = requests.delete(url=url, json=self.ELASTIC_PIT_ID)
        self.logger.debug(f"Deleting ElasticSearch PIT: {self.ELASTIC_PIT_ID}")
        return delete_request.json()

    def elastic_fetch_list_of_provider_names(self):
        _url = "https://oersi.org/resources/api/search/oer_data/_search"

        _payload = {
            "_source": False,
            "size": 0,
            "aggs": {"MetadataProviders": {"terms": {"field": "mainEntityOfPage.provider.name", "size": 500}}},
        }
        # remember to increase the "size"-parameter if the list of metadata-providers reaches > 500 results
        _headers = {"Content-Type": "application/json", "accept": "application/json"}
        response = requests.request("POST", _url, json=_payload, headers=_headers)
        if response.ok:
            response_json: dict = response.json()
            if "aggregations" in response_json:
                aggregations: dict = response_json["aggregations"]
                try:
                    buckets: list[dict] = aggregations["MetadataProviders"]["buckets"]
                    metadata_provider_count_total: int = 0
                    if buckets and isinstance(buckets, list):
                        self.logger.debug(
                            f"OERSI 'MetadataProviders'-query returned {len(buckets)} metadata providers."
                        )
                        self.logger.debug(f"{buckets}")
                    for bucket_item in buckets:
                        if "key" in bucket_item:
                            metadata_provider_name: str = bucket_item["key"]
                            if metadata_provider_name and isinstance(metadata_provider_name, str):
                                self.ELASTIC_PROVIDERS_TO_CRAWL.append(metadata_provider_name)
                        if "doc_count" in bucket_item:
                            metadata_provider_count: int = bucket_item["doc_count"]
                            if metadata_provider_count and isinstance(metadata_provider_count, int):
                                metadata_provider_count_total += metadata_provider_count
                    if self.ELASTIC_PROVIDERS_TO_CRAWL:
                        self.logger.info(
                            f"Successfully retrieved the following metadata providers for future API "
                            f"requests:\n"
                            f"{self.ELASTIC_PROVIDERS_TO_CRAWL}"
                        )
                        if metadata_provider_count_total:
                            self.logger.info(
                                f"Expecting {metadata_provider_count_total} ElasticSearch objects in " f"total."
                            )
                except KeyError as ke:
                    self.logger.error(
                        f"Failed to retrieve 'buckets'-list of metadata providers from OERSI "
                        f"ElasticSearch response (please check (with a debugger) if the property "
                        f"'aggregations.MetadataProviders.buckets' was part of the API response!)"
                    )
                    raise ke
            else:
                self.logger.error(
                    f"Failed to retrieve list of metadata providers from OERSI's ElasticSearch API. "
                    f"(The response object did not return a 'aggregations'-object. Please check the API!)"
                )

    def elastic_query_provider_metadata(self, provider_name, search_after=None):
        """
        Queries OERSI's ElasticSearch API for metadata items from a specific metadata provider, as specified by the
        "provider_name"-string.

        See:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#paginate-search-results
        """
        url = "https://oersi.org/resources/api/search/_search"
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
            self.logger.info(
                f"Recognized OERSI_METADATA_PROVIDER .env setting. Limiting crawl to the following target(s): "
                f"{provider_target_from_env}"
            )
            self.ELASTIC_PROVIDERS_TO_CRAWL = [provider_target_from_env]
            if ";" in provider_target_from_env:
                provider_list: list[str] = provider_target_from_env.split(";")
                self.logger.info(
                    f"Recognized multiple providers within OERSI_METADATA_PROVIDER .env setting:" f"{provider_list}"
                )
                self.ELASTIC_PROVIDERS_TO_CRAWL = provider_list
        # --- BIRD-related hooks ---
        if "iMoox" in self.ELASTIC_PROVIDERS_TO_CRAWL:
            self.fetch_imoox_data()
        if "vhb" in self.ELASTIC_PROVIDERS_TO_CRAWL:
            # experimental BIRD-Hook for "vhb"-courses!
            # ToDo: refactor this implementation into its own (sub-)class ASAP!
            #  (WARNING: This PoC will not scale well for over >50 Metadata-Providers within OERSI
            #  and REQUIRES a separate infrastructure!)
            self.fetch_vhb_data()

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
                        self.logger.info(
                            f"ElasticSearch: pit_id changed between queries, using the new pit_id "
                            f"{current_page_json_response.get('pit_id')} for subsequent queries."
                        )
                if "hits" in current_page_json_response.get("hits"):
                    provider_items: list[dict] = current_page_json_response.get("hits").get("hits")
                    if provider_items:
                        self.logger.debug(f"The provider_items list has {len(provider_items)} entries")
                        for provider_item in provider_items:
                            # we need to keep track of the metadata provider because the ElasticSearch query parameter
                            # will oftentimes NOT be the same string that we receive as the provider metadata value
                            # from "mainEntityOfPage.provider.name"
                            provider_item.update({"OERSI_QUERY_PROVIDER_NAME": provider_name})
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
                        self.logger.info(
                            f"Reached the end of the ElasticSearch results for '{provider_name}' // "
                            f"Total amount of items collected (across all metadata-providers): {len(all_items)}"
                        )
                        break
        return all_items

    def fetch_imoox_data(self):
        imoox_response: requests.Response = requests.get("https://imoox.at/mooc/local/moochubs/classes/webservice.php")
        self.logger.info(f"BIRD: Fetching 'course'-data from iMoox: {imoox_response.url} ...")
        imoox_response_dict: dict = imoox_response.json()
        if imoox_response_dict and isinstance(imoox_response_dict, dict):
            if "data" in imoox_response_dict:
                imoox_course_items = imoox_response_dict["data"]
                self.logger.info(
                    f"BIRD: Successfully retrieved {len(imoox_course_items)} items from {imoox_response.url} ."
                )
                self.imoox_json = copy.deepcopy(imoox_response_dict)
        else:
            self.logger.warning(f"BIRD: Failed to retrieve 'course'-data from 'iMoox' sourceOrganization.")

    def fetch_vhb_data(self):
        vhb_response: requests.Response = requests.get(url="https://open.vhb.org/oersi.json")
        self.logger.info(f"BIRD: Fetching 'course'-data from vhb: {vhb_response.url} ...")
        vhb_response_dict: dict = vhb_response.json()
        if vhb_response_dict and isinstance(vhb_response_dict, dict):
            if "data" in vhb_response_dict:
                vhb_course_items = vhb_response_dict["data"]
                self.logger.info(
                    f"BIRD: Successfully retrieved {len(vhb_course_items)} items " f"from {vhb_response.url} ."
                )
                self.vhb_oersi_json = copy.deepcopy(vhb_response_dict)
        else:
            self.logger.warning(f"BIRD: Failed to retrieve 'course'-data from 'vhb' sourceOrganization.")

    def getId(self, response=None, elastic_item: dict = dict) -> str:
        """
        Uses OERSI's "_source.id"-property to collect a URI. According to the AMB Specifications, the URI can be either:
        - a (direct) URL to the educational resource
        - a URL pointing towards a landing page (describing the educational resource)

        See: https://dini-ag-kim.github.io/amb/latest/#id
        """
        return elastic_item["_source"]["id"]

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
            hash_temp: str = f"{date_published}v{self.version}"
        elif date_created:
            hash_temp: str = f"{date_created}v{self.version}"
        else:
            hash_temp: str = f"{datetime.datetime.now().isoformat()}v{self.version}"
        return hash_temp

    def get_uuid(self, elastic_item: dict):
        """
        Builds a UUID string from the to-be-parsed target URL and returns it.
        """
        # The "getUUID"-method of LomBase couldn't be cleanly overridden because at the point of time when we do this
        # check, there is no "Response"-object available yet.
        item_url = self.get_item_url(elastic_item=elastic_item)
        return EduSharing.build_uuid(item_url)

    def get_item_url(self, elastic_item: dict) -> str | None:
        """
        Retrieves the to-be-parsed URL from OERSI's '_source.id'-field.
        If that (REQUIRED) field was not available, returns None.
        """
        item_url: str = elastic_item["_source"]["id"]
        if item_url:
            return item_url
        else:
            self.logger.warning(f"OERSI Item {elastic_item['_id']} did not provide a URL string. Dropping item.")
            return None

    def hasChanged(self, response=None, elastic_item: dict = dict) -> bool:
        elastic_item = elastic_item
        if self.forceUpdate:
            return True
        if self.uuid:
            if self.get_uuid(elastic_item=elastic_item) == self.uuid:
                self.logger.info(f"matching requested id: {self.uuid}")
                return True
            return False
        if self.remoteId:
            if str(self.getId(response, elastic_item=elastic_item)) == self.remoteId:
                self.logger.info(f"matching requested id: {self.remoteId}")
                return True
            return False
        db = EduSharing().find_item(self.getId(response, elastic_item=elastic_item), self)
        changed = db is None or db[1] != self.getHash(response, elastic_item_source=elastic_item["_source"])
        if not changed:
            self.logger.info(f"Item {self.getId(response, elastic_item=elastic_item)} (uuid: {db[0]}) has not changed")
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
        if affiliation_dict and isinstance(affiliation_dict, dict) and "name" in affiliation_dict:
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

    def validate_academic_title_string(self, honorific_prefix: str) -> str:
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
            self.logger.debug(
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

    def lifecycle_determine_type_of_identifier_and_save_uri(
        self, item_dictionary: dict, lifecycle_item_loader: LomLifecycleItemloader
    ):
        """
        OERSI's "creator"/"contributor"/"affiliation" items might contain an 'id'-field which (optionally) provides
        URI-identifiers that reference GND / ORCID / Wikidata / ROR.
        This method checks if the 'id'-field is available at all, and if it is, determines if the string should be
        saved to an identifier-specific field of LomLifecycleItemLoader.
        If the URI string of "id" could not be recognized, it will save the value to 'lifecycle.url' as a fallback.
        """
        if "id" in item_dictionary and isinstance(item_dictionary["id"], str):
            # "creator.id" can be 'null', therefore we need to explicitly check its type before trying to parse it
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
                self.logger.info(
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

    def enrich_imoox_metadata(self, base_itemloader: BaseItemLoader, elastic_item: dict):
        """
        Combines the retrieved metadata from OERSI's elastic_item with iMoox (MOOCHub v3) metadata
        if the identifiers match.
        """
        if self.imoox_json:
            if "data" in self.imoox_json:
                imoox_item_matched: dict | None = None
                try:
                    imoox_items: list[dict] = self.imoox_json["data"]
                    for imoox_item in imoox_items:
                        imoox_course_url: str = imoox_item["attributes"]["url"]
                        if imoox_course_url and imoox_course_url == self.get_item_url(elastic_item):
                            self.logger.debug(
                                f"BIRD: Matched 'iMoox'-item {imoox_course_url} with OERSI "
                                f"ElasticSearch item {elastic_item['_id']} "
                                f"({elastic_item['_source']['id']})"
                            )
                            imoox_item_matched = imoox_item
                except KeyError as ke:
                    raise ke
                if imoox_item_matched:
                    course_itemloader: CourseItemLoader = CourseItemLoader()
                    if "attributes" in imoox_item_matched:
                        imoox_attributes: dict = imoox_item_matched["attributes"]
                        # ToDo: MOOCHUb Spec v3 allows a list of (multiple, unique) date strings for
                        #  - "startDate"
                        #  - "endDate"
                        #  -> "CourseItem" needs to be expanded to support multiple values for this field
                        #
                        #  (this problem is theoretical in nature at the moment,
                        #  since "iMoox" currently provides only 1 value per property,
                        #  but this might change in the future!)
                        if "startDate" in imoox_attributes:
                            start_dates: list[str] = imoox_attributes["startDate"]
                            if start_dates and isinstance(start_dates, list):
                                for start_date_raw in start_dates:
                                    if start_date_raw and isinstance(start_date_raw, str):
                                        course_itemloader.add_value("course_availability_from", start_date_raw)
                                    else:
                                        self.logger.warning(
                                            f'Received unexpected type for "startDate" {start_date_raw} . '
                                            f"Expected str, but received {type(start_date_raw)} instead."
                                        )
                        if "endDate" in imoox_attributes:
                            end_dates: list[str] = imoox_attributes["endDate"]
                            if end_dates and isinstance(end_dates, list):
                                for end_date_raw in end_dates:
                                    if end_date_raw and isinstance(end_date_raw, str):
                                        course_itemloader.add_value("course_availability_until", end_date_raw)
                                    else:
                                        self.logger.warning(
                                            f'Received unexpected type for "endDate" {end_date_raw}. '
                                            f"Expected str, but received {type(end_date_raw)} instead."
                                        )
                        if "trailer" in imoox_attributes:
                            # example data (as of 2024-05-27)
                            # "trailer": {
                            # 			"contentUrl": "https://www.youtube.com/watch?v=DljC8FPpE1s",
                            # 			"type": "VideoObject",
                            # 			"license": [
                            # 				{
                            # 					"identifier": "CC-BY-SA-4.0",
                            # 					"url": "https://creativecommons.org/licenses/by-sa/4.0/"
                            # 				}
                            # 			]
                            # 		},
                            if "contentUrl" in imoox_attributes["trailer"]:
                                imoox_course_trailer_url: str = imoox_attributes["trailer"]["contentUrl"]
                                if imoox_course_trailer_url and isinstance(imoox_course_trailer_url, str):
                                    course_itemloader.add_value("course_url_video", imoox_course_trailer_url)
                        if "duration" in imoox_attributes and "workload" in imoox_attributes:
                            # ToDo: "duration" and "workload" can currently only be saved as a (coupled)
                            #  value since the destination is "cclom:typicallearningtime" for both fields
                            #  which expects a (total) duration in milliseconds

                            # iMoox provides "duration" as ISO-8601 formatted duration (period) strings.
                            # Typical "duration" values (as of 2024-05-27): "P7W", "P12W" etc.
                            # see MOOCHub v3 Schema:
                            # https://github.com/MOOChub/schema/blob/main/moochub-schema.json#L907-L912
                            amount_of_weeks: int | None = None
                            duration_in_weeks_raw: str = imoox_attributes["duration"]
                            if duration_in_weeks_raw and isinstance(duration_in_weeks_raw, str):
                                duration_pattern: re.Pattern = re.compile(r"""^P(?P<amount_of_weeks>\d+)W$""")
                                duration_result: re.Match | None = duration_pattern.search(duration_in_weeks_raw)
                                if duration_result:
                                    dura_dict: dict = duration_result.groupdict()
                                    if "amount_of_weeks" in dura_dict:
                                        amount_of_weeks = dura_dict["amount_of_weeks"]
                                        # convert to Integer for further calculations
                                        amount_of_weeks = int(amount_of_weeks)
                            # ATTENTION: iMoox uses a different structure for "workload"-objects than vhb!
                            #  (due to different MOOCHub versions)
                            # example data (as of 2024-05-27):
                            # "workload": {
                            # 			"timeValue": 2,
                            # 			"timeUnit": "h/week"
                            # 		},
                            # see MOOCHub v3 Schema - workload:
                            # (https://github.com/MOOChub/schema/blob/main/moochub-schema.json#L1634-L1662),
                            time_value: int | None = None
                            time_unit: str | None = None
                            if "timeUnit" in imoox_attributes["workload"]:
                                # "timeUnit" can be one of several values:
                                # "h/month", "h/week", "h/day"
                                time_unit: str = imoox_attributes["workload"]["timeUnit"]
                            if "timeValue" in imoox_attributes["workload"]:
                                time_value: int = imoox_attributes["workload"]["timeValue"]
                            if time_unit and time_value and amount_of_weeks:
                                # "iMoox" provides all their durations / workloads in a week-related way,
                                # while "cclom:typicallearningtime" expects ms. Therefore:
                                # 1) we extract the amount of weeks from "duration"
                                # 2) calculate: <amount_of_weeks> * <h/week> = total duration in h
                                # 3) convert total duration from hours to seconds
                                # (-> es_connector will handle conversion from s to ms)
                                if time_unit == "h/week":
                                    total_duration_in_hours: int = amount_of_weeks * time_value
                                    duration_delta = datetime.timedelta(hours=total_duration_in_hours)
                                    if duration_delta:
                                        total_duration_in_seconds: int = int(duration_delta.total_seconds())
                                        course_itemloader.add_value("course_duration", total_duration_in_seconds)
                                        self.logger.debug(
                                            f"BIRD: combined iMoox 'duration' "
                                            f"( {duration_in_weeks_raw} ) and 'workload' "
                                            f"( {time_value} {time_unit} ) to {total_duration_in_hours} h "
                                            f"(-> {total_duration_in_seconds} s)."
                                        )
                                else:
                                    # ToDo: convert "h/day" and "h/month" in a similar fashion
                                    self.logger.warning(
                                        f"BIRD: iMoox provided a time unit {time_unit} for 'workload' "
                                        f"which couldn't be handled. "
                                        f"(Please update the crawler!)"
                                    )
                        pass
                    base_itemloader.add_value("course", course_itemloader.load_item())

    def enrich_vhb_metadata(
        self,
        base_itemloader: BaseItemLoader,
        elastic_item: dict,
        lom_general_itemloader: LomGeneralItemloader,
        in_languages: list[str] | None,
    ):
        """
        Combines metadata from OERSI's elastic_item with MOOCHub v2.x metadata from the source (vhb)
        if the identifiers match.
        """
        # Reminder: "VHB" (= "Virtuelle Hochschule Bayern") uses MOOCHub for their JSON export!
        # The following implementation is therefore MOOCHub-specific
        # and NEEDS to be refactored into a separate class hook ASAP!
        if self.vhb_oersi_json:
            if "data" in self.vhb_oersi_json:
                try:
                    vhb_items: list[dict] = self.vhb_oersi_json["data"]
                    vhb_item_matched: dict | None = None
                    for vhb_item in vhb_items:
                        # since the vhb_item has a different "id", the only way to match the OERSI item
                        # against the vhb item is by comparing their URLs:
                        vhb_course_url: str = vhb_item["attributes"]["url"]
                        if vhb_course_url and vhb_course_url == self.get_item_url(elastic_item):
                            self.logger.debug(
                                f"BIRD: Matched 'vhb'-item {vhb_course_url} with OERSI "
                                f"ElasticSearch item {elastic_item['_id']}"
                            )
                            vhb_item_matched = vhb_item
                except KeyError as ke:
                    raise ke
                if vhb_item_matched:
                    # if we found a match, we're now trying to enrich the item with metadata from both
                    # sources
                    course_itemloader: CourseItemLoader = CourseItemLoader()
                    if "attributes" in vhb_item_matched:
                        if not in_languages and "languages" in vhb_item_matched["attributes"]:
                            # beware: the vhb 'languages'-property is a string value!
                            vhb_language: str | None = vhb_item_matched["attributes"]["languages"]
                            if vhb_language and isinstance(vhb_language, str):
                                lom_general_itemloader.add_value("language", vhb_language)
                            elif vhb_language:
                                self.logger.warning(
                                    f"Received unexpected vhb 'languages'-type! " f"(Type: {type(vhb_language)}"
                                )
                        if "abstract" in vhb_item_matched["attributes"]:
                            vhb_abstract: str = vhb_item_matched["attributes"]["abstract"]
                            if vhb_abstract and isinstance(vhb_abstract, str):
                                course_itemloader.add_value("course_description_short", vhb_abstract)
                        if "learningObjectives" in vhb_item_matched["attributes"]:
                            vhb_learning_objectives: str = vhb_item_matched["attributes"]["learningObjectives"]
                            if vhb_learning_objectives and isinstance(vhb_learning_objectives, str):
                                course_itemloader.add_value("course_learningoutcome", vhb_learning_objectives)
                        if "outline" in vhb_item_matched["attributes"]:
                            outline_raw: str = vhb_item_matched["attributes"]["outline"]
                            if outline_raw and isinstance(outline_raw, str):
                                # vhb "outline" -> course_schedule -> "ccm:oeh_course_schedule"
                                # the vhb attribute "outline" describes a course's schedule (Kursablauf)
                                # IMPORTANT: "outline" is not part of MOOCHub v2.x nor 3.x!
                                course_itemloader.add_value("course_schedule", outline_raw)
                            else:
                                self.logger.warning(
                                    f"Received vhb 'outline'-property of unexpected type: " f"{outline_raw}"
                                )
                        if "startDate" in vhb_item_matched["attributes"]:
                            start_date_raw: str = vhb_item_matched["attributes"]["startDate"]
                            if start_date_raw and isinstance(start_date_raw, str):
                                course_itemloader.add_value("course_availability_from", start_date_raw)
                            else:
                                self.logger.warning(
                                    f'Received unexpected type for "startDate" {start_date_raw} . '
                                    f"Expected a string, but received {type(start_date_raw)} instead."
                                )
                        if "video" in vhb_item_matched["attributes"]:
                            video_item: dict = vhb_item_matched["attributes"]["video"]
                            if video_item:
                                if "url" in video_item:
                                    vhb_course_video_url: str = video_item["url"]
                                    if vhb_course_video_url:
                                        course_itemloader.add_value("course_url_video", vhb_course_video_url)
                                # ToDo: "video.licenses" is of type list[dict]
                                #  each "license"-dict can have an "id"- and "url"-property
                        if "workload" in vhb_item_matched["attributes"]:
                            vhb_workload_raw: str = vhb_item_matched["attributes"]["workload"]
                            if vhb_workload_raw and isinstance(vhb_workload_raw, str):
                                # vhb "workload"-values are described as a natural lange (German)
                                # "<number> <unit>"-string, e.g.: "5 Stunden" or "60 Stunden".
                                # Since edu-sharing expects seconds in "cclom:typicallearningtime",
                                # we need to parse the string and convert it to seconds.
                                vhb_workload: str = vhb_workload_raw.strip()
                                duration_pattern = re.compile(r"""(?P<duration_number>\d+)\s*(?P<duration_unit>\w*)""")
                                # ToDo: refactor into
                                #  "MOOCHub (v2?) workload to BIRD course_duration" method
                                duration_match: re.Match | None = duration_pattern.search(vhb_workload)
                                duration_delta: datetime.timedelta = datetime.timedelta()
                                if duration_match:
                                    duration_result: dict = duration_match.groupdict()
                                    if "duration_number" in duration_result:
                                        duration_number_raw: str = duration_result["duration_number"]
                                        duration_number: int = int(duration_number_raw)
                                        if "duration_unit" in duration_result:
                                            duration_unit: str = duration_result["duration_unit"]
                                            duration_unit = duration_unit.lower()
                                            match duration_unit:
                                                case "sekunden":
                                                    duration_delta = duration_delta + datetime.timedelta(
                                                        seconds=duration_number
                                                    )
                                                case "minuten":
                                                    duration_delta = duration_delta + datetime.timedelta(
                                                        minutes=duration_number
                                                    )
                                                case "stunden":
                                                    duration_delta = duration_delta + datetime.timedelta(
                                                        hours=duration_number
                                                    )
                                                case "tage":
                                                    duration_delta = duration_delta + datetime.timedelta(
                                                        days=duration_number
                                                    )
                                                case "wochen":
                                                    duration_delta = duration_delta + datetime.timedelta(
                                                        weeks=duration_number
                                                    )
                                                case "monate":
                                                    # timedelta has no parameter for months
                                                    #  -> X months = X * (4 weeks)
                                                    duration_delta = duration_delta + (
                                                        duration_number * datetime.timedelta(weeks=4)
                                                    )
                                                case _:
                                                    self.logger.warning(
                                                        f"Failed to parse 'workload' time unit"
                                                        f"from vhb course: "
                                                        f"{vhb_item_matched}"
                                                    )
                                            if duration_delta:
                                                workload_in_seconds: int = int(duration_delta.total_seconds())
                                                if workload_in_seconds:
                                                    course_itemloader.add_value("course_duration", workload_in_seconds)
                    base_itemloader.add_value("course", course_itemloader.load_item())

    def look_for_twillo_url_in_elastic_item(self, elastic_item: dict) -> str | None:
        """
        Look for a twillo.de URL with an "/edu-sharing/"-path within OERSI's "_source.id" and "mainEntityOfPage.id"
        properties.
        Returns the twillo URL string if successful, otherwise returns None.
        """
        twillo_url: str | None = None
        twillo_url_from_source_id: str = self.getId(response=None, elastic_item=elastic_item)
        twillo_url_from_maeop_id: str | None = None
        twillo_edu_sharing_url_path: str = "twillo.de/edu-sharing/components/render/"
        if "_source" in elastic_item:
            elastic_item_source: dict = elastic_item["_source"]
            if "mainEntityOfPage" in elastic_item_source:
                main_entity_of_page: list[dict] = elastic_item_source["mainEntityOfPage"]
                for maeop_item in main_entity_of_page:
                    if "id" in maeop_item:
                        maeop_id: str = maeop_item["id"]
                        if maeop_id and twillo_edu_sharing_url_path in maeop_id:
                            twillo_url_from_maeop_id = maeop_id
        if twillo_url_from_source_id and twillo_edu_sharing_url_path in twillo_url_from_source_id:
            twillo_url = twillo_url_from_source_id
        elif twillo_url_from_maeop_id:
            twillo_url = twillo_url_from_maeop_id
        return twillo_url

    @staticmethod
    def extract_twillo_node_id_from_url(twillo_url: str) -> str | None:
        """
        Extract the twillo nodeId from a provided URL string.
        """
        if twillo_url and isinstance(twillo_url, str):
            twillo_node_id: str | None = None
            if "twillo.de/edu-sharing/components/render/" in twillo_url:
                potential_twillo_node_id = twillo_url.split("/")[-1]
                if potential_twillo_node_id and isinstance(potential_twillo_node_id, str):
                    twillo_node_id = potential_twillo_node_id
            if twillo_node_id:
                return twillo_node_id
            else:
                return None

    def request_metadata_for_twillo_node_id(
        self,
        base_itemloader: BaseItemLoader,
        lom_base_itemloader: LomBaseItemloader,
        lom_classification_itemloader: LomClassificationItemLoader,
        lom_educational_itemloader: LomEducationalItemLoader,
        lom_general_itemloader: LomGeneralItemloader,
        lom_technical_itemloader: LomTechnicalItemLoader,
        license_itemloader: LicenseItemLoader,
        valuespaces_itemloader: ValuespaceItemLoader,
        elastic_item: dict,
        twillo_node_id: str,
    ):
        """
        Query the edu-sharing repository of twillo.de for metadata of a specific nodeId.
        If the request was successful, return the response dictionary.
        """
        twillo_api_request_url = (
            f"https://www.twillo.de/edu-sharing/rest/rendering/v1/details/-home-/" f"{twillo_node_id}"
        )
        # note: we NEED to use the "rendering/v1/details/..."-API-endpoint because
        # https://www.twillo.de/edu-sharing/rest/node/v1/nodes/-home-/{twillo_node_id}/metadata?propertyFilter=-all-
        # throws "org.edu_sharing.restservices.DAOSecurityException"-errors (for hundreds of objects!),
        # even though the queried learning objects are publicly available and reachable
        twillo_request = scrapy.Request(
            url=twillo_api_request_url,
            priority=2,
            callback=self.enrich_oersi_item_with_twillo_metadata,
            cb_kwargs={
                "elastic_item": elastic_item,
                "twillo_node_id": twillo_node_id,
                "base_itemloader": base_itemloader,
                "lom_base_itemloader": lom_base_itemloader,
                "lom_classification_itemloader": lom_classification_itemloader,
                "lom_educational_itemloader": lom_educational_itemloader,
                "lom_general_itemloader": lom_general_itemloader,
                "lom_technical_itemloader": lom_technical_itemloader,
                "license_itemloader": license_itemloader,
                "valuespaces_itemloader": valuespaces_itemloader,
            },
        )
        yield twillo_request

    def enrich_oersi_item_with_twillo_metadata(
        self,
        response: scrapy.http.TextResponse,
        base_itemloader: BaseItemLoader,
        lom_base_itemloader: LomBaseItemloader,
        lom_classification_itemloader: LomClassificationItemLoader,
        lom_educational_itemloader: LomEducationalItemLoader,
        lom_general_itemloader: LomGeneralItemloader,
        lom_technical_itemloader: LomTechnicalItemLoader,
        license_itemloader: LicenseItemLoader,
        valuespaces_itemloader: ValuespaceItemLoader,
        elastic_item: dict = None,
        twillo_node_id: str = None,
    ):
        """
        Process the twillo API response and enrich the OERSI item with twillo metadata properties (if possible).
        If the twillo API response was invalid (or didn't provide the metadata we were looking for), yield the
        (complete) BaseItem.

        @param response: the twillo API response (JSON)
        @param base_itemloader: BaseItemLoader object
        @param lom_base_itemloader: LomBaseItemloader object
        @param lom_classification_itemloader: LomClassificationItemloader object
        @param lom_educational_itemloader: LomEducationalItemloader object
        @param lom_general_itemloader: LomGeneralItemloader object
        @param lom_technical_itemloader: LomTechnicalItemloader object
        @param license_itemloader: LicenseItemloader object
        @param valuespaces_itemloader: ValuespacesItemloader object
        @param elastic_item: the ElasticSearch item from the OERSI API
        @param twillo_node_id: the twillo "nodeId"
        @return: the complete BaseItem object
        """
        twillo_response: scrapy.http.TextResponse = response
        twillo_response_json: dict | None = None
        twillo_metadata: dict | None = None
        try:
            twillo_response_json: dict = twillo_response.json()
        except requests.exceptions.JSONDecodeError:
            self.logger.warning(f"BIRD: Received invalid JSON response from {response.url} :" f"{twillo_response}")
        if twillo_response_json and isinstance(twillo_response_json, dict):
            if "node" in twillo_response_json:
                # we assume that the response is valid if we receive a dictionary containing
                # "node" as the main key
                twillo_metadata = twillo_response_json
            else:
                self.logger.warning(
                    f"BIRD: twillo API response for nodeId {twillo_node_id} " f"was invalid: {twillo_response_json}"
                )
        else:
            self.logger.warning(
                f"BIRD: Failed to extract additional metadata for twillo "
                f"nodeId {twillo_node_id} ! "
                f"Received HTTP Response Status {twillo_response.status}."
            )

        if twillo_metadata and isinstance(twillo_metadata, dict):
            # the API response should contain a "node"-key which contains all properties within
            node_dict: dict = twillo_metadata["node"]
            if node_dict and "properties" in node_dict:
                node_properties: dict = node_dict["properties"]
                if node_properties:
                    twillo_typical_learning_time: list[str] | None = None
                    twillo_cclom_context: list[str] | None = None
                    # ToDo:
                    #  - twillo "Level" ("cclom:interactivitylevel") -> BIRD <?>
                    #  - twillo "Event Format" ("cclom:interactivitytype") -> BIRD <?>
                    #  - twillo "Technical Requirements" ("cclom:otherplatformrequirements") -> BIRD <?>
                    if "cclom:typicallearningtime" in node_properties:
                        # twillo "Duration" ("cclom:typicallearningtime") -> BIRD "course_duration"
                        twillo_typical_learning_time: list[str] = node_properties["cclom:typicallearningtime"]
                    if "cclom:context" in node_properties:
                        # twillo "Function" ("cclom:context") -> BIRD "course_learningoutcome"
                        twillo_cclom_context: list[str] = node_properties["cclom:context"]
                    if "cclom:educational_description" in node_properties:
                        educational_description_raw: list[str] = node_properties["cclom:educational_description"]
                        if educational_description_raw and isinstance(educational_description_raw, list):
                            # twillo Frontend: "Field Report" (= "cclom:educational_description")
                            for edu_desc_item in educational_description_raw:
                                if edu_desc_item and isinstance(edu_desc_item, str):
                                    # strip whitespace and sort out the invalid (empty) strings first
                                    edu_desc_item: str = edu_desc_item.strip()
                                    # ToDo: move responsibility of cleaning up "description"-strings
                                    #  into its own pipeline
                                    if edu_desc_item:
                                        lom_educational_itemloader.add_value("description", edu_desc_item)
                    if twillo_typical_learning_time or twillo_cclom_context:
                        course_item_loader = CourseItemLoader()
                        if twillo_typical_learning_time:
                            course_item_loader.add_value("course_duration", twillo_typical_learning_time)
                        if twillo_cclom_context:
                            context_cleaned: list[str] = list()
                            if twillo_cclom_context and isinstance(twillo_cclom_context, list):
                                for context_value in twillo_cclom_context:
                                    if context_value and isinstance(context_value, str):
                                        context_value = context_value.strip()
                                        # whitespace typos and empty string values (" ") are removed
                                        if context_value:
                                            context_cleaned.append(context_value)
                            if context_cleaned:
                                course_item_loader.add_value("course_learningoutcome", context_cleaned)
                        base_itemloader.add_value("course", course_item_loader.load_item())

        # noinspection DuplicatedCode
        lom_base_itemloader.add_value("general", lom_general_itemloader.load_item())
        lom_base_itemloader.add_value("technical", lom_technical_itemloader.load_item())
        lom_base_itemloader.add_value("educational", lom_educational_itemloader.load_item())
        lom_base_itemloader.add_value("classification", lom_classification_itemloader.load_item())
        base_itemloader.add_value("lom", lom_base_itemloader.load_item())
        base_itemloader.add_value("valuespaces", valuespaces_itemloader.load_item())
        base_itemloader.add_value("license", license_itemloader.load_item())

        permissions = super().getPermissions(response)
        base_itemloader.add_value("permissions", permissions.load_item())

        response_loader = ResponseItemLoader()
        identifier_url: str = self.get_item_url(elastic_item=elastic_item)
        response_loader.add_value("url", identifier_url)
        base_itemloader.add_value("response", response_loader.load_item())

        yield base_itemloader.load_item()

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
            self.logger.debug(
                f"OERSI Item {elastic_item['_id']} "
                f"(name: {elastic_item_source['name']}) did not provide a thumbnail."
            )
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

        technical = LomTechnicalItemLoader()
        try:
            identifier_url: str = self.get_item_url(elastic_item=elastic_item)
            # this URL is REQUIRED and should always be available
            # see https://dini-ag-kim.github.io/amb/draft/#id
        except KeyError:
            self.logger.warning(f"Item {elastic_item['_id']} did not have an item URL (AMB 'id' was missing)!")
            return
        if identifier_url:
            general.replace_value("identifier", identifier_url)
            technical.add_value("location", identifier_url)

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

        classification = LomClassificationItemLoader()

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
                            self.logger.debug(
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

        license_loader = LicenseItemLoader()
        if "license" in elastic_item_source:
            license_url: str = elastic_item_source.get("license").get("id")
            if license_url:
                license_mapper = LicenseMapper()
                license_url_mapped = license_mapper.get_license_url(license_string=license_url)
                if license_url_mapped:
                    license_loader.add_value("url", license_url_mapped)

        # --- BIRD HOOKS START HERE!
        if "OERSI_QUERY_PROVIDER_NAME" in elastic_item:
            # BIRD-related requirement: merge item with additional metadata retrieved directly from the source
            if elastic_item["OERSI_QUERY_PROVIDER_NAME"]:
                # checking if the "metadata provider name" that was used for the ElasticSearch query needs to be handled
                query_parameter_provider_name: str = elastic_item["OERSI_QUERY_PROVIDER_NAME"]
                if query_parameter_provider_name:
                    if query_parameter_provider_name == "iMoox":
                        self.enrich_imoox_metadata(base, elastic_item)
                    if query_parameter_provider_name == "twillo":
                        twillo_url: str | None = self.look_for_twillo_url_in_elastic_item(elastic_item)
                        # a typical twillo URL could look like this example:
                        # https://www.twillo.de/edu-sharing/components/render/106ed8e7-1d07-4a77-8ca2-19c9e28782ed
                        # we need the nodeId (the last part of the url) to create an API request for its metadata
                        twillo_node_id: str | None = self.extract_twillo_node_id_from_url(twillo_url)
                        if twillo_node_id:
                            # if a twillo nodeId was found, the complete item will be yielded by its own method
                            yield from self.request_metadata_for_twillo_node_id(
                                base_itemloader=base,
                                lom_base_itemloader=lom,
                                lom_classification_itemloader=classification,
                                lom_educational_itemloader=educational,
                                lom_general_itemloader=general,
                                lom_technical_itemloader=technical,
                                license_itemloader=license_loader,
                                valuespaces_itemloader=vs,
                                elastic_item=elastic_item,
                                twillo_node_id=twillo_node_id,
                            )
                            return None  # necessary to not accidentally parse the same twillo item twice!
                    if query_parameter_provider_name == "vhb":
                        self.enrich_vhb_metadata(base, elastic_item, general, in_languages)
        # --- BIRD HOOKS END HERE!

        # noinspection DuplicatedCode
        lom.add_value("general", general.load_item())
        lom.add_value("technical", technical.load_item())
        lom.add_value("educational", educational.load_item())
        lom.add_value("classification", classification.load_item())
        base.add_value("lom", lom.load_item())
        base.add_value("valuespaces", vs.load_item())
        base.add_value("license", license_loader.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader = ResponseItemLoader()
        response_loader.add_value("url", identifier_url)
        base.add_value("response", response_loader.load_item())

        yield base.load_item()
