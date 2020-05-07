from flask import request
from flask_restful import Resource, reqparse
import json
import requests
class Transform(Resource):
  ids = ['intendedEndUserRole', 'discipline', 'educationalContext', 'learningResourceType', 'sourceContentType']
  valuespaces = {}
  #def __init__(self):
     

  def post(self):
    for v in self.ids:
      url = 'https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/' + v + '/index.json'
      #try:
      r = requests.get(url)
      self.valuespaces[v] = r.json()['hasTopConcept']
      #except:
      #    self.valuespaces[v] = {}

    json = request.get_json(force = True)
    delete = []
    for key in json:
        # remap to new i18n layout
        mapped = []
        for entry in json[key]:
            i18n = {}
            valuespace = self.valuespaces[key]
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
