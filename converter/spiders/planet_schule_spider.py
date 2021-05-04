import logging
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
    version = "0.1.1"

    def __init__(self, **kwargs):
        RSSBase.__init__(self, **kwargs)

    def mapResponse(self, response):
        return LomBase.mapResponse(self, response)

    def startHandler(self, response):
        for item in response.xpath("//rss/channel/item"):
            copyResponse = response.copy()
            copyResponse.meta["item"] = item
            if self.hasChanged(copyResponse):
                yield scrapy.Request(
                    url=item.xpath("link//text()").get(),
                    callback=self.handleLink,
                    meta={"item": item},
                )

    def handleLink(self, response):
        return LomBase.parse(self, response)

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

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("format", "text/html")
        technical.add_value("location", response.url)
        return technical

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
        lrt = ValuespaceHelper.mimetypeToLearningResourceType(
            response.meta["item"].xpath("enclosure/@type").get()
        )
        if lrt:
            valuespaces.add_value("learningResourceType", lrt)
        return valuespaces

    @staticmethod
    def get_expiration_date(response) -> Optional[str]:
        # "Film online bis ..."-XPath:
        # response.xpath('//*[@id="container_mitte"]/div[2]/div[2]/div/div/div[3]/div[2]')
        # or by its class name "licence_info" (sic!) - watch out for the typo on the website itself!
        # (this might get fixed in the future and break the spider!)
        logging.debug("current URL inside the get_expiration_date method: ", response)
        if response is not None:
            temp_string = response.xpath('//div[@class="licence_info"]/text()').get().strip()
            if temp_string is not None:
                temp_string = temp_string.strip()
                date_reg_ex = re.compile(r'(\d{1,2}).\s(\w+)\s(\d{4})')
                date_only = date_reg_ex.search(temp_string)
                parsed_date = dateparser.parse(date_only.group())
                date_in_iso = parsed_date.isoformat()
                return date_in_iso
        return None
