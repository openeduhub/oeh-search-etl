import json
import os.path
from dataclasses import dataclass
from typing import List, Set, Literal

from schulcloud.edusharing import EdusharingAPI, NotFoundException
from schulcloud.util import Environment


ADMIN_GROUP = 'ALFRESCO_ADMINISTRATORS'
ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD', 'SETUP_CONFIG_PATH']


@dataclass
class User:
    name: str
    password: str
    type: Literal['function', 'system']
    groups: List[str]


class EdusharingSetup:
    def __init__(self, es_url: str, user: str, password: str):
        self.api = EdusharingAPI(es_url, user, password)

    def _add_metadata_sets(self):
        xml_name = 'homeApplication.properties.xml'
        key, value = 'metadatasetsV2', 'mds,mds_oeh'
        properties = self.api.get_application_properties(xml_name)
        if key not in properties or not properties[key] == value:
            properties[key] = value
            self.api.set_application_properties(xml_name, properties)

    def _add_users_and_groups(self, users: List[User], groups: Set[str]):
        existing_usernames = [user['userName'] for user in self.api.get_users()]

        for user in users:
            if user.name not in existing_usernames:
                self.api.create_user(user.name, user.password, user.type)
                print(f'Created user {user.name}')
            else:
                print(f'User already exists: {user.name}')

        existing_groupnames = [group['groupName'] for group in self.api.get_groups()]

        # handle admin group
        existing_groupnames.append(ADMIN_GROUP)
        for user in users:
            if user.type == 'system' and ADMIN_GROUP not in user.groups:
                user.groups.append(ADMIN_GROUP)

        for group in groups:
            if group not in existing_groupnames:
                self.api.create_group(group)
                print(f'Created group {group}')
            else:
                print(f'Group already exists: {group}')

        for user in users:
            existing_memberships = [group['groupName'] for group in self.api.user_get_groups(user.name)]
            for group in user.groups:
                if group not in existing_memberships:
                    self.api.group_add_user(group, user.name)

    def _upload_color_picker(self):
        colorpicker_path = 'schulcloud/update_colorpicker.h5p'
        colorpicker_name = os.path.basename(colorpicker_path)
        if not self.api.find_node_by_name('-userhome-', colorpicker_name):
            node = self.api.create_node('-userhome-', colorpicker_name)
            file = open(colorpicker_path, 'rb')
            self.api.upload_content(node.id, colorpicker_name, file)
            file.close()

    def run(self, users: List[User], other_groups: List[str]):
        other_groups = set(other_groups)
        for user in users:
            for group in user.groups:
                other_groups.add(group)

        self._add_metadata_sets()
        self._add_users_and_groups(users, other_groups)
        self._upload_color_picker()


def main():
    env = Environment(ENV_VARS, ask_for_missing=False)

    # look into es_users.example.json for how a config file should look like
    file = open(env['SETUP_CONFIG_PATH'])
    obj = json.load(file)
    file.close()
    groups = obj['groups']
    users = [User(user[0], user[1], user[2], user[3]) for user in obj['users']]

    setup = EdusharingSetup(
        env['EDU_SHARING_BASE_URL'],
        env['EDU_SHARING_USERNAME'],
        env['EDU_SHARING_PASSWORD']
    )
    setup.run(users, groups)


if __name__ == '__main__':
    main()
