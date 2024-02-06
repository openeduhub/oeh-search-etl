from datetime import datetime

import xmltodict as xmltodict
from lxml import etree
from scrapy.spiders import CrawlSpider
from converter.items import *
from .base_classes import LomBase
import scrapy


class MerlinSpider(CrawlSpider, LomBase):
    """
    This crawler fetches data from the Merlin content source, which provides us paginated XML data. For every element
    in the returned XML array we call LomBase.parse(), which in return calls methods, such as getId(), getBase() etc.

    Author: Ioannis Koumarelas, ioannis.koumarelas@hpi.de, Schul-Cloud, Content team.
    """

    name = "merlin_spider"
    url = "https://merlin.nibis.de/index.php"  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = "Merlin"  # name as shown in the search ui
    version = "0.1"  # the version of your crawler, used to identify if a reimport is necessary
    apiUrl = "https://merlin.nibis.de/index.php?action=resultXml&start=%start&anzahl=%anzahl&query[stichwort]=*"  # * regular expression, to represent all possible values.

    limit = 100
    page = 0

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self):
        yield scrapy.Request(
            url=self.apiUrl.replace("%start", str(self.page * self.limit)).replace(
                "%anzahl", str(self.limit)
            ),
            callback=self.parse,
            headers={"Accept": "application/xml", "Content-Type": "application/xml"},
        )

    async def parse(self, response: scrapy.http.Response):
        print("Parsing URL: " + response.url)

        # Call Splash only once per page (that contains multiple XML elements).
        data = self.getUrlData(response.url)
        response.meta["rendered_data"] = data

        # We would use .fromstring(response.text) if the response did not include the XML declaration:
        # <?xml version="1.0" encoding="utf-8"?>
        root = etree.XML(response.body)
        tree = etree.ElementTree(root)

        # If results are returned.
        elements = tree.xpath("/root/items/*")
        if len(elements) > 0:
            for element in elements:
                copyResponse = response.copy()
                element_xml_str = etree.tostring(
                    element, pretty_print=True, encoding="unicode"
                )
                element_dict = xmltodict.parse(element_xml_str)

                # Temporary solution for public-only content.
                # TODO: remove this when licensed content are enabled!
                if not self.is_public(element_dict["data"]):
                    continue

                # TODO: It's probably a pointless attribute.
                # del element_dict["data"]["score"]

                # Passing the dictionary for easier access to attributes.
                copyResponse.meta["item"] = element_dict["data"]

                # In case JSON string representation is preferred:
                # copyResponse._set_body(json.dumps(copyResponse.meta['item'], indent=1, ensure_ascii=False))
                copyResponse._set_body(element_xml_str)

                if self.hasChanged(copyResponse):
                    yield self.handleEntry(copyResponse)

                # LomBase.parse() has to be called for every individual instance that needs to be saved to the database.
                await LomBase.parse(self, copyResponse)

        # TODO: To not stress the Rest APIs.
        # time.sleep(0.1)

        # If the number of returned results is equal to the imposed limit, it means that there are more to be returned.
        if len(elements) == self.limit:
            self.page += 1
            url = self.apiUrl.replace("%start", str(self.page * self.limit)).replace(
                "%anzahl", str(self.limit)
            )
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers={
                    "Accept": "application/xml",
                    "Content-Type": "application/xml",
                },
            )

    def getId(self, response):
        return response.xpath("/data/id_local/text()").get()

    def getHash(self, response):
        """ Since we have no 'last_modified' date from the elements we cannot do something better.
            Therefore, the current implementation takes into account (1) the code version, (2) the item's ID, and (3)
            the date (day, month, year). """
        return (
            hash(self.version)
            + hash(self.getId(response))
            + self._date_to_integer(datetime.date(datetime.now()))
        )

    def _date_to_integer(self, dt_time):
        """ Converting the date to an integer, so it is useful in the getHash method
            Using prime numbers for less collisions. """
        return 9973 * dt_time.year + 97 * dt_time.month + dt_time.day

    def mapResponse(self, response):
        r = ResponseItemLoader(response=response)
        r.add_value("status", response.status)
        r.add_value("headers", response.headers)
        r.add_value("url", self.getUri(response))
        return r

    async def handleEntry(self, response):
        return await LomBase.parse(self, response)

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        base.add_value("thumbnail", response.xpath("/data/thumbnail/text()").get())

        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("title", response.xpath("/data/titel/text()").get())
        general.add_value(
            "description", response.xpath("/data/beschreibung/text()").get()
        )

        return general

    def getUri(self, response):
        location = response.xpath("/data/media_url/text()").get()
        return "http://merlin.nibis.de" + location

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)

        technical.add_value("format", "text/html")
        technical.add_value("location", self.getUri(response))
        technical.add_value("size", len(response.body))

        return technical

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)

        bildungsebene = response.xpath("/data/bildungsebene/text()").get()
        if bildungsebene is not None:
            valuespaces.add_value("intendedEndUserRole", bildungsebene.split(";"))

        # Use the dictionary when it is easier.
        element_dict = response.meta["item"]

        if len(response.xpath("/data/fach/*")) > 0:
            element_dict = response.meta["item"]
            discipline = list(element_dict["fach"].values())[0]
            valuespaces.add_value("discipline", discipline)

        # Consider https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/learningResourceType/index.html
        ressource = element_dict["ressource"] if "ressource" in element_dict else None
        if ressource is not None and len(ressource) > 0:
            if "data" in element_dict["ressource"]:
                resource_types = element_dict["ressource"]["data"]
                if isinstance(resource_types, str):
                    resource_types = [resource_types]
            else:
                resource_types = element_dict["ressource"].values()

            # Convert non-LOM (not known to OEH) resource types, to LOM resource types.
            merlin_to_oeh_types = {
                "Film": "video",
                "Menü": "Menu",
                "Weiteres_Material": "Anderes Material",
                "Diagramm": "Veranschaulichung",
            }
            resource_types = [
                merlin_to_oeh_types[rt] if rt in merlin_to_oeh_types else rt.lower()
                for rt in resource_types
            ]

            valuespaces.add_value("learningResourceType", resource_types)
        return valuespaces

    def is_public(self, element_dict) -> bool:
        """
        Temporary solution to check whether the content is public and only save it if this holds.
        """
        return not (
            element_dict["kreis_id"] is not None and len(element_dict["kreis_id"]) > 0
        )

    # TODO: This code snippet will be enabled in the next PR for licensed content, after clarifications are made.
    #
    # def getPermissions(self, response):
    #     """
    #     In case license information, in the form of Kreis codes, is available. This changes the permissions from
    #     public to private and sets accordingly the groups and mediacenters. For more information regarding the available
    #     Merlin kreis codes please consult 'http://merlin.nibis.de/index.php?action=kreise'
    #     """
    #
    #     permissions = LomBase.getPermissions(self, response)
    #
    #     element_dict = response.meta["item"]
    #
    #     if element_dict["kreis_id"] is not None and len(element_dict["kreis_id"]) > 0:  # private
    #         kreis_ids = element_dict["kreis_id"]["data"]  # ... redundant extra nested dictionary "data"...
    #         if not isinstance(kreis_ids, list):  # one element
    #             kreis_ids = [kreis_ids]
    #         kreis_ids = sorted(kreis_ids, key=lambda x: int(x))
    #         kreis_ids = ["merlin_" + id for id in kreis_ids]  # add prefix
    #
    #         permissions.replace_value('public', False)
    #         permissions.add_value('groups', ['Lower Saxony'])
    #         permissions.add_value('mediacenters', kreis_ids)
    #
    #     return permissions
