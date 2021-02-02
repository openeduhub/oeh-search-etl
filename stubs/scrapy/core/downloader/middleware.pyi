from scrapy.http import Request as Request, Response as Response
from scrapy.middleware import MiddlewareManager as MiddlewareManager
from scrapy.utils.conf import build_component_list as build_component_list
from scrapy.utils.defer import deferred_from_coro as deferred_from_coro, mustbe_deferred as mustbe_deferred
from typing import Any

class DownloaderMiddlewareManager(MiddlewareManager):
    component_name: str = ...
    def download(self, download_func: Any, request: Any, spider: Any): ...
