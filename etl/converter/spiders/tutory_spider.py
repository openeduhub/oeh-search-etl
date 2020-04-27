from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
from converter.spiders.json_base import JSONBase;
import json
import logging
from html.parser import HTMLParser
from converter.pipelines import ProcessValuespacePipeline;
import re
import sys
from converter.constants import Constants;
from scrapy.selector import Selector

# Spider to fetch API from Serlo
class TutorySpider(scrapy.Spider, LomBase, JSONBase):
  name = 'tutory_spider'
  friendlyName = 'tutory'
  url = 'https://www.tutory.de/'
  baseUrl = 'https://www.tutory.de/api/v1/'
  def start_requests(self):
      url = self.baseUrl + 'worksheet?pageSize=999999'
      yield scrapy.Request(url=url, callback=self.parseList)

  def parseList(self, response):
      data = json.loads(response.body)
      for j in data['worksheets']:
        self.item = j
        if self.hasChanged(j):
          url = self.url+ 'worksheet/' + j['id']
          yield scrapy.Request(url=url, callback=self.parse, meta = {'item': j})

  def getId(self, response):
    return str(self.item['id'])

  def getHash(self, response):
    return self.item['updatedAt']

  def parse(self, response):
    self.item = response.meta['item']
    return LomBase.parse(self, response)

  def getBase(self, response):
    base = LomBase.getBase(self, response)
    base.add_value('lastModified', self.item['updatedAt'])
    base.add_value('thumbnail', self.url + 'worksheet/' + self.item['id'] + '.jpg?width=1000')
    return base

  def getValuespaces(self, response):
    valuespaces = LomBase.getValuespaces(self, response)
    discipline = list(map(lambda x: x['code'],filter(lambda x: x['type'] == 'subject', self.item['metaValues'])))
    valuespaces.add_value('discipline', discipline)
    return valuespaces

  def getLicense(self, response):
    license = LomBase.getLicense(self, response)
    license.add_value('internal', Constants.LICENSE_COPYRIGHT_LAW)
    return license

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(self, response)
    general.add_value('title', self.item['name'])
    return general

  def getLOMEducational(self, response):
    educational = LomBase.getLOMEducational(self, response)
    if self.item['description'] != '':
      educational.add_value('description', self.item['description'])
    else:
      html = self.getUrlData(response.url)['html']
      data = Selector(text=html).xpath('//ul[contains(@class,"worksheet-pages")]//text()').getall()
      cutoff = 4
      if len(data)>cutoff:
        for i in range(cutoff):
          del data[0]

      text = ' '.join(data)
      text = text[:1000]
      educational.add_value('description', text)
    return educational

  def getLOMTechnical(self, response):
    technical = LomBase.getLOMTechnical(self, response)
    technical.add_value('location', response.url)
    technical.add_value('format', 'text/html')
    technical.add_value('size', len(response.body))
    return technical