from scrapy.spiders import CrawlSpider
from converter.items import *
import time
import logging
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;

class RSSBase(CrawlSpider, LomBase):
    start_urls = []
    commonProperties = {}
    response = None

    def parse(self, response):
        response.selector.remove_namespaces()
        #common properties
        self.commonProperties['language'] = response.xpath('//rss/channel/language//text()').get()
        self.commonProperties['source'] = response.xpath('//rss/channel/generator//text()').get()
        self.commonProperties['publisher'] = response.xpath('//rss/channel/author//text()').get()
        self.commonProperties['thumbnail'] = response.xpath('//rss/channel/image/url//text()').get()
        self.response = response
        return self.startHandler(response)
                    
    def startHandler(self, response):
        for item in response.xpath('//rss/channel/item'):
            yield LomBase.parse(self, item)

    def getId(self, item):
        return item.xpath('link//text()').get()

    def getHash(self, item):
        return item.xpath('pubDate//text()').get()

    def mapResponse(self, item):
        r = ResponseItemLoader()
        r.add_value('url', item.xpath('link//text()').get())
        return r

    def getBase(self, item):
        base = LomBase.getBase(self, item)
        thumbnail = self.commonProperties['thumbnail']
        if thumbnail:
            base.add_value('thumbnail', thumbnail)
        return base

    def getLOMGeneral(self, item):
        general = LomBase.getLOMGeneral(self, item)
        general.add_value('identifier', item.xpath('guid//text()').get())
        general.add_value('title', item.xpath('title//text()').get())  
        general.add_value('language', self.commonProperties['language'])
        return general
        
    def getLOMEducational(self, item):
        educational = LomBase.getLOMEducational(self, item)
        description = item.xpath('description//text()').get()
        if not description:
            description = item.xpath('//*[name()="summary"]//text()').get()
        educational.add_value('description', description)
        return educational

    def getLOMTechnical(self, item):
        technical = LomBase.getLOMTechnical(self, item)
        #technical.add_value('format', item.xpath('enclosure/@type').get())
        #technical.add_value('size', item.xpath('enclosure/@length').get())
        #technical.add_value('location', item.xpath('enclosure/@url').get())
        technical.add_value('format', 'text/html')
        technical.add_value('location', item.xpath('link//text()').get())
        return technical