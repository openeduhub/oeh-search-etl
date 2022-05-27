import json
import random

import requests
import scrapy.http
import datetime
import converter.env as env
from converter.constants import Constants
from converter.items import *
from converter.spiders.base_classes.lom_base import LomBase
from scrapy.spiders import CrawlSpider
from scrapy.spidermiddlewares.httperror import HttpError

query_string = '''
{
    findAllMetadata(page: 0, pageSize: 4) {
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
    '''
    This crawler fetches data from the SODIX. The Scrapy request with GraphQL in JSON (please refer to body in parse() function).
    The Response will be convert to python dictionary using json.dumps(). Response.meta['item'] is used in every
    get function to facilitate access to metadata.

    For better understanding, please refer to LOM documentation(http://sodis.de/lom-de/LOM-DE.doc), mediothek_pixiothek_spider.py, merlin_spider.py
    and openduhub / oeh-search-etl in Github(https://github.com/openeduhub/oeh-search-etl/wiki/How-To-build-a-crawler-for-edu-sharing-(alternative-method))

    Author: BRB team
    '''

    name = 'sodix_spider'
    url = 'https://www.sodix.de/'  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = 'Sodix'  # name as shown in the search ui
    version = '0.1'  # the version of your crawler, used to identify if a reimport is necessary
    urlLogin = 'https://api.sodix.de/gql/auth/login'  # * regular expression, to represent all possible values.
    urlRequest = 'https://api.sodix.de/gql/graphql'
    user = env.get('SODIX_USER')
    password = env.get('SODIX_PASSWORD')
    counter = 1
    loginStatusCode = None

    # reference : https://stackoverflow.com/questions/62061219/use-a-specific-scrapy-downloader-middleware-per-request
    # custom_settings = {
    #     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    #     'DOWNLOADER_MIDDLEWARES': {'converter.middlewares.CustomRetryMiddleware' : 543},
    # }

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)
        self.access_token = ''

    def start_requests(self):
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
        self.loginStatusCode = response.status_code
        try:
            if not response.json()['error']:
                self.access_token = response.json()['access_token']
                self.logger.info('access token is available')
            else:
                self.logger.error('The login was not successful')
                raise UnexpectedResponseError(f'Unexpected login response: {response.json()}')
        except (KeyError, UnexpectedResponseError):
            raise UnexpectedResponseError(f'Unexpected login response: {response.json()}')

    def getLoginRepsonseStatusCode(self):
        return self.loginStatusCode

    def get_headers(self):
        return {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }

    def get_body(self):
        return json.dumps({'query': query_string})

    def errback_error(self, failure, method):
        if failure.check(HttpError) and self.counter < 3:
            response = failure.value.response
            self.logger.error(f'HTTP error retry login counts : {self.counter}')
            self.counter += 1
            self.logger.error('HTTP Error on %s', response.status)
            self.login()
            yield method()

    # to access sodix with access_token
    def parse_sodix(self, response: scrapy.http.Response):
        json_response = json.loads(response.body.decode())
        metadata = json_response['data']['findAllMetadata']

        # split response metadata into one response per metadata object
        for meta_obj in metadata:
            response_copy = response.copy()
            response_copy.meta['item'] = meta_obj
            response_copy._set_body(json.dumps(meta_obj))

            # In order to transfer data to CSV/JSON, implement these 2 lines.
            yield LomBase.parse(self, response_copy)

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        metadata = response.meta['item']

        base.add_value('thumbnail', metadata['media']['thumbPreview'])
        base.add_value('origin', metadata['publishers'][0]['id'])

        return base

    def getId(self, response):
        metadata = response.meta['item']
        return metadata['id']

    def getHash(self, response):
        return hash(str(self.version) + str(datetime.datetime.now()))

    def mapResponse(self, response):
        r = ResponseItemLoader(response=response)
        r.add_value('status', response.status)
        r.add_value('headers', response.headers)

        return r

    def getLOMEducational(self, response=None):
        educational = LomBase.getLOMEducational(self, response)
        metadata = response.meta['item']

        educational.add_value('language', metadata['language'])

        return educational

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        metadata = response.meta['item']

        general.add_value('aggregationLevel', '1')
        general.add_value('title', metadata['title'])
        general.add_value('keyword', metadata['keywords'] + [metadata['publishers'][0]['title']])
        general.add_value('language', metadata['language'])
        general.add_value('description', metadata['description'])

        return general

    def getLicense(self, response=None):
        license = LomBase.getLicense(self, response)

        try:
            # license.add_value('internal', metadata['license']['name'])
            license.replace_value('internal', Constants.LICENSE_COPYRIGHT_LAW)
        except TypeError:
            self.logger.info('Metadata LicenceName is None.')
            license.add_value('internal', 'None')

        # try:
        #     license.add_value('internal', metadata['license']['text'])
        # except TypeError:
        #     self.logger.info('Metadata LicenceText is None.')
        #     license.add_value('description', 'None')

        return license

    def getLOMLifecycle(self, response=None) -> LomLifecycleItemloader:
        lifecycle = LomBase.getLOMLifecycle(self, response)
        metadata = response.meta['item']

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

        # metadata = response.meta['item']
        #
        # resource = LomRelationResourceItem()
        # resource['identifier'] = metadata['id']
        # relation.add_value('resource', resource)

        return relation

    # refer to getPermissions in mediothek_pixiothek
    def getPermissions(self, response):
        permissions = LomBase.getPermissions(self, response)

        #permissions.replace_value("public", False)
        permissions.add_value('autoCreateGroups', True)
        #permissions.add_value('groups', ['public'])
        permissions.add_value('groups', ['Brandenburg'])
        permissions.add_value('groups', ['Niedersachsen'])
        permissions.add_value('groups', ['Thueringen'])

        return permissions


class UnexpectedResponseError(Exception):
    pass
