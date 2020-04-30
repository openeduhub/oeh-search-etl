from converter.items import *
from converter.spiders.lom_base import LomBase;
import logging
import vobject

class OAIBase(scrapy.Spider, LomBase):
    verb="ListIdentifiers"
    baseUrl = None
    metadataPrefix = None
    set = None

    def getId(self, response):
        response.selector.remove_namespaces()
        record = response.xpath('//OAI-PMH/GetRecord/record')
        return record.xpath('header/identifier//text()').extract_first()

    def getHash(self, response):
        response.selector.remove_namespaces()
        record = response.xpath('//OAI-PMH/GetRecord/record')
        return record.xpath('header/datestamp//text()').extract_first() + self.version

    def start_requests(self):
        listIdentifiersUrl = self.baseUrl + "?verb=" + self.verb + "&set=" + self.set +"&metadataPrefix=" + self.metadataPrefix
        logging.info('OAI starting at ' + listIdentifiersUrl)
        yield scrapy.Request(url=listIdentifiersUrl, callback=self.parse)

    def parse(self, response):
        response.selector.remove_namespaces()
        for header in response.xpath('//OAI-PMH/ListIdentifiers/header'):

            identifier = header.xpath('identifier//text()').extract_first()
            getrecordUrl = self.baseUrl +"?verb=GetRecord&identifier=" +identifier+"&metadataPrefix="+self.metadataPrefix
            self.logger.info('getrecordUrl: %s', getrecordUrl)
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
        base = LomBase.getBase(self, response)
        response.selector.remove_namespaces()
        record = response.xpath('//OAI-PMH/GetRecord/record')
        base.add_value('fulltext', record.xpath('metadata/lom/general/description/string//text()').extract_first())
        
        #publisher
        contributers = record.xpath('metadata/lom/lifeCycle/contribute')
        for contributer in contributers:
           role = contributer.xpath('role/value//text()').extract_first()
           if role == 'publisher':
               vcardStr = contributer.xpath('entity//text()').extract_first()
               vcard = vobject.readOne(vcardStr)      
               base.add_value('publisher',vcard.fn.value)
        return base

    def getLOMGeneral(self, response):
        response.selector.remove_namespaces()
        record = response.xpath('//OAI-PMH/GetRecord/record')

        general = LomBase.getLOMGeneral(response)
        general.add_value('identifier', record.xpath('header/identifier//text()').extract_first())
        general.add_value('title', record.xpath('metadata/lom/general/title/string//text()').extract_first())
        keywords = record.xpath('metadata/lom/general/keyword/string//text()').getall()
        general.add_value('keyword', keywords )
        return general

    def getLOMEducational(self, response):
        response.selector.remove_namespaces()
        record = response.xpath('//OAI-PMH/GetRecord/record')

        educational = LomBase.getLOMEducational(response)
        #TODO put in general description
        educational.add_value('description', record.xpath('metadata/lom/general/description/string//text()').extract_first())
        tarString = record.xpath('metadata/lom/educational/typicalAgeRange/string//text()').extract_first()
        if tarString:
            tar = LomAgeRangeItemLoader()
            tarSplitted = tarString.split('-')
            if len(tarSplitted) > 1:
                tar.add_value('fromRange',tarSplitted[0])
                tar.add_value('toRange',tarSplitted[1])
                educational.add_value('typicalAgeRange',tar.load_item())
            else:
                self.logger.info('unknown agerange %s',tarString) 
        educational.add_value('language',record.xpath('metadata/lom/educational/language//text()').extract_first())
        return educational
    
    def getLOMTechnical(self, response):
        response.selector.remove_namespaces()
        record = response.xpath('//OAI-PMH/GetRecord/record')

        technical = LomBase.getLOMTechnical(response)
        technical.add_value('format', record.xpath('metadata/lom/technical/format//text()').extract_first())
        technical.add_value('size', record.xpath('metadata/lom/technical/size//text()').extract_first())
        technical.add_value('location', record.xpath('metadata/lom/technical/location//text()').extract_first())
        return technical

    def getLOMLifecycle(self, response):
        response.selector.remove_namespaces()
        record = response.xpath('//OAI-PMH/GetRecord/record')

        role = record.xpath('metadata/lom/lifeCycle/contribute/role/value//text()').extract_first()
        lifecycle = LomBase.getLOMLifecycle(response)
        lifecycle.add_value('role',role)
        entity = record.xpath('metadata/lom/lifeCycle/contribute/entity//text()').extract_first()
        if entity:
            vcard = vobject.readOne(entity)
            given = vcard.n.value.given
            family = vcard.n.value.family
            lifecycle.add_value('firstName',given)
            lifecycle.add_value('lastName',family)
        return lifecycle
        


    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        record = response.xpath('//OAI-PMH/GetRecord/record')

        lrts = record.xpath('metadata/lom/educational/learningResourceType/value//text()').getall()
        valuespaces.add_value('learningResourceType', lrts)
        ier = record.xpath('metadata/lom/educational/intendedEndUserRole/value//text()').getall()
        valuespaces.add_value('intendedEndUserRole', ier)
        context = record.xpath('metadata/lom/educational/context/value//text()').getall()
        valuespaces.add_value('educationalContext',context)
        taxonIds = record.xpath('metadata/lom/classification/taxonPath/taxon/id//text()').getall()
        valuespaces.add_value('discipline', taxonIds)
        return valuespaces

    def getLicense(self, response = None):
        license = LomBase.getLicense(self,response);
        record = response.xpath('//OAI-PMH/GetRecord/record')
        rightsDescriptions = record.xpath('metadata/lom/rights/description/string//text()').getall()
        if rightsDescriptions:
            separator = "; "
            license.add_value('internal', separator.join(rightsDescriptions));
        return license



