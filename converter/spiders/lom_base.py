import json

from converter.MethodPerformanceTracing import MethodPerformanceTracing
from converter.items import *
from pprint import pprint
import logging
from converter.constants import Constants
import requests
import html2text
import urllib
from scrapy.utils.project import get_project_settings
from converter.es_connector import EduSharing
import time

class LomBase(MethodPerformanceTracing):
    friendlyName = "LOM Based spider"
    ranking = 1
    version = (
        "1.0"  # you can override this locally and use it for your getHash() function
    )

    uuid = None
    remoteId = None
    forceUpdate = False

    def __init__(self, **kwargs):
        if "uuid" in kwargs:
            self.uuid = kwargs["uuid"]
        if "remoteId" in kwargs:
            self.remoteId = kwargs["remoteId"]
        if "cleanrun" in kwargs and kwargs["cleanrun"] == "true":
            logging.info(
                "cleanrun requested, will force update for crawler " + self.name
            )
            # EduSharing().deleteAll(self)
            self.forceUpdate = True
        if "resetVersion" in kwargs and kwargs["resetVersion"] == "true":
            logging.info(
                "resetVersion requested, will force update + reset versions for crawler "
                + self.name
            )
            # EduSharing().deleteAll(self)
            EduSharing.resetVersion = True
            self.forceUpdate = True

    # override to improve performance and automatically handling id
    def getId(self, response=None) -> str:
        return None

    # override to improve performance and automatically handling hash
    def getHash(self, response=None) -> str:
        return None

    # return the unique uri for the entry
    def getUri(self, response=None) -> str:
        return response.url

    def getUUID(self, response=None) -> str:
        return EduSharing().buildUUID(self.getUri(response))

    def hasChanged(self, response=None) -> bool:
        if self.forceUpdate:
            return True
        if self.uuid:
            if self.getUUID(response) == self.uuid:
                logging.info("matching requested id: " + self.uuid)
                return True
            return False
        if self.remoteId:
            if str(self.getId(response)) == self.remoteId:
                logging.info("matching requested id: " + self.remoteId)
                return True
            return False
        db = EduSharing().findItem(self.getId(response), self)
        changed = db == None or db[1] != self.getHash(response)
        if not changed:
            logging.info("Item " + db[0] + " has not changed")
        return changed

    # you might override this method if you don't want to import specific entries
    def shouldImport(self, response=None) -> bool:
        return True

    def parse(self, response):
        if self.shouldImport(response) == False:
            logging.info(
                "Skipping entry "
                + str(self.getId(response))
                + " because shouldImport() returned false"
            )
            return None
        if self.getId(response) != None and self.getHash(response) != None:
            if not self.hasChanged(response):
                return None
        main = self.getBase(response)
        main.add_value("lom", self.getLOM(response).load_item())
        main.add_value("valuespaces", self.getValuespaces(response).load_item())
        main.add_value("license", self.getLicense(response).load_item())
        main.add_value("permissions", self.getPermissions(response).load_item())
        logging.debug(main.load_item())
        main.add_value("response", self.mapResponse(response).load_item())
        return main.load_item()

    def html2Text(self, html):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        return h.handle(html)

    def getUrlData(self, url):
        settings = get_project_settings()
        html = None
        if settings.get("SPLASH_URL"):
            data = requests.post(
                settings.get("SPLASH_URL") + "/render.json",
                json={
                    "html": 1,
                    "iframes": 1,
                    "url": url,
                    "wait": settings.get("SPLASH_WAIT"),
                    "headers": settings.get("SPLASH_HEADERS"),
                },
            ).content.decode("UTF-8")
            j = json.loads(data)
            html = j['html'] if 'html' in j else ''
            text = html
            text += '\n'.join(list(map(lambda x: x["html"], j["childFrames"]))) if 'childFrames' in j else ''
            return {"html": html, "text": self.html2Text(text)}
        else:
            return {"html": None, "text": None}

    def mapResponse(self, response, fetchData=True):
        r = ResponseItemLoader(response=response)
        r.add_value("status", response.status)
        # r.add_value('body',response.body.decode('utf-8'))

        # render via splash to also get the full javascript rendered content.
        if fetchData:
            data = self.getUrlData(response.url)
            r.add_value("html", data["html"])
            r.add_value("text", data["text"])
        r.add_value("headers", response.headers)
        r.add_value("url", self.getUri(response))
        return r

    def getValuespaces(self, response):
        return ValuespaceItemLoader(response=response)

    def getLOM(self, response) -> LomBaseItemloader:
        lom = LomBaseItemloader(response=response)
        lom.add_value("general", self.getLOMGeneral(response).load_item())
        lom.add_value("lifecycle", self.getLOMLifecycle(response).load_item())
        lom.add_value("technical", self.getLOMTechnical(response).load_item())
        lom.add_value("educational", self.getLOMEducational(response).load_item())
        lom.add_value("classification", self.getLOMClassification(response).load_item())
        return lom

    def getBase(self, response=None) -> BaseItemLoader:
        base = BaseItemLoader()
        base.add_value("sourceId", self.getId(response))
        base.add_value("hash", self.getHash(response))
        # we assume that content is imported. Please use replace_value if you import something different
        base.add_value("type", Constants.TYPE_MATERIAL)
        return base

    def getLOMGeneral(self, response=None) -> LomGeneralItemloader:
        return LomGeneralItemloader(response=response)

    def getLOMLifecycle(self, response=None) -> LomLifecycleItemloader:
        return LomLifecycleItemloader(response=response)

    def getLOMTechnical(self, response=None) -> LomTechnicalItemLoader:
        return LomTechnicalItemLoader(response=response)

    def getLOMEducational(self, response=None) -> LomEducationalItemLoader:
        return LomEducationalItemLoader(response=response)

    def getLicense(self, response=None) -> LicenseItemLoader:
        return LicenseItemLoader(response=response)

    def getLOMClassification(self, response=None) -> LomClassificationItemLoader:
        return LomClassificationItemLoader(response=response)

    def getPermissions(self, response=None) -> PermissionItemLoader:
        permissions = PermissionItemLoader(response=response)
        # default all materials to public, needs to be changed depending on the spider!
        settings = get_project_settings()
        permissions.add_value("public", settings.get("DEFAULT_PUBLIC_STATE"))
        return permissions
