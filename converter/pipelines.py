# -*- coding: utf-8 -*-

from __future__ import annotations

import base64
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import logging
import time
from abc import ABCMeta
from io import BytesIO
from typing import BinaryIO, TextIO, Optional

import dateparser
import dateutil.parser
import isodate
import requests
import scrapy
import scrapy.crawler
from PIL import Image
from itemadapter import ItemAdapter
from scrapy import settings
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter
from scrapy.utils.project import get_project_settings

from converter import env
from converter.constants import *
from converter.es_connector import EduSharing
from converter.items import BaseItem
from converter.web_tools import WebTools, WebEngine
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
            if "location" not in item["lom"]["technical"] and not "binary" in item:
                raise DropItem(
                    "Entry {} has no technical location or binary data".format(item["lom"]["general"]["title"])
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
                        duration = duration.hour * 60 * 60 + duration.minute * 60 + duration.second
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
                        labels = labels + list(v["altLabel"].values())
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
        """
        By default the thumbnail-pipeline handles several cases:
        - if there is a URL-string inside the "BaseItem.thumbnail"-field:
        -- download image from URL; rescale it into different sizes (small/large);
        --- save the thumbnails as base64 within
        ---- "BaseItem.thumbnail.small", "BaseItem.thumbnail.large"
        --- (afterwards delete the URL from "BaseItem.thumbnail")

        - if there is NO "BaseItem.thumbnail"-field:
        -- default: take a screenshot of the URL from "technical.location" with Splash, rescale and save (as above)
        -- alternatively, on-demand: use Playwright to take a screenshot, rescale and save (as above)
        """
        item = ItemAdapter(raw_item)
        response = None
        url = None
        settings = get_settings_for_crawler(spider)
        # checking if the (optional) attribute WEB_TOOLS exists:
        web_tools = settings.get("WEB_TOOLS", WebEngine.Splash)
        # if screenshot_bytes is provided (the crawler has already a binary representation of the image
        # the pipeline will convert/scale the given image
        if "screenshot_bytes" in item:
            # in case we are already using playwright in a spider, we can skip one additional HTTP Request by
            # accessing the (temporary available) "screenshot_bytes"-field
            img = Image.open(BytesIO(item["screenshot_bytes"]))
            self.create_thumbnails_from_image_bytes(img, item, settings)
            # the final BaseItem data model doesn't use screenshot_bytes,
            # therefore we delete it after we're done processing it
            del item["screenshot_bytes"]

            # a thumbnail (url) is given - we will try to fetch it from the url
        elif "thumbnail" in item:
            url = item["thumbnail"]
            response = requests.get(url)
            log.debug(
                "Loading thumbnail took " + str(response.elapsed.total_seconds()) + "s"
            )
            # nothing was given, we try to screenshot the page either via Splash or Playwright
        elif (
                "location" in item["lom"]["technical"]
                and len(item["lom"]["technical"]["location"]) > 0
                and "format" in item["lom"]["technical"]
                and item["lom"]["technical"]["format"] == "text/html"
        ):
            if settings.get("SPLASH_URL") and web_tools == WebEngine.Splash:
                response = requests.post(
                    settings.get("SPLASH_URL") + "/render.png",
                    json={
                        "url": item["lom"]["technical"]["location"][0],
                        # since there can be multiple "technical.location"-values, the first URL is used for thumbnails
                        "wait": settings.get("SPLASH_WAIT"),
                        "html5_media": 1,
                        "headers": settings.get("SPLASH_HEADERS"),
                    },
                )
            if env.get("PLAYWRIGHT_WS_ENDPOINT") and web_tools == WebEngine.Playwright:
                # if the attribute "WEB_TOOLS" doesn't exist as an attribute within a specific spider,
                # it will default back to "splash"

                # this edge-case is necessary for spiders that only need playwright to gather a screenshot,
                # but don't use playwright within the spider itself (e.g. serlo_spider)
                playwright_dict = WebTools.getUrlData(url=item["lom"]["technical"]["location"][0],
                                                      engine=WebEngine.Playwright)
                screenshot_bytes = playwright_dict.get("screenshot_bytes")
                img = Image.open(BytesIO(screenshot_bytes))
                self.create_thumbnails_from_image_bytes(img, item, settings)
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
                    self.create_thumbnails_from_image_bytes(img, item, settings)
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

    # override the project settings with the given ones from the current spider
    # see PR 56 for details

    def create_thumbnails_from_image_bytes(self, image, item, settings):
        small = BytesIO()
        self.scale_image(image, settings.get("THUMBNAIL_SMALL_SIZE")).save(
            small,
            "JPEG",
            mode="RGB",
            quality=settings.get("THUMBNAIL_SMALL_QUALITY"),
        )
        large = BytesIO()
        self.scale_image(image, settings.get("THUMBNAIL_LARGE_SIZE")).save(
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


def get_settings_for_crawler(spider):
    all_settings = get_project_settings()
    crawler_settings = settings.BaseSettings(getattr(spider, "custom_settings") or {}, 'spider')
    if type(crawler_settings) == dict:
        crawler_settings = settings.BaseSettings(crawler_settings, 'spider')
    for key in crawler_settings.keys():
        if (
                all_settings.get(key) and crawler_settings.getpriority(key) > all_settings.getpriority(key)
                or not all_settings.get(key)
        ):
            all_settings.set(key, crawler_settings.get(key), crawler_settings.getpriority(key))
    return all_settings


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
                "hash",
                "lastModified",
                "type",
                "lom",
                "valuespaces",
                "license",
                # "origin",
                # "fulltext",
                # "ranking",
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
        entryUUID = EduSharing.buildUUID(item["response"]["url"] if "url" in item["response"] else item["hash"])
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


# example pipeline which simply outputs the item in the log
class ExampleLoggingPipeline(BasicPipeline):
    def process_item(self, item, spider):
        log.info(item)
        # self.exporter.export_item(item)
        return item


class LisumPipeline(BasicPipeline):
    DISCIPLINE_TO_LISUM = {
        "020": "C-WAT",  # Arbeitslehre -> Wirtschaft, Arbeit, Technik
        "060": "C-KU",  # Bildende Kunst
        "080": "C-BIO",  # Biologie
        "100": "C-CH",  # Chemie
        "120": "C-DE",  # Deutsch
        "160": "C-Eth",  # Ethik
        "200": "C-FS",  # Fremdsprachen
        "220": "C-GEO",  # Geographie,
        "240": "C-GE",  # Geschichte
        "380": "C-MA",  # Mathematik
        "420": "C-MU",  # Musik
        "450": "C-Phil",  # Philosophie
        "460": "C-Ph",  # Physik
        "480": "C-PB",  # Politische Bildung
        "510": "C-Psy",  # Psychologie
        "520": "C-LER",  # Religion -> Lebensgestaltung-Ethik-Religionskunde
        "700": "C-SOWI",  # Wirtschaftskunde -> "Sozialwissenschaft/Wirtschaftswissenschaft"
        "12002": "C-Thea",  # Darstellendes Spiel, Schultheater -> Theater
        "20001": "C-EN",  # Englisch
        "20002": "C-FR",  # Französisch
        "20003": "C-AGR",  # Griechisch -> Altgriechisch
        "20004": "C-IT",  # Italienisch
        "20005": "C-La",  # Latein
        "20006": "C-RU",  # Russisch
        "20008": "C-TR",  # Türkisch
        "20011": "C-PL",  # Polnisch
        "20014": "C-PT",  # Portugiesisch
        "20041": "C-ZH",  # Chinesisch
        "28010": "C-SU",  # Sachkunde -> Sachunterricht
        "32002": "C-Inf",  # Informatik
        "46014": "C-AS",  # Astronomie
        "48005": "C-GEWIWI",  # Gesellschaftspolitische Gegenwartsfragen -> Gesellschaftswissenschaften
        "2800506": "C-PL",  # Polnisch
    }

    EDUCATIONALCONTEXT_TO_LISUM = {
        "elementarbereich": "pre-school",
        "grundschule": "primary school",
        "sekundarstufe_1": "lower secondary school",
        "sekundarstufe_2": "upper secondary school",
        "berufliche_bildung": "vocational education",
        # "fortbildung": "",  # does not exist in Lisum valuespace
        "erwachsenenbildung": "continuing education",
        "foerderschule": "special education",
        # "fernunterricht": ""  # does not exist in Lisum valuespace
    }

    LRT_OEH_TO_LISUM = {
        # LRT-values that aren't listed here, can be mapped 1:1
        "audiovisual_medium": ["audio", "video"],
        # ToDo: INTERAKTION
        "open_activity": "",  # exists in 2 out of 60.000 items
        "broadcast": "audio",
        "demonstration": "image",  # "Veranschaulichung"
    }

    def process_item(self, item: BaseItem, spider: scrapy.Spider) -> Optional[scrapy.Item]:
        """
        Takes a BaseItem and transforms its metadata-values to Lisum-metadataset-compatible values.
        Touches the following fields within the BaseItem:
        - valuespaces.discipline
        - valuespaces.educationalContext
        - valuespaces.intendedEndUserRole
        - valuespaces.learningResourceType
        """
        base_item_adapter = ItemAdapter(item)
        # ToDo: - make sure that discipline.ttl has all possible values, otherwise information loss occurs
        #       - keep raw list for debugging purposes?
        if base_item_adapter.get("valuespaces"):
            valuespaces = base_item_adapter.get("valuespaces")
            if valuespaces.get("discipline"):
                discipline_list = valuespaces.get("discipline")
                # a singular entry will look like 'http://w3id.org/openeduhub/vocabs/discipline/380'
                # the last part of the URL string equals to a corresponding eafCode
                # (see: http://agmud.de/wp-content/uploads/2021/09/eafsys.txt)
                # this eafCode (key) gets mapped to Lisum specific B-B shorthands like "C-MA"
                discipline_lisum_keys = set()
                if discipline_list:
                    for discipline_w3id in discipline_list:
                        discipline_eaf_code: str = discipline_w3id.split(sep='/')[-1]
                        match discipline_eaf_code in self.DISCIPLINE_TO_LISUM:
                            case True:
                                discipline_lisum_keys.add(self.DISCIPLINE_TO_LISUM.get(discipline_eaf_code))
                                # ToDo: there are no Sodix eafCode-values for these Lisum keys:
                                #  - Deutsche Gebärdensprache (C-DGS)
                                #  - Hebräisch (C-HE)
                                #  - Japanisch (C-JP)
                                #  - Naturwissenschaften (5/6) (= C-NW56)
                                #  - Naturwissenschaften (C-NW)
                                #  - Neu Griechisch (C-EL)
                                #  - Sorbisch/Wendisch (C-SW)
                            case _:
                                # ToDo: fallback -> if eafCode can't be mapped, save to keywords?
                                logging.warning(f"Lisum Pipeline failed to map from eafCode {discipline_eaf_code} "
                                                f"to its corresponding ccm:taxonid short-handle")
                discipline_lisum_keys = list(discipline_lisum_keys)
                discipline_lisum_keys.sort()
                logging.debug(f"LisumPipeline: Mapping discipline values from \n {discipline_list} \n to "
                              f"LisumPipeline: discipline_lisum_keys \n {discipline_lisum_keys}")
                valuespaces["discipline"] = discipline_lisum_keys

            if valuespaces.get("educationalContext"):
                # mapping educationalContext values from OEH SKOS to lisum keys
                educational_context_list = valuespaces.get("educationalContext")
                educational_context_lisum_keys = set()
                if educational_context_list:
                    # making sure that we filter out empty lists []
                    # up until this point, every educationalContext entry will be a w3id link, e.g.
                    # 'http://w3id.org/openeduhub/vocabs/educationalContext/grundschule'
                    for educational_context_w3id in educational_context_list:
                        educational_context_w3id_key = educational_context_w3id.split(sep='/')[-1]
                        match educational_context_w3id_key in self.EDUCATIONALCONTEXT_TO_LISUM:
                            case True:
                                educational_context_w3id_key = self.EDUCATIONALCONTEXT_TO_LISUM.get(
                                    educational_context_w3id_key)
                                educational_context_lisum_keys.add(educational_context_w3id_key)
                            case _:
                                logging.debug(f"LisumPipeline: educationalContext {educational_context_w3id_key}"
                                              f"not found in mapping table.")
                educational_context_list = list(educational_context_lisum_keys)
                educational_context_list.sort()
                valuespaces["educationalContext"] = educational_context_list

            if valuespaces.get("intendedEndUserRole"):
                intended_end_user_role_list = valuespaces.get("intendedEndUserRole")
                intended_end_user_roles = set()
                if intended_end_user_role_list:
                    for item_w3id in intended_end_user_role_list:
                        item_w3id: str = item_w3id.split(sep='/')[-1]
                        if item_w3id:
                            intended_end_user_roles.add(item_w3id)
                    intended_end_user_role_list = list(intended_end_user_roles)
                    intended_end_user_role_list.sort()
                valuespaces["intendedEndUserRole"] = intended_end_user_role_list

            if valuespaces.get("learningResourceType"):
                lrt_list: list = valuespaces.get("learningResourceType")
                lrt_temporary_list = list()
                if lrt_list:
                    for lrt_item in lrt_list:
                        if type(lrt_item) is list:
                            # some values like "audiovisual" were already mapped to ["audio", "visual"] multivalues
                            # during transformation from Sodix to OEH
                            lrt_multivalue = list()
                            for lrt_string in lrt_item:
                                lrt_string = lrt_string.split(sep='/')[-1]
                                if lrt_string in self.LRT_OEH_TO_LISUM:
                                    lrt_string = self.LRT_OEH_TO_LISUM.get(lrt_string)
                                if lrt_string:
                                    # making sure to exclude ''-strings
                                    lrt_multivalue.append(lrt_string)
                            lrt_temporary_list.append(lrt_multivalue)
                        if type(lrt_item) is str:
                            lrt_w3id: str = lrt_item.split(sep='/')[-1]
                            if lrt_w3id in self.LRT_OEH_TO_LISUM:
                                lrt_w3id = self.LRT_OEH_TO_LISUM.get(lrt_w3id)
                            if lrt_w3id:
                                # ToDo: workaround
                                # making sure to exclude '' strings from populating the list
                                lrt_temporary_list.append(lrt_w3id)
                    lrt_list = lrt_temporary_list
                    lrt_list.sort()
                    valuespaces["learningResourceType"] = lrt_list
        # ToDo: which fields am I missing? what's next?

        return item
