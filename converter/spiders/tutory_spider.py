import logging
import re
import urllib.parse

import scrapy
import trafilatura
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider

from .base_classes import LomBase, JSONBase
from ..items import (
    LomBaseItemloader,
    BaseItemLoader,
    ResponseItemLoader,
    LomGeneralItemloader,
    LomTechnicalItemLoader,
    LomLifecycleItemloader,
    LomEducationalItemLoader,
    LicenseItemLoader,
    ValuespaceItemLoader,
)
from ..web_tools import WebEngine, WebTools

logger = logging.getLogger(__name__)


class TutorySpider(CrawlSpider, LomBase, JSONBase):
    name = "tutory_spider"
    friendlyName = "tutory"
    url = "https://www.tutory.de/"
    objectUrl = "https://www.tutory.de/bereitstellung/dokument/"
    baseUrl = "https://www.tutory.de/api/v1/share/"
    version = "0.2.1"  # last update: 2024-02-08
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 2,
        "WEB_TOOLS": WebEngine.Playwright,
    }

    API_PAGESIZE_LIMIT = 250

    # the old API pageSize of 999999 (which was used in 2021) doesn't work anymore and throws a 502 Error (Bad Gateway).
    # 2023-03: setting pageSize to 5000 appeared to be a reasonable value with an API response time of 12-15s
    # 2023-08-15: every setting above 500 appears to always return a '502'-Error now. Current response times during api
    # pagination are:
    # - '500': the API response time is roughly 42s.
    # - '250': the API response time is roughly 21s.

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self):
        first_url: str = self.assemble_tutory_api_url(api_page=0)
        # we need to lower the priority of subsequent API page requests because each response takes about 21s while
        # individual documents load within <300 ms
        yield scrapy.Request(url=first_url, callback=self.parse_api_page, priority=-1)

    def parse_api_page(self, response: scrapy.http.TextResponse) -> scrapy.Request:
        """
        This method tries to parse the current pagination parameter from response.url and yields two types of
        scrapy.Requests:
        1) if the "worksheets"-list isn't empty, try to crawl the next API page
        2) if there are "worksheets" in the current JSON Response, try to crawl the individual items
        """
        json_data: dict = response.json()
        page_regex = re.compile(r"&page=(?P<page>\d+)")
        pagination_parameter = page_regex.search(response.url)
        pagination_current_page: int = 0
        if pagination_parameter:
            pagination_current_page: int = pagination_parameter.groupdict().get("page")
        if "total" in json_data:
            total_items = json_data.get("total")
            logger.info(
                f"Currently crawling Tutory API page {pagination_current_page} -> {response.url} // "
                f"Expected items (in total): {total_items}"
            )
        pagination_next_page: int = int(pagination_current_page) + 1
        url_next_page = self.assemble_tutory_api_url(pagination_next_page)
        if "worksheets" in json_data:
            worksheets_data: list = json_data.get("worksheets")
            if worksheets_data:
                # only crawl the next page if the "worksheets"-dict isn't empty
                yield scrapy.Request(url=url_next_page, callback=self.parse_api_page)
                logger.info(
                    f"Tutory API page {pagination_current_page} is expected to yield " f"{len(worksheets_data)} items."
                )
                for j in worksheets_data:
                    response_copy = response.replace(url=self.objectUrl + j["id"])
                    item_url = response_copy.url
                    response_copy.meta["item"] = j
                    if self.hasChanged(response_copy):
                        yield scrapy.Request(url=item_url, callback=self.parse, cb_kwargs={"item_dict": j})

    def assemble_tutory_api_url(self, api_page: int) -> str:
        url_current_page = (
            f"{self.baseUrl}worksheet?groupSlug=entdecken&pageSize={str(self.API_PAGESIZE_LIMIT)}"
            f"&page={str(api_page)}"
        )
        return url_current_page

    def getId(self, response=None, **kwargs) -> str:
        if "item" in response.meta:
            item_id: str = response.meta["item"]["id"]
            return item_id
        else:
            try:
                api_item = kwargs["kwargs"]["item_dict"]
                item_id: str = api_item["id"]
                return item_id
            except KeyError as ke:
                logger.error(f"'getId'-method failed to retrieve item_id for '{response.url}'.")
                raise ke

    def getHash(self, response=None) -> str:
        return response.meta["item"]["updatedAt"] + self.version

    # ToDo (performance): reduce the amount of scrapy Requests by executing hasChanged() earlier:
    #  - if we call hasChanged() earlier, we might have to re-implement getUri() as well (since the resolved URL is
    #  always different from the unique 'dokument'-URL)

    def check_if_item_should_be_dropped(self, response) -> bool:
        drop_item_flag: bool = False
        identifier: str = self.getId(response)
        hash_str: str = self.getHash(response)
        robot_meta_tags: str = response.xpath("//meta[@name='robots']/@content").get()
        if robot_meta_tags:
            if "noindex" in robot_meta_tags or "none" in robot_meta_tags:
                drop_item_flag = True
                logger.info(f"Robot Meta Tag {robot_meta_tags} identified: Tags 'noindex' or 'none' indicate that this "
                            f"item should not be indexed by the crawler. Dropping item...")
                return drop_item_flag
        if self.shouldImport(response) is False:
            logger.debug(f"Skipping entry {identifier} because shouldImport() returned false")
            drop_item_flag = True
            return drop_item_flag
        if identifier is not None and hash_str is not None:
            if not self.hasChanged(response):
                drop_item_flag = True
            return drop_item_flag

    async def parse(self, response, **kwargs):
        try:
            item_dict_from_api: dict = kwargs["item_dict"]
            response.meta["item"] = item_dict_from_api
        except KeyError as ke:
            raise ke

        drop_item_flag: bool = self.check_if_item_should_be_dropped(response)
        if drop_item_flag is True:
            return

        playwright_dict: dict = await WebTools.getUrlData(response.url, engine=WebEngine.Playwright)
        playwright_html: str = playwright_dict["html"]

        base_loader: BaseItemLoader = self.getBase(response)
        lom_loader: LomBaseItemloader = LomBaseItemloader()
        general_loader: LomGeneralItemloader = await self.getLOMGeneral(
            response=response, playwright_dict=playwright_dict
        )
        lom_loader.add_value("general", general_loader.load_item())
        educational_loader: LomEducationalItemLoader = LomEducationalItemLoader()
        lom_loader.add_value("educational", educational_loader.load_item())
        lifecycle_loader = await self.getLOMLifecycle(response)
        lom_loader.add_value("lifecycle", lifecycle_loader.load_item())
        technical_loader: LomTechnicalItemLoader = self.getLOMTechnical(response)
        lom_loader.add_value("technical", technical_loader.load_item())

        base_loader.add_value("lom", lom_loader.load_item())
        base_loader.add_value("valuespaces", self.getValuespaces(response).load_item())
        base_loader.add_value("license", self.getLicense(response).load_item())
        base_loader.add_value("permissions", self.getPermissions(response).load_item())
        response_loader: ResponseItemLoader = await self.mapResponse(response, fetchData=False)
        if playwright_html and isinstance(playwright_html, str):
            response_loader.replace_value("html", playwright_html)
        if "screenshot_bytes" in playwright_dict:
            sbytes: bytes = playwright_dict["screenshot_bytes"]
            base_loader.add_value("screenshot_bytes", sbytes)
        if "text" in playwright_dict:
            playwright_fulltext: str = playwright_dict["text"]
            if playwright_fulltext and isinstance(playwright_fulltext, str):
                response_loader.replace_value("text", playwright_fulltext)
        base_loader.add_value("response", response_loader.load_item())
        yield base_loader.load_item()

    def getBase(self, response=None) -> BaseItemLoader:
        base = LomBase.getBase(self, response)
        base.add_value("lastModified", response.meta["item"]["updatedAt"])
        base.add_value(
            "thumbnail",
            self.objectUrl + response.meta["item"]["id"] + ".jpg?width=1000",
        )
        return base

    def getValuespaces(self, response) -> ValuespaceItemLoader:
        valuespaces: ValuespaceItemLoader = LomBase.getValuespaces(self, response)
        disciplines = set()
        subject_codes: list[str] = list(
            map(
                lambda x: x["code"],
                filter(
                    lambda x: x["type"] == "subject",
                    response.meta["item"]["metaValues"],
                ),
            )
        )
        if subject_codes:
            disciplines.update(subject_codes)
        # This is a (temporary) workaround until ITSJOINTLY-332 has been solved: The vocab matching doesn't hit all
        #  "altLabel"-values because they don't exist in the generated disipline.json. We're therefore trying to collect
        # additional strings which could (hopefully) be mapped.
        subject_names: list[str] = list(
            map(
                lambda x: x["name"],
                filter(
                    lambda x: x["type"] == "subject",
                    response.meta["item"]["metaValues"],
                ),
            )
        )
        if subject_names:
            disciplines.update(subject_names)
        if disciplines:
            # only one 'discipline'-value will remain after vocab-matching in our pipelines, so duplicate values are
            # (for now) no problem, but need to be handled as soon as ITSJOINTLY-332 is solved
            # ToDo: confirm that this workaround still works as intended after ITSJOINTLY-332 has been solved
            # ToDo: known edge-cases for strings which cannot be mapped to our 'discipline'-vocab yet and should be
            #  handled after SC 2023:
            #  - "abu" ("Allg. bildender Unterricht")
            #  - "betriebswirtschaft"
            #  - "naturwissenschaft"
            #  - "technik"
            valuespaces.add_value("discipline", list(disciplines))

        potential_classlevel_values: list[str] = list(
            map(
                lambda x: x["code"],
                filter(
                    lambda x: x["type"] == "classLevel",
                    response.meta["item"]["metaValues"],
                ),
            )
        )
        educontext_set: set[str] = set()
        if potential_classlevel_values and type(potential_classlevel_values) is list:
            potential_classlevel_values.sort()
            two_digits_pattern = re.compile(r"^\d{1,2}$")  # the whole string must be exactly between 1 and 2 digits
            classlevel_set: set[str] = set()
            classlevel_digits: set[int] = set()
            for potential_classlevel in potential_classlevel_values:
                # the classLevel field contains a wild mix of string-values
                # this is a rough mapping that could be improved with further finetuning (and a more structured
                # data-dump of all possible values)
                two_digits_pattern_hit = two_digits_pattern.search(potential_classlevel)
                if two_digits_pattern_hit:
                    # 'classLevel'-values will appear as numbers within a string ("3" or "12") and need to be converted
                    # for our mapping approach
                    classlevel_candidate = two_digits_pattern_hit.group()
                    classlevel_set.add(classlevel_candidate)
                if "ausbildung" in potential_classlevel:
                    # typical values: "1-ausbildungsjahr" / "2-ausbildungsjahr" / "3-ausbildungsjahr"
                    educontext_set.add("berufliche_bildung")
                if "e-1" in potential_classlevel or "e-2" in potential_classlevel:
                    educontext_set.add("sekundarstufe_1")
                    educontext_set.add("sekundarstufe_2")
            if classlevel_set and len(classlevel_set) > 0:
                classlevels_sorted: list[str] = list(classlevel_set)
                classlevels_sorted.sort(key=len)
                for classlevel_string in classlevels_sorted:
                    classlevel_nr: int = int(classlevel_string)
                    classlevel_digits.add(classlevel_nr)
            if classlevel_digits:
                classlevel_integers: list[int] = list(classlevel_digits)
                if classlevel_integers and type(classlevel_integers) is list:
                    # classlevel_min: int = min(classlevel_integers)
                    # classlevel_max: int = max(classlevel_integers)
                    for int_value in classlevel_integers:
                        if 0 < int_value <= 4:
                            educontext_set.add("grundschule")
                        if 5 <= int_value <= 9:
                            educontext_set.add("sekundarstufe_1")
                        if 10 <= int_value <= 13:
                            educontext_set.add("sekundarstufe_2")
        if educontext_set:
            educontext_list: list[str] = list(educontext_set)
            valuespaces.add_value("educationalContext", educontext_list)
        valuespaces.add_value("new_lrt", "36e68792-6159-481d-a97b-2c00901f4f78")  # Arbeitsblatt
        return valuespaces

    def getLicense(self, response=None) -> LicenseItemLoader:
        license_loader: LicenseItemLoader = LomBase.getLicense(self, response)
        if "user" in response.meta["item"]:
            user_dict: dict = response.meta["item"]["user"]
            if "publishName" in user_dict:
                # the 'publishName'-field seems to indicate whether the username or the full name appears on top of a
                # worksheet as author metadata.
                publish_decision: str = user_dict["publishName"]
                if publish_decision and publish_decision.startswith("custom:"):
                    # there are edge-cases where "publishName" starts with "custom:<...name of person>", which means
                    # that a custom string shall be used. (e.g., document id "1cdf1514-af66-475e-956c-b8487588e095"
                    # -> https://www.tutory.de/entdecken/dokument/class-test-checkliste-englisch )
                    custom_name: str = publish_decision
                    custom_name = custom_name.replace("custom:", "")
                    if custom_name:
                        license_loader.add_value("author", custom_name)
                elif publish_decision == "username":
                    if "username" in user_dict:
                        username: str = user_dict["username"]
                        if username:
                            license_loader.add_value("author", username)
                elif publish_decision == "name":
                    firstname = None
                    lastname = None
                    if "firstname" in user_dict:
                        firstname = user_dict.get("firstname")
                    if "lastname" in user_dict:
                        lastname = user_dict.get("lastname")
                    if firstname and lastname:
                        full_name = f"{firstname} {lastname}"
                        license_loader.add_value("author", full_name)
        return license_loader

    async def getLOMLifecycle(self, response: scrapy.http.Response = None) -> LomLifecycleItemloader:
        lifecycle_loader: LomLifecycleItemloader = LomLifecycleItemloader()
        if "user" in response.meta["item"]:
            user_dict: dict = response.meta["item"]["user"]
            lifecycle_loader.add_value("role", "author")
            if "publishName" in user_dict:
                # the 'publishName'-field seems to indicate whether the username or the full name appears on top of a
                # worksheet as author metadata.
                publish_decision: str = user_dict["publishName"]
                if publish_decision and publish_decision.startswith("custom:"):
                    # there are edge-cases where "publishName" starts with "custom:<...name of person>", which means
                    # that a custom string shall be used. (e.g., document id "1cdf1514-af66-475e-956c-b8487588e095"
                    # -> https://www.tutory.de/entdecken/dokument/class-test-checkliste-englisch )
                    custom_name: str = publish_decision
                    custom_name = custom_name.replace("custom:", "")
                    if custom_name:
                        lifecycle_loader.add_value("firstName", custom_name)
                elif publish_decision == "username":
                    if "username" in user_dict:
                        username: str = user_dict["username"]
                        if username:
                            lifecycle_loader.add_value("firstName", username)
                elif publish_decision == "name":
                    if "firstname" in user_dict:
                        firstname: str = user_dict.get("firstname")
                        if firstname:
                            lifecycle_loader.add_value("firstName", firstname)
                    if "lastname" in user_dict:
                        lastname: str = user_dict.get("lastname")
                        if lastname:
                            lifecycle_loader.add_value("lastName", lastname)
                user_profile_path: str = response.xpath(
                    "//a[@class='value']/@href|label[contains(text(), 'Autor')]"
                ).get()
                if user_profile_path and isinstance(user_profile_path, str):
                    user_profile_url: str = urllib.parse.urljoin(self.url, user_profile_path)
                    if user_profile_url:
                        lifecycle_loader.add_value("url", user_profile_url)
        return lifecycle_loader

    async def getLOMGeneral(self, response=None, playwright_dict: dict = None) -> LomGeneralItemloader:
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("title", response.meta["item"]["name"])
        item_description = None
        if "description" in response.meta["item"]:
            item_description = response.meta["item"]["description"]
        meta_description = response.xpath("//meta[@property='description']/@content").get()
        meta_og_description = response.xpath("//meta[@property='og:description']/@content").get()
        if item_description:
            general.add_value("description", item_description)
        elif meta_description:
            # 1st fallback: trying to parse a description string from the header
            general.add_value("description", meta_description)
        elif meta_og_description:
            # 2nd fallback: <meta property="og:description">
            general.add_value("description", meta_og_description)
        elif "html" in playwright_dict:
            # this is where the (expensive) calls to our headless browser start
            playwright_html = playwright_dict["html"]
            if playwright_html:
                # 3rd fallback: trying to extract the fulltext with trafilatura
                playwright_bytes: bytes = playwright_html.encode()
                trafilatura_text = trafilatura.extract(playwright_bytes)
                if trafilatura_text:
                    logger.debug(
                        f"Item {response.url} did not provide any valid 'description' in its DOM header metadata. "
                        f"Fallback to trafilatura fulltext..."
                    )
                    trafilatura_shortened: str = f"{trafilatura_text[:2000]} [...]"
                    general.add_value("description", trafilatura_shortened)
                else:
                    # 4th fallback: resorting to (manual) scraping of DOM elements (via XPaths):
                    # apparently, the human-readable text is nested within
                    # <div class="eduMark"> OR <div class="noEduMark"> elements
                    edumark_combined: list[str] = (
                        Selector(text=playwright_html)
                        .xpath("//div[contains(@class,'eduMark')]//text()|//div[contains(@class,'noEduMark')]//text()")
                        .getall()
                    )
                    if edumark_combined:
                        text_combined: str = " ".join(edumark_combined)
                        text_combined = urllib.parse.unquote(text_combined)
                        text_combined = f"{text_combined[:2000]} [...]"
                        general.add_value("description", text_combined)
        return general

    def getLOMTechnical(self, response=None) -> LomTechnicalItemLoader:
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("location", response.url)
        technical.add_value("format", "text/html")
        technical.add_value("size", len(response.body))
        return technical
