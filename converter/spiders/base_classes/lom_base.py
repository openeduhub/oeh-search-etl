import json
import logging

import html2text
import requests
import scrapy
from scrapy.utils.project import get_project_settings
from typing import Optional

from converter.constants import Constants
from converter.es_connector import EduSharing
from converter.items import *


class LomBase:
    """
    This class is used to build the metadata and should be used wherever possible.

    Use it either as an adapter for converting request data or use it as base class for your spider.

    When you sub-class it from another spider, you should call super during __init__.
    If you merely use it as an adapter, you should pass the kwargs from the spider __init__ to LomBase.
    Otherwise it might not be configured correctly.

    :param uuid: used to check if the item changed
    :param remoteId: used to check if the item changed
    :param cleanrun: set to 'true' if you want to ignore checks for possibly changed version
    :param resetVersion: set to 'true' if you want to ignore the checks and also reset the version in edu-sharing
    """

    name = None
    friendlyName = "LOM Based spider"
    ranking = 1
    version = (
        "1.0"  # you can override this locally and use it for your getHash() function
    )

    uuid = None
    remoteId = None
    forceUpdate = False

    def __init__(self, uuid=None, remoteId=None, cleanrun=None, resetVersion=None, **kwargs):
        if self.name is None:
            raise NotImplementedError(f'{self.__class__.__name__}.name is not defined on crawler')
        self.uuid = uuid
        self.remoteId = remoteId
        self.forceUpdate = False
        if cleanrun == "true":
            logging.info(
                "cleanrun requested, will force update for crawler " + self.name
            )
            # EduSharing().deleteAll(self)
            self.forceUpdate = True
        if resetVersion == "true":
            logging.info(
                "resetVersion requested, will force update + reset versions for crawler "
                + self.name
            )
            # EduSharing().deleteAll(self)
            EduSharing.resetVersion = True
            self.forceUpdate = True

    def getId(self, response: scrapy.http.Response = None) -> str:
        """
        :returns: the unique id of the current item
        """
        raise NotImplementedError(f'{self.__class__.__name__}.getId callback is not defined')

    def getHash(self, response: scrapy.http.Response = None) -> str:
        """
        :returns: the hashed value of the item. This hash is usually used for checking if the item changed
        """
        raise NotImplementedError(f'{self.__class__.__name__}.getHash callback is not defined')

    # return the unique uri for the entry
    def getUri(self, response: scrapy.http.Response = None) -> str:
        """
        override this if the URI of the item is not response.url

        :returns: the URI where the item can be accessed
        """
        return response.url

    def getUUID(self, response: scrapy.http.Response = None) -> str:
        """
        :returns: the uuid, derived from getUri
        """
        return EduSharing().buildUUID(self.getUri(response))

    def hasChanged(self, response: scrapy.http.Response = None) -> bool:
        """
        checks for equality in the following order: uuid, remoteId, getHash.
        But only if uuid/remoteId were set during init.

        :returns: true if the item changed, false otherwise
        """
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
        changed = db is None or db[1] != self.getHash(response)
        if not changed:
            logging.info("Item " + db[0] + " has not changed")
        return changed

    def shouldImport(self, response=None) -> bool:
        """
        Place logic that decides if the item should be imported here.

        :return: True
        """
        return True

    def parse(self, response: scrapy.http.Response) -> Optional[BaseItem]:
        """
        Will generate the item from your response.
        In order to populate the item you should override getLOM, getValuespaces, getLicense,
        and mapResponse.

        Instead of getLOM, you may also override getLOMGeneral, getLOMLifecycle, getLOMTechnical,
        getLOMEducational and getLOMClassification in case it's too much code for one function.

        :return: the populated BaseItem
        """
        if self.shouldImport(response) is False:
            logging.debug(
                "Skipping entry {} because shouldImport() returned false".format(str(self.getId(response)))
            )
            return None
        if self.getId(response) is not None and self.getHash(response) is not None:
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

    def html2Text(self, html: str):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        return h.handle(html)

    def getUrlData(self, url: str):
        """
        collects metadata from the given url

        :param url: the url to collect the metadata from
        :return: a dictionary with keys: text, html, cookies and har
        """
        settings = get_project_settings()
        html = None
        if settings.get("SPLASH_URL"):
            result = requests.post(
                settings.get("SPLASH_URL") + "/render.json",
                json={
                    "html": 1,
                    "iframes": 1,
                    "url": url,
                    "wait": settings.get("SPLASH_WAIT"),
                    "headers": settings.get("SPLASH_HEADERS"),
                    "script": 1,
                    "har": 1,
                    "response_body": 1,
                },
            )
            data = result.content.decode("UTF-8")
            j = json.loads(data)
            html = j['html'] if 'html' in j else ''
            text = html
            text += '\n'.join(list(map(lambda x: x["html"], j["childFrames"]))) if 'childFrames' in j else ''
            cookies = result.cookies.get_dict()
            return {"html": html, "text": self.html2Text(text), "cookies": cookies, "har": json.dumps(j["har"])}
        else:
            return {"html": None, "text": None, "cookies": None, "har": None}

    def mapResponse(self, response: scrapy.http.Response, fetchData=True) -> ResponseItemLoader:
        """
        will use the response to populate some fields in the returned Loader

        :param response: the response to use.
        :param fetchData: if True (default) it will collect more metadata from using the response.url,
          otherwise only the HTTP status, headers and url are inserted.
        :return: the populated loader
        """
        r = ResponseItemLoader(response=response)
        r.add_value("status", response.status)
        # r.add_value('body',response.body.decode('utf-8'))

        # render via splash to also get the full javascript rendered content.
        if fetchData:
            data = self.getUrlData(response.url)
            r.add_value("html", data["html"])
            r.add_value("text", data["text"])
            r.add_value("cookies", data["cookies"])
            r.add_value("har", data["har"])
        r.add_value("headers", response.headers)
        r.add_value("url", self.getUri(response))
        return r

    def getValuespaces(self, response) -> ValuespaceItemLoader:
        return ValuespaceItemLoader(response=response)

    def getLOM(self, response) -> LomBaseItemloader:
        lom = LomBaseItemloader(response=response)
        lom.add_value("general", self.getLOMGeneral(response).load_item())
        lifecycle = self.getLOMLifecycle(response)
        if isinstance(lifecycle, LomLifecycleItemloader):
            lom.add_value("lifecycle", lifecycle.load_item())
        else:
            # support yield and generator for multiple values
            for contribute in lifecycle:
                lom.add_value("lifecycle" ,contribute.load_item())
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

    """
    return one or more lifecycle element
    If you want to return more than one, use yield and generate multiple LomLifecycleItemloader
    """
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
