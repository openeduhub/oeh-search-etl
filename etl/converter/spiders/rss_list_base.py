from scrapy.spiders import CrawlSpider
from converter.items import *
import time
import logging
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase;
from converter.spiders.rss_base import RSSBase;
from converter.valuespace_helper import ValuespaceHelper;
import csv
import os
# rss crawler with a list of entries to crawl and map
class RSSListBase(RSSBase, LomBase):
    # column names supported:
    COLUMN_URL = 'url'
    COLUMN_TYPICAL_AGE_RANGE_FROM = 'typicalAgeRangeFrom'
    COLUMN_TYPICAL_AGE_RANGE_TO = 'typicalAgeRangeTo'
    COLUMN_TYPICAL_DISCIPLINE = 'discipline'
    COLUMN_LEARNING_RESOURCE_TYPE = 'learningResourceType'
    COLUMN_LANGUAGE = 'language'
    COLUMN_LICENSE = 'license'
    mappings = {}
    start_urls = []
    rows = {}
    def getCSVValue(self, response, fieldName):
        return list(map(lambda x: x.strip(),response.meta['row'][self.mappings[fieldName]].split(";")))
    def __init__(self, file, delimiter = ','):
        dir = os.path.dirname(os.path.realpath(__file__))
        with open(dir + '/../' + file) as csvFile:
            csvReader = csv.reader(csvFile, delimiter=delimiter)
            i = 0
            for row in csvReader:
                if i==0:
                    j = 0
                    for c in row:
                        self.mappings[c] = j
                        j += 1
                    i += 1
                    continue
                url = row[self.mappings[RSSListBase.COLUMN_URL]]
                self.rows[url] = row
                #self.start_urls.append(url)
                i += 1
    def start_requests(self):
        requests = []
        for url in self.rows:
            requests.append(scrapy.Request(url=url, callback=self.parse, meta = {'row': self.rows[url]}))
        return requests

    def getLOMGeneral(self, response):
        general = RSSBase.getLOMGeneral(self, response)
        general.replace_value('language', self.getCSVValue(response, RSSListBase.COLUMN_LANGUAGE))
        return general
  
    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        license.add_value('internal', self.getCSVValue(response, RSSListBase.COLUMN_LICENSE))
        return license

    def getValuespaces(self, response):
        valuespaces = RSSBase.getValuespaces(self, response)
        valuespaces.add_value('educationalContext', ValuespaceHelper.educationalContextByAgeRange([
            self.getCSVValue(response, RSSListBase.COLUMN_TYPICAL_AGE_RANGE_FROM)[0], 
            self.getCSVValue(response, RSSListBase.COLUMN_TYPICAL_AGE_RANGE_TO)[0]
            ]))
        
        valuespaces.add_value('discipline', self.getCSVValue(response, RSSListBase.COLUMN_TYPICAL_DISCIPLINE))
        valuespaces.add_value('learningResourceType', self.getCSVValue(response, RSSListBase.COLUMN_LEARNING_RESOURCE_TYPE))
        return valuespaces
