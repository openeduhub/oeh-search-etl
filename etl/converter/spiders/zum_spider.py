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
class ZUMSpider(scrapy.Spider, LomBase, JSONBase):
  name='zum_spider'
  friendlyName='ZUM-Unterrichten'
  url = 'https://unterrichten.zum.de/'
  version = '0.1.0'
  apiUrl = 'https://unterrichten.zum.de/api.php?action=query&format=json&list=allpages&apcontinue=%continue&aplimit=100'
  apiEntryUrl = 'https://unterrichten.zum.de/api.php?action=parse&format=json&pageid=%pageid'
  entryUrl = 'https://unterrichten.zum.de/wiki/%page'
  keywords = {}
  
  def __init__(self, **kwargs):
    LomBase.__init__(self, **kwargs)

  def mapResponse(self, response):
      r = LomBase.mapResponse(self, response, fetchData = False)
      r.replace_value('url', response.meta['item'].get('link'))
      return r

  def getId(self, response):
    return self.get('parse.pageid', json = response.meta['item'])

  def getHash(self, response):
    return str(self.get('parse.revid', json = response.meta['item'])) + self.version

  def startRequest(self, continueToken = ''):
    return scrapy.Request(url = self.apiUrl.replace('%continue', continueToken), callback = self.parseRequest, headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }, meta = {
      'continueToken': continueToken
      })

  def start_requests(self):
    keywords = json.loads(requests.get('https://wirlernenonline.de/wp-json/wp/v2/tags/?per_page=100').content.decode('UTF-8'))
    for keyword in keywords:
      self.keywords[keyword['id']] = keyword['name']

    yield self.startRequest('')

  def parseRequest(self, response):
    results = json.loads(response.body_as_unicode())
    if results:
      for item in results['query']['allpages']:
        yield scrapy.Request(url = self.apiEntryUrl.replace('%pageid', str(item['pageid'])), callback = self.handleEntry)
      if 'continue' in results:
        yield self.startRequest(results['continue']['apcontinue'])
        

  def handleEntry(self, response):
    response.meta['item'] = json.loads(response.body_as_unicode())
    return LomBase.parse(self, response)

  def getBase(self, response):
    base = LomBase.getBase(self, response)
    fulltext = self.get('parse.text.*', json = response.meta['item'])
    base.replace_value('fulltext', self.html2Text(fulltext)) # crashes!
    return base

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(self, response)
    general.replace_value('title', self.get('parse.title', json = response.meta['item']))
    keywords = self.get('parse.links', json = response.meta['item'])
    if keywords:
      keywords = list(map(lambda x: x['*'], keywords))
      general.add_value('keyword', keywords)
    props = self.get('parse.properties')
    if props:
      description = list(map(lambda x: x['*'], filter(lambda x: x['name'] == 'description', props)))
      general.add_value('description', description)
    return general
    

  def getLOMTechnical(self, response):
    technical = LomBase.getLOMTechnical(self, response)
    technical.replace_value('format', 'text/html')
    technical.replace_value('location', self.entryUrl.replace('%page',self.get('parse.title', json = response.meta['item'])))
    return technical
 
  def getLicense(self, response):
    license = LomBase.getLicense(self, response)
    license.add_value('url', Constants.LICENSE_CC_BY_SA_40)
    return license
    
  def getValuespaces(self, response):
    valuespaces = LomBase.getValuespaces(self, response)
    categories = list(map(lambda x: x['*'], self.get('parse.categories', json = response.meta['item'])))
    if categories:
      valuespaces.add_value('discipline', categories)
      valuespaces.add_value('educationalContext', categories)
      valuespaces.add_value('intendedEndUserRole', categories)
    return valuespaces

