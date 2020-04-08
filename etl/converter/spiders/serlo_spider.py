from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
from converter.spiders.json_base import JSONBase;
import json
import logging

# Spider to fetch API from Serlo
class SerloSpider(scrapy.Spider, LomBase, JSONBase):
  name='serlo_spider'
  friendlyName='Serlo'
  baseUrl = 'https://de.serlo.org'
  def start_requests(self):
      url = self.baseUrl + '/entity/api/json/export/article'
      # current dummy fallback since the Serlo API is basically down
      url = 'http://localhost/serlo.json'
      yield scrapy.Request(url=url, callback=self.parseList)
  def parseList(self, response):
      data = json.loads(response.body)
      for j in data:
        url = self.baseUrl + j['link'] + '?contentOnly'
        #logging.info(j)
        #logging.info(url)
        yield scrapy.Request(url=url, callback=self.parse, meta = {'json': j, 'url': url})
  def parse(self, response):
    self.json = response.meta['json']
    return LomBase.parse(self, response)

  def getBase(self, response):
    base = BaseItemLoader()
    base.add_value('sourceId', self.get('guid'))
    base.add_value('hash', self.get('lastModified.date'))
    base.add_value('lastModified', self.get('lastModified.date'))
    base.add_value('ranking', 0.9 + (float(self.get('revisionsCount'))/2 + float(self.get('authorsCount')))/50)
    return base

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(response)
    general.add_value('title', self.get('title'))
    try:
      keywords = list(self.get('keywords').values())
    except:
      keywords = self.get('keywords')
    for c in self.get('categories'):
      keywords += c.split('/')
    general.add_value('keyword', set(keywords))
    return general
  def getLOMEducational(self, response):
    educational = LomBase.getLOMEducational(response)
    educational.add_value('description', self.get('description'))
    return educational
  def getLOMTechnical(self, response):
    technical = LomBase.getLOMTechnical(response)
    technical.add_value('location', response.url)
    technical.add_value('format', 'text/html')
    technical.add_value('size', len(response.body))
    return technical

  # You may override more lom container here