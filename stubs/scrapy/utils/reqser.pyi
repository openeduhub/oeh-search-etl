from scrapy.http import Request as Request
from scrapy.utils.misc import load_object as load_object
from scrapy.utils.python import to_unicode as to_unicode
from typing import Any, Optional

def request_to_dict(request: Any, spider: Optional[Any] = ...): ...
def request_from_dict(d: Any, spider: Optional[Any] = ...): ...
