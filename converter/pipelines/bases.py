from abc import ABCMeta, abstractmethod
from typing import TypeVar, Optional

import scrapy.crawler

T = TypeVar('T')


class BasicAsyncPipeline(metaclass=ABCMeta):
    @abstractmethod
    async def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> Optional[scrapy.Item]:
        pass


class BasicPipeline(metaclass=ABCMeta):
    @abstractmethod
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> Optional[scrapy.Item]:
        """
        This method is called for every item pipeline component.

        `item` is an :ref:`item object <item-types>`, see
        :ref:`supporting-item-types`.

        :meth:`process_item` must either: return an :ref:`item object <item-types>`,
        return a :class:`~twisted.internet.defer.Deferred` or raise a
        :exc:`~scrapy.exceptions.DropItem` exception.

        Dropped items are no longer processed by further pipeline components.

        :param item: the scraped item
        :type item: :ref:`item object <item-types>`

        :param spider: the spider which scraped the item
        :type spider: :class:`~scrapy.spiders.Spider` object
        """
        pass


class PipelineWithPerSpiderMethods(metaclass=ABCMeta):
    @abstractmethod
    def open_spider(self, spider: scrapy.Spider) -> None:
        """
        This method is called when the spider is opened.
        :param spider: the spider which was opened
        """
        pass

    @abstractmethod
    def close_spider(self, spider: scrapy.Spider) -> None:
        """
        This method is called when the spider is closed.

        :param spider: the spider which was closed
        :type spider: :class:`~scrapy.spiders.Spider` object
        """
        pass


class PipelineWithFactoryMethod(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def from_crawler(cls: T, crawler: scrapy.crawler.Crawler) -> T:
        """
        If present, this classmethod is called to create a pipeline instance
        from a :class:`~scrapy.crawler.Crawler`. It must return a new instance
        of the pipeline. Crawler object provides access to all Scrapy core
        components like settings and signals; it is a way for pipeline to
        access them and hook its functionality into Scrapy.

        :param crawler: crawler that uses this pipeline
        :type crawler: :class:`~scrapy.crawler.Crawler` object
        """
        return cls()
