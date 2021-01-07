import copy
import json
import os

from scrapy.spiders import CrawlSpider

from converter.es_connector import EduSharing
from converter.items import *
from converter.spiders.lom_base import LomBase
from converter.constants import *


class MediothekPixiothekSpider(CrawlSpider, LomBase):
    """
    This crawler fetches data from the Mediothek/Pixiothek. The API request sends all results in one page. The outcome
    is an JSON array which will be parsed to their elements.

    Author: Ioannis Koumarelas, ioannis.koumarelas@gmail.com , Schul-Cloud, Content team.
    """

    name = "mediothek_pixiothek_spider"
    url = "https://www.schulportal-thueringen.de/"  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = "MediothekPixiothek"  # name as shown in the search ui
    version = "0.2"  # the version of your crawler, used to identify if a reimport is necessary
    apiUrl = "https://www.schulportal-thueringen.de/tip-ms/api/public_mediothek_metadatenexport/publicMediendatei"
    # Alternatively, you can load the file from a local path
    # "file://LOCAL_FILE_PATH"  # e.g., file:///data/file.json

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self):
        yield scrapy.Request(
            url=self.apiUrl,
            callback=self.parse,
        )

    def parse(self, response: scrapy.http.Response):
        elements = json.loads(response.body_as_unicode())
        prepared_elements = [self.prepare_element(element_dict) for element_dict in elements]

        collection_elements = self.prepare_collections(prepared_elements)

        for i, element_dict in enumerate(collection_elements):

            copyResponse = response.copy()

            # Passing the dictionary for easier access to attributes.
            copyResponse.meta["item"] = element_dict

            # In case JSON string representation is preferred:
            json_str = json.dumps(element_dict, indent=4, sort_keys=True, ensure_ascii=False)
            copyResponse._set_body(json_str)

            if self.hasChanged(copyResponse):
                yield self.handleEntry(copyResponse)

            # LomBase.parse() has to be called for every individual instance that needs to be saved to the database.
            LomBase.parse(self, copyResponse)


    def getId(self, response):
        # Element response as a Python dict.
        element_dict = response.meta["item"]

        return element_dict["id"]

    def getHash(self, response):
        # Element response as a Python dict.
        element_dict = response.meta["item"]
        id = element_dict["id"]

        # presentation timestamp (PTS)
        pts = element_dict["pts"]

        # date_object = datetime.strptime(hash, "%Y-%m-%d %H:%M:%S.%f").date()
        return hash(hash(id) + hash(pts))

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

        base.add_value("searchable", element_dict.get("searchable", "0"))

        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)

        # Element response as a Python dict.
        element_dict = response.meta["item"]

        general.add_value("title", element_dict["title"])

        general.add_value("aggregationLevel", element_dict["aggregation_level"])

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

        if "oeffentlich" in element_dict and element_dict["oeffentlich"] == "0":  # private
            license.replace_value("internal", Constants.LICENSE_NONPUBLIC)
        else:
            license.replace_value("internal", Constants.LICENSE_COPYRIGHT_LAW)  # public

        return license

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)

        technical.add_value("format", "text/html")
        technical.add_value("location", self.getUri(response))
        technical.add_value("size", len(response.body))

        return technical


    def getPermissions(self, response):
        """
        Licensing information is controlled via the 'oeffentlich' flag. When it is '1' it is available to the public,
        otherwise only to Thuringia. Therefore, when the latter happens we set the public to private, and set the groups
        and mediacenters accordingly.
        """
        permissions = LomBase.getPermissions(self, response)

        # Self-explained. Only 1 media center in this case.
        permissions.add_value("autoCreateGroups", True)
        # permissions.add_value("autoCreateMediacenters", True)

        element_dict = response.meta["item"]
        permissions.replace_value('public', False)
        if "oeffentlich" in element_dict and element_dict["oeffentlich"] == "0":  # private
            permissions.add_value('groups', ['Thuringia-private'])
            # permissions.add_value('mediacenters', [self.name])  # only 1 mediacenter.
        else:
            permissions.add_value('groups', ['Thuringia-public'])

        return permissions


    def getLOMRelation(self, response=None) -> LomRelationItemLoader:
        """
        Helps implement collections using relations as described in the LOM-DE.doc#7 (Relation) specifications:
        http://sodis.de/lom-de/LOM-DE.doc .
        """
        relation = LomBase.getLOMRelation(self, response)

        # Element response as a Python dict.
        element_dict = response.meta["item"]

        relation.add_value("kind", element_dict["relation"][0]["kind"])

        resource = LomRelationResourceItem()
        resource["identifier"] = element_dict["relation"][0]["resource"]["identifier"]
        relation.add_value("resource", resource)

        return relation

    def prepare_collections(self, prepared_elements):
        """
        Prepares Mediothek and Pixiothek collections according to their strategies.
        """
        mediothek_elements = []
        pixiothek_elements = []
        for element_dict in prepared_elements:
            if element_dict["pixiothek"] == "1":
                pixiothek_elements.append(element_dict)
            else:
                mediothek_elements.append(element_dict)

        pixiothek_elements_grouped, mediothek_elements = \
            self.group_pixiothek_elements(pixiothek_elements, mediothek_elements)

        mediothek_elements_grouped = self.group_mediothek_elements(mediothek_elements)

        collection_elements = []
        collection_elements.extend(pixiothek_elements_grouped)
        collection_elements.extend(mediothek_elements_grouped)

        return collection_elements

    def group_by_elements(self, elements, group_by):
        """
        This method groups the corresponding elements based on the provided group_by parameter. This changes the logic
        so that every element in the end maps to an educational element in the https://www.schulportal-thueringen.de.
        """
        groups = {}
        for idx, element in enumerate(elements):
            if group_by not in element:
                logging.debug("Element " + str(element["id"])  + " does not contain information about " + group_by)
                continue
            group_by_value = element[group_by]
            if group_by_value not in groups:
                groups[group_by_value] = []
            groups[group_by_value].append(element)

        # For consistency sort all values per key.
        for key in groups.keys():
            groups[key] = sorted(groups[key], key=lambda x: int(x["id"]))

        return groups

    def group_pixiothek_elements(self, pixiothek_elements, mediothek_elements):
        """
        Collection elements in Pixiothek have a "parent" (representative) Mediothek element that describes the whole
        collection. Our task in this method is for every Pixiothek group to find its Mediothek element and add the
        connections between it and the Pixiothek elements. These Mediothek elements will not be considered as children
        of Mediothek collections.

        If we cannot find such a "parent" element among the Mediothek elements, then we select one of them as the
        collection parent (representative element) and set some of its attributes accordingly.
        """

        default_download_url = "https://www.schulportal-thueringen.de/html/images/" \
                               "themes/tsp2/startseite/banner_phone_startseite.jpg?id="

        mediothek_default_download_url = "https://www.schulportal-thueringen.de/web/guest/media/detail?tspi="

        pixiothek_elements_grouped_by = self.group_by_elements(pixiothek_elements, "serientitel")

        # Group Mediothek elements by einzeltitel. We are going to use this dictionary in the following loop to find
        # Pixiothek items that have this value in their serientitel.
        mediothek_elements_grouped_by_einzeltitel = self.group_by_elements(mediothek_elements, "einzeltitel")

        single_element_collection_serientitel = "Mediensammlungen zur freien Verwendung im Bildungsbereich"

        collection_elements = []

        edusharing = EduSharing()

        # Keeping track of "parent" (representative) elements to remove them from the Mediothek elements.
        parent_mediothek_elements = set()

        # Generate new "representative" (parent) element.
        for group_by_key in sorted(pixiothek_elements_grouped_by.keys()):
            group = pixiothek_elements_grouped_by[group_by_key]
            serientitel = None
            if "serientitel" in group[0]:
                serientitel = group[0]["serientitel"]

            # If a single Mediothek element exists with the same einzeltitel as this group's serientitel, then we shall use it
            # as the parent element of this collection.
            if serientitel in mediothek_elements_grouped_by_einzeltitel and \
                len(mediothek_elements_grouped_by_einzeltitel[serientitel]) == 1 and \
                mediothek_elements_grouped_by_einzeltitel[serientitel][0]["id"] not in parent_mediothek_elements: # Is not used as a parent of another collection.

                parent_element = copy.deepcopy(mediothek_elements_grouped_by_einzeltitel[serientitel][0])
                parent_mediothek_elements.add(parent_element["id"])
                parent_element["title"] = parent_element["einzeltitel"]
                parent_element["downloadUrl"] = mediothek_default_download_url + str(parent_element["mediumId"])

                # If the found Mediothek element has a serientitel equal to a predefined value, which indicates that
                # this is a collection item (which should normally be a parent and not a single element), we treat
                # specially and set the title equal to the einzeltitel, which already describes the collection.
                if parent_element["serientitel"] == single_element_collection_serientitel:
                    group.append(copy.deepcopy(mediothek_elements_grouped_by_einzeltitel[serientitel][0]))

            # Else, we shall use any random element of this group as the parent element.
            else:
                parent_element = copy.deepcopy(group[0])

                # We need to assign a new ID, different from the previous ones. For this purpose, we decide to modify
                # the ID of the existing element and add some suffix to note that this is an artificial element.
                # Clearly, such a big number for an ID will have no collisions with existing real elements.
                artificial_element_suffix = "000000"
                parent_element["id"] = parent_element["id"] + artificial_element_suffix

                # Assign a fake URL that we can still recognize if we ever want to allow the access of the collection
                # content.
                parent_element["downloadUrl"] = default_download_url + parent_element["id"]
                parent_element["title"] = parent_element["serientitel"]

            parent_element["searchable"] = 1
            parent_element["aggregation_level"] = 2
            parent_element["uuid"] = edusharing.buildUUID(parent_element["downloadUrl"])

            for element in group:
                element["searchable"] = 0
                element["aggregation_level"] = 1
                element["uuid"] = edusharing.buildUUID(element["downloadUrl"])

            # Add connections from parent to children elements.
            parent_element, group = self.relate_parent_with_children_elements(parent_element, group)

            collection_elements.append(parent_element)
            collection_elements.extend(group)

        # Remove Mediothek elements which were used as parents. We go in reverse mode as only then the indices keep
        # making sense as we keep deleting elements. The other way around, every time you delete an element the
        # consequent indices are not valid anymore.
        for i in reversed(range(len(mediothek_elements))):
            if mediothek_elements[i]["id"] in parent_mediothek_elements:
                del (mediothek_elements[i])

        return collection_elements, mediothek_elements

    def group_mediothek_elements(self, mediothek_elements):
        """
        Collection elements in Mediothek have no special element to represent them (a parent element). Therefore, we
        select one of them as the collection representative (parent element) and set some of its attributes accordingly.
        """
        mediothek_default_download_url = "https://www.schulportal-thueringen.de/web/guest/media/detail?tspi="

        mediothek_elements_grouped_by = self.group_by_elements(mediothek_elements, "mediumNummer")

        # Specifies a special case when a
        single_element_collection_serientitel = "Mediensammlungen zur freien Verwendung im Bildungsbereich"

        collection_elements = []

        edusharing = EduSharing()  # Used to generate UUIDs.

        # Generate new "parent" (representative) element.
        for group_by_key in sorted(mediothek_elements_grouped_by.keys()):
            group = mediothek_elements_grouped_by[group_by_key]
            parent_element = copy.deepcopy(group[0])

            # We need to assign a new ID, different from the previous ones. For this purpose, we decide to modify
            # the ID of the existing element and add some suffix to note that this is an artificial element.
            # Clearly, such a big number for an ID will have no collisions with existing real elements.
            artificial_element_suffix = "000000"
            parent_element["id"] = parent_element["id"] + artificial_element_suffix

            parent_element["downloadUrl"] = mediothek_default_download_url + str(parent_element["mediumId"])

            parent_element["title"] = parent_element["einzeltitel"]

            parent_element["searchable"] = 1
            parent_element["aggregation_level"] = 2
            parent_element["uuid"] = edusharing.buildUUID(parent_element["downloadUrl"])

            for element in group:
                element["searchable"] = 0
                element["aggregation_level"] = 1
                element["uuid"] = edusharing.buildUUID(element["downloadUrl"])

                if "dateiName" in element:
                    # Remove the file extension
                    filename, file_extension = os.path.splitext(element["dateiName"])
                    element["title"] = filename.replace("_", " ")

            # Add connections from parent to children elements.
            parent_element, group = self.relate_parent_with_children_elements(parent_element, group)

            collection_elements.append(parent_element)
            collection_elements.extend(group)

        return collection_elements

    def relate_parent_with_children_elements(self, parent_element, children_elements):
        # Add connections from "parent" to "children" elements.
        parent_element["relation"] = [
            {
                "kind": "haspart",
                "resource": {
                    "identifier": [
                        # Use the ccm:replicationsourceuuid to refer to the children elements.
                        element["uuid"] for element in children_elements
                    ]
                }
            }
        ]

        # Add connections from "children" elements to "parent".
        for element in children_elements:
            element["relation"] = [
                {
                    "kind": "ispartof",
                    "resource": {
                        # Use the ccm:replicationsourceuuid to refer to the parent element.
                        "identifier": [parent_element["uuid"]]
                    }
                }
            ]
        return parent_element, children_elements

    def prepare_element(self, element_dict):
        # TODO: Decide which title. Do we have to construct the title, by concatenating multiple from the provided ones?
        # Einzeltitel, einzeluntertitel, serientitel, serienuntertitel
        # Please keep in mind that we override this value for parent elements of collections.
        element_dict["title"] = element_dict["einzeltitel"]

        return element_dict