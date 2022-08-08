import os
import uuid
import zipfile
from datetime import datetime
import hashlib
from typing import Optional, List, IO

import edusharing
import h5p_extract_metadata
import util


ENV_VARS = ['EDU_SHARING_BASE_URL', 'EDU_SHARING_USERNAME', 'EDU_SHARING_PASSWORD']
H5P_LOCAL_PATH = 'h5p_files'
FOLDER_NAME_GENERAL = 'h5p'
FOLDER_NAME_THURINGIA = 'h5p-thuringia'


def generate_node_properties(
        title: str,
        name: str,
        publisher: str,
        keywords: List[str],
        folder_name: str,
        replication_source_id: Optional[str] = None,
        replication_source_uuid: Optional[str] = None,
        url: str = '',
        relation: Optional[str] = None,
        format: Optional[str] = None,
        aggregation_level: int = 1,
        aggregation_level_hpi: int = 1):
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
        "ccm:replicationsource": [folder_name],
        "ccm:replicationsourceid": [hashlib.sha1(replication_source_id.encode()).hexdigest()],
        "ccm:replicationsourcehash": [date],
        "ccm:replicationsourceuuid": [replication_source_uuid],
        "ccm:commonlicense_key": [publisher],
        "ccm:hpi_searchable": ["1"],
        "ccm:hpi_lom_general_aggregationlevel": [str(aggregation_level_hpi)],
        "cclom:title": [title],
        "cclom:aggregationlevel": [str(aggregation_level)],
        "cclom:general_language": ["de"],
        "cclom:general_keyword": keywords,
        "ccm:lom_annotation": ["{'description': 'searchable==1', 'entity': 'crawler'}"],
        "ccm:wwwurl": [url],
        "ccm:hpi_lom_relation": [relation],
        "ccm:lom_relation": [relation],
        "ccm:create_version": ["false"],
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

    def setup_destination_folder(self, folder_name: str, permitted_groups: Optional[List[str]]):
        if not permitted_groups:
            permitted_groups = ["Brandenburg-public", "Thuringia-public", "LowerSaxony-public"]

        sync_obj = self.api.get_sync_obj_folder()
        destination_folder = self.api.get_or_create_folder(sync_obj.id, folder_name)

        # set permissions for the permitted_groups
        self.api.set_permissions(destination_folder.id, permitted_groups, False)
        print(f"Created folder {folder_name} with permissions for: {permitted_groups}")

        return destination_folder

    def upload_h5p_file(self, folder_name: str, filename: str, metadata: h5p_extract_metadata.Metadata,
                        file: Optional[IO[bytes]] = None, relation: str = "", overwrite_contents: bool = False):
        # get h5p file, add metadata, upload and after all add permissions
        name = os.path.splitext(os.path.basename(filename))[0]
        keywords = ['h5p', metadata.title, metadata.collection, metadata.order, metadata.keywords]

        # ToDo: Add the url of the frontend rendering page
        properties = generate_node_properties(metadata.order, metadata.title, metadata.publisher, keywords,
                                              folder_name, replication_source_id=name, relation=relation)

        node = self.api.sync_node(folder_name, properties, ['ccm:replicationsource', 'ccm:replicationsourceid'])

        if node.size is not None and not overwrite_contents:
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

    def upload_h5p_single(self, h5p_path: str, edusharing_folder_name: str):
        # TODO: read metadata from file
        metadata = h5p_extract_metadata.Metadata('title', 'publisher', [], '', '')
        self.upload_h5p_file(edusharing_folder_name, h5p_path, metadata)

    def upload_h5p_thr_collection(self, zip_path: str, edusharing_folder_name: str):
        """
            Upload multiple H5P files within a zip archive, as a collection
        """
        zip = zipfile.ZipFile(zip_path)
        # get excel_sheet data
        for excel_filename in zip.namelist():
            if excel_filename.endswith(".xlsx"):
                excel_file = zip.open(excel_filename)
                metadata_file = h5p_extract_metadata.MetadataFile(excel_file)
                break
        else:
            raise RuntimeError('Could not find excel file with metadata')

        # save the replicationsourceuuid, nodeId and the collection of each h5p-file corresponding to this package
        package_h5p_files_rep_source_uuids = []
        collection_name = metadata_file.get_collection()

        # now update metadata from the new node (add children) and the h5p-files (add parent)
        # TODO: add keywords of elements to collection
        keywords = ["h5p", collection_name, "Arbeitspaket"]
        properties = generate_node_properties(
            collection_name, collection_name, "MedienLB", keywords, edusharing_folder_name,
            format="text/html", aggregation_level=2, aggregation_level_hpi=2
        )
        collection_rep_source_uuid = properties['ccm:replicationsourceuuid']
        collection_node = self.api.sync_node(edusharing_folder_name, properties,
                                             ['ccm:replicationsource', 'ccm:replicationsourceid'])
        print(f'Created Collection {collection_name}.')

        # loop through the unzipped h5p-files
        for filename in zip.namelist():
            if filename.endswith(".h5p"):
                metadata = metadata_file.get_metadata(filename)
                file = zip.open(filename)

                relation = f"{{'kind': 'ispartof', 'resource': {{'identifier': {collection_rep_source_uuid}}}}}"

                node_id, rep_source_uuid = self.upload_h5p_file(edusharing_folder_name, filename, metadata,
                                                                file=file, relation=relation)
                rep_source_uuid_clean = str(rep_source_uuid).replace('[', '').replace(']', '').replace("'", "")
                package_h5p_files_rep_source_uuids.append(rep_source_uuid_clean)

        excel_file.close()
        zip.close()

        print(package_h5p_files_rep_source_uuids)
        self.api.set_property_relation(collection_node.id, 'ccm:lom_relation', package_h5p_files_rep_source_uuids)
        self.api.set_property_relation(collection_node.id, 'ccm:hpi_lom_relation', package_h5p_files_rep_source_uuids)

    def upload_from_folder(self):
        self.setup_destination_folder(FOLDER_NAME_GENERAL, ['Thuringia-public', 'Brandenburg-public', 'LowerSaxony-public'])
        self.setup_destination_folder(FOLDER_NAME_THURINGIA, ['Thuringia-public'])

        # ToDo:
        #  1. Check the metadata especially name, title and keywords (for the search query in the frontend)
        #  > Actual the sorting seems to sort to the value "score" of the property "collection". Check that!
        #  2. Test the script against edusharing.staging and check the Lern-Store frontend view for the collection.
        #  3. Combine down and upload in one script

        for obj in os.listdir(H5P_LOCAL_PATH):
            path = os.path.join(H5P_LOCAL_PATH + "/" + obj)
            if os.path.isfile(path):
                if obj.endswith('.h5p'):
                    #self.upload_h5p_single(path, FOLDER_NAME_GENERAL)
                    pass
                elif obj.endswith('.zip'):
                    self.upload_h5p_thr_collection(path, FOLDER_NAME_THURINGIA)


if __name__ == '__main__':
    Uploader().upload_from_folder()
