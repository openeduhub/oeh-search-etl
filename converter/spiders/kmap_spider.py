import json
import logging
import re

import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.es_connector import EduSharing
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
    LomAgeRangeItemLoader,
)
from converter.spiders.base_classes import LomBase
from converter.util.sitemap import from_xml_response
from converter.web_tools import WebEngine, WebTools

logger = logging.getLogger(__name__)


class KMapSpider(CrawlSpider, LomBase):
    name = "kmap_spider"
    friendlyName = "KMap.eu"
    version = "0.0.7"  # last update: 2024-01-25
    sitemap_urls = ["https://kmap.eu/server/sitemap/Mathematik", "https://kmap.eu/server/sitemap/Physik"]
    custom_settings = {"ROBOTSTXT_OBEY": False, "AUTOTHROTTLE_ENABLED": True, "AUTOTHROTTLE_DEBUG": True}
    allowed_domains = ["kmap.eu"]
    # keep the console clean from spammy DEBUG-level logging messages, adjust as needed:
    logging.getLogger("websockets.server").setLevel(logging.ERROR)
    logging.getLogger("websockets.protocol").setLevel(logging.ERROR)

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self) -> scrapy.Request:
        for sitemap_url in self.sitemap_urls:
            yield scrapy.Request(url=sitemap_url, callback=self.parse_sitemap)

    def parse_sitemap(self, response) -> scrapy.Request:
        """

        Scrapy Contracts:
        @url https://kmap.eu/server/sitemap/Mathematik
        @returns requests 50
        """
        sitemap_items = from_xml_response(response)
        for sitemap_item in sitemap_items:
            temp_dict = {"lastModified": sitemap_item.lastmod}
            yield scrapy.Request(url=sitemap_item.loc, callback=self.parse, cb_kwargs=temp_dict)

    def getId(self, response=None) -> str:
        return response.url

    def getHash(self, response: scrapy.http.Response = None, json_ld: dict = None) -> str | None:
        try:
            main_entity: dict = json_ld["mainEntity"]
            if "dateModified" in main_entity:
                date_modified: str = main_entity["dateModified"]
                if date_modified:
                    item_hash: str = f"{date_modified}v{self.version}"
                    return item_hash
            elif "datePublished" in main_entity:
                date_published: str = main_entity["datePublished"]
                if date_published:
                    item_hash: str = f"{date_published}v{self.version}"
                    return item_hash
        except KeyError:
            logger.warning(
                f"KMap item {response.url} did not provide the necessary timestamps for building a hash. "
                f"Dropping item..."
            )
            return None

    def hasChanged(self, response=None, json_ld: dict = None) -> bool:
        if self.forceUpdate:
            return True
        if self.uuid:
            if self.getUUID(response) == self.uuid:
                logging.info(f"Matching requested id: {self.uuid} // item URL: {response.url}")
                return True
            return False
        if self.remoteId:
            if str(self.getId(response)) == self.remoteId:
                logging.info(f"Matching requested id: {self.remoteId} // item URL: {response.url}")
                return True
            return False
        db = EduSharing().find_item(self.getId(response), self)
        changed = db is None or db[1] != self.getHash(response=response, json_ld=json_ld)
        if not changed:
            logging.info(f"Item {self.getId(response)} (uuid: {db[0]}) has not changed")
        return changed

    async def parse(self, response: scrapy.http.Response, **kwargs) -> BaseItemLoader | None:
        """

        Scrapy Contracts:
        @url https://kmap.eu/app/browser/Mathematik/Exponentialfunktionen/Asymptoten
        @returns item 1
        """
        last_modified = kwargs.get("lastModified")
        url_data_playwright = await WebTools.getUrlData(response.url, engine=WebEngine.Playwright)
        html_string: str = url_data_playwright.get("html")

        try:
            json_ld_string: str = Selector(text=html_string).xpath('//*[@id="ld"]/text()').get()
            json_ld: dict = json.loads(json_ld_string)
        except TypeError:
            logger.warning(f"Item {response.url} did not contain a JSON_LD. Dropping item...")
            return

        main_entity: dict | None = None
        try:
            if "mainEntity" in json_ld:
                main_entity: dict = json_ld["mainEntity"]
        except KeyError:
            # while 'mainEntity' should be available within every (complete) knowledge card, placeholder cards which
            # are still being worked on might not have this metadata
            logger.warning(
                f"Item {response.url} did not contain a complete JSON_LD: the REQUIRED 'mainEntity' dict "
                f"was not available for parsing. (If you see this warning more often than a few times, "
                f"a crawler update might be necessary!) Dropping item..."
            )
            return

        base = BaseItemLoader()
        base.add_value("sourceId", self.getId(response=response))
        hash_value: str = self.getHash(response=response, json_ld=json_ld)
        if hash_value:
            base.add_value("hash", hash_value)
        else:
            # drop items that cannot be hashed
            return

        if self.shouldImport(response) is False:
            logger.debug(f"Skipping entry {response.url} because shouldImport() returned False.")
            return None
        if self.getId(response) is not None and self.getHash(response=response, json_ld=json_ld) is not None:
            if not self.hasChanged(response=response, json_ld=json_ld):
                return None

        base.add_value("lastModified", last_modified)
        # Thumbnails have their own url path, which can be found in the json+ld:
        #   "thumbnailUrl": "/snappy/Physik/Grundlagen/Potenzschreibweise"
        # e.g., for the item https://kmap.eu/app/browser/Physik/Grundlagen/Potenzschreibweise
        # the thumbnail can be found at https://kmap.eu/snappy/Physik/Grundlagen/Potenzschreibweise
        thumbnail_path = main_entity.get("thumbnailUrl")
        # ToDo: KMap also serves "og:image", which seems to provide slightly different URL paths,
        #  but apparently the same image files
        if thumbnail_path:
            base.add_value("thumbnail", f"https://kmap.eu{thumbnail_path}")

        lom = LomBaseItemloader()
        general = LomGeneralItemloader()
        general.add_value("identifier", main_entity.get("mainEntityOfPage"))
        if main_entity:
            if "keywords" in main_entity:
                keywords_string: str = main_entity.get("keywords")
                if keywords_string:
                    keyword_list: list[str] = keywords_string.rsplit(", ")
                    if keyword_list:
                        general.add_value("keyword", keyword_list)
            if "name" in main_entity:
                general.add_value("title", main_entity.get("name"))
            if "description" in main_entity:
                general.add_value("description", main_entity.get("description"))
            if "inLanguage" in main_entity:
                general.add_value("language", main_entity.get("inLanguage"))
        lom.add_value("general", general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value("format", "text/html")
        technical.add_value("location", response.url)
        if main_entity:
            # if resolved url is different from JSON_LD 'mainEntity.mainEntityOfPage' URL, save both URLs
            if "mainEntityOfPage" in main_entity:
                maeop_url: str = main_entity["mainEntityOfPage"]
                if maeop_url and maeop_url != response.url:
                    technical.add_value("location", maeop_url)
        lom.add_value("technical", technical.load_item())

        if main_entity:
            if "publisher" in main_entity:
                publisher_object: dict = main_entity["publisher"]
                if publisher_object and isinstance(publisher_object, dict):
                    lifecycle_publisher: LomLifecycleItemloader = LomLifecycleItemloader()
                    lifecycle_publisher.add_value("role", "publisher")
                    if "name" in publisher_object:
                        publisher_name: str = publisher_object["name"]
                        if publisher_name:
                            lifecycle_publisher.add_value("organization", publisher_name)
                    if "email" in publisher_object:
                        publisher_email: str = publisher_object["email"]
                        if publisher_email:
                            lifecycle_publisher.add_value("email", publisher_email)
                    if "url" in publisher_object:
                        publisher_url: str = publisher_object["url"]
                        if publisher_url:
                            lifecycle_publisher.add_value("url", publisher_url)
                        if "datePublished" in main_entity:
                            date_published: str = main_entity["datePublished"]
                            if date_published:
                                lifecycle_publisher.add_value("date", date_published)
                    # ToDo: add publisher logo handling as soon as our item model supports it
                    #  mainEntity.publisher.logo: logo.@type / logo.url
                    lom.add_value("lifecycle", lifecycle_publisher.load_item())
            if "author" in main_entity:
                author_object: dict = main_entity["author"]
                if author_object and isinstance(author_object, dict):
                    lifecycle_author: LomLifecycleItemloader = LomLifecycleItemloader()
                    lifecycle_author.add_value("role", "author")
                    if "name" in author_object:
                        author_name: str = author_object["name"]
                        if author_name and " " in author_name:
                            author_split: list[str] = author_name.split(sep=" ", maxsplit=1)
                            if author_split and len(author_split) == 2:
                                lifecycle_author.add_value("firstName", author_split[0])
                                lifecycle_author.add_value("lastName", author_split[1])
                        else:
                            lifecycle_author.add_value("firstName", author_name)
                    if "url" in author_object:
                        author_url: str = author_object["url"]
                        if author_url:
                            lifecycle_author.add_value("url", author_url)
                    if "datePublished" in main_entity:
                        date_published: str = main_entity["datePublished"]
                        if date_published:
                            lifecycle_author.add_value("date", date_published)
                    lom.add_value("lifecycle", lifecycle_author.load_item())

        educational = LomEducationalItemLoader()
        if main_entity:
            if "typicalAgeRange" in main_entity:
                typical_age_range_raw: str = main_entity["typicalAgeRange"]
                if typical_age_range_raw and isinstance(typical_age_range_raw, str):
                    if "-" in typical_age_range_raw:
                        # "typicalAgeRange": "15-18"
                        age_regex = re.compile(r"(\d{1,2})-(\d{1,2})")
                        match_age_range: re.Match[str] | None = age_regex.search(typical_age_range_raw)
                        if match_age_range:
                            if len(match_age_range.groups()) == 2:
                                age_range_from: str = match_age_range.group(1)
                                age_range_to: str = match_age_range.group(2)
                                if age_range_from and age_range_to:
                                    age_range_loader: LomAgeRangeItemLoader = LomAgeRangeItemLoader()
                                    age_range_loader.add_value("fromRange", age_range_from)
                                    age_range_loader.add_value("toRange", age_range_to)
                                    educational.add_value("typicalAgeRange", age_range_loader.load_item())
        lom.add_value("educational", educational.load_item())
        base.add_value("lom", lom.load_item())

        vs = ValuespaceItemLoader()
        # the JSON-LD provides new metadata (spotted on 2024-01-25):
        #  - mainEntity.educationalLevel list[str]
        vs.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)
        if main_entity:
            if "about" in main_entity:
                about: list[str] = main_entity.get("about")
                if about:
                    vs.add_value("discipline", about)
            if "audience" in main_entity:
                audience: list[str] = main_entity.get("audience")
                if audience:
                    vs.add_value("intendedEndUserRole", audience)
            if "learningResourceType" in main_entity:
                lrt: list[str] = main_entity.get("learningResourceType")
                if lrt:
                    vs.add_value("learningResourceType", lrt)
            if "oeh:educationalContext" in main_entity:
                educational_context: list[str] = main_entity["oeh:educationalContext"]
                if educational_context:
                    # "oeh:educationalContext": ["Sekundarstufe I", "Sekundarstufe II"]
                    vs.add_value("educationalContext", educational_context)
        vs.add_value("price", "no")
        vs.add_value("conditionsOfAccess", "login_for_additional_features")
        base.add_value("valuespaces", vs.load_item())

        lic = LicenseItemLoader()
        if "author" in main_entity:
            if "name" in main_entity["author"]:
                author_name: str = main_entity["author"]
                if author_name and isinstance(author_name, str):
                    lic.add_value("author", author_name)
        if "license" in main_entity:
            license_url: str = main_entity.get("license")
            if license_url:
                lic.add_value("url", license_url)
        base.add_value("license", lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_itemloader: ResponseItemLoader = ResponseItemLoader()
        if url_data_playwright:
            if html_string:
                response_itemloader.add_value("html", html_string)
            if "screenshot_bytes" in url_data_playwright:
                sbytes: bytes = url_data_playwright["screenshot_bytes"]
                if sbytes:
                    base.add_value("screenshot_bytes", sbytes)
            # KMap doesn't deliver fulltext to neither splash nor playwright.
            # The fulltext object will be showing up as
            #   'text': 'JavaScript wird benötigt!\n\n',
            # in the final "scrapy.Item". As long as KMap doesn't change the way it's delivering its JavaScript content,
            # our crawler won't be able to work around this limitation.
        base.add_value("response", response_itemloader.load_item())
        return base.load_item()
