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
from converter.constants import Constants;

# Spider to fetch API from Serlo
class SerloSpider(scrapy.Spider, LomBase, JSONBase):
  name = 'serlo_spider'
  friendlyName = 'Serlo'
  url = 'https://de.serlo.org'
  def start_requests(self):
      url = self.url + '/entity/api/json/export/article'
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
        url = self.url + j['link'] + '?contentOnly'
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

  def getValuespaces(self, item):
    valuespaces = LomBase.getValuespaces(self, item)
    text = self.get('categories')[0].split('/')[0]
    # manual mapping to Mathematik
    if text == 'Mathe':
      text = 'Mathematik'
    valuespaces.add_value('discipline', text)
    #for entry in ProcessValuespacePipeline.valuespaces['discipline']:
    #  if len(list(filter(lambda x:x['@value'].casefold() == text.casefold(), entry['label']))):
    #    valuespaces.add_value('discipline',entry['id'])

    primarySchool = re.compile('Klasse\s[1-4]', re.IGNORECASE)
    if len(list(filter(lambda x: primarySchool.match(x), self.getKeywords()))):
      valuespaces.add_value('educationalContext', 'Grundschule')
    sek1 = re.compile('Klasse\s([5-9]|10)', re.IGNORECASE)
    if len(list(filter(lambda x: sek1.match(x), self.getKeywords()))):
      valuespaces.add_value('educationalContext', 'Sekundarstufe 1')
    sek2 = re.compile('Klasse\s1[1-2]', re.IGNORECASE)
    if len(list(filter(lambda x: sek2.match(x), self.getKeywords()))):
      valuespaces.add_value('educationalContext', 'Sekundarstufe 2')
    return valuespaces

  def getKeywords(self):
    try:
      keywords = list(self.get('keywords').values())
    except:
      keywords = self.get('keywords')
    for c in self.get('categories'):
      keywords += c.split('/')
    return set(keywords)

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(self, response)
    general.add_value('title', self.get('title'))
    general.add_value('keyword', self.getKeywords())
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
    
  def getLOMRights(self, response):
    rights = LomBase.getLOMRights(self, response)
    rights.add_value('description', Constants.LICENSE_CC_BY_SA_40)
    return rights
