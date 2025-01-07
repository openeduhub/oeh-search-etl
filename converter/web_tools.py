import json
import logging
from asyncio import Semaphore
from enum import Enum

import html2text
import httpx
import trafilatura
from converter import env
from loguru import logger
from playwright.async_api import async_playwright
from scrapy.utils.project import get_project_settings

logging.getLogger("trafilatura").setLevel(logging.INFO)  # trafilatura is quite spammy

ignored_file_extensions: list[str] = [
    # file extensions that cause unexpected behavior when trying to render them with a headless browser
    ".aac",
    ".avi",
    ".bin",
    ".bmp",
    ".bz",
    ".cda",
    ".csv",
    ".doc",
    ".docx",
    ".epub",
    ".gz",
    ".mbz",
    ".mid",
    ".midi",
    ".mp3",
    ".mp4",
    ".mpeg",
    ".mpkg",
    ".odp",
    ".ods",
    ".odt",
    ".oga",
    ".ogx",
    ".opus",
    ".otf",
    ".pdf",
    ".pptx",
    ".rar",
    ".rtf",
    ".sh",
    ".tar",
    ".ts",
    ".ttf",
    ".txt",
    ".vsd",
    ".wav",
    ".weba",
    ".webm",
    ".webp",
    ".xls",
    ".xlsx",
    ".zip",
    ".3gp",
    ".3g2",
    ".7z",
]


class WebEngine(Enum):
    # Splash (default engine)
    Splash = "splash"
    # Playwright is controlling a headless Chrome browser
    Playwright = "playwright"


class WebTools:
    _sem_splash: Semaphore = Semaphore(10)
    _sem_playwright: Semaphore = Semaphore(10)
    # reminder: if you increase this Semaphore value, you NEED to change the "browserless v2"-docker-container
    # configuration accordingly! (e.g., by increasing the MAX_CONCURRENT_SESSIONS and MAX_QUEUE_LENGTH configuration
    # settings, see: https://www.browserless.io/docs/docker)
    _playwright_cookies: list[dict] = list()
    _playwright_adblocker: bool = False

    @classmethod
    async def __safely_get_splash_response(cls, url: str):
        """Send a URL string to the Splash container for HTTP / Screenshot rendering if a Semaphore can be acquired.

        (The Semaphore is used to control / throttle the number of concurrent pending requests to the Splash container,
        which is necessary because Splash can only handle a specific number of connections at the same time.)
        """
        async with cls._sem_splash:
            return await WebTools.__getUrlDataSplash(url)

    @classmethod
    async def __safely_get_playwright_response(cls, url: str):
        """Send a URL string to the Playwright container ("browserless v2") for HTTP / Screenshot rendering if a
        Semaphore can be acquired.

        (The Semaphore is used to control / throttle the number of concurrent pending requests to the Playwright
        container, which is necessary because Playwright only allows a specific number of connections / requests in the
        queue at the same time.
        browserless v2 defaults to: 5 concurrent requests // 5 requests in the queue
        => Semaphore value of 10 should guarantee that neither the crawler nor the pipelines make more requests than the
        container is able to handle.)

        For details, see:
        https://www.browserless.io/docs/docker#max-concurrent-sessions
        https://www.browserless.io/docs/docker#max-queue-length
        """
        async with cls._sem_playwright:
            return await WebTools.__getUrlDataPlaywright(url)

    @classmethod
    def url_cant_be_rendered_by_headless_browsers(cls, url: str) -> bool:
        """Rudimentary check for problematic file extensions within a provided URL string.
        Returns True if a problematic extension was detected."""
        # ToDo:
        #  - extend the list of problematic file extensions as they occur during debugging
        #  - implement check for parametrized URLs (e.g. "<URL>/image.png?token=..." and other edge-cases
        if isinstance(url, str) and url:
            # checking if the provided URL is actually a string
            for file_extension in ignored_file_extensions:
                if url.endswith(file_extension):
                    logger.warning(
                        f"Problematic file extension {file_extension} detected in URL {url} ! "
                        f"Headless browsers can't render this file type."
                    )
                    return True
        else:
            logger.debug(f"URL {url} does not appear to be a string value. WebTools REQUIRE an URL string.")
            return False

    @classmethod
    async def getUrlData(cls, url: str,
                         engine: WebEngine = WebEngine.Playwright,
                         adblock: bool = None,
                         cookies: list[dict] = None):
        """
        Sends an HTTP request through one of the (dockerized) headless browsers for JavaScript-enabled HTML rendering.
        @param url: the to-be-rendered URL
        @param engine: the WebEngine of choice (either "Splash" or "Playwright")
        @param adblock: (playwright only!) block ads for this HTTP Request (via uBlock Origin) if set to True
        @param cookies: (playwright only!) a list of cookies (type: list[dict]) that shall be transmitted during the
        HTTP request
        @return:
        """
        url_contains_problematic_file_extension: bool = cls.url_cant_be_rendered_by_headless_browsers(url=url)
        if url_contains_problematic_file_extension:
            # most binary files cannot be rendered by Playwright or Splash and would cause unexpected behavior in the
            # Thumbnail Pipeline
            # ToDo: handle websites that redirect to binary downloads gracefully
            #   - maybe by checking the MIME-Type in response headers first?
            logger.warning(
                f"File extension in URL {url} detected which cannot be rendered by headless browsers. "
                f"Skipping WebTools rendering for this url..."
            )
            return
        if cookies:
            # sets the spider-specific cookies for Playwright requests (e.g., to skip a cookie banner)
            cls._playwright_cookies = cookies
        if adblock:
            # controls if the built-in adblocker of "browserless" should be enabled for Playwright
            cls._playwright_adblocker = adblock
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

    @classmethod
    async def fetchDataPlaywright(cls, url: str):
        # relevant docs for this implementation: https://hub.docker.com/r/browserless/chrome#playwright and
        # https://playwright.dev/python/docs/api/class-browsertype#browser-type-connect-over-cdp
        async with async_playwright() as p:
            ws_cdp_endpoint = f"{env.get("PLAYWRIGHT_WS_ENDPOINT")}/chrome/playwright"
            if cls._playwright_adblocker:
                # advertisements pollute the HTML body and obstruct website screenshots, which is why we try to block
                # them from rendering via the built-in adblocker (uBlock Origin) of the browserless docker image.
                # see: https://docs.browserless.io/chrome-flags/#blocking-ads
                ws_cdp_endpoint = f"{ws_cdp_endpoint}?blockAds=true"
            browser = await p.chromium.connect(ws_endpoint=ws_cdp_endpoint)
            browser_context = await browser.new_context()
            if cls._playwright_cookies:
                # Some websites may require setting specific cookies to render properly
                # (e.g., to skip or close annoying cookie banners).
                # Playwright supports passing cookies to requests
                # see: https://playwright.dev/python/docs/api/class-browsercontext#browser-context-add-cookies
                logger.debug(f"Preparing cookies for Playwright HTTP request...")
                prepared_cookies: list[dict] = list()
                for cookie_object in cls._playwright_cookies:
                    if isinstance(cookie_object, dict):
                        # Playwright expects a list[dict]!
                        # Each cookie must have the following (REQUIRED) properties:
                        # "name" (type: str), "value" (type: str) and "url" (type: str)
                        if "name" in cookie_object and "value" in cookie_object:
                            cookie = {
                                "name": cookie_object["name"],
                                "value": cookie_object["value"],
                                "url": url
                            }
                            prepared_cookies.append(cookie)
                        else:
                            logger.warning(f"Cannot set custom cookie for Playwright (headless browser) request due to "
                                        f"missing properties: 'name' and 'value' are REQUIRED attributes "
                                        f"within a cookie object (type: dict)! "
                                        f"Discarding cookie: {cookie_object}")
                if prepared_cookies and isinstance(prepared_cookies, list):
                    await browser_context.add_cookies(cookies=prepared_cookies)
            page = await browser_context.new_page()
            await page.goto(url, wait_until="load", timeout=90000)
            # waits for a website to fire the "load" event or for a timeout of 90 seconds
            # (since waiting for "networkidle" seems to cause timeouts)
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
