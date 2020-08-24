import os
import sys
from dotenv import load_dotenv
from typing import NoReturn

load_dotenv()


def get(key: str, allow_null: bool = False, default: str = None) -> str:
    """
    Get environment variable by key.

    Exits on undefined variable unless either `allow_null` or `default` is set.
    """
    value = os.getenv(key, default)
    if value != None:
        return value
    elif allow_null:
        return None
    else:
        _fail_on_missing_key(key)


def get_bool(key: str, allow_null: bool = False, default: bool = None) -> bool:
    value = os.getenv(key)
    if value != None:
        if value.lower() in ["true", "1", "yes"]:
            return True
        elif value.lower() in ["false", "0", "no"]:
            return False
        else:
            raise RuntimeError(
                "Failed to parse value for boolean variable {}: {}".format(key, value)
            )
    if default != None:
        return default
    elif allow_null:
        return None
    else:
        _fail_on_missing_key(key)


def _fail_on_missing_key(key: str) -> NoReturn:
    print("No configuration for key {} was found in your .env file.".format(key))
    print("Please refer to the .env.example file for a sample value.")
    sys.exit(1)
