
import json
from typing import List

from schulcloud.edusharing import EdusharingAPI, Node
from schulcloud.util import Environment


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']
BLACKLIST_PATH = 'schulcloud/sodix/blacklist.json'

class Blacklist:

    def __init__(self, all_groups: List[str]):
        if 'all' in all_groups:
            raise RuntimeError('Group cannot be named "all"')
        self.all_groups = set(all_groups)
        self.permissions = {}

    def block_permission(self, group: str, publisher_id: str):
        if group == 'all':
            self.permissions[publisher_id] = set()
        else:
            if publisher_id not in self.permissions:
                self.permissions[publisher_id] = set(self.all_groups)
            self.permissions[publisher_id].remove(group)

    def get_groups(self, publisher_id: str):
        if publisher_id in self.permissions:
            return self.permissions[publisher_id]
        else:
            return self.all_groups


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
        if group == 'all':
            # handle edge case explicitly
            for publisher in permission_file['blacklist']['all']:
                blacklist.block_permission('all', publisher['id'])
        else:
            for publisher in permission_file['blacklist'][group]:
                blacklist.block_permission(group, publisher['id'])

    return blacklist


def main():
    environment = Environment(ENV_VARS, ask_for_missing=True)
    blacklist = create_blacklist_from_json(BLACKLIST_PATH)

    api = EdusharingAPI(
        environment['EDU_SHARING_BASE_URL'],
        environment['EDU_SHARING_USERNAME'],
        environment['EDU_SHARING_PASSWORD'])

    sync = find_node_by_name(api, '-userhome-', 'SYNC_OBJ')
    sodix_spider = find_node_by_name(api, sync.id, 'sodix_spider')
    publisher_directories = [node for node in api.get_children(sodix_spider.id) if node.is_directory]

    for dir in publisher_directories:
        publisher_id = dir.name
        print(dir.name)
        if not (dir.name.isalnum() and len(dir.name) == 24):
            print(f'Warning: Skipped directory because name is not a proper id: {publisher_id}')
            continue

        groups_blacklist = blacklist.get_groups(publisher_id)

        if groups_blacklist is blacklist.all_groups:
            api.set_permissions(dir.id, list(blacklist.all_groups), inheritance=True)
        else:
            api.set_permissions(dir.id, list(groups_blacklist), inheritance=False)


if __name__ == '__main__':
    main()
