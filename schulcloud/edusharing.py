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

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url + 'rest'
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = requests.auth.HTTPBasicAuth(self.username, self.password)

    def make_request(self, method: Literal['GET', 'PUT', 'POST', 'DELETE'], url: str,
                     params: Optional[Dict[str, Any]] = None, json_data: Optional[Dict] = None,
                     files: Optional[Dict] = None, stream: bool = False, retry: int = 50):
        # TODO: remove print statements
        if not method == 'GET':
            print(f'{method} {url} {params=} {json_data=}')
        url = f'{self.base_url}{url}'
        headers = {'Accept': 'application/json'}
        while True:
            response = self.session.request(method, url, params=params, headers=headers,
                                            json=json_data, files=files, stream=stream)
            if 500 <= response.status_code < 600 and retry:
                retry -= 1
                time.sleep(1.0)
                continue
            break
        if not method == 'GET':
            print(f'{response.status_code} {response.reason} <--')
        return response

    def get_application_properties(self, xml_file_name: str):
        url = f'/admin/v1/applications/{xml_file_name}'
        response = self.make_request('GET', url)
        response.raise_for_status()
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

    def change_metadata(self, node_id: str, properties: Dict[str, List[str]]):
        url = f'/node/v1/nodes/-home-/{node_id}/metadata'
        params = {'versionComment': 'METADATA_UPDATE'}
        response = self.make_request('POST', url, params=params, json_data=properties)
        if not response.status_code == 200:
            raise RequestFailedException(response)

    def get_user(self, name: str = None):
        if name is None:
            name = '-me-'
        url = f'/iam/v1/people/-home-/{name}'
        response = self.make_request('GET', url)
        if response.status_code == 404:
            raise NotFoundException(name)
        response.raise_for_status()
        return response.json()

    def get_users(self):
        url = f'/iam/v1/people/-home-'
        params = {'pattern': '*'}
        response = self.make_request('GET', url, params=params)
        response.raise_for_status()
        return response.json()['users']

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
        response.raise_for_status()

    def delete_user(self, name: str):
        url = f'/iam/v1/people/-home-/{name}'
        params = {'force': 'true'}
        response = self.make_request('DELETE', url, params=params)
        response.raise_for_status()

    def create_group(self, group_name: str):
        url = f'/iam/v1/groups/-home-/{group_name}'
        body = {
            'displayName': group_name,
            'groupType': None,
            'scopeType': None
        }
        response = self.make_request('POST', url, json_data=body)
        response.raise_for_status()

    def group_add_user(self, group_name: str, user_name: str):
        url = f'/iam/v1/groups/-home-/GROUP_{group_name}/members/{user_name}'
        response = self.make_request('PUT', url)
        response.raise_for_status()

    def get_children(self, node_id: str) -> List[Node]:
        url = f'/node/v1/nodes/-home-/{node_id}/children'
        response = self.make_request('GET', url, {'maxItems': '500', 'skipCount': '0'})
        if response.status_code == 200:
            try:
                return [Node(node) for node in response.json()['nodes']]
            except KeyError:
                raise RuntimeError(f'Could not parse response: {response.text}')
        else:
            raise RequestFailedException(response)

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

    def delete_node(self, node_id: str):
        url = f'/node/v1/nodes/-home-/{node_id}'
        response = self.make_request('DELETE', url)
        if not response.status_code == 200:
            raise RequestFailedException(response)

    def get_permissions(self, node_id: str):
        url = f'/node/v1/nodes/-home-/{node_id}'
        response = self.make_request('GET', url)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        return response.json()

    def set_permissions(self, node_id: str, groups: List[str], inheritance: bool) -> None:
        url = f'/node/v1/nodes/-home-/{node_id}/permissions?sendMail=false&sendCopy=false'
        response = self.make_request('POST', url, json_data=self._craft_permission_body(groups, inheritance))
        if not response.status_code == 200:
            raise RequestFailedException(response)

    def get_sync_obj_folder(self):
        return self.get_or_create_node('-userhome-', 'SYNC_OBJ', type='folder')

    def file_exists(self, parent_id: str, name: str):
        # TODO: should only search within specific parent node, not global search
        return len(self.search_custom('cm:name', name, 2, 'FILES')) > 0

    def search_custom(self, property: str, value: str, max_items: int, content_type: Literal['FOLDERS', 'FILES']):
        url = f'/search/v1/custom/-home-?contentType={content_type}&combineMode=AND&property={property}&value={value}' \
              f'&maxItems={max_items}&skipCount=0'
        response = self.make_request('GET', url)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        json_obj = response.json()
        return [Node(node) for node in json_obj['nodes']]

    def get_metadata_of_node(self, node_id: str):
        url = f'/node/v1/nodes/-home-/{node_id}/metadata'
        response = self.make_request('GET', url)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        json_obj = response.json()
        return json_obj

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

    def set_property(self, node_id: str, property: str, value: Optional[List[str]]):
        # /node/v1/nodes/{repository}/{node}/property
        url = f'/node/v1/nodes/-home-/{node_id}/property'
        params = {'property': property}
        if value is not None:
            params['value'] = value
        response = self.make_request('POST', url, params=params)
        if not response.status_code == 200:
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


class RequestFailedException(Exception):
    def __init__(self, response: requests.Response, context_hint: str = ''):
        if context_hint:
            context_hint += ' -> '
        super(RequestFailedException, self).__init__(f'Request failed: {context_hint}{response.status_code}'
                                                     f' {response.reason}: {response.text}')


class FoundTooManyException(Exception):
    def __init__(self, name: str):
        super(FoundTooManyException, self).__init__(f'Found too many of {name}')


class NotFoundException(Exception):
    def __init__(self, name: str):
        super(NotFoundException, self).__init__(f'Could not find {name}')
