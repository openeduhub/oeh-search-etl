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
        """
        Generate permission-body for request.
        @param groups: List of permitted groups
        @param inheritance: Boolean, if inheritance is wanted or not
        """
        permissions = []
        for group in groups:
            permission = {
                "editable": "true",
                "authority": {
                    "authorityName": f'GROUP_{group}',
                    "authorityType": "GROUP"
                },
                "group": {
                    "displayName": group
                },
                "permissions": ["Consumer"]
            }

            permissions.append(permission)

        return {
            "inherited": inheritance,
            "permissions": permissions
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
        """
        Request method for the Edu-Sharing API.
        @param method: HTTP-method (GET, POST, PUT, DELETE)
        @param url: API URL for the request
        @param params: Additional params
        @param json_data: Request body as JSON
        @param files: Files for upload
        @param stream: Stream for upload
        @param retry: Number of retries, if the request failed
        @param timeout: Time between a retry
        """
        url = f'{self.base_url}{url}'
        headers = {'Accept': 'application/json'}
        i = -1
        while True:
            i += 1
            try:
                response = self.session.request(method, url, params=params, headers=headers,
                                                json=json_data, files=files, stream=stream, timeout=timeout)
            except requests.exceptions.ReadTimeout:
                if i < retry:
                    time.sleep(i // 2)
                    continue
                else:
                    raise RequestTimeoutException()
            if 500 <= response.status_code < 600 and i < retry:
                time.sleep(i // 2)
                continue
            return response

    def get_all(self, url: str, params: Dict[str, str], callback: Callable, max_items: int, retry: int = 50, timeout: Optional[float] = None):
        offset = 0
        items = []
        params['maxItems'] = str(max_items)
        while True:
            params['skipCount'] = str(offset)
            response = self.make_request('GET', url, params, retry=retry, timeout=timeout)
            if response.status_code == 200:
                try:
                    content = response.json()
                    callback(items, content)
                    offset += content['pagination']['count']
                    total = content['pagination']['total']
                except KeyError:
                    raise RuntimeError(f'Could not parse response: {response.text}')
                if offset >= total:
                    break
            else:
                raise RequestErrorResponseException(response)
        return items

    def get_application_properties(self, xml_file_name: str):
        """
        Return the properties of the application.
        @param xml_file_name: Name of the XML-file
        """
        url = f'/admin/v1/applications/{xml_file_name}'
        response = self.make_request('GET', url)
        if not 200 <= response.status_code < 300:
            raise RequestErrorResponseException(response)
        return response.json()

    def set_application_properties(self, xml_file_name: str, values: Dict[str, str]):
        """
        Set the properties of the application.
        @param xml_file_name: Name of the XML-file
        @param values: Values for the properties
        """
        url = f'/admin/v1/applications/{xml_file_name}'
        response = self.make_request('PUT', url, json_data=values)
        if not response.status_code == 200:
            raise RequestErrorResponseException(response)

    def upload_content(self, node_id: str, filename: str, file: IO[bytes], mimetype: str = ''):
        """
        Upload local file into node.
        @param node_id: ID of the node
        @param filename: Name of the local file
        @param file: File as binary files
        @param mimetype: Filetype
        """
        url = f'/node/v1/nodes/-home-/{node_id}/content'
        params = {'versionComment': 'MAIN_FILE_UPLOAD', 'mimetype': mimetype}
        files = {
            'file': (filename, file, mimetype, {'Expires': '0'})
        }
        response = self.make_request('POST', url, params=params, files=files, stream=True)
        if not response.status_code == 200:
            raise RequestErrorResponseException(response)

    def get_user(self, name: str = None):
        """
        Return User by name.
        @param name: Name of the User
        """
        if name is None:
            name = '-me-'
        url = f'/iam/v1/people/-home-/{name}'
        response = self.make_request('GET', url)
        if response.status_code == 404:
            raise NotFoundException(name)
        if not 200 <= response.status_code < 300:
            raise RequestErrorResponseException(response)
        return response.json()

    def get_users(self):
        """
        Get Users from -home- Repository.
        """
        url = f'/iam/v1/people/-home-'
        params = {'pattern': '*'}
        users = self.get_all(url, params, lambda items, content: items.extend(content['users']), 20)
        return users

    def create_user(self, username: str, password: str, type: Literal['function', 'system'], quota: int = 1024 ** 2):
        """
        Creates a User.
        @param username: Name for the User
        @param password: Password for the User
        @param type: Function or System account
        @param quota: Maximum of the download/upload size
        """
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
            raise RequestErrorResponseException(response)

    def delete_user(self, name: str):
        """
        Deletes a User.
        @param name: Name of the User
        """
        url = f'/iam/v1/people/-home-/{name}'
        params = {'force': 'true'}
        response = self.make_request('DELETE', url, params=params)
        if not 200 <= response.status_code < 300:
            raise RequestErrorResponseException(response)

    def user_get_groups(self, username: str):
        """
        Return the groups, the User belongs to.
        @param username: Name of the User
        """
        url = f'/iam/v1/people/-home-/{username}/memberships'
        groups = self.get_all(url, {}, lambda items, content: items.extend(content['groups']), 50)
        return groups

    def create_group(self, group_name: str):
        """
        Creates a group.
        @param group_name: Name of the group
        """
        url = f'/iam/v1/groups/-home-/{group_name}'
        body = {
            'displayName': group_name,
            'groupType': None,
            'scopeType': None
        }
        response = self.make_request('POST', url, json_data=body)
        if not response.status_code == 200:
            raise RequestErrorResponseException(response)

    def get_groups(self):
        """
        Returns the groups.
        """
        url = f'/iam/v1/groups/-home-/'
        params = {'pattern': '*'}
        groups = self.get_all(url, params, lambda items, content: items.extend(content['groups']), 256)
        return groups

    def group_add_user(self, group_name: str, user_name: str):
        """
        Add a User to a group.
        @param group_name: Name of the group
        @param user_name: Name of the User
        """
        url = f'/iam/v1/groups/-home-/GROUP_{group_name}/members/{user_name}'
        response = self.make_request('PUT', url)
        if not 200 <= response.status_code < 300:
            raise RequestErrorResponseException(response)

    def get_children(self, node_id: str, all_properties: bool = False,
                     type: Literal['all', 'folders', 'files'] = 'all') -> List[Node]:
        """
        Returns children of node.
        @param node_id: ID of the parent node
        @param all_properties: Boolean, if all properties as search criteria
        @param type: Type of the children - all, file or folder
        """
        url = f'/node/v1/nodes/-home-/{node_id}/children'
        params = {}
        if all_properties:
            params['propertyFilter'] = '-all-'
        if not type == 'all':
            if type not in ('files', 'folders'):
                raise ValueError(f'Unknown node type: {type}')
            params['filter'] = type
        children = self.get_all(url, params, lambda items, content: items.extend([Node(node) for node in content['nodes']]), 200)
        return children

    def find_node_by_name(self, parent_id: str, child_name: str) -> Node:
        """
        Returns node by name.
        @param parent_id: ID of the parent node
        @param child_name: Name of the child node corresponding to the parent ID
        """
        nodes = self.get_children(parent_id)
        for node in nodes:
            if node.name == child_name:
                return node
        raise NotFoundException(child_name)

    def find_node_by_replication_source_id(self, replication_source_id: str, skip_exception: Optional[bool] = False) -> Node:
        """
        Returns a node by replication source ID.
        @param replication_source_id: Replication Source ID of node
        """
        nodes = self.search_custom('ccm:replicationsourceid', replication_source_id, 2, 'FILES')
        if len(nodes) == 1:
            return nodes[0]
        elif len(nodes) > 1:
            raise FoundTooManyException(replication_source_id)
        else:
            if not skip_exception:
                raise NotFoundException(replication_source_id)

    def create_node(self, parent_id: str, name: str, type: Literal['file', 'folder'] = 'file',
                    properties: Optional[Dict] = None):
        """
        Creates a node with properties.
        @param parent_id: ID of the parent node
        @param name: Name for the node
        @param type: Type of the node - file or folder
        @param properties: Properties for the Node [Optional]
        """
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
            raise RequestErrorResponseException(response)
        return Node(response.json()['node'])

    def sync_node(self, group: str, properties: Dict, match: List[str], type: str = 'ccm:io',
                  group_by: Optional[str] = None):
        """
        Synchronize a node by group params.
        @param group: Group param
        @param properties: Properties for synchronization
        @param match: Matching param
        @param type: Type of the synchronization
        @param group_by: Grouped by the param
        """
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
            raise RequestErrorResponseException(response)
        return Node(response.json()['node'])

    def delete_node(self, node_id: str):
        """
        Delete a node by ID.
        @param node_id: Id of the node
        """
        url = f'/node/v1/nodes/-home-/{node_id}'
        response = self.make_request('DELETE', url)
        if not response.status_code == 200:
            raise RequestErrorResponseException(response)

    def get_sync_obj_folder(self):
        """
        Returns sync_obj folder of Edu-Sharing.
        """
        return self.get_or_create_node('-userhome-', 'SYNC_OBJ', type='folder')

    def file_exists(self, parent_id: str, name: str):
        # TODO: should only search within specific parent node, not global search
        return len(self.search_custom('cm:name', name, 2, 'FILES')) > 0

    def file_exists_by_name(self, name: str):
        """
        Returns boolean, if the file exists.
        @param name: Name of the file
        """
        name = name.replace(" ", "_")
        return len(self.search_custom('name', name, 2, 'FILES')) > 0

    def search_schulcloud(self, query: str):
        """
        Explicit 'Schulcloud-Verbund-Software' search query to get nodes.
        @param query: Searchword for the elasticsearch request
        """
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
        """
        Custom search query to get nodes.
        @param property: Property as search criterion
        @param value: Value as search criterion
        @param max_items: Number of returning nodes
        @param content_type: Search for file or folder
        """
        url = f'/search/v1/custom/-home-?contentType={content_type}&combineMode=AND&property={property}&value={value}' \
              f'&maxItems={max_items}&skipCount=0'
        response = self.make_request('GET', url)
        if not response.status_code == 200:
            raise RequestErrorResponseException(response)
        json_obj = response.json()
        return [Node(node) for node in json_obj['nodes']]

    def get_permissions(self, node_id: str):
        """
        Returns the permissions of the node.
        @param node_id: ID of the node
        """
        url = f'/node/v1/nodes/-home-/{node_id}/permissions'
        response = self.make_request('GET', url)
        if not response.status_code == 200:
            raise RequestErrorResponseException(response)
        try:
            return response.json()['permissions']
        except KeyError:
            raise RequestErrorResponseException(response)

    def set_permissions(self, node_id: str, groups: List[str], inheritance: bool) -> None:
        """
        Set the permissions for the node.
        @param node_id: ID of the node
        @param groups: List of the authorized groups for instances
        @param inheritance: Inheritance True or False
        """
        url = f'/node/v1/nodes/-home-/{node_id}/permissions?sendMail=false&sendCopy=false'
        json = self._craft_permission_body(groups, inheritance)
        response = self.make_request('POST', url, json_data=json, retry=1)
        if not response.status_code == 200:
            raise RequestErrorResponseException(response)

    def get_metadata(self, node_id: str):
        """
        Returns the metadata of the node.
        @param node_id: ID of the node
        """
        url = f'/node/v1/nodes/-home-/{node_id}/metadata'
        response = self.make_request('GET', url)
        if not response.status_code == 200:
            raise RequestErrorResponseException(response)
        return response.json()

    def change_metadata(self, node_id: str, properties: Dict[str, List[str]]):
        """
        Change the metadata of the node.
        @param node_id: ID of the node
        @param properties: Dictionary of the properties to change
        """
        url = f'/node/v1/nodes/-home-/{node_id}/metadata'
        params = {'versionComment': 'METADATA_UPDATE'}
        response = self.make_request('POST', url, params=params, json_data=properties)
        if not response.status_code == 200:
            raise RequestErrorResponseException(response)

    def get_node_timestamp(self, node):
        """
        Returns timestamp of the node.
        @param node: The node for getting timestamp
        """
        meta = self.get_metadata(node.id)
        timestamp_str = str(meta["node"]["createdAt"]).replace("Z", "")
        return datetime.fromisoformat(timestamp_str)

    def get_or_create_node(self, parent_id: str, name: str, type: Literal['file', 'folder'] = 'file',
                           properties: Optional[Dict] = None):
        """
        Try to get the node by name. If the node doesn't exist, the method creates a new node with the given name.
        @param parent_id: ID of the parent node
        @param name: Name of the node
        @param type: Declare if the node is a file or a folder - default: file
        @param properties: Change the metadata of the node by the given properties
        """
        try:
            folder = self.find_node_by_name(parent_id, name)
            if properties:
                self.change_metadata(folder.id, properties)
        except NotFoundException:
            folder = self.create_node(parent_id, name, type=type, properties=properties)
        return folder

    def set_property(self, node_id: str, property: str, value: Optional[List[str]]):
        """
        Sets new property/value pair accordingly to metadataset 'mds_oeh'.
        @param node_id: ID of node
        @param property: Property of the metadataset 'mds_oeh'
        @param property: Value's of the property
        """
        url = f'/node/v1/nodes/-home-/{node_id}/property'
        params = {'property': property}
        if value is not None:
            params['value'] = value
        response = self.make_request('POST', url, params=params, retry=0)
        if not response.status_code == 200 and response.status_code > 500:
            raise RequestErrorResponseException(response, node_id)

    def set_collection_children(self, node_id: str, children_uuids: List[str]):
        """
        Sets collection relation to its children. Reverse operation is also needed for all children.
        @param children_uuids: replication source uuids of ALL children
        @param node_id: ID of node
        """
        # frontend relies on exact syntax, no double quotes (as in json) allowed
        value = f"{{kind': 'hasparts', 'resource': {{'identifier': {str(children_uuids)}}}}}"
        for property in 'ccm:lom_relation', 'ccm:hpi_lom_relation':
            self.set_property(node_id, property, [value])

    def set_collection_parent(self, node_id: str, parent_uuid: str):
        """
        Sets node's relation to its collection. Reverse operation is needed for collection.
        @param parent_uuid: replication source uuid of parent
        @param node_id: ID of node
        """
        # frontend relies on exact syntax, no double quotes (as in json) allowed
        value = f"{{'kind': 'ispartof', 'resource': {{'identifier': ['{parent_uuid}']}}}}"
        for property in 'ccm:lom_relation', 'ccm:hpi_lom_relation':
            self.set_property(node_id, property, [value])

    def set_preview_thumbnail(self, node_id: str, filename: str, type: Literal['local', 'remote'] = 'local'):
        """
        Sets node's preview thumbnail.
        @param node_id: ID of node
        @param filename: Name of the file
        @param type: 'local' for local images, 'remote' for S3-binary-images
        """
        if type == 'local':
            url = f'/node/v1/nodes/-home-/{node_id}/preview?mimetype=image'
            files = {'image': (filename, open(filename, 'rb'))}
            response = self.make_request('POST', url, files=files, stream=True)
            if not response.status_code == 200:
                raise RequestErrorResponseException(response, node_id)
            files['image'][1].close()
        if type == 'remote':
            url = f'/node/v1/nodes/-home-/{node_id}/preview?mimetype=image'
            files = {'image': filename}
            response = self.make_request('POST', url, files=files, stream=True)
            if not response.status_code == 200:
                raise RequestFailedException(response, node_id)


class RequestFailedException(Exception):
    pass


class RequestErrorResponseException(RequestFailedException):
    def __init__(self, response: requests.Response, context_hint: str = ''):
        msg = f'Request failed: {context_hint}; {response.status_code} {response.reason}: {response.text}'
        super(RequestErrorResponseException, self).__init__(msg)


class RequestTimeoutException(RequestFailedException):
    pass


class FoundTooManyException(RequestFailedException):
    def __init__(self, name: str):
        super(FoundTooManyException, self).__init__(f'Found too many of {name}')


class NotFoundException(RequestFailedException):
    def __init__(self, name: str):
        super(NotFoundException, self).__init__(f'Could not find {name}')
