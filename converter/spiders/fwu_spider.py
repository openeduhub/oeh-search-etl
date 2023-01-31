import json
import datetime
import time

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

    name = 'fwu_spider'
    friendlyName = 'FWU'
    version = '0.1'
    s3_url = env.get('S3_ENDPOINT_URL')
    s3_access_key = env.get('S3_ACCESS_KEY')
    s3_secret_key = env.get('S3_SECRET_KEY')
    download_delay = float(env.get('SODIX_DOWNLOAD_DELAY', default='0.5'))  # don't stress sodix image server

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)
        self.access_token = ''
        self.retry_counter = 0
        self.start_time = 0.0
        self.item_pos = 0
        self.item_count = 0

    def start_requests(self):
        self.start_time = time.time()
        self.login()
        yield self.make_request()

    def make_request(self):
        return scrapy.Request(
            body=self.get_body(),
            callback=self.parse_sodix,
            dont_filter=True,
            errback=lambda failure: self.errback_error(failure, self.make_request),
            headers=self.get_headers(),
            method='POST',
            url=self.s3_url,
        )

    def login(self):
        #ToDo: Check login for S3
        response = requests.post(
            self.s3_url,
            headers={'Content-Type': 'application/json'},
            data=f'{{"access_key": "{self.s3_access_key}", "secret_key": "{self.s3_secret_key}"}}'
        )
        try:
            if response.json()['error'] or not response.status_code == 200:
                raise UnexpectedResponseError(f'Unexpected login response: {response.json()}')
            self.access_token = response.json()['access_token']
        except (KeyError, UnexpectedResponseError):
            raise UnexpectedResponseError(f'Unexpected login response: {response.json()}')

    def get_headers(self):
        # ToDo: Check header for S3 login
        return {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }

    def get_body(self):
        #ToDo: Add body for S3 login

        # return json.dumps({'query': query_string})
        pass

    def log_progress(self):
        def seconds_to_str(t: float):
            sec = int(t) % 60
            min = int(t / 60) % 60
            hours = int(t / 3600) % 24
            days = int(t / 3600 / 24)
            s = f'{min:02}:{sec:02}'
            if days:
                s = f'{days:02}:{hours:02}:{s}'
            elif hours:
                s = f'{hours:02}:{s}'
            return s
        percentage = f'{int(self.item_pos / self.item_count * 100)}%'
        absolute = f'{self.item_pos} / {self.item_count}'
        elapsed = time.time() - self.start_time
        remaining = (self.item_count - self.item_pos) / self.item_pos * elapsed
        self.logger.info(f'Progress: |{percentage :^6}|{absolute:^18}|{seconds_to_str(elapsed):^14}|{seconds_to_str(remaining):^14}|')

    def errback_error(self, failure, make_request_method):
        if failure.check(HttpError) and self.retry_counter < 3:
            self.retry_counter += 1
            self.logger.warning(f'Re-login ({self.retry_counter}) ...')
            self.login()
            yield make_request_method()

    def parse_sodix(self, response: scrapy.http.Response):
        json_response = json.loads(response.body.decode())
        metadata = json_response['data']['findAllMetadata']
        self.item_count = len(metadata)

        #ToDo: Add html_parser and summarize in one object.

        # split response metadata into one response per metadata object
        for meta_obj in metadata:
            response_copy = response.copy()
            response_copy.meta['item'] = meta_obj
            response_copy._set_body(json.dumps(meta_obj))

            # In order to transfer data to CSV/JSON
            yield LomBase.parse(self, response_copy)

    def getBase(self, response):
        self.item_pos += 1
        self.log_progress()

        base = LomBase.getBase(self, response)

        #ToDo: Add html_parser for thumbnail
        base.add_value('thumbnail', '')

        #ToDo: Do we need it here? Same on line 184.
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
        #ToDo: Is this needed furthermore
        educational.add_value('language', 'german')

        return educational

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        #ToDo: Add html_parser here
        title = ''
        description = ''
        keywords = ['FWU', title]

        general.add_value('aggregationLevel', '1')
        general.add_value('title', title)
        general.add_value('language', 'german')
        general.add_value('description', description)
        general.add_value('keyword', keywords)

        return general

    def getLicense(self, response=None):
        license = LomBase.getLicense(self, response)

        #ToDo: Clarify the official license - copyright
        license.replace_value('internal', Constants.LICENSE_COPYRIGHT_LAW)
        license.replace_value('description', Constants.LICENSE_NONPUBLIC)

        return license

    def getLOMLifecycle(self, response=None) -> LomLifecycleItemloader:
        lifecycle = LomBase.getLOMLifecycle(self, response)

        lifecycle.add_value('role', 'publisher')
        lifecycle.add_value('organization', 'FWU Institut für Film und Bild in Wissenschaft und Unterricht'
                                                ' gemeinnützige GmbH')

        return lifecycle

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)

        technical.add_value('format', 'video/mp4')
        #ToDo: Add location. S3 URL? Looks like the wwwurl.
        technical.add_value('location', '')
        #ToDo: Does it make sense to specify the size?
        #technical.add_value('size', metadata['media']['size'])

        return technical

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        #ToDo: Is this the right learningResourceType? Clarify with PO.
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
        #ToDo: Add Brandenburg or is it managed by the permission script?
        permissions.add_value('autoCreateGroups', True)
        permissions.add_value('groups', ['public'])

        return permissions


class UnexpectedResponseError(Exception):
    pass
