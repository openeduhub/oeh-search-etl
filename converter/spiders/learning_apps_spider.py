from overrides import overrides
from scrapy.http import Response

from converter import items
from converter.items import *
import time
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase
from converter.valuespace_helper import Valuespaces
import requests
from html.parser import HTMLParser
from converter.constants import Constants


class LearningAppsSpider(scrapy.Spider, LomBase):
    name = "learning_apps_spider"
    friendlyName = "LearningApps.org"
    url = "https://learningapps.org/"
    apiUrl = "https://learningapps.org/api.php"
    version = '0.1.0'

    categories = {}
    subcategories = {}
    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self):
        yield scrapy.Request(url = self.apiUrl + '?getcategories&lang=DE',
                              callback = self.fetchCategories)

    def fetchCategories(self,response):
        for cat in response.xpath('//results/category'):
            self.categories[cat.xpath('@id').get()] = cat.xpath('@name').get()
            for subcat in cat.xpath('subcategory'):
                self.subcategories[subcat.xpath('@id').get()] = subcat.xpath('@title').get()
        yield self.startRequest()

    def startRequest(self, offset=0):
        return scrapy.Request(url=self.apiUrl + '?search=&lang=DE&offset=' + str(offset),
                             callback=self.parseList,
                             meta={'offset': offset}
                             )

    def parseList(self, response):
        for item in response.xpath('//results/app'):
            copyResponse = response.replace(url = item.xpath('@iframeurl').get().replace('//', 'https://'))
            copyResponse.meta["item"] = item
            yield self.parse(copyResponse)
        offset = response.meta['offset']
        offset += len(response.xpath('//results/app'))
        yield self.startRequest(offset)

    def parse(self, response):
        return LomBase.parse(self, response)

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.add_value('discipline', list(map(lambda x: self.categories[x], response.meta["item"].xpath("@category").getall())))
        # TODO: Maybe more useful as a generic keyword?
        try:
            valuespaces.add_value('discipline', list(map(lambda x: self.subcategories[x], response.meta["item"].xpath("@subcategory").getall())))
        except:
            pass
        valuespaces.add_value('learningResourceType', 'Website')
        return valuespaces

    def getId(self, response):
        return response.meta["item"].xpath("@id").get()

    def getHash(self, response):
        return response.meta["item"].xpath("@changed").get() + self.version

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        base.replace_value("thumbnail", response.meta["item"].xpath("@image").get())
        return base

    @overrides
    def getLOMLifecycle(self, response: Response) -> items.LomLifecycleItemloader:
        lifecycle = LomBase.getLOMLifecycle(self, response)
        name = response.meta["item"].xpath("@author").get().split(' ')
        lifecycle.add_value("role", "author")
        if len(name) == 2:
            lifecycle.add_value("firstName", name[0])
            lifecycle.add_value("lastName", name[1])
        else:
            lifecycle.add_value("organization", " ".join(name))
        return lifecycle

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value(
            "title",
            HTMLParser().unescape(response.meta["item"].xpath("@title").get()),
        )
        general.add_value(
            "description", self.html2Text(response.meta["item"].xpath("@task").get())
        )
        general.add_value(
            "language", response.meta["item"].xpath("@language").get()
        )
        general.add_value(
            "keyword",response.meta["item"].xpath("@tags").get()
        )
        return general

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", "text/html")
        technical.add_value(
            "location", self.url + self.getId(response)
        )
        return technical

    def getLicense(self, response):
        license = LomBase.getLicense(self, response)

        return license
