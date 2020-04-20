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
            responseCopy = response.copy()
            responseCopy.meta['item'] = item
            yield LomBase.parse(self, response)

    def getId(self, response):
        return response.meta['item'].xpath('link//text()').get()

    def getHash(self, response):
        return self.version + response.meta['item'].xpath('pubDate//text()').get()

    def mapResponse(self, response):
        r = ResponseItemLoader()
        r.add_value('url', response.meta['item'].xpath('link//text()').get())
        return r

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        thumbnail = self.commonProperties['thumbnail']
        if thumbnail:
            base.add_value('thumbnail', thumbnail)
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value('identifier', response.meta['item'].xpath('guid//text()').get())
        general.add_value('title', response.meta['item'].xpath('title//text()').get())  
        general.add_value('language', self.commonProperties['language'])
        return general
        
    def getLOMEducational(self, response):
        educational = LomBase.getLOMEducational(self, response)
        description = response.meta['item'].xpath('description//text()').get()
        if not description:
            description = response.meta['item'].xpath('//*[name()="summary"]//text()').get()
        educational.add_value('description', description)
        return educational

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        #technical.add_value('format', item.xpath('enclosure/@type').get())
        #technical.add_value('size', item.xpath('enclosure/@length').get())
        #technical.add_value('location', item.xpath('enclosure/@url').get())
        technical.add_value('format', 'text/html')
        technical.add_value('location', response.meta['item'].xpath('link//text()').get())
        return technical