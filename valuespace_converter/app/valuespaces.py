import string

import requests
import json

class Valuespaces:
    idsVocabs = ['intendedEndUserRole', 'discipline', 'educationalContext', 'learningResourceType',
                 'sourceContentType', 'toolCategory', 'conditionsOfAccess', 'oer']
    idsW3ID = ['containsAdvertisement', 'price', 'accessibilitySummary', 'dataProtectionConformity', 'fskRating']
    urls = [
        {'key': 'oehTopics', 'url': 'https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/oehTopics/5e40e372-735c-4b17-bbf7-e827a5702b57.json'}
    ]
    data = {}
    def __init__(self):
        for v in self.idsVocabs:
            self.urls.append({'key': v, 'url': 'https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/' + v + '/index.json'})
        for v in self.idsW3ID:
            self.urls.append({'key': v, 'url': 'http://w3id.org/openeduhub/vocabs/' + v + '/index.json'})
        for url in self.urls:
            #try:
            r = requests.get(url['url'])
            self.data[url['key']] = r.json()['hasTopConcept']
            #except:
            #    self.valuespaces[v] = {}

    @staticmethod
    def findKey(valuespaceId: string, id: string, valuespace = None):
        if not valuespace:
            valuespace = Valuespaces.data[valuespaceId]
        for key in valuespace:
            if key['id'] == id:
                return key
            if 'narrower' in key:
                found = Valuespaces.findKey(valuespaceId, id, key['narrower'])
                if found:
                    return found
        return None


    def initTree(self, tree):
        for t in tree:
            names = self.getNames(t)
            # t['words'] = list(map(lambda x: nlp(x)[0], names))
            t['words'] = names
            if 'narrower' in t:
                self.initTree(t['narrower'])

    def getNames(self, key):
        names = []
        if 'prefLabel' in key:
            if 'de' in key['prefLabel']:
                names += [key['prefLabel']['de']]
            if 'en' in key['prefLabel']:
                names += [key['prefLabel']['en']]
        if 'altLabel' in key:
            names += key['altLabel']['de'] if 'de' in key['altLabel'] else []
            names += key['altLabel']['en'] if 'en' in key['altLabel'] else []
        if 'note' in key:
            names += key['note']['de'] if 'de' in key['note'] else []
            names += key['note']['en'] if 'en' in key['note'] else []

        names = list(set(map(lambda x: x.strip(), names)))
        return names