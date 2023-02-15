import datetime
import logging
import re

import scrapy
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, \
    LomClassificationItemLoader
from converter.spiders.base_classes import LomBase
from converter.web_tools import WebEngine


class KiCampusSpider(CrawlSpider, LomBase):
    name = "ki_campus_spider"
    friendlyName = "ki_campus_spider"
    start_urls = ["https://learn.ki-campus.org/bridges/moochub/courses"]
    version = "0.0.1"  # last update: 2023-02-15
    custom_settings = {
        'WEB_TOOLS': WebEngine.Playwright,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
    }
    COUNTER_JSON_ITEMS = 0  # helper variable to count the amount of JSON Objects during API Pagination
    forceUpdate = True

    def close(self, reason):
        logging.info(f"During the initial API Pagination {self.COUNTER_JSON_ITEMS} JSON Items were counted. "
                     f"(You can compare this value with the amount of items scraped in the scrapy results.)")

    def getId(self, response=None) -> str:
        return response.url

    def getHash(self, response=None, date_string=None) -> str:
        if date_string:
            # not every json item has a 'startDate'-attribute
            date_string = date_string
        else:
            # fallback for items that have no 'startDate': use current datetime instead
            date_string = datetime.datetime.now().isoformat()
        hash_temp = f"{date_string}{self.version}"
        return hash_temp

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse_api_page)

    def parse_api_page(self, response: scrapy.http.TextResponse):
        # The expected API response is a JSON starting with links for pagination, typically looking like this:
        # "links": {
        # 		"self": "https://learn.ki-campus.org/bridges/moochub/courses?page=1",
        # 		"first": "https://learn.ki-campus.org/bridges/moochub/courses?page=1",
        # 		"last": "https://learn.ki-campus.org/bridges/moochub/courses?page=2",
        # 		"next": "https://learn.ki-campus.org/bridges/moochub/courses?page=2"
        # 		}
        json_body: dict = response.json()
        logging.debug(f"API Pagination: Current page: {response.url}")
        if "links" in json_body:
            json_links = json_body["links"]
            api_current_page = None
            api_last_page = None
            if "last" in json_links:
                api_last_page = json_links["last"]
            if "self" in json_links:
                api_current_page = json_links["self"]
            if "next" in json_links:
                # the 'next'-key only exists for pages that have a next page. The 'next'-key is replaced by 'prev' once
                # you've reached the final page during pagination. Example:
                # "links": {
                # 		"self": "https://learn.ki-campus.org/bridges/moochub/courses?page=2",
                # 		"first": "https://learn.ki-campus.org/bridges/moochub/courses?page=1",
                # 		"last": "https://learn.ki-campus.org/bridges/moochub/courses?page=2",
                # 		"prev": "https://learn.ki-campus.org/bridges/moochub/courses?page=1"
                # 	}
                api_next_page = json_links["next"]
                logging.debug(f"API Pagination: Next page is {api_next_page}. Yielding Scrapy Request...")
                yield scrapy.Request(url=api_next_page, callback=self.parse_api_page)
            if api_current_page and api_last_page:
                if api_current_page == api_last_page:
                    logging.debug(f"API Pagination: Reached the final page {api_current_page}")
        if "data" in json_body:
            json_data: list = json_body["data"]
            logging.debug(f"API Pagination: Detected {len(json_data)} JSON items on {response.url}")
            self.COUNTER_JSON_ITEMS += int(len(json_data))
            for json_item in json_data:
                if "attributes" in json_item:
                    if "url" in json_item["attributes"]:
                        item_url = json_item["attributes"]["url"]
                        print(f"{item_url}")
                        yield scrapy.Request(url=item_url, callback=self.parse, cb_kwargs={"json_item": json_item})

    def parse(self, response: scrapy.http.Response, **kwargs) -> BaseItemLoader:
        json_item = kwargs.get("json_item")
        item_attributes = json_item["attributes"]
        # ToDo: (possible) Item Attributes according to the API spec that cannot be properly mapped to edu-sharing
        #  - courseCode                     -> base.identifier
        #  - courseMode                     -> workaround: new_lrt?
        #  - abstract                       -> "Kursbeschreibung"? (no edu-sharing field)
        #  - startDate                      -> no edu-sharing field
        #  - endDate                        -> no edu-sharing field
        #  - image                          -> ?
        #       - licenses                  -> ?
        #           - id                    -> ?
        #           - url                   -> used for 'base.thumbnail'
        #           - name                  -> ?
        #           - author                -> ?
        #  - video                          -> ?
        #       - url                       -> ?
        #       - licenses                  -> ?
        #           - id                    -> ?
        #           - url                   -> ?
        #           - name                  -> ?
        #           - author                -> ?
        #  - instructors                    -> there is no 'lifecycle' role for "instructor" available
        #       - name
        #       - type                      -> ? (can be either 'Person' or 'Organization')
        #       - role                      -> ?
        #       - image                     -> ?
        #           - url                   -> ?
        #           - licenses              -> ?
        #       - description               -> ?
        #  - learningObjectives             -> no edu-sharing field
        #  - duration                       -> no edu-sharing field
        #       (= duration of the whole course ("ISO 8601 encoded duration"))
        #  - workload                       -> no edu-sharing field
        #       (= "specifies the amount of weekly hours course participants should plan with when taking the course")
        #  - partnerInstitute               -> workaround: could be saved as additional lifecycle publisher
        #       - name
        #       - description               -> ?
        #       - logo                      -> no edu-sharing field
        #       - url
        #  - moocProvider                   -> workaround: lifecycle role 'publisher' -> organization
        #       - description               -> ?
        #       - logo                      -> no edu-sharing field

        base = BaseItemLoader()
        # ALL possible keys for the different Item and ItemLoader-classes can be found inside converter/items.py

        base.add_value('sourceId', self.getId(response))
        if "startDate" in item_attributes:
            start_date: str = item_attributes["startDate"]
            if start_date:
                base.add_value('hash', self.getHash(response, date_string=start_date))
        else:
            base.add_value('hash', self.getHash(response))
        if "image" in item_attributes:
            image_url: str = item_attributes["image"]["url"]
            if image_url:
                base.add_value('thumbnail', image_url)

        lom = LomBaseItemloader()
        general = LomGeneralItemloader()
        if "id" in json_item:
            # from the API Docs: "ID of the object, UUID is preferred."
            # Example from the API:
            # "id": "d31c3f75-d4c3-45af-a9b7-b3ff62fbc1e7"
            item_id: str = json_item["id"]
            if item_id:
                general.add_value('identifier', item_id)
        elif "courseCode" in item_attributes:
            course_code: str = item_attributes["courseCode"]
            if course_code:
                general.add_value('identifier', course_code)
        if "name" in item_attributes:
            item_name = item_attributes["name"]
            if item_name:
                general.add_value('title', item_name)
        if "description" in item_attributes:
            item_description: str = item_attributes["description"]
            if item_description:
                general.add_value('description', item_description)
        elif "abstract" in item_attributes:
            # the 'abstract'-attribute can either be a String or null, according to the API docs:
            #   "Abstract of the course as an HTML document"
            # currently, 'description' and 'abstract' seem to be the same String.
            # If this changes in the future, we might need an addition 'abstract' field
            # ToDo: dedicated edu-sharing field for 'abstract'-attribute?
            item_abstract: str = item_attributes["abstract"]
            if item_abstract:
                general.add_value('description', item_abstract)
        if "languages" in item_attributes:
            # ToDo: 'languages'-attribute -> list[str] (the API returns 2-char codes, e.g. 'de' or 'en';
            #  while edu-sharing expects a 4-char language-codes with underscores?)
            language_list: list = item_attributes["languages"]
            if language_list:
                general.add_value('language', language_list)

        technical = LomTechnicalItemLoader()
        technical.add_value('location', response.url)
        if "url" in item_attributes:
            if item_attributes["url"] != response.url:
                # in case the resolved URL might be different from the URI of the json item
                technical.add_value('location', item_attributes["url"])

        if "instructor" in item_attributes:
            instructors: list[dict] = item_attributes["instructor"]
            # ToDo: lifecycle roles don't support "instructors", we could either map them to 'author' or 'publisher' as
            #  a temporary workaround
            if instructors:
                for instructor in instructors:
                    lifecycle_author = LomLifecycleItemloader()
                    instructor_name = None
                    if "name" in instructor:
                        instructor_name = instructor["name"]
                    if "type" in instructor:
                        instructor_type = instructor["type"]
                        if instructor_type:
                            if instructor_type == "Person":
                                pass
                            if instructor_type == "Organization":
                                lifecycle_author.replace_value('role', 'publisher')
                                if instructor_name:
                                    lifecycle_author.add_value('organization', instructor_name)
                    else:
                        # experience shows that the 'name'-field is available more often than the 'type'-attribute
                        if instructor_name:
                            lifecycle_author.add_value('role', 'author')
                            lifecycle_author.add_value('firstName', instructor_name)
                    # ToDo: there is no edu-sharing field for 'description' or 'image' attributes in lifecycle
                    lom.add_value('lifecycle', lifecycle_author.load_item())

        if "moocProvider" in item_attributes:
            mooc_provider: dict = item_attributes["moocProvider"]
            if mooc_provider:
                lifecycle_publisher = LomLifecycleItemloader()
                if "name" in mooc_provider:
                    provider_name: str = mooc_provider["name"]
                    if provider_name:
                        lifecycle_publisher.add_value('organization', provider_name)
                if "url" in mooc_provider:
                    provider_url: str = mooc_provider["url"]
                    if provider_url:
                        lifecycle_publisher.add_value('url', provider_url)
                if "logo" in mooc_provider:
                    provider_logo: str = mooc_provider["logo"]
                    # ToDo: there is currently no equivalent edu-sharing field for provider images / logos
                    if provider_logo:
                        pass
                if "description" in mooc_provider:
                    provider_description: str = mooc_provider["description"]
                    # ToDo: there is currently no equivalent edu-sharing field to store a provider description
                    if provider_description:
                        pass
                lom.add_value('lifecycle', lifecycle_publisher.load_item())

        educational = LomEducationalItemLoader()
        # ToDo: map 'duration' to 'typicalLearningTime'?

        classification = LomClassificationItemLoader()

        vs = ValuespaceItemLoader()
        # for possible values, either consult https://vocabs.openeduhub.de
        # or take a look at https://github.com/openeduhub/oeh-metadata-vocabs
        # wherever possible, please use the skos:Concept <key> instead of literal strings
        # (since they are more stable over a longer period of time)
        # TODO: fill "valuespaces"-keys with values for
        #  - discipline                     recommended
        #  (see: https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/discipline.ttl)
        #   (please set discipline-values by their unique vocab-identifier: e.g. '060' for "Art education")
        vs.add_value('intendedEndUserRole', 'learner')
        vs.add_value('new_lrt', Constants.NEW_LRT_MATERIAL)
        if "type" in json_item:
            item_type: str = json_item["type"]
            if item_type:
                if item_type == "courses":
                    vs.replace_value('new_lrt', '4e16015a-7862-49ed-9b5e-6c1c6e0ffcd1')  # Kurs
        # ToDo: all courses are MOOCs -> as soon as a 'new_lrt'-value is available, we could set it here to be more
        #  precise than "Kurs"
        if "access" in item_attributes:
            # possible values: 'free', 'paid', 'member-only', 'other'
            access_list: list[str] = item_attributes["access"]
            # API docs: "Specifies how this course can be accessed by learners. The different access options shall not
            # be used to transport differences between available content under this access option but rather annotate
            # the course track or certificate that can be achieved"
            if access_list:
                for access_string in access_list:
                    # according to the API specs there could be multiple strings inside the 'access'-attribute, but in
                    # 100% of the 60 items currently provided by the API, there is only a single string value provided
                    match access_string:
                        case "free":
                            vs.replace_value('price', 'no')
                        case "paid":
                            vs.replace_value('price', 'yes')
                        case "member-only":
                            vs.replace_value('conditionsOfAccess', 'login')
                        case "other":
                            # The API docs don't make it clear how 'other' should be interpreted
                            pass
                        case _:
                            logging.debug(f"Received unexpected 'access'-string: {access_string} . Please check if the "
                                          f"moocHub JSON specs have changed.")

        license_loader = LicenseItemLoader()
        if "availableUntil" in item_attributes:
            available_until: str = item_attributes["availableUntil"]
            if available_until:
                # API Docs: "An end date with time in ISO 8601 format specifying when the course is removed (and hence
                # no longer available) for learners. A null value is used for courses not disappearing from the
                # platform."
                license_loader.add_value('expirationDate', available_until)
        if "courseLicenses" in item_attributes:
            licenses: list = item_attributes["courseLicenses"]
            if licenses:
                for license_dict in licenses:
                    if "id" in license_dict:
                        # according to the API docs:
                        # "Either 'Proprietary' or a license identifier according to https://spdx.org/licenses"
                        # ToDo: could be mapped to 'license.internal' as a fallback if necessary, but 'url'-attribute
                        #  should be more stable/reliable in the long term anyway
                        pass
                    if "url" in license_dict:
                        license_url: str = license_dict["url"]
                        if license_url:
                            cc_version_regex = re.compile(r"/\d\.\d$")
                            if cc_version_regex.search(license_url):
                                # license urls will typically look like 'https://creativecommons.org/licenses/by-sa/4.0'
                                # but the license mapper currently expects all CC URLs to end with a slash.
                                # this (temporary) workaround will add the missing slash to the end of the string
                                # ToDo: remove this check once the license mapping in es_connector is improved
                                #  and doesn't check for "==", but also for partial strings
                                license_url = f"{license_url}/"
                            license_loader.add_value('url', license_url)
                    if "name" in license_dict:
                        # "a human readable license name"
                        license_name = license_dict["name"]
                        if license_name:
                            license_loader.add_value('description', license_name)
                    if "author" in license_dict:
                        license_author = license_dict["author"]
                        if license_author:
                            license_loader.add_value('author', license_author)

        permissions = super().getPermissions(response)
        response_loader = super().mapResponse(response)

        lom.add_value('general', general.load_item())
        lom.add_value('technical', technical.load_item())
        lom.add_value('educational', educational.load_item())
        lom.add_value('classification', classification.load_item())

        base.add_value('lom', lom.load_item())
        base.add_value('license', license_loader.load_item())
        base.add_value('valuespaces', vs.load_item())
        base.add_value('permissions', permissions.load_item())
        base.add_value('response', response_loader.load_item())

        yield base.load_item()
