from scrapy.spiders import SitemapSpider
from converter.items import *
from datetime import datetime
from w3lib.html import remove_tags, replace_escape_chars
import json


class ZoerrSpider(SitemapSpider):
  name = 'zoerr_spider'
  sitemap_urls = [
      'https://uni-tuebingen.oerbw.de/edu-sharing/eduservlet/sitemap']

  def parse(self, response):
    self.json = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())
    
    main = self.getBase(response)
    main.add_value('lom', self.getLOM(response).load_item())
    return main.load_item()
  def getBase(self, response):
    base = BaseItemLoader()
    base.add_value('sourceId', self.json['identifier'])
    base.add_value('hash', self.json['version'])
    base.add_value('fulltext', self.json['description'])
    return base

  def getLOM(self, response):
    lom = LomBaseItemloader()
    lom.add_value('general', self.getLOMGeneral(response).load_item())
    lom.add_value('lifecycle', self.getLOMLifecycle(response).load_item())
    return lom

  def getLOMGeneral(self, response):
    general = LomGeneralItemloader()
    general.add_value('identifier', self.json['identifier'])
    general.add_value('title', self.json['name'])
    general.add_value('keyword', self.json['keywords'])
    return general

  def getLOMLifecycle(self, response):
    lifecycle = LomLifecycleItemloader()
    return lifecycle
