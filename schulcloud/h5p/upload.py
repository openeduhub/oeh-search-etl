import os
import sys
import uuid
import re
import hashlib
from typing import Optional, List, IO, Callable, Dict
from datetime import datetime
from zipfile import ZipFile

import boto3

from schulcloud import util
from schulcloud.edusharing import EdusharingAPI, Node, NotFoundException, FoundTooManyException
from schulcloud.h5p.metadata import MetadataFile, Metadata, Collection

EXPECTED_ENV_VARS = [
    'EDU_SHARING_BASE_URL',
    'EDU_SHARING_USERNAME',
    'EDU_SHARING_PASSWORD',
    'S3_ENDPOINT_URL',
    'S3_ACCESS_KEY',
    'S3_SECRET_KEY',
    'S3_BUCKET_NAME'
]
TEMP_FOLDER = 'temp'
H5P_THUMBNAIL_PATH = 'schulcloud/h5p/H5Pthumbnail.png'

GROUPS_EXCEL_TO_ES = {
    'THR': 'Thuringia-public',
    'BRB': 'Brandenburg-public',
    'NDS': 'LowerSaxony-public'
}


def escape_filename(filename: str):
    return re.sub(r'[,;:\'="@$%/\\{}]', '_', filename)


def create_replicationsourceid(name: str):
    return hashlib.sha1(name.encode()).hexdigest()


def generate_node_properties(
        title: str,
        name: str,
        publisher: str,  # TODO: test whether edusharing supports multiple publishers/licenses
        license: str,
        keywords: List[str],
        folder_name: str,
        replication_source_id: Optional[str] = None,
        replication_source_uuid: Optional[str] = None,
        aggregation_level: int = 1,
        hpi_searchable: bool = True):
    if not replication_source_id:
        replication_source_id = name
    if not replication_source_uuid:
        replication_source_uuid = name
    if license is None or license == "":
        license = "CUSTOM"
    date = str(datetime.now())
    properties = {
        "cm:name": [escape_filename(name)],
        "cm:edu_metadataset": ["mds_oeh"],
        "cm:edu_forcemetadataset": ["true"],
        "ccm:objecttype": ["MATERIAL"],
        "ccm:replicationsource": [folder_name],
        "ccm:replicationsourceid": [create_replicationsourceid(replication_source_id)],
        "ccm:replicationsourcehash": [date],
        "ccm:replicationsourceuuid": [str(uuid.uuid5(uuid.NAMESPACE_URL, replication_source_uuid))],
        "ccm:commonlicense_key": [license],  # TODO: test whether edusharing supports multiple licenses
        "ccm:hpi_searchable": ['1' if hpi_searchable else '0'],
        "ccm:hpi_lom_general_aggregationlevel": [str(aggregation_level)],
        "cclom:title": [title],
        "cclom:aggregationlevel": [str(aggregation_level)],
        "cclom:general_language": ["de"],
        "cclom:general_keyword": keywords,
        "ccm:create_version": ["false"],
        "ccm:lifecyclecontributer_publisherFN": [publisher]
        # TODO: test whether edusharing supports multiple publishers
    }
    return properties


class Uploader:
    def __init__(self):
        self.env = util.Environment(EXPECTED_ENV_VARS, ask_for_missing=False)

        self.api = EdusharingAPI(
            self.env['EDU_SHARING_BASE_URL'],
            self.env['EDU_SHARING_USERNAME'],
            self.env['EDU_SHARING_PASSWORD'])
        self.downloader = S3Downloader(
            self.env['S3_ENDPOINT_URL'],
            self.env['S3_ACCESS_KEY'],
            self.env['S3_SECRET_KEY'],
            self.env['S3_BUCKET_NAME']
        )

    @staticmethod
    def get_permitted_groups(permissions: List[str]):
        if 'ALLE' in permissions:
            return list(GROUPS_EXCEL_TO_ES.values())
        else:
            return [GROUPS_EXCEL_TO_ES[group] for group in permissions]

    @staticmethod
    def get_metadata_file(zip: ZipFile):
        # get excel_sheet data
        for excel_filename in zip.namelist():
            if excel_filename.endswith(".xlsx"):
                excel_file = zip.open(excel_filename)
                metadata_file = MetadataFile(excel_file)
                break
        else:
            raise MetadataNotFoundError(zip)
        return metadata_file

    def setup_destination_folder(self, folder_name: str):
        sync_obj = self.api.get_sync_obj_folder()
        destination_folder = self.api.get_or_create_node(sync_obj.id, folder_name, type='folder')
        return destination_folder

    def upload_file(self, folder: Node, metadata: Metadata, file: Optional[IO[bytes]] = None, searchable: bool = True):
        # get h5p file, add metadata, upload and after all add permissions
        filename = os.path.basename(metadata.filepath)
        name = os.path.splitext(filename)[0]
        keywords = [metadata.title, metadata.publisher] + metadata.keywords
        if metadata.collection is not None:
            keywords.append(metadata.collection.name)

        self_opened_file = False
        if file is None:
            file = open(metadata.filepath, 'rb')
            self_opened_file = True

        properties = generate_node_properties(metadata.title, filename, metadata.publisher, metadata.license, keywords,
                                              folder.name, replication_source_id=name, hpi_searchable=searchable)

        node = self.api.get_or_create_node(folder.id, filename)

        self.api.upload_content(node.id, filename, file)
        if self_opened_file:
            file.close()

        for property, value in properties.items():
            self.api.set_property(node.id, property, value)

        permitted_groups = self.get_permitted_groups(permissions=metadata.permission)
        self.api.set_permissions(node.id, permitted_groups, False)

        if filename.endswith('h5p'):
            self.api.set_preview_thumbnail(node_id=node.id, filename=H5P_THUMBNAIL_PATH)

        return node.id, properties["ccm:replicationsourceuuid"][0]

    def upload_collection(self, collection: Collection, zip_file: ZipFile, es_folder: Node, collection_node: Node):
        # save the replicationsourceuuid, nodeId and the collection of each h5p-file corresponding to this package
        children_replication_source_uuids = []

        keywords = [collection.name]
        keywords.extend(collection.keywords)
        keywords.extend(collection.publishers)

        # TODO: test whether edusharing collections supports multiple publishers/licenses
        collection_properties = generate_node_properties(
            collection.name, collection.name, next(iter(collection.publishers)), next(iter(collection.licenses)),
            keywords,
            es_folder.name, aggregation_level=2
        )
        if not collection_node:
            collection_node = self.api.get_or_create_node(es_folder.id, collection.name)

        for property, value in collection_properties.items():
            self.api.set_property(collection_node.id, property, value)
        # permissions
        permitted_groups = self.get_permitted_groups(list(collection.permissions))
        self.api.set_permissions(collection_node.id, permitted_groups, False)

        # TODO: make option to ignore timestamps for (partially) failed uploads etc.

        for child in collection.children:
            file = zip_file.open(child.filepath)
            node_id, rep_source_uuid = self.upload_file(es_folder, child, file=file, searchable=False)
            file.close()
            children_replication_source_uuids.append(rep_source_uuid)
            self.api.set_collection_parent(node_id, collection_properties['ccm:replicationsourceuuid'][0])

        self.api.set_collection_children(collection_node.id, children_replication_source_uuids)

        # TODO: set thumbnail of first item or have other solution for non-h5p collections
        if collection.children[0].filepath.endswith('h5p'):
            self.api.set_preview_thumbnail(node_id=collection_node.id, filename=H5P_THUMBNAIL_PATH)

    def upload_zip(self, zip_file: ZipFile, es_folder_name: str, last_modified: Optional[datetime] = None):
        try:
            metadata_file = self.get_metadata_file(zip_file)
        except MetadataNotFoundError as exc:
            print(f'No metadata file found in {exc.zip.filename}. Skipping.', file=sys.stderr)
            return
        es_folder = self.setup_destination_folder(es_folder_name)

        for collection in metadata_file.collections:
            replicationsourceid = create_replicationsourceid(collection.name)
            collection_node = None

            try:
                collection_node = self.api.find_node_by_replication_source_id(replicationsourceid)
            except NotFoundException as err:
                # just upload
                pass
            except FoundTooManyException as err:
                # TODO: not sure if correct
                print(f'Found multiple nodes for collection: {collection.name}', file=sys.stderr)
                continue
            if collection_node:
                collection_node_children = self.api.get_children(collection_node.id)
                if not collection_node_children:
                    pass
                else:
                    if last_modified:
                        # collection already has some content, so check timestamps
                        edu_timestamp = self.api.get_node_timestamp(collection_node)
                        if edu_timestamp > last_modified:
                            continue
            self.upload_collection(collection, zip_file, es_folder, collection_node)

        for single_metadata in metadata_file.single_files:
            file = zip_file.open(single_metadata.filepath)
            self.upload_file(es_folder, single_metadata, file=file)
            file.close()

        metadata_file.close()

    def upload_from_s3(self):
        excludes = ['FWURAW']

        s3_objects = self.downloader.get_object_list()
        total_size = 0
        for s3_obj in s3_objects:
            total_size += s3_obj['Size']

        for s3_obj in s3_objects:
            if '/' not in s3_obj['Key']:
                print(f'{s3_obj["Key"]} is not within a folder will therefore be ignored', file=sys.stderr)
                continue
            if not s3_obj['Key'].endswith('.zip'):
                print(f'Skipping {s3_obj["Key"]}, not a zip file.', file=sys.stderr)
                continue

            folder_name = s3_obj['Key'].split('/')[0]

            if folder_name in excludes:
                print(f'Skipping {s3_obj["Key"]} because it\'s excluded')
                continue

            self.downloader.download_object(s3_obj['Key'], TEMP_FOLDER)
            zip_path = os.path.join(TEMP_FOLDER, s3_obj['Key'])
            zip_file = ZipFile(zip_path)

            last_modified = s3_obj['LastModified'].replace(tzinfo=None)
            self.upload_zip(zip_file, folder_name, last_modified)
            print(f'Upload done: {zip_file}')
            zip_file.close()
            os.remove(zip_path)

    def test_upload(self):
        sync = self.api.get_sync_obj_folder()
        h5p = self.api.get_or_create_node(sync.id, 'h5p', type='folder')
        nodes = self.api.get_children(h5p.id)
        for node in nodes:
            if node.name.startswith('mags4') or node.name.startswith('Mathematik'):
                self.api.delete_node(node.id)

        zip_file = ZipFile('schulcloud/h5p/Mathe_GS_4_Vol_2.zip')
        self.upload_zip(zip_file, 'h5p')

        nodes = self.api.get_children(h5p.id)
        permissions = self.get_permitted_groups(['ALLE'])
        for node in nodes:
            self.api.set_permissions(node.id, permissions, False)


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
    def __init__(self, zip: ZipFile):
        self.zip = zip
        super(MetadataNotFoundError, self).__init__('Could not find excel file with metadata')


if __name__ == '__main__':
    Uploader().upload_from_s3()
