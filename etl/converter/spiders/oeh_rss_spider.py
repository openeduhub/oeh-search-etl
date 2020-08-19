from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars

from converter.spiders.csv_base import CSVBase
from converter.spiders.lom_base import LomBase
from converter.spiders.rss_list_base import RSSListBase
import json
import logging
from html.parser import HTMLParser
from converter.pipelines import ProcessValuespacePipeline
import re
from converter.valuespace_helper import ValuespaceHelper
from converter.constants import Constants

# Spider to fetch RSS from planet schule
class OEHRSSSpider(RSSListBase):
    name = "oeh_rss_spider"
    friendlyName = "Open Edu Hub RSS"
    version = "0.1.0"

    def __init__(self, **kwargs):
        RSSListBase.__init__(self, "csv/oeh_rss.csv", **kwargs)

    def getBase(self, response):
        base = RSSListBase.getBase(self, response)
        base.replace_value(
            "origin", self.getCSVValue(response, CSVBase.COLUMN_SOURCE_TITLE)
        )
        return base

    def getLOMLifecycle(self, response=None) -> LomLifecycleItemloader:
        lifecycle = RSSListBase.getLOMLifecycle(self, response)
        lifecycle.add_value("role", "author")
        lifecycle.add_value(
            "organization", self.getCSVValue(response, CSVBase.COLUMN_SOURCE_TITLE)
        )
        lifecycle.add_value(
            "url", self.getCSVValue(response, CSVBase.COLUMN_SOURCE_URL)
        )
        return lifecycle
