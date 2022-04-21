import ast
from email.quoprimime import body_check
import json
import time
from types import SimpleNamespace
import xmltodict as xmltodict
from lxml import etree
from scrapy.spiders import CrawlSpider
import scrapy as scrapy
from converter.constants import Constants
from converter.items import *
from converter.spiders.base_classes.lom_base import LomBase


class SodixSpider(CrawlSpider, LomBase):
    """
    This crawler fetches data from the Merlin content source, which provides us paginated XML data. For every element
    in the returned XML array we call LomBase.parse(), which in return calls methods, such as getId(), getBase() etc.

    Author: BRB team
    """

    name            = "sodix_spider"
    url             = "https://www.sodix.de/"  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName    = "Sodix"  # name as shown in the search ui
    version         = "0.1"  # the version of your crawler, used to identify if a reimport is necessary
    apiUrl          = "https://api.sodix.de/gql/auth/login"  # * regular expression, to represent all possible values.
    apiUrl2         = "https://api.sodix.de/gql/graphql"

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)
        #OAIBase.__init__(self, **kwargs)
        
    def open_json(self) :
        with open('/home/leicheng/schulcloud/oeh-search-etl/credentials.json') as f:
            data = json.load(f)
        return data

    # login into sodix page, then call parse function. 
    def start_requests(self):    
        yield scrapy.Request(
                                url      = self.apiUrl,
                                callback = self.parse,
                                method   = 'POST',
                                headers  = { 'Content-Type': 'application/json' },
                                body     = json.dumps(self.open_json())
                            )

    # access sodix database by using access_token only since it has 8 hours of TTL    
    def parse(self, response: scrapy.http.Response):
        # print(  "Parsing URL  :" + response.url,
        #       "\nStatus       :" ,response.status,
        #       "\nresponse.body:" ,response.body ) 
        json_response_body = json.loads(response.body) if response.status==200 else print("LOGIN ERROR")

        # check tokens
        # for x in json_response_body:
        #     print("%s: %s" % (x, json_response_body[x]))
        
        access_token = str(json_response_body['access_token'])
        headers      = { 
                         'Authorization':'Bearer ' + access_token,
                         'Content-Type' : 'application/json'
                       } # dict
        body         = json.dumps({"query":
                                        "{\n sources { id\n name\n created\n metadata { description\n keywords\n language\n learnResourceType\n media { thumbPreview\n } publishers { linkToGeneralUseRights\n } title\n } }\n}"})
        yield scrapy.Request(
                                url      = self.apiUrl2,
                                callback = self.parse_sodix,
                                method   = 'POST',
                                headers  = headers,
                                body     = body   
                            )   

    def getId(self, response) :
        return response.url

    def getHash(self, response): 
        return str(self.version)+str(time.time())

    def getBase(self, response):
        print("sodix_spider : getBase\n")
        base = LomBase.getBase(self, response)
        x    = json.loads(response.body, object_hook=lambda d: SimpleNamespace(**d))
        for i in range(len(x.data.sources)):
            for j in range(len(x.data.sources[i].metadata)):
                base.add_value("thumbnail", x.data.sources[i].metadata[j].media.thumbPreview)
        return base   
    
    # to access sodix with access_token
    def parse_sodix(self, response):
        #json_response_body = json.loads(response.body)
        #data = json.loads(response.body, object_hook=lambda d: SimpleNamespace(**d))
        print("sodix_spider : parse_sodix\n")
        lom = LomBase.parse(self,response)
        return lom
       
 
    def getLOMGeneral(self, response):
        print("sodix_spider : getLOMGeneral\n")
        general = LomBase.getLOMGeneral(self, response)
        x       = json.loads(response.body, object_hook=lambda d: SimpleNamespace(**d))

        for i in range(len(x.data.sources)):
            for j in range(len(x.data.sources[i].metadata)):
           
                general.add_value("identifier", x.data.sources[i].id)
                general.add_value("title", x.data.sources[i].metadata[j].title)
                general.add_value("keyword", x.data.sources[i].metadata[j].keywords)
                general.add_value("language", x.data.sources[i].metadata[j].language)
                general.add_value("description",x.data.sources[i].metadata[j].description)

        return general
    
    # def getLOMTechnical(self, response):
    #     print("sodix_spider : getLOMTechnical\n")
    #     technical = LomBase.getLOMTechnical(response)
       
    #     x = json.loads(response.body, object_hook=lambda d: SimpleNamespace(**d))
    #     for i in range(len(x.data.sources)):
    #         for j in range(len(x.data.sources[i].metadata)):
    #             #size is in int
    #             #technical.add_value("size", x.data.sources[i].metadata[j].size)
    #             #duration is null
    #             #technical.add_value( "duration",x.data.sources[i].metadata[j].duration)

    #     return technical

    def getLOMEducational(self, response=None):
        print("sodix_spider : getLomEducation\n")
        educational = LomBase.getLOMEducational(response)
        x           = json.loads(response.body, object_hook=lambda d: SimpleNamespace(**d))
        
        for i in range(len(x.data.sources)):
            for j in range(len(x.data.sources[i].metadata)):
                educational.add_value("description", x.data.sources[i].metadata[j].description)
                educational.add_value("language", x.data.sources[i].metadata[j].language)
        return educational
    
    def getLicense(self, response=None):
        print("sodix_spider : getLicense\n")
        license = LomBase.getLicense(self, response)
        x       = json.loads(response.body, object_hook=lambda d: SimpleNamespace(**d))
        
        for i in range(len(x.data.sources)):
            for j in range(len(x.data.sources[i].metadata)):
                license.add_value("description", x.data.sources[i].metadata[j].publishers.linkToGeneralUseRights)
        return license

    def getValuespaces(self, response):
        print("sodix_spider : getValuespaces\n")
        valuespaces = LomBase.getValuespaces(self, response)
        x           = json.loads(response.body, object_hook=lambda d: SimpleNamespace(**d))
        
        for i in range(len(x.data.sources)):
            for j in range(len(x.data.sources[i].metadata)):
                valuespaces.add_value("learningResourceType", x.data.sources[i].metadata[j].learnResourceType)

        return valuespaces
    
