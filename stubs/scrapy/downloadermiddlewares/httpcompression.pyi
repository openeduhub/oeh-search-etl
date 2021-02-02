from scrapy.exceptions import NotConfigured as NotConfigured
from scrapy.http import Response as Response, TextResponse as TextResponse
from scrapy.responsetypes import responsetypes as responsetypes
from scrapy.utils.gz import gunzip as gunzip
from typing import Any

ACCEPTED_ENCODINGS: Any

class HttpCompressionMiddleware:
    @classmethod
    def from_crawler(cls, crawler: Any): ...
    def process_request(self, request: Any, spider: Any) -> None: ...
    def process_response(self, request: Any, response: Any, spider: Any): ...
