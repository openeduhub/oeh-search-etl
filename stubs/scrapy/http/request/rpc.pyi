from scrapy.http.request import Request as Request
from scrapy.utils.python import get_func_args as get_func_args
from typing import Any

DUMPS_ARGS: Any

class XmlRpcRequest(Request):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
