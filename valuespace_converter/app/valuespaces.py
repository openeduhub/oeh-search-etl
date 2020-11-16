import requests
import json

class Valuespaces:
    idsVocabs = ['intendedEndUserRole', 'discipline', 'educationalContext', 'learningResourceType',
                 'sourceContentType', 'toolCategory', 'conditionsOfAccess']
    idsW3ID = ['containsAdvertisement', 'price', 'accessibilitySummary', 'dataProtectionConformity', 'fskRating']
    data = {}
    def __init__(self):
        urls = []
        for v in self.idsVocabs:
            urls.append({'key': v, 'url': 'https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/' + v + '/index.json'})
        for v in self.idsW3ID:
            urls.append({'key': v, 'url': 'http://w3id.org/openeduhub/vocabs/' + v + '/index.json'})
        for url in urls:
            #try:
            r = requests.get(url['url'])
            self.data[url['key']] = r.json()['hasTopConcept']
            #except:
            #    self.valuespaces[v] = {}