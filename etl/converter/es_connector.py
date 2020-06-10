import uuid
import requests
import json
import base64
from scrapy.utils.project import get_project_settings
from requests.auth import HTTPBasicAuth
from io import BytesIO

class EduSharing:
    cookie = None
    def __init__(self):
        self.loadSession()
    def getHeaders(self, contentType = 'application/json'):
        return { 'COOKIE' : EduSharing.cookie, 'Accept' : 'application/json', 'Content-Type' : contentType}
    def syncNode(self, spider, type, properties):
        response = requests.put(get_project_settings().get('EDU_SHARING_BASE_URL') + 'rest/bulk/v1/sync/' + spider.name + '?match=ccm:replicationsource&match=ccm:replicationsourceid&type=' + type, 
                    headers = self.getHeaders(),
                    data = json.dumps(properties))
        return json.loads(response.text)['node']
    def setNodeText(self, uuid, item):
        if 'fulltext' in item:
            response = requests.post(get_project_settings().get('EDU_SHARING_BASE_URL') + 'rest/node/v1/nodes/-home-/' + uuid + '/textContent?mimetype = text/plain', 
                        headers = self.getHeaders(None),
                        data = item['fulltext'].encode('utf-8'))
            return response.status_code == 200

    def setNodePreview(self, uuid, item):
        key = 'large' if 'large' in item['thumbnail'] else 'small'
        files = {'image': base64.b64decode(item['thumbnail'][key])}
        response = requests.post(get_project_settings().get('EDU_SHARING_BASE_URL') + 'rest/node/v1/nodes/-home-/' + uuid + '/preview?mimetype=' + item['thumbnail']['mimetype'], 
                    headers = self.getHeaders(None),
                    files = files)
        return response.status_code == 200
 
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
        
        for key in spaces:
            if type(spaces[key]) is tuple:
                spaces[key] = list([x for y in spaces[key] for x in y])
            if not type(spaces[key]) is list:
                spaces[key] = [spaces[key]]

        return spaces

    def insertItem(self, spider, uuid, item):
        node = self.syncNode(spider, 'ccm:io' ,self.transformItem(uuid, spider, item))
        self.setNodePreview(node['ref']['id'], item)
        self.setNodeText(node['ref']['id'], item)


    def updateItem(self, spider, uuid, item):
        self.insertItem(spider, uuid, item)

    def loadSession(self):
        if EduSharing.cookie == None:
            settings = get_project_settings()
            auth = requests.get(settings.get('EDU_SHARING_BASE_URL') + 'rest/authentication/v1/validateSession', 
                    auth = HTTPBasicAuth(settings.get('EDU_SHARING_USERNAME'), settings.get('EDU_SHARING_PASSWORD')),
                    headers = { 'Accept' : 'application/json'}
            )
            isAdmin = json.loads(auth.text)['isAdmin']
            if isAdmin:
                EduSharing.cookie = auth.headers['SET-COOKIE'].split(';')[0]
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
        response = requests.post(get_project_settings().get('EDU_SHARING_BASE_URL') + 'rest/bulk/v1/find',
                    headers = self.getHeaders(),
                    data = json.dumps(properties))
        if response.status_code == 200:
            properties = json.loads(response.text)['node']['properties']
            if 'ccm:replicationsourcehash' in properties and 'ccm:replicationsourceuuid' in properties:
                return [properties['ccm:replicationsourceuuid'][0], properties['ccm:replicationsourcehash'][0]]
        return None

    def findSource(self, spider):
        return True
        
    def createSource(self, spider):
        #src = self.createNode(EduSharing.etlFolder['ref']['id'], 'ccm:map', {'cm:name' : [spider.name]})
        #EduSharing.spiderNodes[spider.name] = src
        #return src
        return None
