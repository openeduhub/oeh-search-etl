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
    self.json = json.loads(response.xpath(self.lrmi_path).extract_first())
    return LomBase.parse(self, response)

  def getBase(self, response):
    base = BaseItemLoader()
    base.add_value('sourceId', self.json.get('identifier'))
    base.add_value('hash', self.json.get('version'))
    return base

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(response)
    general.add_value('identifier', self.json.get('identifier'))
    general.add_value('title', self.json.get('name'))
    general.add_value('keyword', self.json.get('keywords'))
    general.add_value('language', self.json.get('inLanguage'))
    return general

  def getLOMEducational(self, response):
    educational = LomBase.getLOMEducational(response)
    educational.add_value('description', self.json.get('description'))
    return educational

  def getLOMRights(self, response):
    rights = LomBase.getLOMRights(response)
    rights.add_value('description', self.json.get('license'))
    return rights

  def getLOMTechnical(self, response):
    technical = LomBase.getLOMTechnical(response)
    technical.add_value('format', self.json.get('fileFormat'))
    technical.add_value('size', self.json.get('ContentSize'))
    technical.add_value('location', self.json.get('url'))
    return technical
