import logging
import sys

import requests

from .lom_base import LomBase, LomAgeRangeItemLoader
from scrapy.http import JsonRequest
from scrapy.spiders import Spider
import json
import vobject
from converter.es_connector import EduSharingConstants
import converter.env as env
from ...items import LomLifecycleItemloader


class EduSharingBase(Spider, LomBase):
    # max items per request, recommended value between 100-1000
    maxItems = 200
    friendlyName = "Edu-Sharing repository spider"
    # the location of the edu-sharing rest api
    apiUrl = "http://localhost/edu-sharing/rest/"
    savedSearchUrl = "search/v1/queries/load/"
    searchUrl = "search/v1/queriesV2/-home-/"
    searchToken = "*"
    # the mds to use for the search request
    mdsId = "-default-"
    # searchId to import from, if empty, whole repository will be fetched
    importSearchId = ''

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)
        importSearchId = env.get("EDU_SHARING_IMPORT_SEARCH_ID", True, None)

        if importSearchId:
            self.importSearchId = importSearchId
            logging.info("Importing only data based on the search query: {}".format(self.importSearchId))

    def buildUrl(self, offset=0):
        if self.importSearchId:
            return (
                self.apiUrl
                + self.savedSearchUrl
                + self.importSearchId
                + "?contentType=FILES&propertyFilter=-all-"
                + "&maxItems=" + str(self.maxItems) + "&skipCount=" + str(offset)
                + "&sortProperties=cm%3Acreated&sortAscending=true"
            )
        return (
            self.apiUrl
            + self.searchUrl
            + self.mdsId
            + "/ngsearch?contentType=FILES&propertyFilter=-all-"
              "&maxItems=" + str(self.maxItems) + "&skipCount="
            + str(offset)
            + "&sortProperties=cm%3Acreated&sortAscending=true"
        )

    def search(self, offset=0):
        criteria = []
        if "queriesV2" in self.searchUrl:
            criteria = [({"property": "ngsearchword", "values": [self.searchToken]} )]
        data = {}
        if self.importSearchId:
            return JsonRequest(
                url=self.buildUrl(offset)
            )

        # criterias only required for regular endpoint
        return JsonRequest(
            url=self.buildUrl(offset),
            data={
                ("criterias" if "queriesV2" in self.searchUrl else "criteria"): criteria
            },
            callback=self.parse,
        )


    def getProperty(self, name, response):
        return (
            response.meta["item"]["properties"][name]
            if name in response.meta["item"]["properties"]
            else None
        )

    def start_requests(self):
        yield self.search()

    async def parse(self, response):
        data = json.loads(response.text)
        if len(data["nodes"]) > 0:
            for item in data["nodes"]:
                copyResponse = response.replace(url=item["content"]["url"])
                copyResponse.meta["item"] = item
                if self.hasChanged(copyResponse):
                    yield await LomBase.parse(self, copyResponse)
            yield self.search(data["pagination"]["from"] + data["pagination"]["count"])

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        base.replace_value("thumbnail", response.meta["item"]["preview"]["url"])
        base.replace_value(
            "origin", self.getProperty("ccm:replicationsource", response)
        )
        # ToDo: base.origin is used for creating subfolders in "SYNC_OBJ/<crawler_name>/..."
        #  - currently only subfolders for learning objects that were gathered by crawlers are created?
        #  - base.origin could be set for (safe) values from 'ccm:oeh_publisher_combined' as well
        if (
            self.getProperty("ccm:replicationsource", response) and
            self.getProperty("ccm:wwwurl", response)
        ):
            # imported objects usually have the content as binary text
            # TODO: Sometimes, edu-sharing redirects if no local content is found, and this should be html-parsed
            if response.meta["item"]["downloadUrl"]:
                try:
                    r = requests.get(response.meta["item"]["downloadUrl"])
                    if r.status_code == 200:
                        base.replace_value("fulltext", r.text)
                except:
                    logging.warning(
                        "error fetching data from " + str(response.meta["item"]["downloadUrl"]),
                        sys.exc_info()[0],
                    )
        else:
            # try to transform using alfresco
            r = requests.get(
                self.apiUrl
                + "/node/v1/nodes/"
                + response.meta["item"]["ref"]["repo"]
                + "/"
                + response.meta["item"]["ref"]["id"]
                + "/textContent",
                headers={"Accept": "application/json"},
            ).json()
            if "text" in r:
                base.replace_value("fulltext", r["text"])

        return base

    # fulltext is handled in base, response is not necessary
    async def mapResponse(self, response, fetchData=True):
        return await LomBase.mapResponse(self, response, False)

    def getId(self, response=None) -> str:
        return response.meta["item"]["ref"]["id"]

    def getHash(self, response=None) -> str:
        return self.version + response.meta["item"]["properties"]["cm:modified"][0]

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.replace_value("title", response.meta["item"]["title"])
        general.add_value("keyword", self.getProperty("cclom:general_keyword", response))
        general.add_value("description", self.getProperty("cclom:general_description", response))
        general.add_value('identifier', self.getProperty("cclom:general_identifier", response))
        general.add_value('language', self.getProperty("cclom:general_language", response))
        general.add_value('aggregationLevel', self.getProperty("cclom:aggregationLevel", response))
        return general

    def getLOMEducational(self, response):
        educational = LomBase.getLOMEducational(self, response)
        tar_from = self.getProperty("ccm:educationaltypicalagerange_from", response)
        tar_to = self.getProperty("ccm:educationaltypicalagerange_to", response)
        if tar_from and tar_to:
            range = LomAgeRangeItemLoader()
            range.add_value("fromRange", tar_from)
            range.add_value("toRange", tar_to)
            educational.add_value("typicalAgeRange", range.load_item())
        educational.add_value("typicalLearningTime", self.getProperty("cclom:typicallearningtime", response))
        return educational

    def getLOMLifecycle(self, response):
        for role, edu_sharing_lifecycle_property in EduSharingConstants.LIFECYCLE_ROLES_MAPPING.items():
            # there can be multiple authors or contributors per role
            vcard_list: list = self.getProperty(edu_sharing_lifecycle_property, response)
            # vCards are returned by the edu-sharing API as a list of strings
            if vcard_list:
                # making sure that we only create lifecycle items when there's actual vCards to parse
                for vcard_entry in vcard_list:
                    # each vCard-String needs its own LOM Lifecycle Item
                    lifecycle: LomLifecycleItemloader = LomBase.getLOMLifecycle(self, response)
                    if vcard_entry:
                        yield from self.get_lifecycle_from_vcard_string(lifecycle, role, vcard_entry)

    @staticmethod
    def get_lifecycle_from_vcard_string(lifecycle: LomLifecycleItemloader, role, vcard_entry: str):
        """
        This method parses a vCard from a string and saves its values to LifecycleItem's fields if possible.
        """
        vcard: vobject.base.Component = vobject.readOne(vcard_entry)
        if hasattr(vcard, "n"):
            given = vcard.n.value.given
            family = vcard.n.value.family
            lifecycle.add_value("role", role)
            lifecycle.add_value("firstName", given)
            lifecycle.add_value("lastName", family)
        # ToDo: test the 'title'-field before activating it
        # if hasattr(vcard, "title"):
        #     title: str = vcard.title.value
        #     lifecycle.add_value("title", title)
        # ToDo: implement identifiers (GND / ORCID / ROR / Wikidata)
        # if hasattr(vcard, "x-gnd-uri"):
        #     pass
        # if hasattr(vcard, "x-orcid"):
        #     pass
        # if hasattr(vcard, "x-ror"):
        #     pass
        # if hasattr(vcard, "x-wikidata"):
        #     pass
        if hasattr(vcard, "email"):
            # ToDo: recognize multiple emails
            vcard_email: str = vcard.email.value
            lifecycle.add_value("email", vcard_email)
        if hasattr(vcard, "url"):
            # ToDo: recognize multiple URLs
            vcard_url: str = vcard.url.value
            lifecycle.add_value("url", vcard_url)
        if hasattr(vcard, "org"):
            vcard_org: str = vcard.org.value
            lifecycle.add_value("organization", vcard_org)
        if hasattr(vcard, "x-es-lom-contribute-date"):
            # copy the contribution date only if available
            vcard_es_date: list = vcard.contents.get("x-es-lom-contribute-date")  # edu-sharing contributor date
            # has its own vCard extension. By calling vcard.contents.get() we'll receive:
            # a list of <class 'vobject.base.ContentLine>
            if vcard_es_date:
                # <X-ES-LOM-CONTRIBUTE-DATE{}2021-06-05T00:00:00> -> we only need the date itself
                vcard_es_date_value: str = vcard_es_date[0].value
                if vcard_es_date_value:
                    # some (malformed) vCards with the 'x-es-lom-contribute-date'-key look like this:
                    # <X-ES-LOM-CONTRIBUTE-DATE{}> which means they are missing the actual date itself.
                    # By checking if the string is True-ish, empty strings '' won't be saved to Lifecycle
                    lifecycle.add_value("date", vcard_es_date_value)
                # ToDo: this might be a good place for an 'else'-statement to catch malformed vCards
                #  by their node-ID
        if hasattr(vcard, "uid"):
            vcard_uid: str = vcard.uid.value
            lifecycle.add_value("uuid", vcard_uid)
        yield lifecycle

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.replace_value("format", "text/html")
        technical.replace_value("location", response.url)
        # ToDo: 'cclom:location' supports multiple values (compare response.url <-> list of URLs)
        technical.replace_value("duration", self.getProperty("cclom:duration", response))
        return technical

    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        license.add_value("url", response.meta["item"]["license"]["url"])
        license.add_value(
            "internal", self.getProperty("ccm:commonlicense_key", response)
        )
        # ToDo: setting 'internal' here like this might be problematic in regards to CC-Versions:
        #   need to double-check if this might (wrongfully) turn CC x.0 licenses into other versions
        #  - "ccm:commonlicense_cc_version"
        license.add_value("author", self.getProperty("ccm:author_freetext", response))
        license.add_value("description", self.getProperty("cclom:rights_description", response))
        license.add_value("expirationDate", self.getProperty("ccm:license_to", response))
        return license

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.add_value("accessibilitySummary", self.getProperty("ccm:accessibilitySummary", response))
        if self.getProperty("ccm:conditionsOfAccess", response):
            valuespaces.add_value("conditionsOfAccess", self.getProperty("ccm:conditionsOfAccess", response))
        elif self.getProperty("ccm:oeh_quality_login", response):
            # this fallback will lose metadata in the long run since the "conditionsOfAccess"-Vocab has 3 values, while
            # "ccm:oeh_quality_login" returns only binary string values:
            # - "0": login required
            # - "1": no login necessary
            oeh_quality_login_value: list = self.getProperty("ccm:oeh_quality_login", response)
            if oeh_quality_login_value:
                oeh_quality_login_value: str = oeh_quality_login_value[0]
                match oeh_quality_login_value:
                    case "0":
                        valuespaces.add_value("conditionsOfAccess", "login")
                    case "1":
                        valuespaces.add_value("conditionsOfAccess", "no_login")
                    case _:
                        logging.warning(f"edu-sharing property 'ccm:oeh_quality_login' returned an unexpected value: "
                                        f"{oeh_quality_login_value} for node-ID {response.meta['item']['ref']['id']}")
        valuespaces.add_value("dataProtectionConformity", self.getProperty("ccm:dataProtectionConformity", response))
        valuespaces.add_value("discipline", self.getProperty("ccm:taxonid", response))
        valuespaces.add_value("educationalContext", self.getProperty("ccm:educationalcontext", response))
        valuespaces.add_value("fskRating", self.getProperty("ccm:fskRating", response))
        valuespaces.add_value("intendedEndUserRole", self.getProperty("ccm:educationalintendedenduserrole", response))
        valuespaces.add_value("learningResourceType", self.getProperty("ccm:educationallearningresourcetype", response))
        valuespaces.add_value('new_lrt', self.getProperty("ccm:oeh_lrt", response))
        valuespaces.add_value("oer", self.getProperty("ccm:license_oer", response))
        valuespaces.add_value("price", self.getProperty("ccm:price", response))
        # ToDo: confirm if 'sourceContentType' & 'toolCategory' should be used at all,
        #  since they are already obsolete in WLO crawlers (might be obsolete here as well)
        valuespaces.add_value(
            "sourceContentType", self.getProperty("ccm:sourceContentType", response)
        )
        valuespaces.add_value(
            "toolCategory", self.getProperty("ccm:toolCategory", response)
        )
        return valuespaces
