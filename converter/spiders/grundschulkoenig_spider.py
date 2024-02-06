import re

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import BaseItemLoader, LomBaseItemloader, LomGeneralItemloader, LomTechnicalItemLoader, \
    LomEducationalItemLoader, ValuespaceItemLoader, LicenseItemLoader, LomLifecycleItemloader, \
    LomClassificationItemLoader
from converter.spiders.base_classes import LomBase
from converter.util.sitemap import from_xml_response, SitemapEntry


class GrundSchulKoenigSpider(CrawlSpider, LomBase):
    """
    scrapes the Grundschulkönig website.
    """

    start_urls = ['https://www.grundschulkoenig.de/sitemap.xml?sitemap=pages&cHash=b8e1a6633393d69093d0ebe93a3d2616']
    name = 'grundschulkoenig_spider'
    version = "0.0.7"  # last update: 2022-08-26
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        # while there is no robots.txt, there is a 404-forward-page that gets misinterpreted by Scrapy
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_DEBUG": True
    }

    excluded_url_paths = ["/404-page-not-found/",
                          "/blog/",
                          "/footer-bottom/",
                          "/rechtliches/",
                          "/suche/",
                          ]
    excluded_overview_pages = [
        "https://www.grundschulkoenig.de/",
        "https://www.grundschulkoenig.de/deutsch/",
        "https://www.grundschulkoenig.de/deutsch/deutsch-als-fremdsprache/",
        "https://www.grundschulkoenig.de/englisch/",
        "https://www.grundschulkoenig.de/globale-elemente/",
        "https://www.grundschulkoenig.de/hsu-sachkunde/",
        "https://www.grundschulkoenig.de/landing/",
        "https://www.grundschulkoenig.de/links/",
        "https://www.grundschulkoenig.de/mehr/",
        "https://www.grundschulkoenig.de/mehr/jahreskreis/",
        "https://www.grundschulkoenig.de/mathe/",
        "https://www.grundschulkoenig.de/musikkunst/kunst/",
        "https://www.grundschulkoenig.de/musikkunst/musik/",
        "https://www.grundschulkoenig.de/newsletter-abonnieren/",
        "https://www.grundschulkoenig.de/religion/",
        "https://www.grundschulkoenig.de/suchergebnisse/",
        "https://www.grundschulkoenig.de/vorschule/",
        "https://www.grundschulkoenig.de/weitere-faecher/",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_sitemap)

    def getHash(self, response=None) -> str:
        pass

    def getId(self, response=None) -> str:
        pass

    def parse_sitemap(self, response: scrapy.http.XmlResponse):
        """
        one url element usually looks like this::

            <url>
                <loc>https://www.grundschulkoenig.de/mathe/1-klasse/zahlenraum-10/</loc>
                <lastmod>2021-02-03T11:44:34+01:00</lastmod>
                    <priority>0.5</priority>
            </url>

        Scrapy Contracts:
        @url https://www.grundschulkoenig.de/sitemap.xml?sitemap=pages&cHash=06e4f67db47c88d09df2534dfa2ab810
        @returns requests 100
        """

        items = from_xml_response(response)
        for item in items:
            response = response.copy()
            response.meta['sitemap_entry'] = item
            skip_url = False
            for full_url in self.excluded_overview_pages:
                # We don't want to parse the overview pages, but only the specific topic-pages
                full_url_regex = re.compile(full_url)
                if full_url_regex.fullmatch(item.loc) is not None:
                    skip_url = True
                    break
            if skip_url is False:
                # in case the URL is already marked as to-be-skipped, we can skip this additional check
                for url_pattern in self.excluded_url_paths:
                    current_page_regex = re.compile(url_pattern)
                    if current_page_regex.search(item.loc) is not None:
                        skip_url = True
                        break
            if skip_url is False:
                yield response.follow(item.loc, callback=self.parse, cb_kwargs={'sitemap_entry': item})

    async def parse(self, response: scrapy.http.HtmlResponse, sitemap_entry: SitemapEntry = None):
        title = response.xpath('//span[@class="nav__crumb nav__crumb--current"]/span/text()').get()
        # content = response.xpath('//div[@class="page__content"]')
        # Worksheets are grouped, sometimes several worksheet-containers per page exist
        # worksheet_containers = response.xpath('//div[@class="module-worksheet"]')
        # the worksheet_containers hold the links to individual worksheet .pdf files

        base = BaseItemLoader(response=response)
        base.add_value("sourceId", response.url)
        hash_temp = str(sitemap_entry.lastmod + self.version)
        base.add_value("hash", hash_temp)
        thumbnail_url = response.xpath('//meta[@property="og:image"]/@content').get()
        if thumbnail_url is not None:
            base.add_value('thumbnail', thumbnail_url)
        base.add_value('lastModified', sitemap_entry.lastmod)
        lom = LomBaseItemloader()
        general = LomGeneralItemloader(response=response)
        general.add_value('title', title)
        description = response.xpath('//div[@class="content-item module-headline-paragraph"]/p/text()').get()
        # due to the generic descriptions of grundschulkoenig used in the headers, we're using the first paragraph
        # as our description instead. Only if this XPath is somehow unavailable, we're falling back to the actual header
        if description is None:
            description: str = response.xpath('//meta[@name="description"]/@content').get()
        general.add_value('description', description)
        # ToDo: check if "keywords" are available at the source when the next crawler update becomes necessary
        lom.add_value("general", general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value('format', 'text/html')
        technical.add_value('location', sitemap_entry.loc)
        lom.add_value("technical", technical.load_item())

        lifecycle = LomLifecycleItemloader()
        lifecycle.add_value('role', "publisher")
        lifecycle.add_value('url', "https://www.grundschulkoenig.de/rechtliches/impressum/")
        lifecycle.add_value('email', "kontakt@grundschulkoenig.de")
        lifecycle.add_value('organization', "Grundschulkönig GmbH")
        lom.add_value("lifecycle", lifecycle.load_item())

        edu = LomEducationalItemLoader()
        lom.add_value("educational", edu.load_item())

        classification = LomClassificationItemLoader()
        # competency description covers "Lernziele" and "Aufgaben" of the individual materials,
        # not necessarily available for every crawled item
        competency_description: list = response.xpath(
            '//div[@class="aims__aim"]/span[@class="aim__bodytext"]/ul/li/text()').getall()
        if len(competency_description) > 0:
            # if there's no competency_description available, don't bother saving the empty list
            classification.add_value('description', competency_description)
        lom.add_value("classification", classification.load_item())

        base.add_value("lom", lom.load_item())

        vs = ValuespaceItemLoader()
        vs.add_value('conditionsOfAccess', 'no_login')
        vs.add_value('containsAdvertisement', 'yes')
        vs.add_value('price', "yes_for_additional")
        vs.add_value('accessibilitySummary', 'none')
        # Datenschutzerklaerung -> https://www.grundschulkoenig.de/rechtliches/datenschutzerklaerung/
        vs.add_value('dataProtectionConformity', 'noGeneralDataProtectionRegulation')
        vs.add_value('intendedEndUserRole', ["teacher", "learner", "parent"])
        if "/deutsch/" in response.url:
            vs.add_value('discipline', 'Deutsch')
        if "/englisch/" in response.url:
            vs.add_value('discipline', 'Englisch')
        if "/hsu-sachkunde/" in response.url:
            vs.add_value('discipline', 'Sachunterricht')
        if "/mathe/" in response.url:
            vs.add_value('discipline', "Mathematik")
        if "/musikkunst/musik/" in response.url:
            vs.add_value('discipline', "Musik")
        if "/musikkunst/kunst/" in response.url:
            vs.add_value('discipline', "Kunst")
        if "/religion/" in response.url:
            vs.add_value('discipline', "Religionsunterricht")
        vs.add_value('discipline', 'Allgemein')
        vs.add_value('educationalContext', 'Primarstufe')
        # vs.add_value('learningResourceType', 'other_asset_type')
        # ToDo: new_lrt
        if "/vorschule/" in response.url:
            vs.add_value('educationalContext', "Elementarbereich")
            vs.add_value('new_lrt', "65330f23-2802-4789-86ee-c21f9afe74b1")  # "Frühkindliches Bildungsangebot und KITA"
        vs.add_value('new_lrt', ["5098cf0b-1c12-4a1b-a6d3-b3f29621e11d",
                                 "d8c3ef03-b3ab-4a5e-bcc9-5a546fefa2e9",
                                 "36e68792-6159-481d-a97b-2c00901f4f78"])
        # "Unterrichtsbaustein", "Webseite und Portal (stabil), "Arbeitsblatt"
        base.add_value("valuespaces", vs.load_item())

        lic = LicenseItemLoader()
        lic.add_value('internal', Constants.LICENSE_COPYRIGHT_LAW)
        base.add_value("license", lic.load_item())

        permissions = super().getPermissions(response)
        base.add_value("permissions", permissions.load_item())

        response_loader = await super().mapResponse(response)
        base.add_value('response', response_loader.load_item())

        yield base.load_item()
