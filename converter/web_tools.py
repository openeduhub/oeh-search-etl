import asyncio
from enum import Enum

import html2text
import pyppeteer
import requests
from pyppeteer.browser import Browser, Page
from scrapy.utils.project import get_project_settings
import json

from converter import env


class WebEngine(Enum):
    # Splash (default engine)
    Splash = 'splash',
    # Pyppeteer is controlling a headless chrome
    Pyppeteer = 'pyppeteer'

class WebTools:

    def getUrlData(url, engine = WebEngine.Splash):
        if engine == WebEngine.Splash:
            return WebTools.__getUrlDataSplash(url)
        elif engine == WebEngine.Pyppeteer:
            return WebTools.__getUrlDataPyppeteer(url)

        raise Exception("Invalid engine")
    def __getUrlDataPyppeteer(url: str):
        # html = "test"
        html = asyncio.run(WebTools.fetchDataPyppeteer(url))
        return {"html": html, "text": WebTools.html2Text(html), "cookies": None, "har": None}
    def __getUrlDataSplash(url: str):
        settings = get_project_settings()
        html = None
        if settings.get("SPLASH_URL"):
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
                    "response_body": 1,
                },
            )
            data = result.content.decode("UTF-8")
            j = json.loads(data)
            html = j['html'] if 'html' in j else ''
            text = html
            text += '\n'.join(list(map(lambda x: x["html"], j["childFrames"]))) if 'childFrames' in j else ''
            cookies = result.cookies.get_dict()
            return {"html": html, "text": WebEngine.html2Text(text), "cookies": cookies, "har": json.dumps(j["har"])}
        else:
            return {"html": None, "text": None, "cookies": None, "har": None}
    async def fetchDataPyppeteer(url: str):
        browser = await pyppeteer.connect({
            'browserWSEndpoint': env.get('PYPPETEER_WS_ENDPOINT'),
            'logLevel': 'WARN'
        })
        page = await browser.newPage()
        await page.goto(url)
        content = await page.content()
        # await page.close()
        return content



    def html2Text(html):
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        return h.handle(html)
