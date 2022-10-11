import os
import sys
import uuid
import zipfile
import util
import hashlib
from typing import Optional, List, IO, Callable, Dict
from datetime import datetime

import boto3

import edusharing
import h5p_extract_metadata
from h5p_extract_metadata import MetadataFile, Metadata

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
    if license is None or license == "":
        license = "CUSTOM"
    if url is None or url == "":
        url = f'/content/{replication_source_uuid}?isCollection=false&q=h5p'
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
        "ccm:lifecyclecontributer_publisherFN": [publisher]
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

    def setup_destination_folder(self, folder_name: str):
        sync_obj = self.api.get_sync_obj_folder()
        destination_folder = self.api.get_or_create_folder(sync_obj.id, folder_name)
        return destination_folder

    def upload_h5p_file(self, folder_name: str, filename: str, metadata: Metadata,
                        file: Optional[IO[bytes]] = None, s3_last_modified: Optional[datetime] = None,
                        relation: str = ""):
        # get h5p file, add metadata, upload and after all add permissions
        name = os.path.splitext(os.path.basename(filename))[0]
        keywords = ['h5p', metadata.title, metadata.collection, metadata.order, metadata.publisher]
        keywords.extend(metadata.keywords)

        # ToDo: Add the url of the frontend rendering page
        properties = generate_node_properties(metadata.title, metadata.title, metadata.publisher,
                                              metadata.license, keywords, folder_name, replication_source_id=name,
                                              relation=relation)

        rep_value = name
        rep_value = hashlib.sha1(rep_value.encode()).hexdigest()
        node_list = self.api.search_custom("ccm:replicationsourceid", rep_value, 10, 'FILES')
        if len(node_list) > 0:
            node_temp = node_list[0]
            if s3_last_modified is not None:
                timestamps = self.get_timestamp_edu_and_s3(s3_last_modified, node_temp)
                s3_last_modified = timestamps[0]
                timestamp_edusharing = timestamps[1]
                if timestamp_edusharing > s3_last_modified:
                    return

        node = self.api.sync_node(folder_name, properties, ['ccm:replicationsource', 'ccm:replicationsourceid'])

        if file is None:
            file = open(filename, 'rb')
        files = {
            'file': (os.path.basename(filename), file, 'application/zip', {'Expires': '0'})
        }
        mimetype = 'application%2Fzip'
        url_upload = f'/node/v1/nodes/-home-/{node.id}' \
                     f'/content?versionComment=MAIN_FILE_UPLOAD&mimetype={mimetype}'
        self.api.make_request('POST', url_upload, files=files, stream=True)
        # permissions
        permitted_groups = self.get_permitted_groups(permissions=metadata.permission)
        self.api.set_permissions(node.id, permitted_groups, False)
        file.close()

        print(f'Upload complete for: {filename}')
        return node.id, properties["ccm:replicationsourceuuid"]

    def upload_h5p_collection(self, edusharing_folder_name: str, metadata_file: MetadataFile, zip: zipfile.ZipFile):
        """
            Upload multiple H5P files within a zip archive, as a collection
        """
        # save the replicationsourceuuid, nodeId and the collection of each h5p-file corresponding to this package
        package_h5p_files_rep_source_uuids = []
        collection_name = metadata_file.get_collection()

        # check, if all required h5p-files are inside the zip
        filenames = []
        for filename in zip.namelist():
            if filename.endswith(".h5p"):
                filenames.append(filename)
        metadata_file.check_for_files(filenames=filenames)

        # now update metadata from the new node (add children) and the h5p-files (add parent)
        keywords_excel = metadata_file.get_keywords()
        keywords = ["h5p", collection_name, "Arbeitspaket", metadata_file.get_publisher()]
        keywords.extend(keywords_excel)

        properties = generate_node_properties(
            collection_name, collection_name, metadata_file.get_publisher(), metadata_file.get_license(), keywords,
            edusharing_folder_name, format="text/html", aggregation_level=2, aggregation_level_hpi=2
        )
        collection_rep_source_uuid = properties['ccm:replicationsourceuuid']
        collection_node = self.api.sync_node(edusharing_folder_name, properties,
                                             ['ccm:replicationsource', 'ccm:replicationsourceid'])
        # permissions
        permissions = [metadata_file.get_collection_permission()]
        permitted_groups = self.get_permitted_groups(permissions)
        self.api.set_permissions(collection_node.id, permitted_groups, False)
        print(f'Created Collection {collection_name}.')

        # loop through the unzipped h5p-files
        for filename in zip.namelist():
            if filename.endswith(".h5p"):
                metadata = metadata_file.get_metadata(filename)
                file = zip.open(filename)

                relation = f"{{'kind': 'ispartof', 'resource': {{'identifier': {collection_rep_source_uuid}}}}}"

                result = self.upload_h5p_file(edusharing_folder_name, filename, metadata, file=file, relation=relation)
                file.close()
                if result is None:
                    break
                node_id, rep_source_uuid = result
                # metadata_of_node = self.api.get_metadata_of_node(nodeId=node_id)
                # if metadata_of_node['node']['preview']['type'] == "TYPE_DEFAULT":
                self.api.set_preview_thumbnail(node_id=node_id, filename='thumbnail/H5Pthumbnail.png')
                rep_source_uuid_clean = str(rep_source_uuid).replace('[', '').replace(']', '').replace("'", "")
                package_h5p_files_rep_source_uuids.append(rep_source_uuid_clean)

        self.api.set_property_relation(collection_node.id, 'ccm:lom_relation', package_h5p_files_rep_source_uuids)
        self.api.set_property_relation(collection_node.id, 'ccm:hpi_lom_relation', package_h5p_files_rep_source_uuids)

        # set preview thumbnail
        self.api.set_preview_thumbnail(node_id=collection_node.id, filename='thumbnail/H5Pthumbnail.png')

    def upload_h5p_non_collection(self, edusharing_folder_name: str, metadata_file: MetadataFile, zip: zipfile.ZipFile,
                                  s3_last_modified: Optional[datetime] = None):
        """
            Upload multiple H5P files within a zip archive, without a collection
        """

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

                result = self.upload_h5p_file(edusharing_folder_name, filename, metadata, file, s3_last_modified)
                if result is None:
                    break
                node_id, rep_source_uuid = result
                # metadata_of_node = self.api.get_metadata_of_node(nodeId=node_id)
                # if metadata_of_node['node']['preview']['type'] == "TYPE_DEFAULT":
                self.api.set_preview_thumbnail(node_id=node_id, filename='thumbnail/H5Pthumbnail.png')

    def get_permitted_groups(self, permissions: List[str]):
        permitted_groups = []
        for permission in permissions:
            if permission == "ALLE":
                permitted_groups = ['Thuringia-public', 'Brandenburg-public', 'LowerSaxony-public']
            elif permission == "THR":
                permitted_groups.append("Thuringia-public")
            elif permission == "NDS":
                permitted_groups.append("LowerSaxony-public")
            elif permission == "BRB":
                permitted_groups.append("Brandenburg-public")
        return permitted_groups

    def get_metadata_file(self, zip: zipfile.ZipFile):
        # get excel_sheet data
        for excel_filename in zip.namelist():
            if excel_filename.endswith(".xlsx"):
                excel_file = zip.open(excel_filename)
                metadata_file = h5p_extract_metadata.MetadataFile(excel_file)
                break
        else:
            raise MetadataNotFoundError(zip)
        return metadata_file

    def upload_from_folder(self):
        objects = os.listdir(H5P_LOCAL_PATH)
        for obj in objects:
            path = os.path.join(H5P_LOCAL_PATH, obj)
            if '/' not in obj:
                print(f'{obj} is not within a folder will therefore be ignored', file=sys.stderr)
                continue
            es_folder_name = obj.split('/')[-2]
            try:
                zip = zipfile.ZipFile(path)
                metadata_file = self.get_metadata_file(zip)
                collection_name = metadata_file.get_collection()
                self.setup_destination_folder(es_folder_name)
                if collection_name is None:
                    self.upload_h5p_non_collection(es_folder_name, metadata_file, zip)
                else:
                    self.upload_h5p_collection(es_folder_name, metadata_file, zip)
            finally:
                try:
                    metadata_file.close()
                except NameError:
                    pass
                try:
                    zip.close()
                except NameError:
                    pass

    def upload_from_s3(self):
        objects = self.downloader.get_object_list()
        total_size = 0
        for obj in objects:
            total_size += obj['Size']

        for obj in objects:
            path = os.path.join(H5P_TEMP_FOLDER, obj['Key'])
            if '/' not in obj['Key']:
                print(f'{obj["Key"]} is not within a folder will therefore be ignored', file=sys.stderr)
                continue
            es_folder_name, _ = obj['Key'].split('/')
            if path.endswith('.zip'):
                self.downloader.download_object(obj['Key'], H5P_TEMP_FOLDER)
                try:
                    zip = zipfile.ZipFile(path)
                    metadata_file = self.get_metadata_file(zip)
                    collection_name = metadata_file.get_collection()
                    s3_last_modified = obj['LastModified']
                    self.setup_destination_folder(es_folder_name)
                    if collection_name is None:
                        self.upload_h5p_non_collection(es_folder_name, metadata_file, zip, s3_last_modified)
                    else:
                        rep_value = hashlib.sha1(collection_name.encode()).hexdigest()
                        collection_node_list = self.api.search_custom("ccm:replicationsourceid", rep_value, 10, 'FILES')
                        if len(collection_node_list) == 0:
                            self.upload_h5p_collection(es_folder_name, metadata_file, zipfile.ZipFile(path))
                        else:
                            collection_node = collection_node_list[0]
                            if s3_last_modified is not None:
                                timestamps = self.get_timestamp_edu_and_s3(s3_last_modified, collection_node)
                                timestamp_edusharing = timestamps[1]
                                s3_last_modified = timestamps[0]
                                if timestamp_edusharing < s3_last_modified:
                                    self.upload_h5p_collection(es_folder_name, metadata_file, zipfile.ZipFile(path))
                except MetadataNotFoundError as exc:
                    print(f'No metadata file found in {exc.zip.filename}. Skipping.', file=sys.stderr)
                finally:
                    try:
                        metadata_file.close()
                    except NameError:
                        pass
                    try:
                        zip.close()
                    except NameError:
                        pass
                    os.remove(path)
            else:
                print(f'Skipping {obj["Key"]}, not a zip.', file=sys.stderr)

    def get_timestamp_edu_and_s3(self, s3_last_modified, node):
        # timestamp of the node
        res = self.api.get_metadata_of_node(node.id)
        res_createdAt = str(res["node"]["createdAt"])
        res_clean = res_createdAt.replace("Z", "")
        timestamp_edusharing = datetime.fromisoformat(res_clean)
        s3_last_modified = s3_last_modified.replace(tzinfo=None)
        s3_last_modified = s3_last_modified
        timestamps = [s3_last_modified, timestamp_edusharing]
        return timestamps


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
        objs = response['Contents']
        while response['IsTruncated']:
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name,
                ContinuationToken=response['NextContinuationToken']
            )
            objs += response['Contents']
        return objs

    def download_object(self, object_key: str, dir_path: str, callback: Optional[Callable] = None):
        file_path = os.path.join(dir_path, object_key)
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        self.client.download_file(
            Bucket=self.bucket_name,
            Key=object_key,
            Filename=file_path,
            Callback=callback
        )


class MetadataNotFoundError(Exception):
    def __init__(self, zip: zipfile.ZipFile):
        self.zip = zip
        super(MetadataNotFoundError, self).__init__('Could not find excel file with metadata')


if __name__ == '__main__':
    Uploader().upload_from_s3()
