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


query_string = '''
{
    findAllMetadata(page: 0, pageSize: 50000000) {
        id
        description
        keywords
        language
        learnResourceType
        title
        creationDate
        license {
            name
            text
        }
        publishers {
            linkToGeneralUseRights
            id
            title
        }
        media {
            dataType
            thumbPreview
            url
            size
        }
    }
}
'''


class SodixSpider(CrawlSpider, LomBase):
    """
    This crawler fetches data from the SODIX. The Scrapy request with GraphQL in JSON (please refer to body in parse() function).
    The Response will be convert to python dictionary using json.dumps(). Response.meta['item'] is used in every
    get function to facilitate access to metadata.

    For better understanding, please refer to LOM documentation(http://sodis.de/lom-de/LOM-DE.doc), mediothek_pixiothek_spider.py, merlin_spider.py
    and openduhub / oeh-search-etl in Github(https://github.com/openeduhub/oeh-search-etl/wiki/How-To-build-a-crawler-for-edu-sharing-(alternative-method))

    Author: BRB team
    """

    name = 'sodix_spider'
    url = 'https://www.sodix.de/'
    friendlyName = 'Sodix'
    version = '0.1'
    urlLogin = 'https://api.sodix.de/gql/auth/login'
    urlRequest = 'https://api.sodix.de/gql/graphql'
    user = env.get('SODIX_USER')
    password = env.get('SODIX_PASSWORD')
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
            url=self.urlRequest,
        )

    def login(self):
        response = requests.post(
            self.urlLogin,
            headers={'Content-Type': 'application/json'},
            data=f'{{"login": "{self.user}", "password": "{self.password}"}}'
        )
        try:
            if response.json()['error'] or not response.status_code == 200:
                raise UnexpectedResponseError(f'Unexpected login response: {response.json()}')
            self.access_token = response.json()['access_token']
        except (KeyError, UnexpectedResponseError):
            raise UnexpectedResponseError(f'Unexpected login response: {response.json()}')

    def get_headers(self):
        return {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }

    def get_body(self):
        return json.dumps({'query': query_string})

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
        metadata = response.meta['item']
        if metadata['media'] and metadata['media']['thumbPreview']:
            base.add_value('thumbnail', metadata['media']['thumbPreview'])

        if metadata['publishers']:
            base.add_value('origin', [metadata['publishers'][0]['id']])

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
        metadata = response.meta['item']

        if metadata['language']:
            educational.add_value('language', metadata['language'])

        return educational

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        metadata = response.meta['item']

        general.add_value('aggregationLevel', '1')

        for value in 'title', 'language', 'description':
            if metadata[value]:
                general.add_value(value, metadata[value])

        keywords = []
        if metadata['keywords']:
            keywords.extend(metadata['keywords'])
        for publisher in metadata['publishers']:
            keywords.append(publisher['title'])
        general.add_value('keyword', keywords)

        return general

    def getLicense(self, response=None):
        license = LomBase.getLicense(self, response)
        metadata = response.meta['item']

        if metadata['license']:
            license.replace_value('internal', Constants.LICENSE_CUSTOM)
            license.replace_value('description', f'{metadata["license"]["name"]}; {metadata["license"]["text"]}')

        return license

    def getLOMLifecycle(self, response=None) -> LomLifecycleItemloader:
        lifecycle = LomBase.getLOMLifecycle(self, response)
        metadata = response.meta['item']

        if metadata['publishers']:
            lifecycle.add_value('role', 'publisher')
            lifecycle.add_value('organization', metadata['publishers'][0]['title'])

        return lifecycle

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        metadata = response.meta['item']

        technical.add_value('format', metadata['media']['dataType'])
        technical.add_value('location', metadata['media']['url'])
        technical.add_value('size', metadata['media']['size'])

        return technical

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        metadata = response.meta['item']

        valuespaces.add_value('learningResourceType', metadata['learnResourceType'])

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

        permissions.add_value('autoCreateGroups', True)
        permissions.add_value('groups', ['public'])

        return permissions


class UnexpectedResponseError(Exception):
    pass
