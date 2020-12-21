from scrapy import Request

from converter.items import *
from scrapy.spiders import CrawlSpider, SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase
from converter.spiders.lrmi_base import LrmiBase
from converter.constants import Constants
import json
from typing import List


class BpbSpider(LrmiBase, CrawlSpider):
    name = "bpb_spider" 
    url = "https://www.bpb.de"
    friendlyName = "Bundeszentrale für politische Bildung"
    start_urls = ["https://www.bpb.de/sitemap/"]
    allowed_domains = ["bpb.de"]
    allow_list = [
        "politik",
        "internationales",
        "geschichte",
        "gesellschaft",
        # "nachschlagen", # refers to some kind of glossar, which we might not need
        "lernen",
        "mediathek"
    ]

    deny_list: tuple = (
        "/suche",
        "/glossar"
    )

    version = "0.1.2"  # the version of your crawler, used to identify if a reimport is necessary

    rules = (
        Rule(LinkExtractor(allow=()), process_links="process_links",
             callback="parse_links", follow=True),
    )

    def start_requests(self):
        yield Request(url = self.start_urls[0], callback = self.parse)

    def parse(self, response):
        return CrawlSpider.parse(self, response)

    def __init__(self, **kwargs):
        LrmiBase.__init__(self, **kwargs)
        CrawlSpider.__init__(self, **kwargs)

    def process_links(self, links):
        for link in links:
            try:
                if link.url.split("/")[3] not in self.allow_list:
                    continue
                elif link.url.endswith(self.deny_list):
                    continue
                yield link
            except IndexError:
                pass

    def parse_links(self, response):
        return LrmiBase.parse(self, response)

    # return a (stable) id of the source
    def getId(self, response):
        return self.getLRMI("mainEntityOfPage", response=response)

    def getBase(self, response):
        base = LrmiBase.getBase(self, response)
        base.replace_value("thumbnail", None)
        return base

    def getKeywords(self, response) -> List[str]:
        keywords = self.getLRMI("keywords", response=response)
        if keywords.strip():
            return[keyword.strip() for keyword in keywords.split(",")]
        return []
    def getLOMGeneral(self, response):
        general = LrmiBase.getLOMGeneral(self, response)
        general.replace_value("title", self.getLRMI("name", "headline", response=response).replace(" | bpb", ""))
        general.replace_value("identifier", self.getLRMI(
            "mainEntityOfPage", response=response))

        # Keywords (use try catch, some entries might not have keywords)
        try:
            general.replace_value("keyword", self.getKeywords(response))
        except:
            pass

        # Language TODO fill in value by hand or leave empty?
        general.add_value("language", self.getLRMI(
            "inLanguage", response=response))

        # Description
        general.add_value(
            "description", self.getLRMI(
                "description", response=response)
        )
        return general

    def getLOMLifecycle(self, response):
        name = self.getLRMI("author", response=response)
        lifecycle = LrmiBase.getLOMLifecycle(self, response)

        if name == "Bundeszentrale für politische Bildung":
            lifecycle.add_value("role", "author")
            # if author organization
            lifecycle.add_value(
                "organization", name)

        elif name == "Redaktion":
            lifecycle.add_value("role", "author")
            # if author organization
            lifecycle.add_value(
                "organization", name)

        elif "Redaktion werkstatt.bpb.de" in name:
            lifecycle.add_value("role", "author")
            # if author organization
            lifecycle.add_value(
                "organization", name)

        elif ", " not in name:
            # maybe one author
            lifecycle.add_value("role", "author")
            author = name.split(" ")
            lifecycle.add_value("firstName", " ".join(author[:-1]).strip())
            lifecycle.add_value("lastName", author[-1].strip())

        elif ", " in name:
            for author_name in name.split(","):
                lifecycle.add_value("role", "author")
                author = author_name.split(" ")
                lifecycle.add_value("firstName", " ".join(author[:-1]).strip())
                lifecycle.add_value("lastName", author[-1].strip())

        elif "und" in name:
            for author_name in name.split("und"):
                lifecycle.add_value("role", "author")
                author = author_name.split(" ")
                lifecycle.add_value("firstName", " ".join(author[:-1]).strip())
                lifecycle.add_value("lastName", author[-1].strip())

        return lifecycle

    def getLicense(self, response):
        license = LrmiBase.getLicense(self, response)
        license_value: str = response.xpath(
            "//div[@class='cc-license']/a/@href").get()
        if license_value:
            # remove language link from license
            if license_value.endswith("deed.de"):
                license_value = license_value[:-len("deed.de")]
            elif license_value.endswith("de/"):
                license_value = license_value[:-len("de/")]
            # oeh crawling constants all use https
            license_value = license_value.replace("http://", "https://")
            license.replace_value("url", license_value)
        return license

    def getLOMTechnical(self, response):
        technical = LrmiBase.getLOMTechnical(self, response)
        technical.replace_value("format", "text/html")
        # technical.add_value("size", self.getLRMI(
        #     "ContentSize", response=response))
        url = self.getLRMI("mainEntityOfPage", response=response)
        if not url:
            url = response.url
        technical.replace_value("location", url)
        return technical

    def getValuespaces(self, response):
        valuespaces = LrmiBase.getValuespaces(self, response)
        disciplines = ["politik", "geschichte"]
        for discipline in disciplines:
            if "/" + discipline in response.url:
                valuespaces.add_value("discipline", discipline)

        # try to map keywords to known disciplines
        try:
            valuespaces.add_value("discipline", self.getKeywords(response))
        except:
            pass
        return valuespaces