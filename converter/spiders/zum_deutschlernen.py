import json

from converter.items import LomTechnicalItem, LicenseItem, LomGeneralItem, ValuespaceItem
from .base_classes import MediaWikiBase
import scrapy

from ..constants import Constants
from ..web_tools import WebEngine


class ZUMSpider(MediaWikiBase, scrapy.Spider):
    name = "zum_deutschlernen_spider"
    friendlyName = "ZUM-Deutsch-Lernen"
    url = "https://deutsch-lernen.zum.de/"
    version = "0.1.3"  # last update: 2023-01-09
    license = Constants.LICENSE_CC_BY_40
    custom_settings = {
        "WEB_TOOLS": WebEngine.Playwright,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True
    }

    def parse_page_query(self, response: scrapy.http.Response):
        """
        @url https://deutsch-lernen.zum.de/api.php?format=json&action=query&list=allpages&aplimit=100&apfilterredir=nonredirects
        @returns requests 101 101
        """
        yield from super().parse_page_query(response)

    def technical_item(self, response=None) -> LomTechnicalItem:
        """
        @url https://deutsch-lernen.zum.de/api.php?format=json&action=parse&pageid=477&prop=text|categories|links|sections|revid|iwlinks|properties
        @scrapes format location
        """
        response.meta['item'] = json.loads(response.body)
        return self.getLOMTechnical(response).load_item()

    def license_item(self, response) -> LicenseItem:
        """
        @url https://deutsch-lernen.zum.de/api.php?format=json&action=parse&pageid=477&prop=text|categories|links|sections|revid|iwlinks|properties
        @scrapes url
        """
        response.meta['item'] = json.loads(response.body)
        return self.getLicense(response).load_item()

    def general_item(self, response=None) -> LomGeneralItem:
        """
        @url https://deutsch-lernen.zum.de/api.php?format=json&action=parse&pageid=477&prop=text|categories|links|sections|revid|iwlinks|properties
        @scrapes title keyword description
        """
        response.meta['item'] = json.loads(response.body)
        return self.getLOMGeneral(response).load_item()

    def valuespace_item(self, response) -> ValuespaceItem:
        """
        @url https://deutsch-lernen.zum.de/api.php?format=json&action=parse&pageid=477&prop=text|categories|links|sections|revid|iwlinks|properties
        @scrapes discipline educationalContext intendedEndUserRole
        """
        response.meta['item'] = json.loads(response.body)
        return self.getValuespaces(response).load_item()
