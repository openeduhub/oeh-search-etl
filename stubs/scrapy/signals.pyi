from typing import Any

engine_started: Any
engine_stopped: Any
spider_opened: Any
spider_idle: Any
spider_closed: Any
spider_error: Any
request_scheduled: Any
request_dropped: Any
request_reached_downloader: Any
request_left_downloader: Any
response_received: Any
response_downloaded: Any
bytes_received: Any
item_scraped: Any
item_dropped: Any
item_error: Any
stats_spider_opened = spider_opened
stats_spider_closing = spider_closed
stats_spider_closed = spider_closed
item_passed = item_scraped
request_received = request_scheduled
