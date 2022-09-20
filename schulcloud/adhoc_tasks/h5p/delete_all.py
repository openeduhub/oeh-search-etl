
import random

import edusharing
import util


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


def find_node_by_name(api: edusharing.EdusharingAPI, parent_id: str, child_name: str) -> edusharing.Node:
    nodes = api.get_children(parent_id)
    for node in nodes:
        if node.name == child_name:
            return node
    raise RuntimeError(f'Could not find node {child_name}')


def main():
    environment = util.Environment(ENV_VARS, ask_for_missing=True)

    api = edusharing.EdusharingAPI(
        environment['EDU_SHARING_BASE_URL'],
        environment['EDU_SHARING_USERNAME'],
        environment['EDU_SHARING_PASSWORD'])

    sync = find_node_by_name(api, '-userhome-', 'SYNC_OBJ')
    sodix_spider = find_node_by_name(api, sync.id, 'sodix_spider')
    publisher_directories = [node for node in api.get_children(sodix_spider.id) if node.is_directory]
    random.shuffle(publisher_directories)

    count = 0
    for dir in publisher_directories:
        try:
            children = api.get_children(dir.id)
        except RuntimeError:
            continue
        for child in children:
            count += 1
            try:
                api.delete_node(child.id)
                print(f'{count} deleted')
            except RuntimeError:
                print(f'{count} error')
        try:
            api.delete_node(dir.id)
            print('dir deleted')
        except RuntimeError:
            print('dir error')
            continue


if __name__ == '__main__':
    main()
