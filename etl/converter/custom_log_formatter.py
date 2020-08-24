from scrapy.logformatter import LogFormatter
import logging
import os


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
