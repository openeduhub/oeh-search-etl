from .base_classes import RSSListBase


# Spider to fetch RSS from planet schule
class ZDFRSSSpider(RSSListBase):
    name = "zdf_rss_spider"
    friendlyName = "ZDF"
    url = "https://www.zdf.de/"
    version = "0.1.0"

    def __init__(self, **kwargs):
        RSSListBase.__init__(self, "csv/zdf_rss.csv", **kwargs)
