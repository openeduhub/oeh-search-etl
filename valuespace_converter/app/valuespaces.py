import requests


class Valuespaces:
    idsVocabs = [
        "conditionsOfAccess",
        "discipline",
        "educationalContext",
        "hochschulfaechersystematik",
        "intendedEndUserRole",
        "languageLevel",
        "learningResourceType",
        "new_lrt",
        "oer",
        "sourceContentType",
        "toolCategory",
    ]
    idsW3ID = ["containsAdvertisement", "price", "accessibilitySummary", "dataProtectionConformity", "fskRating"]
    data = {}

    def __init__(self):
        vocab_list: list[dict] = []
        # one singular dictionary in the vocab list will typically look like this:
        # {'key': 'discipline', 'url': 'https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/discipline/index.json'}
        for v in self.idsVocabs:
            vocab_list.append(
                {"key": v, "url": "https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/" + v + "/index.json"}
            )
        for v in self.idsW3ID:
            vocab_list.append({"key": v, "url": "http://w3id.org/openeduhub/vocabs/" + v + "/index.json"})
        for vocab_name in vocab_list:
            # try:
            r = requests.get(vocab_name["url"])
            self.data[vocab_name["key"]] = self.flatten(r.json()["hasTopConcept"])
            # except:
            #    self.valuespaces[v] = {}

    def flatten(self, tree: []):
        result = tree
        for leaf in tree:
            if "narrower" in leaf:
                result.extend(self.flatten(leaf["narrower"]))
        return result

    @staticmethod
    def findKey(valuespaceId: str, id: str, valuespace=None):
        if not valuespace:
            valuespace = Valuespaces.data[valuespaceId]
        for key in valuespace:
            if key["id"] == id:
                return key
            if "narrower" in key:
                found = Valuespaces.findKey(valuespaceId, id, key["narrower"])
                if found:
                    return found
        return None

    def findInText(self, valuespaceId: str, text: str, valuespace = None):
        if valuespace is None:
            valuespace: list[dict] = self.data[valuespaceId]
        result = []
        for v in valuespace:
            labels = list(v["prefLabel"].values())
            if "altLabel" in v:
                # the Skohub update on 2024-04-19 generates altLabels as a list[str] per language ("de", "en)
                # (for details, see: https://github.com/openeduhub/oeh-metadata-vocabs/pull/65)
                alt_labels: list[list[str]] = list(v["altLabel"].values())
                if alt_labels and isinstance(alt_labels, list):
                    for alt_label in alt_labels:
                        if alt_label and isinstance(alt_label, list):
                            labels.extend(alt_label)
                        if alt_label and isinstance(alt_label, str):
                            labels.append(alt_label)
            labels = list(map(lambda x: x.casefold(), labels))
            for label in labels:
                # TODO: dirty hack!
                if (" " + label) in text.casefold():
                    result.append(v["id"])
                    break
        for key in valuespace:
            if key['id'] == id:
                return key
            if 'narrower' in key:
                result = result + self.findInText(valuespaceId, text, key['narrower'])
        return result
    def initTree(self, tree):
        for t in tree:
            names = self.getNames(t)
            # t['words'] = list(map(lambda x: nlp(x)[0], names))
            t["words"] = names
            if "narrower" in t:
                self.initTree(t["narrower"])

    def getNames(self, key):
        names = []
        if "prefLabel" in key:
            if "de" in key["prefLabel"]:
                names += [key["prefLabel"]["de"]]
            if "en" in key["prefLabel"]:
                names += [key["prefLabel"]["en"]]
        if "altLabel" in key:
            names += key["altLabel"]["de"] if "de" in key["altLabel"] else []
            names += key["altLabel"]["en"] if "en" in key["altLabel"] else []
        if "note" in key:
            names += key["note"]["de"] if "de" in key["note"] else []
            names += key["note"]["en"] if "en" in key["note"] else []

        names = list(set(map(lambda x: x.strip(), names)))
        return names
