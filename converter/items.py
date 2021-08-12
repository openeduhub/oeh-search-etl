# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

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
    def __init__(self, separator=u" "):
        self.separator = separator

    def __call__(self, values):
        return values


class MutlilangItem(Item):
    key = Field()
    de_DE = Field()


class LomGeneralItem(Item):
    identifier = Field()
    title = Field()
    language = Field()
    keyword = Field(output_processor=JoinMultivalues())
    coverage = Field()
    structure = Field()
    aggregationLevel = Field()
    description = Field()


class LomLifecycleItem(Item):
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
    location = Field()
    requirement = Field()
    installationRemarks = Field()
    otherPlatformRequirements = Field()
    duration = Field()
    "Duration of the element (e.g. for video or audio). Supported formats for automatic transforming include seconds, HH:MM:SS and ISO 8601 duration (PT0H0M0S)"


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
    status = Field()
    url = Field()
    html = Field()
    text = Field()
    headers = Field()
    cookies = Field()
    har = Field()


class ValuespaceItem(Item):
    intendedEndUserRole = Field(output_processor=JoinMultivalues())
    discipline = Field(output_processor=JoinMultivalues())
    educationalContext = Field(output_processor=JoinMultivalues())
    learningResourceType = Field(output_processor=JoinMultivalues())
    sourceContentType = Field(output_processor=JoinMultivalues())
    toolCategory = Field(output_processor=JoinMultivalues())

    conditionsOfAccess = Field(output_processor=JoinMultivalues())
    containsAdvertisement = Field(output_processor=JoinMultivalues())
    price = Field(output_processor=JoinMultivalues())
    accessibilitySummary = Field(output_processor=JoinMultivalues())
    dataProtectionConformity = Field(output_processor=JoinMultivalues())
    fskRating = Field(output_processor=JoinMultivalues())
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
    sourceId = Field()
    uuid = Field()
    "explicit uuid of the target element, please only set this if you actually know the uuid of the internal document"
    hash = Field()
    collection = Field(output_processor=JoinMultivalues())
    "id of collections this entry should be placed into"
    type = Field()
    origin = Field()
    "in case it was fetched from a referatorium, the real origin name may be included here"
    response = Field(serializer=ResponseItem)
    ranking = Field()
    fulltext = Field()
    thumbnail = Field()
    lastModified = Field()
    lom = Field(serializer=LomBaseItem)
    valuespaces = Field(serializer=ValuespaceItem)
    permissions = Field(serializer=PermissionItem)
    "permissions (access rights) for this entry"
    license = Field(serializer=LicenseItem)
    publisher = Field()
    # editorial notes
    notes = Field()


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
