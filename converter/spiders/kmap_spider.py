import json
import logging

import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader
from converter.spiders.base_classes import LomBase
from converter.util.sitemap import from_xml_response
from converter.web_tools import WebEngine, WebTools


class KMapSpider(CrawlSpider, LomBase):
    name = "kmap_spider"
    friendlyName = "KMap.eu"
    version = "0.0.6"   # last update: 2022-05-20
    sitemap_urls = [
        "https://kmap.eu/server/sitemap/Mathematik",
        "https://kmap.eu/server/sitemap/Physik"
    ]
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        # "AUTOTHROTTLE_DEBUG": True
    }
    allowed_domains = ['kmap.eu']
    # keep the console clean from spammy DEBUG-level logging messages, adjust as needed:
    logging.getLogger('websockets.server').setLevel(logging.ERROR)
    logging.getLogger('websockets.protocol').setLevel(logging.ERROR)

    def start_requests(self) -> scrapy.Request:
        for sitemap_url in self.sitemap_urls:
            yield scrapy.Request(url=sitemap_url, callback=self.parse_sitemap)

    def parse_sitemap(self, response) -> scrapy.Request:
        """

        Scrapy Contracts:
        @url https://kmap.eu/server/sitemap/Mathematik
        @returns requests 50
        """
        sitemap_items = from_xml_response(response)
        for sitemap_item in sitemap_items:
            temp_dict = {
                'lastModified': sitemap_item.lastmod
            }
            yield scrapy.Request(url=sitemap_item.loc, callback=self.parse, cb_kwargs=temp_dict)

    def getId(self, response=None) -> str:
        return response.url

    def getHash(self, response=None) -> str:
        pass

    def parse(self, response: scrapy.http.Response, **kwargs) -> BaseItemLoader:
        """

        Scrapy Contracts:
        @url https://kmap.eu/app/browser/Mathematik/Exponentialfunktionen/Asymptoten
        @returns item 1
        """
        last_modified = kwargs.get("lastModified")
        url_data = WebTools.getUrlData(response.url)
        splash_html_string = url_data.get('html')
        json_ld_string: str = Selector(text=splash_html_string).xpath('//*[@id="ld"]/text()').get()
        json_ld: dict = json.loads(json_ld_string)
        # TODO: skip item method - (skips item if it's an empty knowledge map)

        base = BaseItemLoader()
        base.add_value('sourceId', response.url)
        hash_temp = json_ld.get("mainEntity").get("datePublished")
        hash_temp += self.version
        base.add_value('hash', hash_temp)
        base.add_value('lastModified', last_modified)
        # Thumbnails have their own url path, which can be found in the json+ld:
        #   "thumbnailUrl": "/snappy/Physik/Grundlagen/Potenzschreibweise"
        # e.g. for the item https://kmap.eu/app/browser/Physik/Grundlagen/Potenzschreibweise
        # the thumbnail can be found at https://kmap.eu/snappy/Physik/Grundlagen/Potenzschreibweise
        thumbnail_path = json_ld.get("mainEntity").get("thumbnailUrl")
        if thumbnail_path is not None:
            base.add_value('thumbnail', 'https://kmap.eu' + thumbnail_path)

        lom = LomBaseItemloader()
        general = LomGeneralItemloader()
        general.add_value('identifier', json_ld.get("mainEntity").get("mainEntityOfPage"))
        keywords_string: str = json_ld.get("mainEntity").get("keywords")
        keyword_list = keywords_string.rsplit(", ")
        general.add_value('keyword', keyword_list)
        general.add_value('title', json_ld.get("mainEntity").get("name"))
        general.add_value('description', json_ld.get("mainEntity").get("description"))
        general.add_value('language', json_ld.get("mainEntity").get("inLanguage"))
        lom.add_value('general', general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value('format', 'text/html')
        technical.add_value('location', response.url)
        lom.add_value('technical', technical.load_item())

        lifecycle = LomLifecycleItemloader()
        lifecycle.add_value('role', 'publisher')
        lifecycle.add_value('organization', json_ld.get("mainEntity").get("publisher").get("name"))
        author_email = json_ld.get("mainEntity").get("publisher").get("email")
        if author_email is not None:
            lifecycle.add_value('email', author_email)
        lifecycle.add_value('url', 'https://kmap.eu/')
        lifecycle.add_value('date', json_ld.get("mainEntity").get("datePublished"))
        lom.add_value('lifecycle', lifecycle.load_item())

        educational = LomEducationalItemLoader()
        lom.add_value('educational', educational.load_item())
        base.add_value('lom', lom.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value('new_lrt', Constants.NEW_LRT_MATERIAL)
        vs.add_value('discipline', json_ld.get("mainEntity").get("about"))
        vs.add_value('intendedEndUserRole', json_ld.get("mainEntity").get("audience"))
        vs.add_value('new_lrt', json_ld.get("mainEntity").get("learningResourceType"))
        vs.add_value('price', 'no')
        vs.add_value('conditionsOfAccess', 'login required for additional features')
        base.add_value('valuespaces', vs.load_item())

        lic = LicenseItemLoader()
        lic.add_value('author', json_ld.get("mainEntity").get("author").get("name"))
        lic.add_value('url', json_ld.get("mainEntity").get("license"))
        base.add_value('license', lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        base.add_value('response', super().mapResponse(response).load_item())
        # KMap doesn't deliver fulltext to neither splash nor playwright, the fulltext object will be showing up as
        #   'text': 'JavaScript wird benötigt!\n\n',
        # in the final "scrapy.Item". As long as KMap doesn't change the way it's delivering its JavaScript content,
        # our crawler won't be able to work around this limitation.
        return base.load_item()
