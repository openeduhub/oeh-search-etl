from converter.items import LomTechnicalItem, LicenseItem, LomGeneralItem, ValuespaceItem
from .base_classes.mediawiki_base import MediaWikiBase, jmes_pageids
import scrapy
import json
import jmespath
from ..constants import Constants

jmes_continue = jmespath.compile('"query-continue".allpages')


class ZUMSpider(MediaWikiBase, scrapy.Spider):
    name = "zum_klexikon_spider"
    friendlyName = "ZUM-Klexikon"
    url = "https://klexikon.zum.de/"
    version = "0.1.0"
    license = Constants.LICENSE_CC_BY_SA_30

    def parse_page_query(self, response: scrapy.http.Response):
        """
        @url https://klexikon.zum.de/api.php?format=json&action=query&list=allpages&aplimit=100&apfilterredir=nonredirects
        @returns requests 101 101
        """
        data = json.loads(response.body)
        pageids = jmes_pageids.search(data)
        for pageid in pageids:
            yield scrapy.FormRequest(
                url=self.api_url,
                formdata=self._parse_params | {'pageid': str(pageid)},
                callback=self.parse_page_data,
                cb_kwargs={"extra": {'pageid': str(pageid)}}
            )
        if 'query-continue' not in data:
            return
        yield self.query_for_pages(jmes_continue.search(data))

    def getId(self, response=None):
        return response.meta['item_extra']['pageid']

    def technical_item(self, response) -> LomTechnicalItem:
        """
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=10031&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        @scrapes format location
        """
        response.meta['item'] = json.loads(response.body)
        return self.getLOMTechnical(response).load_item()

    def license_item(self, response) -> LicenseItem:
        """
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=10031&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        @scrapes url
        """
        response.meta['item'] = json.loads(response.body)
        return self.getLicense(response).load_item()

    def general_item(self, response) -> LomGeneralItem:
        """
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=4937&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        @scrapes title keyword description
        """
        response.meta['item'] = json.loads(response.body)
        return self.getLOMGeneral(response).load_item()

    def valuespace_item(self, response) -> ValuespaceItem:
        """
        @url https://klexikon.zum.de/api.php?format=json&action=parse&pageid=10031&prop=text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties
        @scrapes discipline educationalContext intendedEndUserRole
        """
        response.meta['item'] = json.loads(response.body)
        return self.getValuespaces(response).load_item()
