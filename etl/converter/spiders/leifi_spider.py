from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
from converter.pipelines import ProcessValuespacePipeline;
import requests
from html.parser import HTMLParser
from converter.constants import Constants;

# LEIFIphysik spider for xml data file
class LeifiSpider(scrapy.Spider, LomBase):
  name='leifi_spider'
  friendlyName = 'LEIFIphysik'
  url = 'https://www.leifiphysik.de/'
  rssUrl = 'http://localhost/sources/leifi_feed_rss.xml'
  def start_requests(self):
      yield scrapy.Request(url=self.rssUrl, callback=self.parseList)
  def parseList(self, response):
    ids = []
    for item in response.xpath('//elixier/datensatz'):
       id = item.xpath('id_local//text()').get()
       if not id in ids:
         ids.append(id)
         yield self.parse(item)

  def parse(self, item):
    return LomBase.parse(self, item)

  def getValuespaces(self, item):
    valuespaces = LomBase.getValuespaces(self, item)
    text = item.xpath('systematikpfad//text()').get()
    for entry in ProcessValuespacePipeline.valuespaces['discipline']:
      if len(list(filter(lambda x:x['@value'].casefold() in text.casefold(), entry['label']))):
        valuespaces.add_value('discipline',entry['id'])
    return valuespaces

  def mapResponse(self, item):
    r = ResponseItemLoader()
    r.add_value('url', requests.get(item.xpath('url_datensatz//text()').get()).content.decode('UTF-8'))
    r.add_value('text', requests.get(item.xpath('url_datensatz//text()').get()).content.decode('UTF-8'))
    return r

  def getId(self, item):
    return item.xpath('id_local//text()').get()

  def getHash(self, item):
    return item.xpath('letzte_aenderung//text()').get()

  def getBase(self, item):
    base = LomBase.getBase(self, item)
    base.add_value('lastModified', item.xpath('letzte_aenderung//text()').get())
    return base

  def getLOMGeneral(self, item):
    general = LomBase.getLOMGeneral(self, item)
    general.add_value('title', HTMLParser().unescape(item.xpath('titel//text()').get()))
    general.add_value('language', item.xpath('sprache//text()').get())
    general.add_value('keyword', HTMLParser().unescape(item.xpath('schlagwort//text()').get()).split('; '))
    return general

  def getLOMEducational(self, item):
    educational = LomBase.getLOMEducational(self, item)
    desc = item.xpath('beschreibung//text()').get().strip()
    # dirty cleaning of invalid descriptions
    # not perfect yet, these objects also appear inside the content
    if not desc.startswith('swiffyobject_'):
      educational.add_value('description', HTMLParser().unescape(desc))
    return educational

  def getLOMTechnical(self, item):
    technical = LomBase.getLOMTechnical(self, item)
    technical.add_value('format', 'text/html')
    technical.add_value('location', item.xpath('url_datensatz//text()').get())
    return technical
    
  def getLOMRights(self, item):
    rights = LomBase.getLOMRights(self, item)
    if item.xpath('rechte//text()').get() == 'Keine Angabe, es gilt die gesetzliche Regelung':
      rights.add_value('description', Constants.LICENSE_COPYRIGHT_LAW)
    return rights
