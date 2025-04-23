import hashlib

from converter.items import (
    BaseItemLoader,
    LicenseItemLoader,
    LomAgeRangeItemLoader,
    LomEducationalItemLoader,
    LomGeneralItemloader,
    LomTechnicalItemLoader,
    ValuespaceItemLoader,
)

from .lom_base import LomBase


# rss crawler with a list of entries to crawl and map
class CSVBase(LomBase):
    # column names supported:
    COLUMN_URL = "url"
    COLUMN_TITLE = "title"
    COLUMN_SOURCE_TITLE = "sourceTitle"
    COLUMN_SOURCE_URL = "sourceUrl"
    COLUMN_DESCRIPTION = "description"
    COLUMN_TYPE = "type"
    COLUMN_THUMBNAIL = "thumbnail"
    COLUMN_KEYWORD = "keyword"
    COLUMN_EDUCATIONAL_CONTEXT = "educationalContext"
    COLUMN_TYPICAL_AGE_RANGE_FROM = "typicalAgeRangeFrom"
    COLUMN_TYPICAL_AGE_RANGE_TO = "typicalAgeRangeTo"
    COLUMN_DISCIPLINE = "discipline"
    COLUMN_LEARNING_RESOURCE_TYPE = "learningResourceType"
    COLUMN_LANGUAGE = "language"
    COLUMN_COLLECTION = "collection"
    COLUMN_LICENSE = "license"
    mappings = None

    def transform(self, row):
        transformed = {}
        for i, key in enumerate(row):
            transformed[self.mappings[i]] = {
                "text": key.strip(),
                "list": list(map(lambda x: x.strip(), key.split(";"))),
            }
            if (
                len(
                    list(
                        filter(lambda x: x != "", transformed[self.mappings[i]]["list"])
                    )
                )
                == 0
            ):
                transformed[self.mappings[i]]["list"] = None
        return transformed

    def read_csv(self, csv, skip_lines=1):
        data = []
        i = 0
        for row in csv:
            if self.mappings is None:
                self.mappings = row
                continue
            i += 1
            if i < skip_lines:
                continue
            data.append(self.transform(row))
        return data

    def getUri(self, response=None) -> str:
        return response.meta["row"][CSVBase.COLUMN_URL]["text"]

    def getId(self, response=None) -> str:
        return response.meta["row"][CSVBase.COLUMN_URL]["text"]

    def getHash(self, response=None) -> str:
        m = hashlib.md5()
        m.update(str(response.meta["row"]).encode("utf-8"))
        return m.hexdigest() + self.version

    def getBase(self, response=None) -> BaseItemLoader:
        base: BaseItemLoader = LomBase.getBase(self, response)
        base.add_value(
            "thumbnail", response.meta["row"][CSVBase.COLUMN_THUMBNAIL]["text"]
        )
        base.add_value(
            "collection", response.meta["row"][CSVBase.COLUMN_COLLECTION]["list"]
        )
        base.replace_value("type", response.meta["row"][CSVBase.COLUMN_TYPE]["text"])
        return base

    def getLOMGeneral(self, response=None) -> LomGeneralItemloader:
        general: LomGeneralItemloader = LomBase.getLOMGeneral(self, response)
        general.add_value("title", response.meta["row"][CSVBase.COLUMN_TITLE]["text"])
        general.replace_value(
            "language", response.meta["row"][CSVBase.COLUMN_LANGUAGE]["text"]
        )
        general.add_value(
            "keyword", response.meta["row"][CSVBase.COLUMN_KEYWORD]["list"]
        )
        general.add_value(
            "description", response.meta["row"][CSVBase.COLUMN_DESCRIPTION]["text"]
        )
        return general

    def getLicense(self, response=None) -> LicenseItemLoader:
        license: LicenseItemLoader = LomBase.getLicense(self, response)
        # add as url + internal to support both data formats
        license.add_value("url", response.meta["row"][CSVBase.COLUMN_LICENSE]["text"])
        license.add_value(
            "internal", response.meta["row"][CSVBase.COLUMN_LICENSE]["text"]
        )
        return license

    def getLOMEducational(self, response=None) -> LomEducationalItemLoader:
        educational: LomEducationalItemLoader = LomBase.getLOMEducational(self, response)
        tar = LomAgeRangeItemLoader()
        tar.add_value(
            "fromRange",
            response.meta["row"][CSVBase.COLUMN_TYPICAL_AGE_RANGE_FROM]["text"],
        )
        tar.add_value(
            "toRange", response.meta["row"][CSVBase.COLUMN_TYPICAL_AGE_RANGE_TO]["text"]
        )
        educational.add_value("typicalAgeRange", tar.load_item())
        return educational

    def getLOMTechnical(self, response=None) -> LomTechnicalItemLoader:
        technical: LomTechnicalItemLoader = LomBase.getLOMTechnical(self, response)
        technical.add_value(
            "location", response.meta["row"][CSVBase.COLUMN_URL]["text"]
        )
        technical.add_value("format", "text/html")
        return technical

    def getValuespaces(self, response) -> ValuespaceItemLoader:
        valuespaces: ValuespaceItemLoader = LomBase.getValuespaces(self, response)
        valuespaces.add_value(
            "educationalContext",
            response.meta["row"][CSVBase.COLUMN_EDUCATIONAL_CONTEXT]["list"],
        )
        valuespaces.add_value(
            "discipline", response.meta["row"][CSVBase.COLUMN_DISCIPLINE]["list"]
        )
        valuespaces.add_value(
            "learningResourceType",
            response.meta["row"][CSVBase.COLUMN_LEARNING_RESOURCE_TYPE]["list"],
        )
        return valuespaces
