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
    print(value)
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

class LomBaseItem(Item):
    general = Field(serializer=LomGeneralItem)
    lifecycle = Field(serializer=LomLifecycleItem)
    technical = Field(serializer=LomTechnicalItem)

class BaseItem(Item):
    sourceId = Field()
    hash = Field()
    ranking = Field()
    license = Field()
    fulltext = Field()
    lom = Field(serializer=LomBaseItem)

class BaseItemLoader(ItemLoader):
    default_item_class = BaseItem
    #default_input_processor = MapCompose(replace_processor)
    default_output_processor = TakeFirst()

class LomBaseItemloader(ItemLoader):
    default_item_class = LomBaseItem
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