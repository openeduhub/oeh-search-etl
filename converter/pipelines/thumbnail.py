import asyncio
import base64
import json
import logging
from io import BytesIO
import aiohttp
import scrapy_splash

import scrapy.crawler
from PIL import Image
from typing import TypeVar
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
import hashlib
from urllib.parse import quote
from pathlib import Path

import scrapy
from itemadapter import ItemAdapter

from converter.pipelines.bases import BasicAsyncPipeline, PipelineWithPerSpiderMethods
log = logging.getLogger(__name__)
T = TypeVar('T')


class ProcessThumbnailPipeline(BasicAsyncPipeline):
    """
    generate thumbnails
    """

    def __init__(self):
        self._session: aiohttp.ClientSession = None
        self.lock = asyncio.Lock()

    async def session(self):
        if self._session:
            return self._session
        async with self.lock:
            if self._session:
                return self._session
            conn = aiohttp.TCPConnector(limit=30)
            self._session = aiohttp.ClientSession(connector=conn)
            return self._session

    @staticmethod
    def scale_image(img, max_size):
        w = float(img.width)
        h = float(img.height)
        while w * h > max_size:
            w *= 0.9
            h *= 0.9
        return img.resize((int(w), int(h)), Image.ANTIALIAS).convert("RGB")

    async def get_thumbnail(self, url):
        session = await self.session()
        async with session.get(url) as response:
            if response.ok:
                data = await response.read()
                return response, data
            return None, None

    async def screenshot_from_splash(self, location):
        settings = get_project_settings()
        session = await self.session()
        if not settings.get("SPLASH_URL"):
            if settings.get("DISABLE_SPLASH") is False:
                log.warning(
                    "No thumbnail provided and SPLASH_URL was not configured for screenshots!"
                )
                return
        payload = {
                "url": location,
                "wait": settings.get("SPLASH_WAIT"),
                "html5_media": 1,
                "headers": settings.get("SPLASH_HEADERS"),
            }
        async with session.post(settings.get("SPLASH_URL") + "/render.png", json=payload) as response:
            if response.ok:
                data = await response.read()
                return response, data
            return None, None

    async def process_item(self, item, spider):
        response = None
        data = None
        url = None
        settings = get_project_settings()
        if "thumbnail" in item:
            url = item["thumbnail"]
            response, data = await self.get_thumbnail(url)
            # log.debug(
            #     "Loading thumbnail took " + str(response.elapsed.total_seconds()) + "s"
            # )
        elif (
                "location" in item["lom"]["technical"]
                and "format" in item["lom"]["technical"]
                and item["lom"]["technical"]["format"] == "text/html"
        ):
            response, data = await self.screenshot_from_splash(item["lom"]["technical"]["location"])
        if response is None:
            if settings.get("DISABLE_SPLASH") is False:
                log.error(
                    "Neither thumbnail or technical.location (and technical.format) provided! Please provide at least one of them"
                )
            return item
        try:
            if response.headers["Content-Type"] == "image/svg+xml":
                if response.content_length > settings.get("THUMBNAIL_MAX_SIZE"):
                    raise Exception(
                        "SVG images can't be converted, and the given image exceeds the maximum allowed size ("
                        + str(response.content_length)
                        + " > "
                        + str(settings.get("THUMBNAIL_MAX_SIZE"))
                        + ")"
                    )
                item["thumbnail"] = {}
                item["thumbnail"]["mimetype"] = response.headers["Content-Type"]
                item["thumbnail"]["small"] = base64.b64encode(
                    data
                ).decode()
                return item
            data = await response.read()
            img = Image.open(BytesIO(data))
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
                return self.process_item(item, spider)
            else:
                # item['thumbnail']={}
                raise DropItem(
                    "No thumbnail provided or ressource was unavailable for fetching"
                )
        return item


class ScreenshotPipeline(BasicAsyncPipeline):
    """Pipeline that uses Splash to render screenshot of
    every Scrapy item.
    does not work with async :/
    """

    async def process_item(self, item, spider):
        settings = get_project_settings()
        if not settings.get("SPLASH_URL"):
            return item
        splash_url = settings.get("SPLASH_URL") + "/render.png"
        adapter = ItemAdapter(item)
        payload = {
                "url": adapter["lom"]["technical"]["location"],
                "wait": settings.get("SPLASH_WAIT"),
                "html5_media": 1,
                "headers": settings.get("SPLASH_HEADERS"),
        }
        headers = {b'content-type': b'application/json'}
        data = json.dumps(payload).encode()
        s_request = scrapy_splash.SplashRequest(adapter["lom"]["technical"]["location"], args=payload, endpoint='render.png')

        request = scrapy.http.Request(splash_url, method='POST', body=data, headers=headers)
        # print(type(spider.crawler.engine.download), type(spider.crawler.engine), type(spider.crawler.engine.download(request, spider)))
        response = spider.crawler.engine.download(s_request, spider)

        print(type(response))
        # FIXME: this await will fail, something's wrong in scrapy 2.4.1.
        result = await response
        print(type(result))
        if result.status != 200:
            # Error happened, return item.
            return item

        # Save screenshot to file, filename will be hash of url.
        url = adapter["url"]
        url_hash = hashlib.md5(url.encode("utf8")).hexdigest()
        filename = f"{url_hash}.png"
        filepath = Path.cwd() / 'screenshots' / spider.name / filename
        filepath.write_bytes(response.body)

        # Store filename in item.
        adapter["screenshot_filename"] = filepath
        return item
