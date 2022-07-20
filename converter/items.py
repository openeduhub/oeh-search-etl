# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from typing import Optional, Union

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from w3lib.html import remove_tags, replace_escape_chars


def replace_processor(value):
    if value is not None:
        return replace_escape_chars(remove_tags(value)).strip()
    else:
        return value


class JoinMultivalues(object):
    def __init__(self, separator=" "):
        self.separator = separator

    def __call__(self, values):
        return values


class MutlilangItem(Item):
    key = Field()
    de_DE = Field()


class LomGeneralItem(Item):
    """
    General requirements:
     - at least one of description or keywords must be provided
    """
    # sys:node-uuid or ccm:general_identifier?, may be completely irrelevant, seems to read nowhere
    identifier = Field()
    # cclom:title
    title: str = Field()
    # cclom:general_language, defaults to de_DE, not required,
    # has an allowed value set (the str would actually be an enum)
    language: Union[None, str, list[str]] = Field()
    # cclom:general_keyword
    keyword: Union[None, str, list[str]] = Field(output_processor=JoinMultivalues())
    # potentially obsolete
    coverage = Field()
    # potentially obsolete
    structure = Field()
    # cclom:aggregationlevel, optional, potentially obsolete
    aggregationLevel = Field()
    # cclom:general_description, "Beschreibung"
    description: Optional[str] = Field()


class LomLifecycleItem(Item):
    # depending on the role value (publisher, author, editor), the values will be mapped either to
    # - ccm:lifecyclecontributer_publisher
    # - ccm:lifecyclecontributer_author
    # - ccm:lifecyclecontributer_editor
    role = Field()
    firstName = Field()
    lastName = Field()
    organization = Field()
    email = Field()
    url = Field()
    uuid = Field()
    date = Field()
    "the date of contribution. Will be automatically transformed/parsed"


class LomTechnicalItem(Item):
    format = Field()
    size = Field()
    # "URI/location of the element, multiple values are supported, the first entry is the primary location, while all others are secondary locations"
    # cclom:location
    location = Field(output_processor=JoinMultivalues())
    requirement = Field()
    installationRemarks = Field()
    otherPlatformRequirements = Field()
    # "Duration of the element (e.g. for video or audio). Supported formats for automatic transforming include seconds, HH:MM:SS and ISO 8601 duration (PT0H0M0S)"
    duration = Field()


class LomAgeRangeItem(Item):
    fromRange = Field()
    toRange = Field()


class LomEducationalItem(Item):
    interactivityType = Field()
    # Please use valuespaces.learningResourceType
    # learningResourceType = Field()
    interactivityLevel = Field()
    semanticDensity = Field()
    # Please use valuespaces.intendedEndUserRole
    intendedEndUserRole = Field(
        serializer=MutlilangItem, output_processor=JoinMultivalues()
    )
    # Please use valuespaces.educationalContext
    # context = Field()
    typicalAgeRange = Field(serializer=LomAgeRangeItem)
    difficulty = Field()
    typicalLearningTime = Field()
    description = Field()
    language = Field()


# please use the seperate license data
# class LomRightsItem(Item):
# cost = Field()
# coyprightAndOtherRestrictions = Field()
# description = Field()


class LomClassificationItem(Item):
    cost = Field()
    purpose = Field()
    taxonPath = Field(output_processor=JoinMultivalues())
    description = Field()
    keyword = Field()


class LomBaseItem(Item):
    general = Field(serializer=LomGeneralItem)
    lifecycle = Field(serializer=LomLifecycleItem, output_processor=JoinMultivalues())
    technical = Field(serializer=LomTechnicalItem)
    educational = Field(serializer=LomEducationalItem)
    # rights = Field(serializer=LomRightsItem)
    classification = Field(serializer=LomClassificationItem)


class ResponseItem(Item):
    """Only used in pipelines, not used in es_connector -> "no" equivalent metadata fields"""
    status = Field()
    # will be used to generate a uuid that will be written into
    # ccm:replicationsourceuuid. if missing, the uuid will be generated from baseitem.hash.
    url = Field()
    html = Field()
    # will be used as fulltext if baseitem.fulltext is not populated.
    text = Field()
    headers = Field()
    cookies = Field()
    har = Field()


class ValuespaceItem(Item):
    # ccm:educationalintendedenduserrole
    intendedEndUserRole = Field(output_processor=JoinMultivalues())
    # ccm:taxonid
    discipline = Field(output_processor=JoinMultivalues())
    # ccm:educationalcontext
    educationalContext = Field(output_processor=JoinMultivalues())
    # ccm:educationallearningresourcetype
    learningResourceType = Field(output_processor=JoinMultivalues())
    # ccm:oeh_lrt
    new_lrt = Field(output_processor=JoinMultivalues())
    # ccm:sourceContentType
    sourceContentType = Field(output_processor=JoinMultivalues())
    # ccm:toolCategory
    toolCategory = Field(output_processor=JoinMultivalues())
    # ccm:conditionsOfAccess
    conditionsOfAccess = Field(output_processor=JoinMultivalues())
    # ccm:containsAdvertisement
    containsAdvertisement = Field(output_processor=JoinMultivalues())
    # ccm:price
    price = Field(output_processor=JoinMultivalues())
    # ccm:accessibilitySummary
    accessibilitySummary = Field(output_processor=JoinMultivalues())
    # ccm:dataProtectionConformity
    dataProtectionConformity = Field(output_processor=JoinMultivalues())
    # ccm:fskRating
    fskRating = Field(output_processor=JoinMultivalues())
    # ccm:license_oer
    oer = Field(output_processor=JoinMultivalues())


class LicenseItem(Item):
    url = Field()
    "url to a license description"
    internal = Field()
    "a internal constants for this license"
    description = Field()
    "a custom, free-text license description. Will only be used if the internal constants is set to CUSTOM"
    oer = Field()
    "a value of OerType (if empty, will be mapped via the given url or internal value)"
    author = Field()
    "an author freetext (basically, how the author should be named in case this is a by-license"
    expirationDate = Field()
    "a date at which any content license expires and the content shouldn't be delivered anymore"


class PermissionItem(Item):
    public = Field()
    "Should this item be public (accessible for anyone)"
    groups = Field(output_processor=JoinMultivalues())
    "Global Groups that should have access to this object"
    mediacenters = Field(output_processor=JoinMultivalues())
    "Mediacenters that should have access to this object"
    autoCreateGroups = Field()
    "Should global groups be created if they don't exist"
    autoCreateMediacenters = Field()
    "Should media centers be created  if they don't exist"


class BaseItem(Item):
    # ccm:replicationsourceid
    sourceId = Field()
    # ccm:replicationsourceuuid, not used anyhwere, seems to always default to None, should probably always be None
    # explicit uuid of the target element, please only set this if you actually know the uuid of the internal document
    uuid = Field()
    # ccm:replicationsourcehash, gets populated by various crawlers
    hash = Field()
    # probably not used, currently always defaults to None
    # id of collections this entry should be placed into
    collection = Field(output_processor=JoinMultivalues())
    # in case it was fetched from a referatorium, the real origin name may be included here
    # EduSharingBase sets this to ccm:replicationsource, es_connector maps it back to ccm:replicationsourceorigin,
    # es_connector assigns spider name to ccm:replicationsource => can probably be removed...
    origin = Field()
    response = Field(serializer=ResponseItem)
    # seems to be unused, seems to be mostly hardcoded to 1
    ranking = Field()
    # populated in a pipeline with response.text if not explicitly initialized from before.
    # will be posted to edusharing service with an extra post call and is not part of the metadata profile
    fulltext = Field()
    # thumbnail is either a string pointing to the uri from where to load a thumbnail.
    # the pipeline then processes it to a dictionary of {mimetype, small, optional(large)} via requesting
    # either the url to the thumbnail or telling splash to render the page (if no thumbnail url is available and the
    # url points to a html document), the small/large entries in the dict are the thumbnail data in base64.
    # this data is then posted with an individual request to edusharing service -> no corresponding metadata entry.
    thumbnail = Field()
    # seems to be ignored (some crawlers populate it but it doesn't get read anywhere)
    lastModified = Field()
    lom = Field(serializer=LomBaseItem)
    valuespaces = Field(serializer=ValuespaceItem)
    # "permissions (access rights) for this entry"
    permissions = Field(serializer=PermissionItem)
    license = Field(serializer=LicenseItem)
    # ?
    publisher = Field()
    # "editorial notes"
    notes = Field()
    # "binary data which should be uploaded (raw data)"
    binary = Field()


class BaseItemLoader(ItemLoader):
    default_item_class = BaseItem
    # default_input_processor = MapCompose(replace_processor)
    default_output_processor = TakeFirst()


class MutlilangItemLoader(ItemLoader):
    default_item_class = MutlilangItem
    default_output_processor = TakeFirst()


class ValuespaceItemLoader(ItemLoader):
    default_item_class = ValuespaceItem
    default_output_processor = TakeFirst()


class LicenseItemLoader(ItemLoader):
    default_item_class = LicenseItem
    default_output_processor = TakeFirst()


class LomBaseItemloader(ItemLoader):
    default_item_class = LomBaseItem
    default_output_processor = TakeFirst()


class ResponseItemLoader(ItemLoader):
    default_item_class = ResponseItem
    default_output_processor = TakeFirst()


class LomGeneralItemloader(ItemLoader):
    default_item_class = LomGeneralItem
    default_output_processor = TakeFirst()


class LomLifecycleItemloader(ItemLoader):
    default_item_class = LomLifecycleItem
    default_output_processor = TakeFirst()


class LomTechnicalItemLoader(ItemLoader):
    default_item_class = LomTechnicalItem
    default_output_processor = TakeFirst()


class LomAgeRangeItemLoader(ItemLoader):
    default_item_class = LomAgeRangeItem
    default_output_processor = TakeFirst()


class LomEducationalItemLoader(ItemLoader):
    default_item_class = LomEducationalItem
    default_output_processor = TakeFirst()


# class LomRightsItemLoader(ItemLoader):
#    default_item_class = LomRightsItem
#    default_output_processor = TakeFirst()
class LomClassificationItemLoader(ItemLoader):
    default_item_class = LomClassificationItem
    default_output_processor = TakeFirst()


class PermissionItemLoader(ItemLoader):
    default_item_class = PermissionItem
    default_output_processor = TakeFirst()
