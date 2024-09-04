import datetime
import json
import logging

import dateparser
import requests
import scrapy

from converter import env
from converter.constants import Constants
from converter.items import (
    BaseItemLoader,
    LomBaseItemloader,
    LomGeneralItemloader,
    LomTechnicalItemLoader,
    LomLifecycleItemloader,
    LomEducationalItemLoader,
    ValuespaceItemLoader,
    LicenseItemLoader,
    ResponseItemLoader,
)
from converter.spiders.base_classes import LomBase
from converter.web_tools import WebEngine, WebTools
from ..es_connector import EduSharing
from ..util.license_mapper import LicenseMapper


class SerloSpider(scrapy.Spider, LomBase):
    name = "serlo_spider"
    friendlyName = "serlo_spider"
    # start_urls = ["https://de.serlo.org"]
    API_URL = "https://api.serlo.org/graphql"
    # for the API description, please check: https://lenabi.serlo.org/metadata-api
    version = "0.3.3"  # last update: 2023-08-16 (Serlo API v1.2.0)
    custom_settings = {
        # Using Playwright because of Splash-issues with thumbnails+text for Serlo
        "WEB_TOOLS": WebEngine.Playwright
    }
    GRAPHQL_MODIFIED_AFTER_PARAMETER: str = ""
    GRAPHQL_INSTANCE_PARAMETER: str = ""

    graphql_items = list()
    # Mapping from EducationalAudienceRole (LRMI) to IntendedEndUserRole(LOM), see:
    # https://www.dublincore.org/specifications/lrmi/concept_schemes/#educational-audience-role
    # https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/intendedEndUserRole.ttl
    EDU_AUDIENCE_ROLE_MAPPING = {
        "administrator": ["manager", "counsellor"],
        # A trainer or educator with administrative authority and responsibility.
        "general public": "other",
        # The public at large.
        "mentor": "counsellor",
        # Someone who advises, trains, supports, and/or guides.
        "peer tutor": ["learner", "other"],
        # The peer learner serving as tutor of another learner.
        "professional": "other",
        # Someone already practicing a profession; an industry partner, or professional development trainer.
        "student": "learner",
    }
    # see: http://w3id.org/kim/schulfaecher/ (https://github.com/dini-ag-kim/schulfaecher)
    KIM_TO_OEH_DISCIPLINE_MAPPING = {
        "s1000": "20003",  # Alt-Griechisch
        "s1040": "46014",  # Astronomie
        "s1001": "080",  # Biologie
        "s1002": "100",  # Chemie
        "s1003": "20041",  # Chinesisch
        "s1004": "12002",  # Darstellendes Spiel
        "s1005": "120",  # Deutsch
        "s1006": "28002",  # Deutsch als Zweitsprache
        # "s1041": "",  # ToDo: "Deutsche Gebärdensprache" doesn't exist in our 'discipline'-vocab yet
        "s1007": "20001",  # Englisch
        "s1044": "04006",  # Ernährung → "Ernährung und Hauswirtschaft"
        "s1045": "440",  # Erziehungswissenschaften → Pädagogik (altLabel: "Erziehungswissenschaften")
        "s1008": "160",  # Ethik
        "s1009": "20002",  # Französisch
        "s1010": "220",  # Geografie
        "s1011": "240",  # Geschichte
        "s1012": "260",  # Gesundheit
        "s1047": "50001",  # Hauswirtschaft
        # "s1034": "",  # ToDo: "Hebräisch" doesn't exist in our 'discipline'-vocab yet
        "s1013": "320",  # Informatik
        "s1014": "20004",  # Italienisch
        # "s1035": "",  # ToDo: "Japanisch" doesn't exist in our 'discipline'-vocab yet
        "s1015": "060",  # Kunst
        "s1016": "20005",  # Latein
        "s1017": "380",  # Mathematik
        "s1046": "900",  # Medienbildung
        "s1019": "04003",  # MINT
        "s1020": "420",  # Musik
        # "s1036": "",  # ToDo: "Neu-Griechisch" doesn't exist in our 'discipline'-vocab yet
        "s1021": "450",  # Philosophie
        "s1022": "460",  # Physik
        "s1023": "480",  # Politik
        # "s1037": "",  # ToDo: "Polnisch" doesn't exist in our 'discipline'-vocab yet
        # "s1038": "",  # ToDo: "Portugiesisch" doesn't exist in our 'discipline'-vocab yet
        # "s1043": "",  # ToDo: "Psychologie" doesn't exist in our 'discipline'-vocab yet
        "s1024": "520",  # Religionslehre (evangelisch) → Religionslehre
        "s1025": "520",  # Religionslehre (islamisch) → Religionslehre
        "s1026": "520",  # Religionslehre (katholisch) → Religionslehre
        "s1027": "20006",  # Russisch
        "s1028": "28010",  # Sachunterricht
        "s1029": "560",  # Sexualerziehung
        "s1039": "20009",  # Sorbisch
        "s1030": "20007",  # Spanisch
        "s1031": "600",  # Sport
        "s1032": "20008",  # Türkisch
        "s1033": "700",  # Wirtschaftskunde
        "s1042": "48005",  # Gesellschaftswissenschaften → Gesellschaftskunde
    }
    # ToDo: refactor this crawler-specific mapping into a separate (and testable) helper utility asap
    # (this mapping table is a temporary workaround until a mapping-utility for DINI AG KIM Schulfächer URLs
    # has been implemented)

    def __init__(self, **kw):
        LomBase.__init__(self, **kw)
        self.decide_crawl_mode()
        self.graphql_items = self.fetch_all_graphql_pages()

    def decide_crawl_mode(self):
        """
        Check the '.env'-file for a 'SERLO_MODIFIED_AFTER'-variable and set the GraphQL API parameter 'modifiedAfter'
        accordingly.

        *   Default behaviour: The Serlo GraphQL API is crawled COMPLETELY. (The 'modifiedAfter'-parameter will be
            omitted in this case.)
        *   Optional behaviour: If the 'SERLO_MODIFIED_AFTER'-variable is set in your .env file (e.g. "2023-07-01"),
            Serlo's GraphQL API shall be queried ONLY for items that have been modified (by Serlo) since that date.

        You can use this '.env'-setting to crawl Serlo more efficiently: Specify a date and only receive items that were
        modified since <date of the last crawling process>.
        """
        graphql_instance_param: str = env.get(key="SERLO_INSTANCE", allow_null=True, default="de")
        if graphql_instance_param:
            logging.info(
                f"INIT: '.env'-Setting 'SERLO_INSTANCE': '{graphql_instance_param}' detected. "
                f"Limiting query to a single language selection. (You should always see this message. "
                f"This setting defaults to: 'de')"
            )
            self.GRAPHQL_INSTANCE_PARAMETER = graphql_instance_param
        graphql_modified_after_param: str = env.get(key="SERLO_MODIFIED_AFTER", allow_null=True, default=None)
        if graphql_modified_after_param:
            logging.info(
                f"INIT: '.env'-Setting 'SERLO_MODIFIED_AFTER': '{graphql_modified_after_param}' detected. "
                f"Trying to parse the date string..."
            )
            # the 'modifiedAfter'-parameter must be an ISO-formatted string WITH timezone information, e.g.:
            # "2023-07-01T00:00:00+00:00". To make future crawler maintenance a bit easier, we use scrapy's dateparser
            # module, so you can control crawls by setting the '.env'-parameter:
            # "SERLO_MODIFIED_AFTER"-Parameter "2023-07-01" and it will convert the string accordingly
            date_parsed = dateparser.parse(
                date_string=graphql_modified_after_param,
                settings={"TIMEZONE": "Europe/Berlin", "RETURN_AS_TIMEZONE_AWARE": True},
            )
            if date_parsed:
                date_parsed_iso = date_parsed.isoformat()
                logging.info(
                    f"INIT: SUCCESS - serlo_spider will ONLY request GraphQL items that were modified (by Serlo) after "
                    f"'{date_parsed_iso}'."
                )
                self.GRAPHQL_MODIFIED_AFTER_PARAMETER = date_parsed_iso
        else:
            logging.info("INIT: Starting COMPLETE Serlo crawl (WITHOUT any GraphQL API 'modifiedAfter'-parameter).")

    def fetch_all_graphql_pages(self):
        all_resources = list()
        pagination_string: str = ""
        has_next_page = True
        while has_next_page is True:
            current_page = self.query_graphql_page(pagination_string=pagination_string)["data"]["metadata"]["resources"]
            all_resources += current_page["nodes"]
            has_next_page = current_page["pageInfo"]["hasNextPage"]
            if has_next_page:
                pagination_string = current_page["pageInfo"]["endCursor"]
            else:
                break
        return all_resources

    def query_graphql_page(self, amount_of_nodes: int = 500, pagination_string: str = None) -> dict:
        amount_of_nodes = amount_of_nodes
        # specifies the amount of nodes that shall be requested (per page) from the GraphQL API
        # (default: 100 // max: 500)
        pagination_string = pagination_string
        modified_after: str = ""
        if self.GRAPHQL_MODIFIED_AFTER_PARAMETER:
            # the 'modifiedAfter'-parameter can be used to only crawl items that have been modified since the last time
            # the crawler ran.
            # see: https://github.com/serlo/documentation/wiki/Metadata-API#tips-for-api-consumer
            modified_after: str = self.GRAPHQL_MODIFIED_AFTER_PARAMETER
            if modified_after:
                # we only add the (optional) 'modifiedAfter'-parameter if the .env-Setting was recognized. By default,
                # the string will stay empty.
                modified_after: str = f', modifiedAfter: "{modified_after}"'
        instance_parameter: str = ""
        if self.GRAPHQL_INSTANCE_PARAMETER:
            # Serlo allows us to limit the query results to a specific serlo instance (the currently 6 possible language
            # codes can be seen here:
            # https://github.com/serlo/documentation/wiki/Metadata-API#understanding-the-request-payload-and-pagination
            instance_value: str = self.GRAPHQL_INSTANCE_PARAMETER
            if instance_value and instance_value in ["de", "en", "es", "ta", "hi", "fr"]:
                instance_parameter: str = f"instance: {instance_value}"
        graphql_metadata_query_body = {
            "query": f"""
                        query {{
                            metadata {{
                                resources(
                                    first: {amount_of_nodes}
                                    after: "{pagination_string}"{modified_after}{instance_parameter}
                                    ){{
                                        nodes
                                        pageInfo {{
                                            hasNextPage
                                            endCursor
                                            }}
                                }}
                            }}
                        }}
                        """
        }
        request = requests.post(
            url=self.API_URL, headers={"Content-Type": "application/json"}, json=graphql_metadata_query_body
        )
        return request.json()

    def start_requests(self):
        for graphql_item in self.graphql_items:
            item_url = graphql_item["id"]
            # ToDo: there is room for further optimization if we do the drop_item check here
            yield scrapy.Request(url=item_url, callback=self.parse, cb_kwargs={"graphql_item": graphql_item})

    def getId(self, response=None, graphql_json=None) -> str:
        # The actual URL of a learning material is dynamic and can change at any given time
        # (e.g. when the title gets changed by a serlo editor/contributor),
        # therefore we use the "id"-field and its identifier value
        # e.g.:     "id": "https://serlo.org/2097"
        #           "value": "2097"
        graphql_json: dict = graphql_json
        try:
            identifier_value: int | str | None = graphql_json["identifier"]["value"]
            if identifier_value:
                if isinstance(identifier_value, int):
                    identifier_value = str(identifier_value)
                    return identifier_value
                if isinstance(identifier_value, str):
                    return identifier_value
            else:
                return response.url
        except KeyError:
            logging.debug(
                f"getId: Could not retrieve Serlo identifier from 'graphql_json'-dict. Falling back to 'response.url'"
            )

    def getHash(self, response=None, graphql_json=None) -> str:
        graphql_json: dict = graphql_json
        try:
            date_modified: str = graphql_json["dateModified"]
            if date_modified:
                hash_combined = f"{date_modified}{self.version}"
                return hash_combined
            else:
                return f"{datetime.datetime.now().isoformat()}{self.version}"
        except KeyError:
            logging.debug(
                f"getHash: Could not retrieve Serlo 'dateModified' from 'graphql_json'-dict. Falling back to "
                f"'datetime.now()'-value for 'hash'."
            )

    def hasChanged(self, response=None, **kwargs) -> bool:
        try:
            graphql_json: dict = kwargs["kwargs"]["graphql_json"]
            identifier: str = self.getId(response, graphql_json)
            hash_str: str = self.getHash(response, graphql_json)
            uuid_str: str = self.getUUID(response)
            # ToDo - further optimization: if we want to save even more time, we could use graphql_json as a parameter
            #  in the 'getUUID'-method (needs to be overwritten) and check if the item should be dropped in the
            #  start_requests()-method before yielding the scrapy.Request
        except KeyError as ke:
            logging.debug(f"hasChanged(): Could not retrieve 'graphql_json' from kwargs.")
            raise ke
        if self.forceUpdate:
            return True
        if self.uuid:
            if uuid_str == self.uuid:
                logging.info(f"matching requested id: {self.uuid}")
                return True
            return False
        if self.remoteId:
            if identifier == self.remoteId:
                logging.info(f"matching requested id: {self.remoteId}")
                return True
            return False
        db = EduSharing().find_item(identifier, self)
        changed = db is None or db[1] != hash_str
        if not changed:
            logging.info(f"Item {identifier} (uuid: {db[0]}) has not changed")
        return changed

    def check_if_item_should_be_dropped(self, response, graphql_json: dict):
        """
        Check if item needs to be dropped (before making any further HTTP Requests).
        This could happen for reasons like "the hash has not changed" (= the object has not changed since the last
        crawl) or if the 'shouldImport'-attribute was set to False.

        :param response: scrapy.http.Response
        :param graphql_json: metadata dictionary of an item (from Serlo's GraphQL API)
        :return: True if item needs to be dropped. Defaults to: False
        """
        drop_item_flag: bool = False  # by default, we assume that all items should be crawled
        identifier: str = self.getId(response, graphql_json)
        hash_str: str = self.getHash(response, graphql_json)
        if self.shouldImport(response) is False:
            logging.debug(f"Skipping entry {identifier} because shouldImport() returned false")
            drop_item_flag = True
            return drop_item_flag
        if identifier is not None and hash_str is not None:
            if not self.hasChanged(response, kwargs={"graphql_json": graphql_json}):
                drop_item_flag = True
            return drop_item_flag
        if "serlo.org/community/" in response.url:
            # As requested by Team4/management on 2023-08-11: items from Serlo's "Blog-Archiv"
            # (https://de.serlo.org/community/111255/blog-archiv) should not be crawled.
            # We can use the resolved URL in 'response.url' for this purpose (minus the language-specific subdomain)
            logging.info(f"Dropping URL {response.url} due to team4 decision on 2023-08-11.")
            drop_item_flag = True
            return drop_item_flag

    async def parse(self, response, **kwargs):
        graphql_json: dict = kwargs.get("graphql_item")

        drop_item_flag = self.check_if_item_should_be_dropped(response, graphql_json)
        if drop_item_flag is True:
            return

        json_ld = response.xpath('//*[@type="application/ld+json"]/text()').get()
        json_ld = json.loads(json_ld)

        playwright_dict = await WebTools.getUrlData(response.url, WebEngine.Playwright)
        html_body = playwright_dict.get("html")
        screenshot_bytes = playwright_dict.get("screenshot_bytes")
        html_text = playwright_dict.get("text")
        selector_playwright: scrapy.Selector = scrapy.Selector(text=html_body)

        robot_meta_tags: list[str] = selector_playwright.xpath("//meta[@name='robots']/@content").getall()
        if robot_meta_tags:
            # Serlo makes use of the Google's Robot Meta Tag Specification
            # (see: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag)
            # Serlo Items that are marked for deletion ("Papierkorb"-Items) carry Robot Meta Tags in the HTML Header,
            # therefore we need to respect these tags and skip the items!
            if "noindex" in robot_meta_tags or "none" in robot_meta_tags:
                logging.info(
                    f"Robot Meta Tag {robot_meta_tags} identified. Robot Meta Tags 'noindex' or 'none' should "
                    f"be skipped by the crawler. Dropping item {response.url} ."
                )
                return

        base = BaseItemLoader()

        og_image: str = selector_playwright.xpath('//meta[@property="og:image"]/@content').get()
        if "image" in graphql_json and graphql_json["image"]:
            # Serlo API v1.2.0 provides an 'image'-property that serves a single URL (type: String)
            base.add_value("thumbnail", graphql_json["image"])
        elif og_image:
            # if an OpenGraph image property is available, we'll use that as our thumbnail URL, e.g.:
            # <meta property="og:image" name="image" content="https://de.serlo.org/_assets/img/meta/mathe.png">
            base.add_value("thumbnail", og_image)
        else:
            base.add_value("screenshot_bytes", screenshot_bytes)
        base.add_value("sourceId", self.getId(response, graphql_json=graphql_json))
        base.add_value("hash", self.getHash(response, graphql_json=graphql_json))
        base.add_value("lastModified", graphql_json["dateModified"])
        if "publisher" in json_ld:
            base.add_value("publisher", json_ld["publisher"])

        lom = LomBaseItemloader()

        general = LomGeneralItemloader()
        # # TODO: fill LOM "general"-keys with values for
        # #  - keyword                        required
        # #  - coverage                       optional
        # #  - structure                      optional
        # #  - aggregationLevel               optional
        general.add_value("identifier", graphql_json["id"])
        title_1st_try: str = graphql_json["name"]
        title_fallback: str = str()
        # not all materials carry a title in the GraphQL API, therefore we're trying to grab a valid title from
        # different sources (GraphQL > (DOM) json_ld > (DOM) header > (DOM) last breadcrumb label)
        if title_1st_try:
            general.add_value("title", title_1st_try)
        elif not title_1st_try:
            title_2nd_try = graphql_json["headline"]
            title_3rd_try = json_ld["name"]
            if title_2nd_try:
                general.add_value("title", title_2nd_try)
                title_fallback = title_2nd_try
            elif title_3rd_try:
                general.add_value("title", title_3rd_try)
                title_fallback = title_3rd_try
            if not title_1st_try and not title_2nd_try and not title_3rd_try:
                title_from_header = response.xpath('//meta[@property="og:title"]/@content').get()
                if title_from_header:
                    general.add_value("title", title_from_header)
                    title_fallback = title_from_header
            if "lernen mit Serlo!" in title_fallback:
                # We assume that Strings ending with "lernen mit Serlo!" are placeholders
                # e.g. "Mathe Aufgabe - lernen mit Serlo!" occurs over 2700 times as a title
                # therefore we try to grab the last breadcrumb label and use it as a more specific fallback
                page_data_json: str = response.xpath("//script[@id='__NEXT_DATA__']/text()").get()
                if page_data_json:
                    page_data_json: dict = json.loads(page_data_json)
                    if page_data_json:
                        if "breadcrumbsData" in page_data_json["props"]["pageProps"]["pageData"]:
                            breadcrumbs: list = page_data_json["props"]["pageProps"]["pageData"]["breadcrumbsData"]
                            if breadcrumbs:
                                if "label" in breadcrumbs[-1]:
                                    title_breadcrumb_last_label: str = breadcrumbs[-1]["label"]
                                    if title_breadcrumb_last_label:
                                        general.replace_value("title", title_breadcrumb_last_label)
        # Not all GraphQL items have a description, but we need one (otherwise the item would get dropped since Serlo
        # provides no keywords either). That's why we try to grab the description from three different sources:
        # (GraphQL > JSON-LD > DOM header)
        description_1st_try = str()
        description_2nd_try = str()
        if "description" in graphql_json:
            description_1st_try: str = graphql_json["description"]
            # as of Serlo's Metadata API v1.0.0:
            # - the "description"-property is only available where a description exists
            # see: https://github.com/serlo/documentation/wiki/Metadata-API#changes-to-entity-descriptions
            if description_1st_try:
                general.add_value("description", description_1st_try)
        if not description_1st_try and "description" in json_ld:
            # some json_ld containers don't have a description either
            description_2nd_try: str = json_ld["description"]
            if description_2nd_try:
                general.add_value("description", description_2nd_try)
        elif not description_1st_try and not description_2nd_try:
            description_from_header: str = response.xpath('//meta[@name="description"]/@content').get()
            if description_from_header:
                general.add_value("description", description_from_header)
        in_language: list = graphql_json["inLanguage"]
        # Serlo provides a list of 2-char-language-codes within its "inLanguage"-property
        general.add_value("language", in_language)
        # ToDo: keywords would be extremely useful, but aren't supplied by neither the API, JSON_LD nor the HTML header
        lom.add_value("general", general.load_item())

        technical = LomTechnicalItemLoader()
        # # TODO: fill "technical"-keys with values for
        # #  - size                           optional
        # #  - requirement                    optional
        # #  - installationRemarks            optional
        # #  - otherPlatformRequirements      optional
        # #  - duration                       optional (only applies to audiovisual content like videos/podcasts)
        if "id" in graphql_json:
            graphql_id: str = graphql_json["id"]  # e.g.: "https://serlo.org/1495"
            technical.add_value("location", graphql_id)
        else:
            # This case should never occur. The resolved URLs will always be longer and less stable than the shortened
            # URI vom the GraphQL 'id'-property above.
            technical.add_value("location", response.url)

        lom.add_value("technical", technical.load_item())

        self.get_lifecycle_authors(graphql_json=graphql_json, lom_base_item_loader=lom)
        # Serlo's new "maintainer"-property holds the identical information as the "creator.affiliaton"-property.

        self.get_lifecycle_metadata_providers(graphql_json=graphql_json, lom_base_item_loader=lom)

        self.get_lifecycle_publishers(graphql_json=graphql_json, lom_base_item_loader=lom)

        educational = LomEducationalItemLoader()
        # # TODO: fill "educational"-keys with values for
        # #  - description                    recommended (= "Comments on how this learning object is to be used")
        # #  - interactivityType              optional
        # #  - interactivityLevel             optional
        # #  - semanticDensity                optional
        # #  - typicalAgeRange                optional
        # #  - difficulty                     optional
        # #  - typicalLearningTime            optional
        educational.add_value("language", in_language)

        lom.add_value("educational", educational.load_item())

        # classification = LomClassificationItemLoader()
        # # TODO: fill "classification"-keys with values for
        # #  - cost                           optional
        # #  - purpose                        optional
        # #  - taxonPath                      optional
        # #  - description                    optional
        # #  - keyword                        optional
        # lom.add_value('classification', classification.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)
        # # for possible values, either consult https://vocabs.openeduhub.de
        # # or take a look at https://github.com/openeduhub/oeh-metadata-vocabs
        # # TODO: fill "valuespaces"-keys with values for
        # #  - conditionsOfAccess             recommended
        # #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/conditionsOfAccess.ttl)
        # #  - educationalContext             optional
        # #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/educationalContext.ttl)
        # #  - accessibilitySummary           optional
        # #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/accessibilitySummary.ttl)
        # #  - dataProtectionConformity       optional
        # #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/dataProtectionConformity.ttl)

        if "audience" in json_ld:
            # mapping educationalAudienceRole to IntendedEndUserRole here
            intended_end_user_roles = list()
            for audience_item in json_ld["audience"]:
                # as of 2024-04-23 the 'audience'-object within JSON-LD looks like this:
                # "audience": [
                #         {
                #             "id": "http://purl.org/dcx/lrmi-vocabs/educationalAudienceRole/student",
                #             "audienceType": "student",
                #             "type": "Audience"
                #         }
                #     ],
                if "id" in audience_item:
                    # points towards a vocab URL, e.g. "http://purl.org/dcx/lrmi-vocabs/educationalAudienceRole/student"
                    pass
                if "audienceType" in audience_item:
                    edu_audience_role = audience_item["audienceType"]
                    if edu_audience_role == "professional":
                        vs.add_value("educationalContext", ["Further Education", "vocational education"])
                    if edu_audience_role in self.EDU_AUDIENCE_ROLE_MAPPING.keys():
                        edu_audience_role = self.EDU_AUDIENCE_ROLE_MAPPING.get(edu_audience_role)
                    intended_end_user_roles.append(edu_audience_role)
            if intended_end_user_roles:
                vs.add_value("intendedEndUserRole", intended_end_user_roles)
                # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/intendedEndUserRole.ttl)

        disciplines_set: set = set()
        if "about" in graphql_json:
            # The graphql_json["about"] field carries more precise information, but uses the DINI KIM Schulfaecher
            #  vocabulary. A non-crawler-specific mapper/resolver will be necessary in the long run. Example:
            # {
            # 		"about": [
            # 			{
            # 				"type": "Concept",
            # 				"id": "http://w3id.org/kim/schulfaecher/s1017",
            # 				"inScheme": {
            # 					"id": "http://w3id.org/kim/schulfaecher/"
            # 				}
            # 			}
            about_list: list[dict] = graphql_json["about"]
            if type(about_list) is list and about_list:
                for about_item in about_list:
                    if "id" in about_item:
                        about_id: str = about_item["id"]
                        if "w3id.org/kim/schulfaecher/" in about_id:
                            about_id_key: str = about_id.split("/")[-1]
                            if about_id_key and about_id_key in self.KIM_TO_OEH_DISCIPLINE_MAPPING:
                                discipline_mapped: str = self.KIM_TO_OEH_DISCIPLINE_MAPPING.get(about_id_key)
                                disciplines_set.add(discipline_mapped)
                            elif about_id_key:
                                logging.debug(
                                    f"Serlo 'about.id'-value {about_id_key} could not be mapped to any OEH "
                                    f"'discipline'. (Please check if all mapping-tables are still up to date.)"
                                )
        elif "about" in json_ld and len(json_ld["about"]) != 0:
            # not every json_ld-container has an "about"-key, e.g.: https://de.serlo.org/5343/5343
            # we need to make sure that we only try to access "about" if it's actually available
            # making sure that we only try to look for a discipline if the "about"-list actually has list items
            disciplines = list()
            json_ld_about: list[dict] = json_ld["about"]
            for about_item in json_ld_about:
                # as of 2024-08-16 the "about"-property in a JSON-LD currently looks like this:
                # "about": [
                #     {
                #       "id": "https://serlo.org/5",
                #       "name": "Mathematik",
                #       "type": "Thing"
                #     }
                if "id" in about_item:
                    json_ld_about_id: str = about_item["id"]
                    pass
                if "name" in about_item:
                    json_ld_about_name: str = about_item["name"]
                    if json_ld_about_name and isinstance(json_ld_about_name, str):
                        disciplines.append(json_ld_about_name)
                elif "prefLabel" in about_item:
                    # ToDo: this case should no longer happen as the "about" structure changed
                    if "de" in about_item["prefLabel"]:
                        discipline_de: str = about_item["prefLabel"]["de"]
                        disciplines.append(discipline_de)
                    elif "en" in about_item["prefLabel"]:
                        discipline_en: str = about_item["prefLabel"]["en"]
                        disciplines.append(discipline_en)
            if len(disciplines) > 0:
                vs.add_value("discipline", disciplines)
                # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/discipline.ttl)
            # if the json_ld doesn't hold a discipline value for us, we'll try to grab the discipline from the url path
        # ToDo: these URL-fallbacks might be obsolete now. Remove them in crawler v0.3.1+ after further debugging
        if "/mathe/" in response.url:
            disciplines_set.add("380")  # Mathematik
        if "/biologie/" in response.url:
            disciplines_set.add("080")  # Biologie
        if "/chemie/" in response.url:
            disciplines_set.add("100")  # Chemie
        if "/nachhaltigkeit/" in response.url:
            disciplines_set.add("64018")  # Nachhaltigkeit
        if "/informatik/" in response.url:
            disciplines_set.add("320")  # Informatik
        if "/deutsch-als-fremdsprache/" in response.url:
            disciplines_set.add("28002")  # DaZ
        if disciplines_set:
            vs.add_value("discipline", list(disciplines_set))
        vs.add_value("containsAdvertisement", "No")
        # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/containsAdvertisement.ttl)
        # serlo doesn't want to distract learners with ads, therefore we can set it by default to 'no'
        if graphql_json["isAccessibleForFree"] is True:
            # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/price.ttl)
            vs.add_value("price", "no")
        elif graphql_json["isAccessibleForFree"] is False:
            # only set the price to "kostenpflichtig" if it's explicitly stated, otherwise we'll leave it empty
            vs.add_value("price", "yes")
        if graphql_json["learningResourceType"]:
            # Serlo is using the learningResourceType vocabulary (as specified in the AMB standard), see:
            # https://github.com/serlo/documentation/wiki/Metadata-API#changes-to-the-learningresourcetype-property
            learning_resource_types: list[dict] = graphql_json["learningResourceType"]
            lrts_new: set[str] = set()
            lrts_old: set[str] = set()
            for lrt_item in learning_resource_types:
                # we're checking for 'new_lrt'-values first and use the old (broader) LRT only as fallback
                if "id" in lrt_item:
                    learning_resource_type_url: str = lrt_item["id"]
                    if "/openeduhub/vocabs/new_lrt/" in learning_resource_type_url:
                        # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/new_lrt.ttl)
                        new_lrt_key: str = learning_resource_type_url.split("/")[-1]
                        if new_lrt_key:
                            lrts_new.add(new_lrt_key)
                    if "/openeduhub/vocabs/learningResourceType/" in learning_resource_type_url:
                        # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/learningResourceType.ttl)
                        lrt_key: str = learning_resource_type_url.split("/")[-1]
                        if lrt_key:
                            lrts_old.add(lrt_key)
            if lrts_new:
                # OER Sommercamp 2023: Kulla and Romy defined precise mappings for our 'new_lrt'-vocab. These will
                # always be more precise than the old (broader) LRT values. If the API provided 'new_lrt'-values, we'll
                # ONLY be using these values.
                lrts_new_list: list[str] = list(lrts_new)
                if lrts_new_list:
                    vs.add_value("new_lrt", lrts_new_list)
            elif lrts_old:
                # OER Sommercamp 2023: For now, the Serlo API provides both the 'learningResourceType' and 'new_lrt'
                # values. We'll only use the old LRT values as a fallback if no 'new_lrt'-values were collected.
                lrts_old_list: list[str] = list(lrts_old)
                if lrts_old_list:
                    vs.add_value("learningResourceType", lrts_old)

        base.add_value("valuespaces", vs.load_item())

        lic = LicenseItemLoader()
        if "license" in graphql_json:
            license_url: str = graphql_json["license"]["id"]
            if license_url:
                license_mapper = LicenseMapper()
                license_url_mapped = license_mapper.get_license_url(license_string=license_url)
                if license_url_mapped:
                    lic.add_value("url", license_url_mapped)

        base.add_value("lom", lom.load_item())
        base.add_value("license", lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader = ResponseItemLoader()
        response_loader.replace_value("headers", response.headers)
        response_loader.replace_value("html", html_body)
        response_loader.replace_value("status", response.status)
        response_loader.replace_value("text", html_text)
        response_loader.replace_value("url", self.getUri(response))
        base.add_value("response", response_loader.load_item())

        yield base.load_item()

    @staticmethod
    def get_lifecycle_authors(graphql_json: dict, lom_base_item_loader: LomBaseItemloader):
        """Retrieve author metadata from GraphQL 'creator'-items and store it in the provided LomBaseItemLoader."""
        if "creator" in graphql_json:
            creators: list[dict] = graphql_json["creator"]
            for creator in creators:
                # a typical "creator" item currently (2023-07-11) looks like this:
                # {
                # 			"type": "Person",
                # 			"id": "https://serlo.org/49129",
                # 			"name": "testaccount",
                # 			"affiliation": {
                # 				"id": "https://serlo.org/organization",
                # 				"name": "Serlo Education e.V.",
                # 				"type": "Organization"
                # 			}
                # While the "affiliation" needs to be handled within the lifecycle_publisher item, we can use the 'name'
                # and 'id'-field for author information. (the 'id'-field leads to the user-profile on Serlo)
                creator_type: str = creator["type"]
                if creator_type and creator_type == "Person":
                    # this is usually the case for Serlo authors
                    lifecycle_author = LomLifecycleItemloader()
                    lifecycle_author.add_value("role", "author")
                    if "name" in creator:
                        # the "name"-property will hold a Serlo username
                        lifecycle_author.add_value("firstName", creator["name"])
                    if "id" in creator:
                        # the "id"-property will point towards a serlo profile
                        lifecycle_author.add_value("url", creator["id"])
                    lom_base_item_loader.add_value("lifecycle", lifecycle_author.load_item())
                elif creator_type == "Organization":
                    # Prior to Serlo's API v1.2.0 there were some edge-cases in Serlo's "license"-property, which
                    # provided URLs to a creator's website in the wrong Serlo API property ("license").
                    # Those (previous) edge-cases are now provided as a "creator"-object of type "Organization" and
                    # typically look like this:
                    # {
                    # 		"type": "Organization",
                    # 		"id": "http://www.strobl-f.de/",
                    # 		"name": "http://www.strobl-f.de/"
                    # 	},
                    lifecycle_org = LomLifecycleItemloader()
                    lifecycle_org.add_value("role", "author")
                    if "name" in creator:
                        lifecycle_org.add_value("organization", creator["name"])
                    if "id" in creator:
                        lifecycle_org.add_value("url", creator["id"])
                    lom_base_item_loader.add_value("lifecycle", lifecycle_org.load_item())

    @staticmethod
    def get_lifecycle_metadata_providers(graphql_json, lom_base_item_loader):
        """
        Retrieve metadata-provider metadata from GraphQL 'mainEntityOfPage'-items and store it in the provided
        LomBaseItemLoader.
        """
        if "mainEntityOfPage" in graphql_json:
            maeop_list: list[dict] = graphql_json["mainEntityOfPage"]
            for maeop_item in maeop_list:
                # for future reference - a single 'mainEntityOfpage'-item might look like this:
                # {
                # 			"dateCreated": "2023-07-11T15:24:14.042782898+00:00",
                # 			"dateModified": "2023-07-11T15:24:14.042782898+00:00",
                # 			"id": "https://serlo.org/metadata",
                # 			"provider": {
                # 				"id": "https://serlo.org/organization",
                # 				"name": "Serlo Education e.V.",
                # 				"type": "Organization"
                # 			}
                # 		}
                lifecycle_metadata_provider = LomLifecycleItemloader()
                lifecycle_metadata_provider.add_value("role", "metadata_provider")
                if "dateCreated" in maeop_item:
                    date_created: str = maeop_item["dateCreated"]
                    if date_created:
                        lifecycle_metadata_provider.add_value("date", date_created)
                elif "dateModified" in maeop_item:
                    date_modified: str = maeop_item["dateModified"]
                    if date_modified:
                        lifecycle_metadata_provider.add_value("date", date_modified)
                if "id" in maeop_item:
                    maeop_item_url: str = maeop_item["id"]
                    if maeop_item_url:
                        lifecycle_metadata_provider.add_value("url", maeop_item_url)
                if "provider" in maeop_item:
                    provider_dict: dict = maeop_item["provider"]
                    if "id" in provider_dict:
                        provider_url: str = provider_dict["id"]
                        if provider_url:
                            lifecycle_metadata_provider.add_value("url", provider_url)
                    if "name" in provider_dict:
                        provider_name: str = provider_dict["name"]
                        lifecycle_metadata_provider.add_value("organization", provider_name)
                lom_base_item_loader.add_value("lifecycle", lifecycle_metadata_provider.load_item())

    @staticmethod
    def get_lifecycle_publishers(graphql_json, lom_base_item_loader):
        """Retrieve publisher metadata from GraphQL 'publisher'-items and store it in the provided LomBaseItemLoader."""
        graphql_publishers: list[dict] = graphql_json["publisher"]
        if graphql_publishers:
            for publisher_dict in graphql_publishers:
                lifecycle_publisher = LomLifecycleItemloader()
                lifecycle_publisher.add_value("role", "publisher")
                if "name" in graphql_json["publisher"]:
                    publisher_name: str = publisher_dict["name"]
                    lifecycle_publisher.add_value("organization", publisher_name)
                if "id" in graphql_json["publisher"]:
                    publisher_url: str = publisher_dict["id"]
                    lifecycle_publisher.add_value("url", publisher_url)
                if "dateCreated" in graphql_json:
                    date_created: str = graphql_json["dateCreated"]
                    lifecycle_publisher.add_value("date", date_created)
                elif "dateModified" in graphql_json:
                    date_modified: str = graphql_json["dateModified"]
                    if date_modified:
                        lifecycle_publisher.add_value("date", date_modified)
                lom_base_item_loader.add_value("lifecycle", lifecycle_publisher.load_item())
