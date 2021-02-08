from converter.items import LomTechnicalItem, LicenseItem, LomGeneralItem, ValuespaceItem
from .base_classes import MediaWikiBase
import scrapy

from ..constants import Constants


class ZUMSpider(MediaWikiBase, scrapy.Spider):
    name = "zum_klexikon_spider"
    friendlyName = "ZUM-Klexikon"
    url = "https://klexikon.zum.de/"
    version = "0.1.0"
    license = Constants.LICENSE_CC_BY_SA_30

    def technical_item(self, response=None) -> LomTechnicalItem:
        """
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=10031&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        @scrapes format location
        """
        return self.getLOMTechnical(response).load_item()

    def license_item(self, response) -> LicenseItem:
        """
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=10031&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        @scrapes url
        """
        return self.getLicense(response).load_item()

    def general_item(self, response=None) -> LomGeneralItem:
        """
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=4937&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        @scrapes title keyword description
        """
        return self.getLOMGeneral(response).load_item()

    def valuespace_item(self, response) -> ValuespaceItem:
        """
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=10031&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        @scrapes discipline educationalContext intendedEndUserRole
        """
        return self.getValuespaces(response).load_item()
