import logging

from flask import request
from flask_restful import Resource
from valuespaces import Valuespaces


class Transform(Resource):
    def __init__(self):
        self.valuespaces = Valuespaces()

    def post(self):
        json = request.get_json(force=True)
        delete = []
        for key in json:
            # remap to new i18n layout
            mapped = []
            for entry in json[key]:
                i18n = {}
                valuespace = self.valuespaces.data[key]
                found = False
                for v in valuespace:
                    labels = list(v["prefLabel"].values())
                    if "altLabel" in v:
                        labels += list(v["altLabel"].values())
                    labels = list(map(lambda x: x.casefold(), labels))
                    if v["id"].endswith(entry) or entry.casefold() in labels:
                        i18n["key"] = v["id"]
                        i18n["de"] = v["prefLabel"]["de"]
                        try:
                            i18n["en"] = v["prefLabel"]["en"]
                        except KeyError:
                            logging.debug(f"Valuespace transformer: No English 'prefLabel' for {i18n['de']} available.")
                            pass
                        found = True
                        break
                if found and len(list(filter(lambda x: x["key"] == i18n["key"], mapped))) == 0:
                    mapped.append(i18n)
            if len(mapped):
                json[key] = mapped
            else:
                delete.append(key)
        for key in delete:
            del json[key]

        return json
