import time
import traceback

from schulcloud.util import Environment
from schulcloud.edusharing import EdusharingAPI, Node, RequestErrorResponseException


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


class ContentQuantityEvaluation:
    def __init__(self):
        env = Environment(env_vars=ENV_VARS)
        self.api = EdusharingAPI(
            env['EDU_SHARING_BASE_URL'],
            username=env['EDU_SHARING_USERNAME'],
            password=env['EDU_SHARING_PASSWORD']
        )
        self.folders = []

    def gather_folders_recursively(self, folder: Node, depth=1):
        if depth >= 3:
            return
        print(f'Gather {folder.name}...')
        folders = self.api.get_children(folder.id, type='folders')
        self.folders.extend(folders)
        for folder in folders:
            self.gather_folders_recursively(folder, depth=depth+1)

    def get_folder_content_count(self, folder_id: str) -> int:
        url = f'/node/v1/nodes/-home-/{folder_id}/children'
        params = {
            'skipCount': '0',
            'maxItems': '1',
            'filter': 'files'
        }
        while True:
            try:
                response = self.api.make_request('GET', url, params)
                break
            except RequestErrorResponseException:
                traceback.print_exc()
                time.sleep(10)
                continue
        return response.json()['pagination']['total']

    def run(self):
        sync_obj = self.api.get_sync_obj_folder()
        self.gather_folders_recursively(sync_obj)

        for folder in self.folders:
            count = self.get_folder_content_count(folder.id)
            print(f'{count:>6} {folder.name}')


if __name__ == '__main__':
    ContentQuantityEvaluation().run()
