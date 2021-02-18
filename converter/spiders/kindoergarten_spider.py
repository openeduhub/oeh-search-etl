from __future__ import annotations
import scrapy
from dataclasses import dataclass, field

from scrapy.utils.project import get_project_settings

from converter.constants import Constants
from converter.items import BaseItemLoader, LomGeneralItemloader, LomBaseItemloader, LomTechnicalItemLoader, \
    LicenseItemLoader, PermissionItemLoader, ResponseItemLoader, LomEducationalItemLoader, ValuespaceItemLoader
from converter.spiders.base_classes.meta_base import SpiderBase
from typing import Optional, List
from converter.dc_items.lom import General, Technical, Schema
from converter.util.sitemap import SitemapEntry, from_xml_response
from urllib import parse


class KindoergartenSpider(scrapy.Spider, metaclass=SpiderBase):
    """
    scrapes the kindOERgarten wordpress.
    this wordpress instance has no json api enabled, so we go by sitemap
    https://kindoergarten.wordpress.com/sitemap.xml
    """
    start_urls = ['https://kindoergarten.wordpress.com/sitemap.xml']
    name = 'kindoergarten_spider'

    def parse(self, response: scrapy.http.XmlResponse, **kwargs):
        """
        one url element usually looks like this:
        <url>
            <loc>https://kindoergarten.wordpress.com/2017/10/20/wuerfelblatt-trauben-bis-3-0047/</loc>
            <mobile:mobile/>
            <image:image>
            <image:loc>https://kindoergarten.files.wordpress.com/2017/08/ankuendigung-wuerfelblatt_trauben_bis3.jpg</image:loc>
            <image:title>Ankuendigung-Wuerfelblatt_Trauben_bis3</image:title>
            </image:image>
            <lastmod>2018-05-29T20:47:12+00:00</lastmod>
            <changefreq>monthly</changefreq>
        </url>
        """
        items = from_xml_response(response)
        # yield from items
        for item in items:
            yield response.follow(item.loc, callback=self.parse_site, cb_kwargs={'sitemap_entry': item})

    def parse_site(self, response: scrapy.http.HtmlResponse, sitemap_entry: SitemapEntry = None):
        # content = response.css('.entry-content')
        # content.css('.sharedaddy').remove()
        # pdf_links = content.css('ul li a').getall()
        # thumbnail_href = response.css('.post-thumbnail img::attr(src)').get()
        # title: str = response.css('.entry-title span::text').get()

        base = BaseItemLoader(response=response)
        base.add_value("sourceId", parse.urlparse(sitemap_entry.loc).path)  # id der Seite
        base.add_value("hash", sitemap_entry.lastmod)  # version/Datum der Seite
        # we assume that content is imported. Please use replace_value if you import something different
        base.add_value("type", Constants.TYPE_MATERIAL)
        base.add_css('thumbnail', '.post-thumbnail img::attr(src)')
        base.add_value('lastModified', sitemap_entry.lastmod)
        lom = LomBaseItemloader()
        general = LomGeneralItemloader(response=response)
        general.add_css('title', '.entry-title span::text')
        general.add_css('description', '.entry-content p::text')
        general.add_css('keyword', '.post-categories a::text')
        lom.add_value("general", general.load_item())
        technical = LomTechnicalItemLoader()
        technical.add_value('format', 'text/html')
        technical.add_value('location', sitemap_entry.loc)
        lom.add_value("technical", technical.load_item())
        # lifecycle = LomLifecycleItemloader()
        # lom.add_value("lifecycle", lifecycle.load_item())
        edu = LomEducationalItemLoader()
        lom.add_value("educational", edu.load_item())
        # classification = LomClassificationItemLoader()
        # lom.add_value("classification", classification.load_item())
        base.add_value("lom", lom.load_item())
        vs = ValuespaceItemLoader()
        base.add_value("valuespaces", vs.load_item())
        lic = LicenseItemLoader()
        lic.add_value('url', Constants.LICENSE_CC_ZERO_10)
        base.add_value("license", lic.load_item())
        permissions = PermissionItemLoader(response=response)
        # default all materials to public, needs to be changed depending on the spider!
        permissions.add_value("public", self.settings.get("DEFAULT_PUBLIC_STATE"))

        base.add_value("permissions", permissions.load_item())
        response_loader = ResponseItemLoader()
        response_loader.add_value('url', response.url)
        base.add_value("response", response_loader.load_item())
        yield base.load_item()
        # yield Schema(general=general, technical=technical)
        # yield technical.to_alfresco() | general.to_alfresco()




