from scrapy.middleware import MiddlewareManager as MiddlewareManager
from scrapy.utils.conf import build_component_list as build_component_list

class ExtensionManager(MiddlewareManager):
    component_name: str = ...
