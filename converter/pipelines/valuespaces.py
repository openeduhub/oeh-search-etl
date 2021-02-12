from converter.pipelines.bases import BasicPipeline
from valuespace_converter.app.valuespaces import Valuespaces


class ProcessValuespacePipeline(BasicPipeline):
    """
    generate de_DE / i18n strings for valuespace fields
    """
    def __init__(self):
        self.valuespaces = Valuespaces()

    def process_item(self, item, spider):
        json = item["valuespaces"]
        delete = []
        for key in json:
            # remap to new i18n layout
            mapped = []
            for entry in json[key]:
                _id = {}
                valuespace = self.valuespaces.data[key]
                found = False
                for v in valuespace:
                    labels = list(v["prefLabel"].values())
                    if "altLabel" in v:
                        labels = labels + list(
                            [x for y in list(v["altLabel"].values()) for x in y]
                        )
                    labels = list(map(lambda x: x.casefold(), labels))
                    if v["id"].endswith(entry) or entry.casefold() in labels:
                        _id = v["id"]
                        found = True
                        break
                if found and len(list(filter(lambda x: x == _id, mapped))) == 0:
                    mapped.append(_id)
            if len(mapped):
                json[key] = mapped
            else:
                delete.append(key)
        for key in delete:
            del json[key]
        item["valuespaces"] = json
        return item
