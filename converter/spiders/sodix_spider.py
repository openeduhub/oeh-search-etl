import json
import requests
import time

import converter.env as env
from converter.items import *
from converter.spiders.base_classes.lom_base import LomBase
from scrapy.spiders import CrawlSpider

query_string = '''
{
    sources {
        metadata {
            description
            id
            keywords
            language
            learnResourceType
            media {
                dataType
                originalUrl
                size
                thumbPreview
            }
            publishers {
                linkToGeneralUseRights
            }
            title
        }
    }
}
'''


class SodixSpider(CrawlSpider, LomBase):
    """
    This crawler fetches data from the SODIX. The Scrapy request with GraphQL in JSON (please refer to body in parse() function). 
    The Response will be convert to python dictionary using json.dumps(). Response.meta["item"] is used in every
    get function to facilitate access to metadata. 

    For better understanding, please refer to LOM documentation(http://sodis.de/lom-de/LOM-DE.doc), mediothek_pixiothek_spider.py, merlin_spider.py
    and openduhub / oeh-search-etl in Github(https://github.com/openeduhub/oeh-search-etl/wiki/How-To-build-a-crawler-for-edu-sharing-(alternative-method))

    Author: BRB team
    """

    name = "sodix_spider"
    url = "https://www.sodix.de/"  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = "Sodix"  # name as shown in the search ui
    version = "0.1"  # the version of your crawler, used to identify if a reimport is necessary
    urlLogin = "https://api.sodix.de/gql/auth/login"  # * regular expression, to represent all possible values.
    urlRequest = "https://api.sodix.de/gql/graphql"
    user = env.get("SODIX_USER")
    password = env.get("SODIX_PASSWORD")

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)
        self.access_token = ''

    def start_requests(self):
        # self.login()
        self.make_requests()
        return iter(())

    def login(self):
        response = requests.post(
            self.urlLogin,
            headers={'Content-Type': 'application/json'},
            data=f'{{"login": "{self.user}", "password": "{self.password}"}}'
        )
        try:
            self.access_token = response.json()['access_token']
            if not self.access_token:
                raise UnexpectedResponseError()
            print(f'login: {response.status_code}')
        except (KeyError, UnexpectedResponseError):
            raise UnexpectedResponseError(f'Unexpected login response: {response.json()}')

    def get_headers(self):
        return {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
        }

    def make_requests(self):
        response = self.sodix_requests()
        print("weiter---------------------------------------------------------------------------------")
        print(f'make_request_graph: {response.text}')
        self.parse_sodix(response)

    def sodix_requests(self):
        for i in range(10):
            headers = self.get_headers()
            body = json.dumps({"query": query_string})

            response = requests.post(self.urlRequest, headers=headers, data=body)
            print(f'make_request_graph: {response.status_code}')
            # TODO: error handling (401, etc.)
            if response.status_code==401:
                self.login()
                continue
            return response

    # to access sodix with access_token
    def parse_sodix(self, response: requests.Response):
        print("Start pare_sodix-----------------------------------------------------------------------------------------")
        # TODO: make independent from scrapy (response)
        elements = json.loads(response.body.decode('utf-8'))
        requestCount = len(elements['data']['sources'])

        for i in range(requestCount):
            # for debugging
            if i == 1:
                print('dev-mode : 1 requests done, exiting...')
                break
            for j in range(len(elements['data']['sources'][i]['metadata'])):

                copyResponse = response.copy()
                copyResponse.meta["item"] = elements['data']['sources'][i]['metadata'][j]

                json_str = json.dumps(elements['data']['sources'][i]['metadata'][j], indent=4, sort_keys=True,
                                      ensure_ascii=False)

                copyResponse._set_body(json_str)

                # In order to transfer data to CSV/JSON, implement these 2 lines.
                if self.hasChanged(copyResponse):
                    yield LomBase.parse(self, copyResponse)

                # to call LomBase functions
                LomBase.parse(self, copyResponse)
            print('Finish parsing: ' + str(i + 1) + '/' + str(requestCount))

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        metadata = response.meta["item"]

        base.add_value("thumbnail", metadata['media']['thumbPreview'])

        return base

    def getId(self, response):
        metadata = response.meta["item"]

        return metadata['id']

    def getHash(self, response):

        return hash(str(self.version) + str(time.time()))

    def mapResponse(self, response):
        r = ResponseItemLoader(response=response)
        r.add_value("status", response.status)
        r.add_value("headers", response.headers)
        r.add_value("url", response.url)

        return r

    def getLOMEducational(self, response=None):
        educational = LomBase.getLOMEducational(self, response)
        metadata = response.meta["item"]

        educational.add_value("language", metadata['language'])

        return educational

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        metadata = response.meta["item"]

        general.add_value("aggregationLevel", "1")
        general.add_value("identifier", metadata['id'])
        general.add_value("title", metadata['title'])
        general.add_value("keyword", metadata['keywords'])
        general.add_value("language", metadata['language'])
        general.add_value("description", metadata['description'])

        return general

    def getLicense(self, response=None):
        license = LomBase.getLicense(self, response)
        metadata = response.meta["item"]

        for i in range(len(metadata['publishers'])):
            license.add_value("description", metadata['publishers'][i]['linkToGeneralUseRights'])

        return license

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        metadata = response.meta["item"]

        technical.add_value("format", metadata['media']['dataType'])
        technical.add_value("location", metadata['media']['originalUrl'])
        technical.add_value("size", metadata['media']['size'])

        return technical

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        metadata = response.meta["item"]

        valuespaces.add_value("learningResourceType", metadata['learnResourceType'])

        return valuespaces

    # TODO
    def getPermissions(self, response):
        permissions = LomBase.getPermissions(self, response)

        return permissions

    # TODO
    def getLOMAnnotation(self, response=None) -> LomAnnotationItemLoader:
        annotation = LomBase.getLOMAnnotation(self, response)
        # metadata  = response.meta["item"]

        # Adding a default searchable value to constitute this element (node) as a valid-to-be-returned object.
        annotation.add_value("entity", "crawler")
        annotation.add_value("description", "searchable==0")

        return annotation

    # TODO
    def getLOMRelation(self, response=None) -> LomRelationItemLoader:
        relation = LomBase.getLOMRelation(self, response)

        return relation


class UnexpectedResponseError(Exception):
    pass
