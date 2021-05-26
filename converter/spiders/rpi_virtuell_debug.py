import html
import json
import logging
import re
from typing import Optional

import scrapy.http
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, ResponseItemLoader, \
    BaseItemLoader
from converter.spiders.base_classes import LomBase


class RpiVirtuellSpider(CrawlSpider, LomBase):
    """
    scrapes materials from https://material.rpi-virtuell.de
    via wp-json API: https://material.rpi-virtuell.de/wp-json/
    """
    name = "rpi_virtuell_debug"
    friendlyName = "rpi-virtuell-debug"
    start_urls = ['https://material.rpi-virtuell.de/wp-json/mymaterial/v1/material/']

    version = "0.0.1"

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'AUTOTHROTTLE_ENABLED': True,
        # 'DUPEFILTER_DEBUG': True
    }
    wp_json_pagination_parameters = {
        # wp-json API returns up to 100 records per request, with the amount of pages total depending on the chosen
        # pagination parameters, see https://developer.wordpress.org/rest-api/using-the-rest-api/pagination/
        'start_page_number': 109,
        # number of records that should be returned per request:
        'per_page_elements': 100
    }
    # Mapping "material_bildungsstufe" -> edu-sharing
    mapping_edu_context = {
        "Arbeit mit Jugendlichen": "",
        "Arbeit mit Kindern": "",
        "Ausbildung": "",
        "Berufsschule": "",
        "Elementarbereich": "",
        "Erwachsenenbildung": "",
        "Gemeinde": "",
        "Grundschule": "",
        "Kindergottesdienst": "",
        "Konfirmandenarbeit": "",
        "Oberstufe": "",
        "Sekundarstufe": "",
        "Schulstufen": "",   # alle Schulstufen?
        "Unterrichtsende": "",
    }

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def getId(self, response=None) -> str:
        """
        returns the review_url of the element
        """
        pass

    def getHash(self, response=None) -> Optional[str]:
        """
        returns a string of the date + version of the crawler
        """
        pass

    def start_requests(self):
        # typically we want to iterate through all pages, starting at 1:
        # https://material.rpi-virtuell.de/wp-json/mymaterial/v1/material/?page=1&per_page=100
        # the following method checks if the urls listed in start_urls are in a format that we can use, e.g. either ends
        # with [...]/material/
        # or
        # with [...]/material/?parameters
        for url in self.start_urls:
            if (url.split('/')[-2] == 'material') and (url.split('/')[-1] == ''):
                # making sure that the crawler is at the correct url and starting at whatever page we choose:
                first_page_number = self.get_first_page_parameter()
                per_page = self.get_per_page_parameter()
                first_url = url + f'?page={first_page_number}&per_page={per_page}'
                yield scrapy.Request(url=first_url, callback=self.parse)
            elif (url.split('/')[-2] == 'material') and (url.split('/') != ''):
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # to find out the maximum number of elements that need to be parsed, we can take a look at the header:
        # response.headers.get("X-WP-TotalPages")
        # depending on the pagination setting (per_page parameter)
        # this will show us how many pages we need to iterate through to fetch all elements

        first_page = int(self.get_first_page_parameter())
        last_page = int(self.get_total_pages(response))
        print("LAST PAGE will be: ", last_page)
        # first_run_page_number helps avoiding duplicate requests
        first_run_page_number = self.get_current_page_number(response)
        for i in range(first_page, (last_page + 1)):
            if i == first_run_page_number:
                # since we don't want to create a duplicate scrapy.Request, we can simply parse_page straight away
                i += 1
                yield from self.parse_page(response)
            else:
                url_temp = response.urljoin(
                    f'?page={i}&per_page={self.get_per_page_parameter()}')
                yield response.follow(url=url_temp, callback=self.parse_page)

        # only use this iteration method if you want to (slowly) go through pages one-by-one:
        # yield from self.iterate_through_pages_slowly(current_url, response)

    def iterate_through_pages_slowly(self, current_url, response):
        last_page = int(self.get_total_pages(response))
        current_page_number = self.get_current_page_number(response)
        yield response.follow(current_url, callback=self.parse_page)
        next_page_number = current_page_number + 1
        if current_page_number < last_page:
            print("Next Page #: ", next_page_number)
            next_url = response.urljoin(f'?page={next_page_number}&per_page={self.get_per_page_parameter()}')
            print("Next URL will be: ", next_url)
            yield response.follow(next_url, callback=self.parse)

    def get_first_page_parameter(self):
        return self.wp_json_pagination_parameters.get("start_page_number")

    def get_per_page_parameter(self):
        return self.wp_json_pagination_parameters["per_page_elements"]

    @staticmethod
    def get_current_page_number(response):
        # last part of the current url will look like this: '?page=1&per_page=10'
        last_part_of_url = response.url.split('/')[-1]
        page_regex = re.compile(r'(\?page=)(\d+)')
        current_page_number = int(page_regex.search(last_part_of_url).group(2))
        print("Current Page #: ", current_page_number)
        return current_page_number

    @staticmethod
    def get_total_pages(response):
        # the number of total_pages is dependant on how many elements per_page are served during a GET-Request
        if response.headers.get("X-WP-TotalPages") is not None:
            # X-WP-TotalPages is returned as a byte, therefore we need to decode it first
            total_pages = response.headers.get("X-WP-TotalPages").decode()
            # logging.debug("Total Pages: ", total_pages)
            return total_pages

    def parse_page(self, response: scrapy.http.Response = None):
        # temp_url = str(response.url)
        # print("DEBUG - INSIDE parse_page: ", temp_url)
        current_page_json = json.loads(response.body)
        # the response.body is pure JSON, each item can be accessed directly:
        for item in current_page_json:
            item_copy = item.copy()
            wp_json_item = {
                "id": item.get("material_review_url"),
                "item": dict(item_copy)
            }
            review_url = item.get("material_review_url")
            yield scrapy.Request(url=review_url, callback=self.get_metadata_from_review_url, cb_kwargs=wp_json_item)

    def get_metadata_from_review_url(self, response, **kwargs):
        # logging.debug("DEBUG inside get_metadata_from_review_url: wp_json_item id", kwargs.get("id"))
        wp_json_item = kwargs.get("item")
        # logging.debug("DEBUG inside get_metadata_from_review_url: response type = ", type(response),
        #               "url =", response.url)

        ld_json_string = response.xpath('/html/head/script[@type="application/ld+json"]/text()').get().strip()
        ld_json_string = html.unescape(ld_json_string)

        ld_json = json.loads(ld_json_string)

        hash_temp: Optional[str] = None
        language_temp: Optional[str] = None
        pub_date: Optional[str] = None
        organization_id: Optional[str] = None
        organization_name: Optional[str] = None
        date_modified: Optional[str] = None
        # this is a workaround to make sure that we actually grab the "dateModified"-Element, no matter where it is:
        # since there seems to be fluctuation how many elements the "@graph"-Array holds, we can't be sure
        # which position "dateModified" actually has:
        # sometimes it's ld_json.get("@graph")[2], sometimes on [3] etc., therefore we must check all of them
        ld_graph_items = ld_json.get("@graph")
        for item in ld_graph_items:
            if item.get("dateModified") is not None:
                date_modified = item.get("dateModified")    # TODO: this could be used instead of "date" in lastModified
                hash_temp = item.get("dateModified") + self.version
            if item.get("@type") == "WebSite":
                language_temp = item.get("inLanguage")
            if item.get("@type") == "WebPage":
                pub_date = item.get("datePublished")
            if item.get("@type") == "Organization":
                organization_id = item.get("@id")
                organization_name = item.get("name")

        # TODO: use hasChanged here?
        base = BaseItemLoader()
        base.add_value("sourceId", response.url)
        base.add_value("hash", hash_temp)
        # base.add_value("response", super().mapResponse(response).load_item())
        base.add_value("type", Constants.TYPE_MATERIAL)  # TODO: is this correct? use mapping for edu-context?
        # TODO: enable thumbnail when done with debugging
        # base.add_value("thumbnail", item.get("material_screenshot"))
        # base.add_value("lastModified", wp_json_item.get("date"))  # TODO: is date for lastModified correct?
        base.add_value("lastModified", date_modified)   # or is this one better?

        lom = LomBaseItemloader()
        general = LomGeneralItemloader(response=response)
        general.add_value("title", wp_json_item.get("material_titel"))
        general.add_value("description", html.unescape(wp_json_item.get("material_beschreibung")))
        general.add_value("identifier", wp_json_item.get("id"))
        if language_temp is not None:
            general.add_value("language", language_temp)

        kw_temp = list()    # TODO: keywords (-> is mapping needed from "material_schlagworte"-dictionary?)
        for item in wp_json_item.get("material_schlagworte"):
            kw_temp.append(item.get("name"))
        general.add_value("keyword", kw_temp)
        lom.add_value("general", general.load_item())

        technical = LomTechnicalItemLoader()
        # TODO: technical format -> hardcode to text/html? or grab from "material_medientyp"
        medien_typ = list()
        for item in wp_json_item.get("material_medientyp"):
            medien_typ.append(item.get("name"))
        # technical.add_value("format", )   # TODO: format
        technical.add_value("location", wp_json_item.get("material_review_url"))
        lom.add_value("technical", technical.load_item())

        lifecycle = LomLifecycleItemloader()
        if organization_name is not None:
            lifecycle.add_value("organization", organization_name)
        if organization_id is not None:
            lifecycle.add_value("url", organization_id)
        if pub_date is not None:
            lifecycle.add_value("date", pub_date)
        lom.add_value("lifecycle", lifecycle.load_item())

        educational = LomEducationalItemLoader()
        lom.add_value("educational", educational.load_item())
        base.add_value("lom", lom.load_item())

        vs = ValuespaceItemLoader()
        # TODO: audience, discipline, learningResourceType
        #   wp_json_item.get("material_altersstufe") -> list
        #   wp_json_item.get("material_medientyp") -> list
        #   wp_json_item.get("material_bildungsstufe") -> list
        #   wp_json_item.get("material_kompetenzen") -> list
        vs.add_value("intendedEndUserRole", "teacher")

        base.add_value("valuespaces", vs.load_item())

        lic = LicenseItemLoader()
        license_description = response.xpath('//div[@class="material-detail-meta-access material-meta"]'
                                             '/div[@class="material-meta-content-entry"]/text()').get()
        if license_description is not None:
            license_description = html.unescape(license_description.strip())
            lic.add_value("description", license_description)
        # TODO:
        #  - license-url
        authors = list()
        for item in wp_json_item.get("material_autoren"):
            if item.get("name") is not None or item.get("name").strip() is not "":
                authors.append(item.get("name"))
        lic.add_value("author", authors)    # TODO: material_autoren -> LOM license or lifecycle?

        base.add_value("license", lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader = ResponseItemLoader()
        base.add_value("response", response_loader.load_item())

        yield base.load_item()
