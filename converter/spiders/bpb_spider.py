import html
from io import BytesIO
from typing import Any, Iterable, Union

import extruct
import scrapy
from lxml import objectify
from lxml.etree import ElementTree
from lxml.objectify import ObjectifiedElement
from scrapy import Request
from scrapy.http import Response
from twisted.internet.defer import Deferred

from converter.spiders.base_classes import LomBase
from ..constants import Constants
from ..es_connector import EduSharing
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
    LomClassificationItemLoader,
    PermissionItemLoader,
)
from ..web_tools import WebEngine


class BpbSpider(scrapy.Spider, LomBase):
    name = "bpb_spider"
    url = "https://www.bpb.de"
    friendlyName = "Bundeszentrale für politische Bildung"
    start_urls = ["https://www.bpb.de/sitemap.xml?page=1", "https://www.bpb.de/sitemap.xml?page=2"]
    # the most-current sitemap can be found at the bottom of the robots.txt file (see: https://www.bpb.de/robots.txt )
    # and contains a sitemap-index,
    # e.g.: https://www.bpb.de/sites/default/files/xmlsitemap/oWx2Pl033k1XFmYJFOs7sO0G3JasH0cjDbduvDwKuwo/index.xml
    # an additional, human-readable sitemap (HTML) can be found at: https://www.bpb.de/sitemap/
    allowed_domains = ["bpb.de"]
    deny_list: list[str] = [
        "/die-bpb/",
        "/impressum/",
        "/kontakt/",
        "/redaktion/",
        "/shop/",
        "/veranstaltungen/",  # ToDo: implement custom handling for events in a future version
    ]
    deny_list_endswith: list[str] = ["/impressum", "/kontakt", "/redaktion"]
    version = "0.2.3"  # last update: 2024-04-10
    # (first version of the crawler after bpb.de completely relaunched their website in 2022-02)
    custom_settings = {
        "WEB_TOOLS": WebEngine.Playwright,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 5,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 2,
    }
    DEBUG_DROPPED_ITEMS: set[str] = set()
    DEBUG_UNIQUE_URLS_TO_BE_CRAWLED: set[str] = set()
    DEBUG_XML_COUNT: int = 0

    def __init__(self, **kwargs):
        scrapy.Spider.__init__(self, **kwargs)
        LomBase.__init__(self, **kwargs)

    def close(self, reason: str) -> Union[Deferred, None]:
        # ToDo (optional): extend functionality by counting filtered duplicates as well
        #  (-> extend Scrapy Dupefilter logging)
        self.logger.info(f"Closing spider (reason: {reason} )...")
        if self.DEBUG_XML_COUNT:
            self.logger.info(
                f"Summary: The sitemap index contained {self.DEBUG_XML_COUNT} (unfiltered) XML elements in total."
            )
        if self.DEBUG_UNIQUE_URLS_TO_BE_CRAWLED:
            self.logger.info(f"Summary: Unique URLs to be crawled: {len(self.DEBUG_UNIQUE_URLS_TO_BE_CRAWLED)}")
        if self.DEBUG_DROPPED_ITEMS:
            self.logger.info(
                f"Summary: Items filtered / dropped (due to sitemap rules "
                f"(see: 'deny_list'-variable / robot meta tags etc.): "
                f"{len(self.DEBUG_DROPPED_ITEMS)}"
            )
        return

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_sitemap, priority=2)

    def parse_sitemap(self, response: Response):
        if response:
            xml: ElementTree = objectify.parse(BytesIO(response.body))
            xml_root: ObjectifiedElement = xml.getroot()
            xml_count: int = len(xml_root.getchildren())
            if xml_count:
                self.logger.info(f"Sitemap {response.url} contained {xml_count} XML elements in total.")
                self.DEBUG_XML_COUNT += xml_count
            ns_map = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            for xml_element in xml_root.findall("ns:url", ns_map):
                # we're only interested in the <loc> of an <url> element, e.g.:
                # <url>
                # 		<loc>https://www.bpb.de/themen/medien-journalismus/netzdebatte/179637/big-data-ein-ungezaehmtes-tier-mit-grossem-potential-ein-interview-mit-frank-schirrmacher/</loc>
                # 		<lastmod>2022-02-07T16:25Z</lastmod>
                # 		<changefreq>yearly</changefreq>
                # 		<priority>0.6</priority>
                # 	</url>
                item_url: str = xml_element.loc.text
                # xml_element.loc is a StringElement -> by calling .text on it, we get the string value
                drop_item_flag: bool = False
                for partial_url in self.deny_list:
                    # since the sitemaps are huge (56.880 urls in total),
                    # we try to not cause HTTP Requests for items that would be dropped anyway
                    if item_url and partial_url in item_url:
                        # URLs which should not be crawled are dropped and logged.
                        # At the end of the crawl process, a counter will display the amount of dropped items for
                        # debugging purposes.
                        drop_item_flag = True
                        # self.logger.debug(f"Dropping item {item_url} due to sitemap rules.")  # this one is spammy!
                        self.DEBUG_DROPPED_ITEMS.add(item_url)
                for url_ending_with_str in self.deny_list_endswith:
                    if item_url and item_url.endswith(url_ending_with_str):
                        # URLs that end with "/impressum", "/kontakt" or "/redaktion" are "Impressum"-like pages which
                        # need to be checked separately from the deny_list.
                        drop_item_flag = True
                        self.DEBUG_DROPPED_ITEMS.add(item_url)
                if not drop_item_flag:
                    self.DEBUG_UNIQUE_URLS_TO_BE_CRAWLED.add(item_url)
                    yield scrapy.Request(url=item_url, callback=self.parse, meta={"dont_merge_cookies": True})
                    # the flag 'dont_merge_cookies' is necessary because bpb.de apparently uses Drupal's BigPipe
                    # implementation, which sets a "no-js"-cookie. After receiving that cookie, all subsequent requests
                    # are 404s and invalid. Invalid responses contain a "/big_pipe/no-js?destination=" path in their URL
            if self.DEBUG_UNIQUE_URLS_TO_BE_CRAWLED:
                self.logger.info(
                    f"Unique URLs to be crawled after parsing sitemap {response.url} : "
                    f"{len(self.DEBUG_UNIQUE_URLS_TO_BE_CRAWLED)}"
                )

    @staticmethod
    def get_json_ld_property(json_lds: list[dict], property_name: str) -> Any | None:
        # JSON-LD embeds on bpb.de typically look like this (best-case scenario):
        # {
        #     "@context": "http:\/\/schema.org",
        #     "@type": "Article",
        #     "author": "Bundeszentrale f\u00fcr politische Bildung",
        #     "headline": "Die USA zwischen Internationalismus und Isolationismus",
        #     "datePublished": "2023-02-02",
        #     "dateCreated": "2023-01-25",
        #     "dateModified": "2023-02-02",
        #     "mainEntityOfPage": "https:\/\/www.bpb.de\/themen\/nordamerika\/usa\/517667\/die-usa-zwischen-internationalismus-und-isolationismus\/",
        #     "description": "Die USA sind die bedeutendste Weltordnungsmacht. Doch immer wieder scheint ihre Au\u00dfen- und Sicherheitspolitik zwischen den beiden Extremen Internationalismus und Isolationismus hin und her zu pendeln. Wie kommt es dazu?",
        #     "keywords": "USA,Au\u00dfenpolitik der USA,Weltordnung,Internationalismus,Isolationismus",
        #     "publisher": {
        #         "@type": "Organization",
        #         "name": "Bundeszentrale f\u00fcr politische Bildung",
        #         "logo": {
        #             "@type": "ImageObject",
        #             "url": "https:\/\/www.bpb.de\/themes\/custom\/bpbtheme\/images\/bpb_logo_ldjson.jpg",
        #             "width": "144",
        #             "height": "60"
        #         }
        #     },
        #     "image": {
        #         "@type": "ImageObject",
        #         "url": "https:\/\/www.bpb.de\/cache\/images\/7\/759897_teaser_3x2_800.jpg?0326D",
        #         "width": 800,
        #         "height": 534
        #     }
        # }
        if json_lds and isinstance(json_lds, list):
            for json_ld in json_lds:
                if property_name in json_ld:
                    property_value = json_ld.get(property_name)
                    if property_value and isinstance(property_value, str):
                        property_value = html.unescape(property_value)
                    return property_value
        else:
            return None

    @staticmethod
    def get_opengraph_property(opengraph_dict: dict, property_name: str) -> Any | None:
        # after using extruct for the opengraph data, the resulting dictionary will have a 'opengraph'-key if
        # extraction was successful. Within that key there will be a list[dict].
        if opengraph_dict and isinstance(opengraph_dict, dict):
            if "opengraph" in opengraph_dict:
                og_list: list[dict] = opengraph_dict["opengraph"]
                for opengraph in og_list:
                    if property_name in opengraph:
                        return opengraph.get(property_name)
        else:
            return None

    def getId(self, response: Response = None, json_lds: list[dict] = None, opengraph: dict = None) -> str:
        item_url: str = str()
        if json_lds:
            main_entity_of_page: str = self.get_json_ld_property(json_lds, property_name="mainEntityOfPage")
            if main_entity_of_page:
                main_entity_of_page: str = html.unescape(main_entity_of_page)
                item_url = main_entity_of_page
        if opengraph:
            og_url: str = self.get_opengraph_property(opengraph_dict=opengraph, property_name="og:url")
            if og_url:
                item_url = og_url
        if item_url:
            return item_url
        elif response:
            self.logger.debug(
                f"Item {response.url} did not provide a stable ID (url). Falling back to response.url ..."
            )
            return response.url

    def getHash(self, response: Response = None, json_lds: list[dict] = None) -> str:
        hash_str: str | None = None
        if json_lds:
            json_ld_date_modified: str = self.get_json_ld_property(json_lds, property_name="dateModified")
            json_ld_date_created: str = self.get_json_ld_property(json_lds, property_name="dateCreated")
            json_ld_date_published: str = self.get_json_ld_property(json_lds, property_name="datePublished")
            if json_ld_date_modified:
                # 'dateModified' is our first priority: this will be the most precise date for hash checks
                hash_str = f"{json_ld_date_modified}v{self.version}"
                return hash_str
            elif json_ld_date_created:
                hash_str = f"{json_ld_date_created}v{self.version}"
                return hash_str
            elif json_ld_date_published:
                hash_str = f"{json_ld_date_published}v{self.version}"
                return hash_str
        if hash_str is None and response:
            # fallback to DOM meta property 'last-modified' if the JSON-LD didn't provide a more precise date
            meta_last_modified: str = response.xpath("//meta[@name='last-modified']/@content").get()
            if meta_last_modified:
                hash_str = f"{meta_last_modified}v{self.version}"
                return hash_str

    def get_keywords(self, response: Response = None, json_lds: list[dict] = None) -> list[str] | None:
        # ToDo: if 'keywords' become available in the HTML header (in the future), we might need the Response object as
        #  our fallback for edge-cases where no JSON-LD was available.
        if json_lds:
            json_ld_keywords: str = self.get_json_ld_property(json_lds, property_name="keywords")
            if json_ld_keywords:
                if json_ld_keywords.strip():
                    if "," in json_ld_keywords:
                        # default case for German articles
                        return [keyword.strip() for keyword in json_ld_keywords.split(",")]
                    if ";" in json_ld_keywords:
                        # edge case: international articles (English / French) often have keywords split by semicolon
                        return [keyword.strip() for keyword in json_ld_keywords.split(";")]
        else:
            return None

    def has_changed(self, response: Response, identifier: str, hash_str: str) -> bool:
        identifier: str = identifier
        hash_str: str = hash_str
        uuid_str: str = self.getUUID(response)
        if self.forceUpdate:
            return True
        if self.uuid:
            if uuid_str == self.uuid:
                self.logger.info(f"Matched requested uuid: {self.uuid} ({identifier}).")
                return True
            return False
        if self.remoteId:
            if identifier == self.remoteId:
                self.logger.info(f"Matched requested remoteId {self.remoteId} ({identifier}).")
                return True
            return False
        db = EduSharing().find_item(identifier, self)
        changed = db is None or db[1] != hash_str
        if not changed:
            self.logger.info(f"Item {identifier} has not changed.")
        return changed

    def check_if_item_should_be_dropped(self, response, json_lds, opengraph_dict) -> bool:
        drop_item_flag: bool = False
        identifier: str = self.getId(response=response, json_lds=json_lds, opengraph=opengraph_dict)
        hash_str: str = self.getHash(response=response, json_lds=json_lds)
        if self.shouldImport(response) is False:
            self.logger.info(f"Skipping entry {identifier} because shouldImport() returned 'False'.")
            drop_item_flag = True
        if identifier is not None and hash_str is not None:
            if not self.has_changed(response=response, identifier=identifier, hash_str=hash_str):
                drop_item_flag = True
        robot_meta_tags: list[str] = response.xpath("//meta[@name='robots']/@content").getall()
        if robot_meta_tags:
            # see: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
            if "noindex" in robot_meta_tags or "none" in robot_meta_tags:
                self.logger.info(
                    f"Robot Meta Tag {robot_meta_tags} identified. Robot Meta Tags 'noindex' or 'none' should "
                    f"be skipped by the crawler. Dropping item {response.url} ."
                )
                drop_item_flag = True
        return drop_item_flag

    async def parse(self, response: Response, **kwargs: Any) -> Any:
        jslde = extruct.JsonLdExtractor()
        json_lds: list[dict] = jslde.extract(response.body)
        opengraph_dict: dict = extruct.extract(htmlstring_or_tree=response.body, syntaxes=["opengraph"], uniform=True)

        drop_item_flag = self.check_if_item_should_be_dropped(response, json_lds, opengraph_dict)
        if drop_item_flag:
            self.DEBUG_DROPPED_ITEMS.add(response.url)
            return

        base_itemloader: BaseItemLoader = BaseItemLoader()

        source_id: str = self.getId(response=response, json_lds=json_lds, opengraph=opengraph_dict)
        base_itemloader.add_value("sourceId", source_id)
        hash_value: str = self.getHash(response=response, json_lds=json_lds)
        base_itemloader.add_value("hash", hash_value)

        json_ld_date_modified: str = self.get_json_ld_property(json_lds, property_name="dateModified")
        if json_ld_date_modified:
            base_itemloader.add_value("lastModified", json_ld_date_modified)

        json_ld_image: dict = self.get_json_ld_property(json_lds, property_name="image")
        og_image: str = self.get_opengraph_property(opengraph_dict, property_name="og:image")
        og_image_url: str = self.get_opengraph_property(opengraph_dict, property_name="og:image:url")
        # og_image_alt: str = self.get_opengraph_property(opengraph_dict, property_name="og:image:alt")
        # ToDo: the image altLabel cannot be saved yet, there exists no edu-sharing attribute in items.py (yet)
        # og_image_type: str = self.get_opengraph_property(opengraph_dict, property_name="og:image:type")
        # ToDo: the image type cannot be saved yet, there exists no edu-sharing property in items.py (yet)
        if json_ld_image and "url" in json_ld_image:
            image_url: str = json_ld_image.get("url")
            image_url = html.unescape(image_url)
            if image_url and image_url != "https://www.bpb.de":
                # there are hundreds of items with wrong JSON-LD metadata.
                # (e.g.: https://www.bpb.de/kurz-knapp/lexika/politiklexikon/296491/shitstorm/ )
                # The image object will typically look like this one:
                # "image": {
                #         "@type": "ImageObject",
                #         "url": "https:\/\/www.bpb.de",
                #         "width": "",
                #         "height": ""
                #     }
                # since the above item is not a valid ImageObject, we need to make sure to not save those urls
                base_itemloader.add_value("thumbnail", image_url)
        elif og_image:
            base_itemloader.add_value("thumbnail", og_image)
        elif og_image_url:
            base_itemloader.add_value("thumbnail", og_image_url)

        lom_base_itemloader: LomBaseItemloader = LomBaseItemloader()

        general_itemloader: LomGeneralItemloader = LomGeneralItemloader()
        json_ld_headline: str = self.get_json_ld_property(json_lds, property_name="headline")
        og_title: str = self.get_opengraph_property(opengraph_dict, property_name="og:title")
        if json_ld_headline:
            general_itemloader.add_value("title", json_ld_headline)
        elif og_title:
            general_itemloader.add_value("title", og_title)

        ambiguous_titles: list[str] = [
            "glossar",
            "links",
            "links zum thema",
            "literatur",
            "weiterführende links",
        ]
        retrieved_titles: list[str] | None = general_itemloader.get_collected_values("title")
        if retrieved_titles and isinstance(retrieved_titles, list):
            for retrieved_title in retrieved_titles:
                if retrieved_title and isinstance(retrieved_title, str):
                    retrieved_title_lc = retrieved_title.lower()
                    if retrieved_title_lc and retrieved_title_lc in ambiguous_titles:
                        # There are edge-cases where the title is too ambiguous to be useful for an end-user.
                        # If we encounter such "useless" titles,
                        # we'll try to use the breadcrumbs as a fallback and build a string
                        breadcrumbs_clickable_raw: list[str] | None = response.xpath(
                            "//nav[@class='breadcrumbs']//li[@class='breadcrumbs__item']//a/text()"
                        ).getall()
                        # clickable breadcrumbs items have a different CSS class than the last word and need to be
                        # extracted separately
                        breadcrumbs_last_word: str | None = response.xpath(
                            "//ol[@class='breadcrumbs__list']//li[last()]//*[last()]/text()"
                        ).get()
                        if breadcrumbs_clickable_raw and isinstance(breadcrumbs_clickable_raw, list):
                            breadcrumbs_title: str = " > ".join(breadcrumbs_clickable_raw)
                            if breadcrumbs_last_word and isinstance(breadcrumbs_last_word, str):
                                # assemble the final string by appending the last, non-clickable word, e.g.:
                                # "Themen > Politik > ... > Glossar"
                                breadcrumbs_title = f"{breadcrumbs_title} > {breadcrumbs_last_word}"
                            general_itemloader.replace_value("title", breadcrumbs_title)

        keywords: list[str] | None = self.get_keywords(response=response, json_lds=json_lds)
        if keywords:
            general_itemloader.add_value("keyword", keywords)

        json_ld_description: str = self.get_json_ld_property(json_lds, property_name="description")
        og_description: str = self.get_opengraph_property(opengraph_dict, property_name="og:description")
        if json_ld_description:
            general_itemloader.add_value("description", json_ld_description)
        elif og_description:
            general_itemloader.add_value("description", og_description)
        identifier_url: str = self.getId(response=response, json_lds=json_lds)
        if identifier_url:
            general_itemloader.add_value("identifier", identifier_url)
        in_language: str = self.get_json_ld_property(json_lds, property_name="inLanguage")
        if in_language:
            general_itemloader.add_value("language", in_language)
        else:
            html_language: str = response.xpath("//html/@lang").get()
            if html_language:
                general_itemloader.add_value("language", html_language)

        technical_itemloader: LomTechnicalItemLoader = LomTechnicalItemLoader()
        technical_itemloader.add_value("format", "text/html")
        # ToDo: confirm if hard-coding "text/html" is still a desired pattern for crawler items
        if source_id.startswith("http"):
            technical_itemloader.add_value("location", source_id)
        og_url: str = self.get_opengraph_property(opengraph_dict, property_name="og:url")
        if source_id != response.url or og_url and source_id != og_url:
            # make sure to only save values that are different from our URL identifier
            if response.url != og_url:
                technical_itemloader.add_value("location", og_url)
                technical_itemloader.add_value("location", response.url)
            elif og_url:
                technical_itemloader.add_value("location", og_url)
            else:
                technical_itemloader.add_value("location", response.url)

        json_ld_date_published: str = self.get_json_ld_property(json_lds, property_name="datePublished")
        json_ld_date_created: str = self.get_json_ld_property(json_lds, property_name="dateCreated")

        json_ld_author: str = self.get_json_ld_property(json_lds, property_name="author")
        if json_ld_author:
            lifecycle_author: LomLifecycleItemloader = LomLifecycleItemloader()
            lifecycle_author.add_value("role", "author")
            if json_ld_author == "Bundeszentrale für politische Bildung":
                lifecycle_author.add_value("organization", json_ld_author)
            else:
                # author names cannot be (safely) split into firstName / lastName by comma because the strings vary too
                # much to make a safe assumption. Oftentimes commas indicate a specification, not a separate person:
                # e.g. "Judyth Twigg (Virginia Commonwealth University, Richmond)"
                # therefore we have no other choice than saving the complete string to firstName
                lifecycle_author.add_value("firstName", json_ld_author)
            if json_ld_date_published:
                lifecycle_author.add_value("date", json_ld_date_published)
            elif json_ld_date_created:
                lifecycle_author.add_value("date", json_ld_date_created)
            lom_base_itemloader.add_value("lifecycle", lifecycle_author.load_item())

        json_ld_publisher: dict = self.get_json_ld_property(json_lds, property_name="publisher")
        if json_ld_publisher:
            # a typical "publisher"-dict looks like this:
            # "publisher": {
            #     "@type": "Organization",
            #     "name": "Bundeszentrale f\u00fcr politische Bildung",
            #     "logo": {
            #         "@type": "ImageObject",
            #         "url": "https:\/\/www.bpb.de\/themes\/custom\/bpbtheme\/images\/bpb_logo_ldjson.jpg",
            #         "width": "144",
            #         "height": "60"
            #     }
            # }
            publisher_name: str = str()
            publisher_type: str = str()
            lifecycle_publisher: LomLifecycleItemloader = LomLifecycleItemloader()
            lifecycle_publisher.add_value("role", "publisher")
            if "name" in json_ld_publisher:
                publisher_name: str = json_ld_publisher.get("name")
            if "@type" in json_ld_publisher:
                publisher_type: str = json_ld_publisher.get("@type")
            if publisher_type and publisher_type == "Organization" and publisher_name:
                lifecycle_publisher.add_value("organization", publisher_name)
            elif publisher_type and publisher_type == "Person" and publisher_name:
                lifecycle_publisher.add_value("firstName", publisher_name)
            if json_ld_date_published:
                lifecycle_publisher.add_value("date", json_ld_date_published)
            elif json_ld_date_created:
                lifecycle_publisher.add_value("date", json_ld_date_created)
            lom_base_itemloader.add_value("lifecycle", lifecycle_publisher.load_item())

        educational_itemloader: LomEducationalItemLoader = LomEducationalItemLoader()
        if in_language:
            educational_itemloader.add_value("language", in_language)

        classification_itemloader: LomClassificationItemLoader = LomClassificationItemLoader()

        vs_itemloader: ValuespaceItemLoader = ValuespaceItemLoader()
        vs_itemloader.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)
        json_ld_type: str = self.get_json_ld_property(json_lds, property_name="@type")
        og_type: str = self.get_opengraph_property(opengraph_dict, property_name="og:type")
        if json_ld_type:
            vs_itemloader.add_value("new_lrt", json_ld_type)
        elif og_type:
            vs_itemloader.add_value("new_lrt", og_type)
        if "/lexika/" in response.url:
            vs_itemloader.add_value("new_lrt", "c022c920-c236-4234-bae1-e264a3e2bdf6")
            # Nachschlagewerk und Glossareintrag
        if "/taegliche-dosis-politik/" in response.url:
            vs_itemloader.add_value("new_lrt", "dc5763ab-6f47-4aa3-9ff3-1303efbeef6e")
            # Nachricht und Neuigkeit
        if "/mediathek/" in response.url and "/podcast/" not in response.url:
            vs_itemloader.add_value("new_lrt", "7a6e9608-2554-4981-95dc-47ab9ba924de")
            # Video (Material)
        if "/podcasts/" in response.url:
            vs_itemloader.add_value("new_lrt", "6e821748-ad12-4ac1-bb14-9b54493e2c50")
            # Radio, Podcastfolge und Interview
        # ToDo: valuespaces vocabs
        #  - intendedEndUserRole?
        #  - educationalContext?
        #  - dataProtectionConformity?
        vs_itemloader.add_value("discipline", ["480", "240"])  # Politik, Geschichte
        if "/wirtschaft/" in response.url:
            vs_itemloader.add_value("discipline", "700")  # Wirtschaftskunde
        if "/umwelt/" in response.url:
            vs_itemloader.add_value("discipline", "640")  # Umwelterziehung
        if "/medienpaedagogik/" in response.url:
            vs_itemloader.add_value("discipline", "900")  # Medienbildung
        vs_itemloader.add_value("conditionsOfAccess", "no_login")
        vs_itemloader.add_value("containsAdvertisement", "no")
        vs_itemloader.add_value("price", "no")

        license_itemloader: LicenseItemLoader = LicenseItemLoader()
        if json_ld_author:
            license_itemloader.add_value("author", json_ld_author)
        license_url: str = response.xpath("//div[@class='article-license']//a[@rel='license']/@href").get()
        if license_url:
            license_itemloader.add_value("url", license_url)

        permission_itemloader: PermissionItemLoader = super().getPermissions(response)

        response_itemloader: ResponseItemLoader = await super().mapResponse(response=response)

        lom_base_itemloader.add_value("general", general_itemloader.load_item())
        lom_base_itemloader.add_value("technical", technical_itemloader.load_item())
        lom_base_itemloader.add_value("educational", educational_itemloader.load_item())
        lom_base_itemloader.add_value("classification", classification_itemloader.load_item())

        base_itemloader.add_value("lom", lom_base_itemloader.load_item())
        base_itemloader.add_value("license", license_itemloader.load_item())
        base_itemloader.add_value("valuespaces", vs_itemloader.load_item())
        base_itemloader.add_value("permissions", permission_itemloader.load_item())
        base_itemloader.add_value("response", response_itemloader.load_item())

        yield base_itemloader.load_item()
