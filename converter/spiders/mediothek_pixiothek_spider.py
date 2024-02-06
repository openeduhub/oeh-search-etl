import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider

from converter.constants import *
from converter.items import *
from .base_classes import LomBase


class MediothekPixiothekSpider(CrawlSpider, LomBase):
    """
    This crawler fetches data from the Mediothek/Pixiothek. The API request sends all results in one page. The outcome is an JSON array which will be parsed to their elements.

    Author: Timur Yure, timur.yure@capgemini.com , Capgemini for Schul-Cloud, Content team.
    """

    name = "mediothek_pixiothek_spider"
    url = "https://www.schulportal-thueringen.de/"  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = "MediothekPixiothek"  # name as shown in the search ui
    version = "0.1.1"  # last update: 2022-05-09
    start_urls = [
        "https://www.schulportal-thueringen.de/tip-ms/api/public_mediothek_metadatenexport/publicMediendatei"
    ]
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
    }

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    async def parse(self, response: scrapy.http.TextResponse, **kwargs):
        data = self.getUrlData(response.url)
        response.meta["rendered_data"] = data
        # as of Scrapy 2.2 the JSON of a TextResponse can be loaded like this,
        # see: https://doc.scrapy.org/en/latest/topics/request-response.html#scrapy.http.TextResponse.json
        elements = response.json()
        for element in elements:
            copy_response = response.copy()
            # Passing the dictionary for easier access to its attributes.
            copy_response.meta["item"] = element
            yield await LomBase.parse(self, response=copy_response)

    # def _if_exists_add(self, edu_dict: dict, element_dict: dict, edu_attr: str, element_attr: str):
    #     if element_attr in element_dict:
    #         edu_dict[edu_attr] = element_dict[element_attr]

    def getId(self, response) -> str:
        # Element response as a Python dict.
        element_dict: dict = response.meta["item"]
        element_id: str = element_dict["id"]
        return element_id

    def getHash(self, response):
        # Element response as a Python dict.
        element_dict = response.meta["item"]
        element_id = element_dict["id"]
        element_timestamp = element_dict["pts"]
        # presentation timestamp (PTS)
        # date_object = datetime.strptime(hash, "%Y-%m-%d %H:%M:%S.%f").date()
        return element_id + element_timestamp

    def mapResponse(self, response):
        r = ResponseItemLoader(response=response)
        r.add_value("status", response.status)
        r.add_value("headers", response.headers)
        r.add_value("url", self.getUri(response))
        return r

    def getBase(self, response):
        base = LomBase.getBase(self, response)

        # Element response as a Python dict.
        element_dict = response.meta["item"]

        # TODO: "For licensing reasons, this content is only available to users registered in the Thuringian school
        #  portal."
        base.add_value("thumbnail", element_dict["previewImageUrl"])

        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)

        # Element response as a Python dict.
        element_dict = response.meta["item"]

        # TODO: Decide which title. Do we have to construct the title, by concatenating multiple from the provided ones?
        # Einzeltitel, einzeluntertitel, serientitel, serienuntertitel
        general.add_value("title", element_dict["einzeltitel"])
        # self._if_exists_add(general, element_dict, "description", "kurzinhalt")
        if "kurzinhalt" in element_dict:
            general.add_value("description", element_dict["kurzinhalt"])

        liste_stichwort = (
            element_dict["listeStichwort"] if "listeStichwort" in element_dict else None
        )
        if liste_stichwort is not None and len(liste_stichwort) > 0:
            general.add_value("keyword", liste_stichwort)

        return general

    def getUri(self, response):
        # Element response as a Python dict.
        element_dict = response.meta["item"]

        return element_dict["downloadUrl"]

    def getLicense(self, response):
        license_loader = LomBase.getLicense(self, response)

        # Element response as a Python dict.
        element_dict = response.meta["item"]

        license_loader.replace_value(
            "internal",
            Constants.LICENSE_NONPUBLIC
            if element_dict["oeffentlich"] == "1"
            else Constants.LICENSE_COPYRIGHT_LAW,
        )
        return license_loader

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)

        technical.add_value("format", "text/html")
        technical.add_value("location", self.getUri(response))
        technical.add_value("size", len(response.body))

        return technical

    @staticmethod
    def is_public(element_dict) -> bool:
        """
        Temporary solution to check whether the content is public and only save it if this holds.
        """
        return element_dict["oeffentlich"] == "1"

    # TODO: This code snippet will be enabled in the next PR for licensed content, after clarifications are made.
    #
    # def getPermissions(self, response):
    #     """
    #     Licensing information is controlled via the 'oeffentlich' flag. When it is '1' it is available to the public,
    #     otherwise only to Thuringia. Therefore, when the latter happens we set the public to private, and set the groups
    #     and mediacenters accordingly.
    #     """
    #     permissions = LomBase.getPermissions(self, response)
    #
    #     element_dict = response.meta["item"]
    #
    #     if element_dict["oeffentlich"] == "0":  # private
    #         permissions.replace_value('public', False)
    #         permissions.add_value('groups', ['Thuringia'])
    #         permissions.add_value('mediacenters', 'mediothek')  # only 1 mediacenter.
    #
    #     return permissions
