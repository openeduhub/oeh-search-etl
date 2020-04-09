from scrapy.spiders import CrawlSpider
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
import json

# Sample Spider, using a SitemapSpider to crawl your web page
# Can be used as a template for your custom spider
class SampleSpider(CrawlSpider, LomBase):
  name = 'sample_spider'
  friendlyName = 'Sample Source' # name as shown in the search ui
  start_urls = ['https://edu-sharing.com']

  def parse(self, response):
    return LomBase.parse(self, response)

  def getBase(self, response):
    base = BaseItemLoader()
    base.add_value('sourceId', response.xpath('//title//text()').get())
    # use a stable hash to detect content changes
    # if there is no hash available, may use the current time as "always changing" info
    base.add_value('hash', time.time())
    return base

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(response)
    general.add_value('title', response.xpath('//title//text()').get())
    general.add_value('language', response.xpath('//meta[@property="og:locale"]/@content').get())
    return general

  def getLOMTechnical(self, response):
    technical = LomBase.getLOMTechnical(response)
    technical.add_value('format', 'text/html')
    technical.add_value('size', len(response.body))
    return technical

  # You may override more lom container here