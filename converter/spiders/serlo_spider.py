import datetime
import json

import requests
import scrapy
from scrapy import settings

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader
from converter.spiders.base_classes import LomBase
from converter.web_tools import WebEngine, WebTools


class SerloSpider(scrapy.Spider, LomBase):
    name = "serlo_spider"
    friendlyName = "serlo_spider"
    # start_urls = ["https://de.serlo.org"]
    API_URL = "https://api.serlo.org/graphql"
    # for the API description, please check: https://lenabi.serlo.org/metadata-api
    version = "0.2.4"  # last update: 2023-02-17
    custom_settings = settings.BaseSettings({
            # playwright cause of issues with thumbnails+text for serlo
            "WEB_TOOLS": WebEngine.Playwright
        }, 'spider')

    graphql_items = list()
    # Mapping from EducationalAudienceRole (LRMI) to IntendedEndUserRole(LOM), see:
    # https://www.dublincore.org/specifications/lrmi/concept_schemes/#educational-audience-role
    # https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/intendedEndUserRole.ttl
    EDU_AUDIENCE_ROLE_MAPPING = {
        "administrator": ["manager", "counsellor"],
        # A trainer or educator with administrative authority and responsibility.
        "general public": "other",
        # The public at large.
        "mentor": "author",
        # Someone who advises, trains, supports, and/or guides.
        "peer tutor": ["learner", "other"],
        # The peer learner serving as tutor of another learner.
        "professional": "other",
        # Someone already practicing a profession; an industry partner, or professional development trainer.
        "student": "learner",
        # "parent": "parent",  # no mapping needed
        # "teacher": "teacher"  # no mapping needed
    }

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.graphql_items = self.fetch_all_graphql_pages()
        # logging.debug(f"Gathered {len(self.graphql_items)} items from the GraphQL API")

    def fetch_all_graphql_pages(self):
        all_entities = list()
        pagination_string: str = ""
        has_next_page = True
        while has_next_page is True:
            current_page = self.query_graphql_page(pagination_string=pagination_string)["data"]["metadata"]["entities"]
            all_entities += current_page["nodes"]
            has_next_page = current_page["pageInfo"]["hasNextPage"]
            if has_next_page:
                pagination_string = current_page["pageInfo"]["endCursor"]
            else:
                break
        return all_entities

    def query_graphql_page(self, amount_of_nodes: int = 500, pagination_string: str = None) -> dict:
        amount_of_nodes = amount_of_nodes
        # specifies the amount of nodes that shall be requested (per page) from the GraphQL API
        # (default: 100 // max: 500)
        pagination_string = pagination_string
        graphql_metadata_query_body = {
            "query": f"""
                        query {{
                            metadata {{
                                entities(first: {amount_of_nodes}, after: "{pagination_string}"){{
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
            url=self.API_URL,
            headers={
                "Content-Type": "application/json"
            },
            json=graphql_metadata_query_body
        )
        return request.json()

    def start_requests(self):
        for graphql_item in self.graphql_items:
            # logging.debug(f"{graphql_item}")
            item_url = graphql_item["id"]
            yield scrapy.Request(url=item_url,
                                 callback=self.parse,
                                 cb_kwargs={
                                     "graphql_item": graphql_item
                                 }
                                 )

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

        base = BaseItemLoader()
        # # ALL possible keys for the different Item and ItemLoader-classes can be found inside converter/items.py
        # # TODO: fill "base"-keys with values for
        # #  - thumbnail          recommended
        base.add_value('screenshot_bytes', screenshot_bytes)
        base.add_value('sourceId', self.getId(response, graphql_json=graphql_json))
        base.add_value('hash', self.getHash(response, graphql_json=graphql_json))
        base.add_value('lastModified', graphql_json["dateModified"])
        # thumbnail_url: str = "This string should hold the thumbnail URL"
        # base.add_value('thumbnail', thumbnail_url)
        if "publisher" in json_ld:
            base.add_value('publisher', json_ld["publisher"])

        lom = LomBaseItemloader()

        general = LomGeneralItemloader()
        # # TODO: fill LOM "general"-keys with values for
        # #  - keyword                        required
        # #  - coverage                       optional
        # #  - structure                      optional
        # #  - aggregationLevel               optional
        general.add_value('identifier', graphql_json["id"])
        title_1st_try: str = graphql_json["headline"]
        # not all materials carry a title in the GraphQL API, therefore we're trying to grab a valid title from
        # different sources (GraphQL > json_ld > header)
        if title_1st_try:
            general.add_value('title', title_1st_try)
        elif not title_1st_try:
            title_2nd_try = json_ld["name"]
            if title_2nd_try:
                general.add_value('title', title_2nd_try)
            if not title_1st_try and not title_2nd_try:
                title_from_header = response.xpath('//meta[@property="og:title"]/@content').get()
                if title_from_header:
                    general.add_value('title', title_from_header)
        # not all GraphQL entries have a description either, therefore we try to grab that from different sources
        # (GraphQL > JSON-LD > DOM header)
        description_1st_try = str()
        description_2nd_try = str()
        if "description" in graphql_json:
            description_1st_try: str = graphql_json["description"]
            if description_1st_try:
                general.add_value('description', description_1st_try)
        if not description_1st_try and "description" in json_ld:
            # some json_ld containers don't have a description either
            description_2nd_try: str = json_ld["description"]
            if description_2nd_try:
                general.add_value('description', description_2nd_try)
        elif not description_1st_try and not description_2nd_try:
            description_from_header: str = response.xpath('//meta[@name="description"]/@content').get()
            if description_from_header:
                general.add_value('description', description_from_header)
        in_language: list = graphql_json["inLanguage"]
        general.add_value('language', in_language)
        # ToDo: keywords would be extremely useful, but aren't supplied by neither the API / JSON_LD nor the header
        # # once we've added all available values to the necessary keys in our LomGeneralItemLoader,
        # # we call the load_item()-method to return a (now filled) LomGeneralItem to the LomBaseItemLoader
        lom.add_value('general', general.load_item())

        technical = LomTechnicalItemLoader()
        # # TODO: fill "technical"-keys with values for
        # #  - size                           optional
        # #  - requirement                    optional
        # #  - installationRemarks            optional
        # #  - otherPlatformRequirements      optional
        # #  - duration                       optional (only applies to audiovisual content like videos/podcasts)
        technical.add_value('format', 'text/html')  # e.g. if the learning object is a web-page
        technical.add_value('location', graphql_json["id"])  # we could also use response.url here

        lom.add_value('technical', technical.load_item())

        lifecycle = LomLifecycleItemloader()
        # # TODO: fill "lifecycle"-keys with values for
        # #  - role                           recommended
        # #  - firstName                      recommended
        # #  - lastName                       recommended
        # #  - uuid                           optional
        if "publisher" in json_ld:
            lifecycle.add_value('organization', "Serlo Education e. V.")
            lifecycle.add_value('role', 'publisher')  # supported roles: "author" / "editor" / "publisher"
            # for available roles mapping, please take a look at converter/es_connector.py
            lifecycle.add_value('url', json_ld["publisher"])
            lifecycle.add_value('email', "de@serlo.org")
            for language_item in in_language:
                if language_item == "en":
                    lifecycle.replace_value('email', "en@serlo.org")
        lifecycle.add_value('date', graphql_json["dateCreated"])
        lom.add_value('lifecycle', lifecycle.load_item())

        educational = LomEducationalItemLoader()
        # # TODO: fill "educational"-keys with values for
        # #  - description                    recommended (= "Comments on how this learning object is to be used")
        # #  - interactivityType              optional
        # #  - interactivityLevel             optional
        # #  - semanticDensity                optional
        # #  - typicalAgeRange                optional
        # #  - difficulty                     optional
        # #  - typicalLearningTime            optional
        educational.add_value('language', in_language)

        lom.add_value('educational', educational.load_item())

        # classification = LomClassificationItemLoader()
        # # TODO: fill "classification"-keys with values for
        # #  - cost                           optional
        # #  - purpose                        optional
        # #  - taxonPath                      optional
        # #  - description                    optional
        # #  - keyword                        optional
        # lom.add_value('classification', classification.load_item())

        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value('new_lrt', Constants.NEW_LRT_MATERIAL)
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
                    vs.add_value('educationalContext', ["Further Education", "vocational education"])
                if edu_audience_role in self.EDU_AUDIENCE_ROLE_MAPPING.keys():
                    edu_audience_role = self.EDU_AUDIENCE_ROLE_MAPPING.get(edu_audience_role)
                intended_end_user_roles.append(edu_audience_role)
            vs.add_value('intendedEndUserRole', intended_end_user_roles)
            # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/intendedEndUserRole.ttl)

        if "about" in json_ld and len(json_ld["about"]) != 0:
            # not every json_ld-container has an "about"-key, e.g.: https://de.serlo.org/5343/5343
            # we need to make sure that we only try to access "about" if it's actually available
            # making sure that we only try to look for a discipline if the "about"-list actually has list items
            disciplines = list()
            for list_item in json_ld["about"]:
                if "de" in list_item["prefLabel"]:
                    discipline_de: str = list_item["prefLabel"]["de"]
                    disciplines.append(discipline_de)
                elif "en" in list_item["prefLabel"]:
                    discipline_en: str = list_item["prefLabel"]["en"]
                    disciplines.append(discipline_en)
            if len(disciplines) > 0:
                vs.add_value('discipline', disciplines)
                # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/discipline.ttl)
            # if the json_ld doesn't hold a discipline value for us, we'll try to grab the discipline from the url path
        else:
            if "/mathe/" in response.url:
                vs.add_value('discipline', "Mathematik")
            if "/biologie/" in response.url:
                vs.add_value('discipline', "Biologie")
            if "/chemie/" in response.url:
                vs.add_value('discipline', "Chemie")
            if "/nachhaltigkeit/" in response.url:
                vs.add_value('discipline', "Nachhaltigkeit")
            if "/informatik/" in response.url:
                vs.add_value('discipline', "Informatik")
        vs.add_value('containsAdvertisement', 'No')
        # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/containsAdvertisement.ttl)
        # serlo doesn't want to distract learners with ads, therefore we can set it by default to 'no'
        if graphql_json["isAccessibleForFree"] is True:
            # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/price.ttl)
            vs.add_value('price', 'no')
        elif graphql_json["isAccessibleForFree"] is False:
            # only set the price to "kostenpflichtig" if it's explicitly stated, otherwise we'll leave it empty
            vs.add_value('price', 'yes')
        if graphql_json["learningResourceType"]:
            # (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/learningResourceType.ttl)
            vs.add_value('learningResourceType', graphql_json["learningResourceType"])

        base.add_value('valuespaces', vs.load_item())

        lic = LicenseItemLoader()
        # # TODO: fill "license"-keys with values for
        # #  - author                         recommended
        # #  - expirationDate                 optional (for content that expires, e.g. ÖR-Mediatheken)
        license_url = graphql_json["license"]["id"]
        if license_url:
            lic.add_value('url', license_url)
        base.add_value('license', lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value('permissions', permissions.load_item())

        response_loader = super().mapResponse(response)
        response_loader.replace_value('html', html_body)
        response_loader.replace_value('text', html_text)
        base.add_value('response', response_loader.load_item())

        yield base.load_item()
