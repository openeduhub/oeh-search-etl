from __future__ import annotations

import scrapy
import trafilatura

from converter.constants import Constants
from converter.items import LicenseItem, LomTechnicalItem, ValuespaceItem, LomGeneralItem, LomGeneralItemloader
from converter.spiders.base_classes import MediaWikiBase
from converter.web_tools import WebEngine


class ZUMSpider(MediaWikiBase, scrapy.Spider):
    name = "zum_spider"
    friendlyName = "ZUM-Unterrichten"
    url = "https://unterrichten.zum.de/"
    version = "0.1.5"  # last update: 2023-08-29
    license = Constants.LICENSE_CC_BY_SA_40
    custom_settings = {"WEB_TOOLS": WebEngine.Playwright, "AUTOTHROTTLE_ENABLED": True, "AUTOTHROTTLE_DEBUG": True}

    def __init__(self, **kwargs):
        MediaWikiBase.__init__(self, **kwargs)

    def getLOMGeneral(self, response=None) -> LomGeneralItemloader:
        general_loader: LomGeneralItemloader = super().getLOMGeneral(response)
        description_collected: list[str] = general_loader.get_collected_values("description")
        if not description_collected:
            # there are several ZUM Unterrichten items which have no description and would be dropped otherwise
            urls_collected: list[str] = self.getLOMTechnical(response=response).get_collected_values("location")
            if urls_collected and type(urls_collected) is list:
                # making sure that we actually fetch the main urL, then extract the fulltext with trafilatura
                item_url: str = urls_collected[0]
                downloaded: str = trafilatura.fetch_url(item_url)
                trafilatura_text: str = trafilatura.extract(downloaded)
                if trafilatura_text:
                    general_loader.replace_value("description", trafilatura_text)
        return general_loader

    # ToDo: The methods below are (most probably) code-artifacts from (unfinished) Scrapy contracts, and aren't
    #  executed during a normal crawl runtime:
    #  - technical_item
    #  - license_item
    #  - general_item
    #  - valuespace_item

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
