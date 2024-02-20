import asyncio
import base64
import json
import logging
import time
import uuid
from asyncio import Semaphore
from enum import Enum
from typing import List

import httpx
import requests
import vobject
from requests.auth import HTTPBasicAuth
from scrapy.utils.project import get_project_settings
from vobject.vcard import VCardBehavior

from converter import env
from converter.constants import Constants
from edu_sharing_client import ABOUTApi
from edu_sharing_client.api.bulk_v1_api import BULKV1Api
from edu_sharing_client.api.iam_v1_api import IAMV1Api
from edu_sharing_client.api.mediacenter_v1_api import MEDIACENTERV1Api
from edu_sharing_client.api.node_v1_api import NODEV1Api
from edu_sharing_client.api_client import ApiClient
from edu_sharing_client.configuration import Configuration
from edu_sharing_client.rest import ApiException

log = logging.getLogger(__name__)


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
        "author": "ccm:lifecyclecontributer_author",
        "editor": "ccm:lifecyclecontributer_editor",
        "metadata_creator": "ccm:metadatacontributer_creator",
        "metadata_provider": "ccm:metadatacontributer_provider",
        "publisher": "ccm:lifecyclecontributer_publisher",
        "unknown": "ccm:lifecyclecontributer_unknown",  # (= contributor in an unknown capacity ("Mitarbeiter"))
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
        if hasattr(attr, "__call__"):

            def newfunc(*args, **kwargs):
                if time.time() - ESApiClient.lastRequestTime > ESApiClient.COOKIE_REBUILD_THRESHOLD:
                    EduSharing.init_cookie()
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
    version: any
    apiClient: ESApiClient
    aboutApi: ABOUTApi
    bulkApi: BULKV1Api
    iamApi: IAMV1Api
    mediacenterApi: MEDIACENTERV1Api
    nodeApi: NODEV1Api
    groupCache: List[str]
    enabled: bool
    _client_async = httpx.AsyncClient()
    _sem: Semaphore = asyncio.Semaphore(25)

    def __init__(self):
        cookie_threshold = env.get("EDU_SHARING_COOKIE_REBUILD_THRESHOLD", True)
        if cookie_threshold:
            log.info("Setting COOKIE_REBUILD_THRESHOLD to " + str(cookie_threshold) + " seconds")
            self.COOKIE_REBUILD_THRESHOLD = cookie_threshold
        self.enabled = env.get("MODE", default="edu-sharing") == "edu-sharing"
        if self.enabled:
            self.init_api_client()

    def get_headers(self, content_type: str | None = "application/json"):
        header_dict: dict = dict()  # result dict that only contains values, no NoneTypes!
        header_dict.update({"Accept": "application/json"})
        if EduSharing.cookie:
            header_dict.update({"COOKIE": EduSharing.cookie})
        if content_type:
            header_dict.update({"Content-Type": content_type})
        return header_dict

    def sync_node(self, spider, type, properties):
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
            # ToDo:
            #  - error-handling for code 500 ("java.util.concurrent.TimeoutException")
            try:
                json_error: dict = json.loads(e.body)
                if json_error["error"] == "java.lang.IllegalStateException":
                    log.warning(
                        "Node '" + properties["cm:name"][0] + "' probably blocked for sync: " + json_error["message"]
                    )
                    return None
            except json.JSONDecodeError:
                log.error(
                    f"ES_CONNECTOR: edu-sharing ApiException 'body'-attribute was't a deserializable JSON "
                    f"String for item '{properties['cm:name'][0]}' "
                    f"(replicationsourceid: '{properties['ccm:replicationsourceid']}'). "
                    f'edu-sharing returned the following exception:\n"{e.body}"'
                )
            raise e
        return response["node"]

    async def set_node_text(self, uuid, item) -> bool:
        if "fulltext" in item:
            response = await self._client_async.post(
                get_project_settings().get("EDU_SHARING_BASE_URL")
                + "rest/node/v1/nodes/-home-/"
                + uuid
                + "/textContent?mimetype=text/plain",
                headers=self.get_headers("multipart/form-data"),
                data=item["fulltext"].encode("utf-8"),
                timeout=None,
            )
            return response.status_code == 200
        # does currently not store data
        # try:
        #     EduSharing.nodeApi.change_content_as_text(EduSharingConstants.HOME, uuid, 'text/plain',item['fulltext'])
        #     return True
        # except ApiException as e:
        #     print(e)
        #     return False

    def set_permissions(self, uuid, permissions) -> bool:
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

    async def set_node_binary_data(self, uuid, item) -> bool:
        if "binary" in item:
            log.info(
                get_project_settings().get("EDU_SHARING_BASE_URL")
                + "rest/node/v1/nodes/-home-/"
                + uuid
                + "/content?mimetype="
                + item["lom"]["technical"]["format"]
            )
            files = {"file": item["binary"]}
            response = await self._client_async.post(
                get_project_settings().get("EDU_SHARING_BASE_URL")
                + "rest/node/v1/nodes/-home-/"
                + uuid
                + "/content?mimetype="
                + item["lom"]["technical"]["format"],
                headers=self.get_headers(None),
                files=files,
                timeout=None,
            )
            return response.status_code == 200
        else:
            return False

    async def set_node_preview(self, uuid, item) -> bool:
        if "thumbnail" in item:
            key = "large" if "large" in item["thumbnail"] else "small" if "small" in item["thumbnail"] else None
            if key:
                files = {"image": base64.b64decode(item["thumbnail"][key])}
                response = await self._client_async.post(
                    get_project_settings().get("EDU_SHARING_BASE_URL")
                    + "rest/node/v1/nodes/-home-/"
                    + uuid
                    + "/preview?mimetype="
                    + item["thumbnail"]["mimetype"],
                    headers=self.get_headers(None),
                    files=files,
                    timeout=None,
                )
                return response.status_code == 200
        else:
            log.warning("No thumbnail provided for " + uuid)

    def map_license(self, spaces, license):
        if "url" in license:
            match license["url"]:
                # ToDo: refactor this ungodly method asap
                case Constants.LICENSE_CC_BY_10:
                    spaces["ccm:commonlicense_key"] = "CC_BY"
                    spaces["ccm:commonlicense_cc_version"] = "1.0"
                case Constants.LICENSE_CC_BY_20:
                    spaces["ccm:commonlicense_key"] = "CC_BY"
                    spaces["ccm:commonlicense_cc_version"] = "2.0"
                case Constants.LICENSE_CC_BY_25:
                    spaces["ccm:commonlicense_key"] = "CC_BY"
                    spaces["ccm:commonlicense_cc_version"] = "2.5"
                case Constants.LICENSE_CC_BY_30:
                    spaces["ccm:commonlicense_key"] = "CC_BY"
                    spaces["ccm:commonlicense_cc_version"] = "3.0"
                case Constants.LICENSE_CC_BY_40:
                    spaces["ccm:commonlicense_key"] = "CC_BY"
                    spaces["ccm:commonlicense_cc_version"] = "4.0"
                case Constants.LICENSE_CC_BY_NC_10:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC"
                    spaces["ccm:commonlicense_cc_version"] = "1.0"
                case Constants.LICENSE_CC_BY_NC_20:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC"
                    spaces["ccm:commonlicense_cc_version"] = "2.0"
                case Constants.LICENSE_CC_BY_NC_25:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC"
                    spaces["ccm:commonlicense_cc_version"] = "2.5"
                case Constants.LICENSE_CC_BY_NC_30:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC"
                    spaces["ccm:commonlicense_cc_version"] = "3.0"
                case Constants.LICENSE_CC_BY_NC_40:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC"
                    spaces["ccm:commonlicense_cc_version"] = "4.0"
                case Constants.LICENSE_CC_BY_NC_ND_20:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_ND"
                    spaces["ccm:commonlicense_cc_version"] = "2.0"
                case Constants.LICENSE_CC_BY_NC_ND_25:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_ND"
                    spaces["ccm:commonlicense_cc_version"] = "2.5"
                case Constants.LICENSE_CC_BY_NC_ND_30:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_ND"
                    spaces["ccm:commonlicense_cc_version"] = "3.0"
                case Constants.LICENSE_CC_BY_NC_ND_40:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_ND"
                    spaces["ccm:commonlicense_cc_version"] = "4.0"
                case Constants.LICENSE_CC_BY_NC_SA_10:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_SA"
                    spaces["ccm:commonlicense_cc_version"] = "1.0"
                case Constants.LICENSE_CC_BY_NC_SA_20:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_SA"
                    spaces["ccm:commonlicense_cc_version"] = "2.0"
                case Constants.LICENSE_CC_BY_NC_SA_25:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_SA"
                    spaces["ccm:commonlicense_cc_version"] = "2.5"
                case Constants.LICENSE_CC_BY_NC_SA_30:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_SA"
                    spaces["ccm:commonlicense_cc_version"] = "3.0"
                case Constants.LICENSE_CC_BY_NC_SA_40:
                    spaces["ccm:commonlicense_key"] = "CC_BY_NC_SA"
                    spaces["ccm:commonlicense_cc_version"] = "4.0"
                case Constants.LICENSE_CC_BY_ND_10:
                    spaces["ccm:commonlicense_key"] = "CC_BY_ND"
                    spaces["ccm:commonlicense_cc_version"] = "1.0"
                case Constants.LICENSE_CC_BY_ND_20:
                    spaces["ccm:commonlicense_key"] = "CC_BY_ND"
                    spaces["ccm:commonlicense_cc_version"] = "2.0"
                case Constants.LICENSE_CC_BY_ND_25:
                    spaces["ccm:commonlicense_key"] = "CC_BY_ND"
                    spaces["ccm:commonlicense_cc_version"] = "2.5"
                case Constants.LICENSE_CC_BY_ND_30:
                    spaces["ccm:commonlicense_key"] = "CC_BY_ND"
                    spaces["ccm:commonlicense_cc_version"] = "3.0"
                case Constants.LICENSE_CC_BY_ND_40:
                    spaces["ccm:commonlicense_key"] = "CC_BY_ND"
                    spaces["ccm:commonlicense_cc_version"] = "4.0"
                case Constants.LICENSE_CC_BY_SA_10:
                    spaces["ccm:commonlicense_key"] = "CC_BY_SA"
                    spaces["ccm:commonlicense_cc_version"] = "1.0"
                case Constants.LICENSE_CC_BY_SA_20:
                    spaces["ccm:commonlicense_key"] = "CC_BY_SA"
                    spaces["ccm:commonlicense_cc_version"] = "2.0"
                case Constants.LICENSE_CC_BY_SA_25:
                    spaces["ccm:commonlicense_key"] = "CC_BY_SA"
                    spaces["ccm:commonlicense_cc_version"] = "2.5"
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
                    log.warning(
                        f"License.url {license['url']} could not be mapped to a license from Constants.\n"
                        f"If you are sure that you provided a correct URL to a license, "
                        f"please check if the license-mapping within es_connector.py is up-to-date."
                    )
        if "internal" in license:
            match license["internal"]:
                case "CC_0" | "CC_BY" | "CC_BY_NC" | "CC_BY_NC_ND" | "CC_BY_NC_SA" | "CC_BY_ND" | "CC_BY_SA" | "PDM" | Constants.LICENSE_COPYRIGHT_FREE | Constants.LICENSE_COPYRIGHT_LAW | Constants.LICENSE_SCHULFUNK | Constants.LICENSE_UNTERRICHTS_UND_SCHULMEDIEN:
                    spaces["ccm:commonlicense_key"] = license["internal"]
                case Constants.LICENSE_CUSTOM:
                    spaces["ccm:commonlicense_key"] = "CUSTOM"
                    if "description" in license:
                        spaces["cclom:rights_description"] = license["description"]
                case _:
                    log.warning(
                        f"Received a value for license['internal'] that is not recognized by es_connector. "
                        f"Please double-check if the provided value {license['internal']} is correctly "
                        f"mapped within Constants AND es_connector."
                    )

        if "author" in license:
            spaces["ccm:author_freetext"] = license["author"]

        if "expirationDate" in license:
            spaces["ccm:license_to"] = [license["expirationDate"].isoformat()]

    def transform_item(self, uuid, spider, item):
        spaces = {
            "ccm:replicationsource": spider.name,
            "ccm:replicationsourceid": item["sourceId"],
            "ccm:replicationsourcehash": item["hash"],
            "ccm:replicationsourceuuid": uuid,
            "cm:name": item["lom"]["general"]["title"],
            "ccm:wwwurl": item["lom"]["technical"]["location"][0] if "location" in item["lom"]["technical"] else None,
            "cclom:location": item["lom"]["technical"]["location"] if "location" in item["lom"]["technical"] else None,
            "cclom:format": item["lom"]["technical"]["format"] if "format" in item["lom"]["technical"] else None,
            "cclom:aggregationlevel": item["lom"]["general"]["aggregationLevel"]
            if "aggregationLevel" in item["lom"]["general"]
            else None,
            "cclom:title": item["lom"]["general"]["title"],
        }
        if "identifier" in item["lom"]["general"]:
            spaces["cclom:general_identifier"] = item["lom"]["general"]["identifier"]
        if "notes" in item:
            spaces["ccm:notes"] = item["notes"]
        if "status" in item:
            spaces["ccm:editorial_state"] = item["status"]
        if "origin" in item:
            spaces["ccm:replicationsourceorigin"] = item["origin"]  # TODO currently not mapped in edu-sharing

        if hasattr(spider, "edu_sharing_source_template_whitelist"):
            # check if there were whitelisted metadata properties in the edu-sharing source template
            # (= "Quellen-Datensatz"-Template) that need to be attached to all items
            whitelisted_properties: dict = getattr(spider, "edu_sharing_source_template_whitelist")
            if whitelisted_properties:
                # if whitelisted properties exist, we re-use the 'custom' field in our data model (if possible).
                # by inserting the whitelisted metadata properties early in the program flow, they should automatically
                # be overwritten by the "real" metadata fields (if metadata was scraped for the specific field by the
                # crawler)
                if hasattr(item, "custom"):
                    custom: dict = item["custom"]
                    if custom:
                        # if 'BaseItem.custom' already exists -> update the dict
                        custom.update(whitelisted_properties)
                        item["custom"] = custom
                else:
                    # otherwise create the 'BaseItem.custom'-field
                    item["custom"] = whitelisted_properties

        # map custom fields directly into the edu-sharing properties:
        if "custom" in item:
            for key in item["custom"]:
                spaces[key] = item["custom"][key]

        self.map_license(spaces, item["license"])
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
                    log.debug(
                        f"The supplied 'technical.duration'-value {duration} could not be converted from "
                        f"seconds to milliseconds. ('cclom:duration' expects ms)"
                    )
                    pass
                spaces["cclom:duration"] = duration

        if "lifecycle" in item["lom"]:
            for person in item["lom"]["lifecycle"]:
                if "role" not in person:
                    continue
                if not person["role"].lower() in EduSharingConstants.LIFECYCLE_ROLES_MAPPING:
                    log.warning(
                        "The lifecycle role "
                        + person["role"]
                        + " is currently not supported by the edu-sharing connector"
                    )
                    continue
                mapping = EduSharingConstants.LIFECYCLE_ROLES_MAPPING[person["role"].lower()]
                # convert to a vcard string
                firstName = person["firstName"] if "firstName" in person else ""
                lastName = person["lastName"] if "lastName" in person else ""
                title: str = person["title"] if "title" in person else ""
                organization = person["organization"] if "organization" in person else ""
                url = person["url"] if "url" in person else ""
                email = person["email"] if "email" in person else ""
                date = person["date"] if "date" in person else None
                id_gnd: str = person["id_gnd"] if "id_gnd" in person else ""
                id_orcid: str = person["id_orcid"] if "id_orcid" in person else ""
                id_ror: str = person["id_ror"] if "id_ror" in person else ""
                id_wikidata: str = person["id_wikidata"] if "id_wikidata" in person else ""
                vcard = vobject.vCard()
                vcard.add("n").value = vobject.vcard.Name(family=lastName, given=firstName)
                vcard.add("fn").value = organization if organization else (firstName + " " + lastName).strip()
                if id_gnd:
                    vcard.add("X-GND-URI").value = id_gnd
                if id_orcid:
                    vcard.add("X-ORCID").value = id_orcid
                if id_ror:
                    vcard.add("X-ROR").value = id_ror
                if id_wikidata:
                    vcard.add("X-Wikidata").value = id_wikidata
                if title:
                    vcard.add("title").value = title
                if date:
                    vcard.add("X-ES-LOM-CONTRIBUTE-DATE").value = date.isoformat()
                    if person["role"].lower() == "publisher":
                        spaces["ccm:published_date"] = date.isoformat()
                if organization:
                    vcard.add("org")
                    # fix a bug of split org values
                    vcard.org.behavior = VCardBehavior.defaultBehavior
                    vcard.org.value = organization
                if url:
                    vcard.add("url")
                    vcard.url.value = url
                if email:
                    vcard.add("EMAIL;TYPE=PREF,INTERNET").value = email
                if mapping in spaces:
                    # checking if a vcard already exists for this role: if so, extend the list
                    spaces[mapping].append(vcard.serialize(lineLength=10000))
                    # default of "lineLength" is 75, which is too short for longer URLs. We're intentionally setting an
                    # absurdly long lineLength, so we don't run into the problem where vCARD attributes like 'url' would
                    # get split up with a '\r\n '-string inbetween, which would cause broken URLs in the final vCard
                    # string and therefore broken links in the edu-sharing front-end
                else:
                    spaces[mapping] = [vcard.serialize(lineLength=10000)]

        valuespaceMapping = {
            "accessibilitySummary": "ccm:accessibilitySummary",
            "conditionsOfAccess": "ccm:conditionsOfAccess",
            "containsAdvertisement": "ccm:containsAdvertisement",
            "dataProtectionConformity": "ccm:dataProtectionConformity",
            "discipline": "ccm:taxonid",
            "educationalContext": "ccm:educationalcontext",
            "fskRating": "ccm:fskRating",
            "hochschulfaechersystematik": "ccm:oeh_taxonid_university",
            "intendedEndUserRole": "ccm:educationalintendedenduserrole",
            "languageLevel": "ccm:oeh_languageLevel",
            "learningResourceType": "ccm:educationallearningresourcetype",
            "new_lrt": "ccm:oeh_lrt",
            "oer": "ccm:license_oer",
            "price": "ccm:price",
            "sourceContentType": "ccm:sourceContentType",
            "toolCategory": "ccm:toolCategory",
        }
        for key in item["valuespaces"]:
            spaces[valuespaceMapping[key]] = item["valuespaces"][key]
        # add raw values if the api supports it
        if EduSharing.version["major"] >= 1 and EduSharing.version["minor"] >= 1:
            for key in item["valuespaces_raw"]:
                splitted = valuespaceMapping[key].split(":")
                splitted[0] = "virtual"
                spaces[":".join(splitted)] = item["valuespaces_raw"][key]
        if "typicalAgeRange" in item["lom"]["educational"]:
            tar = item["lom"]["educational"]["typicalAgeRange"]
            if "fromRange" in tar:
                spaces["ccm:educationaltypicalagerange_from"] = tar["fromRange"]
            if "toRange" in tar:
                spaces["ccm:educationaltypicalagerange_to"] = tar["toRange"]

        # intendedEndUserRole = Field(output_processor=JoinMultivalues())
        # discipline = Field(output_processor=JoinMultivalues())
        # educationalContext = Field(output_processor=JoinMultivalues())
        # learningResourceType = Field(output_processor=JoinMultivalues())
        # sourceContentType = Field(output_processor=JoinMultivalues())
        mdsId = env.get("EDU_SHARING_METADATASET", allow_null=True, default="mds_oeh")
        if mdsId != "default":
            spaces["cm:edu_metadataset"] = mdsId
            spaces["cm:edu_forcemetadataset"] = "true"
            log.debug("Using metadataset " + mdsId)
        else:
            log.debug("Using default metadataset")

        for key in spaces:
            if type(spaces[key]) is tuple:
                spaces[key] = list([x for y in spaces[key] for x in y])
            if not type(spaces[key]) is list:
                spaces[key] = [spaces[key]]

        return spaces

    def create_groups_if_not_exists(self, groups, type: CreateGroupType):
        for group in groups:
            if type == EduSharing.CreateGroupType.MediaCenter:
                uuid = EduSharingConstants.GROUP_PREFIX + EduSharingConstants.MEDIACENTER_PREFIX + group
            else:
                uuid = EduSharingConstants.GROUP_PREFIX + group
            if uuid in EduSharing.groupCache:
                log.debug("Group " + uuid + " is existing in cache, no need to create")
                continue
            log.debug("Group " + uuid + " is not in cache, checking consistency...")
            try:
                group = EduSharing.iamApi.get_group(EduSharingConstants.HOME, uuid)
                log.info("Group " + uuid + " was found in edu-sharing (cache inconsistency), no need to create")
                EduSharing.groupCache.append(uuid)
                continue
            except ApiException as e:
                log.info("Group " + uuid + " was not found in edu-sharing, creating it")
                pass

            if type == EduSharing.CreateGroupType.MediaCenter:
                result = EduSharing.mediacenterApi.create_mediacenter(
                    repository=EduSharingConstants.HOME,
                    mediacenter=group,
                    body={"mediacenter": {}, "displayName": group},
                )
                EduSharing.groupCache.append(result["authorityName"])
            else:
                result = EduSharing.iamApi.create_group(repository=EduSharingConstants.HOME, group=group, body={})
                EduSharing.groupCache.append(result["authorityName"])

    def set_node_permissions(self, uuid, item):
        if env.get_bool("EDU_SHARING_PERMISSION_CONTROL", False, True) is False:
            log.debug("Skipping permissions, EDU_SHARING_PERMISSION_CONTROL is set to false")
            return
        if "permissions" in item:
            permissions = {
                "inherited": True,  # let inherited = true to add additional permissions via edu-sharing
                "permissions": [],
            }
            public = item["permissions"]["public"]
            if public is True:
                if "groups" in item["permissions"] or "mediacenters" in item["permissions"]:
                    log.error(
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
                #    log.error('Invalid state detected: Permissions public is set to false but neither groups or mediacenters are set. Please use either public = true without groups/mediacenters or public = false and set group/mediacenters. No permissions will be set!')
                #    return
                mergedGroups = []
                if "groups" in item["permissions"]:
                    if "autoCreateGroups" in item["permissions"] and item["permissions"]["autoCreateGroups"] is True:
                        self.create_groups_if_not_exists(
                            item["permissions"]["groups"],
                            EduSharing.CreateGroupType.Regular,
                        )
                    mergedGroups += list(
                        map(
                            lambda x: EduSharingConstants.GROUP_PREFIX + x,
                            item["permissions"]["groups"],
                        )
                    )
                if "mediacenters" in item["permissions"]:
                    if (
                        "autoCreateMediacenters" in item["permissions"]
                        and item["permissions"]["autoCreateMediacenters"] is True
                    ):
                        self.create_groups_if_not_exists(
                            item["permissions"]["mediacenters"],
                            EduSharing.CreateGroupType.MediaCenter,
                        )
                    mergedGroups += list(
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
            if not self.set_permissions(uuid, permissions):
                log.error(
                    "Failed to set permissions, please check that the given groups/mediacenters are existing in the repository or set the autoCreate mode to true"
                )
                log.error(item["permissions"])

    async def insert_item(self, spider, uuid, item):
        async with self._sem:
            # inserting items is controlled with a Semaphore, otherwise we'd get PoolTimeout Exceptions when there's a
            # temporary burst of items that need to be inserted
            node = self.sync_node(spider, "ccm:io", self.transform_item(uuid, spider, item))
            self.set_node_permissions(node["ref"]["id"], item)
            await self.set_node_preview(node["ref"]["id"], item)
            if not await self.set_node_binary_data(node["ref"]["id"], item):
                await self.set_node_text(node["ref"]["id"], item)

    async def update_item(self, spider, uuid, item):
        await self.insert_item(spider, uuid, item)

    @staticmethod
    def init_cookie():
        log.debug("Init edu sharing cookie...")
        settings = get_project_settings()
        auth = requests.get(
            settings.get("EDU_SHARING_BASE_URL") + "rest/authentication/v1/validateSession",
            auth=HTTPBasicAuth(
                settings.get("EDU_SHARING_USERNAME"),
                settings.get("EDU_SHARING_PASSWORD"),
            ),
            headers={"Accept": "application/json"},
        )
        isAdmin = json.loads(auth.text)["isAdmin"]
        log.info("Got edu sharing cookie, admin status: " + str(isAdmin))
        if isAdmin:
            cookies = []
            for cookie in auth.headers["SET-COOKIE"].split(","):
                cookies.append(cookie.split(";")[0])
            EduSharing.cookie = ";".join(cookies)
        return auth

    def init_api_client(self):
        if EduSharing.cookie is None:
            settings = get_project_settings()
            auth = self.init_cookie()
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
                EduSharing.aboutApi = ABOUTApi(EduSharing.apiClient)
                EduSharing.bulkApi = BULKV1Api(EduSharing.apiClient)
                EduSharing.iamApi = IAMV1Api(EduSharing.apiClient)
                EduSharing.mediacenterApi = MEDIACENTERV1Api(EduSharing.apiClient)
                EduSharing.nodeApi = NODEV1Api(EduSharing.apiClient)
                about = EduSharing.aboutApi.about()
                EduSharing.version = list(filter(lambda x: x["name"] == "BULK", about["services"]))[0]["instances"][0][
                    "version"
                ]
                version_str = str(EduSharing.version["major"]) + "." + str(EduSharing.version["minor"])
                if (
                    EduSharing.version["major"] != 1
                    or EduSharing.version["minor"] < 0
                    or EduSharing.version["minor"] > 1
                ):
                    raise Exception(f"Given repository api version is unsupported: " + version_str)
                else:
                    log.info("Detected edu-sharing bulk api with version " + version_str)
                if env.get_bool("EDU_SHARING_PERMISSION_CONTROL", False, True) is True:
                    EduSharing.groupCache = list(
                        map(
                            lambda x: x["authorityName"],
                            EduSharing.iamApi.search_groups(EduSharingConstants.HOME, "", max_items=1000000)["groups"],
                        )
                    )
                    log.debug("Built up edu-sharing group cache: {}".format(EduSharing.groupCache))
                    return
                else:
                    return
            log.warning(auth.text)
            raise Exception(
                "Could not authentify as admin at edu-sharing. Please check your settings for repository "
                + settings.get("EDU_SHARING_BASE_URL")
            )

    @staticmethod
    def build_uuid(url):
        return str(uuid.uuid5(uuid.NAMESPACE_URL, url))

    def uuid_exists(self, uuid):
        return False

    def find_item(self, id, spider):
        if not self.enabled:
            return None
        properties = {
            "ccm:replicationsource": [spider.name],
            "ccm:replicationsourceid": [id],
        }
        try:
            response = EduSharing.bulkApi.find(properties)
            properties = response["node"]["properties"]
            if "ccm:replicationsourcehash" in properties and "ccm:replicationsourceuuid" in properties:
                return [
                    properties["ccm:replicationsourceuuid"][0],
                    properties["ccm:replicationsourcehash"][0],
                ]
        except ApiException as e:
            # ToDo:
            #  - find a way to handle statuscode 503 ("Service Temporarily Unavailable") gracefully?
            if e.status == 401:
                # Typically happens when the edu-sharing session cookie is lost and needs to be renegotiated.
                # (edu-sharing error-message: "Admin rights are required for this endpoint")
                log.info(
                    f"ES_CONNECTOR: edu-sharing returned HTTP-statuscode {e.status} for (replicationsourceid "
                    f"'{id}')."
                )
                log.debug(f"(HTTP-Body: '{e.body}\n')" f"Reason: {e.reason}\n" f"HTTP Headers: {e.headers}")
                log.info("ES_CONNECTOR: Re-initializing edu-sharing API Client...")
                self.init_api_client()
                return None
            if e.status == 404:
                try:
                    error_dict: dict = json.loads(e.body)
                    error_name: str = error_dict["error"]
                    if error_name and error_name == "org.edu_sharing.restservices.DAOMissingException":
                        # when there is no already existing node in the edu-sharing repository, edu-sharing returns
                        # a "DAOMissingException". The following debug message is commented out to reduce log-spam:
                        # error_message: str = error_dict["message"]
                        # log.debug(f"ES_CONNECTOR 'find_item': edu-sharing returned HTTP-statuscode 404 "
                        #               f"('{error_message}') for\n '{id}'. \n(This typically means that there was no "
                        #               f"existing node in the edu-sharing repository. Continuing...)")
                        return None
                    else:
                        log.debug(
                            f"ES_CONNECTOR 'find_item': edu-sharing returned HTTP-statuscode {e.status} "
                            f"(replicationsourceid '{id}'):\n"
                            f"HTTP Body: {e.body}\n"
                            f"HTTP Header: {e.headers}"
                        )
                        return None
                except json.JSONDecodeError:
                    log.debug(
                        f"ES_CONNECTOR 'find_item': edu-sharing returned HTTP-statuscode {e.status} "
                        f"(replicationsourceid '{id}'):\n"
                        f"HTTP Body: {e.body}\n"
                        f"HTTP Header: {e.headers}"
                    )
                return None
            else:
                raise e
        return None

    def find_source(self, spider):
        return True

    def create_source(self, spider):
        # src = self.createNode(EduSharing.etlFolder['ref']['id'], 'ccm:map', {'cm:name' : [spider.name]})
        # EduSharing.spiderNodes[spider.name] = src
        # return src
        return None
