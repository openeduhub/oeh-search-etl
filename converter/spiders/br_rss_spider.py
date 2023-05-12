from .base_classes import RSSListBase


# Spider to fetch RSS from planet schule
class BRRSSSpider(RSSListBase):
    name = "br_rss_spider"
    friendlyName = "Bayerischer Rundfunk"
    url = "https://www.br.de/"
    version = "0.1.1"

    def __init__(self, **kwargs):
        RSSListBase.__init__(self, "../csv/br_rss.csv", **kwargs)
