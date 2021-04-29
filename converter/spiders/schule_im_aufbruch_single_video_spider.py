import html
import json
import logging

import scrapy

from converter.items import BaseItemLoader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, PermissionItemLoader, ResponseItemLoader, \
    LomLifecycleItemloader
from converter.spiders.base_classes import LomBase


class SchuleImAufbruchVideoSpider(scrapy.Spider, LomBase):
    name = "sia_single"
    friendlyName = "Schule im Aufbruch (Single Run Spider)"
    url = "https://vimeo.com/412230600"
    version = "0.1.1"

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def getId(self, response: scrapy.http.Response = None) -> str:
        # currently returns the video-title as ID
        return response.xpath('//title//text()').get()

    def getHash(self, response: scrapy.http.Response = None) -> str:
        pass

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response: scrapy.http.Response, **kwargs):
        """
        parses a video-page (e.g. https://vimeo.com/videoID whereby videoID is a number) for metadata
        (condition: only if there is a "json+ld"-script found within the video-page).

        """
        # XPath to description of a video looks like this:
        # //*[@id="main"]/div/main/div/div/div/div[2]/div[3]/div

        edu = LomEducationalItemLoader()

        permissions = PermissionItemLoader(response=response)
        response_loader = ResponseItemLoader()

        # if ld+json script-container doesn't exist, at least log the error
        if (response.xpath('/html/body/script[1]/text()').get().strip()) is not None:
            # using ld+json to fetch metadata:
            # ld_json = self.get_ld_json(response)

            current_url = str(response.url)  # making double-sure that we're using a string for sourceID

            # TODO: there's additional metadata inside a script block: window.vimeo.clip_page_config
            #   - longer description - maybe use this one?
            #   - duration (both in seconds and formatted)
            #   - ads
            #       - house_ads_enabled
            #       - third_party_ads_enabled
            # response.xpath('//*[@id="wrap"]/div[2]/script[1]/text()').get()
            # might have to access it and split it up with regEx

            # TODO: PermissionItemLoader ?
            # permissions.add_value('public', self.settings.get("DEFAULT_PUBLIC_STATE"))  # is this necessary?
            # base.add_value('permissions', permissions.load_item())
            # # TODO: ResponseItemLoader() ?
            # response_loader.add_value('url', response.url)
            # base.add_value('response', response_loader.load_item())

            return LomBase.parse(self, response)
        else:
            logging.debug("Could not find ld+json script, skipping entry: " + response.url)

    @staticmethod
    def get_ld_json(response: scrapy.http.Response) -> list:
        """
        acquires the ld+json script block from the current page and deserializes it into a json list

        """
        ld_json_string = response.xpath('/html/body/script[1]/text()').get().strip()
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
        base = LomBase.getBase(self, response)
        ld_json = self.get_ld_json(response)
        current_url = str(response.url)  # making double-sure that we're using a string for sourceID
        base.add_value('sourceId', current_url)
        base.add_value("hash", ld_json[0]["dateModified"])
        # TODO: datetime-conversion necessary?
        base.add_value("lastModified", ld_json[0]["dateModified"])
        base.add_value('thumbnail', ld_json[0]["thumbnailUrl"])
        return base

    def getLOMGeneral(self, response=None) -> LomGeneralItemloader:
        general = LomBase.getLOMGeneral(self, response)
        ld_json = self.get_ld_json(response)
        general.add_value('title', html.unescape(ld_json[0]["name"]))
        general.add_value('description', html.unescape(ld_json[0]["description"]))
        # TODO: general.add_value('keyword', '') set manually if there are no keywords given?
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
        return technical

    def getValuespaces(self, response) -> ValuespaceItemLoader:
        vs = LomBase.getValuespaces(self, response)
        # TODO: ValueSpaceItemLoader() missing keys? which ones are to be manually set?
        #   - dataProtectionConformity
        #   - fskRating
        #   - oer
        #   - educationalContext
        #   - educationalContentType
        #   - learningResourceType (other_asset_type)?
        vs.add_value('conditionsOfAccess', 'no_login')
        # vs.add_value('containsAdvertisement', 'no')  # do vimeo-advertisements for their own vimeo-plans count?
        vs.add_value('price', 'no')
        vs.add_value('intendedEndUserRole', 'teacher')
        vs.add_value('discipline', '720')  # is this the correct category? (allgemein)
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
