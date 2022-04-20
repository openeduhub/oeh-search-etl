from scrapy.spiders import CrawlSpider
import time
from .base_classes import LomBase
import converter.env as env
import scrapy as scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


# Sample Spider, using a SitemapSpider to crawl your web page
# Can be used as a template for your custom spider
class SodixSpider(CrawlSpider, LomBase):
    name = "sodix_spider"
    url = "https://edu-sharing.com"  # the url which will be linked as the primary link to your source (should be the main url of your site)
    friendlyName = "Sodix"  # name as shown in the search ui
    apiUrl = "https://api.sodix.de/gql/auth/login"
    version = "0.2"  # the version of your crawler, used to identify if a reimport is necessary

    access_token="null"
    user=env.get("SODIX_USER")
    password=env.get("SODIX_PASSWORD")

    def __init__(self, **kwargs):
        LomBase.__init__(self, **kwargs)

    def start_requests(self):
        yield scrapy.http.Request(
            url=self.apiUrl,
            callback=self.parse_sodix,
            method="POST",
            errback=self.errback_sodix,
            headers={
                "Content-Type": "application/json",
            },
            body="{\"login\": \""+self.user+"\",\"password\": \""+self.password+"\"}"
        )

    def parse_sodix(self, response):
        full_response=response.body
        print(full_response)
        self.access_token=str(full_response).split("\"")[3]
        self.access_token="Bearer "+self.access_token
        print(self.access_token)
            #  Timer 5m
        yield scrapy.http.Request(
            url="https://api.sodix.de/gql/graphql",
            callback=self.parse_sodix_end,
            method="POST",
            errback=self.errback_sodix,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.access_token,
                },
            body="{\"query\": \"{sources{id,name}}\"}"
        )

    def parse_sodix_end(self, response):
        full_response=response.body
        print(full_response)
        print(self.access_token)
        self.logger.error('>>>>>>>>>>>>Ende<<<<<<<<<<<<<<')

    def get_new_token(self, response):
        yield scrapy.http.Request(
            url=self.apiUrl,
            callback=self.parse_sodix,
            method="POST",
            errback=self.errback_sodix,
            headers={
                "Content-Type": "application/json",
            },
            body="{\"login\": \""+self.user+"\",\"password\": \""+self.password+"\"}"
        )

    def errback_sodix(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

    def parse(self, response):
        return LomBase.parse(self, response)

    # return a (stable) id of the source
    def getId(self, response):
        return response.xpath("//title//text()").get()

    # return a stable hash to detect content changes
    # if there is no hash available, may use the current time as "always changing" info
    # Please include your crawler version as well
    def getHash(self, response):
        return self.version + time.time()

    def getBase(self, response):
        base = LomBase.getBase(self, response)
        # optionally provide thumbnail. If empty, it will tried to be generated from the getLOMTechnical 'location' (if format is 'text/html')
        # base.add_value('thumbnail', 'https://url/to/thumbnail')
        return base

    def getLOMGeneral(self, response):
        general = LomBase.getLOMGeneral(self, response)
        general.add_value("title", response.xpath("//title//text()").get())
        general.add_value(
            "language", response.xpath('//meta[@property="og:locale"]/@content').get()
        )
        return general

    def getLOMTechnical(self, response):
        technical = LomBase.getLOMTechnical(self, response)
        technical.add_value("location", response.url)
        technical.add_value("format", "text/html")
        technical.add_value("size", len(response.body))
        return technical

    def getValuespaces(self, response):
        valuespaces = LomBase.getValuespaces(self, response)
        # Provide valuespace data. This data will later get automatically mapped
        # Please take a look at the valuespaces here:
        # https://vocabs.openeduhub.de/
        # You can either use full identifiers or also labels. The system will auto-map them accordingly

        # Please also checkout the ValuespaceHelper class which provides usefull mappers for common data

        # valuespaces.add_value('educationalContext', context)
        # valuespaces.add_value('discipline',discipline)
        # valuespaces.add_value('learningResourceType', lrt)
        return valuespaces

    # You may override more functions here, please checkout LomBase class