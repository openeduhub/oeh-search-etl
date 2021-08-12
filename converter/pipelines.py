# -*- coding: utf-8 -*-

from __future__ import annotations
import base64
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import dateparser
import io
import isodate
import logging
import time
from io import BytesIO
from typing import BinaryIO, TextIO, Optional
from abc import ABCMeta
import dateutil.parser
import requests
from PIL import Image
import scrapy
import scrapy.crawler
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter
from scrapy.utils.project import get_project_settings
from itemadapter import ItemAdapter

from converter import env
from converter.constants import *
from converter.es_connector import EduSharing
from valuespace_converter.app.valuespaces import Valuespaces

log = logging.getLogger(__name__)


class BasicPipeline(metaclass=ABCMeta):
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
        return item


class PipelineWithPerSpiderMethods(metaclass=ABCMeta):
    def open_spider(self, spider: scrapy.Spider) -> None:
        """
        This method is called when the spider is opened.
        :param spider: the spider which was opened
        """
        pass

    def close_spider(self, spider: scrapy.Spider) -> None:
        """
        This method is called when the spider is closed.

        :param spider: the spider which was closed
        :type spider: :class:`~scrapy.spiders.Spider` object
        """
        pass


class PipelineWithFactoryMethod(metaclass=ABCMeta):
    @classmethod
    def from_crawler(cls, crawler: scrapy.crawler.Crawler) -> 'PipelineWithFactoryMethod':
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


class LOMFillupPipeline(BasicPipeline):
    """
    fillup missing props by "guessing" or loading them if possible
    """
    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        if "fulltext" not in item and "text" in item["response"]:
            item["fulltext"] = item["response"]["text"]
        return raw_item


class FilterSparsePipeline(BasicPipeline):
    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        try:
            if "title" not in item["lom"]["general"]:
                raise DropItem(
                    "Entry {} has no title location".format(item["sourceId"])
                )
        except KeyError:
            raise DropItem(f'Item {item} has no lom.technical.location')
        try:
            if "location" not in item["lom"]["technical"]:
                raise DropItem(
                    "Entry {} has no technical location".format(item["lom"]["general"]["title"])
                )
        except KeyError:
            raise DropItem(f'Item {item} has no lom.technical.location')
        # pass through explicit uuid elements
        if "uuid" in item:
            return raw_item
        try:
            # if it contains keywords, it's valid
            if _ := item["lom"]["general"]["keyword"]:
                return raw_item
        except KeyError:
            pass
        try:
            # if it has a description, it's valid
            if _ := item["lom"]["general"]["description"]:
                return raw_item
        except KeyError:
            pass
        try:
            # if it the valuespaces.learningResourceType is set, it is valid
            if _ := item["valuespaces"]["learningResourceType"]:
                return raw_item
        except KeyError:
            pass
        # if none of the above matches drop the item

        try:
            raise DropItem(
                "Entry "
                + item["lom"]["general"]["title"]
                + " has neither keywords nor description"
            )
        except KeyError:
            raise DropItem(f'Item {item} was dropped for not providing enough metadata')

class NormLicensePipeline(BasicPipeline):
    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        if "url" in item["license"] and not item["license"]["url"] in Constants.VALID_LICENSE_URLS:
            for key in Constants.LICENSE_MAPPINGS:
                if item["license"]["url"].startswith(key):
                    item["license"]["url"] = Constants.LICENSE_MAPPINGS[key]
                    break
        if "internal" in item["license"] and (
                "url" not in item["license"]
                or item["license"]["url"] not in Constants.VALID_LICENSE_URLS
        ):
            for key in Constants.LICENSE_MAPPINGS_INTERNAL:
                if item["license"]["internal"].casefold() == key.casefold():
                    # use the first entry
                    item["license"]["url"] = Constants.LICENSE_MAPPINGS_INTERNAL[key][0]
                    break

        if "url" in item["license"] and "oer" not in item["license"]:
            if (
                    item["license"]["url"] == Constants.LICENSE_CC_BY_40
                    or item["license"]["url"] == Constants.LICENSE_CC_BY_30
                    or item["license"]["url"] == Constants.LICENSE_CC_BY_SA_30
                    or item["license"]["url"] == Constants.LICENSE_CC_BY_SA_40
                    or item["license"]["url"] == Constants.LICENSE_CC_ZERO_10
            ):
                item["license"]["oer"] = OerType.ALL

        if "internal" in item["license"] and "oer" not in item["license"]:
            internal = item["license"]["internal"].lower()
            if "cc-by-sa" in internal or "cc-0" in internal or "pdm" in internal:
                item["license"]["oer"] = OerType.ALL
        if "expirationDate" in item["license"]:
            item["license"]["expirationDate"] = dateparser.parse(item["license"]["expirationDate"])
        if "lifecycle" in item["lom"]:
            for contribute in item["lom"]["lifecycle"]:
                if "date" in contribute:
                    contribute["date"] = dateparser.parse(contribute["date"])

        return raw_item


class ConvertTimePipeline(BasicPipeline):
    """
    convert typicalLearningTime into an integer representing seconds
    + convert duration into an integer
    """
    def process_item(self, raw_item, spider):
        # map lastModified
        item = ItemAdapter(raw_item)
        if "lastModified" in item:
            try:
                item["lastModified"] = float(item["lastModified"])
            except:
                try:
                    date = dateutil.parser.parse(item["lastModified"])
                    item["lastModified"] = int(date.timestamp())
                except:
                    log.warning(
                        "Unable to parse given lastModified date "
                        + item["lastModified"]
                    )
                    del item["lastModified"]

        if "typicalLearningTime" in item["lom"]["educational"]:
            t = item["lom"]["educational"]["typicalLearningTime"]
            mapped = None
            splitted = t.split(":")
            if len(splitted) == 3:
                mapped = (
                        int(splitted[0]) * 60 * 60
                        + int(splitted[1]) * 60
                        + int(splitted[2])
                )
            if mapped is None:
                log.warning(
                    "Unable to map given typicalLearningTime "
                    + t
                    + " to numeric value"
                )
            item["lom"]["educational"]["typicalLearningTime"] = mapped
        if "technical" in item["lom"]:
            if "duration" in item["lom"]["technical"]:
                raw_duration = item["lom"]["technical"]["duration"]
                duration = raw_duration.strip()
                if duration:
                    if len(duration.split(":")) == 3:
                        duration = isodate.parse_time(duration)
                        duration = duration.hour*60*60 + duration.minute*60 + duration.second
                    elif duration.startswith("PT"):
                        duration = int(isodate.parse_duration(duration).total_seconds())
                    else:
                        try:
                            duration = int(duration)
                        except:
                            duration = None
                            logging.warning("duration {} could not be normalized to seconds".format(raw_duration))
                    item["lom"]["technical"]["duration"] = duration
        return raw_item


class ProcessValuespacePipeline(BasicPipeline):
    """
    generate de_DE / i18n strings for valuespace fields
    """
    def __init__(self):
        self.valuespaces = Valuespaces()

    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        json = item["valuespaces"]
        delete = []
        for key in json:
            # remap to new i18n layout
            mapped = []
            for entry in json[key]:
                _id = {}
                valuespace = self.valuespaces.data[key]
                found = False
                for v in valuespace:
                    labels = list(v["prefLabel"].values())
                    if "altLabel" in v:
                        labels = labels + list(
                            [x for y in list(v["altLabel"].values()) for x in y]
                        )
                    labels = list(map(lambda x: x.casefold(), labels))
                    if v["id"].endswith(entry) or entry.casefold() in labels:
                        _id = v["id"]
                        found = True
                        break
                if found and len(list(filter(lambda x: x == _id, mapped))) == 0:
                    mapped.append(_id)
            if len(mapped):
                json[key] = mapped
            else:
                delete.append(key)
        for key in delete:
            del json[key]
        item["valuespaces"] = json
        return raw_item


class ProcessThumbnailPipeline(BasicPipeline):
    """
    generate thumbnails
    """

    @staticmethod
    def scale_image(img, max_size):
        w = float(img.width)
        h = float(img.height)
        while w * h > max_size:
            w *= 0.9
            h *= 0.9
        return img.resize((int(w), int(h)), Image.ANTIALIAS).convert("RGB")

    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        response = None
        url = None
        settings = get_project_settings()
        if "thumbnail" in item:
            url = item["thumbnail"]
            response = requests.get(url)
            log.debug(
                "Loading thumbnail took " + str(response.elapsed.total_seconds()) + "s"
            )
        elif (
                "location" in item["lom"]["technical"]
                and "format" in item["lom"]["technical"]
                and item["lom"]["technical"]["format"] == "text/html"
        ):
            if settings.get("SPLASH_URL"):
                response = requests.post(
                    settings.get("SPLASH_URL") + "/render.png",
                    json={
                        "url": item["lom"]["technical"]["location"],
                        "wait": settings.get("SPLASH_WAIT"),
                        "html5_media": 1,
                        "headers": settings.get("SPLASH_HEADERS"),
                    },
                )
            else:
                if settings.get("DISABLE_SPLASH") is False:
                    log.warning(
                        "No thumbnail provided and SPLASH_URL was not configured for screenshots!"
                    )
        if response is None:
            if settings.get("DISABLE_SPLASH") is False:
                log.error(
                    "Neither thumbnail or technical.location (and technical.format) provided! Please provide at least one of them"
                )
        else:
            try:
                if response.headers["Content-Type"] == "image/svg+xml":
                    if len(response.content) > settings.get("THUMBNAIL_MAX_SIZE"):
                        raise Exception(
                            "SVG images can't be converted, and the given image exceeds the maximum allowed size ("
                            + str(len(response.content))
                            + " > "
                            + str(settings.get("THUMBNAIL_MAX_SIZE"))
                            + ")"
                        )
                    item["thumbnail"] = {}
                    item["thumbnail"]["mimetype"] = response.headers["Content-Type"]
                    item["thumbnail"]["small"] = base64.b64encode(
                        response.content
                    ).decode()
                else:
                    img = Image.open(BytesIO(response.content))
                    small = BytesIO()
                    self.scale_image(img, settings.get("THUMBNAIL_SMALL_SIZE")).save(
                        small,
                        "JPEG",
                        mode="RGB",
                        quality=settings.get("THUMBNAIL_SMALL_QUALITY"),
                    )
                    large = BytesIO()
                    self.scale_image(img, settings.get("THUMBNAIL_LARGE_SIZE")).save(
                        large,
                        "JPEG",
                        mode="RGB",
                        quality=settings.get("THUMBNAIL_LARGE_QUALITY"),
                    )
                    item["thumbnail"] = {}
                    item["thumbnail"]["mimetype"] = "image/jpeg"
                    item["thumbnail"]["small"] = base64.b64encode(
                        small.getvalue()
                    ).decode()
                    item["thumbnail"]["large"] = base64.b64encode(
                        large.getvalue()
                    ).decode()
            except Exception as e:
                if url is not None:
                    log.warning(
                        "Could not read thumbnail at "
                        + url
                        + ": "
                        + str(e)
                        + " (falling back to screenshot)"
                    )
                if "thumbnail" in item:
                    del item["thumbnail"]
                    return self.process_item(raw_item, spider)
                else:
                    # item['thumbnail']={}
                    raise DropItem(
                        "No thumbnail provided or ressource was unavailable for fetching"
                    )
        return raw_item


class EduSharingCheckPipeline(EduSharing, BasicPipeline):
    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        if "hash" not in item:
            log.error(
                "The spider did not provide a hash on the base object. The hash is required to detect changes on an element. May use the last modified date or something similar"
            )
            item["hash"] = time.time()

        # @TODO: May this can be done only once?
        if self.findSource(spider) is None:
            log.info("create new source " + spider.name)
            self.createSource(spider)

        db_item = self.findItem(item["sourceId"], spider)
        if db_item:
            if item["hash"] != db_item[1]:
                log.debug("hash has changed, continuing pipelines")
            else:
                log.debug("hash unchanged, skip item")
                # self.update(item['sourceId'], spider)
                # for tests, we update everything for now
                # activate this later
                # raise DropItem()
        return raw_item


class JSONStorePipeline(BasicPipeline, PipelineWithPerSpiderMethods):
    def __init__(self):
        self.files: dict[str, BinaryIO] = {}
        self.exporters: dict[str, JsonItemExporter] = {}

    def open_spider(self, spider):
        file = open(f'output_{spider.name}.json', 'wb')
        self.files[spider.name] = file
        exporter = JsonItemExporter(
            file,
            fields_to_export=[
                "sourceId",
                "lom",
                # "valuespaces",
                "license",
                # "type",
                # "origin",
                # "fulltext",
                # "ranking",
                # "lastModified",
                # "thumbnail",
            ],
            encoding='utf-8',
            indent=2,
            ensure_ascii=False)
        self.exporters[spider.name] = exporter
        exporter.start_exporting()

    def close_spider(self, spider):
        self.exporters[spider.name].finish_exporting()
        self.files[spider.name].close()

    def process_item(self, item, spider):
        self.exporters[spider.name].export_item(item)
        return item


class CSVStorePipeline(BasicPipeline, PipelineWithPerSpiderMethods):
    rows = []

    def __init__(self):
        self.files: dict[str, TextIO] = {}
        self.exporters: dict[str, csv.writer] = {}
        CSVStorePipeline.rows = env.get("CSV_ROWS", allow_null=False).split(",")

    def open_spider(self, spider):
        csv_file = open('output_' + spider.name + '.csv', 'w', newline='')
        spamwriter = csv.writer(
            csv_file,
            delimiter=',',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL)

        spamwriter.writerow(self.rows)
        self.files[spider.name] = csv_file
        self.exporters[spider.name] = spamwriter

    @staticmethod
    def get_value(item, value):
        container = item
        tokens = value.split('.')
        for v in tokens:
            if v in container:
                container = container[v]
            else:
                return None
        if tokens[0] == 'valuespaces':
            return list(map(lambda x: Valuespaces.findKey(tokens[1], x)['prefLabel']['de'], container))
        return container

    def close_spider(self, spider):
        # exporter closes automatically?
        self.files[spider.name].close()

    def process_item(self, item, spider):
        self.exporters[spider.name].writerow(list(map(lambda x: self.get_value(item, x), self.rows)))
        self.files[spider.name].flush()
        return item


class EduSharingStorePipeline(EduSharing, BasicPipeline):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        title = "<no title>"
        if "title" in item["lom"]["general"]:
            title = str(item["lom"]["general"]["title"])
        entryUUID = EduSharing.buildUUID(item["response"]["url"])
        self.insertItem(spider, entryUUID, item)
        logging.info("item " + entryUUID + " inserted/updated")

        # @TODO: We may need to handle Collections
        # if 'collection' in item:
        #    for collection in item['collection']:
        # if dbItem:
        #     entryUUID = dbItem[0]
        #     logging.info('Updating item ' + title + ' (' + entryUUID + ')')
        #     self.curr.execute("""UPDATE "references_metadata" SET last_seen = now(), last_updated = now(), hash = %s, data = %s WHERE source = %s AND source_id = %s""", (
        #         item['hash'], # hash
        #         json,
        #         spider.name,
        #         str(item['sourceId']),
        #     ))
        # else:
        #     entryUUID = self.buildUUID(item['response']['url'])
        #     if 'uuid' in item:
        #         entryUUID = item['uuid']
        #     logging.info('Creating item ' + title + ' (' + entryUUID + ')')
        #     if self.uuidExists(entryUUID):
        #         logging.warn('Possible duplicate detected for ' + entryUUID)
        #     else:
        #         self.curr.execute("""INSERT INTO "references" VALUES (%s,true,now())""", (
        #             entryUUID,
        #         ))
        #     self.curr.execute("""INSERT INTO "references_metadata" VALUES (%s,%s,%s,%s,now(),now(),%s)""", (
        #         spider.name, # source name
        #         str(item['sourceId']), # source item identifier
        #         entryUUID,
        #         item['hash'], # hash
        #         json,
        #     ))
        return raw_item


class DummyPipeline(BasicPipeline):
    # Scrapy will print the item on log level DEBUG anyway

    # class Printer:
    #     def write(self, byte_str: bytes) -> None:
    #         logging.debug(byte_str.decode("utf-8"))

    # def open_spider(self, spider):
    #     self.exporter = JsonItemExporter(
    #         DummyOutPipeline.Printer(),
    #         fields_to_export=[
    #             "collection",
    #             "fulltext",
    #             "hash",
    #             "lastModified",
    #             "license",
    #             "lom",
    #             "origin",
    #             "permissions",
    #             "publisher",
    #             "ranking",
    #             # "response",
    #             "sourceId",
    #             # "thumbnail",
    #             "type",
    #             "uuid",
    #             "valuespaces",
    #         ],
    #         indent=2,
    #         encoding="utf-8",
    #     )
    #     self.exporter.start_exporting()

    # def close_spider(self, spider):
    #     self.exporter.finish_exporting()

    def process_item(self, item, spider):
        log.info("DRY RUN scraped {}".format(item["response"]["url"]))
        # self.exporter.export_item(item)
        return item
