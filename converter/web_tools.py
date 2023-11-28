import asyncio
import json
from asyncio import Semaphore
from enum import Enum

import html2text
import httpx
from playwright.async_api import async_playwright
from scrapy.utils.project import get_project_settings

from converter import env


class WebEngine(Enum):
    # Splash (default engine)
    Splash = 'splash',
    # Playwright is controlling a headless Chrome browser
    Playwright = 'playwright'


class WebTools:
    @staticmethod
    async def getUrlData(url: str, engine=WebEngine.Splash):
        sem: Semaphore = asyncio.Semaphore(value=10)
        # the headless browser can only handle 5 concurrent sessions and 5 items in the queue by default
        async with sem:
            if engine == WebEngine.Splash:
                return await WebTools.__getUrlDataSplash(url)
            elif engine == WebEngine.Playwright:
                return await WebTools.__getUrlDataPlaywright(url)

        raise Exception("Invalid engine")

    @staticmethod
    async def __getUrlDataPlaywright(url: str):
        playwright_dict = await WebTools.fetchDataPlaywright(url)
        html = playwright_dict.get("content")
        screenshot_bytes = playwright_dict.get("screenshot_bytes")
        return {"html": html,
                "text": WebTools.html2Text(html),
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
            # ToDo: HAR / text / cookies
            #  if we are able to replicate the Splash response with all its fields, we could save traffic/Requests
            #  that are currently still being handled by Splash
            # await page.close()
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
