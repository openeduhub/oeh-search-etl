from scrapy.commands import ScrapyCommand as ScrapyCommand
from scrapy.crawler import CrawlerProcess as CrawlerProcess
from scrapy.exceptions import UsageError as UsageError
from scrapy.utils.misc import walk_modules as walk_modules
from scrapy.utils.project import get_project_settings as get_project_settings, inside_project as inside_project
from scrapy.utils.python import garbage_collect as garbage_collect
from typing import Any, Optional

def execute(argv: Optional[Any] = ..., settings: Optional[Any] = ...) -> None: ...
