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


class EduSharingBase(Spider, LomBase):
    # max items per request, recommended value between 100-1000
    maxItems = 500
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
                url=self.buildUrl()
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

    def parse(self, response):
        data = json.loads(response.text)
        if len(data["nodes"]) > 0:
            for item in data["nodes"]:
                copyResponse = response.replace(url=item["content"]["url"])
                copyResponse.meta["item"] = item
                if self.hasChanged(copyResponse):
                    yield LomBase.parse(self, copyResponse)
            yield self.search(data["pagination"]["from"] + data["pagination"]["count"])

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        base.replace_value("thumbnail", response.meta["item"]["preview"]["url"])
        base.replace_value(
            "origin", self.getProperty("ccm:replicationsource", response)
        )
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
    def mapResponse(self, response, fetchData=True):
        return LomBase.mapResponse(self, response, False)

    def getId(self, response=None) -> str:
        return response.meta["item"]["ref"]["id"]

    def getHash(self, response=None) -> str:
        return self.version + response.meta["item"]["properties"]["cm:modified"][0]

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.replace_value("title", response.meta["item"]["title"])
        general.add_value(
            "keyword", self.getProperty("cclom:general_keyword", response)
        )
        general.add_value(
            "description", self.getProperty("cclom:general_description", response)
        )
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
        return educational

    def getLOMLifecycle(self, response):
        lifecycle = LomBase.getLOMLifecycle(self, response)
        for role in EduSharingConstants.LIFECYCLE_ROLES_MAPPING.keys():
            entry = self.getProperty("ccm:lifecyclecontributer_" + role, response)
            if entry and entry[0]:
                # TODO: we currently only support one author per role
                vcard = vobject.readOne(entry[0])
                if hasattr(vcard, "n"):
                    given = vcard.n.value.given
                    family = vcard.n.value.family
                    lifecycle.add_value("role", role)
                    lifecycle.add_value("firstName", given)
                    lifecycle.add_value("lastName", family)
        return lifecycle

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.replace_value("format", "text/html")
        technical.replace_value("location", response.url)
        technical.replace_value("duration", self.getProperty("cclom:duration", response))
        return technical

    def getLicense(self, response):
        license = LomBase.getLicense(self, response)
        license.add_value("url", response.meta["item"]["license"]["url"])
        license.add_value(
            "internal", self.getProperty("ccm:commonlicense_key", response)
        )
        license.add_value("author", self.getProperty("ccm:author_freetext", response))
        return license

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        valuespaces.add_value("discipline", self.getProperty("ccm:taxonid", response))
        valuespaces.add_value(
            "intendedEndUserRole",
            self.getProperty("ccm:educationalintendedenduserrole", response),
        )
        valuespaces.add_value(
            "educationalContext", self.getProperty("ccm:educationalcontext", response)
        )
        valuespaces.add_value(
            "learningResourceType",
            self.getProperty("ccm:educationallearningresourcetype", response),
        )
        valuespaces.add_value(
            "sourceContentType", self.getProperty("ccm:sourceContentType", response)
        )
        valuespaces.add_value(
            "toolCategory", self.getProperty("ccm:toolCategory", response)
        )
        return valuespaces
