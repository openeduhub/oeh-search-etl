from scrapy.spiders import SitemapSpider
from converter.items import *
from datetime import datetime
from w3lib.html import remove_tags, replace_escape_chars
from converter.spiders.lom_base import LomBase
import time

# base for spiders using local 'json' data and need to access them
class JSONBase:
    json = None

    def get(self, *params, mode="first", json=None):
        if json == None:
            json = self.json

        for param in params:
            value = json
            for key in param.split("."):
                if value:
                    value = value.get(key)
                else:
                    return None
            if value != None:
                return value
        return None
