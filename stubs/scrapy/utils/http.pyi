from w3lib.http import *
from scrapy.exceptions import ScrapyDeprecationWarning as ScrapyDeprecationWarning
from scrapy.utils.decorators import deprecated as deprecated
from typing import Any

def decode_chunked_transfer(chunked_body: Any): ...
