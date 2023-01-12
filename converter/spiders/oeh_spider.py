import logging

import converter.env as env
from .base_classes import EduSharingBase


class OEHSpider(EduSharingBase):
    name = "oeh_spider"
    friendlyName = "Open Edu Hub"
    url = "https://redaktion.openeduhub.net/edu-sharing/"
    apiUrl = "https://redaktion.openeduhub.net/edu-sharing/rest/"
    searchUrl = "search/v1/queries/-home-/"
    version = "0.1.2"  # last update: 2023-01-12
    mdsId = "mds_oeh"
    importWhitelist: [str] = None

    def __init__(self, **kwargs):
        EduSharingBase.__init__(self, **kwargs)
        import_whitelist = env.get("OEH_IMPORT_SOURCES", True, None)
        if import_whitelist:
            self.importWhitelist = import_whitelist.split(";")
            logging.info("Importing only whitelisted sources: {}".format(self.importWhitelist))

    def getBase(self, response):
        base = EduSharingBase.getBase(self, response)
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
            publisher_combined = str()
            if "ccm:replicationsource" in response.meta["item"]["properties"]:
                source = response.meta["item"]["properties"]["ccm:replicationsource"]
                source = source[0] if source and source[0] else "oeh"
            if "ccm:oeh_publisher_combined" in response.meta["item"]["properties"]:
                publisher_combined = response.meta["item"]["properties"]["ccm:oeh_publisher_combined"]
                publisher_combined = publisher_combined[0] if publisher_combined and publisher_combined[0] else "oeh"
            whitelist_hit_source = False
            whitelist_hit_publisher_combined = False
            if source in self.importWhitelist:
                whitelist_hit_source = True
            if publisher_combined in self.importWhitelist:
                whitelist_hit_publisher_combined = True
            if whitelist_hit_source or whitelist_hit_publisher_combined:
                # Item is detected on one whitelist (either 'ccm:replicationsource' or 'ccm:oeh_publisher_combined')
                if whitelist_hit_source:
                    logging.info("Item {} was found on whitelist for 'ccm:replicationsource: {}".format(
                        response.meta["item"]["ref"]["id"], source))
                if whitelist_hit_publisher_combined:
                    logging.info("Item {} was found on whitelist for 'ccm:oeh_publisher_combined': {}".format(
                        response.meta["item"]["ref"]["id"], publisher_combined))
            elif whitelist_hit_source is False and whitelist_hit_publisher_combined is False:
                logging.info(
                    "Skipping item {} because it has no whitelisted 'ccm:replicationsource'-value: {}".format(
                        response.meta["item"]["ref"]["id"], source)
                )
                logging.info(
                    "Skipping item {} because it has no whitelisted 'ccm:oeh_publisher_combined'-value: {}".format(
                        response.meta["item"]["ref"]["id"], publisher_combined))
                return False
        if "ccm:collection_io_reference" in response.meta["item"]["aspects"]:
            logging.info(
                "Skipping collection_io_reference with id {}".format(response.meta["item"]["ref"]["id"])
            )
            return False
        return True
