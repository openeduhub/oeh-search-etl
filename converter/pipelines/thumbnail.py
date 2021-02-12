import base64
import logging
from io import BytesIO

import requests
from PIL import Image
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

from converter.pipelines.bases import BasicPipeline
log = logging.getLogger(__name__)


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

    def process_item(self, item, spider):
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
                    return self.process_item(item, spider)
                else:
                    # item['thumbnail']={}
                    raise DropItem(
                        "No thumbnail provided or ressource was unavailable for fetching"
                    )
        return item
