from converter.spiders.oai_base import OAIBase

class OAISodis(OAIBase):
    verb="listIdentifiers"
    baseUrl = "https://sodis.de/cp/oai_pmh/oai.php"
    metadataPrefix = "oai_lom-de"
    set = "oer_mebis_activated"

    name="oai_sodis_spider"
    friendlyName='OAI Sodis'
    url = baseUrl
    version = '0.1'

    def getBase(self, response):
        base = OAIBase.getBase(self, response)
        record = response.xpath('//OAI-PMH/GetRecord/record')
        for relation in record.xpath('metadata/lom/relation'):
            kind = relation.xpath('kind/value//text()').extract_first()
            if kind == 'hasthumbnail':
                thumbUrl = relation.xpath('resource/description/string//text()').extract_first()
                base.add_value('thumbnail', thumbUrl)
        return base

    def parseRecord(self, response):    
        lom = OAIBase.parseRecord(self, response)

        if 'publisher' in lom:
            publisher = lom['publisher']
            if publisher:
                publisher = publisher.lower()
                if 'siemens' in publisher:
                    self.logger.info('PUBLISHER is siemens return None: %s',publisher);
                    return None

        return lom
