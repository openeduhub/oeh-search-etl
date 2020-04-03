from scrapy.spiders import SitemapSpider
from converter.items import *
from datetime import datetime
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
import json

# base spider mapping data via LRMI inside the html pages
# Please override the lrmi_path if necessary and add your sitemap_urls 
class LrmiBase(SitemapSpider, LomBase):
  lrmi_path = '//script[@type="application/ld+json"]//text()'
  sitemap_urls = []

  def parse(self, response):
    return LomBase.parse(self, response)

  def pre_parse(self, response):
    self.json = json.loads(response.xpath(self.lrmi_path).extract_first())

  def getBase(self, response):
    base = BaseItemLoader()
    base.add_value('sourceId', self.json['identifier'])
    base.add_value('hash', self.json['version'])
    base.add_value('fulltext', self.json['description'])
    return base

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(response)
    general.add_value('identifier', self.json['identifier'])
    general.add_value('title', self.json['name'])
    general.add_value('keyword', self.json['keywords'])
    return general
