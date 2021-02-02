from converter.items import *

from .base_classes import CSVBase, RSSListBase


# Spider to fetch RSS from planet schule
class OEHRSSSpider(RSSListBase):
    name = "oeh_rss_spider"
    friendlyName = "Open Edu Hub RSS"
    version = "0.1.0"

    def __init__(self, **kwargs):
        RSSListBase.__init__(self, "csv/oeh_rss.csv", **kwargs)

    def getBase(self, response):
        base = RSSListBase.getBase(self, response)
        base.replace_value(
            "origin", self.getCSVValue(response, CSVBase.COLUMN_SOURCE_TITLE)
        )
        return base

    def getLOMLifecycle(self, response=None) -> LomLifecycleItemloader:
        lifecycle = RSSListBase.getLOMLifecycle(self, response)
        lifecycle.add_value("role", "author")
        lifecycle.add_value(
            "organization", self.getCSVValue(response, CSVBase.COLUMN_SOURCE_TITLE)
        )
        lifecycle.add_value(
            "url", self.getCSVValue(response, CSVBase.COLUMN_SOURCE_URL)
        )
        return lifecycle
