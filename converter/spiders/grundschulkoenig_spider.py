from __future__ import annotations

from collections import defaultdict

import scrapy
from dataclasses import dataclass, field
from converter.spiders.base_classes.meta_base import SpiderBase
from typing import Optional, List, Dict, Tuple
from converter.dc_items.lom import General, Technical, Schema
from converter.util.sitemap import from_xml_response, SitemapEntry
from urllib.parse import urlparse
from pathlib import PurePosixPath


class GrundSchulKoenigSpider(scrapy.Spider, metaclass=SpiderBase):
    """
    scrapes the Grundschulkönig website.

    .. todo::

       contains Advertisements
    """
    start_urls = ['https://www.grundschulkoenig.de/sitemap.xml?sitemap=pages&cHash=06e4f67db47c88d09df2534dfa2ab810']
    excluded_paths = [
        'brandenburg-ferien-feiertage-brueckentage',
        'schulferien-feiertage-brueckentage',
        'sachsen-anhalt-ferien-feiertage-brueckentage',
        'rheinland-pfalz-ferien-feiertage-brueckentage',
        'nordrhein-westfalen-ferien-feiertage-brueckentage',
        'mecklenburg-vorpommern-ferien-feiertage-brueckentage',
        'niedersachen-ferien-feiertage-brueckentage',
        'schleswig-holstein-ferien-feiertage-brueckentage',
        'hamburg-ferien-feiertage-brueckentage',
        'bremen-ferien-feiertage-brueckentage',
        'thueringen-ferien-feiertage-brueckentage',
        'berlin-ferien-feiertage-brueckentage',
        'sachsen-ferien-feiertage-brueckentage',
        'saarland-ferien-feiertage-brueckentage',
        'hessen-ferien-feiertage-brueckentage',
        'baden-wuerttemberg-ferien-feiertage-brueckentage',
        'bayern-ferien-feiertage-brueckentage',
        '404-page-not-found',
        'landing',
        'mehr',
    ]
    name = 'grundschulkoenig_spider'

    def parse(self, response: scrapy.http.XmlResponse, **kwargs):
        """
        one url element usually looks like this::

            <url>
                <loc>https://www.grundschulkoenig.de/mathe/1-klasse/zahlenraum-10/</loc>
                <lastmod>2021-02-03T11:44:34+01:00</lastmod>
                    <priority>0.5</priority>
            </url>
        """
        paths_by_depth: Dict[int, List[Tuple[PurePosixPath, SitemapEntry, Dict]]] = defaultdict(list)
        items = from_xml_response(response)
        for item in items:
            path = PurePosixPath(urlparse(item.loc).path)
            # PurePosixPath('/englisch/sports-sport').parts == ('/', 'englisch', 'sports-sport')
            if path.parts[1] in self.excluded_paths:
                # ignore
                continue
            path_depth = len(path.parts)
            children = defaultdict(list)
            paths_by_depth[path_depth].append((path, item, children))

            # yield response.follow(item.loc, callback=self.parse_site, cb_kwargs={'sitemap_entry': item})

        root = paths_by_depth[1][0]
        print(list(sorted(paths_by_depth)))
        print(root)
        for path, item, children in paths_by_depth[2]:
            # sub categories
            if path.parts[1] not in self.excluded_paths:
                print(f"'{path.parts[1]}',")

            pass
        for depth in sorted(paths_by_depth):
            if depth == 1:
                # root is here
                continue
            if depth != 2:
                continue



    def parse_site(self, response: scrapy.http.HtmlResponse, sitemap_entry: SitemapEntry = None):
        # content = response.css('.entry-content')
        # content.css('.sharedaddy').remove()
        # pdf_links = content.css('ul li a').getall()
        # description = content.css('p::text').get()
        # thumbnail_href = response.css('.post-thumbnail img::attr(src)').get()
        # title: str = response.css('.entry-title span::text').get()
        # description: str = content.css('.entry-content p::text').get()
        # keywords: List[str] = response.css('.post-categories a::text').getall()
        # general = General(title=title, description=description, keyword=keywords)
        # technical = Technical(format='text/html', location=response.url)
        # yield Schema(general=general, technical=technical)
        # yield technical.to_alfresco() | general.to_alfresco()
        pass



