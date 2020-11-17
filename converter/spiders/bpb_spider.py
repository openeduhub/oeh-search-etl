from converter.items import *
from scrapy.spiders import CrawlSpider, SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base_no_parse import LomBase
from converter.spiders.lrmi_base_no_parse import LrmiBase
from converter.constants import Constants
import json
from typing import List


class BpbSpider(LrmiBase, CrawlSpider):
    name = "bpb_spider"
    url = "https://www.bpb.de"  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = "Bundeszentrale für politische Bildung"  # name as shown in the search ui
    start_urls = ["https://www.bpb.de/sitemap/"]
    allowed_domains = ['bpb.de']
    whitelist = [
        'politik',
        'internationales',
        'geschichte',
        'gesellschaft',
        'nachschlagen',
        'lernen',
        'mediathek'
        ]

    blacklist: tuple = (
        "/suche",
        "/glossar"
    )

    version = "0.1"  # the version of your crawler, used to identify if a reimport is necessary

    rules = (
        Rule(LinkExtractor(allow=()), process_links='process_links', callback='parse_links', follow=True),
    )

    # save a list of urls crawled and skip if url is already crawled
    crawled = []

    def __init__(self, **kwargs):
        LrmiBase.__init__(self, **kwargs)
        CrawlSpider.__init__(self, **kwargs)

    def process_links(self, links):
        for link in links:
            try:
                if link.url.split("/")[3] not in self.whitelist:
                    continue
                elif link.url.endswith(self.blacklist):
                    continue
                yield link
            except IndexError:
                pass

    def parse_links(self, response):
        # copy from parse method of LomBase
        if self.shouldImport(response) == False:
            logging.info(
                "Skipping entry "
                + str(self.getId(response))
                + " because shouldImport() returned false"
            )
            return None
        # TODO SR turn on again
        # if self.getId(response) != None and self.getHash(response) != None:
        #     if not self.hasChanged(response):
        #         return None
        main = self.getBase(response)
        main.add_value("lom", self.getLOM(response).load_item())
        main.add_value("valuespaces", self.getValuespaces(response).load_item())
        main.add_value("license", self.getLicense(response).load_item())
        main.add_value("permissions", self.getPermissions(response).load_item())
        logging.debug(main.load_item())
        main.add_value("response", self.mapResponse(response).load_item())
        return main.load_item()

    # return a (stable) id of the source
    def getId(self, response):
        return self.getLRMI("mainEntityOfPage", response=response)

    def getHash(self, response):
        if self.version != None:
            return self.getLRMI("dateModified", response=response)
        return time.time()

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        sourceId = self.getId(response)

        ## check if we already crawled that page (TODO SR might be redundant if hash checker is turned on)
        if sourceId in self.crawled:
            print(f"sourceId: {sourceId} was already crawled")
            return None

        self.crawled.append(sourceId)
        base.add_value("sourceId", sourceId)
        # TODO set no thumbnail, so splash will take screenshot
        # base.add_value("thumbnail", self.getLRMI(
        #     "image.url", response=response))
        base.add_value(
            "lastModified",
            self.getLRMI("dateModified", "datePublished", response=response),
        )
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("identifier", self.getLRMI(
            "mainEntityOfPage", response=response))
        general.add_value("title", self.getLRMI("headline", response=response))
        
        # Keywords
        keywords: List[str] = [keyword.strip() for keyword in self.getLRMI(
            "keywords", response=response).split(",")]
        general.add_value("keyword", keywords)

        # Language TODO fill in value by hand or leave empty?
        general.add_value("language", self.getLRMI(
            "inLanguage", response=response))

        # Description
        general.add_value(
            "description", self.getLRMI(
                "description", response=response)
        )
        return general

    # TODO wie Organisationsnamen darstellen? wie mehrfache Autor:innen?
    def getLOMLifecycle(self, response):
        lifecycle = LomBase.getLOMLifecycle(self, response)
        name = self.getLRMI("author", response=response)
        lifecycle.add_value("role", "author")
        lifecycle.add_value("firstName", "")
        lifecycle.add_value("lastName", name)
        return lifecycle

    # TODO welche Lizenz? manche inhalte haben eine Lizenz angabe
    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        license_value: str = response.xpath(
            '//div[@class="cc-license"]/a/@href').get()
        if license_value:
            # remove language link from license
            if license_value.endswith("deed.de"):
                license_value = license_value[:-len("deed.de")]
            elif license_value.endswith("de/"):
                license_value = license_value[:-len("de/")]
            license.add_value("url", license_value)
        return license

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        # TODO added text/html manually to avoid error in pipelines 257
        technical.add_value("format", "text/html")
        # technical.add_value("size", self.getLRMI(
        #     "ContentSize", response=response))
        url = self.getLRMI("mainEntityOfPage", response=response)
        if not url:
            url = response.url
        technical.add_value("location", url)
        return technical
