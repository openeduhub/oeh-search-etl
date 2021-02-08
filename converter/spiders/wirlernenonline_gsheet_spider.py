from .base_classes import LomBase, CSVBase

from converter.constants import *
from io import StringIO
from scrapy import *
import csv


class WirLernenOnlineGSheetSpider(Spider, CSVBase, LomBase):
    ranking = 5
    name = "wirlernenonline_gsheet_spider"
    friendlyName = "Themenportal"
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTmqeYqGD0TADaSkON3zgK66BGTOcPGtsrE280j0wZ8WKtuGL8LZtnKFRIH6HU1FEYIAP28mOWsJYiN/pub?gid=0&single=true&output=csv"
    sourceType = Constants.SOURCE_TYPE_SPIDER

    COLUMN_UUID = "uuid"

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def getBase(self, response=None):
        base = CSVBase.getBase(self, response)
        uuid = response.meta["row"][WirLernenOnlineGSheetSpider.COLUMN_UUID]["text"]
        if uuid:
            base.add_value("uuid", uuid)
        return base

    def start_requests(self):
        yield Request(url=self.url, callback=self.parse)

    def parse(self, response):
        rows = self.readCSV(
            csv.reader(StringIO(response.body.decode("UTF-8")), delimiter=","), 2
        )
        for row in rows:
            copyResponse = response.copy()
            copyResponse.meta["row"] = row
            if self.getId(copyResponse):
                yield LomBase.parse(self, copyResponse)
