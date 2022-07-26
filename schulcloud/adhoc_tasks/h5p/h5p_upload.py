import os
import uuid
import zipfile
from datetime import datetime
import hashlib
from typing import Optional, BinaryIO, List

import edusharing
import h5p_extract_metadata
import util


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']
H5P_LOCAL_PATH = 'h5p_files'
REPLICATION_SOURCE = 'h5p'
FOLDER_NAME = REPLICATION_SOURCE


def generate_node_properties(
        title: str,
        name: str,
        publisher: str,
        keywords: List[str],
        replication_source_id: Optional[str] = None,
        replication_source_uuid: Optional[str] = None,
        url: str = '',
        relation: Optional[str] = None,
        format: Optional[str] = None,
        aggregation_level: int = 1):
    if not replication_source_id:
        replication_source_id = name
    if not replication_source_uuid:
        replication_source_uuid = str(uuid.uuid4())
    if not relation:
        relation = "{'kind': 'ispartof', 'resource': {'identifier': []}}"
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
        "ccm:replicationsourceid": [hashlib.sha1(replication_source_id.encode()).hexdigest()],
        "ccm:replicationsourcehash": [date],
        "ccm:replicationsourceuuid": [replication_source_uuid],
        "ccm:commonlicense_key": [publisher],
        "ccm:hpi_searchable": ["1"],
        "ccm:hpi_lom_general_aggregationlevel": ["1"],
        "cclom:title": [title],
        "cclom:aggregationlevel": [str(aggregation_level)],
        "cclom:general_language": ["de"],
        "cclom:general_keyword": keywords,
        "ccm:lom_annotation": ["{'description': 'searchable==1', 'entity': 'crawler'}"],
        "ccm:wwwurl": [url],
        "ccm:hpi_lom_relation": [relation],
        "ccm:lom_relation": [relation],
    }
    if format:
        properties["cclom:format"] = ["text/html"]
    return properties


class Uploader:
    def __init__(self):
        self.env = util.Environment(ENV_VARS, ask_for_missing=True)

        self.api = edusharing.EdusharingAPI(
            self.env['EDU_SHARING_BASE_URL'],
            self.env['EDU_SHARING_USERNAME'],
            self.env['EDU_SHARING_PASSWORD'])

        self.permitted_groups = ["Brandenburg-public", "Thuringia-public"]

        sync_obj = self.api.get_sync_obj_folder()
        self.destination_folder = self.api.get_or_create_folder(sync_obj.id, FOLDER_NAME)

    def upload(self, filename: str, metadata: h5p_extract_metadata.Metadata, file: Optional[BinaryIO] = None):
        # get h5p file, add metadata, upload and after all add permissions
        name = os.path.splitext(os.path.basename(filename))[0]
        keywords = ['h5p', metadata.title, metadata.collection, metadata.order] + metadata.keywords

        # ToDo: Add the url of the frontend rendering page
        properties = generate_node_properties(metadata.order, metadata.title, metadata.publisher, keywords, replication_source_id=name)

        node = self.api.sync_node(REPLICATION_SOURCE, properties,
                             ['ccm:replicationsource', 'ccm:replicationsourceid'])

        if node.size is not None:
            print(f'Already exists: {filename}')
            return

        if file is None:
            file = open(filename, 'rb')
        files = {
            'file': (os.path.basename(filename), file, 'application/zip', {'Expires': '0'})
        }
        mimetype = 'application%2Fzip'
        url_upload = f'/node/v1/nodes/-home-/{node.id}' \
                     f'/content?versionComment=MAIN_FILE_UPLOAD&mimetype={mimetype}'
        self.api.make_request('POST', url_upload, files=files, stream=True)
        file.close()

        print(f'Upload complete for: {filename}')
        return node.id, properties["ccm:replicationsourceuuid"]

    def main(self):

        # ToDo:
        #  1. Check the metadata especially name, title and keywords (for the search query in the frontend)
        #  > Actual the sorting seems to sort to the value "score" of the property "collection". Check that!
        #  2. Test the script against edusharing.staging and check the Lern-Store frontend view for the collection.
        #  3. Combine down and upload in one script

        # unzip data
        for obj in os.listdir(H5P_LOCAL_PATH):
            if not os.path.isfile(obj) or not obj.endswith('.zip'):
                continue

            zip = zipfile.ZipFile(obj)

            # get excel_sheet data
            for excel_filename in zip.namelist():
                if excel_filename.endswith(".xlsx"):
                    excel_file = zip.open(excel_filename)
                    metadata_file = h5p_extract_metadata.MetadataFile(excel_file)
                    break
            else:
                raise RuntimeError('Could not find excel file with metadata')

            # save the replicationsourceuuid, nodeId and the collection of each h5p-file corresponding to this package
            package_h5p_files = []
            package_h5p_files_nodeId = []
            collection = ''

            # loop through the unzipped h5p-files
            for root, dirs, files in os.walk("unzipped"):
                for filename in files:
                    if filename.endswith(".h5p"):
                        metadata = metadata_file.get_metadata(filename)
                        if collection and not metadata.collection == collection:
                            raise RuntimeError('Collection suddenly changed')
                        collection = metadata.collection
                        # TODO: multiple collections in one excel file / one call?

                        node_id, rep_source_uuid = self.upload(os.path.join(root, filename), metadata)
                        package_h5p_files_nodeId.append(node_id)
                        package_h5p_files.append(rep_source_uuid)

            excel_file.close()
            zip.close()

            # set permissions for the package
            self.api.set_permissions(self.destination_folder.id, self.permitted_groups, False)
            print("Set permissions for: " + str(self.permitted_groups))

            # now update metadata from the new node (add children) and the h5p-files (add parent)

            name = collection
            # name = os.path.splitext(filename)[0]
            relation = "{'kind': 'hasparts', 'resource': {'identifier': " + str(package_h5p_files) + "}}"
            keywords = ["h5p", name, "Arbeitspaket"]
            properties = generate_node_properties(
                name, name, "MedienLB", keywords, relation=relation, format="text/html", aggregation_level=2
            )

            self.api.sync_node(REPLICATION_SOURCE, properties, ['ccm:replicationsource', 'ccm:replicationsourceid'])
            print(f'Created Collection {name}.')

            # update the h5p-files with parent-nodeId
            parent_uuid = properties["ccm:replicationsourceuuid"]

            for node in package_h5p_files_nodeId:
                # TODO: check whether those calls are really necessary
                # TODO: if they are necessary, use urllib.parse.urlencode to do the url encoding
                url_update_lom = f'/node/v1/nodes/-home-/{node}/property?property=ccm%3Alom_relation&value=%7B\'kind\'%3A%20\'ispartof\'%2C%20\'resource\'%3A%20%7B\'identifier\'%3A%20{parent_uuid}%7D'
                url_update_lom_hpi = f'/node/v1/nodes/-home-/{node}/property?property=ccm%3Ahpi_lom_relation&value=%7B\'kind\'%3A%20\'ispartof\'%2C%20\'resource\'%3A%20%7B\'identifier\'%3A%20{parent_uuid}%7D'
                response_update = self.api.make_request('POST', url_update_lom)
                self.api.make_request('POST', url_update_lom_hpi)
                print(f'Response status {response_update.status_code} for node: {node}')


if __name__ == '__main__':
    Uploader().main()
