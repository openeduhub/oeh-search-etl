import requests
import json

class Valuespaces:
    ids = ['intendedEndUserRole', 'discipline', 'educationalContext', 'learningResourceType', 'sourceContentType', 'toolCategory']
    data = {}
    def __init__(self):
        for v in self.ids:
            url = 'https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/' + v + '/index.json'
            #try:
            r = requests.get(url)
            self.data[v] = r.json()['hasTopConcept']
            #except:
            #    self.valuespaces[v] = {}