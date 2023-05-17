import json
import datetime
import sys
import time
import boto3
from bs4 import BeautifulSoup

import requests
import scrapy.http
from scrapy.spiders import CrawlSpider
from scrapy.spidermiddlewares.httperror import HttpError

import converter.env as env
from converter.constants import Constants
from converter.items import *
from converter.spiders.base_classes.lom_base import LomBase


class FWUSpider(CrawlSpider, LomBase):
    """
    This crawler fetches data from the S3, where the FWU contents are stored.

    For better understanding, please refer to LOM documentation(http://sodis.de/lom-de/LOM-DE.doc) and openduhub /
    oeh-search-etl on Github

    Author: Team CaptnEdu
    """
    # ToDo: Comment out name
    # name = 'fwu_spider'
    friendlyName = 'FWU'
    version = '0.1'
    files_index = [5501191, 5501193, 5501202, 5501207, 5501211, 5501213, 5501219, 5501222, 5501224, 5501225, 5501234,
                   5501235, 5501238, 5501239, 5501245, 5501248, 5501252, 5501259, 5501267, 5501454, 5501458, 5501460,
                   5501472, 5501478, 5501588, 5501595, 5501597, 5501630, 5501638, 5501649, 5501655, 5501656, 5501657,
                   5501665, 5501685, 5511001, 5511002, 5511003, 5511004, 5511005, 5511006, 5511018, 5511019, 5511024,
                   5511044, 5511045, 5511050, 5511057, 5511089, 5511093, 5511094, 5511095, 5511098, 5511099, 5511100,
                   5511102, 5511106, 5511123, 5511128, 5511138, 5511184, 5511356, 5521211, 5521227, 5521287, 5521289,
                   5521310, 5521344, 5521345, 5521348, 5521354, 5521366, 5521370, 5521405, 5521408, 5521411, 5521413,
                   5521415, 5521418, 5521427]

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)
        self.s3_url = env.get('S3_ENDPOINT_URL')
        self.s3_access_key = env.get('S3_ACCESS_KEY')
        self.s3_secret_key = env.get('S3_SECRET_KEY')
        self.s3_bucket = env.get('S3_BUCKET_NAME')
        self.download_delay = float(env.get('SODIX_DOWNLOAD_DELAY', default='0.5'))

    def start_requests(self):
        yield self.make_request()

    def make_request(self):
        s3 = boto3.resource(
            's3',
            endpoint_url=self.s3_url,
            aws_access_key_id=self.s3_access_key,
            aws_secret_access_key=self.s3_secret_key,
        )

        fwu_json = {}

        for index in self.files_index:
            key = str(index) + '/index.html'
            s3_object = s3.Object(bucket_name=self.s3_bucket, key=key)
            html_string = s3_object.get()['Body'].read()
            title = self.get_data(html_string, 'pname')
            description = self.get_data(html_string, 'ptext')
            thumbnail_path = self.get_data(html_string, 'player_outer')

            thumbnail_bytes = s3.Object(bucket_name=self.s3_bucket, key=str(index) + '/' + thumbnail_path)
            thumbnail = thumbnail_bytes.get()['Body'].read()

            fwu_object = {'title': title, 'description': description, 'thumbnail': thumbnail.hex()}
            fwu_json[f'fwu-object-{str(index)}'] = fwu_object

        fwu_json_all = json.dumps(fwu_json)

        # Possible Mock Response
        #ToDo: It seems, that in scrapy it is forbidden to send NO URL!!!!

        return fwu_json_all

    def parse(self, response):
        json_response = json.loads(response)
        print(f'JSON RESPONSE: {json_response}')
        # sys.exit("Just stop for the JSON output.")
        metadata = json_response['data']['findAllMetadata']

        # split response metadata into one response per metadata object
        for meta_obj in metadata:
            response_copy = response.copy()
            response_copy.meta['item'] = meta_obj
            response_copy._set_body(json.dumps(meta_obj))

            # In order to transfer data to CSV/JSON
            yield LomBase.parse(self, response_copy)

    def getBase(self, response):
        # self.item_pos += 1
        # self.log_progress()
        metadata = response.meta['item']

        base = LomBase.getBase(self, response)
        base.add_value('thumbnail', metadata['thumbnail'])
        # ToDo: Do we need it here? Same on line 184.
        base.add_value('origin', 'FWU Institut für Film und Bild in Wissenschaft und Unterricht'
                                 ' gemeinnützige GmbH')

        return base

    def getId(self, response):
        metadata = response.meta['item']
        return metadata['id']

    def getHash(self, response):
        return str(self.version) + str(datetime.datetime.now())

    def mapResponse(self, response):
        r = ResponseItemLoader(response=response)
        r.add_value('status', response.status)
        r.add_value('headers', response.headers)

        return r

    def getLOMEducational(self, response=None):
        educational = LomBase.getLOMEducational(self, response)
        # ToDo: Is this needed furthermore
        educational.add_value('language', 'german')

        return educational

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        metadata = response.meta['item']
        keywords = ['FWU', metadata['title']]

        general.add_value('aggregationLevel', '1')
        general.add_value('title', metadata['title'])
        general.add_value('language', 'german')
        general.add_value('description', metadata['description'])
        general.add_value('keyword', keywords)

        return general

    def getLicense(self, response=None):
        license = LomBase.getLicense(self, response)

        # ToDo: Clarify the official license - copyright
        license.replace_value('internal', Constants.LICENSE_COPYRIGHT_LAW)
        license.replace_value('description', Constants.LICENSE_NONPUBLIC)

        return license

    def getLOMLifecycle(self, response=None) -> LomLifecycleItemloader:
        lifecycle = LomBase.getLOMLifecycle(self, response)

        #ToDo: Ask PO for publisher
        lifecycle.add_value('role', 'publisher')
        lifecycle.add_value('organization', 'FWU Institut für Film und Bild in Wissenschaft und Unterricht'
                                            ' gemeinnützige GmbH')

        return lifecycle

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        #ToDo: Check the right format. Sodix make 'application/pdf'
        technical.add_value('format', 'application/pdf')
        # ToDo: Add location. S3 URL? Looks like the wwwurl.
        technical.add_value('location', '')
        # ToDo: Does it make sense to specify the size?
        # technical.add_value('size', metadata['media']['size'])

        return technical

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        # ToDo: Is this the right learningResourceType? Clarify with PO.
        valuespaces.add_value('learningResourceType', 'http://w3id.org/openeduhub/vocabs/learningResourceType/web_page')

        return valuespaces

    def getLOMAnnotation(self, response=None) -> LomAnnotationItemLoader:
        annotation = LomBase.getLOMAnnotation(self, response)

        annotation.add_value('entity', 'crawler')
        annotation.add_value('description', 'searchable==1')

        return annotation

    def getLOMRelation(self, response=None) -> LomRelationItemLoader:
        relation = LomBase.getLOMRelation(self, response)

        return relation

    def getPermissions(self, response):
        permissions = LomBase.getPermissions(self, response)
        # ToDo: Managed by the permission script. Add it to the script.
        permissions.add_value('autoCreateGroups', True)
        permissions.add_value('groups', ['public'])

        return permissions

    def get_data(self, body: str, class_name: str):
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
        data_definition = ""

        if class_name == "pname":
            data_definition = "Title"
        elif class_name == "ptext":
            data_definition = "Description"

        if result is None or result == "" or result == " ":
            raise RuntimeError(f'{data_definition} not found in class "{class_name}"')


class UnexpectedResponseError(Exception):
    pass
