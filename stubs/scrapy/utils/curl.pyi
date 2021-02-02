import argparse
from typing import Any

class CurlParser(argparse.ArgumentParser):
    def error(self, message: Any) -> None: ...

curl_parser: Any
safe_to_ignore_arguments: Any

def curl_to_request_kwargs(curl_command: Any, ignore_unknown_options: bool = ...): ...
