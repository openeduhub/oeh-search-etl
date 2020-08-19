from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
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
class ZDFRSSSpider(RSSListBase):
    name = "zdf_rss_spider"
    friendlyName = "ZDF"
    url = "https://www.zdf.de/"
    version = "0.1.0"

    def __init__(self, **kwargs):
        RSSListBase.__init__(self, "csv/zdf_rss.csv", **kwargs)
