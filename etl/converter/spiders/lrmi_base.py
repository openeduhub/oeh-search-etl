from scrapy.spiders import SitemapSpider
from converter.items import *
from datetime import datetime
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
from converter.spiders.json_base import JSONBase;
import json
import time

# base spider mapping data via LRMI inside the html pages
# Please override the lrmi_path if necessary and add your sitemap_urls 
class LrmiBase(SitemapSpider, LomBase, JSONBase):
  friendlyName = 'LRMI-Header Based spider'
  lrmi_path = '//script[@type="application/ld+json"]//text()'
  sitemap_urls = []

  def parse(self, response):
    self.json = json.loads(response.xpath(self.lrmi_path).extract_first())
    #self.json = json.loads(self.dummy)
    return LomBase.parse(self, response)

  def getBase(self, response):
    base = BaseItemLoader()
    base.add_value('sourceId', self.get('identifier','url','name'))
    base.add_value('thumbnail', self.get('thumbnailUrl'))
    base.add_value('lastModified', self.get('dateModified','datePublished'))
    if self.get('version') != None:
      base.add_value('hash', self.get('version'))
    else:
      base.add_value('hash', time.time())
    return base

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(response)
    general.add_value('identifier', self.get('identifier'))
    general.add_value('title', self.get('name'))
    general.add_value('keyword', self.get('keywords'))
    general.add_value('language', self.get('inLanguage'))
    return general

  def getLOMEducational(self, response):
    educational = LomBase.getLOMEducational(response)
    educational.add_value('description', self.get('description','about'))
    educational.add_value('intendedEndUserRole', self.get('audience.educationalRole'))
    educational.add_value('learningResourceType', self.get('learningResourceType'))
    educational.add_value('typicalLearningTime', self.get('timeRequired'))
    return educational

  def getLOMRights(self, response):
    rights = LomBase.getLOMRights(response)
    rights.add_value('description', self.get('license'))
    return rights

  def getLOMTechnical(self, response):
    technical = LomBase.getLOMTechnical(response)
    technical.add_value('format', self.get('fileFormat'))
    technical.add_value('size', self.get('ContentSize'))
    url = self.get('url')
    if not url:
      url = response.url
    technical.add_value('location', url)
    return technical
