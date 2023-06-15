import asyncio
import logging
import re

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule, Spider

import z_api
from valuespace_converter.app.valuespaces import Valuespaces
from .base_classes import LrmiBase
from .. import env
from ..items import LicenseItemLoader
from ..web_tools import WebEngine, WebTools


# class GenericSpider(CrawlSpider, LrmiBase):

class GenericSpider(Spider, LrmiBase):
    name = "generic_spider"
    friendlyName = "generic_spider"  # name as shown in the search ui
    start_urls = ["https://www.planet-schule.de/schwerpunkt/total-phaenomenal-energie/sonnenenergie-film-100.html"]
    ROBOTSTXT_OBEY = False
    rules = [
        Rule(
            callback='parse'
        ),
    ]
    custom_settings = {
        'WEB_TOOLS': WebEngine.Playwright,
        "ROBOTSTXT_OBEY": False
    }
    clean_tags = ['nav', 'header', 'footer']
    prompts = {
        'description': 'Fasse folgenden Text in 3 Sätzen zusammen: %(text)s',
        'keyword': 'Liefere 4 Schlagworte für folgenden Text: %(text)s',
        'discipline': 'Für welche Schul bzw. Fachgebiete eignet sich folgender Text: %(text)s',
        'educationalContext': 'Für welche Bildungsstufe eignet sich folgender Text: %(text)s',
        'new_lrt': 'Welche Materialart im schulischen Kontext ist folgender Text: %(text)s',
        'intendedEndUserRole': 'Für welche Zielgruppen eignet sich folgender Text: %(text)s',
    }
    version = "0.1.2"
    valuespaces: Valuespaces
    z_api_text: z_api.AITextPromptsApi

    def __init__(self, **kwargs):
        # CrawlSpider.__init__(self, **kwargs)

        LrmiBase.__init__(self, **kwargs)

        self.valuespaces = Valuespaces()
        z_api_config = z_api.Configuration.get_default_copy()
        z_api_config.api_key = {'ai-prompt-token': env.get("Z_API_KEY", False)}
        z_api_client = z_api.ApiClient(configuration=z_api_config)
        self.z_api_text = z_api.AITextPromptsApi(z_api_client)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        if not self.hasChanged(response):
            return
        data = asyncio.run(WebTools.fetchDataPlaywright(response.url))
        response = response.copy()
        parsed_html = BeautifulSoup(data['content'], features='lxml')
        for tag in self.clean_tags:
            tags = parsed_html.find_all(tag) if parsed_html.find_all(tag) else []
            for t in tags:
                t.clear()
        crawler_ignore = parsed_html.find_all(name=None, attrs={'data-crawler': 'ignore'})
        for t in crawler_ignore:
            t.clear();
        html = parsed_html.prettify()
        data['parsed_html'] = parsed_html
        data['text'] = WebTools.html2Text(html)
        response.meta['data'] = data
        return LrmiBase.parse(self, response)

    # return a (stable) id of the source
    def getId(self, response):
        return response.url

    # return a stable hash to detect content changes
    # if there is no hash available, may use the current time as "always changing" info
    # Please include your crawler version as well
    def getHash(self, response):
        return self.version

    def getBase(self, response):
        base = LrmiBase.getBase(self, response)
        # optionally provide thumbnail. If empty, it will tried to be generated from the getLOMTechnical 'location' (if format is 'text/html')
        # base.add_value('thumbnail', 'https://url/to/thumbnail')
        return base

    def mapResponse(self, response):
        return LrmiBase.mapResponse(self, response, False)

    def getLOMGeneral(self, response):
        general = LrmiBase.getLOMGeneral(self, response)
        general.add_value("title", response.meta['data']['title'])
        # TODO: Map language based on z-api
        general.add_value(
            "language", "de"
        )
        general.add_value("description", self.resolve_z_api('description', response))
        general.add_value("keyword", self.resolve_z_api('keyword', response, split=True))
        return general

    def getLicense(self, response) -> LicenseItemLoader:
        license = LrmiBase.getLicense(self, response)
        author = response.meta['data']['parsed_html'].find('meta', {"name": "author"})
        if author:
            license.add_value('author', author.get_text())
        return license

    def getLOMTechnical(self, response):
        technical = LrmiBase.getLOMTechnical(self, response)
        technical.add_value("location", response.url)
        technical.add_value("format", "text/html")
        technical.add_value("size", len(response.body))
        return technical

    def getValuespaces(self, response):
        valuespaces = LrmiBase.getValuespaces(self, response)
        for v in ['educationalContext', 'discipline', 'educationalContext', 'intendedEndUserRole', 'new_lrt']:
            valuespaces.add_value(v,
                                  self.valuespaces.findInText(
                                      v, self.resolve_z_api(v, response)
                                  )
                                  )
        return valuespaces

    def resolve_z_api(self, field, response, split=False):
        prompt = self.prompts[field] % {
            'text': response.meta['data']['text'][:4000]
        }
        result = self.z_api_text.prompt(body=prompt)
        logging.info(result)
        result = result.responses[0].strip()
        # fix utf-8 chars
        # result = codecs.decode(result, 'unicode-escape')
        # data['text'] = data['text'].encode().decode('unicode-escape').encode('latin1').decode('utf-8')
        if split:
            result = list(map(lambda x: x.strip(), re.split(r"[,|\n]", result)))
        return result
