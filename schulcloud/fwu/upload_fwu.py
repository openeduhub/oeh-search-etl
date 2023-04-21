import uuid
import hashlib
from typing import Optional, List
from datetime import datetime

import boto3
import converter.env as env
from bs4 import BeautifulSoup

from schulcloud.edusharing import EdusharingAPI, NotFoundException


class Uploader:
    files_index = [5501191, 5501193, 5501202, 5501207, 5501211, 5501213, 5501219, 5501222, 5501224, 5501225, 5501234,
                   5501235, 5501238, 5501239, 5501245, 5501248, 5501252, 5501259, 5501267, 5501454, 5501458, 5501460,
                   5501472, 5501478, 5501588, 5501595, 5501597, 5501630, 5501638, 5501649, 5501655, 5501656, 5501657,
                   5501665, 5501685, 5511001, 5511002, 5511003, 5511004, 5511005, 5511006, 5511018, 5511019, 5511024,
                   5511044, 5511045, 5511050, 5511057, 5511089, 5511093, 5511094, 5511095, 5511098, 5511099, 5511100,
                   5511102, 5511106, 5511123, 5511128, 5511138, 5511184, 5511356, 5521211, 5521227, 5521287, 5521289,
                   5521310, 5521344, 5521345, 5521348, 5521354, 5521366, 5521370, 5521405, 5521408, 5521411, 5521413,
                   5521415, 5521418, 5521427]

    def __init__(self):
        if env.get('EDU_SHARING_USERNAME') != 'crawleruser':
            raise ValueException(env.get('EDU_SHARING_USERNAME'))
        self.api = EdusharingAPI(
            env.get('EDU_SHARING_BASE_URL'),
            env.get('EDU_SHARING_USERNAME'),
            env.get('EDU_SHARING_PASSWORD')
        )
        self.downloader = S3Downloader(
            env.get('S3_ENDPOINT_URL'),
            env.get('S3_ACCESS_KEY'),
            env.get('S3_SECRET_KEY'),
            env.get('S3_BUCKET_NAME'),
        )

    def setup_destination_folder(self, folder_name: str):
        """
        Create the destination folder for the upload inside the sync_obj folder, if the folder doesn't exist.
        @param folder_name: Name of the folder
        """
        sync_obj = self.api.get_sync_obj_folder()
        destination_folder = self.api.get_or_create_node(sync_obj.id, folder_name, type='folder')
        return destination_folder

    def upload(self):
        """
        Upload the FWU content from AWS S3-bucket to Edu-Sharing and add the metadata to the corresponding node.
        """
        # Fetch the metadata from S3 - Loop over known files (files_index)
        for index in self.files_index:
            key = str(index) + '/index.html'
            response = self.downloader.read_object(key)

            title = self.get_data(response, 'pname')
            title = self.sanitize_string(title)
            description = self.get_data(response, 'ptext')
            thumbnail_key = self.get_data(response, 'player_outer')
            thumbnail_bytes = self.downloader.read_object(str(index) + '/' + thumbnail_key)
            keywords = ['FWU', title]
            license = "COPYRIGHT_LICENSE"
            publisher = 'FWU Institut für Film und Bild in Wissenschaft und Unterricht gemeinnützige GmbH'
            target_url = f'/api/v3/fwu/{key}'

            # Upload the metadata to Edu-Sharing
            es_folder = self.setup_destination_folder('FWU')
            properties = generate_node_properties(title=title, description=description, keywords=keywords,
                                                  replication_source_id=title, hpi_searchable=True, license=license,
                                                  publisher=publisher, url=target_url)

            node = None
            try:
                node = self.api.find_node_by_replication_source_id(properties["ccm:replicationsourceid"][0])
            except NotFoundException:
                pass

            if not node:
                node = self.api.get_or_create_node(es_folder.id, title, properties=properties)

                for property, value in properties.items():
                    self.api.set_property(node.id, property, value)

                # Set thumbnail
                try:
                    self.api.set_preview_thumbnail(node.id, thumbnail_bytes, type='remote')
                except:
                    raise RuntimeError(f'Error: Can not set thumbnail.')

                print(f'Successfully upload file "{title}" (FWU-{index}) to Edu-Sharing.')

            else:
                print(f'Node "{title}" already exist on Edu-Sharing.')

        print(f'Successfully upload all FWU-metadata to Edu-sharing.')

    def get_data(self, body: str, class_name: str):
        """
        Extract the metadata from HTML.
        @param body: HTML body-tag with HTML content
        @param class_name: Name of the CSS-class in the HTML-tag.
        """
        if not class_name == "pname" and not class_name == "ptext" and not class_name == "player_outer":
            raise RuntimeError(
                f'False value "{class_name}" for class_name in get_data(). Options: pname, ptext, player_outer')

        s = BeautifulSoup(body, 'html.parser')

        html_snippet = s.find_all("div", class_=class_name)
        html_snippet = str(html_snippet)

        if class_name == "player_outer":
            index_start = html_snippet.index("(", 0) + 1
            index_end = html_snippet.index(")", 2)
        else:
            index_start = html_snippet.index(">", 0) + 1
            index_end = html_snippet.index("<", 2)

        result = html_snippet[index_start:index_end]
        result = result.strip()

        if class_name != "player_outer":
            self.validate_result(class_name, result)

        return result

    def validate_result(self, class_name: str, result: str):
        """
        Validate, if the result is found inside the CSS-class.
        @param class_name: Name of the CSS-class in the HTML-tag.
        @param result: Content of the extracted HTML-tag
        """
        data_definition = ""

        if class_name == "pname":
            data_definition = "Title"
        elif class_name == "ptext":
            data_definition = "Description"

        if result is None or result == "" or result == " ":
            raise RuntimeError(f'{data_definition} not found in class "{class_name}"')

    def sanitize_string(self, string: str):
        """
        Replace german umlauts and single quotes.
        @param string: String to sanitize
        """
        string = string.replace('ä', 'ae')
        string = string.replace('ö', 'oe')
        string = string.replace('ü', 'ue')
        string = string.replace('ß', 'ss')
        string = string.replace('Ä', 'Ae')
        string = string.replace('Ö', 'Oe')
        string = string.replace('Ü', 'Ue')
        string = string.replace('\'', '')
        string = string.replace(':', ' -')

        return string


class S3Downloader:
    def __init__(self, url: str, access_key: str, secret_key: str, bucket_name: str):
        self.client = boto3.client(
            's3',
            endpoint_url=url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.s3 = boto3.resource(
            's3',
            endpoint_url=url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.bucket_name = bucket_name

    def check_bucket_exists(self, bucket_name: str):
        """
        Check, if the bucket exists on AWS S3.
        @param bucket_name: Name of the bucket on AWS S3
        """
        response = self.client.list_buckets()
        for bucket in response['Buckets']:
            if bucket['Name'] == bucket_name:
                return True
        else:
            raise RuntimeError(f'Bucket {bucket_name} does not exist')

    def get_all_objects(self):
        """
        Return a file list with all object keys from the AWS S3 bucket.
        """
        self.check_bucket_exists(self.bucket_name)
        bucket = self.s3.Bucket(self.bucket_name)
        files_list = []

        for object in bucket.objects.all():
            file = object.key
            files_list.append(file)

        return files_list

    def read_object(self, object_key: str):
        """
        Return the content of the specific AWS S3 object.
        @param object_key: Object key from AWS S3 object.
        """
        self.check_bucket_exists(self.bucket_name)
        s3_object = self.s3.Object(bucket_name=self.bucket_name, key=object_key)
        response = s3_object.get()['Body'].read()
        return response


def generate_node_properties(
        title: str,
        description: str,
        publisher: str,
        license: str,
        keywords: List[str],
        url: Optional[str] = None,
        replication_source_id: Optional[str] = None,
        replication_source_uuid: Optional[str] = None,
        aggregation_level: int = 1,
        hpi_searchable: bool = True):
    """
    Return the node properties corresponding to mds_oeh metadataset.
    @param title: Title of the node
    @param description: Description of the node
    @param publisher: Publisher of the node
    @param license: License for the node
    @param keywords: Keywords of the node
    @param url: URL for external resources
    @param replication_source_id: Replication source ID of the node
    @param replication_source_uuid: Replication source UUID of the node
    @param aggregation_level: Aggregation level of the node
    @param hpi_searchable: 1 is equal to 'isSearchable', 0 is equal to 'notSearchable'
    """
    if not replication_source_id:
        replication_source_id = title
    if not replication_source_uuid:
        replication_source_uuid = title
    if license is None or license == "":
        license = "CUSTOM"
    date = str(datetime.now())
    properties = {
        "cm:name": [title],
        "cm:edu_metadataset": ["mds_oeh"],
        "cm:edu_forcemetadataset": ["true"],
        "ccm:objecttype": ["MATERIAL"],
        "ccm:replicationsource": ["FWU"],
        "ccm:replicationsourceid": [hashlib.md5(replication_source_id.encode()).hexdigest()],
        "ccm:replicationsourcehash": [date],
        "ccm:replicationsourceuuid": [str(uuid.uuid5(uuid.NAMESPACE_URL, replication_source_uuid))],
        "ccm:commonlicense_key": [license],
        "ccm:hpi_searchable": ['1' if hpi_searchable else '0'],
        "ccm:hpi_lom_general_aggregationlevel": [str(aggregation_level)],
        "cclom:title": [title],
        "cclom:general_description": [description],
        "cclom:aggregationlevel": [str(aggregation_level)],
        "cclom:general_language": ["de"],
        "cclom:general_keyword": keywords,
        "ccm:create_version": ["false"],
        "ccm:lifecyclecontributer_publisherFN": [publisher],
        "ccm:wwwurl": [url]
    }
    return properties


class ValueException(Exception):
    def __init__(self, name: str):
        super(ValueException, self).__init__(f'Wrong Edu-Sharing user found for crawling: "{name}". Use "crawleruser" '
                                             f'instead.')


if __name__ == '__main__':
    Uploader().upload()
