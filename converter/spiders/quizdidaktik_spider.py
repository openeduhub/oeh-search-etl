import re

from converter.constants import Constants
from converter.spiders.lernprogramme_spider_base import LernprogrammeSpiderBase


class QuizdidaktikSpider(LernprogrammeSpiderBase):
    name = "quizdidaktik_spider"
    friendlyName = "Quizdidaktik"
    url = "https://quizdidaktik.de/"

    static_values = {
        "author": {
            "first_name": "Joachim",
            "last_name": "Jakob",
        },
        "type": Constants.TYPE_TOOL,
        "format": "text/html",
        "language": "de",
        "licence_url": "https://creativecommons.org/licenses/by/4.0/legalcode",
        "skos": {
            "learningResourceType": [
                "http://w3id.org/openeduhub/vocabs/learningResourceType/application",
                "http://w3id.org/openeduhub/vocabs/learningResourceType/web_page",
            ],
            "discipline": ["http://w3id.org/openeduhub/vocabs/discipline/120"],
            "intendedEndUserRole": [
                "http://w3id.org/openeduhub/vocabs/intendedEndUserRole/learner",
                "http://w3id.org/openeduhub/vocabs/intendedEndUserRole/teacher",
            ],
            "educationalContext": [
                "http://w3id.org/openeduhub/vocabs/educationalContext/grundschule",
                "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_1",
                "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_2",
            ],
            "toolCategory": [
                "http://w3id.org/openeduhub/vocabs/toolCategory/interactive",
            ],
        },
    }

    start_urls = [
        "https://raw.githubusercontent.com/jakjkga/quizdidaktik/master/00_metadaten/quizdidatik_metadaten.csv"
    ]

    exercises = None

    def map_row(self, row: dict) -> dict:
        return {
            **row,
            "thumbnail": "https://quizdidaktik.de/daten/img/vorschaubilder/{}".format(
                row["thumbnail"]
            ),
        }
