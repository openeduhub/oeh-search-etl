import re
from datetime import datetime

import scrapy
import w3lib.html
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, LomLifecycleItemloader, \
    LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, ResponseItemLoader
from converter.spiders.base_classes import LomBase


class DwuSpider(CrawlSpider, LomBase):
    # Previously: Crawler for http://www.zum.de/dwu/
    # After 2022-11-29: Crawler for https://www.dwu-unterrichtsmaterialien.de
    name = "dwu_spider"
    friendlyName = "dwu-Unterrichtsmaterialien"
    start_urls = [
        "https://www.dwu-unterrichtsmaterialien.de/umamtg.htm",  # Mathematik-Teilgebiete
        "https://www.dwu-unterrichtsmaterialien.de/umaptg.htm"  # Physik-Teilgebiete
    ]
    # For historic context:
    # Up until crawler version v0.0.2 this crawler used to be named "zum_dwu_spider", but DWU informed us that the
    # learning materials won't be available on the ZUM Servers in the near future, which is why URLs point towards
    # DWU's private website offering from now on
    version = "0.0.6"  # last update: 2022-12-06
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        # "AUTOTHROTTLE_DEBUG": True
    }

    parsed_urls = set()  # holds the already parsed urls to minimize the amount of duplicate requests
    debug_xls_set = set()
    # The author used an HTML suite for building the .htm documents (Hot Potatoes by Half-Baked Software)
    # this software seems to set its own keywords if the author didn't specify his keywords for a document
    # we don't want these keywords muddying up our keyword lists, therefore we'll use a set to filter them out later:
    keywords_to_ignore = {'University of Victoria', 'Hot Potatoes', 'Windows', 'Half-Baked Software', 'hot', 'potatoes'}

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def getId(self, response=None) -> str:
        return response.url

    def getHash(self, response=None) -> str:
        date_now = datetime.now()
        date_now_iso = date_now.isoformat()
        hash_temp = date_now_iso + response.url + self.version
        return hash_temp

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_section_overview)

    def parse_section_overview(self, response: scrapy.http.Response):
        # Each section (e.g. "Mathematik Teilgebiete") holds a list of individual topic-categories (e.g. "Kreislehre")
        section_urls = response.xpath('/html/body//tr/td/a/@href').getall()
        section_urls.sort()
        # print(section_urls)
        # print("Section URLs: ", len(section_urls))
        for url in section_urls:
            current_url = response.urljoin(url)
            # scraping the overview to extract links to individual materials:
            yield scrapy.Request(url=current_url, callback=self.parse_topic_overview)

    def parse_topic_overview(self, response: scrapy.http.Response):
        # Each topic (e.g. "Bruchzahlen / Bruchrechnen") holds a list of sub-topics that are either individual
        #   .htm-pages with explanations about a specific topic
        #   eLearning-exercises or
        #   "Aufgabengeneratoren" inside a .xls file
        topic_urls = response.xpath('/html/body//tr/td/a/@href').getall()
        # print("Topic URLs:", topic_urls)
        # print("Number of topic_urls in this section:", len(topic_urls))

        url_set = set()
        # xls_set = set()
        for url in topic_urls:
            if url.endswith('.htm') or url.endswith('.html'):
                # topics that consist of illustrations or explanations are found inside individual .htm-documents
                current_url = response.urljoin(url)
                url_set.add(current_url)
            # if url.endswith('.xls'):
            #     # there are currently 3 links to .xls files, which are "Aufgabengeneratoren"
            #     # e.g. on this topic overview: http://www.zum.de/dwu/umamgl.htm
            #     # If we really wanted to handle the 3 .xls links, we need an additional xls-specific parse method
            #     xls_set.add(url)
            #     self.debug_xls_set.add(url)
            elif url.startswith("javascript"):
                # in some sections there are topics that lead to a javascript href, e.g.
                # "javascript:infowin('infodep/i-lingleich.htm');"
                # we'll have to extract the .htm-link from that string to parse it: the starting ' is our delimiter
                js_regex = re.compile(r"([^']*.htm)")
                js_url = js_regex.search(url)
                js_url = js_url.group()
                # url_set.add(js_url)
                current_url = response.urljoin(js_url)
                url_set.add(current_url)

        # print("debug XLS set length:", len(self.debug_xls_set))
        # print(self.debug_xls_set)
        # scraping the overview-page itself:
        yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)

        for url in url_set:
            # only yield a scrapy Request if the url hasn't been parsed yet, this should help with duplicate links
            # that are found across different topics
            if url not in self.parsed_urls:
                url_of_overview_page = response.url  # this workaround is needed to link to the overview-page within
                # the description-text of each material.
                overview_page_title = response.xpath('/html/head/title/text()').get()
                # scraping the individual materials:
                yield scrapy.Request(url=url,
                                     callback=self.parse,
                                     cb_kwargs={'overview_url': url_of_overview_page,
                                                'overview_title': overview_page_title})
                self.parsed_urls.add(url)
        # making sure that we don't crawl the overview-page more than once:
        self.parsed_urls.add(response.url)

    async def parse(self, response: scrapy.http.Response, **kwargs):
        base = super().getBase(response=response)
        lom = LomBaseItemloader()
        general = LomGeneralItemloader(response=response)
        description_addendum = str()
        if 'overview_url' in kwargs and 'overview_title' in kwargs:
            # Due to a request from DWU we're adding the higher-level overview URL to each description string so users
            # can find their way back (in those cases where it isn't possible to reach the overview page with the
            # "back"-Button (implemented as "javascript:history.back()"-Buttons)
            overview_url = kwargs.get('overview_url')
            overview_title = kwargs.get('overview_title')
            description_addendum = f"Dieses Material gehört zur übergeordneten Navigationsseite " \
                                   f"<a href=\"{overview_url}\">{overview_title}</a>" \
                                   f"\n"
        description_raw = response.xpath('//descendant::td[@class="t1fbs"]').getall()
        description_raw: str = ''.join(description_raw)
        if description_raw is not None:
            description_raw = w3lib.html.remove_tags(description_raw)
            description_raw = w3lib.html.strip_html5_whitespace(description_raw)
            clean_description = w3lib.html.replace_escape_chars(description_raw)
            if description_addendum:
                clean_description = f"{description_addendum}{clean_description}"
            general.add_value('description', clean_description)
        if len(description_raw) == 0:
            # Fallback for exercise-pages where there's only 1 title field and 1 short instruction sentence
            # e.g.: http://www.zum.de/dwu/depothp/hp-phys/hppme24.htm
            description_fallback = response.xpath('//descendant::div[@id="InstructionsDiv"]/descendant'
                                                  '::*/text()').get()
            if description_addendum:
                description_fallback = f"{description_addendum}{description_fallback}"
            general.replace_value('description', description_fallback)
        # most of the time the title is stored directly
        title: str = response.xpath('/html/head/title/text()').get()
        if title.startswith("Dieses Info-Fenster"):
            # some subpages carry "Dieses Info-Fenster bleibt bis zum Schließen im Vordergrund" as their title,
            # therefore we need to grab the title from a better suited element.
            # This also means that the "description" is most probably wrong and needs a replacement as well:
            title = response.xpath('//td[@class="tt1math"]/text()').get()
            if title is not None:
                title = title.strip()
            desc_list = response.xpath('//td[@class="t1fbs"]/text()').getall()
            if desc_list is not None and len(desc_list) == 0:
                # if the first attempt at grabbing a description fails, we try it at another place
                desc_list = response.xpath('//td[@class="sg12"]/text()').get()
            if desc_list is not None:
                description_raw = ''.join(desc_list)
                # if there's multiple whitespaces within the description, replace them by a single whitespace:
                description_raw = re.sub(' +', ' ', description_raw)
                clean_description = w3lib.html.replace_escape_chars(description_raw)
                general.replace_value('description', clean_description)

        if title:
            title = w3lib.html.replace_escape_chars(title)
            if title:
                # checking if the title is still valid, which necessary for broken headings that ONLY consisted of
                # escape-chars
                if title == '':
                    # there's some pages (exercises) that only hold escape chars or whitespaces as their title
                    # the title is simply bold text hidden within a div container
                    title = response.xpath('//div[@class="Titles"]/h3[@class="ExerciseSubtitle"]/b/text()').get()
                if title:
                    # checking once more for valid titles, since we might get an empty string from "ExerciseSubtitle"
                    title = title.strip()
                # Since we're grabbing titles from headings, a lot of them have a trailing ":"
                if len(title) > 0 and title.endswith(":"):
                    # replacing the string with itself right up to the point of the colon
                    title = title[:-1]
            general.add_value('title', title)

        general.add_value('identifier', response.url)
        general.add_value('language', 'de')
        # on the vast majority of .htm pages the keywords sit in the http-equiv content tag
        keyword_string = response.xpath('/html/head/meta[@http-equiv="keywords"]/@content').get()
        if keyword_string is None:
            # 1st workaround: some overview-pages have their keywords in a capitalized Keywords container:
            keyword_string = response.xpath('/html/head/meta[@http-equiv="Keywords"]/@content').get()
            if keyword_string is None:
                # but on some sub-pages, especially the interactive javascript pages, the keywords can be found in
                # another element of the DOM
                keyword_string = response.xpath('/html/head/meta[@name="keywords"]/@content').get()
        if keyword_string is not None:
            keyword_list = keyword_string.rsplit(", ")
            # trying to catch the completely broken keyword strings to clean them up manually
            # e.g. at http://www.zum.de/dwu/depothp/hp-math/hpmz21.htm check XPath: /html/head/meta[2]
            kw_set = set()
            if keyword_list[0].endswith(","):
                # broken keyword list detected, now we have to manually clean the string up
                broken_keyword_string: str = response.xpath('//meta[@name="keywords"]').get()
                broken_keyword_list = broken_keyword_string.replace('<meta name="keywords" content=', "") \
                    .replace(">", "").replace('"', "").replace(",", "").replace("=", "").split(" ")
                for item in broken_keyword_list:
                    kw_set.add(item.strip())
            if len(kw_set) == 0:
                # if there was no broken keyword meta field found, this condition always triggers
                kw_set = set(keyword_list)
            # checking if the keywords appear on the set of unwanted keywords, if they do, throw them away and only
            # keep the valid ones
            kw_set.difference_update(self.keywords_to_ignore)
            # once this check is done, add the keywords from the (cleaned up) keyword set
            keyword_list = list(kw_set)
            general.add_value('keyword', keyword_list)
        lom.add_value('general', general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value('format', 'text/html')
        technical.add_value('location', response.url)
        lom.add_value('technical', technical.load_item())

        lifecycle = LomLifecycleItemloader()
        lifecycle.add_value('role', 'author')
        lifecycle.add_value('firstName', 'Dieter')
        lifecycle.add_value('lastName', 'Welz')
        lifecycle.add_value('url', 'mail@dwu-unterrichtsmaterialien.de')
        lifecycle.add_value('organization', 'dwu-Unterrichtsmaterialien')
        lom.add_value('lifecycle', lifecycle.load_item())

        educational = LomEducationalItemLoader()
        lom.add_value('educational', educational.load_item())

        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value('new_lrt', Constants.NEW_LRT_MATERIAL)
        # since the website holds both mathematics- and physics-related materials, we need to take a look at the last
        # section of the url: .htm filenames that start with
        #   m | hpm | tkm       belong to the discipline mathematics
        #   p | kwp | hpp       belong to the discipline physics
        url_last_part = response.url
        url_last_part = url_last_part.split('/')[-1]
        if url_last_part.startswith("m") or url_last_part.startswith("hpm") or url_last_part.startswith("tkm"):
            vs.add_value('discipline', 'Mathematics')
        if url_last_part.startswith("p") or url_last_part.startswith("kwp") or url_last_part.startswith("hpp") \
                or url_last_part.startswith("vcp"):
            vs.add_value('discipline', "Physics")
        vs.add_value('intendedEndUserRole', ['learner',
                                             'teacher',
                                             'parent',
                                             ])
        vs.add_value('price', 'no')
        vs.add_value('conditionsOfAccess', 'no login')

        lic = LicenseItemLoader()
        lic.add_value('description', 'Bitte '
                                     '<a href="https://www.dwu-unterrichtsmaterialien.de/codaim.htm">Copyright-Hinweise'
                                     ' und Nutzungsbedingungen</a> beachten! (siehe auch: '
                                     '<a href="https://www.dwu-unterrichtsmaterialien.de/hilfe.htm">Hilfe</a>)')
        lic.add_value('internal', Constants.LICENSE_CUSTOM)
        lic.add_value('author', response.xpath('/html/head/meta[@http-equiv="author"]/@content').get())

        base.add_value('valuespaces', vs.load_item())
        base.add_value('license', lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value('permissions', permissions.load_item())

        response_itemloader: ResponseItemLoader = await super().mapResponse(response)
        base.add_value('response', response_itemloader.load_item())

        # print(self.parsed_urls)
        # print("debug_url_set length:", len(self.parsed_urls))

        yield base.load_item()
