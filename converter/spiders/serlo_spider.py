import datetime
import json
import logging

import dateparser
import requests
import scrapy

import env
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
from ..util.license_mapper import LicenseMapper


class SerloSpider(scrapy.Spider, LomBase):
    name = "serlo_spider"
    friendlyName = "serlo_spider"
    # start_urls = ["https://de.serlo.org"]
    API_URL = "https://api.serlo.org/graphql"
    # for the API description, please check: https://lenabi.serlo.org/metadata-api
    version = "0.2.8"  # last update: 2023-07-11
    custom_settings = {
        # Using Playwright because of Splash-issues with thumbnails+text for Serlo
        "WEB_TOOLS": WebEngine.Playwright
    }
    GRAPHQL_MODIFIED_AFTER_PARAMETER: str = ""

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

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
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
                    f"'{date_parsed_iso}' ."
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
        graphql_metadata_query_body = {
            "query": f"""
                        query {{
                            metadata {{
                                resources(first: {amount_of_nodes}, after: "{pagination_string}"{modified_after}){{
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
            # logging.debug(f"{graphql_item}")
            item_url = graphql_item["id"]
            yield scrapy.Request(url=item_url, callback=self.parse, cb_kwargs={"graphql_item": graphql_item})

    def getId(self, response=None, graphql_json=None) -> str:
        # The actual URL of a learning material is dynamic and can change at any given time
        # (e.g. when the title gets changed by a serlo editor/contributor),
        # therefore we use the "id"-field and its identifier value
        # e.g.:     "id": "https://serlo.org/2097"
        #           "value": "2097"
        graphql_json: dict = graphql_json
        if "identifier" in graphql_json:
            if "value" in graphql_json["identifier"]:
                identifier_value = graphql_json["identifier"]["value"]
                if identifier_value:
                    return identifier_value
        else:
            return response.url

    def getHash(self, response=None, graphql_json=None) -> str:
        graphql_json: dict = graphql_json
        if "dateModified" in graphql_json:
            date_modified: str = graphql_json["dateModified"]
            if date_modified:
                hash_combined = f"{date_modified}{self.version}"
                return hash_combined
        else:
            return f"{datetime.datetime.now().isoformat()}{self.version}"

    def parse(self, response, **kwargs):
        graphql_json: dict = kwargs.get("graphql_item")

        json_ld = response.xpath('//*[@type="application/ld+json"]/text()').get()
        json_ld = json.loads(json_ld)

        playwright_dict = WebTools.getUrlData(response.url, WebEngine.Playwright)
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
                return None

        base = BaseItemLoader()
        og_image: str = selector_playwright.xpath('//meta[@property="og:image"]/@content').get()
        if og_image:
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
        technical.add_value("format", "text/html")  # e.g. if the learning object is a web-page
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

        base.add_value("lom", lom.load_item())

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
                edu_audience_role = audience_item["prefLabel"]["en"]
                if edu_audience_role == "professional":
                    vs.add_value("educationalContext", ["Further Education", "vocational education"])
                if edu_audience_role in self.EDU_AUDIENCE_ROLE_MAPPING.keys():
                    edu_audience_role = self.EDU_AUDIENCE_ROLE_MAPPING.get(edu_audience_role)
                intended_end_user_roles.append(edu_audience_role)
            vs.add_value("intendedEndUserRole", intended_end_user_roles)
            # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/intendedEndUserRole.ttl)

        # ToDo: the graphql_json["about"] field might carry more precise information, but uses the DINI KIM Schulfaecher
        #  vocabulary. A mapper/resolver might be necessary. Example:
        # {
        # 		"about": [
        # 			{
        # 				"type": "Concept",
        # 				"id": "http://w3id.org/kim/schulfaecher/s1017",
        # 				"inScheme": {
        # 					"id": "http://w3id.org/kim/schulfaecher/"
        # 				}
        # 			}
        if "about" in json_ld and len(json_ld["about"]) != 0:
            # not every json_ld-container has an "about"-key, e.g.: https://de.serlo.org/5343/5343
            # we need to make sure that we only try to access "about" if it's actually available
            # making sure that we only try to look for a discipline if the "about"-list actually has list items
            disciplines = list()
            for about_item in json_ld["about"]:
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
        else:
            if "/mathe/" in response.url:
                vs.add_value("discipline", "Mathematik")
            if "/biologie/" in response.url:
                vs.add_value("discipline", "Biologie")
            if "/chemie/" in response.url:
                vs.add_value("discipline", "Chemie")
            if "/nachhaltigkeit/" in response.url:
                vs.add_value("discipline", "Nachhaltigkeit")
            if "/informatik/" in response.url:
                vs.add_value("discipline", "Informatik")
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
            # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/learningResourceType.ttl)
            learning_resource_types: list[dict] = graphql_json["learningResourceType"]
            for lrt_item in learning_resource_types:
                if "id" in lrt_item:
                    learning_resource_type_url: str = lrt_item["id"]
                    if "/openeduhub/vocabs/learningResourceType/" in learning_resource_type_url:
                        lrt_key: str = learning_resource_type_url.split("/")[-1]
                        if lrt_key:
                            vs.add_value("learningResourceType", lrt_key)
                    else:
                        logging.debug(
                            f"Serlo 'learningResourceType' {learning_resource_type_url} was not recognized "
                            f"as part of the OpenEduHub 'learningResourceType' vocabulary. Please check the "
                            f"crawler or the vocab at oeh-metadata-vocabs/learningResourceType.ttl"
                        )

        base.add_value("valuespaces", vs.load_item())

        lic = LicenseItemLoader()
        if "license" in graphql_json:
            license_url: str = graphql_json["license"]["id"]
            if license_url:
                license_mapper = LicenseMapper()
                license_url_mapped = license_mapper.get_license_url(license_string=license_url)
                if license_url_mapped:
                    lic.add_value("url", license_url_mapped)
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
                lifecycle_author = LomLifecycleItemloader()
                lifecycle_author.add_value("role", "author")
                if "name" in creator:
                    # the "name"-property will hold a Serlo username
                    lifecycle_author.add_value("firstName", creator["name"])
                if "id" in creator:
                    # the "id"-property will point towards a serlo profile
                    lifecycle_author.add_value("url", creator["id"])
                lom_base_item_loader.add_value("lifecycle", lifecycle_author.load_item())

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
