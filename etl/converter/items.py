# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, BaseItem, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags, replace_escape_chars

def replace_processor(value):
    if value is not None:
        return replace_escape_chars(remove_tags(value)).strip()
    else:
        return value

class LomGeneralItem(Item):
    identifier = Field()
    title = Field()
    language = Field()
    keyword = Field()
    coverage = Field()
    structure = Field()
    aggregationLevel = Field()

class LomLifecycleItem(Item):
    role = Field()
    firstName = Field()
    lastName = Field()
    organization = Field()
    uuid = Field()

class LomTechnicalItem(Item):
    format = Field()
    size = Field()
    location = Field()
    requirement = Field()
    installationRemarks = Field()
    otherPlatformRequirements = Field()
    duration = Field()

class LomAgeRangeItem(Item):
    fromRange = Field()
    toRange = Field()

class LomEducationalItem(Item):
    interactivityType = Field()
    learningResourceType = Field()
    interactivityLevel = Field()
    semanticDensity = Field()
    intentedEndUserRole = Field()
    context = Field()
    typicalAgeRange = Field(serializer=LomAgeRangeItem)
    difficulty = Field()
    typicalLearningTime = Field()
    description = Field()
    language = Field()

class LomRightsItem(Item):
    cost = Field()
    coyprightAndOtherRestrictions = Field()
    description = Field()

class LomClassificationItem(Item):
    cost = Field()
    purpose = Field()
    taxonPath = Field()
    description = Field()
    keyword = Field()

class LomBaseItem(Item):
    general = Field(serializer=LomGeneralItem)
    lifecycle = Field(serializer=LomLifecycleItem)
    technical = Field(serializer=LomTechnicalItem)
    educational = Field(serializer=LomEducationalItem)
    rights = Field(serializer=LomRightsItem)
    classification = Field(serializer=LomRightsItem)

class ResponseItem(Item):
    status = Field()
    url = Field()
    body = Field()
    headers = Field()

class BaseItem(Item):
    sourceId = Field()
    hash = Field()
    response = Field(serializer=ResponseItem)
    ranking = Field()
    fulltext = Field()
    lom = Field(serializer=LomBaseItem)

class BaseItemLoader(ItemLoader):
    default_item_class = BaseItem
    #default_input_processor = MapCompose(replace_processor)
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
class LomRightsItemLoader(ItemLoader):
    default_item_class = LomRightsItem
    default_output_processor = TakeFirst()
class LomClassificationItemLoader(ItemLoader):
    default_item_class = LomClassificationItem
    default_output_processor = TakeFirst()