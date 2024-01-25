# -*- coding: utf-8 -*-

from __future__ import annotations

import base64
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import datetime
import logging
import re
import time
from abc import ABCMeta
from asyncio import Future
from io import BytesIO
from typing import BinaryIO, TextIO, Optional

import PIL
import dateparser
import dateutil.parser
import isodate
import scrapy
import scrapy.crawler
import twisted.internet.error
from PIL import Image
from async_lru import alru_cache
from itemadapter import ItemAdapter
from scrapy import settings
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter
from scrapy.http.request import NO_CALLBACK
from scrapy.utils.defer import maybe_deferred_to_future
from scrapy.utils.project import get_project_settings
from twisted.internet.defer import Deferred

from converter import env
from converter.constants import *
from converter.es_connector import EduSharing
from converter.items import BaseItem
from converter.util.edu_sharing_source_template_helper import EduSharingSourceTemplateHelper
from converter.util.language_mapper import LanguageMapper
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


class NormLanguagePipeline(BasicPipeline):
    """Normalize raw or ambiguous language strings to 2-letter-language-codes (ISO 639-1)."""
    def process_item(self, item, spider):
        item_adapter = ItemAdapter(item)
        try:
            lom_general_languages: list[str] = item_adapter["lom"]["general"]["language"]
            if lom_general_languages:
                language_mapper = LanguageMapper(languages=lom_general_languages)
                normalized_language_codes: list[str] | None = language_mapper.normalize_list_of_language_strings()
                if normalized_language_codes:
                    item_adapter["lom"]["general"]["language"] = normalized_language_codes
        except KeyError:
            # happens when the "language" field does not exist within lom.general
            pass
        try:
            lom_educational_languages: list[str] = item_adapter["lom"]["educational"]["language"]
            if lom_educational_languages:
                language_mapper = LanguageMapper(languages=lom_educational_languages)
                normalized_language_codes: list[str] | None = language_mapper.normalize_list_of_language_strings()
                if normalized_language_codes:
                    item_adapter["lom"]["general"]["language"] = normalized_language_codes
        except KeyError:
            # happens when the "language" field does not exist within lom.educational
            pass
        return item


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
            match item["license"]["url"]:
                case Constants.LICENSE_CC_BY_20 | \
                     Constants.LICENSE_CC_BY_25 | \
                     Constants.LICENSE_CC_BY_30 | \
                     Constants.LICENSE_CC_BY_40 | \
                     Constants.LICENSE_CC_BY_SA_20 | \
                     Constants.LICENSE_CC_BY_SA_25 | \
                     Constants.LICENSE_CC_BY_SA_30 | \
                     Constants.LICENSE_CC_BY_SA_40 | \
                     Constants.LICENSE_CC_ZERO_10:
                    item["license"]["oer"] = OerType.ALL
                case _:
                    # ToDo: log default case if not too spammy
                    pass

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
                            log.warning("duration {} could not be normalized to seconds".format(raw_duration))
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
        item["valuespaces_raw"] = dict(json)
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
        return img.resize((int(w), int(h)), Image.Resampling.LANCZOS).convert("RGB")

    async def process_item(self, raw_item, spider):
        """
        By default, the thumbnail-pipeline handles several cases:
        - if there is a URL-string inside the "BaseItem.thumbnail"-field:
        -- download image from URL; rescale it into different sizes (small/large);
        --- save the thumbnails as base64 within
        ---- "BaseItem.thumbnail.small", "BaseItem.thumbnail.large"
        --- (afterward delete the URL from "BaseItem.thumbnail")

        - if there is NO "BaseItem.thumbnail"-field:
        -- default: take a screenshot of the URL from "technical.location" with Splash, rescale and save (as above)
        -- alternatively, on-demand: use Playwright to take a screenshot, rescale and save (as above)
        """
        item = ItemAdapter(raw_item)
        response: scrapy.http.Response | None = None
        url: str | None = None
        settings_crawler = get_settings_for_crawler(spider)
        # checking if the (optional) attribute WEB_TOOLS exists:
        web_tools = settings_crawler.get("WEB_TOOLS", default=WebEngine.Splash)
        _splash_success: bool | None = None  # control flag flips to False if Splash can't handle a URL

        # if screenshot_bytes is provided (the crawler has already a binary representation of the image,
        # the pipeline will convert/scale the given image
        if "screenshot_bytes" in item:
            # in case we are already using playwright in a spider, we can skip one additional HTTP Request by
            # accessing the (temporary available) "screenshot_bytes"-field
            img = Image.open(BytesIO(item["screenshot_bytes"]))
            self.create_thumbnails_from_image_bytes(img, item, settings_crawler)
            # The final BaseItem data model doesn't use screenshot_bytes.
            # Therefore, we delete it after we're done with processing it
            del item["screenshot_bytes"]
        elif "thumbnail" in item:
            # a thumbnail (url) was provided within the item -> we will try to fetch it from the url
            url: str = item["thumbnail"]
            time_start: datetime = datetime.datetime.now()
            try:
                thumbnail_response: scrapy.http.Response = await self.download_thumbnail_url(url, spider)
                # we expect that some thumbnail URLs will be wrong, outdated or already offline, which is why we catch
                # the most common Exceptions while trying to dwonload the image.
            except twisted.internet.error.TCPTimedOutError:
                log.warning(f"Thumbnail download of URL {url} failed due to TCPTimedOutError. "
                            f"(You might see this error if the image is unavailable under that specific URL.) "
                            f"Falling back to website screenshot.")
                del item["thumbnail"]
                return await self.process_item(raw_item, spider)
            except twisted.internet.error.DNSLookupError:
                log.warning(f"Thumbnail download of URL {url} failed due to DNSLookupError. "
                            f"(The webserver might be offline.) Falling back to website screenshot.")
                del item["thumbnail"]
                return await self.process_item(raw_item, spider)
            time_end: datetime = datetime.datetime.now()
            log.debug(f"Loading thumbnail from {url} took {time_end - time_start} (incl. awaiting).")
            log.debug(f"Thumbnail-URL-Cache: {self.download_thumbnail_url.cache_info()} after trying to query {url} ")
            if thumbnail_response.status != 200:
                log.debug(f"Thumbnail-Pipeline received a unexpected response (status: {thumbnail_response.status}) "
                          f"from {url} (-> resolved URL: {thumbnail_response.url}")
                # fall back to website screenshot
                del item["thumbnail"]
                return await self.process_item(raw_item, spider)
            else:
                # Some web-servers 'lie' in regard to their HTTP status, e.g., they forward to a 404 HTML page and still
                # respond with a '200' code.
                try:
                    # We need to do additional checks before accepting the response object as a valid candidate for the
                    # image transformation
                    _mimetype: bytes = thumbnail_response.headers["Content-Type"]
                    _mimetype: str = _mimetype.decode()
                    if _mimetype.startswith("image/"):
                        # we expect thumbnail URLs to be of MIME-Type 'image/...'
                        # see: https://www.iana.org/assignments/media-types/media-types.xhtml#image
                        response = thumbnail_response
                        # only set the response if thumbnail retrieval was successful!
                    elif _mimetype == "application/octet-stream":
                        # ToDo: special handling for 'application/octet-stream' necessary?
                        log.debug(f"Thumbnail URL of MIME-Type 'image/...' expected, "
                                 f"but received '{_mimetype}' instead. "
                                 f"(If thumbnail conversion throws unexpected errors further down the line, "
                                 f"the Thumbnail-Pipeline needs to be re-visited! URL: {url} )")
                        response = thumbnail_response
                    else:
                        log.warning(f"Thumbnail URL {url} does not seem to be an image! "
                                    f"Header contained Content-Type '{_mimetype}' instead. "
                                    f"(Falling back to screenshot)")
                        del item["thumbnail"]
                        return await self.process_item(raw_item, spider)
                except KeyError:
                    log.warning(f"Thumbnail URL response did not contain a Content-Type / MIME-Type! "
                                f"Thumbnail URL queried: {url} "
                                f"-> resolved URL: {thumbnail_response.url} "
                                f"(HTTP Status: {thumbnail_response.status}")
                    del item["thumbnail"]
                    return await self.process_item(raw_item, spider)
        elif (
                "location" in item["lom"]["technical"]
                and len(item["lom"]["technical"]["location"]) > 0
        ):
            if settings_crawler.get("SPLASH_URL") and web_tools == WebEngine.Splash:
                target_url: str = item["lom"]["technical"]["location"][0]
                _splash_url: str = f"{settings_crawler.get('SPLASH_URL')}/render.png"
                _splash_parameter_wait: str = f"{settings_crawler.get('SPLASH_WAIT')}"
                _splash_parameter_html5media: str = str(1)
                _splash_headers: dict = settings_crawler.get("SPLASH_HEADERS")
                _splash_dict: dict = {
                    "url": target_url,
                    "wait": _splash_parameter_wait,
                    "html5_media": _splash_parameter_wait,
                    "headers": _splash_headers
                }
                request_splash = scrapy.FormRequest(
                    url=_splash_url,
                    formdata=_splash_dict,
                    callback=NO_CALLBACK,
                    priority=1
                )
                splash_response: scrapy.http.Response = await maybe_deferred_to_future(
                    spider.crawler.engine.download(request_splash)
                )
                if splash_response and splash_response.status != 200:
                    log.debug(f"SPLASH could not handle the requested website. "
                              f"(Splash returned HTTP Status {splash_response.status} for {target_url} !)")
                    _splash_success = False
                    # ToDo (optional): more granular Error-Handling for unsupported URLs?
                    if splash_response.status == 415:
                        log.debug(f"SPLASH (HTTP Status {splash_response.status} -> Unsupported Media Type): "
                                  f"Could not render target url {target_url}")
                elif splash_response:
                    response: scrapy.http.Response = splash_response
                else:
                    log.debug(f"SPLASH returned HTTP Status {splash_response.status} for {target_url} ")

            playwright_websocket_endpoint: str | None = env.get("PLAYWRIGHT_WS_ENDPOINT")
            if (not bool(_splash_success) and playwright_websocket_endpoint
                    or playwright_websocket_endpoint and web_tools == WebEngine.Playwright):
                # we're using Playwright to take a website screenshot if:
                # - the spider explicitly defined Playwright in its 'custom_settings'-dict
                # - or: Splash failed to render a website (= fallback)
                # - or: the thumbnail URL could not be downloaded (= fallback)

                # this edge-case is necessary for spiders that only need playwright to gather a screenshot,
                # but don't use playwright within the spider itself
                target_url: str = item["lom"]["technical"]["location"][0]
                playwright_dict = await WebTools.getUrlData(url=target_url,
                                                            engine=WebEngine.Playwright)
                screenshot_bytes = playwright_dict.get("screenshot_bytes")
                img = Image.open(BytesIO(screenshot_bytes))
                self.create_thumbnails_from_image_bytes(img, item, settings_crawler)
            else:
                if settings_crawler.get("DISABLE_SPLASH") is False:
                    log.warning(
                        "No thumbnail provided (and .env variable 'SPLASH_URL' was not configured for screenshots!)"
                    )
        if response is None:
            if settings_crawler.get("DISABLE_SPLASH") is False:
                log.error(
                    "Neither thumbnail or technical.location (and technical.format) provided! "
                    "Please provide at least one of them"
                )
        else:
            try:
                if response.headers["Content-Type"] == b"image/svg+xml":
                    if len(response.body) > settings_crawler.get("THUMBNAIL_MAX_SIZE"):
                        raise Exception(
                            "SVG images can't be converted, and the given image exceeds the maximum allowed size ("
                            + str(len(response.body))
                            + " > "
                            + str(settings_crawler.get("THUMBNAIL_MAX_SIZE"))
                            + ")"
                        )
                    item["thumbnail"] = {}
                    _mimetype: bytes = response.headers["Content-Type"]
                    if _mimetype and isinstance(_mimetype, bytes):
                        item["thumbnail"]["mimetype"] = _mimetype.decode()
                    elif _mimetype and isinstance(_mimetype, str):
                        item["thumbnail"]["mimetype"] = _mimetype
                    item["thumbnail"]["small"] = base64.b64encode(
                        response.body
                    ).decode()
                else:
                    img = Image.open(BytesIO(response.body))
                    self.create_thumbnails_from_image_bytes(img, item, settings_crawler)
            except PIL.UnidentifiedImageError:
                # this error can be observed when a website serves broken / malformed images
                if url:
                    log.warning(f"Thumbnail download of image file {url} failed: image file could not be identified "
                                f"(Image might be broken or corrupt). Falling back to website-screenshot.")
                del item["thumbnail"]
                return await self.process_item(raw_item, spider)
            except Exception as e:
                if url is not None:
                    log.warning(f"Could not read thumbnail at {url}: {str(e)} (falling back to screenshot)")
                    raise e
                if "thumbnail" in item:
                    del item["thumbnail"]
                    return await self.process_item(raw_item, spider)
                else:
                    # item['thumbnail']={}
                    raise DropItem(
                        "No thumbnail provided or resource was unavailable for fetching"
                    )
        return raw_item

    @alru_cache(maxsize=128)
    async def download_thumbnail_url(self, url: str, spider: scrapy.Spider):
        """
        Download a thumbnail URL and **caches** the result.

        The cache works similarly to Python's built-in `functools.lru_cache`-decorator and discards the
        least recently used items first.
        (see: https://github.com/aio-libs/async-lru)

        Typical use-case:
        Some webhosters serve generic placeholder images as their default thumbnail.
        By caching the response of such URLs, we can save a significant amount of time and traffic.

        :param spider: The spider process that collected the URL.
        :param url: URL of a thumbnail/image.
        :return: Response or None
        """
        try:
            request = scrapy.Request(url=url, callback=NO_CALLBACK, priority=1)
            # Thumbnail downloads will be executed with a slightly higher priority (default: 0), so there's less delay
            # between metadata processing and thumbnail retrieval steps in the pipelines
            response: Deferred | Future = await maybe_deferred_to_future(
                spider.crawler.engine.download(request)
            )
            return response
        except ValueError:
            log.debug(f"Thumbnail-Pipeline received an invalid URL: {url}")

    # override the project settings with the given ones from the current spider
    # see PR 56 for details

    def create_thumbnails_from_image_bytes(self, image: Image.Image, item, settings):
        small_buffer: BytesIO = BytesIO()
        large_buffer: BytesIO = BytesIO()
        if image.format == "PNG":
            # PNG images with image.mode == "RGBA" cannot be converted cleanly to JPEG,
            # which is why we're handling PNGs separately
            small_copy = image.copy()
            large_copy = image.copy()
            # Pillow modifies the image object in place -> remember to use the correct copy
            small_copy.thumbnail(size=(250, 250))
            large_copy.thumbnail(size=(800, 800))
            # ToDo:
            #  Rework settings.py thumbnail config to retrieve values as width & height instead of sum(int)
            small_copy.save(small_buffer, format="PNG")
            large_copy.save(large_buffer, format="PNG")
            item["thumbnail"] = {}
            item["thumbnail"]["mimetype"] = "image/png"
            item["thumbnail"]["small"] = base64.b64encode(large_buffer.getvalue()).decode()
            item["thumbnail"]["large"] = base64.b64encode(large_buffer.getvalue()).decode()
        else:
            self.scale_image(image, settings.get("THUMBNAIL_SMALL_SIZE")).save(
                small_buffer,
                "JPEG",
                mode="RGB",
                quality=settings.get("THUMBNAIL_SMALL_QUALITY"),
            )
            self.scale_image(image, settings.get("THUMBNAIL_LARGE_SIZE")).save(
                large_buffer,
                "JPEG",
                mode="RGB",
                quality=settings.get("THUMBNAIL_LARGE_QUALITY"),
            )
            item["thumbnail"] = {}
            item["thumbnail"]["mimetype"] = "image/jpeg"
            item["thumbnail"]["small"] = base64.b64encode(
                small_buffer.getvalue()
            ).decode()
            item["thumbnail"]["large"] = base64.b64encode(
                large_buffer.getvalue()
            ).decode()


def get_settings_for_crawler(spider) -> scrapy.settings.Settings:
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
                "The spider did not provide a hash on the base object. "
                "The hash is required to detect changes on an element. "
                "(You should use the last modified date or something similar, "
                "e.g. '<date_modified_str>v<crawler_version>')"
            )
            item["hash"] = time.time()

        # @TODO: May this can be done only once?
        if self.find_source(spider) is None:
            log.info("create new source " + spider.name)
            self.create_source(spider)

        db_item = self.find_item(item["sourceId"], spider)
        if db_item:
            if item["hash"] != db_item[1]:
                log.debug(f"hash has changed, continuing pipelines for item {item['sourceId']}")
            else:
                log.debug(f"hash unchanged, skipping item {item['sourceId']}")
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

    def open_spider(self, spider):
        logging.debug("Entering EduSharingStorePipeline...\n"
                      "Checking if 'crawler source template' ('Quellendatensatz-Template') should be used "
                      "(see: 'EDU_SHARING_SOURCE_TEMPLATE_ENABLED' .env setting)...")
        est_enabled: bool = env.get_bool("EDU_SHARING_SOURCE_TEMPLATE_ENABLED", allow_null=True, default=False)
        # defaults to False for backwards-compatibility.
        # (The EduSharingSourceTemplateHelper class is explicitly set to throw errors and abort a crawl if this setting
        # is enabled! Activate this setting on a per-crawler basis!)
        if est_enabled:
            # "Quellendatensatz-Templates" might not be available on every edu-sharing instance. This feature is only
            # active if explicitly set via the .env file. (This choice was made to avoid errors with
            # old or unsupported crawlers.)
            est_helper: EduSharingSourceTemplateHelper = EduSharingSourceTemplateHelper(crawler_name=spider.name)
            whitelisted_properties: dict | None = est_helper.get_whitelisted_metadata_properties()
            if whitelisted_properties:
                setattr(spider, "edu_sharing_source_template_whitelist", whitelisted_properties)
                logging.debug(f"Edu-sharing source template retrieval was successful. "
                              f"The following metadata properties will be whitelisted for all items:\n"
                              f"{whitelisted_properties}")
            else:
                logging.error(f"Edu-Sharing Source Template retrieval failed. "
                              f"(Does a 'Quellendatensatz' exist in the edu-sharing repository for this spider?)")
        else:
            log.debug(f"Edu-Sharing Source Template feature is NOT ENABLED. Continuing EduSharingStorePipeline...")

    async def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        title = "<no title>"
        if "title" in item["lom"]["general"]:
            title = str(item["lom"]["general"]["title"])
        entryUUID = EduSharing.build_uuid(item["response"]["url"] if "url" in item["response"] else item["hash"])
        await self.insert_item(spider, entryUUID, item)
        log.info("item " + entryUUID + " inserted/updated")

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
    DISCIPLINE_TO_LISUM_SHORTHAND = {
        "020": "C-WAT",         # Arbeitslehre -> Wirtschaft, Arbeit, Technik
        "060": "C-KU",          # Bildende Kunst
        "080": "C-BIO",         # Biologie
        "100": "C-CH",          # Chemie
        "120": "C-DE",          # Deutsch
        "160": "C-Eth",         # Ethik
        "200": "C-FS",          # Fremdsprachen
        "220": "C-GEO",         # Geographie,
        "240": "C-GE",          # Geschichte
        "260": "B-GES",         # Gesundheit -> Gesundheitsförderung
        "320": "C-Inf",         # Informatik
        "380": "C-MA",          # Mathematik
        "400": "B-BCM",         # Medienerziehung / Medienpädagogik -> Basiscurriculum Medienbildung
        "420": "C-MU",          # Musik
        "450": "C-Phil",        # Philosophie
        "460": "C-Ph",          # Physik
        "480": "C-PB",          # Politische Bildung
        "510": "C-Psy",         # Psychologie
        "520": "C-LER",         # Religion -> Lebensgestaltung-Ethik-Religionskunde
        "560": "B-SE",          # Sexualerziehung
        # "600": "",              # ToDo: "Sport" is not available as a Lisum Rahmenlehrplan shorthand
        "660": "B-MB",          # Verkehrserziehung -> "Mobilitätsbildung und Verkehrserziehung"
        "700": "C-SOWI",        # Wirtschaftskunde -> "Sozialwissenschaft/Wirtschaftswissenschaft"
        "900": "B-BCM",         # Medienbildung -> "Basiscurriculum Medienbildung"
        "12002": "C-Thea",      # Darstellendes Spiel, Schultheater -> Theater
        "20001": "C-EN",        # Englisch
        "20002": "C-FR",        # Französisch
        "20003": "C-AGR",       # Griechisch -> Altgriechisch
        "20004": "C-IT",        # Italienisch
        "20005": "C-La",        # Latein
        "20006": "C-RU",        # Russisch
        "20007": "C-ES",        # Spanisch
        "20008": "C-TR",        # Türkisch
        "20011": "C-PL",        # Polnisch
        "20014": "C-PT",        # Portugiesisch
        "20041": "C-ZH",        # Chinesisch
        "28010": "C-SU",        # Sachkunde -> Sachunterricht
        "32002": "C-Inf",       # Informatik
        "46014": "C-AS",        # Astronomie
        "48005": "C-GEWIWI",    # Gesellschaftspolitische Gegenwartsfragen -> Gesellschaftswissenschaften
        "2800506": "C-PL",      # Polnisch
    }

    EAFCODE_EXCLUSIONS = [
        # eafCodes in this list are used as keys in
        # https://github.com/openeduhub/oeh-metadata-vocabs/blob/master/discipline.ttl
        # but are not part of the (standard) http://agmud.de/wp-content/uploads/2021/09/eafsys.txt
        '04010',  # OEH: "Körperpflege" <-> eafCode 04010: "Mechatronik"
        '20090',  # OEH: "Esperanto" <-> eafCode: 20080
        '44099',  # "Open Educational Resources"
        '64018',  # "Nachhaltigkeit"
        '72001',  # "Zeitgemäße Bildung"
        '900',  # Medienbildung
        '999',  # Sonstiges
        'niederdeutsch',
        'oeh01',  # "Arbeit, Ernährung, Soziales"
        'oeh04010'  # OEH: "Mechatronik" <-> eafCode: 04010 (Mechatronik)
    ]

    EDUCATIONALCONTEXT_TO_LISUM = {
        "elementarbereich": "pre-school",
        "grundschule": "primary school",
        "sekundarstufe_1": "lower secondary school",
        "sekundarstufe_2": "upper secondary school",
        "berufliche_bildung": "vocational education",
        "fortbildung": "professional development",
        "erwachsenenbildung": "continuing education",
        "foerderschule": "special education",
        # "fernunterricht": ""  # does not exist in Lisum valuespace
    }

    LRT_OEH_TO_LISUM = {
        # LRT-values that aren't listed here, can be mapped 1:1
        "audiovisual_medium": ["audio", "video"],
        "open_activity": "",  # exists in 2 out of 60.000 items
        "broadcast": "audio",
        "demonstration": ["demonstration", "image"],  # "Veranschaulichung"
    }

    def process_item(self, item: BaseItem, spider: scrapy.Spider) -> Optional[scrapy.Item]:
        """
        Takes a BaseItem and transforms its metadata-values to Lisum-metadataset-compatible values.
        Touches the following fields within the BaseItem:
        - base.custom
        - valuespaces.discipline
        - valuespaces.educationalContext
        - valuespaces.intendedEndUserRole
        - valuespaces.learningResourceType
        """
        base_item_adapter = ItemAdapter(item)
        discipline_lisum_keys = set()
        discipline_eafcodes = set()
        sodix_lisum_custom_lrts = set()
        if base_item_adapter.get("custom"):
            custom_field = base_item_adapter.get("custom")
            if "ccm:taxonentry" in custom_field:
                taxon_entries: list = custom_field.get("ccm:taxonentry")
                # first round of mapping from SODIX eafCodes to 'ccm:taxonid'
                if taxon_entries:
                    for taxon_entry in taxon_entries:
                        if taxon_entry in self.DISCIPLINE_TO_LISUM_SHORTHAND:
                            discipline_lisum_keys.add(self.DISCIPLINE_TO_LISUM_SHORTHAND.get(taxon_entry))
        if base_item_adapter.get("valuespaces"):
            valuespaces = base_item_adapter.get("valuespaces")
            if valuespaces.get("discipline"):
                discipline_list = valuespaces.get("discipline")
                # a singular entry will look like 'http://w3id.org/openeduhub/vocabs/discipline/380'
                # the last part of the URL string equals to a corresponding eafCode
                # (see: http://agmud.de/wp-content/uploads/2021/09/eafsys.txt)
                # this eafCode (key) gets mapped to Lisum specific B-B shorthands like "C-MA"
                if discipline_list:
                    for discipline_w3id in discipline_list:
                        discipline_eaf_code: str = discipline_w3id.split(sep='/')[-1]
                        eaf_code_digits_only_regex: re.Pattern = re.compile(r'\d{3,}')
                        match discipline_eaf_code in self.DISCIPLINE_TO_LISUM_SHORTHAND:
                            case True:
                                discipline_lisum_keys.add(self.DISCIPLINE_TO_LISUM_SHORTHAND.get(discipline_eaf_code))
                                # ToDo: there are no Sodix eafCode-values for these Lisum keys:
                                #  - Deutsche Gebärdensprache (C-DGS)
                                #  - Hebräisch (C-HE)
                                #  - Japanisch (C-JP)
                                #  - Naturwissenschaften (5/6) (= C-NW56)
                                #  - Naturwissenschaften (C-NW)
                                #  - Neu Griechisch (C-EL)
                                #  - Sorbisch/Wendisch (C-SW)
                            case _:
                                # due to having the 'custom'-field as a (raw) list of all eafCodes, this mainly serves
                                # the purpose of reminding us if a 'discipline'-value couldn't be mapped to Lisum
                                log.debug(f"LisumPipeline failed to map from eafCode {discipline_eaf_code} "
                                              f"to its corresponding 'ccm:taxonid' short-handle. Trying Fallback...")
                        match discipline_eaf_code:
                            # catching edge-cases where OEH 'discipline'-vocab-keys don't line up with eafsys.txt values
                            case "320":
                                discipline_eafcodes.add("32002")  # Informatik
                            case "20090":
                                discipline_eafcodes.add("20080")  # Esperanto
                            case "oeh04010":
                                discipline_eafcodes.add("04010")  # Mechatronik
                            case "04010":
                                discipline_eafcodes.add("2600103")  # Körperpflege
                        if eaf_code_digits_only_regex.search(discipline_eaf_code):
                            # each numerical eafCode must have a length of (minimum) 3 digits to be considered valid
                            log.debug(f"LisumPipeline: Writing eafCode {discipline_eaf_code} to buffer. (Wil be "
                                          f"used later for 'ccm:taxonentry').")
                            if discipline_eaf_code not in self.EAFCODE_EXCLUSIONS:
                                # making sure to only save eafCodes that are part of the standard eafsys.txt
                                discipline_eafcodes.add(discipline_eaf_code)
                            else:
                                log.debug(f"LisumPipeline: eafCode {discipline_eaf_code} is not part of 'EAF "
                                              f"Sachgebietssystematik' (see: eafsys.txt), therefore skipping this "
                                              f"value.")
                        else:
                            # our 'discipline.ttl'-vocab holds custom keys (e.g. 'niederdeutsch', 'oeh04010') which
                            # shouldn't be saved into 'ccm:taxonentry' (since they are not part of the regular
                            # "EAF Sachgebietssystematik"
                            log.debug(f"LisumPipeline eafCode fallback for {discipline_eaf_code} to "
                                          f"'ccm:taxonentry' was not possible. Only eafCodes with a minimum length "
                                          f"of 3+ digits are valid. (Please confirm if the provided value is part of "
                                          f"the 'EAF Sachgebietssystematik' (see: eafsys.txt))")
                log.debug(f"LisumPipeline: Mapping discipline values from \n {discipline_list} \n to "
                              f"LisumPipeline: discipline_lisum_keys \n {discipline_lisum_keys}")
                valuespaces["discipline"] = list()  # clearing 'discipline'-field, so we don't accidentally write the
                # remaining OEH w3id-URLs to Lisum's 'ccm:taxonid'-field

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
                                log.debug(f"LisumPipeline: educationalContext {educational_context_w3id_key} "
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
                            if lrt_w3id and type(lrt_w3id) is str:
                                # making sure to exclude '' strings from populating the list
                                lrt_temporary_list.append(lrt_w3id)
                            elif lrt_w3id and type(lrt_w3id) is list:
                                lrt_temporary_list.extend(lrt_w3id)
                    lrt_list = list(set(lrt_temporary_list))
                # after everything is mapped, we're saving the (updated) list back to our LRT:
                valuespaces["learningResourceType"] = lrt_list

            # Mapping from valuespaces_raw["learningResourceType"]: "INTERAKTION" -> "interactive_material"
            # (edge-cases like "INTERAKTION" don't exist in the OEH 'learningResourceType'-vocab, therfore wouldn't be
            # available in valuespaces)
            if base_item_adapter.get("valuespaces_raw"):
                vs_raw: dict = base_item_adapter.get("valuespaces_raw")
                if "learningResourceType" in vs_raw:
                    raw_lrt: list = vs_raw.get("learningResourceType")
                    for raw_lrt_item in raw_lrt:
                        if raw_lrt_item == "INTERAKTION":
                            sodix_lisum_custom_lrts.add("interactive_material")
            if sodix_lisum_custom_lrts:
                # if there's any Sodix custom LRT values present (e.g. "INTERAKTION"):
                if valuespaces.get("learningResourceType"):
                    # extending the LRT-list if it was already available
                    lrt_list: list = valuespaces.get("learningResourceType")
                    lrt_list.extend(sodix_lisum_custom_lrts)
                    valuespaces["learningResourceType"] = lrt_list
                else:
                    # since most of the time there will be no LRT field available (if "INTERAKTION" is the only
                    # LRT value, it needs to be created)
                    lrt_list = list(sodix_lisum_custom_lrts)
                    valuespaces["learningResourceType"] = lrt_list

            if discipline_lisum_keys:
                discipline_lisum_keys = list(discipline_lisum_keys)
                discipline_lisum_keys.sort()
                valuespaces["discipline"] = discipline_lisum_keys  # only shorthand values are saved to 'ccm:taxonid'
            if discipline_eafcodes:
                # Fallback: saving 'discipline.ttl'-Vocab keys to eafCodes ('ccm:taxonentry')
                if base_item_adapter.get("custom"):
                    custom_field = base_item_adapter.get("custom")
                    if "ccm:taxonentry" in custom_field:
                        taxon_entries: list = custom_field.get("ccm:taxonentry")
                        if taxon_entries:
                            # if eafCodes already exist in the custom filed (e.g.: sodix_spider), we're making sure that
                            # there are no double entries of the same eafCode
                            taxon_set = set(taxon_entries)
                            taxon_set.update(discipline_eafcodes)
                            taxon_entries = list(taxon_set)
                            log.debug(f"LisumPipeline: Saving eafCodes {taxon_entries} to 'ccm:taxonentry'.")
                            base_item_adapter["custom"]["ccm:taxonentry"] = taxon_entries
                else:
                    # oeh_spider typically won't have neither the 'custom'-field nor the 'ccm:taxonentry'-field
                    # Therefore we have to create and fill it with the eafCodes that we gathered from our
                    # 'discipline'-vocabulary-keys.
                    discipline_eafcodes_list = list(discipline_eafcodes)
                    log.debug(f"LisumPipeline: Saving eafCodes {discipline_eafcodes_list} to 'ccm:taxonentry'.")
                    base_item_adapter.update(
                        {'custom': {
                            'ccm:taxonentry': discipline_eafcodes_list}})
                    base_item_adapter["custom"]["ccm:taxonentry"] = discipline_eafcodes_list
        return item
