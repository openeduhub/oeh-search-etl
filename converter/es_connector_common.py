import uuid
from enum import Enum
from converter.constants import Constants
from vobject.vcard import VCardBehavior
import vobject
import logging
log = logging.getLogger(__name__)


class CreateGroupType(Enum):
    Regular = 1
    MediaCenter = 2


class EduSharingConstants:
    HOME = "-home-"
    GROUP_EVERYONE = "GROUP_EVERYONE"
    AUTHORITYTYPE_GROUP = "GROUP"
    AUTHORITYTYPE_EVERYONE = "EVERYONE"
    PERMISSION_CONSUMER = "Consumer"
    PERMISSION_CCPUBLISH = "CCPublish"
    GROUP_PREFIX = "GROUP_"
    MEDIACENTER_PREFIX = "MEDIA_CENTER_"
    MEDIACENTER_PROXY_PREFIX = "MEDIA_CENTER_PROXY_"
    LIFECYCLE_ROLES_MAPPING = {
        "publisher": "ccm:lifecyclecontributer_publisher",
        "author": "ccm:lifecyclecontributer_author",
        "editor": "ccm:lifecyclecontributer_editor",
    }


def build_uuid(url):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, url))


def map_license(spaces, _license):
    if "url" in _license:
        if _license["url"] == Constants.LICENSE_CC_BY_40:
            spaces["ccm:commonlicense_key"] = "CC_BY"
            spaces["ccm:commonlicense_cc_version"] = "4.0"
        if _license["url"] == Constants.LICENSE_CC_BY_30:
            spaces["ccm:commonlicense_key"] = "CC_BY"
            spaces["ccm:commonlicense_cc_version"] = "3.0"
        if _license["url"] == Constants.LICENSE_CC_BY_SA_30:
            spaces["ccm:commonlicense_key"] = "CC_BY_SA"
            spaces["ccm:commonlicense_cc_version"] = "3.0"
        if _license["url"] == Constants.LICENSE_CC_BY_SA_40:
            spaces["ccm:commonlicense_key"] = "CC_BY_SA"
            spaces["ccm:commonlicense_cc_version"] = "4.0"
        if _license["url"] == Constants.LICENSE_CC_BY_NC_ND_30:
            spaces["ccm:commonlicense_key"] = "CC_BY_NC_ND"
            spaces["ccm:commonlicense_cc_version"] = "3.0"
        if _license["url"] == Constants.LICENSE_CC_BY_NC_ND_40:
            spaces["ccm:commonlicense_key"] = "CC_BY_NC_ND"
            spaces["ccm:commonlicense_cc_version"] = "4.0"
        if _license["url"] == Constants.LICENSE_CC_ZERO_10:
            spaces["ccm:commonlicense_key"] = "CC_0"
            spaces["ccm:commonlicense_cc_version"] = "1.0"
        if _license["url"] == Constants.LICENSE_PDM:
            spaces["ccm:commonlicense_key"] = "PDM"
    if "internal" in _license:
        if _license["internal"] == Constants.LICENSE_COPYRIGHT_LAW:
            spaces["ccm:commonlicense_key"] = "COPYRIGHT_FREE"
        if _license["internal"] == Constants.LICENSE_CUSTOM:
            spaces["ccm:commonlicense_key"] = "CUSTOM"
            if "description" in _license:
                spaces["cclom:rights_description"] = _license["description"]

    if "author" in _license:
        spaces["ccm:author_freetext"] = _license["author"]


def transform_item(_uuid, spider, item):
    spaces = {
        "ccm:replicationsource": spider.name,
        "ccm:replicationsourceid": item["sourceId"],
        "ccm:replicationsourcehash": item["hash"],
        "ccm:objecttype": item["type"],
        "ccm:replicationsourceuuid": _uuid,
        "cm:name": item["lom"]["general"]["title"],
        "ccm:wwwurl": item["lom"]["technical"]["location"],
        "cclom:location": item["lom"]["technical"]["location"],
        "cclom:title": item["lom"]["general"]["title"],
    }
    if "notes" in item:
        spaces["ccm:notes"] = item["notes"]
    if "origin" in item:
        spaces["ccm:replicationsourceorigin"] = item[
            "origin"
        ]  # TODO currently not mapped in edu-sharing

    map_license(spaces, item["license"])
    if "description" in item["lom"]["general"]:
        spaces["cclom:general_description"] = item["lom"]["general"]["description"]

    if "language" in item["lom"]["general"]:
        spaces["cclom:general_language"] = item["lom"]["general"]["language"]

    if "keyword" in item["lom"]["general"]:
        spaces["cclom:general_keyword"] = (item["lom"]["general"]["keyword"],)
    else:
        spaces["cclom:general_keyword"] = []
    # TODO: this does currently not support multiple values per role
    if "lifecycle" in item["lom"]:
        for person in item["lom"]["lifecycle"]:
            if not "role" in person:
                continue
            if (
                not person["role"].lower()
                in EduSharingConstants.LIFECYCLE_ROLES_MAPPING
            ):
                log.warn(
                    "The lifecycle role "
                    + person["role"]
                    + " is currently not supported by the edu-sharing connector"
                )
                continue
            mapping = EduSharingConstants.LIFECYCLE_ROLES_MAPPING[
                person["role"].lower()
            ]
            # convert to a vcard string
            firstName = person["firstName"] if "firstName" in person else ""
            lastName = person["lastName"] if "lastName" in person else ""
            organization = (
                person["organization"] if "organization" in person else ""
            )
            url = person["url"] if "url" in person else ""
            vcard = vobject.vCard()
            vcard.add("n").value = vobject.vcard.Name(
                family=lastName, given=firstName
            )
            vcard.add("fn").value = (
                organization
                if organization
                else (firstName + " " + lastName).strip()
            )
            if organization:
                vcard.add("org")
                # fix a bug of splitted org values
                vcard.org.behavior = VCardBehavior.defaultBehavior
                vcard.org.value = organization
            vcard.add("url").value = url
            spaces[mapping] = [vcard.serialize()]

    valuespaceMapping = {
        "discipline": "ccm:taxonid",
        "intendedEndUserRole": "ccm:educationalintendedenduserrole",
        "educationalContext": "ccm:educationalcontext",
        "learningResourceType": "ccm:educationallearningresourcetype",
        "sourceContentType": "ccm:sourceContentType",
        "toolCategory": "ccm:toolCategory",
        "conditionsOfAccess": "ccm:conditionsOfAccess",
        "containsAdvertisement": "ccm:containsAdvertisement",
        "price": "ccm:price",
        "accessibilitySummary": "ccm:accessibilitySummary",
        "dataProtectionConformity": "ccm:dataProtectionConformity",
        "fskRating": "ccm:fskRating",
        "oer": "ccm:license_oer",
    }
    for key in item["valuespaces"]:
        spaces[valuespaceMapping[key]] = item["valuespaces"][key]
    if "typicalagerange" in item["lom"]["educational"]:
        spaces["ccm:educationaltypicalagerange_from"] = item["lom"]["educational"][
            "typicalagerange"
        ]["from"]
        spaces["ccm:educationaltypicalagerange_to"] = item["lom"]["educational"][
            "typicalagerange"
        ]["to"]
    # intendedEndUserRole = Field(output_processor=JoinMultivalues())
    # discipline = Field(output_processor=JoinMultivalues())
    # educationalContext = Field(output_processor=JoinMultivalues())
    # learningResourceType = Field(output_processor=JoinMultivalues())
    # sourceContentType = Field(output_processor=JoinMultivalues())
    spaces["cm:edu_metadataset"] = "mds_oeh"
    spaces["cm:edu_forcemetadataset"] = "true"
    for key in spaces:
        if type(spaces[key]) is tuple:
            spaces[key] = list([x for y in spaces[key] for x in y])
        if not type(spaces[key]) is list:
            spaces[key] = [spaces[key]]

    return spaces

