# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json
from wsgiref.util import request_uri
from regex import R
from scrapy import signals

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from scrapy.exceptions import IgnoreRequest

class OerScrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class OerScrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

# documentation for retry https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.retry
class CustomRetryMiddleware(RetryMiddleware):


    def __init__(self, spider, settings):
        self.spider_name = spider.name
        #self.settings = settings
        super(CustomRetryMiddleware, self).__init__(settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.spider, crawler.settings)
        
    def process_response(self, request, response, spider):
        print("{s} is processing stuff".format(s=self.spider_name))
        
        # HTTP response codes to retry. Default : [500, 502, 503, 504, 522, 524, 408, 429] 
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        elif response.status == 401:
            if response.url != 'https://api.sodix.de/gql/graphql':
                raise IgnoreRequest()
            print(f'counter in middleware : {spider.counter}\nresponse : {response.status}')
            
            spider.counter += 1
            request.headers = spider.get_headers(spider.counter)
            print(request.headers)
            # request.headers = {
            #     'Authorization': 'Bearer ' + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtleUlkIn0.eyJ1c2VyX25hbWUiOiJicmItc29kaXgiLCJzY29wZSI6WyJhbGwiXSwiYXRpIjoiZVVHTWRfTS1GT0c5c3NzUzNWNnYzSW5OYUlzIiwiZXhwIjoxNjUzNDc5MjUyLCJ1c2VyIjp7ImlkIjoiNjI0NWEzNzhhMTYwZGQ2ZDcxZTM5MDY1IiwidXNlcm5hbWUiOiJicmItc29kaXgiLCJmaXJzdE5hbWUiOiJCUkIiLCJsYXN0TmFtZSI6IlNvZGl4IiwiZW1haWwiOiJkZXZvcHNAZGJpbGR1bmdzY2xvdWQuZGUiLCJyb2xlcyI6WyJST0xFX0FQSSJdLCJlbmFibGVkIjp0cnVlLCJjdXJyZW50VGVuYW50Ijp7ImtleSI6Im5iYyIsIm5hbWUiOiJOQkMiLCJlbWFpbCI6ImZ3dUBnbWFpbC5jb20ifSwidGVuYW50cyI6W3sia2V5IjoibmJjIiwibmFtZSI6Ik5CQyIsImVtYWlsIjoiZnd1QGdtYWlsLmNvbSJ9XX0sImF1dGhvcml0aWVzIjpbIlJPTEVfQVBJIl0sImp0aSI6ImFoamNSaXhNM2o3MzJ6SnExZnd4MnhaNEM1byIsImNsaWVudF9pZCI6InNvZGl4In0.ixkXe4Fp8O6_nwCoimqpyfwuaoehieB1o60n6gsCmLZW2AxfxmTKyPbfnojUK2NJPwVxFmBIfskSkxthLuU2OLngzxl_n9hpm-NDby_mbmenS_Tr-xXN2SSiaR2q6sxRPejHGN9MeC1PLKw5Kawj12GO2n9PJX4qx_qkxLSHS-A3gPUcXSigOwCFHFiP9kNDNCLHTfFyXDCYbxX-t5BebkBL6Alci0nakJ6cMWp88rQYRT5mSdpHt21AIzbv8Q_KG2onbQEmiJ7lMdHGJapCLnbLRPKknQ9lxm_z8iJxgsmaN20JJDJF9dj2-YGqjbcR8X_bUF0Of0ehkj64v90YyA",
            #     'Content-Type': 'application/json'
            # }

            return self._retry(request, 'response.status:{}'.format(response.status), spider) or response
            
        elif response.status ==200:
            print("success")
            return response

        return response
    
    def process_exception(self, request, exception, spider):
        print("process_exception")  
        pass

    def spider_opened(self, spider):
        self.spider_name = spider.name
        spider.logger.info("Spider opened: %s" % spider.name)


