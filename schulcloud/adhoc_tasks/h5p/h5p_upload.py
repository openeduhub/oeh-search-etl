import edusharing
import util
import os
from datetime import datetime

ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


def main():
    environment = util.Environment(ENV_VARS, ask_for_missing=True)

    api = edusharing.EdusharingAPI(
        environment['EDU_SHARING_BASE_URL'],
        environment['EDU_SHARING_USERNAME'],
        environment['EDU_SHARING_PASSWORD'])

    # groups with permission
    groups = ["Brandenburg-public", "Thuringia-public"]

    # get SYNC_OBJ Folder ID
    url_sync_obj = f'/search/v1/custom/-home-?contentType=FOLDERS&combineMode=AND&' \
                   f'property=name&value=SYNC_OBJ&maxItems=100&skipCount=0'
    response_sync_obj = api.make_request('GET', url_sync_obj)
    sync_obj_node_id = response_sync_obj.json()['nodes'][0]['ref']['id']

    # create new h5p folder in SYNC_OBJ, if not exist. Otherwise, get the nodeId of the folder.
    url_new_folder = f'/node/v1/nodes/-home-/{sync_obj_node_id}/children?type=cm%3Afolder&renameIfExists=false'
    payload_new_folder = {
        "cm:name": ["h5p-elements"],
        "cm:edu_metadataset": ["mds"],
        "cm:edu_forcemetadataset": ["true"]
    }
    response_new_folder = api.make_request('POST', url_new_folder, json_data=payload_new_folder)

    if not response_new_folder.status_code == 200:
        url_h5p = f'/search/v1/custom/-home-?contentType=FOLDERS&combineMode=' \
                  f'AND&property=name&value=h5p-elements&maxItems=10&skipCount=0'
        response_h5p = api.make_request('GET', url_h5p)
        folder_node_id = response_h5p.json()['nodes'][0]['ref']['id']
    else:
        folder_node_id = response_new_folder.json()['node']['ref']['id']

    # extract all h5p files from directory and upload to folder 'h5p-elements'. Upload only, if the file doesn't exist.
    for root, dirs, files in os.walk(r'h5p_files'):
        for filename in files:
            # check, if the file already exists
            url_search_file = f'/search/v1/custom/-home-?contentType=FILES&combineMode=AND' \
                              f'&property=name&value={filename}&maxItems=10&skipCount=0'
            response_search_file = api.make_request('GET', url_search_file)

            if response_search_file.json()['pagination']['count'] > 0:
                print(f'File {filename} already exists.')
            else:
                # create basic file
                url_base_file = f'/node/v1/nodes/-home-/{folder_node_id}/children/?type=ccm%3Aio&renameIfExists=true' \
                                f'&assocType=&versionComment=&'
                payload_base_file = {"cm:name": [filename]}
                response_base_file = api.make_request('POST', url_base_file, json_data=payload_base_file)

                # get nodeId of the new created file
                file_node_id = response_base_file.json()['node']['ref']['id']

                # upload the file content
                files = {
                    'file': (f'{filename}', open(f'h5p_files/{filename}', 'rb'), 'application/zip', {'Expires': '0'})
                }
                url_upload = f'/node/v1/nodes/-home-/{file_node_id}/content?versionComment=MAIN_FILE_UPLOAD&mimetype='
                api.make_request('POST', url_upload, files=files, stream=True)

                # set "cm:edu_metadataset" to "default", because otherwise edusharing crashes
                # with 'can't read metadataset' error
                # ToDo: First, it prevents for crashing edusharing,
                #  but perhaps we need to set it to 'mds_oeh' for adding more Metadata
                index = filename.rfind(".")
                name = filename[:index]
                date = str(datetime.now())

                url_change_value = f'/node/v1/nodes/-home-/{file_node_id}/metadata?versionComment=update_metadata'
                payload_change_value = {"cm:edu_metadataset": ["default"],
                                        "ccm:replicationsourcehash": [date],
                                        "cclom:general_keyword": ["h5p", name]
                                        }
                api.make_request('POST', url_change_value, json_data=payload_change_value)

                print(f'Upload complete for: ' + filename)

    # permissions
    modify_permissions(folder_nodeID, groups, base_url, session, headers)


def modify_permissions(node_id, groups: List[str], base_url, session, headers):
    set_permissions(node_id, groups, base_url,  session, headers)
    print("Set permissions for: " + str(groups))


def set_permissions(node_id, groups: List[str], base_url,  session, headers):
    # data = json.loads(data)
    url = f'{base_url}/rest/node/v1/nodes/-home-/{node_id}/permissions?sendMail=false&sendCopy=false'
    data_json = craft_permission_body(groups)
    session.request('POST', url, json=data_json, headers=headers)


def craft_permission_body(groups: List[str]):
    permissions = []
    for group in groups:
        permission = {
            'editable': True,
            'authority': {
                'authorityName': f'GROUP_{group}',
                'authorityType': 'GROUP'
            },
            'group': {
                'displayName': group
            },
            'permissions': ['Consumer']
        }

        permissions.append(permission)

    return {
        'inherited': 'false',
        'permissions': permissions
    }


if __name__ == '__main__':
    main()
