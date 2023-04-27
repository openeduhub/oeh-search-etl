import os
import sys
import time
import uuid
import re
import hashlib
from typing import Optional, List, IO, Callable, Dict
from datetime import datetime
from zipfile import ZipFile

import boto3

from botocore.config import Config
from botocore.exceptions import ResponseStreamingError
from urllib3.exceptions import ProtocolError
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
    'S3_BUCKET_NAME',
    'S3_REGION'
]
TEMP_FOLDER = 'temp'
H5P_THUMBNAIL_PATH = 'schulcloud/h5p/H5Pthumbnail.png'

GROUPS_EXCEL_TO_ES = {
    'THR': 'Thuringia-public',
    'BRB': 'Brandenburg-public',
    'NDS': 'LowerSaxony-public'
}


def escape_filename(filename: str):
    """
    Return filename with escaped characters.
    @param filename: Name of the file
    """
    return re.sub(r'[,;:\'="@$?%/\\{}]', '_', filename)


def create_replicationsourceid(name: str):
    """
    Return replicationsoureceID with SHA1 encryption.
    @param name: Name of the replicationsource
    """
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
    """
    Return the node properties corresponding to mds_oeh metadataset.
    @param title: Title of the node
    @param name: Name of the node
    @param publisher: Publisher of the node
    @param license: License for the node
    @param keywords: Keywords of the node
    @param folder_name: Name of the replication source
    @param replication_source_id: Replication source ID of the node
    @param replication_source_uuid: Replication source UUID of the node
    @param aggregation_level: Aggregation level of the node
    @param hpi_searchable: 1 is equal to 'isSearchable', 0 is equal to 'notSearchable'
    """
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

        if self.env['EDU_SHARING_USERNAME'] != 'crawleruser':
            raise ValueException(self.env['EDU_SHARING_USERNAME'])
        self.api = EdusharingAPI(
            self.env['EDU_SHARING_BASE_URL'],
            self.env['EDU_SHARING_USERNAME'],
            self.env['EDU_SHARING_PASSWORD'])
        self.downloader = S3Downloader(
            self.env['S3_ENDPOINT_URL'],
            self.env['S3_ACCESS_KEY'],
            self.env['S3_SECRET_KEY'],
            self.env['S3_BUCKET_NAME'],
            self.env['S3_REGION']
        )

    @staticmethod
    def get_permitted_groups(permissions: List[str]):
        """
        Return permitted groups from Excelsheet, which matching with the list.
        @param permissions: List of known permissions
        """
        if 'ALLE' in permissions:
            return list(GROUPS_EXCEL_TO_ES.values())
        else:
            return [GROUPS_EXCEL_TO_ES[group] for group in permissions]

    @staticmethod
    def get_metadata_file(zip: ZipFile):
        """
        Return metadata from Excelsheet.
        @param zip: Zip file
        """
        for excel_filename in zip.namelist():
            if excel_filename.endswith(".xlsx"):
                excel_file = zip.open(excel_filename)
                metadata_file = MetadataFile(excel_file)
                break
        else:
            raise MetadataNotFoundError(zip)
        return metadata_file

    def collection_status(self, collection: Collection, zip_file: ZipFile):
        """
        Return exists, if the collection exists already on Edu-Sharing.
        Return missing, if the collection doesn't exist on Edu-Sharing.
        Return broken, if the collection exists partially on Edu-Sharing.
        @param collection: Node of collection
        @param zip_file: File as zip.
        """
        uploaded_nodes = 0
        for child in collection.children:
            file = zip_file.open(child.filepath)
            filename = os.path.basename(child.filepath)
            name = os.path.splitext(filename)[0]
            rep_source_id = create_replicationsourceid(name)
            file.close()
            node_exists = self.api.find_node_by_replication_source_id(rep_source_id, skip_exception=True)
            if not node_exists:
                if uploaded_nodes == 0:
                    return "missing"
                else:
                    return "broken"
            else:
                uploaded_nodes = uploaded_nodes + 1
        return "exists"

    def get_collection_owned(self, collection_node_id):
        collection_node = self.api.get_node(collection_node_id)
        collection_owner = collection_node.obj['owner']['firstName']
        return collection_owner

    def setup_destination_folder(self, folder_name: str):
        """
        Create the destination folder for the upload inside the sync_obj folder, if the folder doesn't exist.
        @param folder_name: Name of the folder
        """
        sync_obj = self.api.get_sync_obj_folder()
        destination_folder = self.api.get_or_create_node(sync_obj.id, folder_name, type='folder')
        return destination_folder

    def upload_file(self, folder: Node, metadata: Metadata, file: Optional[IO[bytes]] = None, searchable: bool = True):
        """
        Get the H5P-file and add the metadata from the excelsheet. Then upload the H5P-file with metadata and add
        the permission.
        @param folder: Basic node for the upload
        @param metadata: Metadata for the Node
        @param file: H5P-file to upload
        @param searchable: Boolean, if the node should be searchable in the 'Schulcloud-Verbund Software'
        """
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
            self.api.set_preview_thumbnail(node.id, H5P_THUMBNAIL_PATH)

        return node.id, properties["ccm:replicationsourceuuid"][0]

    def upload_collection(self, collection: Collection, zip_file: ZipFile, es_folder: Node, collection_node: Node):
        """
        Summarize related H5P-files to an educational collection.
        @param collection: Collection of H5P-files
        @param zip_file: File as zip
        @param es_folder: Folder on Edu-Sharing to upload to
        @param collection_node: Node of collection
        """
        children_replication_source_uuids = []
        keywords = [collection.name]
        keywords.extend(collection.keywords)
        keywords.extend(collection.publishers)

        # TODO: test whether edusharing collections supports multiple publishers/licenses
        collection_properties = generate_node_properties(
            collection.name, collection.name, next(iter(collection.publishers)), next(iter(collection.licenses)),
            keywords, es_folder.name, aggregation_level=2
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
            self.api.set_preview_thumbnail(collection_node.id, H5P_THUMBNAIL_PATH)

    def upload_zip(self, zip_file: ZipFile, es_folder_name: str, last_modified: Optional[datetime] = None):
        """
        Upload zip-file to Edu-sharing folder.
        @param zip_file: File as zip
        @param es_folder_name: Folder on Edu-Sharing to upload to
        @param last_modified: Optional timestamp
        """
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
                print(f'Found multiple nodes for collection: {collection.name}', file=sys.stderr)
                continue
            if collection_node:
                collection_status = self.collection_status(collection, zip_file)
                if collection_status == "missing":
                    pass
                if collection_status == "exists":
                    collection_owner = self.get_collection_owned(collection_node.id)
                    if collection_owner != self.api.username:
                        raise RuntimeError(
                            f'Collection {collection.name} exists already and is owned by: {collection_owner}')
                    else:
                        if last_modified:
                            # collection already has some content, so check timestamps
                            if collection_node.created_at > last_modified:
                                print(
                                    f'Collection {collection.name} already exists and is owned by {collection_owner}.')
                                continue
                if collection_status == "broken":
                    collection_owner = self.get_collection_owned(collection_node.id)
                    if collection_owner != self.api.username:
                        raise RuntimeError(
                            f'Collection {collection.name} is partially uploaded by: {collection_owner}')

            self.upload_collection(collection, zip_file, es_folder, collection_node)

        for single_metadata in metadata_file.single_files:
            file = zip_file.open(single_metadata.filepath)
            self.upload_file(es_folder, single_metadata, file=file)
            file.close()

        metadata_file.close()

    def upload_from_s3(self):
        """
        Upload zip-file from AWS S3 bucket to Edu-sharing folder.
        """

        s3_objects = self.downloader.get_object_list()
        total_size = 0
        for s3_obj in s3_objects:
            total_size += s3_obj['Size']

        for s3_obj in s3_objects:
            if not s3_obj['Key'].endswith('.zip'):
                print(f'Skipping {s3_obj["Key"]}, not a zip file.', file=sys.stderr)
                continue

            folder_name = "H5P"
            self.downloader.download_object(s3_obj['Key'], TEMP_FOLDER)

            zip_path = os.path.join(TEMP_FOLDER, s3_obj['Key'])
            zip_file = ZipFile(zip_path)

            last_modified = s3_obj['LastModified'].replace(tzinfo=None)
            self.upload_zip(zip_file, folder_name, last_modified)
            print(f'Upload done: {zip_file}')
            zip_file.close()
            os.remove(zip_path)

        print(f'Finished uploading H5P learning contents.')

    def test_upload(self):
        """
        Test the local upload to Edu-Sharing.
        """
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
    def __init__(self, url: str, key: str, secret: str, bucket_name: str, region: str):
        self.env = util.Environment(EXPECTED_ENV_VARS, ask_for_missing=False)
        s3_client_config = Config(
            region_name=region,
            tcp_keepalive=True,
            retries={
                'max_attempts': 10,
                'mode': 'adaptive'
            }
        )
        self.client = boto3.client(
            's3',
            endpoint_url=url,
            aws_access_key_id=key,
            aws_secret_access_key=secret,
            config=s3_client_config
        )
        self.bucket_name = bucket_name

    def check_bucket_exists(self) -> None:
        """
        Check, if the bucket exists on AWS S3.
        """
        response = self.client.list_buckets()
        for bucket in response['Buckets']:
            if bucket['Name'] == self.bucket_name:
                break
        else:
            raise RuntimeError(f'Bucket {self.bucket_name} does not exist')

    def get_object_list(self) -> List[Dict]:
        """
        Return max. 1000 objects from the AWS S3 bucket.
        """
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
        """
        Download all objects from the AWS S3 bucket to a local directory.
        @param object_key: The key from the AWS S3 object
        @param dir_path: Path to the directory to download to
        @param callback: Optional callback for the download
        """
        file_path = os.path.join(dir_path, object_key)
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        self.retry_function(self.client.download_file,
                            {"Bucket": self.bucket_name, "Key": object_key, "Filename": file_path, "Callback": callback
                             }, 10)

    @staticmethod
    def retry_function(function, params: Dict, max_retries: int):
        retries = 0
        while retries < max_retries:
            try:
                function(**params)
                break
            except (ResponseStreamingError, ConnectionResetError, ProtocolError) as error:
                print(f'>>>>>>Got Error1: {type(error)}')
                if retries == max_retries - 1:
                    raise error
                else:
                    print(f'>>>>>>retry: {retries} for {function}')
                    retries = retries + 1
            except BaseException as error:
                print(f'>>>>>>Got Error2: {type(error)}')
                print(f'>>>>>>Errortype is ResponseStreamingError: {type(error) is ResponseStreamingError}')
                if retries == max_retries - 1:
                    raise error
                else:
                    print(f'retry: {retries} for {function}')
                    retries = retries + 1


class MetadataNotFoundError(Exception):
    def __init__(self, zip: ZipFile):
        self.zip = zip
        super(MetadataNotFoundError, self).__init__('Could not find excel file with metadata')


class ValueException(Exception):
    def __init__(self, name: str):
        super(ValueException, self).__init__(f'Wrong Edu-Sharing user found for crawling: "{name}". Use "crawleruser" '
                                             f'instead.')


if __name__ == '__main__':
    Uploader().upload_from_s3()
