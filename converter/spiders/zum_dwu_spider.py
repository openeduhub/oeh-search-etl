import re
from datetime import datetime

import scrapy
import w3lib.html
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, LomLifecycleItemloader, \
    LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader
from converter.spiders.base_classes import LomBase


class ZumDwuSpider(CrawlSpider, LomBase):
    name = "zum_dwu_spider"
    friendlyName = "ZUM DWU"
    start_urls = [
        # "http://www.zum.de/dwu/",
        "http://www.zum.de/dwu/umamtg.htm",  # Mathematik-Teilgebiete
        "http://www.zum.de/dwu/umaptg.htm"      # Physik-Teilgebiete
    ]
    version = "0.0.1"
    parsed_urls = set()  # holds the already parsed urls to minimize the amount of duplicate requests
    debug_xls_set = set()
    # The author used a HTML suite for building the .htm documents (Hot Potatoes by Half-Baked Software)
    # this software seems to set its own keywords if the author didn't specify his own keywords for sub-page
    # we don't want these keywords muddying up our keyword lists:
    keywords_to_ignore = {'University of Victoria', 'Hot Potatoes', 'Windows', 'Half-Baked Software'}

    def __init__(self, **kwargs):
        CrawlSpider.__init__(self, **kwargs)

    def getId(self, response=None) -> str:
        pass

    def getHash(self, response=None) -> str:
        pass

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_section_overview)
        pass

    def parse_section_overview(self, response: scrapy.http.Response):
        # Each section (e.g. "Mathematik Teilgebiete") holds a list of individual topic-categories (e.g. "Kreislehre")
        section_urls = response.xpath('/html/body/table/tr/td/a/@href').getall()
        section_urls.sort()
        # print(section_urls)
        # print("Section URLs: ", len(section_urls))
        for url in section_urls:
            current_url = response.urljoin(url)
            yield scrapy.Request(url=current_url, callback=self.parse_topic_overview)
        pass

    def parse_topic_overview(self, response: scrapy.http.Response):
        # Each topic (e.g. "Bruchzahlen / Bruchrechnen") holds a list of sub-topics that are either individual
        #   .htm-pages with explanations about a specific topic
        #   eLearning-exercises or
        #   "Aufgabengeneratoren" inside a .xls file
        topic_urls = response.xpath('/html/body/table/tr/td/a/@href').getall()
        # print("Topic URLs:", topic_urls)
        # print("Number of topic_urls in this section:", len(topic_urls))

        url_set = set()
        xls_set = set()
        for url in topic_urls:
            if url.endswith('.htm') or url.endswith('.html'):
                # topics that consist of illustrations or explanations are found inside individual .htm-documents
                current_url = response.urljoin(url)
                url_set.add(current_url)
            if url.endswith('.xls'):
                # there are currently 3 links to .xls files, which are "Aufgabengeneratoren"
                # e.g. on this topic overview: http://www.zum.de/dwu/umamgl.htm
                # TODO: handle .xls links with a different parse-method than the other .htm links?
                xls_set.add(url)
                self.debug_xls_set.add(url)
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
        # TODO: further optimize the dupefilter?
        for url in url_set:
            # only yield a scrapy Request if the url hasn't been parsed yet, this should help with duplicate links
            # that are found across different topics
            if url not in self.parsed_urls:
                yield scrapy.Request(url=url, callback=self.parse)
                self.parsed_urls.add(url)
        pass

    def parse(self, response: scrapy.http.Response, **kwargs):
        date_now = datetime.now()
        date_now_iso = date_now.isoformat()

        base = super().getBase(response=response)
        base.add_value('sourceId', response.url)
        # TODO: base
        #  - thumbnail
        base.add_value('type', Constants.TYPE_MATERIAL)
        # there's no "lastModified" or other date found on the website, therefore we have to built our own hash
        hash_temp = date_now_iso + response.url + self.version
        base.add_value('hash', hash_temp)

        lom = LomBaseItemloader()
        general = LomGeneralItemloader(response=response)
        description_raw = response.xpath('/html/body/table/tr[4]/td/table/tr/td').get()
        if description_raw is not None:
            description_raw = w3lib.html.remove_tags(description_raw)
            description_raw = w3lib.html.strip_html5_whitespace(description_raw)
            clean_description = w3lib.html.replace_escape_chars(description_raw)
            general.add_value('description', clean_description)
        # most of the time the title is stored directly
        title: str = response.xpath('/html/head/title/text()').get()
        if title.startswith("Dieses Info-Fenster"):
            # some subpages carry "Dieses Info-Fenster bleibt bis zum Schließen im Vordergrund" as their title,
            # therefore we need to grab the title from a better suited element.
            # This also means that the "description" is most probably wrong and needs a replacement as well:
            title = response.xpath('//td[@class="tt1math"]/text()').get()
            title = title.strip()
            # desc_list = response.xpath('/html/body/table[2]/tr/td/table/tr[1]/td[1]/text()').getall()
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

        if title is not None:
            title = w3lib.html.replace_escape_chars(title)
            if title == '':
                # there's some pages (Exercises) that only hold escape chars or whitespaces as their title
                # the title is simply bold text hidden within a div container
                title = response.xpath('//div[@class="Titles"]/h3[@class="ExerciseSubtitle"]/b/text()').get()
            general.add_value('title', title)

        general.add_value('identifier', response.url)
        general.add_value('language', 'de')
        # on the vast majority of .htm pages the keywords sit in the http-equiv content tag
        keyword_string = response.xpath('/html/head/meta[@http-equiv="keywords"]/@content').get()
        if keyword_string is None:
            # but on some sub-pages, especially the interactive javascript pages, the keywords are in another container
            keyword_string = response.xpath('/html/head/meta[@name="keywords"]/@content').get()
        if keyword_string is not None:
            keyword_list = keyword_string.rsplit(", ")
            # trying to catch the completely broken keyword strings to clean them up manually
            # e.g. at http://www.zum.de/dwu/depothp/hp-math/hpmz21.htm check XPath: /html/head/meta[2]
            kw_set = set()
            if keyword_list[0].endswith(","):
                # broken keyword list detected, now we have to manually clean the string up
                broken_keyword_string: str = response.xpath('//meta[@name="keywords"]').get()
                broken_keyword_list = broken_keyword_string.replace('<meta name="keywords" content=', "").rsplit(",")
                for item in broken_keyword_list:
                    kw_set.add(item.replace('"', "").replace("=", "").strip())
            if len(kw_set) == 0:
                # if there was no broken keyword meta field found, this condition always triggers
                kw_set = set(keyword_list)
            # checking if the keywords appear on the set of unwanted keywords, if they do, throw them away and only
            # keep the valid ones
            kw_set.difference_update(self.keywords_to_ignore)
            # once this check is done, add the keywords from the (cleaned up) keyword set
            keyword_list = list(kw_set)
            # catching the edge-case where all keywords are the Hot Potatoes default string, which means our keyword set
            # is empty => the entry would get dropped without keywords or a valid description
            if kw_set is not None and len(kw_set) == 0:
                interactive_instructions = response.xpath('//*[@id="InstructionsDiv"]/p/text()').get()
                # and sometimes even these instructions are found in another div container, so we'll give it a 2nd try:
                if interactive_instructions is None:
                    interactive_instructions = response.xpath('//p[@id="Instructions"]/b/text()').get()
                # by now we should have at least one valid description so the item doesn't get dropped completely
                if interactive_instructions is not None:
                    general.replace_value('description', interactive_instructions)
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
        lifecycle.add_value('url', 'dwu@zum.de')
        lifecycle.add_value('organization',
                            response.xpath('/html/head/meta[@http-equiv="organization"]/@content').get())
        lom.add_value('lifecycle', lifecycle.load_item())

        educational = LomEducationalItemLoader()
        lom.add_value('educational', educational.load_item())

        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()
        url_last_part = response.url
        url_last_part = url_last_part.split('/')[-1]
        if url_last_part.startswith("m") or url_last_part.startswith("hpm") or url_last_part.startswith("tkm"):
            vs.add_value('discipline', 'Mathematics')
        if url_last_part.startswith("p") or url_last_part.startswith("kwp") or url_last_part.startswith("hpp") \
                or url_last_part.startswith("vcp"):
            vs.add_value('discipline', "Physics")
        vs.add_value('learningResourceType', Constants.TYPE_MATERIAL)
        vs.add_value('intendedEndUserRole', ['learner',
                                             'teacher',
                                             'parent',
                                             ])
        vs.add_value('price', 'no')
        vs.add_value('conditionsOfAccess', 'no login')

        lic = LicenseItemLoader()
        lic.add_value('url', 'http://www.zum.de/dwu/hilfe.htm')
        lic.add_value('internal', Constants.LICENSE_COPYRIGHT_LAW)
        lic.add_value('author', response.xpath('/html/head/meta[@http-equiv="author"]/@content').get())

        base.add_value('valuespaces', vs.load_item())
        base.add_value('license', lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value('permissions', permissions.load_item())

        base.add_value('response', super().mapResponse(response).load_item())

        # print(self.parsed_urls)
        # print("debug_url_set length:", len(self.parsed_urls))

        yield base.load_item()
        pass
