import time
import uuid
import requests
import json
import base64
from scrapy.utils.project import get_project_settings
from requests.auth import HTTPBasicAuth
import logging

from edu_sharing_client.api_client import ApiClient
from edu_sharing_client.configuration import Configuration
from edu_sharing_client.api.bulk_v1_api import BULKV1Api
from edu_sharing_client.api.iam_v1_api import IAMV1Api
from edu_sharing_client.api.node_v1_api import NODEV1Api
from edu_sharing_client.api.mediacenter_v1_api import MEDIACENTERV1Api
from edu_sharing_client.rest import ApiException
from converter.es_connector_common import transform_item, EduSharingConstants, CreateGroupType
from typing import List
from enum import Enum


# creating the swagger client: java -jar swagger-codegen-cli-3.0.20.jar generate -l python -i http://localhost:8080/edu-sharing/rest/swagger.json -o edu_sharing_swagger -c edu-sharing-swagger.config.json
class ESApiClient(ApiClient):
    COOKIE_REBUILD_THRESHOLD = 60 * 5
    lastRequestTime = 0

    def deserialize(self, response, response_type):
        """Deserializes response into an object.

        :param response: RESTResponse object to be deserialized.
        :param response_type: class literal for
            deserialized object, or string of class name.

        :return: deserialized object.
        """
        # handle file downloading
        # save response body into a tmp file and return the instance
        if response_type == "file":
            return self.__deserialize_file(response)

        # fetch data from response object
        try:
            data = json.loads(response.data)
        except ValueError:
            data = response.data
        # workaround for es: simply return to prevent error throwing
        # return self.__deserialize(data, response_type)
        return data

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            def newfunc(*args, **kwargs):
                if time.time() - ESApiClient.lastRequestTime > ESApiClient.COOKIE_REBUILD_THRESHOLD:
                    EduSharing.initCookie()
                    self.cookie =  EduSharing.cookie

                # store last request time
                ESApiClient.lastRequestTime = time.time()
                return attr(*args, **kwargs)


            return newfunc
        else:
            return attr



class EduSharing:
    cookie: str = None
    resetVersion: bool = False
    apiClient: ESApiClient
    bulkApi: BULKV1Api
    iamApi: IAMV1Api
    mediacenterApi: MEDIACENTERV1Api
    nodeApi: NODEV1Api
    groupCache: List[str]

    def __init__(self):
        self.initApiClient()

    def getHeaders(self, contentType="application/json"):
        return {
            "COOKIE": EduSharing.cookie,
            "Accept": "application/json",
            "Content-Type": contentType,
        }

    def syncNode(self, spider, type, properties):
        groupBy = []
        if "ccm:replicationsourceorigin" in properties:
            groupBy = ["ccm:replicationsourceorigin"]
        try:
            response = EduSharing.bulkApi.sync(
                body=properties,
                match=["ccm:replicationsource", "ccm:replicationsourceid"],
                type=type,
                group=spider.name,
                group_by=groupBy,
                reset_version=EduSharing.resetVersion,
            )
        except ApiException as e:
            jsonError = json.loads(e.body)
            if jsonError["error"] == "java.lang.IllegalStateException":
                logging.warning("Node '" + properties['cm:name'][0] + "' probably blocked for sync: " + jsonError["message"])
                return None
            raise e
        return response["node"]

    def setNodeText(self, uuid, item) -> bool:
        if "fulltext" in item:
            response = requests.post(
                get_project_settings().get("EDU_SHARING_BASE_URL")
                + "rest/node/v1/nodes/-home-/"
                + uuid
                + "/textContent?mimetype=text/plain",
                headers=self.getHeaders("multipart/form-data"),
                data=item["fulltext"].encode("utf-8"),
            )
            return response.status_code == 200
            # does currently not store data
            # try:
            #     EduSharing.nodeApi.change_content_as_text(EduSharingConstants.HOME, uuid, 'text/plain',item['fulltext'])
            #     return True
            # except ApiException as e:
            #     print(e)
            #     return False

    def setPermissions(self, uuid, permissions) -> bool:
        try:
            EduSharing.nodeApi.set_permission(
                repository=EduSharingConstants.HOME,
                node=uuid,
                body=permissions,
                send_mail=False,
                send_copy=False,
            )
            return True
        except ApiException as e:
            return False

    def setNodePreview(self, uuid, item) -> bool:
        if "thumbnail" in item:
            key = (
                "large"
                if "large" in item["thumbnail"]
                else "small"
                if "small" in item["thumbnail"]
                else None
            )
            if key:
                files = {"image": base64.b64decode(item["thumbnail"][key])}
                response = requests.post(
                    get_project_settings().get("EDU_SHARING_BASE_URL")
                    + "rest/node/v1/nodes/-home-/"
                    + uuid
                    + "/preview?mimetype="
                    + item["thumbnail"]["mimetype"],
                    headers=self.getHeaders(None),
                    files=files,
                )
                return response.status_code == 200
        else:
            if get_project_settings().get("DISABLE_SCRAPY") is False:
                logging.warning("No thumbnail provided for " + uuid)

    def createGroupsIfNotExists(self, groups, type: CreateGroupType):
        for group in groups:
            if type == CreateGroupType.MediaCenter:
                uuid = (
                    EduSharingConstants.GROUP_PREFIX
                    + EduSharingConstants.MEDIACENTER_PREFIX
                    + group
                )
            else:
                uuid = EduSharingConstants.GROUP_PREFIX + group
            if uuid in EduSharing.groupCache:
                logging.debug(
                    "Group " + uuid + " is existing in cache, no need to create"
                )
                continue
            logging.debug("Group " + uuid + " is not in cache, checking consistency...")
            try:
                group = EduSharing.iamApi.get_group(EduSharingConstants.HOME, uuid)
                logging.info(
                    "Group "
                    + uuid
                    + " was found in edu-sharing (cache inconsistency), no need to create"
                )
                EduSharing.groupCache.append(uuid)
                continue
            except ApiException as e:
                logging.info(
                    "Group " + uuid + " was not found in edu-sharing, creating it"
                )
                pass

            if type == CreateGroupType.MediaCenter:
                result = EduSharing.mediacenterApi.create_mediacenter(
                    repository=EduSharingConstants.HOME,
                    mediacenter=group,
                    body={"mediacenter": {}, "displayName": group},
                )
                EduSharing.groupCache.append(result["authorityName"])
            else:
                result = EduSharing.iamApi.create_group(
                    repository=EduSharingConstants.HOME, group=group, body={}
                )
                EduSharing.groupCache.append(result["authorityName"])

    def setNodePermissions(self, uuid, item):
        if "permissions" in item:
            permissions = {
                "inherited": True,  # let inherited = true to add additional permissions via edu-sharing
                "permissions": [],
            }
            public = item["permissions"]["public"]
            if public == True:
                if (
                    "groups" in item["permissions"]
                    or "mediacenters" in item["permissions"]
                ):
                    logging.error(
                        "Invalid state detected: Permissions public is set to true but groups or mediacenters are also set. Please use either public = true without groups/mediacenters or public = false and set group/mediacenters. No permissions will be set!"
                    )
                    return
                permissions["permissions"].append(
                    {
                        "authority": {
                            "authorityName": EduSharingConstants.GROUP_EVERYONE,
                            "authorityType": EduSharingConstants.AUTHORITYTYPE_EVERYONE,
                        },
                        "permissions": [
                            EduSharingConstants.PERMISSION_CONSUMER,
                            EduSharingConstants.PERMISSION_CCPUBLISH,
                        ],
                    }
                )
            else:
                # Makes not much sense, may no permissions at all should be set
                # if not 'groups' in item['permissions'] and not 'mediacenters' in item['permissions']:
                #    logging.error('Invalid state detected: Permissions public is set to false but neither groups or mediacenters are set. Please use either public = true without groups/mediacenters or public = false and set group/mediacenters. No permissions will be set!')
                #    return
                mergedGroups = []
                if "groups" in item["permissions"]:
                    if (
                        "autoCreateGroups" in item["permissions"]
                        and item["permissions"]["autoCreateGroups"] == True
                    ):
                        self.createGroupsIfNotExists(
                            item["permissions"]["groups"],
                            CreateGroupType.Regular,
                        )
                    mergedGroups = mergedGroups + list(
                        map(
                            lambda x: EduSharingConstants.GROUP_PREFIX + x,
                            item["permissions"]["groups"],
                        )
                    )
                if "mediacenters" in item["permissions"]:
                    if (
                        "autoCreateMediacenters" in item["permissions"]
                        and item["permissions"]["autoCreateMediacenters"] == True
                    ):
                        self.createGroupsIfNotExists(
                            item["permissions"]["mediacenters"],
                            CreateGroupType.MediaCenter,
                        )
                    mergedGroups = mergedGroups + list(
                        map(
                            lambda x: EduSharingConstants.GROUP_PREFIX
                            + EduSharingConstants.MEDIACENTER_PROXY_PREFIX
                            + x,
                            item["permissions"]["mediacenters"],
                        )
                    )
                for group in mergedGroups:
                    permissions["permissions"].append(
                        {
                            "authority": {
                                "authorityName": group,
                                "authorityType": EduSharingConstants.AUTHORITYTYPE_GROUP,
                            },
                            "permissions": [
                                EduSharingConstants.PERMISSION_CONSUMER,
                                EduSharingConstants.PERMISSION_CCPUBLISH,
                            ],
                        }
                    )
            if not self.setPermissions(uuid, permissions):
                logging.error(
                    "Failed to set permissions, please check that the given groups/mediacenters are existing in the repository or set the autoCreate mode to true"
                )
                logging.error(item["permissions"])

    def insertItem(self, spider, uuid, item):
        node = self.syncNode(spider, "ccm:io", transform_item(uuid, spider, item))
        self.setNodePermissions(node["ref"]["id"], item)
        self.setNodePreview(node["ref"]["id"], item)
        self.setNodeText(node["ref"]["id"], item)

    def updateItem(self, spider, uuid, item):
        self.insertItem(spider, uuid, item)
    @staticmethod
    def initCookie():
        settings = get_project_settings()
        auth = requests.get(
            settings.get("EDU_SHARING_BASE_URL")
            + "rest/authentication/v1/validateSession",
            auth=HTTPBasicAuth(
                settings.get("EDU_SHARING_USERNAME"),
                settings.get("EDU_SHARING_PASSWORD"),
            ),
            headers={"Accept": "application/json"},
        )
        isAdmin = json.loads(auth.text)["isAdmin"]
        if isAdmin:
            EduSharing.cookie = auth.headers["SET-COOKIE"].split(";")[0]
        return auth
    def initApiClient(self):
        if EduSharing.cookie == None:
            settings = get_project_settings()
            auth = self.initCookie()
            isAdmin = json.loads(auth.text)["isAdmin"]
            if isAdmin:
                configuration = Configuration()
                configuration.host = settings.get("EDU_SHARING_BASE_URL") + "rest"
                EduSharing.apiClient = ESApiClient(
                    configuration,
                    cookie=EduSharing.cookie,
                    header_name="Accept",
                    header_value="application/json",
                )
                EduSharing.bulkApi = BULKV1Api(EduSharing.apiClient)
                EduSharing.iamApi = IAMV1Api(EduSharing.apiClient)
                EduSharing.mediacenterApi = MEDIACENTERV1Api(EduSharing.apiClient)
                EduSharing.nodeApi = NODEV1Api(EduSharing.apiClient)
                EduSharing.groupCache = list(
                    map(
                        lambda x: x["authorityName"],
                        EduSharing.iamApi.search_groups(
                            EduSharingConstants.HOME, "", max_items=1000000
                        )["groups"],
                    )
                )
                logging.debug("Built up edu-sharing group cache", EduSharing.groupCache)
                return
            logging.warning(auth.text)
            raise Exception(
                "Could not authentify as admin at edu-sharing. Please check your settings for repository "
                + settings.get("EDU_SHARING_BASE_URL")
            )

    def buildUUID(self, url):
        return str(uuid.uuid5(uuid.NAMESPACE_URL, url))

    def uuidExists(self, uuid):
        return False

    def findItem(self, id, spider):
        properties = {
            "ccm:replicationsource": [spider.name],
            "ccm:replicationsourceid": [id],
        }
        try:
            response = EduSharing.bulkApi.find(properties)
            properties = response["node"]["properties"]
            if (
                "ccm:replicationsourcehash" in properties
                and "ccm:replicationsourceuuid" in properties
            ):
                return [
                    properties["ccm:replicationsourceuuid"][0],
                    properties["ccm:replicationsourcehash"][0],
                ]
        except ApiException as e:
            if e.status == 404:
                pass
            else:
                raise e
        return None

    def findSource(self, spider):
        return True

    def createSource(self, spider):
        # src = self.createNode(EduSharing.etlFolder['ref']['id'], 'ccm:map', {'cm:name' : [spider.name]})
        # EduSharing.spiderNodes[spider.name] = src
        # return src
        return None
