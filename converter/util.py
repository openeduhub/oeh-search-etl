import logging
import time
from functools import wraps

log = logging.getLogger(__name__)
ee_log_prefix = f'{__name__}.entry_exit'
ee_log = logging.getLogger(f'{ee_log_prefix}')


def async_entry_exit_log(f, entry_char, exit_char):
    @wraps(f)
    async def wrapper(*args, **kwds):
        ee_log.info(entry_char)
        result = await f(*args, **kwds)
        ee_log.info(exit_char)
        return result
    return wrapper


def entry_exit_log(f, entry_char, exit_char):
    @wraps(f)
    def wrapper(*args, **kwds):
        ee_log.info(entry_char)
        result = f(*args, **kwds)
        ee_log.info(exit_char)
        return result
    return wrapper


def timed(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time.monotonic()
        f(*args, **kwds)
        end = time.monotonic()
        diff = end - start
        if diff > 2:
            logging.error(f"""WARNING!
            call to {f.__name__} took {diff:.2f}:
            args: {args}
            kwargs: {kwds}
            """)
    return wrapper


def async_timed(f):
    @wraps(f)
    async def wrapper(*args, **kwds):
        start = time.monotonic()
        result = await f(*args, **kwds)
        end = time.monotonic()
        diff = end - start
        if diff > 2:
            log.error(f"""WARNING!
            call to {f.__name__} took {diff:.2f}:
            args: {args}
            kwargs: {kwds}
            """)
        return result
    return wrapper
