import json
import os.path
import sys
import traceback

from schulcloud.edusharing import EdusharingAPI, Node, RequestFailedException
from schulcloud.util import Environment


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


class PermissionUpdater:
    def __init__(self):
        self.env = Environment(env_vars=ENV_VARS)
        self.api = EdusharingAPI(
            self.env['EDU_SHARING_BASE_URL'],
            self.env['EDU_SHARING_USERNAME'],
            self.env['EDU_SHARING_PASSWORD']
        )
        self.node_cache: dict[str, Node] = {}

    def get_node_by_path(self, path: str) -> Node:
        path = os.path.normpath(path)
        try:
            return self.node_cache[path]
        except KeyError:
            pass
        parent_path = os.path.dirname(path)
        if parent_path:
            parent_id = self.get_node_by_path(parent_path).id
        else:
            parent_id = '-userhome-'
        node_name = os.path.basename(path)
        node = None
        for child in self.api.get_children(parent_id, type='folders'):
            self.node_cache[os.path.join(parent_path, child.name)] = child
            if child.name == node_name:
                node = child
        if node is None:
            raise PathNotFoundException(path)
        else:
            return node

    def run(self):
        file = open('schulcloud/permissions.json')
        permissions = json.load(file)['permissions']
        file.close()
        for permission in permissions:
            print()
            print(permission['path'])
            try:
                node = self.get_node_by_path(permission['path'])
                self.api.set_permissions(node.id, permission['permitted_groups'], permission['inherit'])
            except PathNotFoundException:
                print(f'Warning: Could not find {permission["path"]}', file=sys.stderr)
            except:
                print(f'Error: Could not set permission for {permission["path"]}', file=sys.stderr)
                traceback.print_exc()


class PathNotFoundException(Exception):
    def __init__(self, path: str):
        super(PathNotFoundException, self).__init__(f'Path not found: {path}')
        self.path = path


if __name__ == '__main__':
    PermissionUpdater().run()
