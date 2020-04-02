from scrapy.spiders import SitemapSpider
from converter.items import *
from datetime import datetime
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
import json


class ZoerrSpider(SitemapSpider, LomBase):
  name = 'zoerr_spider'
  sitemap_urls = [
      'https://uni-tuebingen.oerbw.de/edu-sharing/eduservlet/sitemap']

  def parse(self, response):
    return LomBase.parse(self, response)

  def pre_parse(self, response):
    self.json = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(response)
    general.add_value('identifier', self.json['identifier'])
    general.add_value('title', self.json['name'])
    general.add_value('keyword', self.json['keywords'])
    return general
