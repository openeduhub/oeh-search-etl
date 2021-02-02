from scrapy.http import TextResponse as TextResponse
from scrapy.responsetypes import responsetypes as responsetypes
from scrapy.utils.decorators import defers as defers
from typing import Any

class DataURIDownloadHandler:
    lazy: bool = ...
    def download_request(self, request: Any, spider: Any): ...
