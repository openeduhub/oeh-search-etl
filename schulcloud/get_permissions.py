
import sys
import json

from schulcloud.edusharing import EdusharingAPI, Node
from schulcloud.util import Environment


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


class PermissionStuff:
    def __init__(self):
        self.env = Environment(env_vars=ENV_VARS)
        self.api = EdusharingAPI(
            self.env['EDU_SHARING_BASE_URL'],
            self.env['EDU_SHARING_USERNAME'],
            self.env['EDU_SHARING_PASSWORD']
        )
        self.permissions = []
        self.path_stack: list[Node] = []
        self.white_list = [
            'SYNC_OBJ',
            'SYNC_OBJ/oeh_spider',
            'SYNC_OBJ/sodix_spider'
        ]

    def get_current_path(self):
        """
        Get the current path of the folder.
        """
        return '/'.join([folder.name for folder in self.path_stack])

    def get_permissions(self, node: Node):
        """
        Get the current permission of the node.
        @param node: Node of Edu-Sharing
        """
        if node.name == 'geogebra_spider' or self.path_stack and self.path_stack[-1].name == 'sodix_spider':
            return
        self.path_stack.append(node)
        print(self.get_current_path())
        permissions = self.api.get_permissions(node.id)
        for permission_list in permissions['localPermissions']['permissions'], permissions['inheritedPermissions']:
            for i in range(len(permission_list)):
                permission_list[i] = permission_list[i]['authority']['authorityName']
        self.permissions.append(
            {
                'path': self.get_current_path(),
                'permissions': permissions
            }
        )
        if self.get_current_path() in self.white_list:
            for child in self.api.get_children(node.id, type='folders'):
                if child.is_directory:
                    self.get_permissions(child)
        self.path_stack.pop()

    def run(self):
        """
        Run the permissions.
        """
        sync_obj = self.api.get_sync_obj_folder()
        self.get_permissions(sync_obj)
        file = open(sys.argv[1], 'w')
        json.dump(self.permissions, file)
        file.close()


if __name__ == '__main__':
    PermissionStuff().run()
