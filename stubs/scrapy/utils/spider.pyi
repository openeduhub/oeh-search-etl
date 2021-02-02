from scrapy.spiders import Spider as Spider
from scrapy.utils.defer import deferred_from_coro as deferred_from_coro
from scrapy.utils.misc import arg_to_iter as arg_to_iter
from scrapy.utils.py36 import collect_asyncgen as collect_asyncgen
from typing import Any, Optional

logger: Any

def iterate_spider_output(result: Any): ...
def iter_spider_classes(module: Any) -> None: ...
def spidercls_for_request(spider_loader: Any, request: Any, default_spidercls: Optional[Any] = ..., log_none: bool = ..., log_multiple: bool = ...): ...

class DefaultSpider(Spider):
    name: str = ...
