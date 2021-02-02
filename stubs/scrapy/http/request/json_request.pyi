from scrapy.http.request import Request as Request
from scrapy.utils.deprecate import create_deprecated_class as create_deprecated_class
from typing import Any

class JsonRequest(Request):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def replace(self, *args: Any, **kwargs: Any): ...

JSONRequest: Any
