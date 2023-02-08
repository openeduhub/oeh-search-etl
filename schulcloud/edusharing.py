import time
from datetime import datetime
from typing import Dict, List, Literal, Optional, IO, Any

import requests
import requests.auth


class Node:

    def __init__(self, obj: Dict):
        try:
            self.id: str = obj['ref']['id']
            self.name: str = obj['name']
            self.size: Optional[int] = int(obj['size']) if obj['size'] else None
            self.is_directory: bool = obj['isDirectory']
        except KeyError:
            raise RuntimeError(f'Could not parse node object: {obj}')
        self.obj = obj

    def __eq__(self, other):
        if isinstance(other, Node):
            return other.id == self.id
        return False

    def __repr__(self):
        return f'Node<{self.id}, {self.name}, is_dir={self.is_directory}>'


class EdusharingAPI:

    @staticmethod
    def _craft_permission_body(groups: List[str], inheritance: bool):
        permissions = []
        for group in groups:
            permission = {
                'editable': True,
                'authority': {
                    'authorityName': f'GROUP_{group}',
                    'authorityType': 'GROUP'
                },
                'group': {
                    'displayName': group
                },
                'permissions': ['Consumer']
            }

            permissions.append(permission)

        return {
            'inherited': inheritance,
            'permissions': permissions
        }

    def __init__(self, base_url: str, username: str = '', password: str = ''):
        self.base_url = base_url + 'rest'
        self.username = username
        self.password = password
        self.session = requests.Session()
        if self.username and self.password:
            self.session.auth = requests.auth.HTTPBasicAuth(self.username, self.password)

    def make_request(self, method: Literal['GET', 'PUT', 'POST', 'DELETE'], url: str,
                     params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict] = None,
                     files: Optional[Dict] = None, stream: bool = False, retry: int = 50,
                     timeout: Optional[float] = None):
        url = f'{self.base_url}{url}'
        headers = {'Accept': 'application/json'}
        i = 0
        while True:
            print(method, url, params, json_data)
            response = None
            try:
                response = self.session.request(method, url, params=params, headers=headers,
                                                json=json_data, files=files, stream=stream, timeout=timeout)
            except requests.exceptions.ReadTimeout:
                pass
            if (response is None or 500 <= response.status_code < 600) and i < retry:
                time.sleep(i // 2)
                i += 1
                continue
            break
        return response

    def get_application_properties(self, xml_file_name: str):
        url = f'/admin/v1/applications/{xml_file_name}'
        response = self.make_request('GET', url)
        if not 200 <= response.status_code < 300:
            raise RequestFailedException(response)
        return response.json()

    def set_application_properties(self, xml_file_name: str, values: Dict[str, str]):
        url = f'/admin/v1/applications/{xml_file_name}'
        response = self.make_request('PUT', url, json_data=values)
        if not response.status_code == 200:
            raise RequestFailedException(response)

    def upload_content(self, node_id: str, filename: str, file: IO[bytes], mimetype: str = ''):
        url = f'/node/v1/nodes/-home-/{node_id}/content'
        params = {'versionComment': 'MAIN_FILE_UPLOAD', 'mimetype': mimetype}
        files = {
            'file': (filename, file, mimetype, {'Expires': '0'})
        }
        response = self.make_request('POST', url, params=params, files=files, stream=True)
        if not response.status_code == 200:
            raise RequestFailedException(response)

    def get_user(self, name: str = None):
        if name is None:
            name = '-me-'
        url = f'/iam/v1/people/-home-/{name}'
        response = self.make_request('GET', url)
        if response.status_code == 404:
            raise NotFoundException(name)
        if not 200 <= response.status_code < 300:
            raise RequestFailedException(response)
        return response.json()

    def get_users(self):
        url = f'/iam/v1/people/-home-'
        params = {'pattern': '*'}
        response = self.make_request('GET', url, params=params)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        response = response.json()
        if not response['pagination']['count'] == response['pagination']['total']:
            raise RequestFailedException(response, 'Too many users')
        return response['users']

    def create_user(self, username: str, password: str, type: Literal['function', 'system'], quota: int = 1024 ** 2):
        url = f'/iam/v1/people/-home-/{username}'
        params = {'password': password}
        body = {
            'primaryAffiliation': type,
            'skills': None,
            'types': [],
            'sizeQuota': quota,
            'vcard': None,
            'firstName': username,
            'lastName': username,
            'email': 'nomail',
            'avatar': None,
            'about': None
        }
        response = self.make_request('POST', url, params=params, json_data=body)
        if not 200 <= response.status_code < 300:
            raise RequestFailedException(response)

    def delete_user(self, name: str):
        url = f'/iam/v1/people/-home-/{name}'
        params = {'force': 'true'}
        response = self.make_request('DELETE', url, params=params)
        if not 200 <= response.status_code < 300:
            raise RequestFailedException(response)

    def user_get_groups(self, username: str):
        url = f'/iam/v1/people/-home-/{username}/memberships'
        response = self.make_request('GET', url)
        if not 200 <= response.status_code < 300:
            raise RequestFailedException(response)
        response = response.json()
        if not response['pagination']['count'] == response['pagination']['total']:
            raise RequestFailedException(response, 'Too many groups')
        return response['groups']

    def create_group(self, group_name: str):
        url = f'/iam/v1/groups/-home-/{group_name}'
        body = {
            'displayName': group_name,
            'groupType': None,
            'scopeType': None
        }
        response = self.make_request('POST', url, json_data=body)
        if not response.status_code == 200:
            raise RequestFailedException(response)

    def get_groups(self):
        url = f'/iam/v1/groups/-home-/'
        params = {'pattern': '*', 'maxItems': 1024}
        response = self.make_request('GET', url, params=params)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        response = response.json()
        if not response['pagination']['count'] == response['pagination']['total']:
            raise RequestFailedException(response, 'Too many groups')
        return response['groups']

    def group_add_user(self, group_name: str, user_name: str):
        url = f'/iam/v1/groups/-home-/GROUP_{group_name}/members/{user_name}'
        response = self.make_request('PUT', url)
        if not 200 <= response.status_code < 300:
            raise RequestFailedException(response)

    def get_children(self, node_id: str, all_properties: bool = False, type: Literal['all', 'folders', 'files'] = 'all') -> List[Node]:
        url = f'/node/v1/nodes/-home-/{node_id}/children'
        params = {'maxItems': '200'}
        if all_properties:
            params['propertyFilter'] = '-all-'
        if not type == 'all':
            if type not in ('files', 'folders'):
                raise ValueError(f'Unknown node type: {type}')
            params['filter'] = type
        offset = 0
        children = []
        while True:
            params['skipCount'] = str(offset)
            response = self.make_request('GET', url, params)
            if response.status_code == 200:
                content = response.json()
                try:
                    children += [Node(node) for node in content['nodes']]
                    offset += content['pagination']['count']
                    total = content['pagination']['total']
                except KeyError:
                    raise RuntimeError(f'Could not parse response: {response.text}')
                if offset >= total:
                    break
            else:
                raise RequestFailedException(response)
        return children

    def find_node_by_name(self, parent_id: str, child_name: str) -> Node:
        nodes = self.get_children(parent_id)
        for node in nodes:
            if node.name == child_name:
                return node
        raise NotFoundException(child_name)

    def find_node_by_replication_source_id(self, replication_source_id: str) -> Node:
        nodes = self.search_custom('ccm:replicationsourceid', replication_source_id, 2, 'FILES')
        if len(nodes) == 1:
            return nodes[0]
        elif len(nodes) > 1:
            raise FoundTooManyException(replication_source_id)
        else:
            raise NotFoundException(replication_source_id)

    def create_node(self, parent_id: str, name: str, type: Literal['file', 'folder'] = 'file', properties: Optional[Dict] = None):
        url = f'/node/v1/nodes/-home-/{parent_id}/children'
        params = {
            'type': 'ccm:io' if type == 'file' else 'cm:folder',
            'renameIfExists': 'false',
            'assocType': '',
            'versionComment': '',
        }
        data = {
            'cm:name': [name],
            'cm:edu_metadataset': ['mds_oeh'],
            'cm:edu_forcemetadataset': [True],
        }
        if properties:
            data.update(properties)
        response = self.make_request('POST', url, params=params, json_data=data)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        return Node(response.json()['node'])

    def sync_node(self, group: str, properties: Dict, match: List[str], type: str = 'ccm:io',
                  group_by: Optional[str] = None):
        url = f'/bulk/v1/sync/{group}'
        params = {
            'type': type,
            'resetVersion': 'false',
            'match': match
        }
        if group_by is not None:
            params['groupBy'] = group_by
        response = self.make_request('PUT', url, params=params, json_data=properties)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        return Node(response.json()['node'])

    def delete_node(self, node_id: str):
        url = f'/node/v1/nodes/-home-/{node_id}'
        response = self.make_request('DELETE', url)
        if not response.status_code == 200:
            raise RequestFailedException(response)

    def get_sync_obj_folder(self):
        return self.get_or_create_node('-userhome-', 'SYNC_OBJ', type='folder')

    def file_exists(self, parent_id: str, name: str):
        # TODO: should only search within specific parent node, not global search
        return len(self.search_custom('cm:name', name, 2, 'FILES')) > 0

    def file_exists_by_name(self, name: str):
        name = name.replace(" ", "_")
        return len(self.search_custom('name', name, 2, 'FILES')) > 0

    def search_schulcloud(self, query: str):
        url = f'/search/v1/queries/-home-/mds_oeh/ngsearch/'
        params = {
            'contentType': 'FILES',
            'skipCount': '0',
            'maxItems': '20',
            'sortProperties': 'score',
            'sortAscending': 'false',
            'propertyFilter': '-all-',
        }
        body = {
            "criteria": [
                {
                    "property": "ccm:ph_invited",
                    "values": [
                        "GROUP_county-12051", "GROUP_public", "GROUP_LowerSaxony-public",
                                      "GROUP_Brandenburg-public", "GROUP_Thuringia-public"
                    ]
                },
                {
                    "property": "ccm:hpi_searchable", "values": ["1"]},
                {
                    "property": "ngsearchword", "values": [query]
                }
            ],
            "facets": ["cclom:general_keyword"]
        }
        response = self.make_request('POST', url, params=params, json_data=body)
        return response

    def search_custom(self, property: str, value: str, max_items: int, content_type: Literal['FOLDERS', 'FILES']):
        url = f'/search/v1/custom/-home-?contentType={content_type}&combineMode=AND&property={property}&value={value}' \
              f'&maxItems={max_items}&skipCount=0'
        response = self.make_request('GET', url)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        json_obj = response.json()
        return [Node(node) for node in json_obj['nodes']]

    def get_permissions(self, node_id: str):
        url = f'/node/v1/nodes/-home-/{node_id}/permissions'
        response = self.make_request('GET', url)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        try:
            return response.json()['permissions']
        except KeyError:
            raise RequestFailedException(response)

    def set_permissions(self, node_id: str, groups: List[str], inheritance: bool) -> None:
        url = f'/node/v1/nodes/-home-/{node_id}/permissions?sendMail=false&sendCopy=false'
        response = self.make_request('POST', url, json_data=self._craft_permission_body(groups, inheritance), timeout=8)
        if not response.status_code == 200:
            raise RequestFailedException(response)

    def get_metadata(self, node_id: str):
        url = f'/node/v1/nodes/-home-/{node_id}/metadata'
        response = self.make_request('GET', url)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        return response.json()

    def change_metadata(self, node_id: str, properties: Dict[str, List[str]]):
        url = f'/node/v1/nodes/-home-/{node_id}/metadata'
        params = {'versionComment': 'METADATA_UPDATE'}
        response = self.make_request('POST', url, params=params, json_data=properties)
        if not response.status_code == 200:
            raise RequestFailedException(response)

    def get_node_timestamp(self, node):
        meta = self.get_metadata_of_node(node.id)
        timestamp_str = str(meta["node"]["createdAt"]).replace("Z", "")
        return datetime.fromisoformat(timestamp_str)

    def get_or_create_node(self, parent_id: str, name: str, type: Literal['file', 'folder'] = 'file', properties: Optional[Dict] = None):
        try:
            folder = self.find_node_by_name(parent_id, name)
            if properties:
                self.change_metadata(folder.id, properties)
        except NotFoundException:
            folder = self.create_node(parent_id, name, type=type, properties=properties)
        return folder

    def set_property(self, node_id: str, property: str, value: Optional[List[str]]):
        # /node/v1/nodes/{repository}/{node}/property
        url = f'/node/v1/nodes/-home-/{node_id}/property'
        params = {'property': property}
        if value is not None:
            params['value'] = value
        response = self.make_request('POST', url, params=params, retry=0)
        if not response.status_code == 200 and response.status_code > 500:
            raise RequestFailedException(response, node_id)

    def set_collection_children(self, node_id: str, children_uuids: List[str]):
        """
        Sets collection relation to its children. Reverse operation is also needed for all children.
        @param children_uuids: replication source uuids of ALL children
        """
        # frontend relies on exact syntax, no double quotes (as in json) allowed
        value = f"{{kind': 'hasparts', 'resource': {{'identifier': {str(children_uuids)}}}}}"
        for property in 'ccm:lom_relation', 'ccm:hpi_lom_relation':
            self.set_property(node_id, property, [value])

    def set_collection_parent(self, node_id: str, parent_uuid: str):
        """
        Sets node's relation to its collection. Reverse operation is needed for collection.
        @param parent_uuid: replication source uuid of parent
        """
        # frontend relies on exact syntax, no double quotes (as in json) allowed
        value = f"{{'kind': 'ispartof', 'resource': {{'identifier': ['{parent_uuid}']}}}}"
        for property in 'ccm:lom_relation', 'ccm:hpi_lom_relation':
            self.set_property(node_id, property, [value])

    def set_preview_thumbnail(self, node_id: str, filename: str):
        url = f'/node/v1/nodes/-home-/{node_id}/preview?mimetype=image'
        files = {'image': (filename, open(filename, 'rb'))}
        response = self.make_request('POST', url, files=files, stream=True)
        if not response.status_code == 200:
            raise RequestFailedException(response, node_id)
        files['image'][1].close()

    def set_preview_thumbnail_fwu(self, node_id: str, filename: str):
        url = f'/node/v1/nodes/-home-/{node_id}/preview?mimetype=image'
        files = {'image': filename}
        response = self.make_request('POST', url, files=files, stream=True)
        if not response.status_code == 200:
            raise RequestFailedException(response, node_id)


class RequestFailedException(Exception):
    def __init__(self, response: requests.Response, context_hint: str = ''):
        super(RequestFailedException, self).__init__(f'Request failed: {response.status_code} {response.reason}: '
                                                     f':{response.text}; {context_hint}')


class FoundTooManyException(Exception):
    def __init__(self, name: str):
        super(FoundTooManyException, self).__init__(f'Found too many of {name}')


class NotFoundException(Exception):
    def __init__(self, name: str):
        super(NotFoundException, self).__init__(f'Could not find {name}')
