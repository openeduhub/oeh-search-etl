from __future__ import annotations
import scrapy
from converter.constants import Constants
from converter.items import BaseItemLoader, LomClassificationItemLoader, LomGeneralItemloader, LomBaseItemloader, LomLifecycleItemloader, LomTechnicalItemLoader, \
    LicenseItemLoader, PermissionItemLoader, ResponseItemLoader, LomEducationalItemLoader, ValuespaceItemLoader, \
    LomLifecycleItemloader, LomClassificationItemLoader
from converter.util.sitemap import SitemapEntry, from_xml_response
from urllib import parse
from converter.spiders.base_classes import LomBase
from extruct.jsonld import JsonLdExtractor

jslde = JsonLdExtractor()

about_maps = {
    "Lernfeld Gesundheit (LF16)": "Gesundheit",
    "Handlungsfeld Gesellschaft": "Gesellschaftskunde"
}

class FobizzSpider(scrapy.Spider, LomBase):
    """
    scrapes the fobizz website.
    https://plattform.fobizz.com/sitemap
    """

    start_urls = ['https://plattform.fobizz.com/sitemap']
    name = 'fobizz_spider'
    version = '0.0.1'

    def getId(self, response: scrapy.http.Response = None) -> str:
        return parse.urlparse(response.meta["sitemap_entry"].loc).path

    def getHash(self, response: scrapy.http.Response = None) -> str:
        return response.meta["sitemap_entry"].lastmod + self.version

    def parse(self, response: scrapy.http.XmlResponse, **kwargs):
        """
        one url element usually looks like this:
        <url>
            <loc>https://plattform.fobizz.com/unterrichtsmaterialien/81-quiz-zum-thema-wirbeltiere</loc>
            <lastmod>2020-02-24T08:21:04Z</lastmod>
        </url>
        """
        items = from_xml_response(response)
        # yield from items
        for item in items:
            if not item.loc.startswith("https://plattform.fobizz.com/unterrichtsmaterialien/"):
                continue
            # there are some pages in the sitemap which direct to empty pages
            # they contain grade_type oder subject_type in their url
            elif "grade_type" in item.loc:
                continue
            elif "subject_type" in item.loc:
                continue
            if self.hasChanged:
                yield response.follow(item.loc, callback=self.parse_site, cb_kwargs={'sitemap_entry': item})

    def parse_site(self, response: scrapy.http.HtmlResponse, sitemap_entry: SitemapEntry = None):
        # extract the jsonld
        data = jslde.extract(response.text)[0]
        response.meta['sitemap_entry'] = sitemap_entry
        base = super().getBase(response=response)
        base.add_value("response", super().mapResponse(response).load_item())
        # we assume that content is imported. Please use replace_value if you import something different
        base.add_value("type", Constants.TYPE_MATERIAL)
        base.add_value('thumbnail', data.get("thumbnailUrl", None))
        base.add_value('lastModified', data.get("dateModified", None))
        for publisher in data.get("publisher", []):
            # TODO add type, e.g. organization
            base.add_value("publisher", publisher.get("name"))

        lom = LomBaseItemloader()
        general = LomGeneralItemloader(response=response)
        general.add_value('title', data.get("name", None))
        general.add_value('description', data.get("description", None))
        general.add_value("identifier", data.get("identifier", None))
        for language in data.get("language", []):
            general.add_value("language", language)
        lom.add_value("general", general.load_item())

        technical = LomTechnicalItemLoader()
        technical.add_value('format', 'text/html')
        technical.add_value('location', sitemap_entry.loc)
        lom.add_value("technical", technical.load_item())

        lifecycle = LomLifecycleItemloader()
        lom.add_value("lifecycle", lifecycle.load_item())
        edu = LomEducationalItemLoader()
        lom.add_value("educational", edu.load_item())
        # classification = LomClassificationItemLoader()
        # lom.add_value("classification", classification.load_item())
        base.add_value("lom", lom.load_item())

        vs = ValuespaceItemLoader()
        for audience in data.get("audience", []):
            vs.add_value("intendedEndUserRole", audience)

        for discipline in (d.strip() for d in data.get("about", []).split(",")):
            if discipline in about_maps.keys():
                discipline = about_maps[discipline]
            vs.add_value('discipline', discipline)

        for lrt in data.get("type", []):
            vs.add_value('learningResourceType', lrt)
        base.add_value("valuespaces", vs.load_item())

        lic = LicenseItemLoader()
        lic.add_value('url', data.get("license", None))
        for creator in data.get("creator", []):
            lic.add_value("author", creator.get("name", ""))
        
        base.add_value("license", lic.load_item())
        
        permissions = super().getPermissions(response)

        base.add_value("permissions", permissions.load_item())
        response_loader = ResponseItemLoader()
        response_loader.add_value('url', response.url)
        base.add_value("response", response_loader.load_item())
        yield base.load_item()


