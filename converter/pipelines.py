# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from converter.constants import *
import json
import re
from w3lib.html import replace_escape_chars
from scrapy.exporters import JsonItemExporter
import io
from datetime import date
import time
import dateutil.parser
import logging
from pprint import pprint
from PIL import Image
from io import BytesIO
import requests
import urllib
import base64
import html2text
import scrapy
import sys
import uuid
from valuespace_converter.app.valuespaces import Valuespaces
from scrapy.utils.project import get_project_settings
from converter.es_connector import EduSharing

# fillup missing props by "guessing" or loading them if possible
class LOMFillupPipeline:
    def process_item(self, item, spider):
        if not "fulltext" in item and "text" in item["response"]:
            item["fulltext"] = item["response"]["text"]
        return item


class FilterSparsePipeline:
    def process_item(self, item, spider):
        valid = False
        if not "location" in item["lom"]["technical"]:
            raise DropItem(
                "Entry "
                + item["lom"]["general"]["title"]
                + " has no technical location"
            )
        # pass through explicit uuid elements
        if "uuid" in item:
            return item
        try:
            valid = item["lom"]["general"]["keyword"]
        except:
            pass
        try:
            valid = valid or item["lom"]["general"]["description"]
        except:
            pass
        try:
            valid = valid or item["valuespaces"]["learningResourceType"]
        except:
            pass
        if not valid:
            raise DropItem(
                "Entry "
                + item["lom"]["general"]["title"]
                + " has neither keywords nor description"
            )
        return item


class NormLicensePipeline:
    def process_item(self, item, spider):
        if "url" in item["license"]:
            for key in Constants.LICENSE_MAPPINGS:
                if item["license"]["url"].startswith(key):
                    item["license"]["url"] = Constants.LICENSE_MAPPINGS[key]
                    break
        if "internal" in item["license"] and (
            not "url" in item["license"]
            or not item["license"]["url"] in Constants.VALID_LICENSE_URLS
        ):
            for key in Constants.LICENSE_MAPPINGS_INTERNAL:
                if item["license"]["internal"].casefold() == key.casefold():
                    item["license"]["url"] = Constants.LICENSE_MAPPINGS_INTERNAL[key]
                    break

        if "url" in item["license"] and not "oer" in item["license"]:
            if (
                item["license"]["url"] == Constants.LICENSE_CC_BY_40
                or item["license"]["url"] == Constants.LICENSE_CC_BY_SA_30
                or item["license"]["url"] == Constants.LICENSE_CC_BY_SA_40
                or item["license"]["url"] == Constants.LICENSE_CC_ZERO_10
            ):
                item["license"]["oer"] = OerType.ALL

        if "internal" in item["license"] and not "oer" in item["license"]:
            internal = item["license"]["internal"].lower()
            if "cc-by-sa" in internal or "cc-0" in internal or "pdm" in internal:
                item["license"]["oer"] = OerType.ALL
        return item


# convert typicalLearningTime into a integer representing seconds
class ConvertTimePipeline:
    def process_item(self, item, spider):
        # map lastModified
        if "lastModified" in item:
            try:
                item["lastModified"] = float(item["lastModified"])
            except:
                try:
                    date = dateutil.parser.parse(item["lastModified"])
                    item["lastModified"] = int(date.timestamp())
                except:
                    logging.warn(
                        "Unable to parse given lastModified date "
                        + item["lastModified"]
                    )
                    del item["lastModified"]

        if "typicalLearningTime" in item["lom"]["educational"]:
            time = item["lom"]["educational"]["typicalLearningTime"]
            mapped = None
            splitted = time.split(":")
            if len(splitted) == 3:
                mapped = (
                    int(splitted[0]) * 60 * 60
                    + int(splitted[1]) * 60
                    + int(splitted[2])
                )
            if mapped == None:
                logging.warn(
                    "Unable to map given typicalLearningTime "
                    + time
                    + " to numeric value"
                )
            item["lom"]["educational"]["typicalLearningTime"] = mapped
        return item


# generate de_DE / i18n strings for valuespace fields
class ProcessValuespacePipeline:
    valuespaces = None

    def __init__(self):
        self.valuespaces = Valuespaces()

    def process_item(self, item, spider):
        json = item["valuespaces"]
        delete = []
        for key in json:
            # remap to new i18n layout
            mapped = []
            for entry in json[key]:
                id = {}
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
                        id = v["id"]
                        found = True
                        break
                if found and len(list(filter(lambda x: x == id, mapped))) == 0:
                    mapped.append(id)
            if len(mapped):
                json[key] = mapped
            else:
                delete.append(key)
        for key in delete:
            del json[key]
        item["valuespaces"] = json
        return item


# generate thumbnails
class ProcessThumbnailPipeline:
    def scaleImage(self, img, maxSize):
        w = float(img.width)
        h = float(img.height)
        while w * h > maxSize:
            w *= 0.9
            h *= 0.9
        return img.resize((int(w), int(h)), Image.ANTIALIAS).convert("RGB")

    def process_item(self, item, spider):
        response = None
        settings = get_project_settings()
        url = False

        if "thumbnail" in item:
            url = item["thumbnail"]
            response = requests.get(url)
            logging.debug(
                "Loading thumbnail took " + str(response.elapsed.total_seconds()) + "s"
            )
        elif 'defaultThumbnail' in item:
            url = item['defaultThumbnail']
            response = requests.get(url)
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
                logging.warning(
                    "No thumbnail provided and SPLASH_URL was not configured for screenshots!"
                )
        if response == None:
            logging.error(
                "Neither thumbnail or technical.location provided! Please provide at least one of them"
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
                    self.scaleImage(img, settings.get("THUMBNAIL_SMALL_SIZE")).save(
                        small,
                        "JPEG",
                        mode="RGB",
                        quality=settings.get("THUMBNAIL_SMALL_QUALITY"),
                    )
                    large = BytesIO()
                    self.scaleImage(img, settings.get("THUMBNAIL_LARGE_SIZE")).save(
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
                if url:
                    logging.warn(
                        "Could not read thumbnail at "
                        + url
                        + ": "
                        + str(e)
                    )
                if "thumbnail" in item:
                    logging.warn("(falling back to " + ("defaultThumbnail" if "defaultThumbnail" in item else "screenshot") + ")")
                    del item["thumbnail"]
                    return self.process_item(item, spider)
                elif 'defaultThumbnail' in item:
                    logging.warn("(falling back to screenshot)")
                    del item['defaultThumbnail']
                    return self.process_item(item, spider)
                else:
                    # item['thumbnail']={}
                    raise DropItem(
                        "No thumbnail provided or ressource was unavailable for fetching"
                    )
        return item


class EduSharingCheckPipeline(EduSharing):
    def process_item(self, item, spider):
        if not "hash" in item:
            logging.error(
                "The spider did not provide a hash on the base object. The hash is required to detect changes on an element. May use the last modified date or something similar"
            )
            item["hash"] = time.time()

        # @TODO: May this can be done only once?
        if self.findSource(spider) == None:
            logging.info("create new source " + spider.name)
            self.createSource(spider)

        dbItem = self.findItem(item["sourceId"], spider)
        if dbItem:
            if item["hash"] != dbItem[1]:
                logging.debug("hash has changed, continuing pipelines")
            else:
                logging.debug("hash unchanged, skip item")
                # self.update(item['sourceId'], spider)
                # for tests, we update everything for now
                # activate this later
                # raise DropItem()
        return item


class EduSharingStorePipeline(EduSharing):
    def process_item(self, item, spider):
        output = io.BytesIO()
        exporter = JsonItemExporter(
            output,
            fields_to_export=[
                "lom",
                "valuespaces",
                "license",
                "type",
                "origin",
                "fulltext",
                "ranking",
                "lastModified",
                "thumbnail",
            ],
        )
        exporter.export_item(item)
        title = "<no title>"
        if "title" in item["lom"]["general"]:
            title = str(item["lom"]["general"]["title"])
        entryUUID = self.buildUUID(item["response"]["url"])
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
        output.close()
        return item


class DummyOutPipeline:
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
        logging.info("DRY RUN scraped {}".format(item["response"]["url"]))
        # self.exporter.export_item(item)
        return item
