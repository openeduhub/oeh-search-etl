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

    # create new h5p folder in SYNC_OBJ
    url_new_folder = f'{base_url}rest/node/v1/nodes/-home-/{sync_obj_nodeId}/children?type=cm%3Afolder&renameIfExists=false'
    payload_new_folder = {"cm:name": ["h5p-elements"], "cm:edu_metadataset": ["mds"], "cm:edu_forcemetadataset": ["true"]}
    response_new_folder = session.request('POST', url_new_folder, headers=headers, json=payload_new_folder)
    new_folder_nodeID = response_new_folder.json()['node']['ref']['id']

    # extract all h5p files from directory and upload to new created folder 'h5p-elements'
    for root, dirs, files in os.walk(r'h5p_files'):
        for filename in files:
            url_base_file = f'{base_url}rest/node/v1/nodes/-home-/{new_folder_nodeID}/children/?type=ccm%3Aio&renameIfExists=true&assocType=&versionComment=&'
            payload_base_file = {"cm:name": [filename]}
            response_base_file = session.request('POST', url_base_file, headers=headers, json=payload_base_file)
            file_nodeId = response_base_file.json()['node']['ref']['id']
            files = {
                'file': (f'{filename}', open(f'h5p_files/{filename}', 'rb'), 'application/zip', {'Expires': '0'})
            }
            upload_url = f'{base_url}rest/node/v1/nodes/-home-/{file_nodeId}/content?versionComment=MAIN_FILE_UPLOAD&mimetype='
            upload_response = session.request('POST', upload_url, files=files, stream=True)

            print(f'Upload complete for: ' + filename)


if __name__ == '__main__':
    main()
