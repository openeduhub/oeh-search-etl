from converter.items import *
from .lom_base import LomBase
import logging
import vobject
import scrapy


class OAIBase(scrapy.Spider, LomBase):
    verb = "ListIdentifiers"
    baseUrl = None
    metadataPrefix = None
    set = None

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def getId(self, response):
        response.selector.remove_namespaces()
        if "header" in response.meta:
            header = response.meta["header"]
        else:
            header = response.xpath("//OAI-PMH/GetRecord/record/header")
        return header.xpath("identifier//text()").extract_first()

    def getHash(self, response):
        response.selector.remove_namespaces()
        if "header" in response.meta:
            header = response.meta["header"]
        else:
            header = response.xpath("//OAI-PMH/GetRecord/record/header")
        return header.xpath("datestamp//text()").extract_first() + self.version

    def start_requests(self):
        listIdentifiersUrl = (
            self.baseUrl
            + "?verb="
            + self.verb
            + "&set="
            + self.set
            + "&metadataPrefix="
            + self.metadataPrefix
        )
        logging.info("OAI starting at " + listIdentifiersUrl)
        yield scrapy.Request(url=listIdentifiersUrl, callback=self.parse)

    def getRecordUrl(self, identifier):
        return (
            self.baseUrl
            + "?verb=GetRecord&identifier="
            + identifier
            + "&metadataPrefix="
            + self.metadataPrefix
        )

    def parse(self, response):
        response.selector.remove_namespaces()
        for header in response.xpath("//OAI-PMH/ListIdentifiers/header"):
            copyResponse = response.copy()
            copyResponse.meta["header"] = header
            if self.hasChanged(copyResponse):
                identifier = header.xpath("identifier//text()").extract_first()
                getrecordUrl = self.getRecordUrl(identifier)
                self.logger.debug("getrecordUrl: %s", getrecordUrl)
                yield scrapy.Request(url=getrecordUrl, callback=self.parseRecord)

        resumptionToken = response.xpath(
            "//OAI-PMH/ListIdentifiers/resumptionToken//text()"
        ).extract_first()
        if resumptionToken:
            self.logger.info("resumptionToken: %s", resumptionToken)
            nextUrl = (
                self.baseUrl
                + "?verb="
                + self.verb
                + "&resumptionToken="
                + resumptionToken
            )
            yield scrapy.Request(url=nextUrl, callback=self.parse)

    async def parseRecord(self, response):
        lom = await LomBase.parse(self, response)
        return lom

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        response.selector.remove_namespaces()
        record = response.xpath("//OAI-PMH/GetRecord/record")
        base.add_value(
            "fulltext",
            record.xpath(
                "metadata/lom/general/description/string//text()"
            ).extract_first(),
        )
        thumbnail = record.xpath(
            'metadata/lom/relation/kind/value[text()="hasthumbnail"]/parent::*/parent::*/resource/description/string//text()'
        ).get()
        if thumbnail:
            base.add_value("thumbnail", thumbnail)
        # publisher
        contributers = record.xpath("metadata/lom/lifeCycle/contribute")
        for contributer in contributers:
            role = contributer.xpath("role/value//text()").extract_first()
            if role == "publisher":
                vcardStr = contributer.xpath("entity//text()").extract_first()
                vcard = vobject.readOne(vcardStr)
                if hasattr(vcard, "fn"):
                    base.add_value("publisher", vcard.fn.value)
        return base

    def getLOMGeneral(self, response):
        response.selector.remove_namespaces()
        record = response.xpath("//OAI-PMH/GetRecord/record")

        general = LomBase.getLOMGeneral(response)
        general.add_value(
            "identifier", record.xpath("header/identifier//text()").extract_first()
        )
        general.add_value(
            "title",
            record.xpath("metadata/lom/general/title/string//text()").extract_first(),
        )
        general.add_value(
            "description",
            record.xpath(
                "metadata/lom/general/description/string//text()"
            ).extract_first(),
        )
        keywords = record.xpath("metadata/lom/general/keyword/string//text()").getall()
        general.add_value("keyword", keywords)
        return general

    def getLOMEducational(self, response):
        response.selector.remove_namespaces()
        record = response.xpath("//OAI-PMH/GetRecord/record")

        educational = LomBase.getLOMEducational(response)

        tarString = record.xpath(
            "metadata/lom/educational/typicalAgeRange/string//text()"
        ).extract_first()
        if tarString:
            tar = LomAgeRangeItemLoader()
            tarSplitted = tarString.split("-")
            if len(tarSplitted) > 1:
                tar.add_value("fromRange", tarSplitted[0])
                tar.add_value("toRange", tarSplitted[1])
                educational.add_value("typicalAgeRange", tar.load_item())
            else:
                self.logger.info("unknown agerange %s", tarString)
        educational.add_value(
            "language",
            record.xpath("metadata/lom/educational/language//text()").extract_first(),
        )
        return educational

    def getLOMTechnical(self, response):
        response.selector.remove_namespaces()
        record = response.xpath("//OAI-PMH/GetRecord/record")

        technical = LomBase.getLOMTechnical(response)
        technicalEntries = record.xpath("metadata/lom/technical")
        found = False
        for entry in technicalEntries:
            format = entry.xpath("format//text()").extract_first()
            if format == "text/html":
                found = True
                technical.add_value(
                    "format", entry.xpath("format//text()").extract_first()
                )
                technical.add_value("size", entry.xpath("size//text()").extract_first())
                technical.add_value(
                    "location", entry.xpath("location//text()").extract_first()
                )
        if not found:
            technical.add_value(
                "format",
                record.xpath("metadata/lom/technical/format//text()").extract_first(),
            )
            technical.add_value(
                "size",
                record.xpath("metadata/lom/technical/size//text()").extract_first(),
            )
            technical.add_value(
                "location",
                record.xpath("metadata/lom/technical/location//text()").extract_first(),
            )
        return technical

    def getLOMLifecycle(self, response):
        response.selector.remove_namespaces()
        record = response.xpath("//OAI-PMH/GetRecord/record")

        role = record.xpath(
            "metadata/lom/lifeCycle/contribute/role/value//text()"
        ).extract_first()
        lifecycle = LomBase.getLOMLifecycle(response)
        entity = record.xpath(
            "metadata/lom/lifeCycle/contribute/entity//text()"
        ).extract_first()
        if entity:
            vcard = vobject.readOne(entity)
            if hasattr(vcard, "n"):
                given = vcard.n.value.given
                family = vcard.n.value.family
                lifecycle.add_value("role", role)
                lifecycle.add_value("firstName", given)
                lifecycle.add_value("lastName", family)
        return lifecycle

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        record = response.xpath("//OAI-PMH/GetRecord/record")

        lrts = record.xpath(
            "metadata/lom/educational/learningResourceType/value//text()"
        ).getall()
        valuespaces.add_value("learningResourceType", lrts)
        ier = record.xpath(
            "metadata/lom/educational/intendedEndUserRole/value//text()"
        ).getall()
        valuespaces.add_value("intendedEndUserRole", ier)
        context = record.xpath(
            "metadata/lom/educational/context/value//text()"
        ).getall()
        valuespaces.add_value("educationalContext", context)
        taxonIds = record.xpath(
            "metadata/lom/classification/taxonPath/taxon/id//text()"
        ).getall()
        valuespaces.add_value("discipline", taxonIds)
        return valuespaces

    def getLicense(self, response=None):
        license = LomBase.getLicense(self, response)
        record = response.xpath("//OAI-PMH/GetRecord/record")
        for desc in record.xpath("metadata/lom/rights/description/string"):
            id = desc.xpath("text()").get()
            if id.startswith("http"):
                license.add_value("url", id)
            else:
                license.add_value("internal", id)
        return license
