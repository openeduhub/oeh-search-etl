import datetime
import time
import traceback

from schulcloud.util import Environment
from schulcloud.edusharing import EdusharingAPI, Node, RequestErrorResponseException, RequestTimeoutException

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
            self.gather_folders_recursively(folder, depth=depth + 1)

    def get_folder_content_count(self, folder: Node) -> int:
        url = f'/node/v1/nodes/-home-/{folder.id}/children'
        params = {
            'skipCount': '0',
            'maxItems': '1',
            'filter': 'files'
        }
        while True:
            try:
                print(f'{datetime.datetime.now()} get content count of {folder.name}')
                response = self.api.make_request('GET', url, params, retry=0)
                print(f'--> {response.status_code}')
                break
            except RequestTimeoutException:
                print('--> Timeout')
            except RequestErrorResponseException as err:
                print(f'--> {err.response.status_code} {err.response.reason} {err.response.text if err.response.status_code == 500 else ""}')
            time.sleep(10)
        response.raise_for_status()
        content = response.json()
        count = content['pagination']['total']
        print('Count:', count)
        return count

    def run(self):
        print('Results are printed when done or stopped.')
        sync_obj = self.api.get_sync_obj_folder()
        self.gather_folders_recursively(sync_obj)

        counts = []
        for folder in self.folders:
            try:
                max_count = -1
                while True:
                    count = self.get_folder_content_count(folder)
                    print()
                    if count == max_count:
                        break
                    elif count > max_count:
                        max_count = count
                counts.append((folder.name, count))
            except (SystemExit, KeyboardInterrupt):
                break
            except Exception:
                traceback.print_exc()

        counts.sort(key=lambda item: item[0])

        print()
        print()
        print('Results:')
        for folder_name, count in counts:
            print(f'{folder_name:<90} {count:>6}')


if __name__ == '__main__':
    ContentQuantityEvaluation().run()
