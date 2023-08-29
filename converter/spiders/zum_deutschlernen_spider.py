import json

import jmespath
import trafilatura

from converter.items import (
    LomTechnicalItem,
    LicenseItem,
    LomGeneralItem,
    ValuespaceItem,
    LomGeneralItemloader,
    ValuespaceItemLoader,
)
from .base_classes import MediaWikiBase
import scrapy

from ..constants import Constants
from ..web_tools import WebEngine


class ZUMDeutschLernenSpider(MediaWikiBase, scrapy.Spider):
    name = "zum_deutschlernen_spider"
    friendlyName = "ZUM-Deutsch-Lernen"
    url = "https://deutsch-lernen.zum.de/"
    version = "0.1.5"  # last update: 2023-08-29
    license = Constants.LICENSE_CC_BY_40
    custom_settings = {"WEB_TOOLS": WebEngine.Playwright, "AUTOTHROTTLE_ENABLED": True, "AUTOTHROTTLE_DEBUG": True}

    def __init__(self, **kwargs):
        MediaWikiBase.__init__(self, **kwargs)

    def parse_page_query(self, response: scrapy.http.Response):
        """
        @url https://deutsch-lernen.zum.de/api.php?format=json&action=query&list=allpages&aplimit=100&apfilterredir=nonredirects
        @returns requests 101 101
        """
        yield from super().parse_page_query(response)

    def getLOMGeneral(self, response=None) -> LomGeneralItemloader:
        general_loader: LomGeneralItemloader = super().getLOMGeneral(response)
        jmes_categories = jmespath.compile('parse.categories[]."*"')
        category_list: list[str] = jmes_categories.search(response.meta["item"])
        # the API sometimes returns unusable descriptions like "START_WIDGET87710400b0e5c411-0END_WIDGET" (and carries
        # the same string in the header)
        descriptions_collected: list[str] = general_loader.get_collected_values('description')
        if descriptions_collected and type(descriptions_collected) is list:
            description_str: str = descriptions_collected[0]
            if description_str.startswith("START_WIDGET"):
                # this will typically be the case for H5P materials which carry almost no useful metadata
                urls_collected: list[str] = self.getLOMTechnical(response=response).get_collected_values('location')
                if urls_collected and type(urls_collected) is list:
                    # making sure that we actually fetch the main urL, then extract the fulltext with trafilatura
                    item_url: str = urls_collected[0]
                    downloaded: str = trafilatura.fetch_url(item_url)
                    trafilatura_text: str = trafilatura.extract(downloaded)
                    if trafilatura_text:
                        general_loader.replace_value('description', trafilatura_text)

        general_loader.replace_value("keyword", category_list)
        # ToDo (later): clean up matched Vocab values from keywords, so they don't appear in both fields?
        return general_loader

    def getValuespaces(self, response):
        vs_loader: ValuespaceItemLoader = super().getValuespaces(response)
        # hard-coded to "Deutsch" / "DaZ" because all materials of this MediaWiki were created for this purpose
        vs_loader.add_value("discipline", "28002")  # "Deutsch als Zweitsprache"
        vs_loader.add_value("discipline", "120")  # Deutsch
        jmes_categories = jmespath.compile('parse.categories[]."*"')
        category_list: list[str] = jmes_categories.search(response.meta["item"])
        vs_loader.add_value('languageLevel', category_list)
        return vs_loader

    # ToDo: The methods below are (most probably) code-artifacts from (unfinished) Scrapy contracts, and aren't
    #  executed during a normal crawl runtime:
    #  - technical_item
    #  - license_item
    #  - general_item
    #  - valuespace_item

    def technical_item(self, response=None) -> LomTechnicalItem:
        """
        @url https://deutsch-lernen.zum.de/api.php?format=json&action=parse&pageid=477&prop=text|categories|links|sections|revid|iwlinks|properties
        @scrapes format location
        """
        response.meta["item"] = json.loads(response.body)
        return self.getLOMTechnical(response).load_item()

    def license_item(self, response) -> LicenseItem:
        """
        @url https://deutsch-lernen.zum.de/api.php?format=json&action=parse&pageid=477&prop=text|categories|links|sections|revid|iwlinks|properties
        @scrapes url
        """
        response.meta["item"] = json.loads(response.body)
        return self.getLicense(response).load_item()

    def general_item(self, response=None) -> LomGeneralItem:
        """
        @url https://deutsch-lernen.zum.de/api.php?format=json&action=parse&pageid=477&prop=text|categories|links|sections|revid|iwlinks|properties
        @scrapes title keyword description
        """
        response.meta["item"] = json.loads(response.body)
        return self.getLOMGeneral(response).load_item()

    def valuespace_item(self, response) -> ValuespaceItem:
        """
        @url https://deutsch-lernen.zum.de/api.php?format=json&action=parse&pageid=477&prop=text|categories|links|sections|revid|iwlinks|properties
        @scrapes discipline educationalContext intendedEndUserRole
        """
        response.meta["item"] = json.loads(response.body)
        return self.getValuespaces(response).load_item()
