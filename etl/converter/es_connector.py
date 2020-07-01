import uuid
import requests
import json
import base64
from scrapy.utils.project import get_project_settings
from requests.auth import HTTPBasicAuth
from io import BytesIO
import logging
from converter.constants import Constants
from edu_sharing_client.api_client import ApiClient
from edu_sharing_client.configuration import Configuration
from edu_sharing_client.api.bulk_v1_api import BULKV1Api
from edu_sharing_client.api.iam_v1_api import IAMV1Api
from edu_sharing_client.api.node_v1_api import NODEV1Api
from edu_sharing_client.rest import ApiException


class EduSharingConstants:
    HOME = '-home-'
    GROUP_EVERYONE = 'GROUP_EVERYONE'
    AUTHORITYTYPE_GROUP = 'GROUP'
    AUTHORITYTYPE_EVERYONE = 'EVERYONE'
    PERMISSION_CONSUMER = 'Consumer'
    PERMISSION_CCPUBLISH = 'CCPublish'
    GROUP_PREFIX = 'GROUP_'
    MEDIACENTER_PROXY_PREFIX = 'MEDIA_CENTER_PROXY_'

# creating the swagger client: java -jar swagger-codegen-cli-3.0.20.jar generate -l python -i http://localhost:8080/edu-sharing/rest/swagger.json -o edu_sharing_swagger -c edu-sharing-swagger.config.json
class ESApiClient(ApiClient):
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
        #return self.__deserialize(data, response_type)
        return data
class EduSharing:

    cookie = None
    apiClient = None
    bulkApi = None
    iamApi = None
    nodeApi = None
    def __init__(self):
        self.initApiClient()
    def getHeaders(self, contentType = 'application/json'):
        return { 'COOKIE' : EduSharing.cookie, 'Accept' : 'application/json', 'Content-Type' : contentType}
    def syncNode(self, spider, type, properties):
        response = EduSharing.bulkApi.sync(spider.name, ['ccm:replicationsource', 'ccm:replicationsourceid'], type, properties)
        return response['node']
    def setNodeText(self, uuid, item):
        if 'fulltext' in item:
            response = requests.post(get_project_settings().get('EDU_SHARING_BASE_URL') + 'rest/node/v1/nodes/-home-/' + uuid + '/textContent?mimetype = text/plain', 
                headers = self.getHeaders(None),
                data = item['fulltext'].encode('utf-8'))
            return response.status_code == 200
            # does currently not store data
            # try:
            #     EduSharing.nodeApi.change_content_as_text(EduSharingConstants.HOME, uuid, 'text/plain',item['fulltext'])
            #     return True
            # except ApiException as e:
            #     print(e)
            #     return False

    def setPermissions(self, uuid, permissions):
        try:
            EduSharing.nodeApi.set_permission(EduSharingConstants.HOME, uuid, permissions, False, False)
            return True
        except ApiException as e:
            return False
    def setNodePreview(self, uuid, item):
        key = 'large' if 'large' in item['thumbnail'] else 'small'
        files = {'image': base64.b64decode(item['thumbnail'][key])}
        response = requests.post(get_project_settings().get('EDU_SHARING_BASE_URL') + 'rest/node/v1/nodes/-home-/' + uuid + '/preview?mimetype=' + item['thumbnail']['mimetype'], 
                    headers = self.getHeaders(None),
                    files = files)
        return response.status_code == 200
 
    def mapLicense(self, spaces, license):
        if 'url' in license:
            if license['url'] == Constants.LICENSE_CC_BY_40:
                spaces['ccm:commonlicense_key'] = 'CC_BY'
                spaces['ccm:commonlicense_cc_version'] = '4.0'
            if license['url'] == Constants.LICENSE_CC_BY_SA_30:
                spaces['ccm:commonlicense_key'] = 'CC_BY_SA'
                spaces['ccm:commonlicense_cc_version'] = '3.0'
            if license['url'] == Constants.LICENSE_CC_BY_SA_40:
                spaces['ccm:commonlicense_key'] = 'CC_BY_SA'
                spaces['ccm:commonlicense_cc_version'] = '4.0'
            if license['url'] == Constants.LICENSE_CC_ZERO_10:
                spaces['ccm:commonlicense_key'] = 'CC_0'
                spaces['ccm:commonlicense_cc_version'] = '1.0'
        if 'internal' in license:
            if license['internal'] == Constants.LICENSE_COPYRIGHT_LAW:
                spaces['ccm:commonlicense_key'] = 'COPYRIGHT_FREE'

    def transformItem(self, uuid, spider, item):
        spaces = {
            'ccm:replicationsource' : spider.name,
            'ccm:replicationsourceid' : item['sourceId'],
            'ccm:replicationsourcehash' : item['hash'], # @TODO create this field in edu-sharing
            'ccm:io_type' : item['type'], # @TODO find suited field
            'ccm:replicationsourceuuid' : uuid, # @TODO find suited field
            'cm:name' : item['lom']['general']['title'],
            'ccm:wwwurl' : item['lom']['technical']['location'],
            'cclom:location' : item['lom']['technical']['location'],
            'cclom:title' : item['lom']['general']['title'],
        }
        self.mapLicense(spaces, item['license'])
        if 'description' in item['lom']['general']:
            spaces['cclom:general_description'] = item['lom']['general']['description']

        if 'language' in item['lom']['general']:
            spaces['cclom:general_language'] = item['lom']['general']['language']

        if 'keyword' in item['lom']['general']:
            spaces['cclom:general_keyword'] = item['lom']['general']['keyword'],

        valuespaceMapping = {
            'discipline' : 'ccm:taxonid',
            'intendedEndUserRole' : 'ccm:educationalintendedenduserrole',
            'educationalContext' : 'ccm:educationalcontext',
            'learningResourceType' : 'ccm:learningResourceType',
            'sourceContentType' : 'ccm:sourceContentType', # @TODO find suited data field
        }
        for key in item['valuespaces']:
            spaces[valuespaceMapping[key]] = item['valuespaces'][key]
        if 'typicalagerange' in item['lom']['educational']:
            spaces['ccm:educationaltypicalagerange_from'] = item['lom']['educational']['typicalagerange']['from']
            spaces['ccm:educationaltypicalagerange_to'] = item['lom']['educational']['typicalagerange']['to']
        # intendedEndUserRole = Field(output_processor=JoinMultivalues())
        # discipline = Field(output_processor=JoinMultivalues())
        # educationalContext = Field(output_processor=JoinMultivalues())
        # learningResourceType = Field(output_processor=JoinMultivalues())
        # sourceContentType = Field(output_processor=JoinMultivalues())
        spaces['cm:edu_metadataset'] = 'mds_oeh'
        spaces['cm:edu_forcemetadataset'] = 'true'
        
        for key in spaces:
            if type(spaces[key]) is tuple:
                spaces[key] = list([x for y in spaces[key] for x in y])
            if not type(spaces[key]) is list:
                spaces[key] = [spaces[key]]

        return spaces
    def setNodePermissions(self, uuid, item):
        if 'permissions' in item:
            permissions = {
                "inherited": False,
                "permissions": []
            }
            public = item['permissions']['public']
            if public == True:
                if 'groups' in item['permissions'] or 'mediacenters' in item['permissions']:
                    logging.error('Invalid state detected: Permissions public is set to true but groups or mediacenters are also set. Please use either public = true without groups/mediacenters or public = false and set group/mediacenters. No permissions will be set!')
                    return
                permissions['permissions'].append({
                    "authority": {
                        "authorityName": EduSharingConstants.GROUP_EVERYONE,
                        "authorityType": EduSharingConstants.AUTHORITYTYPE_EVERYONE
                    },
                    "permissions": [ EduSharingConstants.PERMISSION_CONSUMER, EduSharingConstants.PERMISSION_CCPUBLISH ]
                })
            else:
                if not 'groups' in item['permissions'] and not 'mediacenters' in item['permissions']:
                    logging.error('Invalid state detected: Permissions public is set to false but neither groups or mediacenters are set. Please use either public = true without groups/mediacenters or public = false and set group/mediacenters. No permissions will be set!')
                    return
                groups = []
                if 'groups' in item['permissions']:
                    groups = groups + list(map(lambda x: EduSharingConstants.GROUP_PREFIX + x, item['permissions']['groups']))
                if 'mediacenters' in item['permissions']:
                    groups = groups + list(map(lambda x: EduSharingConstants.GROUP_PREFIX + EduSharingConstants.MEDIACENTER_PROXY_PREFIX + x, item['permissions']['mediacenters']))
                for group in groups:
                    permissions['permissions'].append({
                        "authority": {
                            "authorityName": group,
                            "authorityType": EduSharingConstants.AUTHORITYTYPE_GROUP
                        },
                        "permissions": [ EduSharingConstants.PERMISSION_CONSUMER, EduSharingConstants.PERMISSION_CCPUBLISH ]
                    })
            if not self.setPermissions(uuid, permissions):
                logging.error('Failed to set permissions, please check that the given groups/mediacenters are existing in the repository ')
                logging.error(item['permissions'])

    def insertItem(self, spider, uuid, item):
        node = self.syncNode(spider, 'ccm:io' ,self.transformItem(uuid, spider, item))
        self.setNodePermissions(node['ref']['id'], item)
        self.setNodePreview(node['ref']['id'], item)
        self.setNodeText(node['ref']['id'], item)


    def updateItem(self, spider, uuid, item):
        self.insertItem(spider, uuid, item)

    def initApiClient(self):
        if EduSharing.cookie == None:
            settings = get_project_settings()
            auth = requests.get(settings.get('EDU_SHARING_BASE_URL') + 'rest/authentication/v1/validateSession', 
                    auth = HTTPBasicAuth(settings.get('EDU_SHARING_USERNAME'), settings.get('EDU_SHARING_PASSWORD')),
                    headers = { 'Accept' : 'application/json'}
            )
            isAdmin = json.loads(auth.text)['isAdmin']
            if isAdmin:
                EduSharing.cookie = auth.headers['SET-COOKIE'].split(';')[0]
                configuration = Configuration()
                configuration.host = settings.get('EDU_SHARING_BASE_URL') + 'rest'
                EduSharing.apiClient = ESApiClient(configuration, cookie = EduSharing.cookie, header_name = 'Accept', header_value = 'application/json')
                EduSharing.bulkApi = BULKV1Api(EduSharing.apiClient)
                EduSharing.iamApi = IAMV1Api(EduSharing.apiClient)
                EduSharing.nodeApi = NODEV1Api(EduSharing.apiClient)
                return
            raise Exception('Could not authentify as admin at edu-sharing. Please check your settings for repository ' + settings.get('EDU_SHARING_BASE_URL'))
            
    def buildUUID(self, url):
        return str(uuid.uuid5(uuid.NAMESPACE_URL, url))

    def uuidExists(self, uuid):
        return False

    def findItem(self, id, spider):
        properties = {
            'ccm:replicationsource': [spider.name],
            'ccm:replicationsourceid': [id],
        }
        try:
            response = EduSharing.bulkApi.find(properties)
            properties = response['node']['properties']
            if 'ccm:replicationsourcehash' in properties and 'ccm:replicationsourceuuid' in properties:
                return [properties['ccm:replicationsourceuuid'][0], properties['ccm:replicationsourcehash'][0]]
        except ApiException as e:
            if e.status == 404:
                pass
            else:
                raise e
        return None

    def findSource(self, spider):
        return True
        
    def createSource(self, spider):
        #src = self.createNode(EduSharing.etlFolder['ref']['id'], 'ccm:map', {'cm:name' : [spider.name]})
        #EduSharing.spiderNodes[spider.name] = src
        #return src
        return None
