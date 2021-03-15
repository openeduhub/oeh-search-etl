from __future__ import annotations

from collections import defaultdict
from urllib import parse

import scrapy
from dataclasses import dataclass, field

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, PermissionItemLoader, ResponseItemLoader
from typing import Optional, List, Dict, Tuple, Set
from converter.dc_items.lom import General, Technical, Schema
from converter.util.sitemap import from_xml_response, SitemapEntry
from urllib.parse import urlparse
from pathlib import PurePosixPath


class GrundSchulKoenigSpider(scrapy.Spider):
    """
    scrapes the Grundschulkönig website.

    .. todo::

       contains Advertisements
    """
    start_urls = ['https://www.grundschulkoenig.de/sitemap.xml?sitemap=pages&cHash=06e4f67db47c88d09df2534dfa2ab810']
    name = 'grundschulkoenig_spider'
    excluded = ['blog']

    def parse(self, response: scrapy.http.XmlResponse, **kwargs):
        """
        one url element usually looks like this::

            <url>
                <loc>https://www.grundschulkoenig.de/mathe/1-klasse/zahlenraum-10/</loc>
                <lastmod>2021-02-03T11:44:34+01:00</lastmod>
                    <priority>0.5</priority>
            </url>
        """
        paths_by_depth: Dict[int, List[Tuple[PurePosixPath, SitemapEntry]]] = defaultdict(list)
        items = from_xml_response(response)
        for item in items:
            path = PurePosixPath(urlparse(item.loc).path)
            path_depth = len(path.parts)
            if path_depth == 1:
                continue  # root: ignore
            if path.parts[1] in self.excluded:
                continue  # ignore
            if path.parts[1].endswith('brueckentage'):
                continue  # ignore holiday listing pages
            paths_by_depth[path_depth].append((path, item))

            # yield response.follow(item.loc, callback=self.parse_site, cb_kwargs={'sitemap_entry': item})
        print(list(sorted(paths_by_depth)))
        rev_idx = list(reversed(sorted(paths_by_depth.keys())))
        for child_depth, parent_depth in zip(rev_idx[:-1], rev_idx[1:]): # (5,4),(4,3),(3,2)
            # start at the leaves and the remove their parents
            parents_to_keep: List[Tuple[PurePosixPath, SitemapEntry]] = []
            parents_to_remove: Set[PurePosixPath] = set()
            for path, entry in paths_by_depth[child_depth]:
                parents_to_remove.add(path.parent)
                yield response.follow(entry.loc, callback=self.parse_site, cb_kwargs={'sitemap_entry': entry})
            for path, entry in paths_by_depth[parent_depth]:
                if path in parents_to_remove:
                    continue
                parents_to_keep.append((path, entry))
            paths_by_depth[parent_depth] = parents_to_keep


    def parse_site(self, response: scrapy.http.HtmlResponse, sitemap_entry: SitemapEntry = None):
        # sollte wenigstens eine instanz von .css('.worksheet__content') enthalten, damit sicher ist, dass auch wirklich content da ist.
        content = response.css('.page__content')
        if 0 == len(content):
            return
        # >>> content.css('.module-breadcrumb')[0]
        crumbs = []  # after loop: ['Home', 'Deutsch', '1. Klasse', 'Abschreibtexte']
        for crumb in content.css('.nav__crumb'):
            crumbs.append(crumb.css('span::text').get())

        assert crumbs[0] == 'Home'
        title = crumbs[-1]
        worksheet_containers = content.css('.col-wrapper .module-worksheet').pop()

        if 0 == len(response.css('.worksheet__content').getall()):
            # keine Arbeitsblätter auf der webseite
            return

        base = BaseItemLoader(response=response)
        base.add_value("sourceId", parse.urlparse(sitemap_entry.loc).path)  # id der Seite
        base.add_value("hash", sitemap_entry.lastmod)  # version/Datum der Seite
        # we assume that content is imported. Please use replace_value if you import something different
        base.add_value("type", Constants.TYPE_MATERIAL)
        # base.add_css('thumbnail', '.post-thumbnail img::attr(src)')
        base.add_value('lastModified', sitemap_entry.lastmod)
        lom = LomBaseItemloader()
        general = LomGeneralItemloader(response=response)
        general.add_css('title', 'h1.-color-secondary-beta')
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
        vs.add_value('conditionsOfAccess', 'no_login')
        vs.add_value('containsAdvertisement', 'yes')
        vs.add_value('price', 'no')
        vs.add_value('accessibilitySummary', 'none')
        vs.add_value('dataProtectionConformity', 'noGeneralDataProtectionRegulation')
        vs.add_value('fskRating', '0')
        vs.add_value('oer', '0')
        vs.add_value('intendedEndUserRole', 'teacher')
        vs.add_value('discipline', '720')  # allgemein
        vs.add_value('educationalContext', 'elementarbereich')
        vs.add_value('sourceContentType', '004')  # Material/Aufgabensammlung
        # vs.add_value('toolCategory', 'noGeneralDataProtectionRegulation')
        vs.add_value('learningResourceType', 'other_asset_type')

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



