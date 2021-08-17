import json

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy_splash import SplashRequest

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomLifecycleItemloader, LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, ResponseItemLoader
from converter.spiders.base_classes import LomBase
from converter.util.sitemap import from_xml_response


class KMapSpider(CrawlSpider, LomBase):
    name = "kmap_spider"
    friendlyName = "KMap.eu"
    version = "0.0.3"
    sitemap_urls = [
        "https://kmap.eu/server/sitemap/Mathematik",
        "https://kmap.eu/server/sitemap/Physik"
    ]
    allowed_domains = ['kmap.eu']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
        },
        'SPIDER_MIDDLEWARES': {'scrapy_splash.SplashDeduplicateArgsMiddleware': 100},
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter'
    }

    def start_requests(self) -> scrapy.Request:
        for sitemap_url in self.sitemap_urls:
            yield scrapy.Request(url=sitemap_url, callback=self.parse_sitemap)

    def parse_sitemap(self, response) -> scrapy.Request:
        sitemap_items = from_xml_response(response)
        for sitemap_item in sitemap_items:
            temp_dict = {
                'lastModified': sitemap_item.lastmod
            }
            yield SplashRequest(url=sitemap_item.loc, callback=self.parse, cb_kwargs=temp_dict, args={
                'wait': 5,
                'html': 1
            })

    def getId(self, response=None) -> str:
        return response.url

    def getHash(self, response=None) -> str:
        pass

    def parse(self, response: scrapy.http.Response, **kwargs) -> BaseItemLoader:
        # print("PARSE METHOD:", response.url)
        last_modified = kwargs.get("lastModified")
        json_ld_string: str = response.xpath('//*[@id="ld"]/text()').get()
        json_ld: dict = json.loads(json_ld_string)
        # for debug purposes - checking if the json_ld is correct/available:
        # print("LD_JSON =", json_ld)
        # print(type(json_ld))

        base = BaseItemLoader()
        base.add_value('sourceId', response.url)
        hash_temp = json_ld.get("mainEntity").get("datePublished")
        hash_temp += self.version
        base.add_value('hash', hash_temp)
        base.add_value('lastModified', last_modified)
        base.add_value('type', Constants.TYPE_MATERIAL)
        # Thumbnails have their own url path, which can be found in the json+ld:
        #   "thumbnailUrl": "/snappy/Physik/Grundlagen/Potenzschreibweise"
        # e.g. for the item https://kmap.eu/app/browser/Physik/Grundlagen/Potenzschreibweise
        # the thumbnail can be found at https://kmap.eu/snappy/Physik/Grundlagen/Potenzschreibweise
        thumbnail_path = json_ld.get("mainEntity").get("thumbnailUrl")
        if thumbnail_path is not None:
            base.add_value('thumbnail', thumbnail_path)

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
        vs.add_value('discipline', json_ld.get("mainEntity").get("about"))
        vs.add_value('intendedEndUserRole', json_ld.get("mainEntity").get("audience"))
        vs.add_value('learningResourceType', json_ld.get("mainEntity").get("learningResourceType"))
        vs.add_value('price', 'no')
        vs.add_value('conditionsOfAccess', 'login required for additional features')
        base.add_value('valuespaces', vs.load_item())

        lic = LicenseItemLoader()
        lic.add_value('author', json_ld.get("mainEntity").get("author").get("name"))
        lic.add_value('url', json_ld.get("mainEntity").get("license"))
        base.add_value('license', lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader = ResponseItemLoader()
        response_loader.add_value("url", response.url)
        base.add_value("response", response_loader.load_item())

        return base.load_item()
