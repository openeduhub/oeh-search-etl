import csv
import os

import scrapy

from converter.valuespace_helper import ValuespaceHelper
from .csv_base import CSVBase
from .lom_base import LomBase
from .rss_base import RSSBase


# rss crawler with a list of entries to crawl and map
# for supported columns, please check the CSVbase class
class RSSListBase(RSSBase, LomBase):
    mappings = {}
    start_urls = []
    rows = {}

    def getCSVValue(self, response, fieldName):
        data = list(
            map(
                lambda x: x.strip(),
                response.meta["row"][self.mappings[fieldName]].split(";"),
            )
        )
        if len(list(filter(lambda x: x != "", data))) > 0:
            return data
        return None

    def __init__(self, file, delimiter=",", **kwargs):
        LomBase.__init__(self, **kwargs)
        dir = os.path.dirname(os.path.realpath(__file__))
        with open(dir + "/../../" + file, encoding="utf-8") as csvFile:
            csvReader = csv.reader(csvFile, delimiter=delimiter)
            i = 0
            for row in csvReader:
                if i == 0:
                    j = 0
                    for c in row:
                        self.mappings[c] = j
                        j += 1
                    i += 1
                    continue
                url = row[self.mappings[CSVBase.COLUMN_URL]]
                self.rows[url] = row
                # self.start_urls.append(url)
                i += 1

    def start_requests(self):
        requests = []
        for url in self.rows:
            requests.append(
                scrapy.Request(
                    url=url, callback=self.parse, meta={"row": self.rows[url]}
                )
            )
        return requests

    def getLOMGeneral(self, response):
        general = RSSBase.getLOMGeneral(self, response)
        general.replace_value(
            "language", self.getCSVValue(response, CSVBase.COLUMN_LANGUAGE)
        )
        general.replace_value(
            "keyword", self.getCSVValue(response, CSVBase.COLUMN_KEYWORD)
        )
        return general

    def getLicense(self, response):
        license = RSSBase.getLicense(self, response)
        license.add_value(
            "internal", self.getCSVValue(response, CSVBase.COLUMN_LICENSE)
        )
        return license

    def getValuespaces(self, response):
        valuespaces = RSSBase.getValuespaces(self, response)
        tar_from = self.getCSVValue(response, CSVBase.COLUMN_TYPICAL_AGE_RANGE_FROM)
        tar_to = self.getCSVValue(response, CSVBase.COLUMN_TYPICAL_AGE_RANGE_TO)
        if tar_from and tar_to:
            valuespaces.add_value(
                "educationalContext",
                ValuespaceHelper.educationalContextByAgeRange([tar_from[0], tar_to[0]]),
            )
        valuespaces.add_value(
            "discipline", self.getCSVValue(response, CSVBase.COLUMN_DISCIPLINE)
        )
        valuespaces.add_value(
            "learningResourceType",
            self.getCSVValue(response, CSVBase.COLUMN_LEARNING_RESOURCE_TYPE),
        )
        return valuespaces
