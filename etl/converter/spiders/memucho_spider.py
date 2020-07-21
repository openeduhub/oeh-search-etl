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
from converter.valuespace_helper import ValuespaceHelper;
from converter.constants import Constants;

# Spider to fetch RSS from planet schule
class MemuchoSpider(CrawlSpider, LomBase, JSONBase):
  name='memucho_spider'
  friendlyName='memucho'
  url = 'https://memucho.de'
  start_urls = ['https://memucho.de/api/edusharing/search?pageSize=999999']
  version = '0.1'

  def __init__(self, **kwargs):
    LomBase.__init__(self, **kwargs)


  def mapResponse(self, response):
      return LomBase.mapResponse(self, response)

  def getId(self, response):
    return response.meta['item'].get('TopicId')
  def getHash(self, response):
    # @TODO: Api currently does not seem to have a hash value
    return time.time()

  def parse(self, response):
      data = json.loads(response.body_as_unicode())
      
      for item in data.get('Items'):
        copyResponse = response.copy()
        copyResponse.meta['item'] = item
        if self.hasChanged(copyResponse):
          yield scrapy.Request(url = item.get('ItemUrl'), callback = self.handleLink, meta = {'item': item})

  def handleLink(self, response):
    return LomBase.parse(self, response)

  # thumbnail is always the same, do not use the one from rss
  def getBase(self, response):
    base = LomBase.getBase(self, response)
    thumb = response.xpath('//meta[@property="og:image"]//@content').get()
    if thumb:
      base.add_value('thumbnail', self.url + thumb.replace('_350','_1000'))
    # base.add_value('thumbnail', self.url + '/Images/Categories/' + str(self.getId(response)) + '_1000.jpg')
    return base

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(self, response)
    general.add_value('title', response.meta['item'].get('Name').strip())
    general.add_value('keyword', list(filter(lambda x: x,map(lambda x: x.strip(), response.xpath('//*[@id="ContentModuleApp"]//*[@class="topic-name"]//text()').getall()))))
    description = '\n'.join(list(filter(lambda x: x,map(lambda x: x.strip(), response.xpath('//*[@id="ContentModuleApp"]//*[@content-module-type="inlinetext"]//p//text()').getall())))).strip()
    general.add_value('description', description)
    return general
    

  def getLOMTechnical(self, response):
    technical = LomBase.getLOMTechnical(self, response)
    technical.add_value('format', 'text/html')
    technical.add_value('location', response.url)
    return technical
 
  def getLicense(self, response):
    license = LomBase.getLicense(self, response)
    license.add_value('url', Constants.LICENSE_CC_BY_40)
    return license
    
  def getValuespaces(self, response):
    valuespaces = LomBase.getValuespaces(self, response)
    return valuespaces

