
import os
import uuid
from datetime import datetime
import hashlib

import edusharing
import util


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']
H5P_LOCAL_PATH = 'h5p_files'
REPLICATION_SOURCE = 'h5p'
FOLDER_NAME = REPLICATION_SOURCE


def main():

    environment = util.Environment(ENV_VARS, ask_for_missing=True)

    api = edusharing.EdusharingAPI(
        environment['EDU_SHARING_BASE_URL'],
        environment['EDU_SHARING_USERNAME'],
        environment['EDU_SHARING_PASSWORD'])

    permitted_groups = ["Brandenburg-public", "Thuringia-public", "LowerSaxony-public"]

    sync_obj = api.get_sync_obj_folder()
    destination_folder = api.get_or_create_folder(sync_obj.id, FOLDER_NAME)

    for root, dirs, files in os.walk(H5P_LOCAL_PATH):
        for filename in files:
            name = os.path.splitext(filename)[0]
            date = str(datetime.now())
            properties = {
                "access": [
                    "Read",
                    "ReadAll",
                    "Comment",
                    "Feedback",
                    "AddChildren",
                    "ChangePermissions",
                    "Write",
                    "Delete",
                    "CCPublish"
                ],
                "cm:name": [name],
                "cm:edu_metadataset": ["mds_oeh"],
                "cm:edu_forcemetadataset": ["true"],
                "ccm:ph_invited": ["GROUP_public"],
                "ccm:ph_action": ["PERMISSION_ADD"],
                "ccm:objecttype": ["MATERIAL"],
                "ccm:replicationsource": [REPLICATION_SOURCE],
                "ccm:replicationsourceid": [hashlib.sha1(name.encode()).hexdigest()],
                "ccm:replicationsourcehash": [date],
                "ccm:replicationsourceuuid": [str(uuid.uuid4())],
                "ccm:commonlicense_key": ["CUSTOM"],
                "ccm:hpi_searchable": ["1"],
                "ccm:hpi_lom_general_aggregationlevel": ["1"],
                "ccm:hpi_lom_relation": ["{}"],
                "cclom:title": [name],
                "cclom:aggregationlevel": ["1"],
                "cclom:general_language": ["de"],
                "cclom:general_keyword": ["h5p", name],
                "ccm:lom_annotation": ["{'description': 'searchable==1', 'entity': 'crawler'}"],
            }
            node = api.sync_node(REPLICATION_SOURCE, properties, ['ccm:replicationsource', 'ccm:replicationsourceid'])

            if node.size is not None:
                print(f'Already exists: {filename}')
                continue

            file = open(os.path.join(root, filename), 'rb')
            files = {
                'file': (filename, file, 'application/zip', {'Expires': '0'})
            }
            mimetype = 'application%2Fzip'
            url_upload = f'/node/v1/nodes/-home-/{node.id}/content?versionComment=MAIN_FILE_UPLOAD&mimetype={mimetype}'
            api.make_request('POST', url_upload, files=files, stream=True)
            file.close()
            print(f'Upload complete for: {filename}')

    api.set_permissions(destination_folder.id, permitted_groups, False)
    print("Set permissions for: " + str(permitted_groups))


if __name__ == '__main__':
    main()
