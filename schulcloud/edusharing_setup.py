import json
import os.path
from dataclasses import dataclass
from typing import List, Set, Literal

from schulcloud.edusharing import EdusharingAPI, NotFoundException
from schulcloud.util import Environment


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


@dataclass
class User:
    name: str
    password: str
    type: Literal['function', 'system']
    groups: List[str]


class EdusharingSetup:
    def __init__(self):
        self.env = Environment(ENV_VARS, ask_for_missing=True)
        self.api = EdusharingAPI(
            self.env['EDU_SHARING_BASE_URL'],
            self.env['EDU_SHARING_USERNAME'],
            self.env['EDU_SHARING_PASSWORD'])

    def _add_metadata_sets(self):
        xml_name = 'homeApplication.properties.xml'
        key, value = 'metadatasetsV2', 'mds,mds_oeh'
        properties = self.api.get_application_properties(xml_name)
        if key not in properties or not properties[key] == value:
            properties[key] = value
            self.api.set_application_properties(xml_name, properties)

    def _add_users_and_groups(self, users: List[User], groups: Set[str]):
        # requirement: all groups within "users" must also be within "groups"

        existing_usernames = [user['userName'] for user in self.api.get_users()]

        for user in users:
            if user.name not in existing_usernames:
                self.api.create_user(user.name, user.password, user.type)
                print(f'Created user {user.name}')
            else:
                print(f'User already exists: {user.name}')

        existing_groupnames = [group['groupName'] for group in self.api.get_groups()]

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
        # the color picker h5p content contains the color picker library needed for other h5p items
        # which will be installed after upload
        colorpicker_path = 'schulcloud/update_colorpicker.h5p'
        colorpicker_name = os.path.basename(colorpicker_path)
        try:
            self.api.find_node_by_name('-userhome-', colorpicker_name)
        except NotFoundException:
            node = self.api.create_node('-userhome-', colorpicker_name)
            file = open(colorpicker_path, 'rb')
            self.api.upload_content(node.id, colorpicker_name, file)
            file.close()

    def _county_workaround(self):
        counties = [
            'county-3455',
            'county-3357',
            'county-3103',
            'county-3156',
            'county-3154',
            'county-3100',
            'county-3254',
            'county-3355',
            'county-3359',
            'county-3461',
            'county-3256',
            'county-3404',
            'county-3459',
            'county-3462',
            'county-3352',
            'county-3356',
            'county-3401',
            'county-3151',
            'county-3158',
            'county-3360',
            'county-3453',
            'county-3458',
            'county-3152',
            'county-3403',
            'county-3452',
            'county-3155',
            'county-3101',
            'county-3241',
            'county-3252',
            'county-3255',
            'county-3358',
            'county-3361',
            'county-3456',
            'county-3457',
            'county-3351',
            'county-3451',
            'county-3153',
            'county-3460',
            'county-3102',
            'county-3402',
            'county-3354',
            'county-3251',
            'county-3353',
            'county-3157',
            'county-3454',
            'county-3257',
            'LowerSaxony-private' 
        ]
        existing_groupnames = [group['groupName'] for group in self.api.get_groups()]

        for county in counties:
            if county not in existing_groupnames:
                self.api.create_group(county)
                print(f'Created group {county}')
            else:
                print(f'Group already exists: {county}')

    def run(self, users: List[User], groups: List[str]):
        groups = set(groups)
        for user in users:
            for group in user.groups:
                groups.add(group)

        self._add_metadata_sets()
        self._add_users_and_groups(users, groups)
        # only needed when setup is scaled - has to run on single replica (repository-service)
        # self._county_workaround()  # TODO: remove once fixed
        self._upload_color_picker()


def temporary_setup():
    file = open('schulcloud/es_users.json')
    obj = json.load(file)
    file.close()
    json_users = obj['users']
    groups = obj['groups']
    users = []
    for json_user in json_users:
        users.append(User(json_user[0], json_user[1], json_user[2], json_user[3]))
    EdusharingSetup().run(users, groups)


def example():
    # users and groups should be taken from 1password
    users: List[User] = [
        User('BrandenburgUser', 'test123', 'function', ['Brandenburg-public, Brandenburg-private'])
    ]
    other_groups = ['public']
    EdusharingSetup().run(users, other_groups)


if __name__ == '__main__':
    temporary_setup()
