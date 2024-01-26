from __future__ import annotations

import re

import scrapy
import w3lib.html

from converter.constants import Constants
from converter.items import LomGeneralItemloader, LomBaseItemloader, LomTechnicalItemLoader, \
    LicenseItemLoader, ResponseItemLoader, LomEducationalItemLoader, ValuespaceItemLoader, BaseItem
from converter.spiders.base_classes import LomBase
from converter.util.sitemap import SitemapEntry, from_xml_response


class KindoergartenSpider(scrapy.Spider, LomBase):
    """
    scrapes the kindOERgarten wordpress.
    this wordpress instance has no json api enabled, so we go by sitemap
    https://kindoergarten.wordpress.com/sitemap.xml
    """

    start_urls = ['https://kindoergarten.wordpress.com/sitemap.xml']
    name = 'kindoergarten_spider'
    version = '0.1.4'   # last update: 2022-04-14
    skip_these_urls = [
        '/impressum/',
        '/nutzungsbedingungen/',
        '/robin-hood-prinzip/',
        '/sponsor-wie/',
        '/fachredaktion-und-produktion/',
        '/category/ueber-kindoergarten/'
    ]

    def getId(self, response: scrapy.http.Response = None) -> str:
        return response.url

    def getHash(self, response: scrapy.http.Response = None) -> str:
        return response.meta["sitemap_entry"].lastmod + self.version

    def parse(self, response: scrapy.http.XmlResponse, **kwargs):
        """
        parse XML sitemap for items and afterwards follow individual items by their item.loc (url)
        with a callback to parse_site

        Scrapy Contracts:
        @url https://kindoergarten.wordpress.com/sitemap.xml
        @returns requests 105
        """
        # one url element usually looks like this:
        # <url>
        #     <loc>https://kindoergarten.wordpress.com/2018/07/30/buchstabe-k-0095/</loc>
        #     <image:image>
        #       <image:loc>https://kindoergarten.files.wordpress.com/2018/05/ankucc88ndigung_buchstabenk.jpg</image:loc>
        #       <image:title>ankündigung_buchstabenK</image:title>
        #     </image:image>
        #     <lastmod>2018-05-29T21:12:41+00:00</lastmod>
        #     <changefreq>monthly</changefreq>
        #   </url>

        items = from_xml_response(response)
        for item in items:
            response = response.copy()
            response.meta['sitemap_entry'] = item
            # if url is on the undesired urls list, skip parsing the current item
            skip_check = False
            for url_pattern in self.skip_these_urls:
                current_regex = re.compile(url_pattern)
                if current_regex.search(item.loc) is not None:
                    skip_check = True
                    break
            # only if the current url doesn't appear in the skip_these_urls list, the parse request will be triggered
            if self.hasChanged(response) and skip_check is False:
                yield response.follow(item.loc, callback=self.parse_site, cb_kwargs={'sitemap_entry': item})

    async def parse_site(self, response: scrapy.http.HtmlResponse, sitemap_entry: SitemapEntry = None) -> BaseItem:
        """
        parses metadata from an individual item both by its HtmlResponse and its sitemap tags

        :param response: the current scrapy.http.HtmlResponse (needed for xpath and css selectors)
        :param sitemap_entry: a copy of the original sitemap entry for this item
        :return: yields a BaseItemLoader
        """
        response.meta['sitemap_entry'] = sitemap_entry
        base = super().getBase(response=response)
        response_itemloader: ResponseItemLoader = await super().mapResponse(response)
        base.add_value("response", response_itemloader.load_item())
        # we assume that content is imported. Please use replace_value if you import something different
        # thumbnail_href = response.css('.post-thumbnail img::attr(src)').get()
        base.add_value('thumbnail', response.css('.post-thumbnail img::attr(src)').get())
        base.add_value('lastModified', sitemap_entry.lastmod)

        lom = LomBaseItemloader()
        general = LomGeneralItemloader(response=response)
        # the CSS Selector for 7 items was sometimes empty, which caused the pipeline to drop the whole item
        # this if-condition should always grab a title
        title = response.css('.entry-title span::text').get()
        if title is not None:
            general.add_value('title', response.css('.entry-title span::text').get())
        if title is None:
            general.add_value('title', response.xpath('//*[@class="entry-title"]/text()').get())

        content = response.css('.entry-content')
        # remove the sharedaddy-buttons before parsing the description text
        content.css('.sharedaddy').remove()
        # TODO: attach pdf links (if available) to new items.py ItemLoader for deep-links (not yet implemented)
        # pdf_links = content.css('ul li a::attr(href)').getall()
        description_temp = content.xpath('//*[@class="entry-content"]//descendant::*/text()').getall()
        raw_description = str()
        raw_description = raw_description.join(description_temp)

        # hacky, alternative method without removing the "sharedaddy"-container:
        #   even though the <div id="jp-post-flair">-container is completely separate from the "entry-content"-div
        #   it will grab the share-button descriptions. As a workaround, we're grabbing all descriptions, but manually
        #   break the loop as soon as we reach the "Teilen mit:"-String
        # raw_description = str()
        # for item in description_temp:
        #     if item.get() == "Teilen mit:":
        #         break
        #     raw_description += item.get()

        raw_description = w3lib.html.remove_tags(raw_description)
        general.add_value('description', raw_description)

        general.add_value('keyword', response.css('.post-categories a::text').getall())
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
        vs.add_value('intendedEndUserRole', 'teacher')
        vs.add_value('discipline', 'Allgemein')
        vs.add_value('educationalContext', 'Elementarbereich')
        # vs.add_value('toolCategory', 'noGeneralDataProtectionRegulation')
        # ToDo: remove old learningResourceType code when reaching crawler v0.1.4
        # vs.add_value('learningResourceType', 'other_asset_type')
        vs.add_value('new_lrt', "65330f23-2802-4789-86ee-c21f9afe74b1")
        # default for all scrapy items: "Frühkindliches Bildungsangebot und KITA", "Lehr- und Lernmaterial"
        if "arbeitsblatt" in response.url:
            vs.add_value('new_lrt', "36e68792-6159-481d-a97b-2c00901f4f78")  # "Arbeitsblatt"
        if "spiel" in response.url or "wuerfelblatt" in response.url:
            vs.add_value('new_lrt', "b0495f44-b05d-4bde-9dc5-34d7b5234d76")  # "Lernspiel"
        if "malvorlage" in response.url:
            vs.add_value('new_lrt', "39db0dbd-cb6f-4153-910f-9f11177b48f2")  # "Mal- und Bastelvorlage"
        base.add_value("valuespaces", vs.load_item())

        lic = LicenseItemLoader()
        lic.add_value('url', Constants.LICENSE_CC_ZERO_10)
        base.add_value("license", lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader = ResponseItemLoader()
        response_loader.add_value('url', response.url)
        base.add_value("response", response_loader.load_item())

        yield base.load_item()
