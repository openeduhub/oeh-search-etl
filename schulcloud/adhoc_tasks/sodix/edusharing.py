
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
        pass
