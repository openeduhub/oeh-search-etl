import re

import dateparser
import scrapy
from playwright.sync_api import sync_playwright

from converter.constants import Constants
from converter.items import LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, LomLifecycleItemloader, \
    LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader
from converter.spiders.base_classes import LomBase


class ZumPhysikAppsSpider(scrapy.Spider, LomBase):
    name = "zum_physik_apps_spider"
    friendlyName = "ZUM Physik Apps"
    # the materials on the ZUM URL have been last updated on 2020-12 and directly links to the author's website
    # the materials on the author's website are more recently updated (2021-04)
    start_urls = [
        "https://www.walter-fendt.de/html5/phde/",
        # "https://www.zum.de/ma/fendt/phde/"
    ]
    version = "0.0.1"  # reflects the structure of ZUM Physik Apps on 2021-07-15
    playwright_instance = None
    browser_permanent = None

    # def __init__(self):
    #     LomBase.__init__(self, **kwargs)

    def getId(self, response=None) -> str:
        return response.url

    def getHash(self, response=None) -> str:
        pass

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_topic_overview)
        # scrapy won't see the <p class="Ende">-container where license information, lastModified and other metadata
        # is held, therefore we need to use playwright to render the javascript
        self.playwright_instance = sync_playwright().start()
        self.browser_permanent = self.playwright_instance.chromium.launch()

    def close(self, reason):
        # when the spider is done with its crawling process, it should close the playwright- and browser-instance
        self.browser_permanent.close()
        self.playwright_instance.stop()

    def parse_topic_overview(self, response):
        # the different topics are within tables: response.xpath('//table[@class="Gebiet"]')
        topic_urls = response.xpath('//td[@class="App"]/a/@href').getall()
        for topic_url in topic_urls:
            topic_url = response.urljoin(topic_url)
            yield scrapy.Request(url=topic_url, callback=self.parse)

        pass

    def parse(self, response, **kwargs):
        context = self.browser_permanent.new_context()
        page = context.new_page()
        page.goto(response.url)

        # fetching publication date and lastModified from dynamically loaded <p class="Ende">-element:
        page_end_element = page.inner_html('xpath=//p[@class="Ende"]')
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
                # each "sentence"-list holds exactly 2 elements now, whereby the last element should be the date
                # we could now either access it with sentence1[-1] or by iterating through the 2 items
                for item in sentence1:
                    if dateparser.parse(item) is not None:
                        published_date = dateparser.parse(item)
            if temp_string.startswith('Letzte Änderung:'):
                sentence2 = temp_string.rsplit(': ')
                for item2 in sentence2:
                    if dateparser.parse(item2) is not None:
                        last_modified = dateparser.parse(item2)

        base = super().getBase(response=response)
        base.add_value('type', Constants.TYPE_MATERIAL)
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
        vs.add_value('conditionsOfAccess', 'no login')
        vs.add_value('discipline', 'Physik')
        vs.add_value('intendedEndUserRole', ['learner', 'teacher', 'parent'])
        vs.add_value('learningResourceType', ['application', 'web page'])
        vs.add_value('price', 'no')
        base.add_value('valuespaces', vs.load_item())

        lic = LicenseItemLoader()
        lic.add_value('author', 'Walther Fendt')
        # if scrapy could render the <p class="Ende">-element, the license url could be found with the following XPath:
        # license_url = response.xpath('//p[@class="Ende"]/a[@rel="license"]/@href')
        # but since scrapy can't "see" this container, we're extracting the information with playwright
        license_url = page.get_attribute('//p[@class="Ende"]/a[@rel="license"]', "href")
        if license_url is not None:
            lic.add_value('url', license_url)
        base.add_value('license', lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value('permissions', permissions.load_item())
        base.add_value('response', super().mapResponse(response).load_item())

        yield base.load_item()

        pass
