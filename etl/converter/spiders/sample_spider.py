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
  url = 'https://edu-sharing.com' # the url which will be linked as the primary link to your source (should be the main url of your site)
  friendlyName = 'Sample Source' # name as shown in the search ui
  start_urls = ['https://edu-sharing.com']
  version = '0.1' # the version of your crawler, used to identify if a reimport is necessary

  def parse(self, response):
    return LomBase.parse(self, response)

  # return a (stable) id of the source
  def getId(self, response):
    return response.xpath('//title//text()').get()

  # return a stable hash to detect content changes
  # if there is no hash available, may use the current time as "always changing" info
  # Please include your crawler version as well
  def getHash(self, response):
    return self.version + time.time()

  def getBase(self, response):
    base = LomBase.getBase(self, response)
    return base

  def getLOMGeneral(self, response):
    general = LomBase.getLOMGeneral(self, response)
    general.add_value('title', response.xpath('//title//text()').get())
    general.add_value('language', response.xpath('//meta[@property="og:locale"]/@content').get())
    return general

  def getLOMTechnical(self, response):
    technical = LomBase.getLOMTechnical(self, response)
    technical.add_value('format', 'text/html')
    technical.add_value('size', len(response.body))
    return technical

  # You may override more lom container here