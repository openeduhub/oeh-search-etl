from scrapy.middleware import MiddlewareManager as MiddlewareManager
from scrapy.utils.conf import build_component_list as build_component_list
from scrapy.utils.defer import mustbe_deferred as mustbe_deferred
from scrapy.utils.python import MutableChain as MutableChain
from typing import Any

class SpiderMiddlewareManager(MiddlewareManager):
    component_name: str = ...
    def scrape_response(self, scrape_func: Any, response: Any, request: Any, spider: Any): ...
    def process_start_requests(self, start_requests: Any, spider: Any): ...
