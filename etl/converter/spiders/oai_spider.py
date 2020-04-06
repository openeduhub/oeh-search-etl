from converter.items import *
from converter.spiders.lom_base import LomBase;

class OAISpider(scrapy.Spider, LomBase):
    name = "OAI"
    verb="listIdentifiers"
    baseUrl = None
    metadataPrefix = None
    set = None

    def start_requests(self):
        listIdentifiersUrl = self.baseUrl + "?verb=" + self.verb + "&set=" + self.set +"&metadataPrefix=" + self.metadataPrefix
        yield scrapy.Request(url=listIdentifiersUrl, callback=self.parse)

    def parse(self, response):
        response.selector.remove_namespaces()
        for header in response.xpath('//OAI-PMH/ListIdentifiers/header'):

            identifier = header.xpath('identifier//text()').extract_first()
            getrecordUrl = self.baseUrl +"?verb=getRecord&identifier=" +identifier+"&metadataPrefix="+self.metadataPrefix
            yield scrapy.Request(url=getrecordUrl, callback=self.parseRecord)

        resumptionToken = response.xpath('//OAI-PMH/ListIdentifiers/resumptionToken//text()').extract_first()
        if resumptionToken:
            self.logger.info('resumptionToken: %s', resumptionToken)
            nextUrl = self.baseUrl + "?verb=" + self.verb +"&resumptionToken=" +resumptionToken
            yield scrapy.Request(url=nextUrl, callback=self.parse)

    def parseRecord(self, response):    
        lom = LomBase.parse(self, response)
        return lom

    def getBase(self, response):
        response.selector.remove_namespaces()
        record = response.xpath('//OAI-PMH/GetRecord/record')

        base = BaseItemLoader()
        base.add_value('sourceId', record.xpath('header/identifier//text()').extract_first())
        base.add_value('hash', record.xpath('header/identifier//text()').extract_first())
        base.add_value('fulltext', record.xpath('metadata/lom/general/description/string//text()').extract_first())
        return base

    def getLOMGeneral(self, response):
        response.selector.remove_namespaces()
        record = response.xpath('//OAI-PMH/GetRecord/record')

        general = LomBase.getLOMGeneral(response)
        general.add_value('identifier', record.xpath('header/identifier//text()').extract_first())
        general.add_value('title', record.xpath('metadata/lom/general/title/string//text()').extract_first())
        keywords = record.xpath('metadata/lom/general/keyword/string//text()').getall()
        self.logger.info(keywords)
        general.add_value('keyword', keywords )
        #general.add_value('keyword', response.xpath('metadata/lom/general/keyword/string//text()').extract_first())
        return general

