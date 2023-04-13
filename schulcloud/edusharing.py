import os
import time
from datetime import datetime
from typing import Dict, List, Literal, Optional, IO, Any, Callable

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
        if not base_url.endswith('/'):
            base_url += '/'
        self.debug_enabled = os.environ.get('EDU_SHARING_API_DEBUG', 'false').lower() == 'true'
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
        i = -1
        while True:
            i += 1
            if self.debug_enabled:
                print(method, url, params, json_data)
            try:
                response = self.session.request(method, url, params=params, headers=headers,
                                                json=json_data, files=files, stream=stream, timeout=timeout)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
                if i < retry:
                    time.sleep(i // 2)
                    continue
                else:
                    if isinstance(exc, requests.exceptions.Timeout):
                        raise RequestTimeoutException()
                    else:
                        raise ConnectionErrorException()
            if 500 <= response.status_code < 600 and i < retry:
                time.sleep(i // 2)
                continue
            if not (200 <= response.status_code < 300):
                raise RequestErrorResponseException(response)
            return response

    def get_all(self, method: Literal['GET', 'POST'], url: str, params: Dict[str, str], callback: Callable, max_items: int, json_data: Optional[dict] = None, retry: int = 50, timeout: Optional[float] = None):
        offset = 0
        items = []
        params['maxItems'] = str(max_items)
        while True:
            params['skipCount'] = str(offset)
            response = self.make_request(method, url, params, json_data=json_data, retry=retry, timeout=timeout)
            try:
                content = response.json()
                callback(items, content)
                offset += content['pagination']['count']
                total = content['pagination']['total']
            except KeyError:
                raise RuntimeError(f'Could not parse response: {response.text}')
            if offset >= total:
                break
        return items

    def get_application_properties(self, xml_file_name: str):
        url = f'/admin/v1/applications/{xml_file_name}'
        response = self.make_request('GET', url)
        return response.json()

    def set_application_properties(self, xml_file_name: str, values: Dict[str, str]):
        url = f'/admin/v1/applications/{xml_file_name}'
        response = self.make_request('PUT', url, json_data=values)

    def upload_content(self, node_id: str, filename: str, file: IO[bytes], mimetype: str = ''):
        url = f'/node/v1/nodes/-home-/{node_id}/content'
        params = {'versionComment': 'MAIN_FILE_UPLOAD', 'mimetype': mimetype}
        files = {
            'file': (filename, file, mimetype, {'Expires': '0'})
        }
        response = self.make_request('POST', url, params=params, files=files, stream=True)

    def get_user(self, name: str = None):
        if name is None:
            name = '-me-'
        url = f'/iam/v1/people/-home-/{name}'
        response = self.make_request('GET', url)
        if response.status_code == 404:
            raise NotFoundException(name)
        return response.json()

    def get_users(self):
        url = f'/iam/v1/people/-home-'
        params = {'pattern': '*'}
        users = self.get_all('GET', url, params, lambda items, content: items.extend(content['users']), 20)
        return users

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

    def mark_user_for_deletion(self, name: str):
        url = f'/iam/v1/people/-home-/{name}/status/todelete?notify=false'
        params = {
            'notify': 'false'
        }
        response = self.make_request('PUT', url, params=params)

    def delete_user(self, name: str):
        url = f'/iam/v1/people/-home-/{name}'
        params = {'force': 'true'}
        response = self.make_request('DELETE', url, params=params)

    def user_get_groups(self, username: str):
        url = f'/iam/v1/people/-home-/{username}/memberships'
        groups = self.get_all('GET', url, {}, lambda items, content: items.extend(content['groups']), 50)
        return groups

    def create_group(self, group_name: str):
        url = f'/iam/v1/groups/-home-/{group_name}'
        body = {
            'displayName': group_name,
            'groupType': None,
            'scopeType': None
        }
        response = self.make_request('POST', url, json_data=body)

    def get_groups(self):
        url = f'/iam/v1/groups/-home-/'
        params = {'pattern': '*'}
        groups = self.get_all('GET', url, params, lambda items, content: items.extend(content['groups']), 256)
        return groups

    def group_add_user(self, group_name: str, user_name: str):
        url = f'/iam/v1/groups/-home-/GROUP_{group_name}/members/{user_name}'
        self.make_request('PUT', url)

    def get_children(self, node_id: str, all_properties: bool = False, type: Literal['all', 'folders', 'files'] = 'all', start: int = 0, count: int = 0) -> List[Node]:
        url = f'/node/v1/nodes/-home-/{node_id}/children'
        params = {}
        if all_properties:
            params['propertyFilter'] = '-all-'
        if not type == 'all':
            if type not in ('files', 'folders'):
                raise ValueError(f'Unknown node type: {type}')
            params['filter'] = type
        if count == 0:
            return self.get_all('GET', url, params, lambda items, content: items.extend([Node(node) for node in content['nodes']]), 200)
        else:
            params['skipCount'] = start
            params['maxItems'] = count
            response = self.make_request('GET', url, params=params)
            return [Node(node) for node in response.json()['nodes']]

    def find_node_by_name(self, parent_id: str, child_name: str, type: Literal['all', 'files', 'folders'] = 'all') -> Node:
        nodes = self.get_children(parent_id, type=type)
        for node in nodes:
            if node.name == child_name:
                return node
        raise NotFoundException(child_name)

    def find_node_by_replication_source_id(self, replication_source_id: str, skip_exception: Optional[bool] = False) -> Node:
        nodes = self.search_custom('ccm:replicationsourceid', replication_source_id, content_type='FILES')
        if len(nodes) == 1:
            return nodes[0]
        elif len(nodes) > 1:
            raise FoundTooManyException(replication_source_id)
        else:
            if not skip_exception:
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
        return Node(response.json()['node'])

    def delete_node(self, node_id: str):
        url = f'/node/v1/nodes/-home-/{node_id}'
        self.make_request('DELETE', url)

    def get_sync_obj_folder(self):
        return self.get_or_create_node('-userhome-', 'SYNC_OBJ', type='folder')

    def file_exists(self, parent_id: str, name: str):
        # TODO: should only search within specific parent node, not global search
        return len(self.search_custom('cm:name', name, content_type='FILES')) > 0

    def search_ngsearch(self, criteria: list[dict[str, str]], content_type: Optional[Literal['FOLDERS', 'FILES']] = None, all_properties: bool = False):
        url = f'/search/v1/queries/-home-/mds_oeh/ngsearch/'
        params = {
             'sortProperties': 'score'
        }
        if content_type:
            params['contentType'] = content_type
        if all_properties:
            params['propertyFilter'] = '-all-'
        body = {
            'criteria': criteria,
            'facets': ['cclom:general_keyword']
        }
        nodes = self.get_all('POST', url, params, lambda items, content: items.extend([Node(node) for node in content['nodes']]), 100, json_data=body)
        return nodes

    def search_schulcloud(self, query: str):
        url = f'/search/v1/queries/-home-/mds_oeh/ngsearch/'
        params = {
            'contentType': 'FILES',
            'sortProperties': 'score',
            'sortAscending': 'false',
            'propertyFilter': '-all-',
        }
        body = {
            "criteria": [
                {"property": "ccm:hpi_searchable", "values": ["1"]},
                {"property": "ngsearchword", "values": [query]}
            ],
            "facets": ["cclom:general_keyword"]
        }

        nodes = self.get_all('POST', url, params, lambda items, content: items.extend([Node(node) for node in content['nodes']]), 100, json_data=body)
        return nodes

    def search_custom(self, property: str, value: str, content_type: Optional[Literal['FOLDERS', 'FILES']] = None, all_properties: bool = False):
        url = f'/search/v1/custom/-home-'
        params = {
            'combineMode': 'AND',
            'property': property,
            'value': value,
        }
        if content_type:
            params['contentType'] = content_type
        if all_properties:
            params['propertyFilter'] = '-all-'
        nodes = self.get_all('GET', url, params, lambda items, content: items.extend([Node(node) for node in content['nodes']]), 100)
        return nodes

    def get_permissions(self, node_id: str):
        url = f'/node/v1/nodes/-home-/{node_id}/permissions'
        response = self.make_request('GET', url)
        return response.json()['permissions']

    def get_permissions_groups(self, node_id: str) -> (list[str], bool):
        permissions = self.get_permissions(node_id)
        groups = []
        for permission in permissions['localPermissions']['permissions']:
            auth_name: str = permission['authority']['authorityName']
            if not auth_name.startswith('GROUP_'):
                continue
            groups.append(auth_name.replace('GROUP_', '', 1))
        return groups, permissions['localPermissions']['inherited']

    def set_permissions(self, node_id: str, groups: List[str], inheritance: bool) -> None:
        url = f'/node/v1/nodes/-home-/{node_id}/permissions?sendMail=false&sendCopy=false'
        response = self.make_request('POST', url, json_data=self._craft_permission_body(groups, inheritance), timeout=8)

    def get_metadata(self, node_id: str):
        url = f'/node/v1/nodes/-home-/{node_id}/metadata'
        response = self.make_request('GET', url)
        return response.json()

    def change_metadata(self, node_id: str, properties: Dict[str, List[str]]):
        url = f'/node/v1/nodes/-home-/{node_id}/metadata'
        params = {'versionComment': 'METADATA_UPDATE'}
        self.make_request('POST', url, params=params, json_data=properties)

    def get_node_timestamp(self, node):
        meta = self.get_metadata(node.id)
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
        self.make_request('POST', url, params=params)

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
            raise RequestErrorResponseException(response, node_id)
        files['image'][1].close()


class RequestFailedException(Exception):
    pass


class RequestErrorResponseException(RequestFailedException):
    def __init__(self, response: requests.Response, context_hint: str = ''):
        self.response = response
        msg = f'Request failed: {context_hint}; {response.status_code} {response.reason}: {response.text}'
        super(RequestErrorResponseException, self).__init__(msg)


class RequestTimeoutException(RequestFailedException):
    pass


class ConnectionErrorException(RequestFailedException):
    pass


class FoundTooManyException(RequestFailedException):
    def __init__(self, name: str):
        super(FoundTooManyException, self).__init__(f'Found too many of {name}')


class NotFoundException(RequestFailedException):
    def __init__(self, name: str):
        super(NotFoundException, self).__init__(f'Could not find {name}')
