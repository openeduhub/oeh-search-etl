import requests
from requests import Response


class Valuespaces:
    idsVocabs: list[str] = [
        "conditionsOfAccess",
        "discipline",
        "educationalContext",
        "hochschulfaechersystematik",
        "intendedEndUserRole",
        "kldb",
        "languageLevel",
        "learningResourceType",
        "new_lrt",
        "oer",
        "sourceContentType",
        "toolCategory",
    ]
    idsW3ID: list[str] = [
        "containsAdvertisement",
        "price",
        "accessibilitySummary",
        "dataProtectionConformity",
        "fskRating",
    ]
    data: dict = {}

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
            r: Response = requests.get(vocab_name["url"])
            self.data[vocab_name["key"]] = self.flatten(r.json()["hasTopConcept"])
            # except:
            #    self.valuespaces[v] = {}

    def flatten(self, tree: list[dict]) -> list[dict]:
        result: list[dict] = tree
        for leaf in tree:
            if "narrower" in leaf:
                result.extend(self.flatten(leaf["narrower"]))
        return result

    @staticmethod
    def find_key(valuespace_id: str, id: str, valuespace=None):
        if not valuespace:
            valuespace = Valuespaces.data[valuespace_id]
        for key in valuespace:
            if key["id"] == id:
                return key
            if "narrower" in key:
                found = Valuespaces.find_key(valuespace_id, id, key["narrower"])
                if found:
                    return found
        return None

    def init_tree(self, tree):
        # ToDo: this method appears to be dead code that hasn't been used anywhere.
        for t in tree:
            names = self.get_names(t)
            # t['words'] = list(map(lambda x: nlp(x)[0], names))
            t["words"] = names
            if "narrower" in t:
                self.init_tree(t["narrower"])

    def get_names(self, key):
        # ToDo: this method appears to be dead code that hasn't been used anywhere.
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
