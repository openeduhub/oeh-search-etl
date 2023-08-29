import json

import jmespath
import scrapy
import w3lib.html
from scrapy import Selector

from converter.items import (
    LomTechnicalItem,
    LicenseItem,
    LomGeneralItemloader,
    ValuespaceItem,
    ValuespaceItemLoader,
    LomEducationalItemLoader,
    LomAgeRangeItemLoader,
)
from .base_classes.mediawiki_base import MediaWikiBase, jmes_pageids, jmes_title, jmes_links, jmes_continue
from ..constants import Constants
from ..web_tools import WebEngine


class ZUMKlexikonSpider(MediaWikiBase, scrapy.Spider):
    name = "zum_klexikon_spider"
    friendlyName = "ZUM-Klexikon"
    url = "https://klexikon.zum.de/"
    version = "0.1.7"  # last update: 2023-08-29
    license = Constants.LICENSE_CC_BY_SA_40
    custom_settings = {"WEB_TOOLS": WebEngine.Playwright, "AUTOTHROTTLE_ENABLED": True, "AUTOTHROTTLE_DEBUG": True}

    def parse_page_query(self, response: scrapy.http.Response):
        """

        Scrapy Contracts:
        @url https://klexikon.zum.de/api.php?format=json&action=query&list=allpages&aplimit=100&apfilterredir=nonredirects
        @returns requests 101 101
        """
        data = json.loads(response.body)
        pageids = jmes_pageids.search(data)
        for pageid in pageids:
            yield scrapy.FormRequest(
                url=self.api_url,
                formdata=self._parse_params | {"pageid": str(pageid)},
                callback=self.parse_page_data,
                cb_kwargs={"extra": {"pageid": str(pageid)}},
            )
        if "continue" not in data:
            return
        yield self.query_for_pages(jmes_continue.search(data))

    def getId(self, response=None):
        return response.meta["item_extra"]["pageid"]

    def getLOMGeneral(self, response=None) -> LomGeneralItemloader:
        """
        Gathers title, keyword and (short-)description and returns the LomGeneralItemloader afterwards.

        Scrapy Contracts:
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=4937&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        """
        # old implementation with missing 'description'-value:
        response.meta["item"] = json.loads(response.body)
        # return self.getLOMGeneral(response).load_item()
        general = LomGeneralItemloader()
        data = json.loads(response.body)
        general.replace_value("title", jmes_title.search(data))
        general.replace_value("keyword", jmes_links.search(data))

        jmes_text = jmespath.compile('parse.text."*"')
        fulltext = jmes_text.search(data)
        first_paragraph = Selector(text=fulltext).xpath("//p").get()
        # grabbing the first <p>-Element as a workaround for the missing short-description
        if first_paragraph:
            first_paragraph = w3lib.html.remove_tags(first_paragraph)
            general.add_value("description", first_paragraph)
        else:
            # if for some reason the first paragraph is not found, this is a fallback solution to manually split the
            # fulltext by its first newline (since we don't want to copypaste the "fulltext" into our description
            fulltext = w3lib.html.remove_tags(fulltext)
            first_paragraph = fulltext.split("\n")[0]
            first_paragraph = first_paragraph.strip()
            general.add_value("description", first_paragraph)
        return general

    def getValuespaces(self, response):
        vs_loader: ValuespaceItemLoader = super().getValuespaces(response)
        data: dict = json.loads(response.body)
        jmes_categories = jmespath.compile('parse.categories[]."*"')
        categories: list[str] = jmes_categories.search(data)
        if categories:
            for category in categories:
                category: str = str(category).lower()
                if "erdkunde" in category:
                    # ToDo: this is a temporary workaround because the altLabel for "geografie" is currently not
                    #  generated properly (see: ITSJOINTLY-332) and can be removed once the problem has been fixed
                    vs_loader.add_value("discipline", "220")
                if "körper und gesundheit" in category:
                    vs_loader.add_value("discipline", "080")
                if "tiere und natur" in category:
                    vs_loader.add_value("discipline", "080")
                if "politik und gesellschaft" in category:
                    vs_loader.add_value("discipline", "480")
        # ToDo: Jugendschutz - "unauffällig" -> ('ccm:oeh_quality_protection_of_minjors': 0)
        #  - we would need to implement 'oeh_quality_...'-aspects into the data model first
        #  (places that need to be touched for these (breaking?) changes: 'items.py', 'es_connector' ...?)
        vs_loader.add_value("educationalContext", "grundschule")
        vs_loader.add_value("educationalContext", "sekundarstufe_1")
        vs_loader.add_value("intendedEndUserRole", "learner")
        return vs_loader

    def getLOMEducational(self, response=None) -> LomEducationalItemLoader:
        educational_loader: LomEducationalItemLoader = super().getLOMEducational(response)
        lom_age_range_loader: LomAgeRangeItemLoader = LomAgeRangeItemLoader()
        lom_age_range_loader.add_value("fromRange", "6")
        lom_age_range_loader.add_value("toRange", "12")
        educational_loader.add_value("typicalAgeRange", lom_age_range_loader.load_item())
        return educational_loader

    # ToDo: The methods below are code-artifacts from (unfinished) Scrapy contracts, and aren't executed during normal
    #  crawl runtime:
    #  - technical_item
    #  - license_item
    #  - valuespace_item

    def technical_item(self, response) -> LomTechnicalItem:
        """

        Scrapy Contracts:
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=10031&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        """
        response.meta["item"] = json.loads(response.body)
        return self.getLOMTechnical(response).load_item()

    def license_item(self, response) -> LicenseItem:
        """

        Scrapy Contracts:
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=10031&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        """
        response.meta["item"] = json.loads(response.body)
        return self.getLicense(response).load_item()

    def valuespace_item(self, response) -> ValuespaceItem:
        """
        Scrapy Contracts:
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=10031&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        """
        response.meta["item"] = json.loads(response.body)
        return self.getValuespaces(response).load_item()
