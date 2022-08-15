import os
import uuid
import zipfile
from datetime import datetime
import hashlib
from typing import Optional, List, IO, Callable, Dict

import boto3

import edusharing
import h5p_extract_metadata
import util


EXPECTED_ENV_VARS = [
    'EDU_SHARING_BASE_URL',
    'EDU_SHARING_USERNAME',
    'EDU_SHARING_PASSWORD',
    'S3_ENDPOINT_URL',
    'S3_ACCESS_KEY',
    'S3_SECRET_KEY',
    'S3_BUCKET_NAME'
]
H5P_TEMP_FOLDER = 'h5p_temp'
H5P_LOCAL_PATH = 'h5p_files'  # TODO: remove, was only for testing
ES_FOLDER_NAME_GENERAL = 'h5p'
ES_FOLDER_NAME_THURINGIA = 'h5p-thuringia'


def generate_node_properties(
        title: str,
        name: str,
        publisher: str,
        license: str,
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
    if license == "":
        license = "CUSTOM"
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
        "ccm:commonlicense_key": [license],
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
        "ccm:lifecyclecontributer_publisherVCARD_ORG": [publisher]
    }
    if format:
        properties["cclom:format"] = ["text/html"]
    return properties


class Uploader:
    def __init__(self):
        self.env = util.Environment(EXPECTED_ENV_VARS, ask_for_missing=False)

        self.api = edusharing.EdusharingAPI(
            self.env['EDU_SHARING_BASE_URL'],
            self.env['EDU_SHARING_USERNAME'],
            self.env['EDU_SHARING_PASSWORD'])
        self.downloader = S3Downloader(
            self.env['S3_ENDPOINT_URL'],
            self.env['S3_ACCESS_KEY'],
            self.env['S3_SECRET_KEY'],
            self.env['S3_BUCKET_NAME']
        )

    def setup(self):
        self.setup_destination_folder(ES_FOLDER_NAME_GENERAL, ['Thuringia-public', 'Brandenburg-public',
                                                               'LowerSaxony-public'])
        self.setup_destination_folder(ES_FOLDER_NAME_THURINGIA, ['Thuringia-public'])

    def setup_destination_folder(self, folder_name: str, permitted_groups: Optional[List[str]]):
        if not permitted_groups:
            permitted_groups = ["Brandenburg-public", "Thuringia-public", "LowerSaxony-public"]

        sync_obj = self.api.get_sync_obj_folder()
        destination_folder = self.api.get_or_create_folder(sync_obj.id, folder_name)

        # set permissions for the permitted_groups
        # ToDo: Add permissions from excel-sheet.
        #  Split collections into single folders with corresponding permissions.
        self.api.set_permissions(destination_folder.id, permitted_groups, False)
        print(f"Created folder {folder_name} with permissions for: {permitted_groups}")

        return destination_folder

    def upload_h5p_file(self, folder_name: str, filename: str, metadata: h5p_extract_metadata.Metadata,
                        file: Optional[IO[bytes]] = None, relation: str = "", overwrite_contents: bool = True):
        # get h5p file, add metadata, upload and after all add permissions
        name = os.path.splitext(os.path.basename(filename))[0]
        keywords = ['h5p', metadata.title, metadata.collection, metadata.order]
        keywords.extend(metadata.keywords)

        # ToDo: Add the url of the frontend rendering page
        properties = generate_node_properties(metadata.title, metadata.title, metadata.publisher,
                                              metadata.license, keywords, folder_name, replication_source_id=name,
                                              relation=relation)

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
        metadata = h5p_extract_metadata.Metadata('title', 'publisher', [], '', '', [])
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
        keywords_excel = metadata_file.get_keywords()
        keywords = ["h5p", collection_name, "Arbeitspaket"]
        keywords.extend(keywords_excel)

        # ToDo: add publisher from excel-sheet and replace "MedienLB".
        #  Add License from excel-sheet.

        properties = generate_node_properties(
            collection_name, collection_name, "MedienLB", "", keywords, edusharing_folder_name,
            format="text/html", aggregation_level=2, aggregation_level_hpi=2
        )
        collection_rep_source_uuid = properties['ccm:replicationsourceuuid']
        collection_node = self.api.sync_node(edusharing_folder_name, properties,
                                             ['ccm:replicationsource', 'ccm:replicationsourceid'])
        print(f'Created Collection {collection_name}.')

        # check, if all required h5p-files are inside the zip
        filenames = []
        for filename in zip.namelist():
            if filename.endswith(".h5p"):
                filenames.append(filename)
        metadata_file.check_for_files(filenames=filenames)

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

        self.api.set_property_relation(collection_node.id, 'ccm:lom_relation', package_h5p_files_rep_source_uuids)
        self.api.set_property_relation(collection_node.id, 'ccm:hpi_lom_relation', package_h5p_files_rep_source_uuids)

    def upload_from_folder(self):
        self.setup()

        for obj in os.listdir(H5P_LOCAL_PATH):
            path = os.path.join(H5P_LOCAL_PATH, obj)
            if os.path.isfile(path):
                if obj.endswith('.h5p'):
                    # self.upload_h5p_single(path, FOLDER_NAME_GENERAL)
                    pass
                elif obj.endswith('.zip'):
                    self.upload_h5p_thr_collection(path, ES_FOLDER_NAME_THURINGIA)

    def upload_from_s3(self):
        self.setup()
        objects = self.downloader.get_object_list()
        total_size = 0
        for obj in objects:
            total_size += obj['Size']

        for obj in objects:
            path = os.path.join(H5P_TEMP_FOLDER, obj['Key'])
            self.downloader.download_object(obj['Key'], H5P_TEMP_FOLDER)
            if not os.path.exists(path):
                raise RuntimeError(f'Download of object {obj["Key"]} somehow failed')
            if path.endswith('.h5p'):
                # self.upload_h5p_single(path, ES_FOLDER_NAME_GENERAL)
                pass
            elif path.endswith('.zip'):
                self.upload_h5p_thr_collection(path, ES_FOLDER_NAME_THURINGIA)


class S3Downloader:
    def __init__(self, url: str, key: str, secret: str, bucket_name: str):
        self.env = util.Environment(EXPECTED_ENV_VARS, ask_for_missing=False)
        self.client = boto3.client(
            's3',
            endpoint_url=url,
            aws_access_key_id=key,
            aws_secret_access_key=secret,
        )
        self.bucket_name = bucket_name

    def check_bucket_exists(self) -> None:
        response = self.client.list_buckets()
        for bucket in response['Buckets']:
            if bucket['Name'] == self.bucket_name:
                break
        else:
            raise RuntimeError(f'Bucket {self.bucket_name} does not exist')

    def get_object_list(self) -> List[Dict]:
        self.check_bucket_exists()
        response = self.client.list_objects_v2(Bucket=self.bucket_name)
        return response['Contents']

    def download_object(self, object_key: str, dir_path: str, callback: Optional[Callable] = None):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.client.download_file(
            Bucket=self.bucket_name,
            Key=object_key,
            Filename=os.path.join(dir_path, object_key),
            Callback=callback
        )


if __name__ == '__main__':
    Uploader().upload_from_folder()
