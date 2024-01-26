from __future__ import annotations

import json
import logging
import urllib.parse
from pathlib import Path
from urllib import parse

import jmespath
import requests
import scrapy
import trafilatura

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


jmes_pageids = jmespath.compile("query.allpages[].pageid")
jmes_continue = jmespath.compile("continue")
jmes_title = jmespath.compile("parse.title")
jmes_categories = jmespath.compile('parse.categories[]."*"')
jmes_links = jmespath.compile('parse.links[]."*"')
jmes_description = jmespath.compile("parse.properties[?name=='description'].\"*\" | [0]")
jmes_text = jmespath.compile('parse.text."*"')
jmes_pageid = jmespath.compile("parse.pageid")
jmes_revid = jmespath.compile("parse.revid")


def _api_url(url) -> str:
    p = parse.urlparse(url)
    path = Path(p.path)
    api_path = path / "api.php"
    return parse.urljoin(url, str(api_path))


class MediaWikiBase(LomBase, metaclass=SpiderBase):
    name = None
    url = None
    friendlyName = None
    version = None
    license = None

    _default_params = {
        "format": "json",
        # 'formatversion': '2',
    }

    """
    The query action API: https://www.mediawiki.org/w/api.php?action=help&modules=query
    The allpages parameters
    https://www.mediawiki.org/w/api.php?action=help&modules=query%2Ballpages
    """
    _query_params = _default_params | {
        "action": "query",
        "list": "allpages",
        "aplimit": "500",  # Values between 1 and 500 are allowed by MediaWiki APIs
        "apfilterredir": "nonredirects",  # ignore redirection pages
    }

    # _query_request_url = f"{_api_url(url)}?{parse.urlencode(_query_params)}"

    """
    The parse action API: https://www.mediawiki.org/w/api.php?action=help&modules=parse
    default for prop is:
    text|langlinks|categories|links|templates|images|externallinks|sections|revid|displaytitle|iwlinks|properties|parsewarnings
    we're using pageid, revid, text, title, links, properties, categories
    """
    _parse_params = _default_params | {
        "action": "parse",
        "prop": "|".join(
            [
                "text",  # Gives the parsed text of the wikitext.
                # 'langlinks',  # Gives the language links in the parsed wikitext.
                "categories",  # Gives the categories in the parsed wikitext.
                # 'categorieshtml',  # Gives the HTML version of the categories.
                "links",  # Gives the internal links in the parsed wikitext.
                # 'templates',  # Gives the templates in the parsed wikitext.
                # 'images',  # Gives the images in the parsed wikitext.
                # 'externallinks',  # Gives the external links in the parsed wikitext.
                # 'sections',  # Gives the sections in the parsed wikitext.
                "revid",  # Adds the revision ID of the parsed page.
                "displaytitle",  # Adds the title of the parsed wikitext.
                # 'subtitle',  # Adds the page subtitle for the parsed page.
                # 'headhtml',  # Gives parsed doctype, opening <html>, <head> element and opening <body> of the page.
                # 'modules',  # Gives the ResourceLoader modules used on the page.
                # 'jsconfigvars',  # Gives the JavaScript configuration variables specific to the page.
                # 'encodedjsconfigvars',  # Gives the JavaScript configuration variables specific to the page as a JSON string.
                # 'indicators',  # Gives the HTML of page status indicators used on the page.
                "iwlinks",  # Gives interwiki links in the parsed wikitext.
                # 'wikitext',  # Gives the original wikitext that was parsed.
                "properties",  # Gives various properties defined in the parsed wikitext.
                # 'limitreportdata',  # Gives the limit report in a structured way. Gives no data, when disablelimitreport is set.
                # 'limitreporthtml',  # Gives the HTML version of the limit report. Gives no data, when disablelimitreport is set.
                # 'parsetree',  # The XML parse tree of revision content (requires content model wikitext)
                # 'parsewarnings',  # Gives the warnings that occurred while parsing content.
                # 'headitems',  # Deprecated. Gives items to put in the <head> of the page.
            ]
        ),
    }

    keywords = {}

    def __init__(self, **kwargs):
        self.api_url = _api_url(self.url)
        super().__init__(**kwargs)

    def start_requests(self):
        keywords = json.loads(
            requests.get("https://wirlernenonline.de/wp-json/wp/v2/tags/?per_page=100").content.decode("UTF-8")
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
                formdata=self._parse_params | {"pageid": str(pageid)},
                callback=self.parse_page_data,
                cb_kwargs={"extra": data},
            )
        if "batchcomplete" not in data:
            return
        if "continue" not in data:
            return
        yield self.query_for_pages(jmes_continue.search(data))

    async def parse_page_data(self, response: scrapy.http.Response, extra=None):
        data = json.loads(response.body)
        response.meta["item"] = data
        response.meta["item_extra"] = extra
        if error := data.get("error", None):
            logging.error(
                f"""
            | Wiki Error: {error}
            | for request {response.request.body}
            | extra data: {extra}
            """
            )
            return None

        return await super().parse(response)

    def getId(self, response=None):
        data = response.meta["item"]
        return jmes_pageid.search(data)

    def getHash(self, response=None):
        return str(jmes_revid.search(response.meta["item"])) + self.version

    async def mapResponse(self, response, fetchData=True):
        mr = await super().mapResponse(response, fetchData=False)
        data = json.loads(response.body)
        title: str = jmes_title.search(data)
        title_underscored: str = title.replace(" ", "_")
        mr.replace_value("url", f"{self.url}{urllib.parse.quote('wiki/')}{urllib.parse.quote(title_underscored)}")
        # response.url can't be used for string concatenation here since it would point to "/api.php"
        # self.url is overwritten by the children of MediaWikiBase with the URL root
        return mr

    def getBase(self, response=None) -> BaseItemLoader:
        # r: ParseResponse = response.meta["item"]
        loader = super().getBase(response)
        data = response.meta["item"]
        text = jmes_text.search(response.meta["item"])
        if text is None:
            print("text of wikipage was empty:")
            print(f"{data}")
        trafilatura_text: str = trafilatura.extract(text)
        if trafilatura_text:
            loader.replace_value("fulltext", trafilatura_text)
        return loader

    def getLOMGeneral(self, response=None) -> LomGeneralItemloader:
        # r: ParseResponse = response.meta["item"]
        loader = super().getLOMGeneral(response)
        data = response.meta["item"]
        loader.replace_value("title", jmes_title.search(data))
        loader.add_value("keyword", jmes_links.search(data))
        loader.add_value("description", jmes_description.search(data))
        return loader

    def getLicense(self, response=None) -> LicenseItemLoader:
        loader = super().getLicense(response)
        loader.add_value("url", self.license)
        return loader

    def getLOMTechnical(self, response=None) -> LomTechnicalItemLoader:
        loader = super().getLOMTechnical(response)
        loader.replace_value("format", "text/html")
        data = response.meta["item"]
        title: str = jmes_title.search(data)
        title_underscored: str = title.replace(" ", "_")
        # Sommercamp 2023: MediaWiki generates URLs from the title by replacing whitespace chars with underscores.
        # Since these URLs can be used to query the edu-sharing 'getLRMI'-API-endpoint, we need to make sure that URLs
        # are saved in the same format.
        loader.replace_value(
            "location", f"{self.url}{urllib.parse.quote('wiki/')}{urllib.parse.quote(title_underscored)}"
        )
        return loader

    def getValuespaces(self, response):
        loader = super().getValuespaces(response)
        data = response.meta["item"]
        categories: list[str] = jmes_categories.search(data)  # ['Ethik', 'Sekundarstufe_1']
        # hard-coded values for all 3 ZUM crawlers as per feature-request on 2023-08-11 from Team4 (Romy):
        loader.add_value("conditionsOfAccess", "no_login")
        loader.add_value("price", "no")
        if categories:
            loader.add_value("discipline", categories)
            loader.add_value("educationalContext", categories)
            loader.add_value("intendedEndUserRole", categories)
            for category in categories:
                # ZUM MediaWiki "category"-strings can consist of several words. We're looking for individual parts of
                # the whole string and use a search-hit as our indicator to set the corresponding "new_lrt"-value.
                category: str = str(category).lower()
                if "arbeitsblatt" in category:
                    loader.add_value("new_lrt", "36e68792-6159-481d-a97b-2c00901f4f78")  # "Arbeitsblatt"
                if "erklärvideo" in category:
                    loader.add_value(
                        "new_lrt", "a0218a48-a008-4975-a62a-27b1a83d454f"
                    )  # "Erklärvideo und gefilmtes Experiment"
                if "lernpfad" in category:
                    loader.add_value("new_lrt", "ad9b9299-0913-40fb-8ad3-50c5fd367b6a")  # "Lernpfad, Lernobjekt"
                if "methode" in category:
                    loader.add_value("new_lrt", "0a79a1d0-583b-47ce-86a7-517ab352d796")  # "Methode"
                if "tool" in category:
                    loader.add_value("new_lrt", "cefccf75-cba3-427d-9a0f-35b4fedcbba1")  # "Tool"
                if "unterrichtsidee" in category:
                    loader.add_value("new_lrt", "94222751-6c90-4623-9c7e-09e21d885599")  # Unterrichtsidee
                if "video" in category:
                    loader.add_value("new_lrt", "7a6e9608-2554-4981-95dc-47ab9ba924de")  # "Video"
                if "übung" in category:
                    loader.add_value("new_lrt", "a33ef73d-9210-4305-97f9-7357bbf43486")  # "Übungsmaterial"
                if "glossar" in category:
                    loader.add_value("new_lrt", "c022c920-c236-4234-bae1-e264a3e2bdf6")  # "Nachschlagewerk und Glossar"
                if "fortbildung" in category:
                    loader.add_value("new_lrt", "4fe167ea-1f40-44b7-8c17-355f256b4fc9")  # "Fortbildungsangebot"
        loader.add_value("new_lrt", "6b9748e4-fb3b-4082-ae08-c7a11c717256")  # "Wiki (dynamisch)"
        return loader
