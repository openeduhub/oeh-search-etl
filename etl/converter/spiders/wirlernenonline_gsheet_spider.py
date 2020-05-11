from converter.spiders.lom_base import LomBase
from converter.spiders.oai_base import OAIBase
from converter.spiders.csv_base import CSVBase
from converter.constants import *
import csv
from scrapy.spiders import Spider
import logging
from io import StringIO
from scrapy import *
import csv

class WirLernenOnlineGSheetSpider(Spider, CSVBase, LomBase):
  name = 'wirlernenonline_gsheet_spider'
  friendlyName='WirLernenOnline'
  url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTmqeYqGD0TADaSkON3zgK66BGTOcPGtsrE280j0wZ8WKtuGL8LZtnKFRIH6HU1FEYIAP28mOWsJYiN/pub?gid=0&single=true&output=csv'
  sourceType = Constants.SOURCE_TYPE_SPIDER
  def __init__(self, **kwargs):
    LomBase.__init__(self, **kwargs)
    
  def start_requests(self):
      yield Request(url=self.url, callback=self.parse)

  def getCSVValue(self, response, fieldName):
    return list(map(lambda x: x.strip(),response.meta['row'][self.mappings[fieldName]].split(";")))

  def parse(self, response):
    rows = self.readCSV(csv.reader(StringIO(response.body.decode('UTF-8')), delimiter=','), 2)
    for row in rows:
      copyResponse = response.replace(url = row['url']['text'])
      copyResponse.meta['row'] = row
      if self.getId(copyResponse):
        yield LomBase.parse(self, copyResponse)
