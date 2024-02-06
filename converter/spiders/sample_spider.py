from scrapy.spiders import CrawlSpider
import time
from .base_classes import LomBase


# Sample Spider, using a SitemapSpider to crawl your web page
# Can be used as a template for your custom spider
class SampleSpider(CrawlSpider, LomBase):
    name = "sample_spider"
    url = "https://edu-sharing.com"  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = "Sample Source"  # name as shown in the search ui
    start_urls = ["https://edu-sharing.com"]
    version = "0.1"  # the version of your crawler, used to identify if a reimport is necessary

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    async def parse(self, response):
        return await LomBase.parse(self, response)

    # return a (stable) id of the source
    def getId(self, response):
        return response.xpath("//title//text()").get()

    # return a stable hash to detect content changes
    # if there is no hash available, may use the current time as "always changing" info
    # Please include your crawler version as well
    def getHash(self, response):
        return self.version + time.time()

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        # optionally provide thumbnail. If empty, it will tried to be generated from the getLOMTechnical 'location' (if format is 'text/html')
        # base.add_value('thumbnail', 'https://url/to/thumbnail')
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("title", response.xpath("//title//text()").get())
        general.add_value(
            "language", response.xpath('//meta[@property="og:locale"]/@content').get()
        )
        return general

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("location", response.url)
        technical.add_value("format", "text/html")
        technical.add_value("size", len(response.body))
        return technical

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        # Provide valuespace data. This data will later get automatically mapped
        # Please take a look at the valuespaces here:
        # https://vocabs.openeduhub.de/
        # You can either use full identifiers or also labels. The system will auto-map them accordingly

        # Please also checkout the ValuespaceHelper class which provides usefull mappers for common data

        # valuespaces.add_value('educationalContext', context)
        # valuespaces.add_value('discipline',discipline)
        # valuespaces.add_value('learningResourceType', lrt)
        return valuespaces

    # You may override more functions here, please checkout LomBase class
