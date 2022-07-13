
import edusharing
import util
import os
from datetime import datetime

ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']


def main():
    environment = util.Environment(ENV_VARS, ask_for_missing=True)
    h5p_path = 'h5p_files'

    api = edusharing.EdusharingAPI(
        environment['EDU_SHARING_BASE_URL'],
        environment['EDU_SHARING_USERNAME'],
        environment['EDU_SHARING_PASSWORD'])

    permitted_groups = ["Brandenburg-public", "Thuringia-public"]

    sync_obj = api.get_sync_obj_folder()
    new_folder = api.create_or_get_folder(sync_obj.id, 'h5p-elements')

    # extract all h5p files from directory and upload to folder 'h5p-elements'. Upload only, if the file doesn't exist.
    for root, dirs, files in os.walk(h5p_path):
        for filename in files:
            if api.file_exists(filename):
                print(f'File {filename} already exists.')
            else:
                new_node = api.create_node(new_folder.id, filename)
                file = open(os.path.join(root, filename), 'rb')

                files = {
                    'file': (filename, file, 'application/zip', {'Expires': '0'})
                }
                url_upload = f'/node/v1/nodes/-home-/{new_node.id}/content?versionComment=MAIN_FILE_UPLOAD&mimetype='
                api.make_request('POST', url_upload, files=files, stream=True)

                file.close()

                # set "cm:edu_metadataset" to "default", because otherwise edusharing crashes
                # with 'can't read metadataset' error
                # ToDo: First, it prevents for crashing edusharing,
                #  but perhaps we need to set it to 'mds_oeh' for adding more Metadata
                index = filename.rfind(".")
                name = filename[:index]
                date = str(datetime.now())

                url_change_value = f'/node/v1/nodes/-home-/{new_node.id}/metadata?versionComment=update_metadata'
                payload_change_value = {"cm:edu_metadataset": ["mds_oeh"],
                                        "cm:edu_forcemetadataset": ["true"],
                                        "ccm:replicationsourcehash": [date],
                                        "cclom:general_keyword": ["h5p", name]
                                        }
                api.make_request('POST', url_change_value, json_data=payload_change_value)

                print(f'Upload complete for: ' + filename)

    api.set_permissions(new_folder.id, permitted_groups, False)
    print("Set permissions for: " + str(permitted_groups))


if __name__ == '__main__':
    main()
