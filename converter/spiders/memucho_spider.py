import logging

import scrapy
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from .base_classes import LomBase, JSONBase


class MemuchoSpider(CrawlSpider, LomBase, JSONBase):
    name = "memucho_spider"
    friendlyName = "memucho"
    url = "https://memucho.de"
    start_urls = ["https://memucho.de/api/edusharing/search?pageSize=999999"]
    version = "0.1.1"  # last update: 2022-02-28

    # The crawler uses the memucho API with the following item structure (example):
    # {
    #       "TopicId": 199,
    #       "Name": "UNESCO-Weltkulturerbe",
    #       "ImageUrl": "https://memucho.de/Images/Categories/199_350s.jpg?t=20161105081125",
    #       "ItemUrl": "https://memucho.de/UNESCO-Weltkulturerbe/199",
    #       "Licence": "CC_BY",
    #       "Author": "Christof",
    #       "DateModified": 1643303499
    #     }
    # Since there are lots of deadlinks (Error 404, 500) in the API, the dupefilter will show a lot of dropped items

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self):
        """

        :return:
        """
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_sitemap)
        pass

    async def mapResponse(self, response):
        return await LomBase.mapResponse(self, response)

    def getId(self, response):
        return response.meta["item"].get("TopicId")

    def getHash(self, response):
        date_modified = response.meta["item"].get("DateModified")
        hash_temp: str = str(date_modified) + self.version
        # return time.time()
        return hash_temp

    def parse_sitemap(self, response):
        json_items = response.json()

        for item in json_items.get("Items"):
            copy_response = response.copy()
            copy_response.meta["item"] = item
            if self.hasChanged(copy_response):
                yield scrapy.Request(
                    url=item.get("ItemUrl"),
                    callback=self.parse,
                    meta={"item": item},
                )

    async def parse(self, response):
        return await LomBase.parse(self, response)

    # thumbnail is always the same, do not use the one from rss
    def getBase(self, response):

        if response.url == "https://memucho.de/Fehler/404" or response.url == "https://memucho.de/Fehler/500":
            # the API lists dozens of (personal) Wikis that are no longer maintained and forward to deadlinks,
            # most of them get filtered by Scrapy's dupefilter, but some might slip through - so we drop those as well
            raise DropItem(f"Deadlink found for entry {response.url}")

        base = LomBase.getBase(self, response)
        thumbnail_url = response.meta["item"].get("ImageUrl")
        # the API holds urls to thumbnails, but some thumbnails forward to Deadlinks - we try to filter them out:
        if thumbnail_url == "https://memucho.de/Fehler/404" or thumbnail_url == "https://memucho.de/Fehler/500":
            logging.warning(f"Deadlink found for thumbnail_url: {thumbnail_url}")
        if thumbnail_url is not None:
            base.add_value("thumbnail", thumbnail_url)
        # alternative Thumbnail (just in case it's needed in the future):
        # thumb = response.xpath('//meta[@property="og:image"]//@content').get()
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("title", response.meta["item"].get("Name").strip())
        # ToDo confirm if we keep these keywords or not, this has always been a workaround-solution
        # keywords are grabbed from the link-descriptions of "Untergeordnete Themen"
        # keywords = response.xpath('//*[@class="topic-name"]//text()').getall()
        keyword_set = set(
            filter(
                lambda x: x,
                map(
                    lambda x: x.strip(),
                    response.xpath(
                        '//*[@id="ContentModuleApp"]//*[@class="topic-name"]//text()'
                    ).getall(),
                ),
            )
        )
        keyword_set.remove("{{category.Name}}")  # remove placeholders
        general.add_value("keyword", list(keyword_set))
        description_from_header = response.xpath('//meta[@name="description"]/@content').getall()
        # description_from_body = "\n".join(
        #     list(
        #         filter(
        #             lambda x: x,
        #             map(
        #                 lambda x: x.strip(),
        #                 response.xpath(
        #                     '//*[@id="ContentModuleApp"]//*[@content-module-type="inlinetext"]//p//text()'
        #                 ).getall(),
        #             ),
        #         )
        #     )
        # ).strip()
        general.add_value("description", description_from_header)
        return general

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", "text/html")
        technical.add_value("location", response.url)
        return technical

    def getLicense(self, response):
        license_loader = LomBase.getLicense(self, response)
        license_loader.add_value("url", Constants.LICENSE_CC_BY_40)
        # author = response.meta["item"].get("Author")
        # the author information comes straight from the memucho API and consists of memucho usernames
        # ToDo: confirm if memucho usernames are desired values for author information
        # if author is not None:
        #     license_loader.add_value("author", author)
        return license_loader

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.add_value("new_lrt", "6b9748e4-fb3b-4082-ae08-c7a11c717256")  # "Wiki (dynamisch)"
        return valuespaces
