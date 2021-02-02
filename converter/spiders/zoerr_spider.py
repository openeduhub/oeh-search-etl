from .base_classes import LrmiBase
from scrapy.spiders import SitemapSpider


class ZoerrSpider(SitemapSpider, LrmiBase):
    name = "zoerr_spider"
    friendlyName = "OER-Repositorium Baden-Württemberg (ZOERR)"
    url = "https://www.oerbw.de"
    baseUrl = "https://www.oerbw.de/edu-sharing/eduservlet/oai/provider"
    set = "default"
    metadataPrefix = "lom"
    sitemap_urls = ["https://www.oerbw.de/edu-sharing/eduservlet/sitemap"]

    def __init__(self, **kwargs):
        SitemapSpider.__init__(self)
        LrmiBase.__init__(self, **kwargs)

    def parse(self, response):
        return LrmiBase.parse(self, response)
