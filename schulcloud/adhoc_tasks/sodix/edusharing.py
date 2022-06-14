import json
from typing import Dict, List, Literal

import requests
import requests.auth


class Node:

    def __init__(self, obj: Dict):
        try:
            self.id: str = obj['ref']['id']
            self.name: str = obj['name']
            self.is_directory: bool = obj['isDirectory']
        except KeyError:
            raise RuntimeError(f'Could not parse node object: {obj}')
        self.obj = obj

    def __repr__(self):
        return f'Node<{self.id}, {self.name}, is_dir={self.is_directory}>'


class EdusharingAPI:
    query_string = ""

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url + 'rest'
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = requests.auth.HTTPBasicAuth(self.username, self.password)

    def make_request(self, method: Literal['GET', 'PUT', 'POST', 'DELETE'], url: str, params: Dict[str, str] = None):
        if not params:
            params = {}
        url = f'{self.base_url}{url}'
        headers = {'Accept': 'application/json'}
        return self.session.request(method, url, params=params, headers=headers)

    def make_request_permissions(self, method: Literal['GET', 'PUT', 'POST', 'DELETE'], url: str,
                                 params: Dict[str, str] = None):
        if not params:
            params = {}
        url = f'{self.base_url}{url}'
        headers = {"Accept": "application/json"}
        return self.session.request(method, url, params=params, json=self.get_body(), headers=headers)

    def set_body(self, groups: List[str]):

        string_parts = []
        for groupBlacklist in groups:
            string_part = \
                f'''\u007b
    "editable": true,
    "authority": \u007b
        "properties": \u007b\u007d,
        "authorityName": "GROUP_{groupBlacklist}",
        "authorityType": "GROUP"
    \u007d,
    "user": \u007b
        "primaryAffiliation": "string",
        "skills": [
            "string"
        ],
        "types": [
            "string"
        ],
        "vcard": "string",
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "avatar": "string",
        "about": "string"
    \u007d,
    "group": \u007b
        "groupEmail": "string",
        "displayName": "{groupBlacklist}",
        "groupType": "string",
        "scopeType": "string"
    \u007d,
    "permissions": [
        "Consumer"
    ]
\u007d'''

            string_parts.append(string_part)

        complete_string = ""
        for i in range(len(string_parts)):
            if i == len(string_parts) - 1:
                complete_string = complete_string + string_parts[i]
            else:
                complete_string = complete_string + string_parts[i] + ",\n"

        self.query_string = \
            f'''\u007b
    "inherited": false,
    "permissions": [
        {complete_string} 
    ]
\u007d'''

    def get_body(self):
        return json.loads(self.query_string)

    def get_children(self, node_id: str) -> List[Node]:
        url = f'/node/v1/nodes/-home-/{node_id}/children'
        response = self.make_request('GET', url, {'maxItems': '500', 'skipCount': '0'})
        if response.status_code == 200:
            try:
                return [Node(node) for node in response.json()['nodes']]
            except KeyError:
                raise RuntimeError(f'Could not parse response: {response.text}')
        else:
            raise RuntimeError(f'Unexpected response: {response.status_code}: {response.text}')

    def delete_node(self, node_id: str):
        url = f'/node/v1/nodes/-home-/{node_id}'
        response = self.make_request('DELETE', url)
        if not response.status_code == 200:
            raise RuntimeError(f'Request failed: {response.status_code}: {response.text}')

    def set_permissions(self, node_id: str, groups: List[str], inheritance: bool = False):
        # TODO: implement api call: https://edusharing.staging.hpi-schul-cloud.org/edu-sharing/swagger/#!/NODE_v1/setPermission
        url = f'/node/v1/nodes/-home-/{node_id}/permissions?sendMail=false&sendCopy=false'
        self.set_body(groups)
        response = self.make_request_permissions('POST', url)
        if not response.status_code == 200:
            raise RuntimeError(f'Request failed: {response.status_code}: {response.text}')
