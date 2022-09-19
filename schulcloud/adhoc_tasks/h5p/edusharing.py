from typing import Dict, List, Literal, Optional

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
                     params: Optional[Dict[str, str]] = None, json_data: Optional[Dict] = None,
                     files: Optional[Dict] = None, stream: bool = False):
        url = f'{self.base_url}{url}'
        headers = {'Accept': 'application/json'}
        return self.session.request(method, url, params=params, headers=headers,
                                    json=json_data, files=files, stream=stream)

    def create_user(self, username: str, password: str, type: Literal['function', 'system'], quota: int = 1024 ** 2):
        url = f'/iam/v1/people/-home-/{username}?password={password}'
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
        response = self.make_request('POST', url, json_data=body)
        # response.raise_for_status()

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

    def delete_node(self, node_id: str):
        url = f'/node/v1/nodes/-home-/{node_id}'
        response = self.make_request('DELETE', url)
        if not response.status_code == 200:
            raise RequestFailedException(response)

    def set_permissions(self, node_id: str, groups: List[str], inheritance: bool):
        url = f'/node/v1/nodes/-home-/{node_id}/permissions?sendMail=false&sendCopy=false'
        response = self.make_request('POST', url, json_data=self._craft_permission_body(groups, inheritance))
        if not response.status_code == 200:
            raise RequestFailedException(response)

    def get_sync_obj_folder(self):
        return self.get_or_create_folder('-userhome-', 'SYNC_OBJ')

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

    def get_metadata_of_node(self, nodeId: str):
        url = f'/node/v1/nodes/-home-/{nodeId}/metadata'
        response = self.make_request('GET', url)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        json_obj = response.json()
        return json_obj

    def create_folder(self, parent_id: str, name: str, metadataset: str = 'mds_oeh', payload: Optional[Dict] = None):
        url = f'/node/v1/nodes/-home-/{parent_id}/children?type=cm%3Afolder&renameIfExists=false'
        if payload is None:
            payload = {}
        payload['cm:name'] = [name]
        payload['cm:edu_metadataset'] = [metadataset]
        payload['cm:edu_forcemetadataset'] = [True]
        response = self.make_request('POST', url, json_data=payload)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        return Node(response.json()['node'])

    def get_or_create_folder(self, parent_id: str, name: str, metadataset: str = 'mds_oeh',
                             payload: Optional[Dict] = None):
        try:
            folder = self.find_node_by_name(parent_id, name)
        except NotFoundException:
            folder = self.create_folder(parent_id, name, metadataset, payload)
            print(f"Created folder {name}")
        return folder

    # ToDo: Do we actual need this method anywhere?
    # def create_node(self, parent_id: str, name: str):
    #     url = f'/node/v1/nodes/-home-/{parent_id}/children/' \
    #           f'?type=ccm%3Aio&renameIfExists=true&assocType=&versionComment=&'
    #     data = {"cm:name": [name]}
    #     response = self.make_request('POST', url, json_data=data)
    #     if not response.status_code == 200:
    #         raise RequestFailedException(response)
    #     return Node(response.json()['node'])

    def sync_node(self, group: str, properties: Dict, match: List[str], type: str = 'ccm:io',
                  group_by: Optional[str] = None):
        url = f'/bulk/v1/sync/{group}?type={type}&resetVersion=false'
        if group_by is not None:
            url += f'&groupBy={group_by}'
        for m in match:
            url += f'&match={m}'
        response = self.make_request('PUT', url, json_data=properties)
        if not response.status_code == 200:
            raise RequestFailedException(response)
        return Node(response.json()['node'])

    def set_property_relation(self, node_id: str, property: str, value: List):
        property_replacement = property.replace(":", "%3A")
        url = f'/node/v1/nodes/-home-/{node_id}/property?property={property_replacement}&value=%7B\'kind\'' \
              f'%3A%20\'haspart\'%2C%20\'resource\'%3A%20%7B\'identifier\'%3A%20{value}%7D%7D'
        response = self.make_request('POST', url)
        if not response.status_code == 200:
            raise RequestFailedException(response, node_id)

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


class NotFoundException(Exception):
    def __init__(self, name: str):
        super(NotFoundException, self).__init__(f'Could not find {name}')
