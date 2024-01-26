import html
import json
import logging

import scrapy

from converter.items import BaseItemLoader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, PermissionItemLoader, LomLifecycleItemloader
from converter.spiders.base_classes import LomBase


class SchuleImAufbruchSpider(scrapy.Spider, LomBase):
    name = "schule_im_aufbruch_spider"
    friendlyName = "Schule im Aufbruch"
    url = "https://vimeo.com/user12637410/videos"
    version = "0.1.3"   # last update: 2021-09-30

    # this list will be filled with urls to crawl through, (currently it's only used for debugging purposes)
    video_urls_to_crawl = list()

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def getId(self, response: scrapy.http.Response = None) -> str:
        # currently returns the video-title as ID
        return response.xpath('//title//text()').get()

    def getHash(self, response: scrapy.http.Response = None) -> str:
        pass

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        uses variable "url" (format: https://vimeo.com/userID/videos) as the starting point to crawl the overview-page
        for links to video-sub-pages and grabs the next overview-page afterwards

        (by default vimeo shows only 12 video-thumbnails per overview-page)

        Scrapy Contracts:
        @url https://vimeo.com/user12637410/videos
        @returns requests 12
        """

        yield from self.get_video_urls_from_overview(response)
        logging.debug("urls_to_crawl is currently the size of " + str(len(self.video_urls_to_crawl)))

        # by default vimeo shows only 12 videos per overview-page,
        # we need to iterate through all pages on the vimeo-channel:
        yield from self.get_next_vimeo_overview_page(response)

    def get_video_urls_from_overview(self, response):
        """
        looks for the ld+json script block on the current overview page and grab the URLs.
        Afterwards tells the video parser to go through the video-sub-pages and yield the metadata

        Scrapy Contracts:
        @url https://vimeo.com/user12637410/videos
        @returns requests 12
        """

        # there's an alternative way to acquire thumbnails from the overview as well:
        # thumbnails can be acquired using the 'srcset' attribute on each thumbnail, e.g.:
        # response.xpath('//*[@id="clip_412230600"]/a/img/@srcset').get()

        # acquire current URLs from <script type="application/ld+json"> block
        current_page_json = self.get_ld_json(response)

        # the urls we need are inside a nested dictionary
        current_page_nested = json.dumps(current_page_json[1]["itemListElement"])
        # we need to be able to access the data as JSON elements to get their values more comfortably:
        current_page_video_dictionary = json.loads(current_page_nested)

        for items in current_page_video_dictionary:
            video_full_url = response.urljoin(items["url"])

            # TODO: technically we don't need the video_urls_to_crawl list anymore
            self.video_urls_to_crawl.append(video_full_url)
            # following each video_url to the dedicated video-subpage to grab metadata
            yield response.follow(url=video_full_url, callback=self.parse_video_page)

    async def parse_video_page(self, response: scrapy.http.Response = None):
        """
        parses a video-page (e.g. https://vimeo.com/videoID whereby videoID is a number) for metadata
        (condition: only if there is a "json+ld"-script found within the video-page).

        """
        # XPath to description of a video looks like this:
        # //*[@id="main"]/div/main/div/div/div/div[2]/div[3]/div

        # if ld+json script-container doesn't exist, at least log the error
        if (response.xpath('//script[@type="application/ld+json"]').get().strip()) is not None:

            # TODO: there's additional metadata inside a script block: window.vimeo.clip_page_config
            #   - longer description - maybe use this one?
            #   - duration (both in seconds and formatted)
            #   - ads
            #       - house_ads_enabled
            #       - third_party_ads_enabled
            # response.xpath('//*[@id="wrap"]/div[2]/script[1]/text()').get()
            # might have to access it and split it up with regEx

            return await LomBase.parse(self, response)
        else:
            logging.debug("Could not find ld+json script, skipping entry: " + response.url)

    @staticmethod
    def get_ld_json(response: scrapy.http.Response) -> list:
        """
        acquires the ld+json script block from the current page and deserializes it into a json list

        """
        ld_json_string = response.xpath('//script[@type="application/ld+json"]/text()').get().strip()
        ld_json = json.loads(ld_json_string)
        return ld_json

    @staticmethod
    def get_license(response: scrapy.http.Response = None) -> str:
        """
        grabs the license information from the "about"-button (pop-in)

        :return: url of license as String
        """
        # check first if the license information is present:
        if (response.xpath('/html/head/link[9]/@rel').get()) == "license":
            license_url = response.xpath('/html/head/link[9]/@href').get()
            return license_url
        else:
            return "license information not found"

    def getBase(self, response=None) -> BaseItemLoader:
        base: BaseItemLoader = LomBase.getBase(self, response)
        ld_json = self.get_ld_json(response)
        current_url = str(response.url)  # making double-sure that we're using a string for sourceID
        base.add_value('sourceId', current_url)
        # maybe add sourceID + dateModified as hash?
        hash_temp: str = str(ld_json[0]["dateModified"] + self.version)
        base.add_value("hash", hash_temp)
        base.add_value("lastModified", ld_json[0]["dateModified"])
        base.add_value('thumbnail', ld_json[0]["thumbnailUrl"])
        return base

    def getLOMGeneral(self, response=None) -> LomGeneralItemloader:
        general = LomBase.getLOMGeneral(self, response)
        ld_json = self.get_ld_json(response)
        general.add_value('title', html.unescape(ld_json[0]["name"]))
        general.add_value('description', html.unescape(ld_json[0]["description"]))
        # TODO: set manually if there are no keywords given?
        #  general.add_value('keyword', '')     # manual keywords?
        return general

    def getLOMTechnical(self, response=None) -> LomTechnicalItemLoader:
        # TODO: LomTechnicalItemLoader()
        technical = LomBase.getLOMTechnical(self, response)
        ld_json = self.get_ld_json(response)

        # TODO: Make sure that we're grabbing the right type for 'format'
        # if we were to acquire the format by an API call
        # (see https://developer.vimeo.com/api/reference/responses/video), vimeo would offer 3 options:
        # 'live' (for live events),
        # 'stock' (this video is a Vimeo Stock video)
        # 'video' (this video is a standard Vimeo video)

        # grabs the video type from the metadata header - most of the times it'll be video.other
        technical.add_value('format', response.xpath('/html/head/meta[18]/@content').get())
        technical.add_value('location', ld_json[0]["url"])
        technical.add_value('duration', ld_json[0]["duration"])
        return technical

    def getValuespaces(self, response) -> ValuespaceItemLoader:
        vs = LomBase.getValuespaces(self, response)
        # TODO: ValueSpaceItemLoader() missing keys? which ones are to be manually set?
        #   - dataProtectionConformity
        #   - fskRating
        #   - oer
        #   - educationalContext
        #   - educationalContentType
        vs.add_value('conditionsOfAccess', 'no_login')
        vs.add_value('containsAdvertisement', 'yes')  # set to yes because of vimeos own advertisements
        vs.add_value('price', 'no')
        vs.add_value('intendedEndUserRole', 'teacher')
        vs.add_value('learningResourceType', 'video')
        return vs

    def getLOMLifecycle(self, response=None) -> LomLifecycleItemloader:
        lifecycle = LomBase.getLOMLifecycle(self, response)
        ld_json = self.get_ld_json(response)
        # author information is inside a dictionary with schema.org type Person
        # we could maybe grab the whole object instead?
        author_dict = ld_json[1]["itemListElement"][0]["item"]
        # TODO: LomLifeCycleItemLoader
        lifecycle.add_value('organization', author_dict["name"])
        lifecycle.add_value('url', author_dict["@id"])
        return lifecycle

    def getLOMEducational(self, response=None) -> LomEducationalItemLoader:
        edu = LomBase.getLOMEducational(self, response)
        # TODO: which category does "schule im Aufbruch" fit into? double-check!
        edu.add_value('language', 'de')  # okay to hardcode this? (some videos are bilingual, but meta
        # data from vimeo doesn't offer language attributes)
        return edu

    def getLicense(self, response=None) -> LicenseItemLoader:
        lic = LomBase.getLicense(self, response)
        license_url = self.get_license(response)
        lic.add_value('url', license_url)
        return lic

    def getPermissions(self, response=None) -> PermissionItemLoader:
        permissions = LomBase.getPermissions(self, response)
        # TODO: PermissionItemLoader - which value should be set?
        permissions.add_value('public', self.settings.get("DEFAULT_PUBLIC_STATE"))  # is this necessary?
        return permissions

    def get_next_vimeo_overview_page(self, response: scrapy.http.Response):
        """
        if there is a "next"-button at the bottom of the vimeo-user's overview page:
        grabs the url from it and yields it
        """
        # next_vimeo_overview_page = response.xpath('//*[@id="pagination"]/ol/li[9]').get()
        next_vimeo_overview_page = response.css('#pagination > ol > li.pagination_next a::attr(href)').get()
        if next_vimeo_overview_page is not None:
            yield response.follow(next_vimeo_overview_page, self.parse)
