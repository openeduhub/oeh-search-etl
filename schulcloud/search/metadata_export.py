
import json
import os

import tqdm

from schulcloud.util import Environment
from schulcloud.edusharing import EdusharingAPI, Node


ENV_VARS = [
    'EDU_SHARING_BASE_URL',
    'EDU_SHARING_USERNAME',
    'EDU_SHARING_PASSWORD'
]


class MetadataExporter:
    FOLDER = 'schulcloud/search/metadata'

    def __init__(self):
        self.env = Environment(env_vars=ENV_VARS)
        self.api = EdusharingAPI(self.env['EDU_SHARING_BASE_URL'], self.env['EDU_SHARING_USERNAME'], self.env['EDU_SHARING_PASSWORD'])
        self.sync_obj = self.api.get_sync_obj_folder()
        self.json_file_count = 0
        self.progress_stack = []

    def print_progress(self, current: str = ''):
        print('\r', end='')
        for progress in self.progress_stack:
            print(f'{progress[0]}/{progress[1]} ', end='')
        print(current, end='')

    def get_json_file(self, name: str):
        if not os.path.exists(self.FOLDER):
            os.makedirs(self.FOLDER)
        file = open(os.path.join(self.FOLDER, f'{self.json_file_count:03}_{name}'), 'w')
        self.json_file_count += 1
        return file

    def search_directory(self, dir: Node, path: str = ''):
        results = []
        progress_i = len(self.progress_stack)
        self.progress_stack.append((0, 0))
        children = self.api.get_children(dir.id)
        path += dir.name + '/'

        for i in range(len(children)):
            self.progress_stack[progress_i] = (i, len(children))
            self.print_progress(path)
            child = children[i]
            if child.is_directory:
                self.search_directory(child, path)
            else:
                results.append(child.obj)
        file = self.get_json_file(path.replace('/', '_'))
        json.dump(results, file)
        file.close()

        self.progress_stack.pop()

    def run(self):
        self.search_directory(self.sync_obj)
        print()


if __name__ == '__main__':
    MetadataExporter().run()
