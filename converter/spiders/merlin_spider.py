import xmltodict as xmltodict
from lxml import etree
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from converter.items import *
from converter.spiders.lom_base import LomBase


class MerlinSpider(CrawlSpider, LomBase):
    """
    This crawler fetches data from the Merlin content source, which provides us paginated XML data. For every element
    in the returned XML array we call LomBase.parse(), which in return calls methods, such as getId(), getBase() etc.

    Author: Ioannis Koumarelas, ioannis.koumarelas@hpi.de, Schul-Cloud, Content team.
    """

    name = "merlin_spider"
    url = "https://merlin.nibis.de/index.php"  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = "Merlin"  # name as shown in the search ui
    version = "0.2"  # the version of your crawler, used to identify if a reimport is necessary
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

    def parse(self, response: scrapy.http.Response):
        print("Parsing URL: " + response.url)

        # Call Splash only once per page (that contains multiple XML elements).
        data = self.getUrlData(response.url)
        response.meta["rendered_data"] = data

        # We would use .fromstring(response.text) if the response did not include the XML declaration:
        # <?xml version="1.0" encoding="utf-8"?>
        root = etree.XML(response.body)
        tree = etree.ElementTree(root)

        # Get the total number of possible elements
        elements_total = int(tree.xpath('/root/sum')[0].text)

        # If results are returned.
        elements = tree.xpath("/root/items/*")
        if len(elements) > 0:
            for element in elements:
                copyResponse = response.copy()
                element_xml_str = etree.tostring(
                    element, pretty_print=True, encoding="unicode"
                )
                try:
                    element_dict = xmltodict.parse(element_xml_str)
                    element_dict = element_dict["data"]

                    # Preparing the values here helps for all following logic across the methods.
                    self.prepare_element(element_dict)

                    # If there is no available county (Kreis) code, then we do not want to deal with this element.
                    if not("county_ids" in element_dict
                           and element_dict["county_ids"] is not None
                           and len(element_dict["county_ids"]) > 0):
                        continue

                    # TODO: It's probably a pointless attribute.
                    # del element_dict["data"]["score"]

                    # Passing the dictionary for easier access to attributes.
                    copyResponse.meta["item"] = element_dict

                    # In case JSON string representation is preferred:
                    # copyResponse._set_body(json.dumps(copyResponse.meta['item'], indent=1, ensure_ascii=False))
                    copyResponse._set_body(element_xml_str)

                    if self.hasChanged(copyResponse):
                        yield self.handleEntry(copyResponse)

                    # LomBase.parse() has to be called for every individual instance that needs to be saved to the database.
                    LomBase.parse(self, copyResponse)
                except Exception as e:
                    print("Issues with the element: " + str(element_dict["id_local"]) if "id_local" in element_dict else "")
                    print(str(e))

        current_expected_count = (self.page+1) * self.limit

        # TODO: To not stress the Rest APIs.
        # time.sleep(0.1)

        # If we are below the total available numbers continue fetching more pages.
        if current_expected_count < elements_total:
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
            # + self._date_to_integer(datetime.date(datetime.now()))
        )

    # def _date_to_integer(self, dt_time):
    #     """ Converting the date to an integer, so it is useful in the getHash method
    #         Using prime numbers for less collisions. """
    #     return 9973 * dt_time.year + 97 * dt_time.month + dt_time.day

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
        element_dict = dict(response.meta["item"])

        base.add_value("thumbnail", element_dict.get("thumbnail", ""))  # get or default

        # As a backup, if no other thumbnail URL is available.
        element_dict["hardcodedDefaultLogoUrl"] = "/logos/bs_logos/merlin.png"

        # By the order of preference. As soon as one of these default thumbnails is available you keep that.
        for default_thumbnail in ["srcLogoUrl", "logo", "hardcodedDefaultLogoUrl"]:
            if default_thumbnail in element_dict:
                base.add_value("defaultThumbnail", "https://merlin.nibis.de" + element_dict[default_thumbnail])
                break

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

    def getLicense(self, response):
        license = LomBase.getLicense(self, response)

        # Element response as a Python dict.
        element_dict = response.meta["item"]

        # If there is only one element and is the County code 3100, then it is public content.
        if len(element_dict["county_ids"]) == 1 and str(element_dict["county_ids"][0]) == "county-3100":
            license.replace_value('internal', Constants.LICENSE_COPYRIGHT_LAW)  # public
        else:
            license.replace_value('internal', Constants.LICENSE_NONPUBLIC)  # private

        return license

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

    def getPermissions(self, response):
        """
        In case license information, in the form of counties (Kreis codes), is available. This changes the permissions from
        public to private and sets accordingly the groups and mediacenters. For more information regarding the available
        Merlin county (kreis) codes please consult 'http://merlin.nibis.de/index.php?action=kreise'
        """

        permissions = LomBase.getPermissions(self, response)

        element_dict = response.meta["item"]

        permissions.replace_value("public", False)
        permissions.add_value("autoCreateGroups", True)

        groups = []

        county_ids = element_dict["county_ids"]
        public_county = "county-3100"

        # If there is only one element and is the County code 3100, then it is public content.
        if len(county_ids) == 1 and str(county_ids[0]) == public_county:
            # Add to state-wide public group.
            # groups.append("state-LowerSaxony-public")
            groups.append("LowerSaxony-public")

            # Add 1 group per County-code, which in this case is just "100" (3100).
            groups.extend(county_ids)
        else:
            # Add to state-wide private/licensed group.
            # groups.append("state-LowerSaxony-licensed")
            groups.append("LowerSaxony-private")

            # If County code 100 (country-wide) is included in the list, remove it.
            if public_county in county_ids:
                county_ids.remove(public_county)

            # Add 1 group per county.
            groups.extend(county_ids)

        permissions.add_value("groups", groups)

        return permissions

    def prepare_element(self, element_dict):
        # Step 1. Prepare county (Kreis) codes.
        if "kreis_id" in element_dict and element_dict["kreis_id"] is not None:
            county_ids = element_dict["kreis_id"]["data"]  # ... redundant extra nested dictionary "data"...
            if not isinstance(county_ids, list):  # one element
                county_ids = [county_ids]
            county_ids = sorted(county_ids, key=lambda x: int(x))

            # Add prefix "3" to conform with nationally-assigned IDs:
            # https://de.wikipedia.org/wiki/Liste_der_Landkreise_in_Deutschland
            county_ids = ["3" + id for id in county_ids]
            county_ids = ["county-" + x for x in county_ids]
            element_dict["county_ids"] = county_ids

        # Step 2. Fix thumbnail URL.
        thumbnail_prepared = element_dict["thumbnail"]

        # Step 2. Case a: Remove the 3 dots "...".
        thumbnail_prepared = thumbnail_prepared.replace("...", "")

        # Step 2. Case b: Replace "%2F" with '/'
        # TODO: check why not ALL occurrences are replaced.
        thumbnail_prepared = thumbnail_prepared.replace("%2F", "/")

        # Step 2. Case c: Replace the dot after the parent identifier with a '/'.
        if element_dict["parent_identifier"] is not None:
            parent_identifier = element_dict["parent_identifier"]
            subpath_position = thumbnail_prepared.find(parent_identifier) + len(parent_identifier)
            if thumbnail_prepared[subpath_position] == ".":
                thumbnail_prepared = thumbnail_prepared[:subpath_position] + "/" + thumbnail_prepared[subpath_position + 1:]

            element_dict["thumbnail"] = thumbnail_prepared

        return element_dict

