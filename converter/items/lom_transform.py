import vobject

from converter.constants import Constants


def map_license(spaces, _license):
    if "internal" in _license:
        if _license["internal"] == Constants.LICENSE_COPYRIGHT_LAW:
            spaces["ccm:commonlicense_key"] = "COPYRIGHT_FREE"
        if _license["internal"] == Constants.LICENSE_CUSTOM:
            spaces["ccm:commonlicense_key"] = "CUSTOM"
            if "description" in _license:
                spaces["cclom:rights_description"] = _license["description"]

    if "author" in _license:
        spaces["ccm:author_freetext"] = _license["author"]


def transform_item(uuid, spider, item):
    # TODO: this does currently not support multiple values per role
    for person in item['lom'].get("lifecycle", default=[]):
        if "role" not in person:
            continue
        mapping = f'ccm:lifecyclecontributer_{person["role"].lower()}'

        vcard = vobject.vCard()
        spaces[mapping] = [vcard.serialize()]

