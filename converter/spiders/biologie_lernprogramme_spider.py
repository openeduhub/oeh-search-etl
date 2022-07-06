import re

from scrapy import Request
from scrapy.spiders import CrawlSpider

from converter.constants import Constants
from .base_classes import LernprogrammeSpiderBase


class BiologieLernprogrammeSpider(LernprogrammeSpiderBase, CrawlSpider):
    name = "biologie_lernprogramme_spider"
    friendlyName = "Biologie-Lernprogramme"
    url = "https://biologie-lernprogramme.de/"
    version = "0.1.1"  # last update: 2022-02-22
    custom_settings = {
        "ROBOTSTXT_OBEY": False
    }

    static_values = {
        "author": {
            "first_name": "Joachim",
            "last_name": "Jakob",
        },
        "format": "text/html",
        "language": "de",
        "licence_url": "https://creativecommons.org/licenses/by/4.0/legalcode",
        "skos": {
            "new_lrt": Constants.NEW_LRT_MATERIAL,
            "learningResourceType": [
                "http://w3id.org/openeduhub/vocabs/learningResourceType/application",
                "http://w3id.org/openeduhub/vocabs/learningResourceType/web_page",
            ],
            "discipline": ["http://w3id.org/openeduhub/vocabs/discipline/080"],
            "intendedEndUserRole": [
                "http://w3id.org/openeduhub/vocabs/intendedEndUserRole/learner",
                "http://w3id.org/openeduhub/vocabs/intendedEndUserRole/teacher",
            ],
            "educationalContext": [
                "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_1",
                "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_2",
            ],
            "toolCategory": [
                "http://w3id.org/openeduhub/vocabs/toolCategory/interactive",
            ],
        },
    }

    start_urls = [
        "https://raw.githubusercontent.com/jakjkga/biologie-lernprogramme/master/00_metadaten/biologie-lernprogramme_metadaten.csv"
    ]

    exercises = {
        "static_value_overrides": {
            "format": "application/pdf",
            "skos": {
                "new_lrt": Constants.NEW_LRT_MATERIAL,
                "learningResourceType": [
                    "http://w3id.org/openeduhub/vocabs/learningResourceType/drill_and_practice"
                ],
                "toolCategory": [],
            },
        },
        "get_url": (
            lambda row: "https://biologie-lernprogramme.de/daten/ueb/ueb_{}.pdf".format(
                re.search(
                    "^https://biologie-lernprogramme.de/daten/programme/js/(.*?)(?:[-_]online)?(?:/|/index.html|.html)$",
                    row["url"],
                ).group(1)
            )
        ),
        "get_row_overrides": (
            lambda row: {
                "title": 'Übungsaufgaben zum Lernprogramm "{}"'.format(row["title"]),
                "description": "Lernprogramm zur Übung: {}".format(row["url"]),
                "thumbnail": "https://redaktion.openeduhub.net/edu-sharing/themes/default/images/common/mime-types/previews/file-pdf.svg",
            }
        ),
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)
