from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib import parse

import jmespath
import requests
import scrapy

from converter.items import BaseItemLoader, LomGeneralItemloader, LomTechnicalItemLoader, LicenseItemLoader
from converter.spiders.base_classes.meta_base import SpiderBase
from .lom_base import LomBase


class PossibleTests:
    """
    https://klexikon.zum.de/api.php?action=query&format=json&list=allpages&aplimit=100&formatversion=2
    {
      "warnings": {
        "main": {
          "*": "Unrecognized parameter: 'formatversion'"
        }
      },
      ...
    } when api is too old for format v2

    aplimit=0 !
    https://klexikon.zum.de/api.php?action=query&format=json&list=allpages&aplimit=0&formatversion=2
    {
      "query-continue": {
        "allpages": {
          "apcontinue": "112"
        }
      },
      "warnings": {
        "main": {
          "*": "Unrecognized parameter: 'formatversion'"
        },
        "allpages": {
          "*": "aplimit may not be less than 1 (set to 0)"
        }
      },
      "query": {
        "allpages": [
          {
            "pageid": 1201,
            "ns": 0,
            "title": "1. Weltkrieg"
          }
        ]
      }
    }
    """


jmes_pageids = jmespath.compile('query.allpages[].pageid')
jmes_continue = jmespath.compile('continue')
jmes_title = jmespath.compile('parse.title')
jmes_categories = jmespath.compile('parse.categories[]."*"')
jmes_links = jmespath.compile('parse.links[]."*"')
jmes_description = jmespath.compile('parse.properties[?name==\'description\']."*" | [0]')
jmes_text = jmespath.compile('parse.text."*"')
jmes_pageid = jmespath.compile('parse.pageid')
jmes_revid = jmespath.compile('parse.revid')
log = logging.getLogger(__name__)


def _api_url(url) -> str:
    p = parse.urlparse(url)
    path = Path(p.path)
    api_path = path / 'api.php'
    return parse.urljoin(url, str(api_path))


class MediaWikiBase(LomBase, metaclass=SpiderBase):
    name = None
    url = None
    friendlyName = None
    version = None
    license = None

    _default_params = {
        'format': 'json',
        # 'formatversion': '2',
    }

    """
    The query action API: https://www.mediawiki.org/w/api.php?action=help&modules=query
    The allpages parameters
    https://www.mediawiki.org/w/api.php?action=help&modules=query%2Ballpages
    """
    _query_params = _default_params | {
        'action': 'query',
        'list': 'allpages',
        'aplimit': '100',
        'apfilterredir': 'nonredirects'  # ignore redirection pages
    }

    # _query_request_url = f"{_api_url(url)}?{parse.urlencode(_query_params)}"

    """
    The parse action API: https://www.mediawiki.org/w/api.php?action=help&modules=parse
    default for prop is:
    text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties|parsewarnings
    we're using pageid, revid, text, title, links, properties, categories
    """
    _parse_params = _default_params | {
        'action': 'parse',
        'prop': '|'.join([
            'text',  # Gives the parsed text of the wikitext.
            # 'langlinks',  # Gives the language links in the parsed wikitext.
            'categories',  # Gives the categories in the parsed wikitext.
            # 'categorieshtml',  # Gives the HTML version of the categories.
            'links',  # Gives the internal links in the parsed wikitext.
            # 'templates',  # Gives the templates in the parsed wikitext.
            # 'images',  # Gives the images in the parsed wikitext.
            # 'externallinks',  # Gives the external links in the parsed wikitext.
            # 'sections',  # Gives the sections in the parsed wikitext.
            'revid',  # Adds the revision ID of the parsed page.
            'displaytitle',  # Adds the title of the parsed wikitext.
            # 'subtitle',  # Adds the page subtitle for the parsed page.
            # 'headhtml',  # Gives parsed doctype, opening <html>, <head> element and opening <body> of the page.
            # 'modules',  # Gives the ResourceLoader modules used on the page.
            # 'jsconfigvars',  # Gives the JavaScript configuration variables specific to the page.
            # 'encodedjsconfigvars',  # Gives the JavaScript configuration variables specific to the page as a JSON string.
            # 'indicators',  # Gives the HTML of page status indicators used on the page.
            'iwlinks',  # Gives interwiki links in the parsed wikitext.
            # 'wikitext',  # Gives the original wikitext that was parsed.
            'properties',  # Gives various properties defined in the parsed wikitext.
            # 'limitreportdata',  # Gives the limit report in a structured way. Gives no data, when disablelimitreport is set.
            # 'limitreporthtml',  # Gives the HTML version of the limit report. Gives no data, when disablelimitreport is set.
            # 'parsetree',  # The XML parse tree of revision content (requires content model wikitext)
            # 'parsewarnings',  # Gives the warnings that occurred while parsing content.
            # 'headitems',  # Deprecated. Gives items to put in the <head> of the page.
        ])
    }

    keywords = {}

    def __init__(self, **kwargs):
        self.api_url = _api_url(self.url)
        super().__init__(**kwargs)

    def start_requests(self):
        keywords = json.loads(
            requests.get(
                "https://wirlernenonline.de/wp-json/wp/v2/tags/?per_page=100"
            ).content.decode("UTF-8")
        )
        for keyword in keywords:
            self.keywords[keyword["id"]] = keyword["name"]

        yield self.query_for_pages()

    def query_for_pages(self, continue_token: dict[str, str] = None):
        params = self._query_params
        if continue_token is None:
            continue_token = {}
        return scrapy.FormRequest(
            url=self.api_url,
            formdata=params | continue_token,
            callback=self.parse_page_query,
            headers={"Accept": "application/json"},
        )

    def parse_page_query(self, response: scrapy.http.Response):
        data = json.loads(response.body)
        pageids = jmes_pageids.search(data)
        for pageid in pageids:
            yield scrapy.FormRequest(
                url=self.api_url,
                formdata=self._parse_params | {'pageid': str(pageid)},
                callback=self.parse_page_data,
                cb_kwargs={"extra": data}
            )
        if 'batchcomplete' not in data:
            return
        if 'continue' not in data:
            return
        yield self.query_for_pages(jmes_continue.search(data))

    def parse_page_data(self, response: scrapy.http.Response, extra=None):
        data = json.loads(response.body)
        response.meta['item'] = data
        response.meta['item_extra'] = extra
        if error := data.get('error', None):
            log.error(f"""
            | Wiki Error: {error}
            | for request {response.request.body}
            | extra data: {extra}
            """)
            return None

        return super().parse(response)

    def getId(self, response=None):
        data = response.meta['item']
        return jmes_pageid.search(data)

    def getHash(self, response=None):
        return str(jmes_revid.search(response.meta['item'])) + self.version

    def mapResponse(self, response, fetchData=True):
        mr = super().mapResponse(response, fetchData=False)
        data = json.loads(response.body)
        mr.replace_value('url', f'{self.url}wiki/{jmes_title.search(data)}')
        return mr

    def getBase(self, response=None) -> BaseItemLoader:
        # r: ParseResponse = response.meta["item"]
        loader = super().getBase(response)
        data = response.meta['item']
        # fulltext = r.parse.text
        text = jmes_text.search(response.meta['item'])
        if text is None:
            print('text of wikipage was empty:')
            print(f'{data}')
        loader.replace_value("fulltext", self.html2Text(text))  # crashes!
        return loader

    def getLOMGeneral(self, response=None) -> LomGeneralItemloader:
        # r: ParseResponse = response.meta["item"]
        loader = super().getLOMGeneral(response)
        data = response.meta['item']
        loader.replace_value('title', jmes_title.search(data))
        loader.add_value('keyword', jmes_links.search(data))
        loader.add_value('description', jmes_description.search(data))
        return loader

    def getLicense(self, response=None) -> LicenseItemLoader:
        loader = super().getLicense(response)
        loader.add_value('url', self.license)
        return loader

    def getLOMTechnical(self, response=None) -> LomTechnicalItemLoader:
        loader = super().getLOMTechnical(response)
        loader.replace_value('format', 'text/html')
        data = response.meta['item']
        title = jmes_title.search(data)
        loader.replace_value('location', f'{self.url}wiki/{title}')
        return loader

    def getValuespaces(self, response):
        loader = super().getValuespaces(response)
        data = response.meta['item']
        categories = jmes_categories.search(data)  # ['Ethik', 'Sekundarstufe_1']
        if categories:
            loader.add_value("discipline", categories)
            loader.add_value("educationalContext", categories)
            loader.add_value("intendedEndUserRole", categories)
        loader.add_value("new_lrt", "6b9748e4-fb3b-4082-ae08-c7a11c717256")  # "Wiki (dynamisch)"
        return loader
