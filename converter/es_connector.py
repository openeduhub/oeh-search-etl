import base64
import collections
import json
import logging
import time
import uuid
from enum import Enum
from typing import List

import requests
import vobject
from requests.auth import HTTPBasicAuth
from scrapy.utils.project import get_project_settings
from vobject.vcard import VCardBehavior

from converter import env
from converter.constants import Constants
from edu_sharing_client.api.bulk_v1_api import BULKV1Api
from edu_sharing_client.api.iam_v1_api import IAMV1Api
from edu_sharing_client.api.mediacenter_v1_api import MEDIACENTERV1Api
from edu_sharing_client.api.node_v1_api import NODEV1Api
from edu_sharing_client.api_client import ApiClient
from edu_sharing_client.configuration import Configuration
from edu_sharing_client.rest import ApiException


class EduSharingConstants:
    HOME = "-home-"
    GROUP_EVERYONE = "GROUP_EVERYONE"
    AUTHORITYTYPE_GROUP = "GROUP"
    AUTHORITYTYPE_EVERYONE = "EVERYONE"
    PERMISSION_CONSUMER = "Consumer"
    PERMISSION_CCPUBLISH = "CCPublish"
    GROUP_PREFIX = "GROUP_"
    MEDIACENTER_PREFIX = "MEDIA_CENTER_"
    MEDIACENTER_PROXY_PREFIX = "MEDIA_CENTER_PROXY_"
    LIFECYCLE_ROLES_MAPPING = {
        "publisher": "ccm:lifecyclecontributer_publisher",
        "author": "ccm:lifecyclecontributer_author",
        "editor": "ccm:lifecyclecontributer_editor",
        "metadata_creator": "ccm:metadatacontributer_creator",
        "metadata_provider": "ccm:metadatacontributer_provider",
    }


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
                    self.cookie = EduSharing.cookie

                # store last request time
                ESApiClient.lastRequestTime = time.time()
                return attr(*args, **kwargs)

            return newfunc
        else:
            return attr


class EduSharing:
    class CreateGroupType(Enum):
        Regular = 1
        MediaCenter = 2

    cookie: str = None
    resetVersion: bool = False
    apiClient: ESApiClient
    bulkApi: BULKV1Api
    iamApi: IAMV1Api
    mediacenterApi: MEDIACENTERV1Api
    nodeApi: NODEV1Api
    groupCache: List[str]
    enabled: bool

    def __init__(self):
        self.enabled = env.get("MODE", default="edu-sharing") == "edu-sharing"
        if self.enabled:
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
                logging.warning(
                    "Node '" + properties['cm:name'][0] + "' probably blocked for sync: " + jsonError["message"])
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

    def setNodeBinaryData(self, uuid, item) -> bool:
        if "binary" in item:
            logging.info(get_project_settings().get("EDU_SHARING_BASE_URL")
                         + "rest/node/v1/nodes/-home-/"
                         + uuid
                         + "/content?mimetype="
                         + item["lom"]["technical"]["format"]
                         )
            files = {"file": item["binary"]}
            response = requests.post(
                get_project_settings().get("EDU_SHARING_BASE_URL")
                + "rest/node/v1/nodes/-home-/"
                + uuid
                + "/content?mimetype="
                + item["lom"]["technical"]["format"],
                headers=self.getHeaders(None),
                files=files,
            )
            return response.status_code == 200
        else:
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
            logging.warning("No thumbnail provided for " + uuid)

    def mapLicense(self, spaces, license):
        if "url" in license:
            match license["url"]:
                case Constants.LICENSE_CC_BY_30:
                    spaces["ccm:commonlicense_key"] = "CC_BY"
                    spaces["ccm:commonlicense_cc_version"] = "3.0"
                case Constants.LICENSE_CC_BY_40:
                    spaces["ccm:commonlicense_key"] = "CC_BY"
                    spaces["ccm:commonlicense_cc_version"] = "4.0"
                case Constants.LICENSE_CC_BY_NC_30:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC"
                    spaces["ccm:commonlicense_cc_version"] = "3.0"
                case Constants.LICENSE_CC_BY_NC_40:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC"
                    spaces["ccm:commonlicense_cc_version"] = "4.0"
                case Constants.LICENSE_CC_BY_NC_ND_30:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_ND"
                    spaces["ccm:commonlicense_cc_version"] = "3.0"
                case Constants.LICENSE_CC_BY_NC_ND_40:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_ND"
                    spaces["ccm:commonlicense_cc_version"] = "4.0"
                case Constants.LICENSE_CC_BY_NC_SA_30:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_SA"
                    spaces["ccm:commonlicense_cc_version"] = "3.0"
                case Constants.LICENSE_CC_BY_NC_SA_40:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_SA"
                    spaces["ccm:commonlicense_cc_version"] = "4.0"
                case Constants.LICENSE_CC_BY_ND_30:
                    spaces["ccm:commonlicense_key"] = "CC_BY_ND"
                    spaces["ccm:commonlicense_cc_version"] = "3.0"
                case Constants.LICENSE_CC_BY_ND_40:
                    spaces["ccm:commonlicense_key"] = "CC_BY_ND"
                    spaces["ccm:commonlicense_cc_version"] = "4.0"
                case Constants.LICENSE_CC_BY_SA_30:
                    spaces["ccm:commonlicense_key"] = "CC_BY_SA"
                    spaces["ccm:commonlicense_cc_version"] = "3.0"
                case Constants.LICENSE_CC_BY_SA_40:
                    spaces["ccm:commonlicense_key"] = "CC_BY_SA"
                    spaces["ccm:commonlicense_cc_version"] = "4.0"
                case Constants.LICENSE_CC_ZERO_10:
                    spaces["ccm:commonlicense_key"] = "CC_0"
                    spaces["ccm:commonlicense_cc_version"] = "1.0"
                case Constants.LICENSE_PDM:
                    spaces["ccm:commonlicense_key"] = "PDM"
                case _:
                    logging.warning(f"License.url {license['url']} could not be mapped to a license from Constants.\n"
                                    f"If you are sure that you provided a correct URL to a license, "
                                    f"please check if the license-mapping within es_connector.py is up-to-date.")
        if "internal" in license:
            match license["internal"]:
                case Constants.LICENSE_COPYRIGHT_LAW:
                    spaces["ccm:commonlicense_key"] = "COPYRIGHT_FREE"
                case Constants.LICENSE_CUSTOM:
                    spaces["ccm:commonlicense_key"] = "CUSTOM"
                    if "description" in license:
                        spaces["cclom:rights_description"] = license["description"]
                case _:
                    logging.warning(f"Received a value for license['internal'] that is not recognized by es_connector."
                                    f"Please double-check if the provided value {license['internal']} is correctly "
                                    f"mapped within Constants AND es_connector.")

        if "author" in license:
            spaces["ccm:author_freetext"] = license["author"]

        if "expirationDate" in license:
            spaces["ccm:license_to"] = [license["expirationDate"].isoformat()]

    def transformItem(self, uuid, spider, item):
        spaces = {
            "ccm:replicationsource": spider.name,
            "ccm:replicationsourceid": item["sourceId"],
            "ccm:replicationsourcehash": item["hash"],
            "ccm:replicationsourceuuid": uuid,
            "cm:name": item["lom"]["general"]["title"],
            "ccm:wwwurl": item["lom"]["technical"]["location"][0]
            if "location" in item["lom"]["technical"] else None,
            "cclom:location": item["lom"]["technical"]["location"]
            if "location" in item["lom"]["technical"] else None,
            "cclom:format": item["lom"]["technical"]["format"] if "format" in item["lom"]["technical"] else None,
            "cclom:aggregationlevel": item["lom"]["general"]["aggregationLevel"] if "aggregationLevel" in item["lom"]["general"] else None,
            "cclom:title": item["lom"]["general"]["title"],
            "cclom:general_identifier": item["lom"]["general"]["identifier"]
        }
        if "notes" in item:
            spaces["ccm:notes"] = item["notes"]
        if "origin" in item:
            spaces["ccm:replicationsourceorigin"] = item[
                "origin"
            ]  # TODO currently not mapped in edu-sharing

        self.mapLicense(spaces, item["license"])
        if "description" in item["lom"]["general"]:
            spaces["cclom:general_description"] = item["lom"]["general"]["description"]

        if "identifier" in item["lom"]["general"]:
            spaces["cclom:general_identifier"] = item["lom"]["general"]["identifier"]

        if "language" in item["lom"]["general"]:
            spaces["cclom:general_language"] = item["lom"]["general"]["language"]

        if "keyword" in item["lom"]["general"]:
            spaces["cclom:general_keyword"] = (item["lom"]["general"]["keyword"],)
        else:
            spaces["cclom:general_keyword"] = None
        if "technical" in item["lom"]:
            if "duration" in item["lom"]["technical"]:
                duration = item["lom"]["technical"]["duration"]
                try:
                    # edusharing requires milliseconds
                    duration = int(float(duration) * 1000)
                except:
                    pass
                spaces["cclom:duration"] = duration

        # TODO: this does currently not support multiple values per role
        if "lifecycle" in item["lom"]:
            for person in item["lom"]["lifecycle"]:
                if not "role" in person:
                    continue
                if (
                        not person["role"].lower()
                            in EduSharingConstants.LIFECYCLE_ROLES_MAPPING
                ):
                    logging.warning(
                        "The lifecycle role "
                        + person["role"]
                        + " is currently not supported by the edu-sharing connector"
                    )
                    continue
                mapping = EduSharingConstants.LIFECYCLE_ROLES_MAPPING[
                    person["role"].lower()
                ]
                # convert to a vcard string
                firstName = person["firstName"] if "firstName" in person else ""
                lastName = person["lastName"] if "lastName" in person else ""
                organization = (
                    person["organization"] if "organization" in person else ""
                )
                url = person["url"] if "url" in person else ""
                email = person["email"] if "email" in person else ""
                date = person["date"] if "date" in person else None
                vcard = vobject.vCard()
                vcard.add("n").value = vobject.vcard.Name(
                    family=lastName, given=firstName
                )
                vcard.add("fn").value = (
                    organization
                    if organization
                    else (firstName + " " + lastName).strip()
                )
                if date:
                    vcard.add("X-ES-LOM-CONTRIBUTE-DATE").value = date.isoformat()
                    if person["role"].lower() == 'publisher':
                        spaces["ccm:published_date"] = date.isoformat()
                if organization:
                    vcard.add("org")
                    # fix a bug of splitted org values
                    vcard.org.behavior = VCardBehavior.defaultBehavior
                    vcard.org.value = organization
                vcard.add("url").value = url
                if email:
                    vcard.add("EMAIL;TYPE=PREF,INTERNET").value = email
                spaces[mapping] = [vcard.serialize()]

        valuespaceMapping = {
            "discipline": "ccm:taxonid",
            "intendedEndUserRole": "ccm:educationalintendedenduserrole",
            "educationalContext": "ccm:educationalcontext",
            "learningResourceType": "ccm:educationallearningresourcetype",
            "new_lrt": "ccm:oeh_lrt",
            "sourceContentType": "ccm:sourceContentType",
            "toolCategory": "ccm:toolCategory",
            "conditionsOfAccess": "ccm:conditionsOfAccess",
            "containsAdvertisement": "ccm:containsAdvertisement",
            "price": "ccm:price",
            "accessibilitySummary": "ccm:accessibilitySummary",
            "dataProtectionConformity": "ccm:dataProtectionConformity",
            "fskRating": "ccm:fskRating",
            "oer": "ccm:license_oer",
        }
        for key in item["valuespaces"]:
            spaces[valuespaceMapping[key]] = item["valuespaces"][key]
        if "typicalAgeRange" in item["lom"]["educational"]:
            tar = item["lom"]["educational"]["typicalAgeRange"]
            if "fromRange" in tar:
                spaces["ccm:educationaltypicalagerange_from"] = tar["fromRange"]
            if "toRange" in tar:
                spaces["ccm:educationaltypicalagerange_to"] = tar["toRange"]

        # map custom fields directly into the edu-sharing properties
        if "custom" in item:
            for key in item["custom"]:
                spaces[key] = item["custom"][key]

        # intendedEndUserRole = Field(output_processor=JoinMultivalues())
        # discipline = Field(output_processor=JoinMultivalues())
        # educationalContext = Field(output_processor=JoinMultivalues())
        # learningResourceType = Field(output_processor=JoinMultivalues())
        # sourceContentType = Field(output_processor=JoinMultivalues())
        mdsId = env.get("EDU_SHARING_METADATASET", allow_null=True, default="mds_oeh")
        if mdsId != "default":
            spaces["cm:edu_metadataset"] = mdsId
            spaces["cm:edu_forcemetadataset"] = "true"
        for key in spaces:
            if type(spaces[key]) is tuple:
                spaces[key] = list([x for y in spaces[key] for x in y])
            if not type(spaces[key]) is list:
                spaces[key] = [spaces[key]]

        return spaces

    def createGroupsIfNotExists(self, groups, type: CreateGroupType):
        for group in groups:
            if type == EduSharing.CreateGroupType.MediaCenter:
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

            if type == EduSharing.CreateGroupType.MediaCenter:
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
                            EduSharing.CreateGroupType.Regular,
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
                            EduSharing.CreateGroupType.MediaCenter,
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
        node = self.syncNode(spider, "ccm:io", self.transformItem(uuid, spider, item))
        self.setNodePermissions(node["ref"]["id"], item)
        self.setNodePreview(node["ref"]["id"], item)
        if not self.setNodeBinaryData(node["ref"]["id"], item):
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
            cookies = []
            for cookie in auth.headers["SET-COOKIE"].split(","):
                cookies.append(cookie.split(";")[0])
            EduSharing.cookie = ";".join(cookies)
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
                logging.debug("Built up edu-sharing group cache: {}".format(EduSharing.groupCache))
                return
            logging.warning(auth.text)
            raise Exception(
                "Could not authentify as admin at edu-sharing. Please check your settings for repository "
                + settings.get("EDU_SHARING_BASE_URL")
            )

    @staticmethod
    def buildUUID(url):
        return str(uuid.uuid5(uuid.NAMESPACE_URL, url))

    def uuidExists(self, uuid):
        return False

    def findItem(self, id, spider):
        if not self.enabled:
            return None
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
