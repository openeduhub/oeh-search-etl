from scrapy.responsetypes import responsetypes as responsetypes
from typing import Any

logger: Any

class DecompressionMiddleware:
    def __init__(self) -> None: ...
    def process_response(self, request: Any, response: Any, spider: Any): ...
