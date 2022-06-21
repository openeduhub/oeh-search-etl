from scrapy.spiders import CrawlSpider
from .lom_base import LomBase


class RSSBase(CrawlSpider, LomBase):
    start_urls = []
    commonProperties = {}
    response = None

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def parse(self, response):
        response.selector.remove_namespaces()
        # common properties
        self.commonProperties["language"] = response.xpath(
            "//rss/channel/language//text()"
        ).get()
        self.commonProperties["source"] = response.xpath(
            "//rss/channel/generator//text()"
        ).get()
        self.commonProperties["publisher"] = response.xpath(
            "//rss/channel/author//text()"
        ).get()
        self.commonProperties["thumbnail"] = response.xpath(
            "//rss/channel/image/url//text()"
        ).get()
        self.response = response
        return self.startHandler(response)

    def startHandler(self, response):
        for item in response.xpath("//rss/channel/item"):
            responseCopy = response.replace(url=item.xpath("link//text()").get())
            responseCopy.meta["item"] = item
            yield LomBase.parse(self, responseCopy)

    def getId(self, response):
        return response.meta["item"].xpath("link//text()").get()

    def getHash(self, response):
        return self.version + str(response.meta["item"].xpath("pubDate//text()").get())

    def mapResponse(self, response):
        r = LomBase.mapResponse(self, response)
        return r

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        thumbnail = self.commonProperties["thumbnail"]
        if thumbnail:
            base.add_value("thumbnail", thumbnail)
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value(
            "identifier", response.meta["item"].xpath("guid//text()").get()
        )
        general.add_value(
            "title", response.meta["item"].xpath("title//text()").get().strip()
        )
        general.add_value("language", self.commonProperties["language"])
        description = response.meta["item"].xpath("description//text()").get()
        if not description:
            description = (
                response.meta["item"].xpath('//*[name()="summary"]//text()').get()
            )
        general.add_value("description", description)
        return general

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        # technical.add_value('format', item.xpath('enclosure/@type').get())
        # technical.add_value('size', item.xpath('enclosure/@length').get())
        # technical.add_value('location', item.xpath('enclosure/@url').get())
        technical.add_value("format", "text/html")
        if response.meta["item"].xpath("duration//text()").get() is not None:
            # not all RSS-Feeds hold a "duration"-field (e.g. text-based article-feeds don't)
            # therefore we need to make sure that duration is only set where it's appropriate
            technical.add_value("duration", response.meta["item"].xpath("duration//text()").get().strip())
        technical.add_value(
            "location", response.meta["item"].xpath("link//text()").get()
        )
        return technical

    def getLOMLifecycle(self, response):
        lifecycle = LomBase.getLOMLifecycle(self, response)
        lifecycle.add_value('role', 'publisher')
        lifecycle.add_value('organization', response.meta["item"].xpath("*[name()='itunes:author']/text()").get())
        lifecycle.add_value('date', response.meta["item"].xpath("pubDate//text()").get())
        return lifecycle