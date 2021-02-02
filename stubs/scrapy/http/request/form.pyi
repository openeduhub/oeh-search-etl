from scrapy.http.request import Request as Request
from scrapy.utils.python import is_listlike as is_listlike, to_bytes as to_bytes
from scrapy.utils.response import get_base_url as get_base_url
from typing import Any, Optional

class FormRequest(Request):
    valid_form_methods: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @classmethod
    def from_response(cls, response: Any, formname: Optional[Any] = ..., formid: Optional[Any] = ..., formnumber: int = ..., formdata: Optional[Any] = ..., clickdata: Optional[Any] = ..., dont_click: bool = ..., formxpath: Optional[Any] = ..., formcss: Optional[Any] = ..., **kwargs: Any): ...
