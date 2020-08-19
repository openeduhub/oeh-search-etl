from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase
from converter.spiders.rss_base import RSSBase
import json
import logging
from html.parser import HTMLParser
from converter.pipelines import ProcessValuespacePipeline
import re
from converter.valuespace_helper import ValuespaceHelper
from converter.constants import Constants

# Spider to fetch RSS from planet schule
class IRightsSpider(RSSBase):
    name = "irights_spider"
    friendlyName = "iRights.info"
    start_urls = ["https://irights.info/feed"]
    version = "0.1.0"

    def __init__(self, **kwargs):
        RSSBase.__init__(self, **kwargs)

    def getLOMGeneral(self, response):
        general = RSSBase.getLOMGeneral(self, response)
        general.add_value(
            "keyword", response.meta["item"].xpath("category//text()").getall()
        )
        return general

    def getLOMLifecycle(self, response):
        lifecycle = RSSBase.getLOMLifecycle(self, response)
        name = response.meta["item"].xpath("creator//text()").get().split(" ")
        lifecycle.add_value("role", "author")
        lifecycle.add_value("firstName", name[0])
        del name[0]
        lifecycle.add_value("lastName", " ".join(name))
        return lifecycle

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.add_value("educationalContext", "sekundarstufe_2")
        valuespaces.add_value("educationalContext", "berufliche_bildung")
        valuespaces.add_value("educationalContext", "erwachsenenbildung")
        valuespaces.add_value("discipline", "700")  # Wirtschaftskunde
        valuespaces.add_value("discipline", "48005")  # Gesellschaftskunde
        return valuespaces
