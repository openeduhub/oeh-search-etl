import json

from scrapy.spiders import CrawlSpider
from converter.items import *
from .base_classes import LomBase
from converter.constants import *


class MediothekPixiothekSpider(CrawlSpider, LomBase):
    """
    This crawler fetches data from the Mediothek/Pixiothek. The API request sends all results in one page. The outcome is an JSON array which will be parsed to their elements.

    Author: Timur Yure, timur.yure@capgemini.com , Capgemini for Schul-Cloud, Content team.
    """

    name = "mediothek_pixiothek_spider"
    url = "https://www.schulportal-thueringen.de/"  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = "MediothekPixiothek"  # name as shown in the search ui
    version = "0.1"  # the version of your crawler, used to identify if a reimport is necessary
    start_urls = [
        "https://www.schulportal-thueringen.de/tip-ms/api/public_mediothek_metadatenexport/publicMediendatei"
    ]

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def parse(self, response: scrapy.http.Response):

        # Call Splash only once per page (that contains multiple XML elements).
        data = self.getUrlData(response.url)
        response.meta["rendered_data"] = data
        elements = json.loads(response.body_as_unicode())
        for i, element in enumerate(elements):
            copyResponse = response.copy()

            # Passing the dictionary for easier access to attributes.
            copyResponse.meta["item"] = element

            # In case JSON string representation is preferred:
            json_str = json.dumps(element, indent=4, sort_keys=True, ensure_ascii=False)
            copyResponse._set_body(json_str)
            print(json_str)

            if self.hasChanged(copyResponse):
                yield self.handleEntry(copyResponse)

            # LomBase.parse() has to be called for every individual instance that needs to be saved to the database.
            LomBase.parse(self, copyResponse)

    # def _if_exists_add(self, edu_dict: dict, element_dict: dict, edu_attr: str, element_attr: str):
    #     if element_attr in element_dict:
    #         edu_dict[edu_attr] = element_dict[element_attr]

    def getId(self, response):
        # Element response as a Python dict.
        element_dict = response.meta["item"]

        return element_dict["id"]

    def getHash(self, response):
        # Element response as a Python dict.
        element_dict = response.meta["item"]
        # presentation timestamp (PTS)
        id = element_dict["id"]
        pts = element_dict["pts"]
        # date_object = datetime.strptime(hash, "%Y-%m-%d %H:%M:%S.%f").date()
        return id + pts

    def mapResponse(self, response):
        r = ResponseItemLoader(response=response)
        r.add_value("status", response.status)
        r.add_value("headers", response.headers)
        r.add_value("url", self.getUri(response))
        return r

    def handleEntry(self, response):
        return LomBase.parse(self, response)

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
        license = LomBase.getLicense(self, response)

        # Element response as a Python dict.
        element_dict = response.meta["item"]

        license.replace_value(
            "internal",
            Constants.LICENSE_NONPUBLIC
            if element_dict["oeffentlich"] == "1"
            else Constants.LICENSE_COPYRIGHT_LAW,
        )
        return license

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)

        technical.add_value("format", "text/html")
        technical.add_value("location", self.getUri(response))
        technical.add_value("size", len(response.body))

        return technical

    def is_public(self, element_dict) -> bool:
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
