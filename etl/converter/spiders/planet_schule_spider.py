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

# Spider to fetch RSS from planet schule
class PlanetSchuleSpider(RSSBase):
  name='planet_schule_spider'
  friendlyName='planet schule'
  start_urls = ['https://www.planet-schule.de/data/planet-schule-vodcast-komplett.rss']

  response = None
  def mapResponse(self, item):
      return LomBase.mapResponse(self, self.response)

  def startHandler(self, response):
      for item in response.xpath('//rss/channel/item'):
        if self.hasChanged(item):
          yield scrapy.Request(url = item.xpath('link//text()').get(), callback = self.handleLink, meta = {'item': item})

  def handleLink(self, response):
    self.response = response
    return LomBase.parse(self, response.meta['item'])

  # thumbnail is always the same, do not use the one from rss
  def getBase(self, item):
    return LomBase.getBase(self, item)

  def getLOMGeneral(self, item):
    general = RSSBase.getLOMGeneral(self, item)
    general.add_value('keyword', self.response.xpath('//div[@class="sen_info_v2"]//p[contains(text(),"Schlagworte")]/parent::*/parent::*/div[last()]/p/a//text()').getall())
    return general

  def getLOMTechnical(self, item):
    technical = LomBase.getLOMTechnical(self, item)
    technical.add_value('format', 'text/html')
    technical.add_value('location', self.response.url)
    return technical
    
  def getValuespaces(self, item):
    valuespaces = RSSBase.getValuespaces(self, item)
    try:
      range = self.response.xpath('//div[@class="sen_info_v2"]//p[contains(text(),"Klassenstufe")]/parent::*/parent::*/div[last()]/p//text()').get()
      range = range.split(" - ")
      valuespaces.add_value('educationalContext', ValuespaceHelper.educationalContextByAgeRange(range))
    except:
      pass
    discipline = self.response.xpath('//div[@class="sen_info_v2"]//p[contains(text(),"Fächer")]/parent::*/parent::*/div[last()]/p/a//text()').getall()
    valuespaces.add_value('discipline',discipline)
    lrt = ValuespaceHelper.mimetypeToLearningResourceType(item.xpath('enclosure/@type').get())
    if lrt:
      valuespaces.add_value('learningResourceType', lrt)
    return valuespaces

