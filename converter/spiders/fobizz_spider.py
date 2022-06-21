from __future__ import annotations

from urllib import parse

import scrapy
from extruct.jsonld import JsonLdExtractor

from converter.constants import Constants
from converter.items import LomGeneralItemloader, LomBaseItemloader, LomTechnicalItemLoader, \
    LicenseItemLoader, ResponseItemLoader, LomEducationalItemLoader, ValuespaceItemLoader, \
    LomLifecycleItemloader
from converter.spiders.base_classes import LomBase
from converter.util.sitemap import SitemapEntry, from_xml_response

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
    version = '0.0.2'  # last update: 2022-05-23

    overview_pages_without_a_json_ld = [
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Religion",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Economy",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Biology",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Ethics",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Philosophie",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Geographie",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/History",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Politics",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Other",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Media",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Computer%20Science",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Sport",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Art",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Natural%20Sciences",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Technology",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Personal%20Education",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Physics",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Chemistry",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Englisch",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Unspecified",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/German",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Foreign%20Languages",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Music",
        "https://plattform.fobizz.com/unterrichtsmaterialien/faecher/Math",
        "https://plattform.fobizz.com/unterrichtsmaterialien/klassenstufen/Other",
        "https://plattform.fobizz.com/unterrichtsmaterialien/klassenstufen/Lower%20Grade",
        "https://plattform.fobizz.com/unterrichtsmaterialien/klassenstufen/Upper%20School",
        "https://plattform.fobizz.com/unterrichtsmaterialien/klassenstufen/Middle%20Level",
        "https://plattform.fobizz.com/unterrichtsmaterialien/klassenstufen/Elementary%20School",
        "https://plattform.fobizz.com/unterrichtsmaterialien/klassenstufen/Special%20School",
        "https://plattform.fobizz.com/unterrichtsmaterialien/klassenstufen/Vocational%20School"
    ]

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
            if item.loc in self.overview_pages_without_a_json_ld:
                # there are 31 overview-pages that don't hold a json_ld, therefore can't be parsed
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
        vs.add_value('new_lrt', Constants.NEW_LRT_MATERIAL)
        for audience in data.get("audience", []):
            vs.add_value("intendedEndUserRole", audience)

        for discipline in (d.strip() for d in data.get("about", []).split(",")):
            if discipline in about_maps.keys():
                discipline = about_maps[discipline]
            vs.add_value('discipline', discipline)

        for lrt in data.get("type", []):
            vs.add_value('new_lrt', lrt)
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
