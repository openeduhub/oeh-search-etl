import re

import scrapy.http
from scrapy.spiders import CrawlSpider

from converter.spiders.base_classes import LomBase


class RpiVirtuellSpider(CrawlSpider, LomBase):
    """
    scrapes materials from https://material.rpi-virtuell.de
    via wp-json API: https://material.rpi-virtuell.de/wp-json/
    """
    name = "rpi_virtuell_debug"
    friendlyName = "rpi-virtuell-debug"
    start_urls = ['https://material.rpi-virtuell.de/wp-json/mymaterial/v1/material/']
    # start_urls = ['https://material.rpi-virtuell.de/wp-json/mymaterial/v1/material/?page=1&per_page=10']
    version = "0.0.1"

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'AUTOTHROTTLE_ENABLED': True,
        # 'DUPEFILTER_DEBUG': True
    }
    wp_json_pagination_parameters = {
        # wp-json API returns up to 100 records per request, depending on the chosen pagination parameters
        # see https://developer.wordpress.org/rest-api/using-the-rest-api/pagination/
        'start_page_number': 1,
        # number of records that should be returned per request:
        'per_page_elements': 100
    }

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def getId(self, response=None) -> str:
        # TODO: getID
        pass

    def getHash(self, response=None) -> str:
        # TODO: getHash
        pass

    def start_requests(self):
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
        # typically we want to iterate through all pages, starting at 1:
        # https://material.rpi-virtuell.de/wp-json/mymaterial/v1/material/?page=1&per_page=100
        # https://material.rpi-virtuell.de/wp-json/mymaterial/v1/material/?page=1&per_page=100&orderby=date&order=desc
        # to find out the maximum number of elements that need to be parsed, we can take a look at the header:
        # response.headers.get("X-WP-TotalPages")
        # depending on the pagination setting (per_page), this will show us how many pages we need to iterate through

        first_page = int(self.get_first_page_parameter())
        last_page = int(self.get_total_pages(response))
        # logging.debug("last page = ", last_page)
        print("LAST PAGE: ", last_page)

        # for i in range(first_page, last_page + 1):
        for i in range(first_page, (10 + 1)):
            url_temp = response.urljoin(
                f'?page={i}&per_page={self.get_per_page_parameter()}&orderby=date&order=desc')
            yield response.follow(url=url_temp, callback=self.parse_page)

        # only use this iteration method if you want to go through pages one-by-one:
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
        temp_url = str(response.url)
        print("DEBUG - INSIDE parse_page: ", temp_url)
        # return LomBase.parse(self, response)
