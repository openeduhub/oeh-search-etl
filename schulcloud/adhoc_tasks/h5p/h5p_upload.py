import os
import uuid
from datetime import datetime
import hashlib
import edusharing
import h5p_extract_metadata
import util


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']
H5P_LOCAL_PATH = 'h5p_files'
REPLICATION_SOURCE = 'h5p'
FOLDER_NAME = REPLICATION_SOURCE


def main():

    # ToDo:
    #  1. Check the metadata especially name, title and keywords (for the search query in the frontend)
    #  > Actual the sorting after searching is bad.
    #  2. Create node "collection" (not a Edusharing collection!, but rather with the metadata: "ccm:lom_relation")
    #  3. Add h5p-files to "collection" (not a Edusharing collection!, more with the metadata: "ccm:lom_relation")
    #  > Therefor the mediothek_pixiothek_spider does the same. Check and adapt that!

    environment = util.Environment(ENV_VARS, ask_for_missing=True)

    api = edusharing.EdusharingAPI(
        environment['EDU_SHARING_BASE_URL'],
        environment['EDU_SHARING_USERNAME'],
        environment['EDU_SHARING_PASSWORD'])

    permitted_groups = ["Brandenburg-public", "Thuringia-public"]

    sync_obj = api.get_sync_obj_folder()
    destination_folder = api.get_or_create_folder(sync_obj.id, FOLDER_NAME)

    # unzip data
    for root, dirs, files in os.walk(H5P_LOCAL_PATH):
        for filename in files:
            # create dir to unzip the files temporarily
            if os.path.exists('unzipped'):
                h5p_extract_metadata.UnzipLocalFile.delete_local_folder(folder_name="unzipped")
                h5p_extract_metadata.UnzipLocalFile.create_local_folder(folder_name='unzipped')
            else:
                h5p_extract_metadata.UnzipLocalFile.create_local_folder(folder_name='unzipped')

            # unzip the package
            h5p_extract_metadata.UnzipLocalFile\
                .unzip_local_file(file_path=f'{H5P_LOCAL_PATH}{filename}', unzipped_dir="unzipped")

            # get excel_sheet
            excel_sheet = ""
            for filename in os.listdir("unzipped"):
                if filename.endswith(".xlsx"):
                    excel_sheet = filename

            # save the replicationsourceuuid of each h5p-file corresponding to this package
            package_h5p_files = []

            # loop through the unzipped h5p-files
            for root, dirs, files in os.walk("unzipped"):
                for filename in files:
                    # get h5p file, add metadata, upload and add permissions
                    if filename.endswith(".h5p"):
                        name = os.path.splitext(filename)[0]
                        date = str(datetime.now())
                        metadata_excel = h5p_extract_metadata.UnzipLocalFile \
                            .extract_metadata_from_excel(excel_file_path=f'unzipped/{excel_sheet}', file_name=filename)

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
                            "cm:name": [metadata_excel["order"]],
                            "cm:edu_metadataset": ["mds_oeh"],
                            "cm:edu_forcemetadataset": ["true"],
                            "ccm:ph_invited": ["GROUP_public"],
                            "ccm:ph_action": ["PERMISSION_ADD"],
                            "ccm:objecttype": ["MATERIAL"],
                            "ccm:replicationsource": [REPLICATION_SOURCE],
                            "ccm:replicationsourceid": [hashlib.sha1(name.encode()).hexdigest()],
                            "ccm:replicationsourcehash": [date],
                            "ccm:replicationsourceuuid": [str(uuid.uuid4())],
                            "ccm:commonlicense_key": [metadata_excel["publisher"]],
                            "ccm:hpi_searchable": ["1"],
                            "ccm:hpi_lom_general_aggregationlevel": ["1"],
                            "cclom:title": [metadata_excel["title"]],
                            "cclom:aggregationlevel": ["1"],
                            "cclom:general_language": ["de"],
                            "cclom:general_keyword": ["h5p", name, metadata_excel["keywords"], metadata_excel["order"],
                                                      metadata_excel["collection"]],
                            "ccm:lom_annotation": ["{'description': 'searchable==1', 'entity': 'crawler'}"],
                            "ccm:wwwurl": [""]  # ToDo: Add the url of the frontend rendering page.
                        }
                        node = api.sync_node(REPLICATION_SOURCE, properties,
                                             ['ccm:replicationsource', 'ccm:replicationsourceid'])

                        if node.size is not None:
                            print(f'Already exists: {filename}')
                            continue

                        file = open(os.path.join(root, filename), 'rb')
                        files = {
                            'file': (filename, file, 'application/zip', {'Expires': '0'})
                        }
                        mimetype = 'application%2Fzip'
                        url_upload = f'/node/v1/nodes/-home-/{node.id}' \
                                     f'/content?versionComment=MAIN_FILE_UPLOAD&mimetype={mimetype}'
                        api.make_request('POST', url_upload, files=files, stream=True)
                        file.close()

                        # add uuid of the file to the package array
                        package_h5p_files.append(properties["ccm:replicationsourceuuid"])

                        print(f'Upload complete for: {filename}')

            # delete the unzipped folder including the files
            h5p_extract_metadata.UnzipLocalFile.delete_local_folder(folder_name="unzipped")
            print(package_h5p_files)

            # set permissions
            api.set_permissions(destination_folder.id, permitted_groups, False)
            print("Set permissions for: " + str(permitted_groups))

            # set package with relations (all relations with the "ccm:replicationsourceuuid")
            # collection_name = metadata_excel["collection"]
            # print(f"Created package with corresponding h5p-elements: {package_h5p_files}")
            # properties = {
            #     "access": [
            #         "Read",
            #         "ReadAll",
            #         "Comment",
            #         "Feedback",
            #         "AddChildren",
            #         "ChangePermissions",
            #         "Write",
            #         "Delete",
            #         "CCPublish"
            #     ],
            #     "cm:name": [name],
            #     "cm:edu_metadataset": ["mds_oeh"],
            #     "cm:edu_forcemetadataset": ["true"],
            #     "ccm:ph_invited": ["GROUP_public"],
            #     "ccm:ph_action": ["PERMISSION_ADD"],
            #     "ccm:objecttype": ["MATERIAL"],
            #     "ccm:replicationsource": [REPLICATION_SOURCE],
            #     "ccm:replicationsourceid": [hashlib.sha1(name.encode()).hexdigest()],
            #     "ccm:replicationsourcehash": [date],
            #     "ccm:replicationsourceuuid": [str(uuid.uuid4())],
            #     "ccm:commonlicense_key": [metadata_excel["publisher"]],
            #     "ccm:hpi_searchable": ["1"],
            #     "ccm:hpi_lom_general_aggregationlevel": ["2"],
            #     "cclom:title": [collection_name],
            #     "cclom:aggregationlevel": ["2"],
            #     "cclom:general_language": ["de"],
            #     "cclom:general_keyword": ["h5p", name],
            #     "ccm:lom_annotation": ["{'description': 'searchable==1', 'entity': 'crawler'}"],
            #     "ccm:wwwurl": [""],  # ToDo: see above
            #     "ccm:lom_relation": [
            #         "{'kind': 'haspart', 'resource': {'identifier': ['dba622f1-ccee-5c3b-b446-94968c117f52',
            #         'e1956eb8-cbc3-5098-953d-f96e813bb819', '453f1156-b84d-53c2-bb1c-210da37b0f4c',
            #         'c920eba4-f4d8-53cb-bb89-37aa7908fb27', '41cd8508-3f8a-5c87-b846-12192dab3b3d',
            #         '0258b36e-2ec7-52db-96fd-ad1fc1b9da5f', 'ad6d9c78-636d-522c-8302-9d488a79dcac',
            #         '14be28c3-a49b-5872-b275-9d25794d4b52']}}"
            #     ],
            #     "ccm:hpi_lom_relation": [
            #         "{'kind': 'haspart', 'resource': {'identifier': ['dba622f1-ccee-5c3b-b446-94968c117f52',
            #         'e1956eb8-cbc3-5098-953d-f96e813bb819', '453f1156-b84d-53c2-bb1c-210da37b0f4c',
            #         'c920eba4-f4d8-53cb-bb89-37aa7908fb27', '41cd8508-3f8a-5c87-b846-12192dab3b3d',
            #         '0258b36e-2ec7-52db-96fd-ad1fc1b9da5f', 'ad6d9c78-636d-522c-8302-9d488a79dcac',
            #         '14be28c3-a49b-5872-b275-9d25794d4b52']}}"
            #     ],
            #     "cclom:format": ["text/html"],
            # }
            #
            # api.sync_node(REPLICATION_SOURCE, properties, ['ccm:replicationsource', 'ccm:replicationsourceid'])


if __name__ == '__main__':
    main()
