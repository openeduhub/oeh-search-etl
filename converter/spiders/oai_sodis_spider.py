from .base_classes import OAIBase


class OAISodis(OAIBase):
    verb = "listIdentifiers"
    baseUrl = "https://sodis.de/cp/oai_pmh/oai.php"
    metadataPrefix = "oai_lom-de"
    set = "oer_mebis_activated"

    name = "oai_sodis_spider"
    friendlyName = "FWU Sodis Contentpool"
    url = "https://fwu.de/"
    version = "0.1"

    def __init__(self, **kwargs):
        OAIBase.__init__(self, **kwargs)

    # def getRecordUrl(self, identifier):
    #    return self.baseUrl +"?verb=GetRecord&identifier=" +identifier+"&metadataPrefix="+self.metadataPrefix+"&set="+self.set

    def getBase(self, response):
        base = OAIBase.getBase(self, response)
        record = response.xpath("//OAI-PMH/GetRecord/record")
        for relation in record.xpath("metadata/lom/relation"):
            kind = relation.xpath("kind/value//text()").extract_first()
            if kind == "hasthumbnail":
                thumbUrl = relation.xpath(
                    "resource/description/string//text()"
                ).extract_first()
                base.add_value("thumbnail", thumbUrl)
        return base

    def parseRecord(self, response):
        lom = OAIBase.parseRecord(self, response)
        try:
            if "publisher" in lom:
                publisher = lom["publisher"]
                if publisher:
                    publisher = publisher.lower()
                    if "siemens" in publisher:
                        id = lom["sourceId"]
                        self.logger.info(
                            "PUBLISHER contains siemens return None: %s", id
                        )
                        return None
        except:
            self.logger.info("PUBLISHER was not parsable, will skip entry")
            return None
        return lom
