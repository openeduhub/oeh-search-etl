import html
import re
from typing import Optional

import dateparser
import requests
import scrapy

from converter.constants import Constants
from converter.valuespace_helper import ValuespaceHelper
from .base_classes import LomBase, RSSBase


# Spider to fetch RSS from planet schule
class PlanetSchuleSpider(RSSBase):
    name = "planet_schule_spider"
    friendlyName = "planet schule"
    url = "https://www.planet-schule.de"
    start_urls = [
        "https://www.planet-schule.de/data/planet-schule-vodcast-komplett.rss"
    ]
    version = "0.1.3"   # last update: 2022-02-16
    # Planet Schule allows us to crawl their site, therefore ignore the robots.txt directions, but don't hammer the
    # site while debugging
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        # 'AUTOTHROTTLE_ENABLED': True
    }

    # forceUpdate = True        # for debugging purposes (or forcing a "duration"-update on every video entry)

    def __init__(self, **kwargs):
        RSSBase.__init__(self, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    async def mapResponse(self, response):
        return await LomBase.mapResponse(self, response)

    def startHandler(self, response):
        for item in response.xpath("//rss/channel/item"):
            copyResponse = response.copy()
            # TODO: rebuild copyResponse.meta["item"] with scrapy's more modern solution to handling additional data
            #  in callbacks, see:
            # https://docs.scrapy.org/en/latest/topics/request-response.html#topics-request-response-ref-request-callback-arguments
            copyResponse.meta["item"] = item
            if self.hasChanged(copyResponse):
                yield scrapy.Request(
                    url=item.xpath("link//text()").get(),
                    callback=self.handleLink,
                    meta={"item": item},
                    # cb_kwargs=dict({
                    #     item.xpath("link//text()").get(): item.xpath("duration//text()").get()
                    # })
                )

    async def handleLink(self, response):
        return await LomBase.parse(self, response)

    # thumbnail is always the same, do not use the one from rss
    def getBase(self, response):
        return LomBase.getBase(self, response)

    def getLOMGeneral(self, response):
        general = RSSBase.getLOMGeneral(self, response)
        general.add_value(
            "keyword",
            response.xpath(
                '//div[@class="sen_info_v2"]//p[contains(text(),"Schlagworte")]/parent::*/parent::*/div[last()]/p/a//text()'
            ).getall(),
        )
        return general

    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        license.add_value("internal", Constants.LICENSE_COPYRIGHT_LAW)
        # since expirationDate is only found in the html body, we need to crawl the site itself as well:
        page_content = scrapy.Selector(requests.get(response.url))
        date = self.get_expiration_date(page_content)
        if date:
            license.add_value('expirationDate', date)
        return license

    def getValuespaces(self, response):
        valuespaces = RSSBase.getValuespaces(self, response)
        try:
            range = response.xpath(
                '//div[@class="sen_info_v2"]//p[contains(text(),"Klassenstufe")]/parent::*/parent::*/div[last()]/p//text()'
            ).get()
            range = range.split(" - ")
            valuespaces.add_value(
                "educationalContext", ValuespaceHelper.educationalContextByGrade(range)
            )
        except:
            pass
        discipline = response.xpath(
            '//div[@class="sen_info_v2"]//p[contains(text(),"Fächer")]/parent::*/parent::*/div[last()]/p/a//text()'
        ).getall()
        valuespaces.add_value("discipline", discipline)

        # # ToDo: remove old learningResourceType after crawler version 0.1.4
        # # since the old learningResourceType is getting phased out -> it is replaced by new_lrt
        # lrt = ValuespaceHelper.mimetypeToLearningResourceType(
        #     response.meta["item"].xpath("enclosure/@type").get()
        # )
        # if lrt:
        #     valuespaces.add_value("learningResourceType", lrt)

        valuespaces.add_value('new_lrt', "3616febb-8cf8-4503-8f80-ebc552d85506")
        # "TV-Sendung und Video-Podcast"
        return valuespaces

    @staticmethod
    def get_expiration_date(response) -> Optional[str]:
        # "Film online bis ..." is a string inside a div container. The XPath to it is:
        # response.xpath('//*[@id="container_mitte"]/div[2]/div[2]/div/div/div[3]/div[2]')
        # or by its class name "licence_info" (sic!) - watch out for the typo on the website itself!
        # (this might get fixed in the future and break the spider!)
        if response is not None:
            temp_string = response.xpath('//div[@class="licence_info"]/text()').get().strip()
            if temp_string is not None:
                # fetch the date from the
                temp_string = temp_string.strip()
                date_reg_ex = re.compile(r'(\d{1,2}).\s(\w+)\s(\d{4})')
                date_only = date_reg_ex.search(temp_string)
                # parse the date and give it back as ISO-formatted string
                parsed_date = dateparser.parse(date_only.group())
                date_in_iso = parsed_date.isoformat()
                return date_in_iso
        return None

    @staticmethod
    def get_embed_code(response) -> Optional[str]:
        # work in progress (not used anywhere at the moment), grabs the <div><iframe> container as a string
        # (the one that you get after clicking on the embed button)
        if response is not None:
            # grab embed script from the content page itself:
            # example url that has an embed element: https://www.planet-schule.de/sf/php/sendungen.php?sendung=11142
            # important: not every video has embed-codes enabled!

            # find the "film_embed"-button/link:
            # //*[@id="container_mitte"]/div[2]/div[2]/div/div/div[3]/a[4]
            film_embed_link = response.xpath('//a[@class="film_embed_link"]').get()
            if film_embed_link is not None:
                # the embed code itself:
                embed_code = response.xpath('//*[@id="film_embed_code"]/text()').get()
                if embed_code is not None:
                    embed_code = html.unescape(embed_code)
                    return embed_code
