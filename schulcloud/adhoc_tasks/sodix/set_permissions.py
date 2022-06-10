#!/usr/bin/python3

import json
import logging
from typing import Literal, Dict, List

import requests
import requests.auth

import util


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


class Blacklist:

    def __init__(self, all_groups: List[str]):
        self.all_groups = all_groups
        self.permissions = {}

    def block_permission(self, group: str, publisher_id: str):
        if publisher_id not in self.permissions:
            self.permissions[publisher_id] = set(self.all_groups)
        self.permissions[publisher_id].remove(group)

    def get_groups(self, publisher_id: str):
        if publisher_id in self.permissions:
            return self.permissions[publisher_id]
        else:
            return self.all_groups


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

    def make_request(self, method: Literal['GET', 'POST'], url: str, params: Dict[str, str]):
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

    def set_permissions(self, node_id: str, groups: List[str], inheritance: bool = False):
        # TODO: implement api call: https://edusharing.staging.hpi-schul-cloud.org/edu-sharing/swagger/#!/NODE_v1/setPermission
        pass


def find_node_by_name(api: EdusharingAPI, parent_id: str, child_name: str) -> Node:
    nodes = api.get_children(parent_id)
    for node in nodes:
        if node.name == child_name:
            return node
    raise RuntimeError(f'Could not find node {child_name}')


def load_json_file(file_path: str):
    file = open(file_path)
    data = file.read()
    file.close()
    return json.loads(data)


def create_blacklist_from_json(file_path: str):
    permission_file = load_json_file(file_path)
    all_groups = permission_file['all_groups']
    blacklist = Blacklist(all_groups)

    for group in permission_file['blacklist']:
        for publisher in permission_file['blacklist'][group]:
            blacklist.block_permission(group, publisher['id'])

    return blacklist


def main():
    environment = util.Environment(ENV_VARS, ask_for_missing=True)
    blacklist = create_blacklist_from_json('blacklist.json')

    api = EdusharingAPI(environment['EDU_SHARING_BASE_URL'], environment['EDU_SHARING_USERNAME'], environment['EDU_SHARING_PASSWORD'])

    sync = find_node_by_name(api, '-userhome-', 'SYNC_OBJ')
    sodix_spider = find_node_by_name(api, sync.id, 'sodix_spider')
    publisher_directories = [node for node in api.get_children(sodix_spider.id) if node.is_directory]

    for dir in publisher_directories:
        publisher_id = dir.name
        if not (dir.name.isalnum() and len(dir.name) == 24):
            logging.warning(f'Skipped directory because name is not a proper id: {publisher_id}')

        groups = blacklist.get_groups(publisher_id)

        if groups is blacklist.all_groups:
            api.set_permissions(dir.id, [], inheritance=True)
        else:
            # if we want, we could turn off inheritance even if all groups are allowed
            api.set_permissions(dir.id, groups, inheritance=False)
        #print(f'{dir.name} -> {groups}')


if __name__ == '__main__':
    main()
