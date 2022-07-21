
import os
import uuid
from datetime import datetime
import hashlib
import json
import edusharing
import h5p_extract_metadata
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

            if os.path.exists('unzipped'):
                h5p_extract_metadata.UnzipLocalFile.delete_local_folder(folder_name="unzipped")
                h5p_extract_metadata.UnzipLocalFile.create_local_folder(folder_name='unzipped')
            else:
                h5p_extract_metadata.UnzipLocalFile.create_local_folder(folder_name='unzipped')

            h5p_extract_metadata.UnzipLocalFile.unzip_local_file(file_path=f"h5p_files/{filename}", unzipped_dir="unzipped")
            metadata = json.loads(h5p_extract_metadata.UnzipLocalFile.read_file(file_path="unzipped/h5p.json"))
            metadata_h5p = h5p_extract_metadata.UnzipLocalFile.extract_metadata_from_json(metadata=metadata)

            # ToDo: Add the value of "ccm:wwwurl". For example the url of the iframe-rendering-page.
            #  It refers to the button "Zum Lerninhalt" in the lern-store frontend view.
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
                "ccm:commonlicense_key": [metadata_h5p["copyright_license"]],
                "ccm:hpi_searchable": ["1"],
                "ccm:hpi_lom_general_aggregationlevel": ["1"],
                "ccm:hpi_lom_relation": ["{}"],
                "cclom:title": [metadata_h5p["title"]],
                "cclom:aggregationlevel": ["1"],
                "cclom:general_language": ["de"],
                "cclom:general_keyword": ["h5p", name],
                "ccm:lom_annotation": ["{'description': 'searchable==1', 'entity': 'crawler'}"],
                "ccm:wwwurl": [""],  # ToDo: see above
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
            h5p_extract_metadata.UnzipLocalFile.delete_local_folder(folder_name="unzipped")
            print(f'Upload complete for: {filename}')

    api.set_permissions(destination_folder.id, permitted_groups, False)
    print("Set permissions for: " + str(permitted_groups))


if __name__ == '__main__':
    main()
