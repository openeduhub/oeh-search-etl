from overrides import overrides
from scrapy.http import Response

from converter import items
from converter.items import *
from .base_classes import LomBase
import html
import scrapy

class LearningAppsSpider(scrapy.Spider, LomBase):
    name = "learning_apps_spider"
    friendlyName = "LearningApps.org"
    url = "https://learningapps.org/"
    apiUrl = "https://learningapps.org/api.php"
    version = '0.1.2'

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

        yield self.startRequest(0, 0)
        for cat in self.categories:
            yield self.startRequest(cat, 0)
            for subcat in self.subcategories:
                yield self.startRequest(cat, subcat)

    def startRequest(self, cat, subcat,  offset=0):
        return scrapy.Request(url=self.apiUrl + '?getapps&lang=DE&category=' + str(cat) + '&subcategory='+ str(subcat) + '&offset=' + str(offset),
                             callback=self.parseList,
                             meta={'cat': cat, 'subcat': subcat, 'offset': offset}
                             )

    def parseList(self, response):
        for item in response.xpath('//results/app'):
            copyResponse = response.replace(url = item.xpath('@iframeurl').get().replace('//', 'https://'))
            copyResponse.meta['item'] = item
            yield self.parse(copyResponse)
        offset = response.meta['offset']
        offset += len(response.xpath('//results/app'))
        yield self.startRequest(response.meta['cat'], response.meta['subcat'], offset)

    async def parse(self, response):
        return await LomBase.parse(self, response)

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        try:
            valuespaces.add_value('discipline', list(map(lambda x: self.categories[x], response.meta["item"].xpath("@category").getall())))
        except:
            pass

        valuespaces.add_value('learningResourceType', 'Lernspiel')
        valuespaces.add_value('learningResourceType', 'Website')
        levels = int(response.meta["item"].xpath("@levels").get())
        if levels & 1:
            valuespaces.add_value('educationalContext', 'Primarstufe')
        if levels & 4:
            valuespaces.add_value('educationalContext', 'Sekundarstufe I')
        if levels & 8:
            valuespaces.add_value('educationalContext', 'Sekundarstufe II')

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
            html.unescape(response.meta["item"].xpath("@title").get()),
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
        # TODO: Maybe later in a vocabulary
        try:
            general.add_value('keyword', list(
                map(lambda x: self.subcategories[x], response.meta["item"].xpath("@subcategory").getall())))
        except:
            pass
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
