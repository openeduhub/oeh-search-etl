import re

import scrapy
import w3lib.html

from converter.constants import Constants
from converter.items import LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, LomLifecycleItemloader, \
    LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, ResponseItemLoader
from converter.spiders.base_classes import LomBase


class GinkgoMapsSpider(scrapy.Spider, LomBase):
    name = "ginkgomaps_spider"
    friendlyName = "GinkgoMaps"
    allowed_domains = ["ginkgomaps.com"]
    start_urls = [
        "http://ginkgomaps.com/index_de.html"
    ]
    version = "0.0.1"  # reflects the structure of Ginkgomaps.com on 2021-10-04

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }
    skip_these_urls = [
        "index_de.html",
        "datenschutz.html",
        "impressum.html",
        "http://www.mygeo.info"
    ]

    navigation_urls = set()
    debug_parsed_urls = set()
    debug_dead_end_counter = int()

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.get_navigation_urls_first_level)

    def crawl_next_url_level(self, diff_set, response: scrapy.http.Response, url_depth: int):
        # To fetch all sub-pages of the website, we must grab all the unique urls from the navigation sidebar first
        # The sidebar has several levels, e.g.:
        # Welt                      1st level links (= url_depth 1)
        #   Afrika                  2nd level links (= url_depth 2)
        #       Afrika ( - D)       3rd level links (= url_depth 3)
        #           Ägypten         4th level links (= url_depth 4)
        # each of these layers has its own .html and only shows the child-links if you navigate through the parent-node.
        # For example, to see "landkarten_aegypten.html", we need to be on the "Afrika ( - D)"-level of the sidebar.

        if diff_set.issubset(self.navigation_urls) is False:
            self.navigation_urls.update(diff_set)
            if len(diff_set) > 0:
                # print("Found", (len(diff_set)), "new URLs to crawl on url_depth =", url_depth)
                for diff_item in diff_set:
                    # print(diff_item)
                    temp_url = response.urljoin(diff_item)
                    if url_depth == 1:
                        yield scrapy.Request(url=temp_url, callback=self.get_navigation_urls_second_level)
                    if url_depth == 2:
                        yield scrapy.Request(url=temp_url, callback=self.get_navigation_urls_third_level)
                    if url_depth == 3:
                        yield scrapy.Request(url=temp_url, callback=self.get_navigation_urls_fourth_level)

    def check_for_dead_ends_before_parsing(self, response: scrapy.http.Response):
        """
        Checks if the current response.url has already been parsed or is on the "skip_these_urls"-list.
        If the current url hasn't been parsed already, copies the response and calls parse to gather metadata
        from the current .html
        :param response:
        :return:
        """
        if response is not None:
            # Only call the parse method if the current url is no dead-end without content:
            table_body = response.xpath('//table[@class="smalltable"]')
            if table_body is not None:
                no_entry_regex = re.compile(r'Bisher kein Eintrag')
                for table_item in table_body:
                    if (no_entry_regex.search(table_item.get())) is not None:
                        self.debug_dead_end_counter += 1
                        # print("The URL", response.url, "is a 'Bisher kein Eintrag'-dead-end.")
                        # print("check_for_dead_ends... Method: already parsed URLs =", len(self.debug_parsed_urls),
                        #       "| gathered urls =", len(self.navigation_urls), "| skip_these_urls =",
                        #       len(self.skip_these_urls), "| Total amount of dead-ends:", self.debug_dead_end_counter)

                    # check if the current url has already been parsed:
                    elif (response.url not in self.debug_parsed_urls) and (response is not None):
                        # check if current url contains an undesired url-pattern
                        skip_check = False
                        for url_pattern in self.skip_these_urls:
                            current_regex = re.compile(url_pattern)
                            if current_regex.search(response.url) is not None:
                                skip_check = True
                        # if the current url is a "fresh" one, call the parse method to extract metadata
                        if skip_check is False:
                            # print("URL TO BE PARSED: ", response.url)
                            self.debug_parsed_urls.add(response.url)
                            response_copy = response.copy()
                            yield from self.parse(response_copy)

    def getHash(self, response=None) -> str:
        pass

    def getId(self, response=None) -> str:
        pass

    def get_navigation_urls_first_level(self, response: scrapy.http.Response):
        """

        Scrapy Contracts:
        @url http://ginkgomaps.com/index_de.html
        @returns requests 5
        """
        url_depth = 1

        yield from self.check_for_dead_ends_before_parsing(response)
        temp_set = set()

        nav_sidebar = response.xpath('/html/body/center/table[1]/tr[2]/td[1]/table')

        for item in nav_sidebar.xpath('tr/td[@class="NavCell"]'):
            # nav_name = item.xpath('a[@class="NavLink"]/text()').get()
            nav_url = item.xpath('a[@class="NavLink"]/@href').get()
            if nav_url is not None:
                temp_set.add(nav_url)

        temp_set.difference_update(self.skip_these_urls)
        diff_set = temp_set.difference(self.navigation_urls)

        yield from self.crawl_next_url_level(diff_set, response, url_depth)

    def get_navigation_urls_second_level(self, response: scrapy.http.Response):
        """

        @url http://ginkgomaps.com/landkarten_amerikanische_jungferninseln.html
        @returns requests 3
        """
        url_depth = 2
        yield from self.check_for_dead_ends_before_parsing(response)
        temp_set = set()

        nav_sidebar = response.xpath('/html/body/center/table[1]/tr[2]/td[1]/table')

        for sub_item in nav_sidebar.xpath('tr/td[@class="SubNavCell"]'):
            # sub_nav_name = sub_item.xpath('a[@class="SubNavLink"]/text()').get()
            sub_nav_url = sub_item.xpath('a[@class="SubNavLink"]/@href').get()
            if sub_nav_url is not None:
                temp_set.add(sub_nav_url)

        temp_set.difference_update(self.skip_these_urls)
        diff_set = temp_set.difference(self.navigation_urls)

        yield from self.crawl_next_url_level(diff_set, response, url_depth)

    def get_navigation_urls_third_level(self, response: scrapy.http.Response):
        """

        @url http://ginkgomaps.com/landkarten_midway_midwayinseln.html
        @returns requests 10
        """
        url_depth = 3
        yield from self.check_for_dead_ends_before_parsing(response)
        temp_set = set()

        nav_sidebar = response.xpath('/html/body/center/table[1]/tr[2]/td[1]/table')
        for sub_sub_item in nav_sidebar.xpath('//td[@class="SubSubNavCell"]'):
            # sub_sub_name = sub_sub_item.xpath('a[@class="SubSubNavLink"]/text()').get()
            sub_sub_url = sub_sub_item.xpath('a[@class="SubSubNavLink"]/@href').get()
            if sub_sub_url is not None:
                temp_set.add(sub_sub_url)

        temp_set.difference_update(self.skip_these_urls)
        diff_set = temp_set.difference(self.navigation_urls)

        yield from self.crawl_next_url_level(diff_set, response, url_depth)

    def get_navigation_urls_fourth_level(self, response: scrapy.http.Response):
        # url_depth = 4
        # as of 2021-06-14 there's no urls that go deeper than 4 levels in the nav-sidebar
        yield from self.check_for_dead_ends_before_parsing(response)

        # for debugging purposes:
        # print("fourth level Method: current url = ", str(response.url), " amount of URLs in total: ",
        #       len(self.navigation_urls))

    async def parse(self, response: scrapy.http.Response, **kwargs):
        """

        Scrapy Contracts:
        @url http://ginkgomaps.com/landkarten_deutschland.html
        @returns items 1
        """
        # making sure that the current url is marked as parsed:
        self.debug_parsed_urls.add(response.url)

        # IMPORTANT: modern browsers add "tbody"-elements into tables, scrapy doesn't see those tags!
        #   Remember: whatever request you see with the developer tools in your browser, you need to manually remove
        #   ANY <tbody>-tag that sits inside your xpath expression, otherwise it will return an empty [] !
        #       response.xpath('/html/body/center/table[1]/tr[4]/td[3]/table[1]').get()

        # first index page contains 42 maps, all inside tables of the class "smalltable":
        # response.xpath('//table[@class="smalltable"]')

        table_body = response.xpath('//table[@class="smalltable"]')
        description_temp = str()
        first_thumbnail = str()
        if table_body is not None:
            for table_item in table_body:
                # print(table_item.get())
                map_title = table_item.xpath('tr/td[1]/a[2]/text()').get()
                map_design_heading = table_item.xpath('tr/td[2]/u[1]/text()').get()
                map_design = table_item.xpath('tr/td[2]/p[1]/text()').get()
                map_content_heading = table_item.xpath('tr/td[2]/u[2]/text()').get()
                map_content = table_item.xpath('tr/td[2]/p[2]/text()').get()
                # map_thumbnail = response.urljoin(table_item.xpath('tr/td[1]/a[1]/img/@src').get())
                # map_thumbnail_description = table_item.xpath('tr/td[1]/a[1]/img/@alt').get()

                # pdf_download_url = response.urljoin(table_item.xpath('tr/td[2]/p[3]/a[1]/@href').get())
                # pdf_download_title = table_item.xpath('tr/td[2]/p[3]/a[2]/text()').get()
                # jpeg_download_medium_url = response.urljoin(table_item.xpath('tr/td[2]/p[4]/a[2]/@href').get())
                # jpeg_download_medium_description = table_item.xpath('tr/td[2]/p[4]/a[2]/text()').get()
                # jpeg_download_high_url = response.urljoin(table_item.xpath('tr/td[2]/p[5]/a[2]/@href').get())
                # jpeg_download_high_description = table_item.xpath('tr/td[2]/p[5]/a[2]/text()').get()

                description_temp += map_title + "\n" \
                    + map_design_heading + map_design \
                    + map_content_heading + map_content
            # while we could theoretically grab all thumbnails during the above loop,
            # the first one is enough for a preview-image in edu-sharing
            first_thumbnail = response.urljoin(table_body[0].xpath('tr/td[1]/a[1]/img/@src').get())

        description_temp = w3lib.html.strip_html5_whitespace(description_temp)

        base = super().getBase(response=response)
        base.add_value('sourceId', response.url)

        last_modified = response.xpath('/html/head/meta[6]/@content').get()
        hash_temp = last_modified + self.version
        base.add_value('hash', hash_temp)
        if first_thumbnail is not None:
            base.add_value('thumbnail', first_thumbnail)
        base.add_value('lastModified', last_modified)

        lom = LomBaseItemloader()
        general = LomGeneralItemloader(response=response)
        general.add_value('language', 'de')
        general.add_value('identifier', response.url)
        # the description could be extended with additional infos about the map-formats and their resolutions,
        # (if necessary)
        general.add_value('description', description_temp)
        general.add_value('title', response.xpath('/html/head/title/text()').get())
        # keywords are stored inside a String, separated by commas with (sometimes multiple) whitespaces,
        # therefore RegEx is needed to provide a list with individual keywords since a String.split() isn't enough:
        keyword_string = response.xpath('/html/head/meta[@name="keywords"]/@content').get()
        kw_regex_split = re.split(r'\s*,\s*', keyword_string)
        general.add_value('keyword', kw_regex_split)
        lom.add_value('general', general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value('format', 'text/html')
        technical.add_value('location', response.url)
        lom.add_value('technical', technical.load_item())

        lifecycle = LomLifecycleItemloader()
        lifecycle.add_value('date', last_modified)
        lifecycle.add_value('role', 'author')
        lifecycle.add_value('firstName', 'Dirk')
        lifecycle.add_value('lastName', 'Benkert')
        lifecycle.add_value('organization', 'Ginkgomaps')
        lifecycle.add_value('url', 'https://dirkbenkert.com/')
        lom.add_value('lifecycle', lifecycle.load_item())

        educational = LomEducationalItemLoader()
        # since the learning objects are maps, expositive seems to be the best fit for interactivityType:
        educational.add_value('interactivityType', 'expositive')
        lom.add_value('educational', educational.load_item())
        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()
        # since no educationalContext is given, either hardcode these values or don't use them at all
        # vs.add_value('educationalContext', ["Sekundarstufe I",
        #                                     "Sekundarstufe II",
        #                                     "Berufliche Bildung",
        #                                     "Erwachsenenbildung"])
        vs.add_value('new_lrt', [Constants.NEW_LRT_MATERIAL, 'b6ceade0-58d3-4179-af71-d53ebc6e49d4'])  # karte
        vs.add_value('intendedEndUserRole', ["learner",
                                             "teacher",
                                             "parent"])
        vs.add_value('discipline', 'Geografie')  # Geografie
        vs.add_value('conditionsOfAccess', 'no login')

        lic = LicenseItemLoader()
        # if needed, the license description could also be gathered and constructed from multiple tags within a
        # container: /html/body/center/table[1]/tbody/tr[5]/td[2]/p
        license_url: str = response.xpath('/html/body/center/table[1]/tr[5]/td[2]/p/a/@href').get()
        if (license_url is not None) and (license_url.endswith("deed.de")):
            license_url = license_url[:-len("deed.de")]
            license_url = license_url.replace("http://", "https://")
            lic.add_value('url', license_url)
        lic.add_value('author', response.xpath('/html/head/meta[3]/@content').get())

        base.add_value('valuespaces', vs.load_item())
        base.add_value('license', lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value('permissions', permissions.load_item())

        response_itemloader: ResponseItemLoader = await super().mapResponse(response)
        base.add_value('response', response_itemloader.load_item())

        yield base.load_item()
