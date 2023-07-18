import re
from typing import Optional

import requests
import scrapy

from .base_classes import RSSListBase
from ..web_tools import WebEngine


class ZDFRSSSpider(RSSListBase):
    name = "zdf_rss_spider"
    friendlyName = "ZDF"
    url = "https://www.zdf.de/"
    version = "0.1.1"  # last update: 2023-02-01
    custom_settings = {
        'WEB_TOOLS': WebEngine.Playwright
    }

    def __init__(self, **kwargs):
        RSSListBase.__init__(self, "../csv/zdf_rss.csv", **kwargs)  # couldn't find file, had to move 1 folder upwards

    def getLicense(self, response):
        license_info = RSSListBase.getLicense(self, response)
        page_content = scrapy.Selector(requests.get(response.url))
        date = self.get_expiration_date(page_content)
        if date:
            license_info.add_value('expirationDate', date)
        return license_info

    @staticmethod
    def get_expiration_date(response) -> Optional[str]:
        # grabbing the expiration date from the "other-infos"-container:
        # XPath: /html/body/div[1]/div/main/article/article[1]/div/div/div[2]/div/div[1]/div/dl[2]/dd
        # using the container-name instead to grab the 'verfügbar bis <datum>'-string:
        # logging.debug("current URL inside the get_expiration_date method: ", response)
        if response is not None:
            temp_string = response.xpath(
                '//div[contains(@class,"other-infos")]/dl[2]/dd[contains(@class,"desc-text")]/text()'
            ).get()
            if temp_string is not None:
                temp_string = temp_string.strip()
                # using RegEx to grab the date only, by using this pattern:
                # (1-2 digits for the day).(1-2 digits for the month).(4 digits for the year), e.g. 13.04.2026
                date_reg_ex = re.compile(r'(\d{1,2}).(\d{1,2}).(\d{4})')
                date_temp = date_reg_ex.search(temp_string)
                return date_temp.group()
        return None
