import edusharing
import requests.auth
import requests
import os
import converter.env as env

ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


def main():
    # ToDO: Authentification with edusharing.py
    # Authentification
    username = env.get('EDU_SHARING_USERNAME')
    password = env.get('EDU_SHARING_PASSWORD')
    base_url = env.get('EDU_SHARING_BASE_URL')
    headers = {'Accept': 'application/json'}
    session = requests.Session()
    session.auth = requests.auth.HTTPBasicAuth(username, password)

    # get SYNC_OBJ Folder ID
    url_sync_obj = f'{base_url}rest/search/v1/custom/-home-?contentType=FOLDERS&combineMode=AND&property=name&value=SYNC_OBJ&maxItems=100&skipCount=0'
    response_sync_obj = session.request('GET', url_sync_obj, headers=headers)
    sync_obj_nodeId = response_sync_obj.json()['nodes'][0]['ref']['id']

    # create new h5p folder in SYNC_OBJ, if not exist. Otherwise get the nodeId of the folder.
    url_new_folder = f'{base_url}rest/node/v1/nodes/-home-/{sync_obj_nodeId}/children?type=cm%3Afolder&renameIfExists=false'
    payload_new_folder = {"cm:name": ["h5p-elements"], "cm:edu_metadataset": ["mds"], "cm:edu_forcemetadataset": ["true"]}
    response_new_folder = session.request('POST', url_new_folder, headers=headers, json=payload_new_folder)
    if not response_new_folder.status_code == 200:
        url_h5p = f'{base_url}rest/search/v1/custom/-home-?contentType=FOLDERS&combineMode=AND&property=name&value=h5p-elements&maxItems=100&skipCount=0'
        response_h5p = session.request('GET', url_h5p, headers=headers)
        folder_nodeID = response_h5p.json()['nodes'][0]['ref']['id']
    else:
        folder_nodeID = response_new_folder.json()['node']['ref']['id']

    # extract all h5p files from directory and upload to folder 'h5p-elements'. Upload only, if the file doesn't exist.
    for root, dirs, files in os.walk(r'h5p_files'):
        for filename in files:
            # check, if the file exists already
            url_search_file = f'http://localhost/edu-sharing/rest/search/v1/custom/-home-?contentType=FILES&combineMode=AND&property=name&value={filename}&maxItems=10&skipCount=0'
            response_search_file = session.request('GET', url_search_file, headers=headers)
            if response_search_file.json()['pagination']['count'] > 0:
                print(f'File {filename} already exists.')
            else:
                # create basic file
                url_base_file = f'{base_url}rest/node/v1/nodes/-home-/{folder_nodeID}/children/?type=ccm%3Aio&renameIfExists=true&assocType=&versionComment=&'
                payload_base_file = {"cm:name": [filename]}
                response_base_file = session.request('POST', url_base_file, headers=headers, json=payload_base_file)

                # get nodeId of the new created file
                file_nodeId = response_base_file.json()['node']['ref']['id']

                # upload the file content
                files = {
                    'file': (f'{filename}', open(f'h5p_files/{filename}', 'rb'), 'application/zip', {'Expires': '0'})
                }
                upload_url = f'{base_url}rest/node/v1/nodes/-home-/{file_nodeId}/content?versionComment=MAIN_FILE_UPLOAD&mimetype='
                upload_response = session.request('POST', upload_url, files=files, stream=True)

                print(f'Upload complete for: ' + filename)


if __name__ == '__main__':
    main()
