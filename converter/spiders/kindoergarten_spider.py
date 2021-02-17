from __future__ import annotations
import scrapy
from dataclasses import dataclass, field
from converter.spiders.base_classes.meta_base import SpiderBase
from typing import Optional, List
from converter.dc_items.lom import General, Technical, Schema
from converter.util.sitemap import SitemapEntry, from_xml_response


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
        yield from items
        # for item in items:
        #     yield response.follow(item.loc, callback=self.parse_site, cb_kwargs={'sitemap_entry': item})

    def parse_site(self, response: scrapy.http.HtmlResponse, sitemap_entry: SitemapEntry = None):
        content = response.css('.entry-content')
        content.css('.sharedaddy').remove()
        pdf_links = content.css('ul li a').getall()
        description = content.css('p::text').get()
        thumbnail_href = response.css('.post-thumbnail img::attr(src)').get()
        title: str = response.css('.entry-title span::text').get()
        description: str = content.css('.entry-content p::text').get()
        keywords: List[str] = response.css('.post-categories a::text').getall()
        general = General(title=title, description=description, keyword=keywords)
        technical = Technical(format='text/html', location=response.url)
        yield Schema(general=general, technical=technical)
        # yield technical.to_alfresco() | general.to_alfresco()




