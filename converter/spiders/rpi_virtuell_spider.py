import logging
import re
from typing import Optional

import scrapy.http
import w3lib.html
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import (
    LomBaseItemloader,
    LomGeneralItemloader,
    LomTechnicalItemLoader,
    LomLifecycleItemloader,
    LomEducationalItemLoader,
    ValuespaceItemLoader,
    LicenseItemLoader,
    ResponseItemLoader,
    BaseItemLoader,
    LomAgeRangeItemLoader,
)
from converter.spiders.base_classes import LomBase
from converter.web_tools import WebEngine

logger = logging.getLogger(__name__)


class RpiVirtuellSpider(CrawlSpider, LomBase):
    """
    scrapes materials from https://material.rpi-virtuell.de
    via wp-json API: https://material.rpi-virtuell.de/wp-json/
    """

    name = "rpi_virtuell_spider"
    friendlyName = "rpi-virtuell"
    start_urls = ["https://material.rpi-virtuell.de/wp-json/mymaterial/v1/material/"]

    version = "0.0.9"  # last update: 2024-01-24

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 12,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 6,
        "WEB_TOOLS": WebEngine.Playwright,
        # 'DUPEFILTER_DEBUG': True
    }
    wp_json_pagination_parameters = {
        # wp-json API returns up to 100 records per request, with the amount of pages in total depending on the chosen
        # pagination parameters, see https://developer.wordpress.org/rest-api/using-the-rest-api/pagination/
        "start_page_number": 0,
        # number of records that should be returned per request:
        "per_page_elements": 100,
    }
    # Mapping "material_bildungsstufe" -> SkoHub:
    # see https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/educationalContext/index.html

    mapping_edu_context = {
        "Arbeit mit Jugendlichen": "",
        "Arbeit mit Kindern": "",
        "Ausbildung": "http://w3id.org/openeduhub/vocabs/educationalContext/berufliche_bildung",
        "Berufsschule": "http://w3id.org/openeduhub/vocabs/educationalContext/berufliche_bildung",
        "Elementarbereich": "http://w3id.org/openeduhub/vocabs/educationalContext/elementarbereich",
        "Erwachsenenbildung": "http://w3id.org/openeduhub/vocabs/educationalContext/erwachsenenbildung",
        "Gemeinde": "",
        "Grundschule": "http://w3id.org/openeduhub/vocabs/educationalContext/grundschule",
        "Kindergottesdienst": "",
        "Konfirmandenarbeit": "",
        "Oberstufe": "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_2",
        "Schulstufen": "",  # alle Schulstufen? age range?
        "Sekundarstufe": "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_1",
        "Unterrichtende": "",
    }
    # copyright is only available as a String (description) on the material_review_url itself, this debug list could be
    # deleted once it's confirmed with rpi-virtuell which OER model they actually use here:
    copyright_debug_list = {
        "Zur Wiederverwendung und Veränderung gekennzeichnet": "",
        "Zur Wiederverwendung und Veränderung gekennzeichnet\t        \t        \t\t        frei zugänglich": "",
        "Zur nicht kommerziellen Wiederverwendung gekennzeichnet": "",
        "Zur nicht kommerziellen Wiederverwendung gekennzeichnet\t        \t        \t\t        frei zugänglich": "",
        "Zur nicht kommerziellen Wiederverwendung und Veränderung gekennzeichnet": "",
        "Zur nicht kommerziellen Wiederverwendung und Veränderung gekennzeichnet"
        "\t        \t        \t\t        frei zugänglich": "",
        "frei zugänglich": "",
        "kostenfrei nach Anmeldung": "",
        "kostenpflichtig": "",
    }
    #   rpi-virtuell has clarified their license-description:
    #   'Zur Wiederverwendung und Veränderung gekennzeichnet' can be both CC_BY and CC_BY_SA
    #       since CC_BY_SA is slightly more restricting, we choose this mapping rather than the more liberal CC_BY
    mapping_copyright_url = {
        "?fwp_lizenz=non-commercial-remixable": Constants.LICENSE_CC_BY_NC_SA_30,
        "?fwp_lizenz=non-commercial-copyable": Constants.LICENSE_CC_BY_NC_ND_40,
        "?fwp_lizenz=remixable": Constants.LICENSE_CC_BY_SA_40,
        "?fwp_verfuegbarkeit=kostenpflichtig": Constants.LICENSE_COPYRIGHT_LAW
        # unclear to map to anything
        # '?fwp_lizenz=copyable': Constants.
    }

    mapping_media_types = {
        "Anforderungssituation": "",
        "Arbeitsblatt": "worksheet",
        "Audio": "audio",
        "Aufgabenstellung": "",
        "Bild": "image",
        "Dossier": "",
        "E-Learning": "",
        "Erzählung": "",
        "Fachinformation": "",  # reference (Primärquelle?)
        "Gamification": "",  # maybe map to educational game ?
        "Gebet/Lied": "",
        "Gottesdienstentwurf": "",
        "Internetportal": "web page",
        "Lernorte": "",
        "Lernstationen": "",
        "Lokale Einrichtung": "",
        "Medien": "audiovisual medium",
        "Online Lesson": "",
        "Praxishilfen": "",
        "Projektplanung": "",
        "Präsentation": "presentation",
        "Text/Aufsatz": "text",
        "Unterrichtsentwurf": "lesson plan",
        "Video": "video",
        "Video im Medienportal": "video",
        "Virtueller Lernort": "",
        "Vorbereitung": "lesson plan",
        "Zeitschrift/Buch": "text",
    }

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def getId(self, response=None) -> str:
        """
        Return the current item URL (resolved "review_url") as a string.
        """
        return response.url

    def getHash(self, response=None) -> Optional[str]:
        """
        Return a string of the last modified date and the version of the crawler as a string.
        """
        date_modified: str = response.xpath('//meta[@property="og:article:modified_time"]/@content').get()
        hash_temp: str = f"{date_modified}v{self.version}"
        return hash_temp

    def start_requests(self):
        """
        Before starting the actual parsing this method determines in which format the url in start_urls was provided.
        If "?page="-query-parameters are missing, it attaches these via urljoin before parsing.
        """
        # typically, we want to iterate through all pages, starting at 1:
        # https://material.rpi-virtuell.de/wp-json/mymaterial/v1/material/?page=1&per_page=100
        # the following method checks if the urls listed in start_urls are in a format that we can use, e.g. either ends
        # with [...]/material/
        # or
        # with [...]/material/?parameters
        for url in self.start_urls:
            if (url.split("/")[-2] == "material") and (url.split("/")[-1] == ""):
                # making sure that the crawler is at the correct url and starting at whatever page we choose:
                first_page_number = self.get_first_page_parameter()
                per_page = self.get_per_page_parameter()
                first_url = url + f"?page={first_page_number}&per_page={per_page}"
                yield scrapy.Request(url=first_url, callback=self.parse)
            elif (url.split("/")[-2] == "material") and (url.split("/") != ""):
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.TextResponse, **kwargs):
        """
        Checks how many pages need to be parsed with the currently set parameters (per_page items) first
        then yields all following scrapy.http.Requests that are needed to iterate through all wp_json pages.
        The individual wp_json-pages are parsed with the "parse_page"-callback
        """
        # to find out the maximum number of elements that need to be parsed, we can take a look at the header:
        # response.headers.get("X-Wp-TotalPages")
        # depending on the pagination setting (per_page parameter)
        # this will show us how many pages we need to iterate through to fetch all elements

        first_page = int(self.get_first_page_parameter())
        last_page = int(self.get_total_pages(response))
        # logging.debug(f"LAST PAGE will be: {last_page}")
        # first_run_page_number helps avoid duplicate requests
        first_run_page_number = self.get_current_page_number(response)
        for i in range(first_page, (last_page + 1)):
            if i == first_run_page_number:
                # since we don't want to create a duplicate scrapy.Request, we can simply parse_page straight away
                i += 1
                yield from self.parse_page(response)
            else:
                url_temp = response.urljoin(f"?page={i}&per_page={self.get_per_page_parameter()}")
                yield response.follow(url=url_temp, callback=self.parse_page)

        # only use this iteration method if you want to (slowly) go through pages one-by-one:
        # yield from self.iterate_through_pages_slowly(current_url, response)

    def iterate_through_pages_slowly(self, current_url, response):
        # this was initially used for debugging purposes and currently isn't used at all anymore
        last_page = int(self.get_total_pages(response))
        current_page_number = self.get_current_page_number(response)
        yield response.follow(current_url, callback=self.parse_page)
        next_page_number = current_page_number + 1
        if current_page_number < last_page:
            # logging.debug(f"Next Page #: {next_page_number}")
            next_url = response.urljoin(f"?page={next_page_number}&per_page={self.get_per_page_parameter()}")
            # logging.debug(f"Next URL will be: {next_url}")
            yield response.follow(next_url, callback=self.parse)

    def get_first_page_parameter(self) -> int:
        """
        :return: first page to crawl as Integer
        """
        return self.wp_json_pagination_parameters.get("start_page_number")

    def get_per_page_parameter(self) -> int:
        """
        getter for the provided "?per_page"-query-parameter, see:
        https://developer.wordpress.org/rest-api/using-the-rest-api/pagination/
        :return: the "?per_page="-parameter as Integer
        """
        return self.wp_json_pagination_parameters["per_page_elements"]

    @staticmethod
    def get_current_page_number(response) -> int:
        """
        use response.url to grab the current position of the crawler from the current url,
        e.g. from: '?page=1&per_page=10' this method will grab the ?page= query parameter

        relevant docs: https://developer.wordpress.org/rest-api/using-the-rest-api/pagination/

        :return: number of the current "wp_json"-page as Integer
        """
        # last part of the current url will look like this: '?page=1&per_page=10'
        last_part_of_url = response.url.split("/")[-1]
        page_regex = re.compile(r"(\?page=)(\d+)")
        current_page_number = int(page_regex.search(last_part_of_url).group(2))
        print("Current Page #: ", current_page_number)
        return current_page_number

    @staticmethod
    def get_total_pages(response) -> str:
        """
        the number of total_pages that are returned by the "wp_json"-API are dependent on which
        "?per_page"-query-parameter was used during a GET-Request.

        This method grabs "X-WP-TotalPages" from the header to determine how many "wp_json"-pages need to be parsed in
        total.

        relevant docs: https://developer.wordpress.org/rest-api/using-the-rest-api/pagination/

        :return: the amount of pages that can be returned by the API
        """
        # the number of total_pages is dependent on how many elements per_page are served during a GET-Request
        if response.headers.get("X-Wp-TotalPages") is not None:
            # X-WP-TotalPages is returned as a byte, therefore we need to decode it first
            total_pages = response.headers.get("X-Wp-TotalPages").decode()
            # logging.debug("Total Pages: ", total_pages)
            return total_pages

    def parse_page(self, response: scrapy.http.TextResponse = None):
        """
        Parses a "wp_json"-page for individual json items. After fetching a json-item, a dictionary consisting of the
        "material_review_url" and a copy of the json item is passed on to the "get_metadata_from_review_url"-method.

        :param response: the current "wp_json"-page that needs to be parsed for individual json items
        """
        # logging.debug("REACHED PARSE_PAGE")
        current_page_json: dict = response.json()

        for item in current_page_json:
            item_copy: dict = item
            wp_json_item = {"id": item_copy.get("material_review_url"), "item": item_copy}
            review_url = item_copy.get("material_review_url")
            yield scrapy.Request(url=review_url, callback=self.get_metadata_from_review_url, cb_kwargs=wp_json_item)

    def get_metadata_from_review_url(self, response: scrapy.http.Response, **kwargs):
        """
        grabs metadata from the "material_review_url"-page and uses the wp_json_item from the
        "parse_page"-method to return a BaseItemLoader with the combined metadata from both sources.

        :param response: the scrapy.http.Response object for the currently parsed page
        :param kwargs: wp_json_item-dictionary
        """
        # logging.debug("DEBUG inside get_metadata_from_review_url: wp_json_item id", kwargs.get("id"))
        wp_json_item = kwargs.get("item")

        if self.shouldImport(response) is False:
            logger.debug(f"Skipping entry {response.url} because shouldImport() returned False")
            return None
        if self.getId(response) is not None and self.getHash(response) is not None:
            if not self.hasChanged(response):
                return None

        base = BaseItemLoader()
        base.add_value("sourceId", self.getId(response=response))
        date_modified: str = response.xpath('//meta[@property="og:article:modified_time"]/@content').get()
        base.add_value("hash", self.getHash(response=response))

        base.add_value("thumbnail", wp_json_item.get("material_screenshot"))
        # base.add_value("lastModified", wp_json_item.get("date"))  # is "date" from wp_json for lastModified correct?
        base.add_value("lastModified", date_modified)  # or is this one better (grabbed from material_review_url)?

        lom = LomBaseItemloader()
        general = LomGeneralItemloader(response=response)
        general.add_value("title", wp_json_item.get("material_titel"))

        # the source material heavily fluctuates between perfectly fine strings and messy (hardcoded) html tags
        # as well as "\n" and "\t", therefore we need to clean up that String first:
        raw_description = wp_json_item.get("material_beschreibung")
        raw_description = w3lib.html.remove_tags(raw_description)
        raw_description = w3lib.html.strip_html5_whitespace(raw_description)
        clean_description = w3lib.html.replace_escape_chars(raw_description)
        general.add_value("description", clean_description)
        general.add_value("identifier", wp_json_item.get("id"))

        kw_temp = list()
        for item in wp_json_item.get("material_schlagworte"):
            kw_temp.append(item.get("name"))
        general.add_value("keyword", kw_temp)
        lom.add_value("general", general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value("format", "text/html")
        technical.add_value("location", wp_json_item.get("material_review_url"))
        lom.add_value("technical", technical.load_item())

        lifecycle = LomLifecycleItemloader()
        date_published = response.xpath('//meta[@property="og:article:published_time"]/@content').get()
        if date_published is not None:
            lifecycle.add_value("date", date_published)
        lom.add_value("lifecycle", lifecycle.load_item())

        educational = LomEducationalItemLoader()
        if wp_json_item.get("material_altersstufe") is not None:
            # age range is returned as a list of <from_age>-<to_age>-Strings, possible return values are:
            # e.g. "01-05", "05-10", "10-13", "13-15", "15-19" and "18-99"
            age_regex = re.compile(r"(\d{1,2})-(\d{1,2})")
            age_range = set()
            age_range_item_loader = LomAgeRangeItemLoader()
            for item in wp_json_item.get("material_altersstufe"):
                age_range_raw: str = item.get("name")
                match_age_from: re.Match[str] | None = age_regex.search(age_range_raw)
                match_age_to: re.Match[str] | None = age_regex.search(age_range_raw)
                if match_age_from:
                    age_from: str = match_age_from.group(1)
                    age_range.add(age_from)
                if match_age_to:
                    age_to: str = match_age_to.group(2)
                    age_range.add(age_to)
            if len(age_range) != 0:
                age_range_item_loader.add_value("fromRange", min(age_range))
                age_range_item_loader.add_value("toRange", max(age_range))
                educational.add_value("typicalAgeRange", age_range_item_loader.load_item())
        lom.add_value("educational", educational.load_item())
        base.add_value("lom", lom.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value("new_lrt", Constants.NEW_LRT_MATERIAL)
        vs.add_value("discipline", "http://w3id.org/openeduhub/vocabs/discipline/520")  # Religion
        # mapping educationalContext
        educational_context = list()
        for edu_con_item in wp_json_item.get("material_bildungsstufe"):
            educational_context.append(edu_con_item.get("name"))
        for edu_item in educational_context:
            if edu_item in self.mapping_edu_context.keys():
                edu_item = self.mapping_edu_context.get(edu_item)
            if edu_item != "":
                vs.add_value("educationalContext", edu_item)

        # using mapped media_type_list for valuespaces -> learningResourceType
        media_type_list = list()
        for item in wp_json_item.get("material_medientyp"):
            media_type_list.append(item.get("name"))
        for media_type_item in media_type_list:
            if media_type_item in self.mapping_media_types.keys():
                media_type_item = self.mapping_media_types.get(media_type_item)
            if media_type_item != "":
                vs.add_value("learningResourceType", media_type_item)
        # see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/learningResourceType/index.html

        # there's metadata for "Kompetenzen" (e.g.: "Deuten", "Gestalten", "Reflexion") within the returned wp_json
        # that our data-model doesn't support yet. for future reference though:
        #   wp_json_item.get("material_kompetenzen") -> list

        vs.add_value("intendedEndUserRole", "teacher")

        lic = LicenseItemLoader()

        # important clarification from rpi-virtuell:
        #   'frei zugänglich' describes 'ungeklärte Lizenz' / 'volles Urheberrecht'
        #   CC licenses > 'frei zugänglich' if both values are found in the license description

        for key in self.mapping_copyright_url:
            if response.xpath('//a[contains(@href,"' + key + '")]').get():
                # the mapping table holds "INTERNAL"-constants, which need to be saved to another field than urls:
                if self.mapping_copyright_url[key] == Constants.LICENSE_COPYRIGHT_LAW:
                    lic.add_value("internal", self.mapping_copyright_url[key])
                else:
                    lic.add_value("url", self.mapping_copyright_url[key])
                break

        # (original assumption during the initial development of this crawler in regard to licenses:
        # by default, all materials should be CC_BY_SA - according to the rpi-virtuell ToS)
        # changed/decided on 2022-10-13: We can't assume that this license is correct and will not set any license

        if response.xpath('//a[contains(@href,"' + "?fwp_verfuegbarkeit=kostenpflichtig" + '")]').get():
            vs.add_value("price", "yes")
        else:
            vs.add_value("price", "no")
        if response.xpath('//a[contains(@href,"' + "?fwp_verfuegbarkeit=kostenfrei-nach-anmeldung" + '")]').get():
            vs.add_value("conditionsOfAccess", "login")

        authors = list()
        # the author should end up in LOM lifecycle, but the returned metadata are too messily formatted to parse them
        # by easy patterns like (first name) + (last name)
        for item in wp_json_item.get("material_autoren"):
            if item.get("name") is not None:
                if item.get("name").strip() != "":
                    authors.append(item.get("name"))
        if len(authors) == 0:
            author_from_header: str = response.xpath('//meta[@name="author"]/@content').get()
            if author_from_header is not None:
                authors.append(author_from_header)
        if len(authors) > 0:
            lic.add_value("author", authors)

        base.add_value("valuespaces", vs.load_item())

        base.add_value("license", lic.load_item())

        contributor = LomLifecycleItemloader()
        publisher = response.xpath('//div[@class="detail-herkunft-organisation"]//a[2]/text()').get()
        if publisher:
            contributor.add_value("role", "metadata_provider")
            contributor.add_value("organization", publisher)
            contributor.add_value("url", response.xpath('//div[@class="detail-herkunft-organisation"]/a/@href').get())
            lom.add_value("lifecycle", contributor.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader = ResponseItemLoader()
        response_loader.add_value("url", response.url)
        base.add_value("response", response_loader.load_item())

        yield base.load_item()
