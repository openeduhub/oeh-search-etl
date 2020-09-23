import string

import requests
import json

class Valuespaces:
    ids = ['intendedEndUserRole', 'discipline', 'educationalContext', 'EAF-Sachgebietssystematik', 'allSchoolTopics', 'learningResourceType', 'sourceContentType', 'toolCategory']
    data = {}
    def __init__(self):
        for v in self.ids:
            url = 'https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/' + v + '/index.json'
            #try:
            r = requests.get(url)
            self.data[v] = r.json()['hasTopConcept']
            self.initTree(self.data[v])
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

        names = list(map(lambda x: x.strip(), names))
        return names