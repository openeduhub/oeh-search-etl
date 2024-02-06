import re

import dateparser
import scrapy
from scrapy import Selector

from converter.constants import Constants
from converter.items import LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, LomLifecycleItemloader, \
    LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, ResponseItemLoader
from converter.spiders.base_classes import LomBase
from converter.web_tools import WebTools, WebEngine


class ZumPhysikAppsSpider(scrapy.Spider, LomBase):
    name = "zum_physik_apps_spider"
    friendlyName = "ZUM Physik Apps"
    # the materials on the ZUM URL have been last updated on 2020-12 and directly links to the author's website
    # the materials on the author's website are more recently updated (2021-04)
    start_urls = [
        "https://www.walter-fendt.de/html5/phde/",
        # "https://www.zum.de/ma/fendt/phde/"
    ]
    version = "0.0.6"  # last update: 2022-05-23
    # expected number of items after a successful crawl: 55
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        # "AUTOTHROTTLE_DEBUG": True
    }

    def getId(self, response=None) -> str:
        return response.url

    def getHash(self, response=None) -> str:
        pass

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_topic_overview)

    def parse_topic_overview(self, response: scrapy.http.Response):
        """
        Looks for individual topics within the overview and yields the URL to the main parse()-method.

        :param response: the current 'url' from start_urls
        :return: scrapy.Request

        Scrapy Contracts:
        @url https://www.walter-fendt.de/html5/phde/
        @returns requests 50
        """
        # the different topics are within tables: response.xpath('//table[@class="Gebiet"]')
        topic_urls = response.xpath('//td[@class="App"]/a/@href').getall()
        for topic_url in topic_urls:
            topic_url = response.urljoin(topic_url)
            yield scrapy.Request(url=topic_url, callback=self.parse)

    async def parse(self, response: scrapy.http.Response, **kwargs):
        """
        Populates a BaseItemLoader with metadata and yields the individual BaseItem via BaseItemLoader.load_item()
        afterwards.

        Scrapy Contracts:
        @url https://www.walter-fendt.de/html5/phde/newtonlaw2_de.htm
        @returns item 1
        """
        # fetching publication date and lastModified from dynamically loaded <p class="Ende">-element:
        url_data_splash_dict = await WebTools.getUrlData(response.url, engine=WebEngine.Playwright)
        splash_html_string = url_data_splash_dict.get('html')
        page_end_element = Selector(text=splash_html_string).xpath('//p[@class="Ende"]').get()
        line_regex = re.compile(r'<br>')
        page_end_string = line_regex.split(page_end_element)
        published_date = None
        last_modified = None
        # the two strings inside the <p>-Container will look like this:
        # Walter Fendt, 2. November 2000
        # Letzte Änderung: 17. Oktober 2017
        # therefore we'll need to extract the dates by splitting up the strings
        for temp_string in page_end_string:
            if temp_string.startswith("Walter Fendt"):
                sentence1 = temp_string.rsplit(', ')
                # each "sentence" list now holds exactly 2 elements, whereby the last element should be the date
                for item in sentence1:
                    if dateparser.parse(item) is not None:
                        published_date = dateparser.parse(item)
            if temp_string.startswith('Letzte Änderung:'):
                sentence2 = temp_string.rsplit(': ')
                for item2 in sentence2:
                    if dateparser.parse(item2) is not None:
                        last_modified = dateparser.parse(item2)

        base = super().getBase(response=response)
        if last_modified is not None:
            hash_temp = last_modified.isoformat() + self.version
            base.add_value('hash', hash_temp)
            base.add_value('lastModified', last_modified.isoformat())
        base.add_value('sourceId', response.url)

        lom = LomBaseItemloader()
        general = LomGeneralItemloader(response=response)
        general.add_value('identifier', response.url)
        general.add_value('title', response.xpath('/html/head/title/text()').get())
        general.add_value('description', response.xpath('/html/head/meta[@name="description"]/@content').get())
        keywords_string: str = response.xpath('/html/head/meta[@name="keywords"]/@content').get()
        if keywords_string is not None:
            keyword_list = keywords_string.rsplit(", ")
            general.add_value('keyword', keyword_list)
        general.add_value('language', 'de')
        lom.add_value('general', general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value('format', "text/html")
        technical.add_value('location', response.url)
        lom.add_value('technical', technical.load_item())

        lifecycle = LomLifecycleItemloader()
        lifecycle.add_value('role', 'author')
        lifecycle.add_value('firstName', 'Walter')
        lifecycle.add_value('lastName', 'Fendt')
        lifecycle.add_value('url', "https://www.walter-fendt.de/wf.htm")  # author information
        if published_date is not None:
            lifecycle.add_value('date', published_date.isoformat())
        lom.add_value('lifecycle', lifecycle.load_item())

        educational = LomEducationalItemLoader()
        educational.add_value('interactivityType', 'mixed')
        lom.add_value('educational', educational.load_item())

        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value('new_lrt', Constants.NEW_LRT_TOOL)
        vs.add_value('conditionsOfAccess', 'no login')
        vs.add_value('discipline', 'Physik')
        vs.add_value('intendedEndUserRole', ['learner', 'teacher', 'parent'])
        vs.add_value('price', 'no')
        base.add_value('valuespaces', vs.load_item())

        lic = LicenseItemLoader()
        lic.add_value('author', 'Walter Fendt')
        # if scrapy could render the <p class="Ende">-element, the license url could be found with the following XPath:
        # license_url = response.xpath('//p[@class="Ende"]/a[@rel="license"]/@href')
        # but since scrapy can't "see" this container, we're extracting the information with scrapy-splash
        license_url = Selector(text=splash_html_string).xpath('//p[@class="Ende"]/a[@rel="license"]/@href').get()
        if license_url is not None:
            # the license url links to the /de/ version, which currently doesn't get mapped properly
            # "https://creativecommons.org/licenses/by-nc-sa/3.0/de/"
            # -> 'https://creativecommons.org/licenses/by-nc-sa/3.0/' is the url-format we want
            if "creativecommons.org/licenses/" in license_url and license_url.endswith("/de/"):
                license_url = license_url.split("de/")[0]
            lic.add_value('url', license_url)
        base.add_value('license', lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value('permissions', permissions.load_item())
        response_itemloader: ResponseItemLoader = await super().mapResponse(response)
        base.add_value('response', response_itemloader.load_item())

        yield base.load_item()
