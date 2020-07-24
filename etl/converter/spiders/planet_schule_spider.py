from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
from converter.spiders.rss_base import RSSBase;
import json
import logging
from html.parser import HTMLParser
from converter.pipelines import ProcessValuespacePipeline;
import re
from converter.valuespace_helper import ValuespaceHelper;
from converter.constants import Constants;

# Spider to fetch RSS from planet schule
class PlanetSchuleSpider(RSSBase):
  name='planet_schule_spider'
  friendlyName='planet schule'
  url = 'https://www.planet-schule.de'
  start_urls = ['https://www.planet-schule.de/data/planet-schule-vodcast-komplett.rss']
  version = '0.1'

  def __init__(self, **kwargs):
    RSSBase.__init__(self, **kwargs)

  def mapResponse(self, response):
      return LomBase.mapResponse(self, response)

  def startHandler(self, response):
      for item in response.xpath('//rss/channel/item'):
        copyResponse = response.copy()
        copyResponse.meta['item'] = item
        if self.hasChanged(copyResponse):
          yield scrapy.Request(url = item.xpath('link//text()').get(), callback = self.handleLink, meta = {'item': item})

  def handleLink(self, response):
    return LomBase.parse(self, response)

  # thumbnail is always the same, do not use the one from rss
  def getBase(self, response):
    return LomBase.getBase(self, response)

  def getLOMGeneral(self, response):
    general = RSSBase.getLOMGeneral(self, response)
    general.add_value('keyword', response.xpath('//div[@class="sen_info_v2"]//p[contains(text(),"Schlagworte")]/parent::*/parent::*/div[last()]/p/a//text()').getall())
    return general

  def getLOMTechnical(self, response):
    technical = LomBase.getLOMTechnical(self, response)
    technical.add_value('format', 'text/html')
    technical.add_value('location', response.url)
    return technical
 
  def getLicense(self, response):
    license = LomBase.getLicense(self, response)
    license.add_value('internal', Constants.LICENSE_COPYRIGHT_LAW)
    return license
    
  def getValuespaces(self, response):
    valuespaces = RSSBase.getValuespaces(self, response)
    try:
      range = response.xpath('//div[@class="sen_info_v2"]//p[contains(text(),"Klassenstufe")]/parent::*/parent::*/div[last()]/p//text()').get()
      range = range.split(" - ")
      valuespaces.add_value('educationalContext', ValuespaceHelper.educationalContextByGrade(range))
    except:
      pass
    discipline = response.xpath('//div[@class="sen_info_v2"]//p[contains(text(),"Fächer")]/parent::*/parent::*/div[last()]/p/a//text()').getall()
    valuespaces.add_value('discipline',discipline)
    lrt = ValuespaceHelper.mimetypeToLearningResourceType(response.meta['item'].xpath('enclosure/@type').get())
    if lrt:
      valuespaces.add_value('learningResourceType', lrt)
    return valuespaces

