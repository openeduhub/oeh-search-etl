
import random

import tqdm

from schulcloud.util import Environment
from schulcloud.edusharing import EdusharingAPI, Node


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


def find_node_by_name(api: EdusharingAPI, parent_id: str, child_name: str) -> Node:
    """
    Find Edu-Sharing nodes by name.
    @param api: Edu-Sharing API module
    @param parent_id: ID of the parent node
    @param child_name: Name of the child node
    """
    nodes = api.get_children(parent_id)
    for node in nodes:
        if node.name == child_name:
            return node
    raise RuntimeError(f'Could not find node {child_name}')


def delete_sodix(api: EdusharingAPI):
    """
    Delete all Sodix nodes on Edu-Sharing.
    @param api: Edu-Sharing API module
    """
    sync = find_node_by_name(api, '-userhome-', 'SYNC_OBJ')
    sodix_spider = find_node_by_name(api, sync.id, 'sodix_spider')
    publisher_directories = [node for node in api.get_children(sodix_spider.id) if node.is_directory]

    for dir in tqdm.tqdm(publisher_directories):
        try:
            children = api.get_children(dir.id)
            for child in tqdm.tqdm(children):
                try:
                    api.delete_node(child.id)
                except RuntimeError:
                    continue
            api.delete_node(dir.id)
        except RuntimeError:
            continue


def delete_h5p(api: EdusharingAPI):
    """
    Delete all H5P nodes on Edu-Sharing.
    @param api: Edu-Sharing API module
    """
    sync = find_node_by_name(api, '-userhome-', 'SYNC_OBJ')
    h5p = find_node_by_name(api, sync.id, 'h5pFiles')

    count = 0
    for node in [node for node in api.get_children(h5p.id) if not node.is_directory]:
        count += 1
        try:
            api.delete_node(node.id)
            print(f'{count} deleted')
        except RuntimeError:
            print(f'{count} error')


def delete_fwu(api: EdusharingAPI):
    """
    Delete all FWU nodes on Edu-Sharing.
    @param api: Edu-Sharing API module
    """
    sync = find_node_by_name(api, '-userhome-', 'SYNC_OBJ')
    fwu = find_node_by_name(api, sync.id, 'FWU')

    count = 0
    for node in [node for node in api.get_children(fwu.id) if not node.is_directory]:
        count += 1
        try:
            api.delete_node(node.id)
            print(f'{count} deleted')
        except RuntimeError:
            print(f'{count} error')


def main():
    environment = Environment(ENV_VARS, ask_for_missing=True)

    api = EdusharingAPI(
        environment['EDU_SHARING_BASE_URL'],
        environment['EDU_SHARING_USERNAME'],
        environment['EDU_SHARING_PASSWORD'])

    delete_sodix(api)


if __name__ == '__main__':
    main()
