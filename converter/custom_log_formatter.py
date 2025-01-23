import logging
import os

from loguru import logger
from scrapy.logformatter import LogFormatter


class CustomLogFormatter(LogFormatter):
    DROPPEDMSG = "Dropped: %(exception)s" + os.linesep + "%(item)s"
    ITEMERRORMSG = "Error processing %(item)s"

    def dropped(self, item, exception, response, spider):
        """Logs a message when an item is dropped while it is passing through the item pipeline."""
        return {
            "level": logging.WARNING,
            "msg": self.DROPPEDMSG,
            "args": {"exception": exception, "item": item["lom"],},
        }

    def item_error(self, item, exception, response, spider):
        """Logs a message when an item causes an error while it is passing
            through the item pipeline.

            .. versionadded:: 2.0
            """
        return {
            "level": logging.ERROR,
            "msg": self.ITEMERRORMSG,
            "args": {"item": item["lom"],},
        }


class PropagateHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        """Propagate Loguru messages to Python's built-in logger.
        (This is necessary to have the log counts appear in scrapy's stats module.)
        """
        logging.getLogger(record.name).handle(record)

logger.add(PropagateHandler(), format="{message}")