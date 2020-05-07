from flask import request
from flask_restful import Resource, reqparse
from valuespaces import Valuespaces;
import json
import requests
class Transform(Resource):
  def __init__(self):
      self.valuespaces = Valuespaces()

  def post(self):
    json = request.get_json(force = True)
    delete = []
    for key in json:
        # remap to new i18n layout
        mapped = []
        for entry in json[key]:
            i18n = {}
            valuespace = self.valuespaces.data[key]
            found = False
            for v in valuespace:
                #if v['id'].endswith(entry) or len(list(filter(lambda x: x['@value'].casefold() == entry.casefold(), v['altId']))) > 0 or len(list(filter(lambda x: x['@value'].casefold() == entry.casefold(), v['label']))) > 0:
                  if v['id'].endswith(entry) or len(list(filter(lambda x: x.casefold() == entry.casefold(), v['prefLabel'].values()))) > 0:
                    i18n['key'] = v['id']
                    i18n['de'] = v['prefLabel']['de']
                    try:
                        i18n['en'] = v['prefLabel']['en']
                    except:
                        pass
                    found = True
                    break
            if found and len(list(filter(lambda x: x['key'] == i18n['key'], mapped))) == 0:
                mapped.append(i18n)
        if len(mapped):
            json[key] = mapped
        else:
            delete.append(key)
    for key in delete:
        del json[key]

    return json
