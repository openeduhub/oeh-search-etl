from scrapy.spiders import CrawlSpider
from converter.items import *
import time
import logging
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;

class RSSSpider(CrawlSpider, LomBase):
    name='rss_spider'
    start_urls = ['https://feeds.br.de/telekolleg-mathematik/feed.xml']
    commonProperties = {}
    
    def parse(self, response):
        response.selector.remove_namespaces()
        #common properties
        self.commonProperties['language'] = response.xpath('//rss/channel/language//text()').get()
        self.commonProperties['source'] = response.xpath('//rss/channel/generator//text()').get()
        self.commonProperties['publisher'] = response.xpath('//rss/channel/author//text()').get()
        self.commonProperties['thumbnail'] = response.xpath('//rss/channel/image/url//text()').get()

        for item in response.xpath('//rss/channel/item'):
            base = self.getBase(item)
            base.add_value('lom', self.parseItem(item).load_item())
            yield base.load_item()
                    
    def parseItem(self, item):
        return self.getLOM(item)
    
    def getBase(self, item):
        base = BaseItemLoader()
        base.add_value('sourceId', item.xpath('guid//text()').get() )
        base.add_value('hash', time.time())
        base.add_value('fulltext', item.xpath('description//text()').get())
        thumbnail = self.commonProperties['thumbnail']
        if thumbnail:
            base.add_value('thumbnail', thumbnail)
        return base

    def getLOMGeneral(self, item):
        general = LomBase.getLOMGeneral(item)
        general.add_value('identifier', item.xpath('guid//text()').get())
        general.add_value('title', item.xpath('title//text()').get())  
        general.add_value('description', item.xpath('description//text()').get())
        general.add_value('language', self.commonProperties['language'])
        return general

    def getLOMTechnical(self, item):
        technical = LomBase.getLOMTechnical(item)
        technical.add_value('format', item.xpath('enclosure/@type').get())
        technical.add_value('size', item.xpath('enclosure/@length').get())
        technical.add_value('location', item.xpath('enclosure/@url').get())
        return technical