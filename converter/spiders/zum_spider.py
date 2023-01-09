from __future__ import annotations

import scrapy

from converter.constants import Constants
from converter.items import LicenseItem, LomTechnicalItem, ValuespaceItem, LomGeneralItem
from converter.spiders.base_classes import MediaWikiBase
from converter.web_tools import WebEngine


class ZUMSpider(MediaWikiBase, scrapy.Spider):
    name = "zum_spider"
    friendlyName = "ZUM-Unterrichten"
    url = "https://unterrichten.zum.de/"
    version = "0.1.3"  # last update: 2023-01-09
    license = Constants.LICENSE_CC_BY_SA_40
    custom_settings = {
        "WEB_TOOLS": WebEngine.Playwright,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True
    }

    def technical_item(self, response=None) -> LomTechnicalItem:
        """
        @url https://unterrichten.zum.de/api.php?format=json&action=parse&pageid=19445&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties|parsewarnings
        @scrapes format location
        """
        return self.getLOMTechnical(response).load_item()

    def license_item(self, response) -> LicenseItem:
        """
        @url https://unterrichten.zum.de/api.php?format=json&action=parse&pageid=19445&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties|parsewarnings
        @scrapes url
        """
        return self.getLicense(response).load_item()

    def general_item(self, response=None) -> LomGeneralItem:
        """
        @url https://unterrichten.zum.de/api.php?format=json&action=parse&pageid=19445&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties|parsewarnings
        @scrapes title keyword description
        """
        return self.getLOMGeneral(response).load_item()

    def valuespace_item(self, response) -> ValuespaceItem:
        """
        @url https://unterrichten.zum.de/api.php?format=json&action=parse&pageid=19445&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties|parsewarnings
        @scrapes discipline educationalContext intendedEndUserRole
        """
        return self.getValuespaces(response).load_item()
