import logging

from .base_classes import EduSharingBase
import converter.env as env


class OEHSpider(EduSharingBase):
    name = "oeh_spider"
    friendlyName = "Open Edu Hub"
    url = "https://redaktion.openeduhub.net/edu-sharing/"
    apiUrl = "https://redaktion.openeduhub.net/edu-sharing/rest/"
    version = "0.1.1"
    mdsId = "mds_oeh"
    importWhitelist: [str] = None
    def __init__(self, **kwargs):
        EduSharingBase.__init__(self, **kwargs)
        importWhitelist = env.get("OEH_IMPORT_SOURCES", True, None)
        if importWhitelist:
            self.importWhitelist = importWhitelist.split(",")
            logging.info("Importing only whitelisted sources: {}".format(self.importWhitelist))

    def getBase(self, response):
        base = EduSharingBase.getBase(self, response)
        base.replace_value("type", self.getProperty("ccm:objecttype", response))
        return base


    def getLOMTechnical(self, response):
        technical = EduSharingBase.getLOMTechnical(self, response)
        if "ccm:wwwurl" in response.meta["item"]["properties"]:
            technical.replace_value("format", "text/html")
            technical.replace_value("location", response.meta["item"]["properties"]["ccm:wwwurl"][0])
        return technical


    def shouldImport(self, response=None):
        if self.importWhitelist:
            source = "oeh"
            if "ccm:replicationsource" in response.meta["item"]["properties"]:
                source = response.meta["item"]["properties"]["ccm:replicationsource"]
                source = source[0] if source and source[0] else "oeh"
            if source not in self.importWhitelist:
                logging.info(
                    "Skipping item {} because it has no whitelisted source {}".format(
                        response.meta["item"]["ref"]["id"], source)
                )
                return False
        if "ccm:collection_io_reference" in response.meta["item"]["aspects"]:
            logging.info(
                "Skipping collection_io_reference with id {}".format(response.meta["item"]["ref"]["id"])
            )
            return False
        return True
