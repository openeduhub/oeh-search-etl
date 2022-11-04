import os
import random
import sys
import uuid
import util
import hashlib
from typing import Optional, List, IO, Callable, Dict
from datetime import datetime
from zipfile import ZipFile

import boto3

import edusharing
from h5p_extract_metadata import MetadataFile, Metadata, Collection


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

GROUPS_EXCEL_TO_ES = {
    'THR': 'Thuringia-public',
    'BRB': 'Brandenburg-public',
    'NDS': 'LowerSaxony-public'
}


def generate_node_properties(
        title: str,
        name: str,
        publisher: str,  # TODO: test whether edusharing supports multiple publishers/licenses
        license: str,
        keywords: List[str],
        folder_name: str,
        replication_source_id: Optional[str] = None,
        replication_source_uuid: Optional[str] = None,
        relation: Optional[str] = None,
        aggregation_level: int = 1,
        hpi_searchable: bool = True):
    if not replication_source_id:
        replication_source_id = name
    if not replication_source_uuid:
        replication_source_uuid = str(uuid.uuid4())
    if not relation:
        relation = "{'kind': 'ispartof', 'resource': {'identifier': []}}"
    if license is None or license == "":
        license = "CUSTOM"
    date = str(datetime.now())
    properties = {
        "ccm:objecttype": ["MATERIAL"],
        "ccm:replicationsource": [folder_name],
        "ccm:replicationsourceid": [hashlib.sha1(replication_source_id.encode()).hexdigest()],
        "ccm:replicationsourcehash": [date],
        "ccm:replicationsourceuuid": [replication_source_uuid],
        "ccm:commonlicense_key": [license],  # TODO: test whether edusharing supports multiple licenses
        "ccm:hpi_searchable": ['1' if hpi_searchable else '0'],
        "ccm:hpi_lom_general_aggregationlevel": [str(aggregation_level)],
        "cclom:title": [title],
        "cclom:aggregationlevel": [str(aggregation_level)],
        "cclom:general_language": ["de"],
        "cclom:general_keyword": keywords,
        "ccm:lom_annotation": ["{'description': 'searchable==1', 'entity': 'crawler'}"],
        "ccm:hpi_lom_relation": [relation],
        "ccm:lom_relation": [relation],
        "ccm:create_version": ["false"],
        "ccm:lifecyclecontributer_publisherFN": [publisher]  # TODO: test whether edusharing supports multiple publishers
    }
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

    def upload_file(self, folder: edusharing.Node, metadata: Metadata, file: Optional[IO[bytes]] = None, relation: str = "", searchable: bool = True):
        # get h5p file, add metadata, upload and after all add permissions
        filename = os.path.basename(metadata.filepath)
        name = os.path.splitext(filename)[0]
        keywords = [metadata.title, metadata.collection.name, metadata.publisher] + metadata.keywords

        self_opened_file = False
        if file is None:
            file = open(metadata.filepath, 'rb')
            self_opened_file = True

        properties = generate_node_properties(metadata.title, filename, metadata.publisher, metadata.license, keywords,
                                              folder.name, replication_source_id=name, relation=relation,
                                              hpi_searchable=searchable)

        node = self.api.get_or_create_node(folder.id, filename, properties=properties)

        self.api.upload_content(node.id, filename, file)
        if self_opened_file:
            file.close()

        permitted_groups = self.get_permitted_groups(permissions=metadata.permission)
        self.api.set_permissions(node.id, permitted_groups, False)

        if filename.endswith('h5p'):
            metadata_of_node = self.api.get_metadata_of_node(node.id)
            if metadata_of_node['node']['preview']['type'] == "TYPE_DEFAULT":
                self.api.set_preview_thumbnail(node_id=node.id, filename='thumbnail/H5Pthumbnail.png')

        print(f'Upload complete for: {metadata.filepath}')
        return node.id, properties["ccm:replicationsourceuuid"][0]

    def upload_collection(self, collection: Collection, zip_file: ZipFile, es_folder: edusharing.Node):
        # save the replicationsourceuuid, nodeId and the collection of each h5p-file corresponding to this package
        children_replication_source_uuids = []

        keywords = [collection.name]
        keywords.extend(collection.keywords)
        keywords.extend(collection.publishers)

        # TODO: test whether edusharing collections supports multiple publishers/licenses
        collection_properties = generate_node_properties(
            collection.name, collection.name, next(iter(collection.publishers)), next(iter(collection.licenses)), keywords,
            es_folder.name, aggregation_level=2
        )
        collection_node = self.api.get_or_create_node(es_folder.id, collection.name, properties=collection_properties)
        # permissions
        permitted_groups = self.get_permitted_groups(list(collection.permissions))
        self.api.set_permissions(collection_node.id, permitted_groups, False)
        print(f'Created Collection {collection.name}.')

        # TODO: make option to ignore timestamps for (partially) failed uploads etc.

        for child in collection.children:
            file = zip_file.open(child.filepath)
            relation = f"{{'kind': 'ispartof', 'resource': {{'identifier': {collection_properties['ccm:replicationsourceuuid']}}}}}"
            result = self.upload_file(es_folder, child, file=file, relation=relation, searchable=False)
            file.close()
            if result is None:
                break
            node_id, rep_source_uuid = result
            children_replication_source_uuids.append(rep_source_uuid)

        self.api.set_property_relation(collection_node.id, 'ccm:lom_relation', children_replication_source_uuids)
        self.api.set_property_relation(collection_node.id, 'ccm:hpi_lom_relation', children_replication_source_uuids)

        # TODO: set thumbnail of first item
        self.api.set_preview_thumbnail(node_id=collection_node.id, filename='thumbnail/H5Pthumbnail.png')

    def upload_from_s3(self):
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

            zip_path = os.path.join(TEMP_FOLDER, s3_obj['Key'])
            es_folder_name, _ = s3_obj['Key'].split('/')
            self.downloader.download_object(s3_obj['Key'], TEMP_FOLDER)
            zip_file = ZipFile(zip_path)
            try:
                metadata_file = self.get_metadata_file(zip_file)
            except MetadataNotFoundError as exc:
                print(f'No metadata file found in {exc.zip.filename}. Skipping.', file=sys.stderr)
                continue

            for collection in metadata_file.collections:
                es_folder = self.setup_destination_folder(es_folder_name)

                replicationsourceid = hashlib.sha1(collection.name.encode()).hexdigest()
                collection_node = None
                try:
                    collection_node = self.api.find_node_by_replication_source_id(replicationsourceid)
                except edusharing.NotFoundException as err:
                    # just upload
                    pass
                except edusharing.FoundTooManyException as err:
                    # TODO: not sure if correct
                    print(f'Found multiple nodes for collection: {collection.name}', file=sys.stderr)
                    continue
                if collection_node:
                    # collection already has some content, so check timestamps
                    edu_timestamp = self.api.get_node_timestamp(collection_node)
                    s3_last_modified = s3_obj['LastModified'].replace(tzinfo=None)
                    if edu_timestamp > s3_last_modified:
                        continue
                self.upload_collection(collection, ZipFile(zip_path), es_folder)

            for single_metadata in metadata_file.single_files:
                file = zip_file.open(single_metadata.filepath)
                self.upload_file(es_folder_name, single_metadata, file=file)
                file.close()

            metadata_file.close()
            zip_file.close()
            os.remove(zip_path)


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
