import logging

from scrapy.spiders import CrawlSpider

from .lom_base import LomBase
from ...constants import Constants
from ...items import LicenseItemLoader, ValuespaceItemLoader


class RSSBase(CrawlSpider, LomBase):
    start_urls = []
    commonProperties = {}
    response = None

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def parse(self, response):
        # common properties
        self.commonProperties["language"] = response.xpath("//rss/channel/language//text()").get()
        self.commonProperties["source"] = response.xpath("//rss/channel/generator//text()").get()
        self.commonProperties["publisher"] = response.xpath("//rss/channel/author//text()").get()
        self.commonProperties["thumbnail"] = response.xpath("//rss/channel/image/url//text()").get()
        self.response = response
        return self.startHandler(response)

    async def startHandler(self, response):
        for item in response.xpath("//rss/channel/item"):
            responseCopy = response.replace(url=item.xpath("link//text()").get())
            responseCopy.meta["item"] = item
            yield await LomBase.parse(self, responseCopy)

    def getId(self, response):
        return response.meta["item"].xpath("link//text()").get()

    def getHash(self, response):
        return self.version + str(response.meta["item"].xpath("pubDate//text()").get())

    async def mapResponse(self, response):
        r = await LomBase.mapResponse(self, response)
        return r

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        thumbnail_channel = self.commonProperties["thumbnail"]
        thumbnail_channel_itunes = response.meta["item"].xpath('//*[name()="itunes:image"]/@href').get()
        thumbnail_item_itunes = response.meta["item"].xpath('*[name()="itunes:image"]/@href').get()
        # according to Apple's RSS guidelines the <itunes:image href="...">-element should be used for a
        # channel-thumbnail, but experience shows that some RSS Feeds also include this element within individual items.
        if thumbnail_item_itunes:
            # if the thumbnail URL for an individual episode is available, it will be the primary choice
            base.add_value("thumbnail", thumbnail_item_itunes)
        elif thumbnail_channel:
            # otherwise the channel-thumbnail found within <image> will be used as a fallback URL
            base.add_value("thumbnail", thumbnail_channel)
        elif thumbnail_channel_itunes:
            # if the <image> tag doesn't exist, we're using <itunes:image href="..."> as a final fallback
            base.add_value("thumbnail", thumbnail_channel_itunes)
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        guid = response.meta["item"].xpath("guid//text()").get()  # optional <guid>-Element can (optionally) have an
        # "isPermaLink"-attribute, see: https://www.rssboard.org/rss-specification#ltguidgtSubelementOfLtitemgt
        if guid:
            # by default, all guids are treated as (local) identifiers
            general.add_value("identifier", guid)
        general.add_value("title", response.meta["item"].xpath("title//text()").get().strip())
        general.add_value("language", self.commonProperties["language"])
        description: str = response.meta["item"].xpath("description//text()").get()
        summary: str = response.meta["item"].xpath('*[name()="summary"]//text()').get()
        itunes_summary: str = response.meta["item"].xpath('*[name()="itunes:summary"]//text()').get()
        # in case that a RSS feed doesn't adhere to the RSS 2.0 spec (<description>), we're using two fallbacks:
        # <summary> or if that doesn't exist: <itunes:summary>
        if description:
            general.add_value("description", description)
        elif summary:
            general.add_value("description", summary)
        elif itunes_summary:
            general.add_value("description", itunes_summary)
        rss_category_channel: list = response.xpath("//rss/channel/category/text()").getall()
        rss_category_item: list = response.meta["item"].xpath("category/text()").getall()
        # see: https://www.rssboard.org/rss-profile#element-channel-item-category
        itunes_category: list = response.xpath('//*[name()="itunes:category"]/@text').getall()
        keyword_set = set()
        if rss_category_channel:
            keyword_set.update(rss_category_channel)
        if rss_category_item:
            keyword_set.update(rss_category_item)
        if itunes_category:
            keyword_set.update(itunes_category)
        if keyword_set:
            keyword_list: list = list(keyword_set)
            if keyword_list:
                keyword_list.sort()
                general.add_value("keyword", keyword_list)
        return general

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", "text/html")
        # the <enclosure>-element should always have 3 attributes: 'size', 'type' and 'url'
        # see https://www.rssboard.org/rss-specification#ltenclosuregtSubelementOfLtitemgt
        # enclosure_size = response.meta["item"].xpath("enclosure/@type").get()  # size in bytes
        # enclosure_type = response.meta["item"].xpath("enclosure/@type").get()  # MIME-type
        enclosure_url = response.meta["item"].xpath("enclosure/@url").get()  # URL (of the .mp3 / .mp4)
        # if enclosure_type:
        #     # ToDo: setting format and size breaks edu-sharing's file preview and thumbnail generation
        #     technical.replace_value("format", enclosure_type)
        # if enclosure_size:
        #     technical.replace_value("size", enclosure_size)
        rss_duration: str = response.meta["item"].xpath("duration//text()").get()
        itunes_duration: str = response.meta["item"].xpath("*[name()='itunes:duration']/text()").get()
        # <itunes:duration> is valid in 3 different variations:
        # hours:minutes:seconds // minutes:seconds // total_seconds
        if rss_duration:
            # not all RSS-Feeds hold a "duration"-field (e.g. text-based news-feeds typically do not)
            # therefore we need to make sure that duration is only set where it's appropriate
            technical.add_value("duration", rss_duration.strip())
        elif itunes_duration:
            # fallback: if there's no <duration>-element, there might be an optional <itunes:duration>-tag
            technical.add_value("duration", itunes_duration.strip())
        link_url = response.meta["item"].xpath("link//text()").get()
        if link_url:
            technical.add_value("location", link_url)
        guid: str = response.meta["item"].xpath("guid//text()").get()
        guid_is_permalink: str = response.meta["item"].xpath("guid/@isPermaLink").get()
        if guid:
            # if <guid>'s "isPermaLink"-attribute is true or missing, the guid points to a URL
            if guid_is_permalink:
                if guid_is_permalink.strip() == "false" and guid:
                    logging.debug(f"The <guid> {guid} is not an URL. Will not save it to 'technical.location'")
            elif guid:
                if guid != response.url:
                    # making sure to save the provided URI (in addition to the resolved URL)
                    technical.add_value("location", guid)
        elif enclosure_url:
            # According to Apple RSS Guidelines, the enclosure URL-attribute is considered a fallback for a missing
            # <guid> element
            technical.add_value("location", enclosure_url)
        return technical

    def getLOMLifecycle(self, response):
        lifecycle = LomBase.getLOMLifecycle(self, response)
        lifecycle.add_value("role", "publisher")
        channel_author: str = response.xpath("//rss/channel/*[name()='itunes:author']/text()").get()
        # if <itunes:author> appears in /rss/channel, it will carry publisher/organizational information
        if "publisher" in self.commonProperties:
            lifecycle.add_value("organization", self.commonProperties["publisher"])
        elif channel_author:
            lifecycle.add_value("organization", channel_author)
        # ToDo: optional <dc:creator>-element in <item>, as soon as we actually encounter a RSS feed to test it against
        #   see: https://www.rssboard.org/rss-profile#namespace-elements-dublin-creator
        pub_date = response.meta["item"].xpath("pubDate//text()").get()  # <pubDate> according to the RSS 2.0 specs
        # see: https://www.rssboard.org/rss-specification#ltpubdategtSubelementOfLtitemgt
        pub_date_variation2 = response.meta["item"].xpath("PubDate//text()").get()
        # according to Apple RSS Guidelines, Newsfeeds might use <PubDate>
        # see: https://support.apple.com/guide/news-publisher/rss-guidelines-for-apple-news-apdc2c7520ff/icloud
        pub_date_variation3 = response.meta["item"].xpath("published//text()").get()
        # according to Apple's RSS Guidelines, some (Atom-inspired) feeds might use <published> instead
        if pub_date:
            # <pubDate> is an OPTIONAL sub-element of <item>
            lifecycle.add_value("date", pub_date)
        elif pub_date_variation2:
            # if <pubDate> isn't available, <PubDate> might be
            lifecycle.add_value("date", pub_date_variation2)
        elif pub_date_variation3:
            # if the RSS feed differs from the RSS 2.0 specs, <published> might be available
            lifecycle.add_value("date", pub_date_variation3)
        return lifecycle

    def getLicense(self, response=None) -> LicenseItemLoader:
        license_item_loader = LomBase.getLicense(self, response)
        copyright_description: str = response.xpath("//rss/channel/copyright/text()").get()
        if copyright_description:
            license_item_loader.add_value("internal", Constants.LICENSE_CUSTOM)
            # 'internal' needs to be set to CUSTOM for 'description' to be read
            license_item_loader.add_value("description", copyright_description)
        item_author: str = response.meta["item"].xpath("*[name()='itunes:author']/text()").get()
        if item_author:
            # if the optional field <itunes:author> is nested in /rss/channel/item, it will contain author information
            license_item_loader.add_value("author", item_author)
        return license_item_loader

    def getValuespaces(self, response):
        vs_loader = LomBase.getValuespaces(self, response)
        # as per team4 request on 2023-08-11 the values for 'conditionsOfAccess' and 'price' are hard-coded:
        vs_loader.add_value("conditionsOfAccess", "no login")
        vs_loader.add_value("price", "no")
        return vs_loader
