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
    #  > Actual the sorting seems to sort to the value "score" of the property "collection". Check that!
    #  2. Test the script against edusharing.staging and check the Lern-Store frontend view for the collection.

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
                .unzip_local_file(file_path=f'{H5P_LOCAL_PATH}/{filename}', unzipped_dir="unzipped")

            # get excel_sheet data
            excel_sheet = ""
            for filename in os.listdir("unzipped"):
                if filename.endswith(".xlsx"):
                    excel_sheet = filename

            # save the replicationsourceuuid, nodeId and the collection of each h5p-file corresponding to this package
            package_h5p_files = []
            package_h5p_files_nodeId = []
            collection_h5p_files = ""

            # loop through the unzipped h5p-files
            for root, dirs, files in os.walk("unzipped"):
                for filename in files:
                    # get h5p file, add metadata, upload and after all add permissions
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
                            "cm:name": [metadata_excel["title"]],
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
                            "cclom:title": [metadata_excel["order"]],
                            "cclom:aggregationlevel": ["1"],
                            "cclom:general_language": ["de"],
                            "cclom:general_keyword": ["h5p", metadata_excel["keywords"], metadata_excel["order"],
                                                      metadata_excel["collection"], metadata_excel["title"]],
                            "ccm:lom_annotation": ["{'description': 'searchable==1', 'entity': 'crawler'}"],
                            "ccm:wwwurl": [""],  # ToDo: Add the url of the frontend rendering page.
                            "ccm:hpi_lom_relation": ["{'kind': 'ispartof', 'resource': {'identifier': []}}"],
                            "ccm:lom_relation": ["{'kind': 'ispartof', 'resource': {'identifier': []}}"],
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

                        # add uuid, nodeId and collection name of the file to the package array
                        package_h5p_files.append(properties["ccm:replicationsourceuuid"])
                        package_h5p_files_nodeId.append(node.id)
                        collection_h5p_files = metadata_excel["collection"]

                        print(f'Upload complete for: {filename}')

            # delete the unzipped folder including all files
            h5p_extract_metadata.UnzipLocalFile.delete_local_folder(folder_name="unzipped")
            print(package_h5p_files)

            # set permissions for the package
            api.set_permissions(destination_folder.id, permitted_groups, False)
            print("Set permissions for: " + str(permitted_groups))

            # now update metadata from the new node (add children) and the h5p-files (add parent)
            name = collection_h5p_files
            # name = os.path.splitext(filename)[0]
            date = str(datetime.now())
            relation = "{'kind': 'hasparts', 'resource': {'identifier': " + str(package_h5p_files) + "}}"

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
                "ccm:commonlicense_key": ["MedienLB"],
                "ccm:hpi_searchable": ["1"],
                "ccm:hpi_lom_general_aggregationlevel": ["2"],
                "cclom:title": [name],
                "cclom:aggregationlevel": ["2"],
                "cclom:general_language": ["de"],
                "cclom:general_keyword": ["h5p", name, "Arbeitspaket"],
                "ccm:lom_annotation": ["{'description': 'searchable==1', 'entity': 'crawler'}"],
                "ccm:wwwurl": [""],
                "ccm:hpi_lom_relation": [relation],
                "ccm:lom_relation": [relation],
                "cclom:format": ["text/html"]
            }

            api.sync_node(REPLICATION_SOURCE, properties, ['ccm:replicationsource', 'ccm:replicationsourceid'])
            print(f'Created Collection {name}.')

            # update the h5p-files with parent-nodeId
            parent_uuid = properties["ccm:replicationsourceuuid"]

            for node in package_h5p_files_nodeId:
                url_update_lom = f'/node/v1/nodes/-home-/{node}/property?property=ccm%3Alom_relation&value=%7B\'kind\'%3A%20\'ispartof\'%2C%20\'resource\'%3A%20%7B\'identifier\'%3A%20{parent_uuid}%7D'
                url_update_lom_hpi = f'/node/v1/nodes/-home-/{node}/property?property=ccm%3Ahpi_lom_relation&value=%7B\'kind\'%3A%20\'ispartof\'%2C%20\'resource\'%3A%20%7B\'identifier\'%3A%20{parent_uuid}%7D'
                response_update = api.make_request('POST', url_update_lom)
                api.make_request('POST', url_update_lom_hpi)
                print(f'Response status {response_update.status_code} for node: {node}')


if __name__ == '__main__':
    main()
