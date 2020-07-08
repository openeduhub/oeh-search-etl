from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
from converter.spiders.json_base import JSONBase;
import json
import logging
import requests
from html.parser import HTMLParser
from converter.pipelines import ProcessValuespacePipeline;
import re
from converter.valuespace_helper import ValuespaceHelper;
from converter.constants import *;

# Spider to fetch RSS from planet schule
class WirLernenOnlineSpider(scrapy.Spider, LomBase, JSONBase):
  name='wirlernenonline_spider'
  friendlyName='WirLernenOnline'
  url = 'https://wirlernenonline.de/'
  version = '0.1.2'
  apiUrl = 'https://wirlernenonline.de/wp-json/wp/v2/%type/?per_page=50&page=%page'
  keywords = {}

  def __init__(self, **kwargs):
    LomBase.__init__(self, **kwargs)

  def mapResponse(self, response):
      r = LomBase.mapResponse(self, response)
      r.replace_value('text', '')
      r.replace_value('html', '')
      r.replace_value('url', response.meta['item'].get('link'))
      return r

  def getId(self, response):
    return response.meta['item'].get('id')

  def getHash(self, response):
    return response.meta['item'].get('modified') + self.version

  def startRequest(self, type, page = 1):
    return scrapy.Request(url = self.apiUrl.replace('%page', str(page)).replace('%type', type), callback = self.parseRequest, headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }, meta = {
      'page': page,
      'type': type
      })

  def start_requests(self):
    keywords = json.loads(requests.get('https://wirlernenonline.de/wp-json/wp/v2/tags/?per_page=100').content.decode('UTF-8'))
    for keyword in keywords:
      self.keywords[keyword['id']] = keyword['name']

    yield self.startRequest('edusource')
    yield self.startRequest('edutool')

  def parseRequest(self, response):
    results = json.loads(response.body_as_unicode())
    if results:
      for item in results:
        copyResponse = response.copy()
        copyResponse.meta['item'] = item
        if self.hasChanged(copyResponse):
          yield self.handleEntry(copyResponse)
      yield self.startRequest(response.meta['type'], response.meta['page'] + 1)
        

  def handleEntry(self, response):
    return LomBase.parse(self, response)

  def getType(self, response):
    if response.meta['type'] == 'edusource':
      return Constants.TYPE_SOURCE
    elif response.meta['type'] == 'edutool':
      return Constants.TYPE_TOOL
    return None

  # thumbnail is always the same, do not use the one from rss
  def getBase(self, response):
    base = LomBase.getBase(self, response)
    base.replace_value('thumbnail', self.get('acf.thumbnail.url', json = response.meta['item']))
    base.replace_value('type', self.getType(response))
    fulltext = self.get('acf.long_text', json = response.meta['item'])
    base.replace_value('fulltext', HTMLParser().unescape(fulltext))
    return base

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(self, response)
    general.replace_value('title', HTMLParser().unescape(self.get('title.rendered', json = response.meta['item'])))
    keywords = self.get('tags', json = response.meta['item'])
    if keywords:
      keywords = list(map(lambda x: self.keywords[x], keywords))
      general.add_value('keyword', keywords)
    general.add_value('description', HTMLParser().unescape(self.get('acf.short_text', json = response.meta['item'])))
    return general
    

  def getLOMTechnical(self, response):
    technical = LomBase.getLOMTechnical(self, response)
    technical.replace_value('format', 'text/html')
    technical.replace_value('location', self.get('acf.url', json = response.meta['item']))
    return technical
 
  def getLicense(self, response):
    license = LomBase.getLicense(self, response)
    try:
      licenseId = self.get('acf.licence', json = response.meta['item'])[0]['value']
      if licenseId == '10':
        license.add_value('oer', OerType.NONE)
      elif licenseId == '11':
        license.add_value('oer', OerType.MIXED)
      elif licenseId == '12':
        license.add_value('oer', OerType.NONE)
    except:
      pass
    return license
    
  def getValuespaces(self, response):
    valuespaces = LomBase.getValuespaces(self, response)
    discipline = list(map(lambda x: x['value'], self.get('acf.fachgebiet', json = response.meta['item'])))
    valuespaces.add_value('discipline', discipline)
    sourceContentType = list(map(lambda x: x['value'], self.get('acf.lernresourcentyp', json = response.meta['item'])))
    valuespaces.add_value('sourceContentType', sourceContentType)
    context = list(map(lambda x: x['value'], self.get('acf.schulform', json = response.meta['item'])))
    valuespaces.add_value('educationalContext', context)
    role = list(map(lambda x: x['value'], self.get('acf.role', json = response.meta['item'])))
    valuespaces.add_value('intendedEndUserRole', role)
    return valuespaces

