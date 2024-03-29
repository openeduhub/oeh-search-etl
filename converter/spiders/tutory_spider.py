import logging
import re
import urllib.parse

import scrapy
import trafilatura
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider

from .base_classes import LomBase, JSONBase
from ..items import LomBaseItemloader, BaseItemLoader, ResponseItemLoader
from ..web_tools import WebEngine, WebTools


class TutorySpider(CrawlSpider, LomBase, JSONBase):
    name = "tutory_spider"
    friendlyName = "tutory"
    url = "https://www.tutory.de/"
    objectUrl = "https://www.tutory.de/bereitstellung/dokument/"
    baseUrl = "https://www.tutory.de/api/v1/share/"
    version = "0.1.9"  # last update: 2023-08-18
    custom_settings = {
        # "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
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
        yield scrapy.Request(url=first_url, callback=self.parse_api_page)

    def parse_api_page(self, response: scrapy.http.TextResponse):
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
            logging.info(
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
                logging.info(
                    f"Tutory API page {pagination_current_page} is expected to yield " f"{len(worksheets_data)} items."
                )
                for j in worksheets_data:
                    response_copy = response.replace(url=self.objectUrl + j["id"])
                    item_url = response_copy.url
                    response_copy.meta["item"] = j
                    if self.hasChanged(response_copy):
                        yield scrapy.Request(url=item_url, callback=self.parse, cb_kwargs={"item_dict": j})

    def assemble_tutory_api_url(self, api_page: int):
        url_current_page = (
            f"{self.baseUrl}worksheet?groupSlug=entdecken&pageSize={str(self.API_PAGESIZE_LIMIT)}"
            f"&page={str(api_page)}"
        )
        return url_current_page

    def getId(self, response=None, **kwargs):
        if "item" in response.meta:
            item_id: str = response.meta["item"]["id"]
            return item_id
        else:
            try:
                api_item = kwargs["kwargs"]["item_dict"]
                item_id: str = api_item["id"]
                return item_id
            except KeyError as ke:
                logging.error(f"'getId'-method failed to retrieve item_id for '{response.url}'.")
                raise ke

    def getHash(self, response=None):
        return response.meta["item"]["updatedAt"] + self.version

    # ToDo (performance): reduce the amount of scrapy Requests by executing hasChanged() earlier:
    #  - if we call hasChanged() earlier, we might have to re-implement getUri() as well (since the resolved URL is
    #  always different from the unique 'dokument'-URL)

    def check_if_item_should_be_dropped(self, response) -> bool:
        drop_item_flag: bool = False
        identifier: str = self.getId(response)
        hash_str: str = self.getHash(response)
        if self.shouldImport(response) is False:
            logging.debug(f"Skipping entry {identifier} because shouldImport() returned false")
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
        # if we need more metadata from the DOM, this could be a suitable place to move up the call to Playwright
        base_loader: BaseItemLoader = self.getBase(response)
        lom_loader: LomBaseItemloader = self.getLOM(response)
        lom_loader.add_value("general", self.getLOMGeneral(response))
        lom_loader.add_value("technical", self.getLOMTechnical(response))

        base_loader.add_value("lom", lom_loader.load_item())
        base_loader.add_value("valuespaces", self.getValuespaces(response).load_item())
        base_loader.add_value("license", self.getLicense(response).load_item())
        base_loader.add_value("permissions", self.getPermissions(response).load_item())
        response_itemloader: ResponseItemLoader = await self.mapResponse(response, fetchData=False)
        base_loader.add_value("response", response_itemloader.load_item())
        yield base_loader.load_item()

    def getBase(self, response=None):
        base = LomBase.getBase(self, response)
        base.add_value("lastModified", response.meta["item"]["updatedAt"])
        base.add_value(
            "thumbnail",
            self.objectUrl + response.meta["item"]["id"] + ".jpg?width=1000",
        )
        return base

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
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

    def getLicense(self, response=None):
        license_loader = LomBase.getLicense(self, response)
        if "user" in response.meta["item"]:
            user_dict: dict = response.meta["item"]["user"]
            if "publishName" in user_dict:
                # the 'publishName'-field seems to indicate whether the username or the full name appears on top of a
                # worksheet as author metadata.
                publish_decision: str = user_dict["publishName"]
                if publish_decision == "username":
                    if "username" in user_dict:
                        username: str = user_dict["username"]
                        if username:
                            license_loader.add_value("author", username)
                elif publish_decision == "name":
                    # ToDo: this information could also be used for lifecycle role 'author' in a future crawler update
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

    async def getLOMGeneral(self, response=None):
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
        else:
            # this is where the (expensive) calls to our headless browser start
            playwright_dict = await WebTools.getUrlData(response.url, engine=WebEngine.Playwright)
            playwright_html = playwright_dict["html"]
            # ToDo: if we need DOM data from Playwright in another method, move the call to Playwright into parse()
            #  and parametrize the result
            if playwright_html:
                # 3rd fallback: trying to extract the fulltext with trafilatura
                playwright_bytes: bytes = playwright_html.encode()
                trafilatura_text = trafilatura.extract(playwright_bytes)
                if trafilatura_text:
                    logging.debug(
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

    def getLOMTechnical(self, response=None):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("location", response.url)
        technical.add_value("format", "text/html")
        technical.add_value("size", len(response.body))
        return technical
