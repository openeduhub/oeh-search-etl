import asyncio
import dataclasses
import json
import logging
from enum import Enum
from typing import Optional, Any

import html2text
import pyppeteer
import requests
from playwright.async_api import async_playwright, Cookie
from scrapy.utils.project import get_project_settings

from converter import env


class WebEngine(Enum):
    # Splash (default engine)
    Splash = ("splash",)
    # Pyppeteer is controlling a headless Chrome browser
    Pyppeteer = "pyppeteer"
    # Playwright is controlling a headless Chrome browser
    Playwright = "playwright"


@dataclasses.dataclass(frozen=True)
class URLData:
    html: str
    screenshot: bytes
    cookies: Optional[list[Cookie]] = None
    har: Optional[Any] = None

    @property
    def text(self) -> Optional[str]:
        if self.html is None:
            return None
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        return h.handle(self.html)

    def __getitem__(self, key: str) -> Any:
        # fixme: remove this and directly use the dataclass attributes in the crawlers instead of data["html"]
        if key == "screenshot_bytes":
            logging.warning("deprecated, use .screenshot")
            return self["screenshot"]
        return getattr(self, key)

    def get(self, key: str, default=None) -> Any:
        # fixme: remove this and directly use the dataclass attributes in the crawlers instead of data["html"]
        if key == "screenshot_bytes":
            logging.warning("deprecated, use .screenshot")
            return self.get("screenshot")
        return getattr(self, key, default)


class WebTools:

    @staticmethod
    def getUrlData(url: str, engine=WebEngine.Playwright) -> URLData:
        if engine == WebEngine.Splash:
            return WebTools.__getUrlDataSplash(url)
        elif engine == WebEngine.Pyppeteer:
            return WebTools.__getUrlDataPyppeteer(url)
        elif engine == WebEngine.Playwright:
            return asyncio.run(WebTools.fetchDataPlaywright(url))

        raise Exception("Invalid engine")

    @staticmethod
    def __getUrlDataPyppeteer(url: str) -> URLData:
        # html = "test"
        html = asyncio.run(WebTools.fetchDataPyppeteer(url))
        return URLData(html=html, cookies=None, har=None)

    @staticmethod
    def __getUrlDataSplash(url: str) -> URLData:
        settings = get_project_settings()
        # html = None
        if (
            settings.get("SPLASH_URL")
            and not url.endswith(".pdf")
            and not url.endswith(".docx")
        ):
            # Splash can't handle some binary direct-links (Splash will throw "LUA Error 400: Bad Request" as a result)
            # ToDo: which additional filetypes need to be added to the exclusion list? - media files (.mp3, mp4 etc.?)
            result = requests.post(
                settings.get("SPLASH_URL") + "/render.json",
                json={
                    "html": 1,
                    "iframes": 1,
                    "url": url,
                    "wait": settings.get("SPLASH_WAIT"),
                    "headers": settings.get("SPLASH_HEADERS"),
                    "script": 1,
                    "har": 1,
                    "png": 1,
                    "response_body": 1,
                },
            )
            data = result.content.decode("UTF-8")
            j = json.loads(data)
            html = j["html"] if "html" in j else None
            text = html
            text += (
                "\n".join(list(map(lambda x: x["html"], j["childFrames"])))
                if "childFrames" in j
                else ""
            )
            # fixme: do we really want the cookies of the communication with splash here?
            #        Or do we want the cookies that are part of the communication of splash with the actual content?
            #        Because those would be part of the har structure anyway.
            return URLData(
                html=html,
                # todo: make sure we initialize the screenshot bytes exactly the same way as it was previously
                #       done in the ProcessThumbnailPipeline where the screenshot was fetched via an initial
                #       request.
                screenshot=j["png"],
                har=json.dumps(j["har"]),
                cookies=result.cookies.get_dict()
            )
        else:
            return URLData(html="", screenshot=b"")

    @staticmethod
    async def fetchDataPyppeteer(url: str):
        browser = await pyppeteer.connect(
            {"browserWSEndpoint": env.get("PYPPETEER_WS_ENDPOINT"), "logLevel": "WARN"}
        )
        page = await browser.newPage()
        await page.goto(url)
        content = await page.content()
        # await page.close()
        return content

    @staticmethod
    async def fetchDataPlaywright(url: str) -> URLData:
        # relevant docs for this implementation: https://hub.docker.com/r/browserless/chrome#playwright and
        # https://playwright.dev/python/docs/api/class-browsertype#browser-type-connect-over-cdp
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(
                endpoint_url=env.get("PLAYWRIGHT_WS_ENDPOINT")
            )
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle", timeout=90000)
            # waits for page to fully load (= no network traffic for 500ms),
            # maximum timeout: 90s
            # ToDo: HAR / text / cookies
            #  if we are able to replicate the Splash response with all its fields, we could save traffic/Requests
            #  that are currently still being handled by Splash
            return URLData(
                html=await page.content(),
                screenshot=await page.screenshot(),
                cookies=None,
                har=None
            )


    @staticmethod
    def html2Text(html: str):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        return h.handle(html)
