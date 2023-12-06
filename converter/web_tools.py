import json
from asyncio import Semaphore
from enum import Enum

import html2text
import httpx
import trafilatura
from playwright.async_api import async_playwright
from scrapy.utils.project import get_project_settings

from converter import env


class WebEngine(Enum):
    # Splash (default engine)
    Splash = 'splash',
    # Playwright is controlling a headless Chrome browser
    Playwright = 'playwright'


class WebTools:
    _sem_splash: Semaphore = Semaphore(10)
    _sem_playwright: Semaphore = Semaphore(10)

    @classmethod
    async def __safely_get_splash_response(cls, url: str):
        # ToDo: Docs
        async with cls._sem_splash:
            return await WebTools.__getUrlDataSplash(url)

    @classmethod
    async def __safely_get_playwright_response(cls, url: str):
        # ToDo: Docs
        async with cls._sem_playwright:
            return await WebTools.__getUrlDataPlaywright(url)

    @classmethod
    async def getUrlData(cls, url: str, engine: WebEngine = WebEngine.Playwright):
        if engine == WebEngine.Splash:
            return await cls.__safely_get_splash_response(url)
        elif engine == WebEngine.Playwright:
            return await cls.__safely_get_playwright_response(url)
        raise Exception("Invalid engine")

    @staticmethod
    async def __getUrlDataPlaywright(url: str):
        playwright_dict = await WebTools.fetchDataPlaywright(url)
        html: str = playwright_dict.get("content")
        screenshot_bytes: bytes = playwright_dict.get("screenshot_bytes")
        fulltext: str = WebTools.html2Text(html)
        if html and isinstance(html, str):
            html_bytes: bytes = html.encode()
            trafilatura_text: str | None = trafilatura.extract(html_bytes)
            if trafilatura_text:
                # trafilatura text extraction is (in general) more precise than html2Text, so we'll use it if available
                fulltext = trafilatura_text
        return {"html": html,
                "text": fulltext,
                "cookies": None,
                "har": None,
                "screenshot_bytes": screenshot_bytes}

    @staticmethod
    async def __getUrlDataSplash(url: str):
        settings = get_project_settings()
        # html = None
        if settings.get("SPLASH_URL") and not url.endswith(".pdf") and not url.endswith(".docx"):
            # Splash can't handle some binary direct-links (Splash will throw "LUA Error 400: Bad Request" as a result)
            # ToDo: which additional filetypes need to be added to the exclusion list? - media files (.mp3, mp4 etc.?)
            async with httpx.AsyncClient() as client:
                result = await client.post(
                    settings.get("SPLASH_URL") + "/render.json",
                    json={
                        "html": 1,
                        "iframes": 1,
                        "url": url,
                        "wait": settings.get("SPLASH_WAIT"),
                        "headers": settings.get("SPLASH_HEADERS"),
                        "script": 1,
                        "har": 1,
                        "response_body": 1,
                    },
                    timeout=30
                )
                data = result.content.decode("UTF-8")
                j = json.loads(data)
                html = j['html'] if 'html' in j else ''
                text = html
                text += '\n'.join(list(map(lambda x: x["html"], j["childFrames"]))) if 'childFrames' in j else ''
                cookies = dict(result.cookies)
                return {"html": html,
                        "text": WebTools.html2Text(text),
                        "cookies": cookies,
                        "har": json.dumps(j["har"])}
        else:
            return {"html": None, "text": None, "cookies": None, "har": None}

    @staticmethod
    async def fetchDataPlaywright(url: str):
        # relevant docs for this implementation: https://hub.docker.com/r/browserless/chrome#playwright and
        # https://playwright.dev/python/docs/api/class-browsertype#browser-type-connect-over-cdp
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(endpoint_url=env.get("PLAYWRIGHT_WS_ENDPOINT"))
            page = await browser.new_page()
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            # waits for a website to fire the DOMContentLoaded event or for a timeout of 90s
            # since waiting for 'networkidle' seems to cause timeouts
            content = await page.content()
            screenshot_bytes = await page.screenshot()
            # ToDo: HAR / cookies
            #  if we are able to replicate the Splash response with all its fields,
            #  we could save traffic/requests that are currently still being handled by Splash
            #  see: https://playwright.dev/python/docs/api/class-browsercontext#browser-context-cookies
            return {
                "content": content,
                "screenshot_bytes": screenshot_bytes
            }

    @staticmethod
    def html2Text(html: str):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        return h.handle(html)
