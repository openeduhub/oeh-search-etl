from datetime import datetime

import xmltodict as xmltodict
from lxml import etree
from scrapy.spiders import CrawlSpider
from converter.items import *
from converter.spiders.lom_base import LomBase


class MerlinSpider(CrawlSpider, LomBase):
    """
    This crawler fetches data from the Merlin content source, which provides us paginated XML data. For every element
    in the returned XML array we call LomBase.parse(), which in return calls methods, such as getId(), getBase() etc.

    Author: Ioannis Koumarelas, ioannis.koumarelas@hpi.de, Schul-Cloud, Content team.
    """
    name = 'merlin_spider'
    url = 'http://merlin.nibis.de/index.php'  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = 'Merlin'  # name as shown in the search ui
    version = '0.1'  # the version of your crawler, used to identify if a reimport is necessary
    apiUrl = 'http://merlin.nibis.de/index.php?action=resultXml&start=%start&anzahl=%anzahl&query[stichwort]=*'     # * regular expression, to represent all possible values.

    limit = 100
    page = 0

    def start_requests(self):
        yield scrapy.Request(url=self.apiUrl.replace('%start', str(self.page * self.limit))
                              .replace('%anzahl', str(self.limit)),
                              callback=self.parse, headers={
                'Accept': 'application/xml',
                'Content-Type': 'application/xml'
            })

    def parse(self, response: scrapy.http.Response):
        print("Parsing URL: " + response.url)

        # Call Splash only once per page (that contains multiple XML elements).
        data = self.getUrlData(response.url)
        response.meta["rendered_data"] = data

        # We would use .fromstring(response.text) if the response did not include the XML declaration:
        # <?xml version="1.0" encoding="utf-8"?>
        root = etree.XML(response.body)
        tree = etree.ElementTree(root)

        # If results are returned.
        elements = tree.xpath('/root/items/*')
        if len(elements) > 0:
            for element in elements:

                copyResponse = response.copy()
                element_xml_str = etree.tostring(element, pretty_print=True, encoding='unicode')
                element_dict = xmltodict.parse(element_xml_str)

                # TODO: It's probably a pointless attribute.
                #del element_dict["data"]["score"]

                # Passing the dictionary for easier access to attributes.
                copyResponse.meta['item'] = element_dict["data"]

                # In case JSON string representation is preferred:
                # copyResponse._set_body(json.dumps(copyResponse.meta['item'], indent=1, ensure_ascii=False))
                copyResponse._set_body(element_xml_str)

                if self.hasChanged(copyResponse):
                    yield self.handleEntry(copyResponse)

                # LomBase.parse() has to be called for every individual instance that needs to be saved to the database.
                LomBase.parse(self, copyResponse)

        # TODO: To not stress the Rest APIs.
        # time.sleep(0.1)

        # If the number of returned results is equal to the imposed limit, it means that there are more to be returned.
        if len(elements) == self.limit:
            self.page += 1
            url = self.apiUrl.replace('%start', str(self.page * self.limit)).replace('%anzahl', str(self.limit))
            yield scrapy.Request(url=url, callback=self.parse, headers={
                    'Accept': 'application/xml',
                    'Content-Type': 'application/xml'
                })

    def getId(self, response):
        return response.xpath('/data/id_local/text()').get()

    def getHash(self, response):
        """ Since we have no 'last_modified' date from the elements we cannot do something better.
            Therefore, the current implementation takes into account (1) the code version, (2) the item's ID, and (3)
            the date (day, month, year). """
        return hash(self.version) + hash(self.getId(response)) + self._date_to_integer(datetime.date(datetime.now()))

    def _date_to_integer(self, dt_time):
        """ Converting the date to an integer, so it is useful in the getHash method
            Using prime numbers for less collisions. """
        return 9973 * dt_time.year + 97 * dt_time.month + dt_time.day

    def handleEntry(self, response):
        return LomBase.parse(self, response)

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        base.add_value('thumbnail', response.xpath('/data/thumbnail/text()').get())

        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value('title', response.xpath('/data/titel/text()').get())

        return general

    def getLOMEducational(self, response):
        educational = LomBase.getLOMEducational(self, response)

        educational.add_value('description', response.xpath('/data/beschreibung/text()').get())

        bildungsebene = response.xpath('/data/bildungsebene/text()').get()
        if bildungsebene is not None:
            educational.add_value('intendedEndUserRole', bildungsebene.split(';'))

        return educational

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)

        technical.add_value('format', 'application/xml')
        location = response.xpath('/data/media_url/text()').get()
        technical.add_value('location', "http://merlin.nibis.de" + location)
        technical.add_value('size', len(response.body))

        return technical

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)

        # Use the dictionary when it is easier.
        element_dict = response.meta["item"]

        if len(response.xpath('/data/fach/*')) > 0:
            element_dict = response.meta["item"]
            discipline = list(element_dict["fach"].values())[0]
            valuespaces.add_value('discipline', discipline)

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
            resource_types = [merlin_to_oeh_types[rt] if rt in merlin_to_oeh_types else rt.lower() for rt in resource_types]

            valuespaces.add_value('learningResourceType', resource_types)
        return valuespaces