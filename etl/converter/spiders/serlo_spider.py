from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
from converter.spiders.json_base import JSONBase;
import json
import logging
from html.parser import HTMLParser

# Spider to fetch API from Serlo
class SerloSpider(scrapy.Spider, LomBase, JSONBase):
  name='serlo_spider'
  friendlyName='Serlo'
  baseUrl = 'https://de.serlo.org'
  def start_requests(self):
      url = self.baseUrl + '/entity/api/json/export/article'
      # current dummy fallback since the Serlo API is basically down
      url = 'http://localhost/sources/serlo.json'
      yield scrapy.Request(url=url, callback=self.parseList)

  # some fields are having xml entities (for whatever reason), we will unescape them here
  def get(self, *params):
    data = JSONBase.get(self, *params)
    try:
      return HTMLParser().unescape(data)
    except:
      try:
        result = []
        for p in data:
          result.append(HTMLParser().unescape(p))
        return result
      except:
        return data

  def parseList(self, response):
      data = json.loads(response.body)
      for j in data:
        url = self.baseUrl + j['link'] + '?contentOnly'
        self.json = j
        if self.hasChanged():
          yield scrapy.Request(url=url, callback=self.parse, meta = {'json': j, 'url': url})

  def getId(self, response):
    return self.get('guid')

  def getHash(self, response):
    return self.get('lastModified.date')

  def parse(self, response):
    self.json = response.meta['json']
    return LomBase.parse(self, response)

  def getBase(self, response):
    base = LomBase.getBase(self, response)
    base.add_value('lastModified', self.get('lastModified.date'))
    base.add_value('ranking', 0.9 + (float(self.get('revisionsCount'))/2 + float(self.get('authorsCount')))/50)
    return base

  def getLOMRights(self, response):
    rights = LomBase.getLOMRights(self, response)
    rights.add_value('description', 'https://creativecommons.org/licenses/by-sa/4.0/deed.de')
    return rights

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(self, response)
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
    educational = LomBase.getLOMEducational(self, response)
    educational.add_value('description', self.get('description'))
    return educational

  def getLOMTechnical(self, response):
    technical = LomBase.getLOMTechnical(self, response)
    technical.add_value('location', response.url)
    technical.add_value('format', 'text/html')
    technical.add_value('size', len(response.body))
    return technical