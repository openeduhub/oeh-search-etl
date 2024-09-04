# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from w3lib.html import remove_tags, replace_escape_chars


def replace_processor(value):
    if value is not None:
        return replace_escape_chars(remove_tags(value)).strip()
    else:
        return value


class JoinMultivalues(object):
    def __init__(self, separator=" "):
        self.separator = separator

    def __call__(self, values):
        return values


class MutlilangItem(Item):
    key = Field()
    de_DE = Field()


class LomGeneralItem(Item):
    """
    General requirements:

    - 'description'
    - 'keyword'
    - 'title'

    (If neither 'description' nor 'keyword' are provided, the whole item gets dropped by the pipeline.)
    """

    aggregationLevel = Field()
    """Corresponding edu-sharing property: 'cclom:aggregationlevel'"""
    coverage = Field()
    # ToDo: 'coverage' is currently not used; no equivalent edu-sharing property
    description = Field()
    """Corresponding edu-sharing property: 'cclom:general_description'"""
    identifier = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'cclom:general_identifier' """
    keyword = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'cclom:general_keyword'"""
    language = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'cclom:general_language'"""
    structure = Field()
    # ToDo: 'structure' is currently not used; no equivalent edu-sharing property
    title = Field()
    """Corresponding edu-sharing properties: 'cm:title' & 'cclom:title'"""


class LomLifecycleItem(Item):
    """
    Depending on the 'role'-value that is chosen for a LomLifecycleItem, values are written to a VCARD-string and mapped
    to either one of these corresponding edu-sharing properties:

    - 'ccm:lifecyclecontributer_publisher'              ('role'-value = 'publisher')
    - 'ccm:lifecyclecontributer_author'                 ('role'-value = 'author')
    - 'ccm:lifecyclecontributer_editor'                 ('role'-value = 'editor')
    - 'ccm:metadatacontributer_creator'                 ('role'-value = 'metadata_creator')
    - 'ccm:metadatacontributer_provider'                ('role'-value = 'metadata_provider')
    - 'ccm:lifecyclecontributer_unknown'                ('role'-value = 'unknown')

    The role 'unknown' is used for contributors in an unknown capacity ("Mitarbeiter").
    """

    date = Field()
    """The (publication) date of a contribution. Date values will be automatically transformed/parsed.
    Corresponding edu-sharing property: 'ccm:published_date'"""
    email = Field()
    firstName = Field()
    lastName = Field()
    organization = Field()
    role = Field()
    title = Field()
    """The (academic) title of a person. String value will be prefixed to '(title) firstName lastName' and written into
    the vCard-field 'TITLE'.
    """
    url = Field()
    uuid = Field()
    id_gnd = Field()
    """The GND identifier (URI) of a PERSON, e.g. "https://d-nb.info/gnd/<identifier>". 
    Values will be written into the vCard namespace 'X-GND-URI'."""
    id_orcid = Field()
    """The ORCID identifier (URI) of a PERSON, e.g. "https://orcid.org/<identifier>". 
    Values will be written into the vCard namespace 'X-ORCID'."""
    id_ror = Field()
    """The ROR identifier (URI) of an ORGANIZATION, e.g. "https://ror.org/<identifier>".
    Values will be written into the vCard namespace 'X-ROR'."""
    id_wikidata = Field()
    """The Wikidata identifier (URI) of an ORGANIZATION, e.g. "https://www.wikidata.org/wiki/<identifier>". 
    Values will be written into the vCard namespace 'X-Wikidata'."""
    address_city = Field()
    """vCard v3 "ADR"-attribute for city strings."""
    address_country = Field()
    """vCard v3 "ADR"-attribute for country strings."""
    address_postal_code = Field()
    """vCard v3 "ADR"-attribute for postal code strings."""
    address_region = Field()
    """vCard v3 "ADR"-attribute for region strings."""
    address_street = Field()
    """vCard v3 "ADR"-attribute for street strings."""
    address_type = Field(output_processor=JoinMultivalues())
    """vCard v3 "ADR"-attribute type. Expects a single string or a list[str] from the following values:
    ["dom", "intl", "postal", "parcel", "home", "work", "pref"]"""


class LomTechnicalItem(Item):
    duration = Field()
    """Duration of the element (e.g. for video or audio content). Supported formats for automatic transforming include 
    seconds, HH:MM:SS and ISO 8601 duration (PT0H0M0S).
    Corresponding edu-sharing property: 'cclom:duration'"""
    format = Field()
    """'format' expects MIME-type as a string, e.g. "text/html" or "video/mp4".
    Corresponding edu-sharing property: 'cclom:format'"""
    installationRemarks = Field()
    # ToDo: 'installationRemarks' is an unused field
    location = Field(output_processor=JoinMultivalues())
    """URI/location of the element; multiple values are supported. 
    The first entry is the primary location, while all others are secondary locations.
    Corresponding edu-sharing properties: 'ccm:wwwurl' & 'cclom:location'"""
    otherPlatformRequirements = Field()
    # ToDo: LOM.technical attribute 'otherPlatformRequirements' has no equivalent property in edu-sharing (and has never
    #  been provided by any of the crawled APIs, yet.
    requirement = Field()
    # ToDo: LOM.technical attribute 'requirement' has no equivalent property in edu-sharing
    size = Field()
    """Content size in bytes. (The value is automatically calculated by the edu-sharing back-end)
    Corresponding edu-sharing property: 'cclom:size'"""


class LomAgeRangeItem(Item):
    fromRange = Field()
    """Corresponding edu-sharing property: 'ccm:educationaltypicalagerange_from'"""
    toRange = Field()
    """Corresponding edu-sharing property: 'ccm:educationaltypicalagerange_to"""


class LomEducationalItem(Item):
    """
    Item modeled after LOM-DE "Educational". Attention: Some fields which originally appear in "educational" are handled
    by "ValuespaceItem" instead because of vocabularies which need to be mapped.

    Please DO NOT use/fill the following fields here in "educational", but rather use them in ValuespaceItem:

    - intendedEndUserRole       (see: 'valuespaces.intendedEndUserRole')
    - learningResourceType      (see: 'valuespaces.learningResourceType')
    - context                   (see: 'valuespaces.educationalContext')
    """

    description = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'cclom:educational_description'"""
    difficulty = Field()
    """Corresponding edu-sharing property: 'ccm:educationaldifficulty'"""
    # ToDo: 'ccm:educationaldifficulty' is currently not used in edu-sharing / WLO
    #  - either use this field or get rid of it
    intendedEndUserRole = Field(serializer=MutlilangItem, output_processor=JoinMultivalues())
    # Please use valuespaces.intendedEndUserRole instead!
    interactivityLevel = Field()
    # ToDo: 'interactivityLevel' is currently not used anywhere in edu-sharing
    interactivityType = Field()
    """Corresponding edu-sharing property: 'ccm:educationalinteractivitytype'"""
    # ToDo: 'ccm:educationalinteractivitytype' is currently not used anywhere in edu-sharing
    language = Field(output_processor=JoinMultivalues())
    # ToDo: "Educational language" seems to be unused in edu-sharing.
    semanticDensity = Field()
    # ToDo: 'semanticDensity' is not used anywhere and there doesn't appear to be an edu-sharing property for it
    typicalAgeRange = Field(serializer=LomAgeRangeItem)
    """See LomAgeRangeItem. Corresponding edu-sharing properties: 
    'ccm:educationaltypicalagerange_from' & 'ccm:educationaltypicalagerange_to'"""
    typicalLearningTime = Field()
    """Corresponding edu-sharing property: 'cclom:typicallearningtime' (expects values in ms!)"""


# please use the seperate license data
# class LomRightsItem(Item):
# cost = Field()
# coyprightAndOtherRestrictions = Field()
# description = Field()


class LomClassificationItem(Item):
    """
    LOM "Classification"-specific metadata.
    (see: LOM-DE specifications: "Classification"-category)
    """

    cost = Field()
    # ToDo: no equivalent property in edu-sharing, might be obsolete (see: 'valuespaces.price')
    description = Field()
    # ToDo: LOM classification 'description' has no equivalent property in edu-sharing
    keyword = Field()
    # ToDo: 'ccm:classification_keyword' currently not used in edu-sharing
    purpose = Field()
    # ToDo: 'ccm:classification_purpose' not actively used in edu-sharing?
    taxonPath = Field(output_processor=JoinMultivalues())
    # ToDo: LOM classification 'taxonPath' has no equivalent property in edu-sharing, might be obsolete


class LomBaseItem(Item):
    """
    LomBaseItem provides the nested structure for LOM (Sub-)Elements. No metadata is saved here.
    (Please check the specific class definitions of the nested Items for more information.)
    """

    classification = Field(serializer=LomClassificationItem)
    educational = Field(serializer=LomEducationalItem)
    general = Field(serializer=LomGeneralItem)
    lifecycle = Field(serializer=LomLifecycleItem, output_processor=JoinMultivalues())
    # rights = Field(serializer=LomRightsItem)
    technical = Field(serializer=LomTechnicalItem)


class ResponseItem(Item):
    """
    Attributes of ResponseItem are populated by either Playwright or Splash when an item is processed by the pipelines.
    """

    cookies = Field()
    # ToDo: 'cookies' are not stored in edu-sharing. This field might be obsolete.
    headers = Field()
    # ToDo: 'headers' are not stored in edu-sharing. This field might be obsolete.
    har = Field()
    # ToDo: 'har' logs are not stored in edu-sharing. This field might be obsolete.
    html = Field()
    # ToDo: The 'raw' HTML body is not stored in edu-sharing at the moment. This field might become relevant in the
    #  future, but as of 2024-03-15 we can only store one "textContent" per item via the edu-sharing API.
    #  (see: 'ResponseItem.text')
    status = Field()
    # ToDo: the HTTP status code is not stored in edu-sharing. This field might be obsolete.
    text = Field()
    """Corresponding ElasticSearch (!) property: 'content.fulltext'. (The 'full text' of an item is only used for 
    indexing purposes and not readily available as an edu-sharing property!)"""
    url = Field()
    # ToDo: This field might be obsolete. URL(s) of items are stored within 'LomTechnicalItem.location'!


class ValuespaceItem(Item):
    """
    Values provided for attributes of ValuespaceItem are mapped against OEH (SKOS) vocabularies before saving them to
    edu-sharing. (see: https://github.com/openeduhub/oeh-metadata-vocabs)
    """

    accessibilitySummary = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:accessibilitysummary'"""
    conditionsOfAccess = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:conditionsOfAccess'"""
    containsAdvertisement = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:containsAdvertisement'"""
    dataProtectionConformity = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:dataProtectionConformity'"""
    discipline = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:taxonid'"""
    educationalContext = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:educationalcontext'"""
    fskRating = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:fskRating'"""
    hochschulfaechersystematik = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:oeh_taxonid_university"""
    intendedEndUserRole = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:intendedEndUserRole'"""
    languageLevel = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:oeh_languageLevel"""
    learningResourceType = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:educationallearningresourcetype'"""
    new_lrt = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:oeh_lrt'"""
    oer = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:license_oer'"""
    price = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:price'"""
    sourceContentType = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:sourceContentType'"""
    # ToDo: sourceContentType is no longer used in edu-sharing
    # DO NOT SET this field in crawlers for individual materials!
    toolCategory = Field(output_processor=JoinMultivalues())
    """Corresponding edu-sharing property: 'ccm:toolCategory'"""


class LicenseItem(Item):
    """
    Metadata provided within LicenseItem is used to recognize and map specific licenses to edu-sharing's corresponding
    properties. To make sure that licenses are properly recognized by edu-sharing, make sure to provide a valid
    'url'-string and if that's not possible, set a correct 'internal'-constant. (see: constants.py)
    """

    author = Field(output_processor=JoinMultivalues())
    """An author freetext string. (Basically, how the author should be named in case this is a 'CC-BY'-license.
    Corresponding edu-sharing property: 'ccm:author_freetext'"""
    description = Field()
    """A custom, free-text license description. Will only be used if the 'internal'-attribute (see: constants.py) is set 
    to 'CUSTOM'.
    Corresponding edu-sharing property: 'cclom:rights_description'"""
    expirationDate = Field()
    """A date at which any content license expires and the content shouldn't be delivered anymore.
    Corresponding edu-sharing property: 'ccm:license_to'"""
    internal = Field()
    """An internal (edu-sharing) constant for this license.
    Corresponding edu-sharing property: 'ccm:commonlicense_key'"""
    oer = Field()
    """A value of OerType (if empty, will be mapped via the given url or internal value).
    Corresponding edu-sharing property: 'ccm:oer'"""
    url = Field()
    """Expects a URL (String) to a license description.
    Gets mapped to two corresponding edu-sharing properties: 'ccm:commonlicense_key' & 'ccm:commonlicense_version'"""


class PermissionItem(Item):
    """
    PermissionItem sets the edu-sharing permissions for a crawled item.
    """

    autoCreateGroups = Field()
    """Should global groups be created if they don't already exist"""
    autoCreateMediacenters = Field()
    """Should media centers be created if they don't already exist"""
    groups = Field(output_processor=JoinMultivalues())
    """Global Groups that should have access to this object"""
    mediacenters = Field(output_processor=JoinMultivalues())
    """Mediacenters that should have access to this object"""
    public = Field()
    """Determines if this item should be 'public' (= accessible by anyone)"""


class CourseItem(Item):
    """
    BIRD-specific metadata properties intended only for courses.
    """
    course_availability_from = Field()
    """Corresponding edu-sharing property: 'ccm:oeh_event_begin' (expects ISO datetime string)"""
    course_availability_until = Field()
    """Corresponding edu-sharing property: 'ccm:oeh_event_end' (expects ISO datetime string)"""
    course_description_short = Field()
    """Corresponding edu-sharing property: 'ccm:oeh_course_description_short'"""
    course_duration = Field()
    """Expects a duration in seconds. 
    Corresponding edu-sharing property: 'cclom:typicallearningtime'.
    (ATTENTION: edu-sharing expects 'cclom:typicallearningtime'-values (type: int) in milliseconds! 
    -> the es_connector will handle transformation from s to ms.)"""
    course_learningoutcome = Field(output_processor=JoinMultivalues())
    """Describes "Lernergebnisse" or "learning objectives". (Expects a string, with or without HTML-formatting!)
    Corresponding edu-sharing property: 'ccm:learninggoal'"""
    course_schedule = Field()
    """Describes the schedule of a course ("Kursablauf"). (Expects a string, with or without HTML-formatting!)
    Corresponding edu-sharing property: 'ccm:oeh_course_schedule'."""
    course_url_video = Field()
    """URL of a course-specific trailer- or teaser-video.
    Corresponding edu-sharing property: 'ccm:oeh_course_url_video'"""
    course_workload = Field()
    """Describes the workload per week."""
    # ToDo: confirm where "workload" values should be saved within edu-sharing


class BaseItem(Item):
    """
    BaseItem provides the basic data structure for any crawled item.

    BaseItem requirements:
    - 'sourceId'
    - 'hash'

    Expected Items to be nested within BaseItem:
    - LicenseItem
    - LomBaseItem
    - PermissionItem
    - ResponseItem
    - ValuespaceItem
    """

    binary = Field()
    """Binary data which should be uploaded to edu-sharing (= raw data, e.g. ".pdf"-files)."""
    collection = Field(output_processor=JoinMultivalues())
    """id of edu-sharing collections this entry should be placed into"""
    course = Field(serializer=CourseItem)
    custom = Field()
    """A field for custom data which can be used by the target transformer to store data in the native format 
    (i.e. 'ccm:'/'cclom:'-properties in edu-sharing)."""
    fulltext = Field()
    """The 'fulltext'-attribute gets populated by a 'ResponseItem.text'-call in the pipelines and is stored in the 
    ElasticSearch index within the 'content.fulltext' property."""
    hash = Field()
    """Corresponding edu-sharing property: 'ccm:replicationsourcehash'"""
    lastModified = Field()
    # ToDo: 'lastModified' doesn't appear to be mapped to any edu-sharing property
    license = Field(serializer=LicenseItem)
    lom = Field(serializer=LomBaseItem)
    notes = Field()
    """Editorial notes (e.g. as used in edu-sharing between editors (WLO: "FachredakteurInnen")).
    Corresponding edu-sharing property: 'ccm:notes'"""
    origin = Field()
    """In case an item was fetched from a "referatorium", the real origin name may be included here.
    Corresponding edu-sharing property: 'ccm:replicationsourceorigin'"""
    # 'origin' is currently used to create crawler subfolders in edu-sharing's workspace view:
    # e.g.: "SYNC_OBJ/<crawler_name>/<origin-value>/..."
    permissions = Field(serializer=PermissionItem)
    """edu-sharing permissions (access rights) for this entry"""
    publisher = Field()
    # ToDo: publisher is implemented as a part of Lifecycle. This field isn't used anywhere, is most probably an
    #  oversight and should be deleted.
    ranking = Field()
    # ToDo: ranking isn't used anywhere, might be obsolete
    response = Field(serializer=ResponseItem)
    sourceId = Field()
    """Corresponding edu-sharing property: 'ccm:replicationsourceid'"""
    status = Field()
    """Status information of a given node, i.e. activated or deactivated.
    Corresponding edu-sharing property: 'ccm:editorial_state'"""
    thumbnail = Field()
    """Expects a thumbnail URL which in turn is consumed by the thumbnail pipeline. If a valid URL is provided,
    the resulting 'thumbnail'-dictionary consists of 3 key-value pairs after completion:
    - 'mimetype'    mimetype (String)
    - 'small'       image data in base64
    - 'large'       image data in base64"""
    uuid = Field()
    """Explicit uuid of the target element. 
    Please ONLY set this manually IF you actually know the uuid of the internal document!
    Corresponding edu-sharing property: 'ccm:replicationsourceuuid'"""
    valuespaces = Field(serializer=ValuespaceItem)
    """All items which are based on (SKOS) based valuespaces vocabularies. 
    The ProcessValuespacePipeline will automatically convert items inside here."""
    valuespaces_raw = Field(serializer=ValuespaceItem)
    """This item is only used by the ProcessValuespacePipeline and holds the ""raw"" data which were given to the 
    valuespaces. Please DO NOT use it within normal crawlers"""
    screenshot_bytes = Field()
    """screenshot_bytes is a (temporary) field that gets deleted after the thumbnail pipeline processed its byte-data"""


class BaseItemLoader(ItemLoader):
    default_item_class = BaseItem
    # default_input_processor = MapCompose(replace_processor)
    default_output_processor = TakeFirst()


class CourseItemLoader(ItemLoader):
    default_item_class = CourseItem
    default_output_processor = TakeFirst()


class MutlilangItemLoader(ItemLoader):
    default_item_class = MutlilangItem
    default_output_processor = TakeFirst()


class ValuespaceItemLoader(ItemLoader):
    default_item_class = ValuespaceItem
    default_output_processor = TakeFirst()


class LicenseItemLoader(ItemLoader):
    default_item_class = LicenseItem
    default_output_processor = TakeFirst()


class LomBaseItemloader(ItemLoader):
    default_item_class = LomBaseItem
    default_output_processor = TakeFirst()


class ResponseItemLoader(ItemLoader):
    default_item_class = ResponseItem
    default_output_processor = TakeFirst()


class LomGeneralItemloader(ItemLoader):
    default_item_class = LomGeneralItem
    default_output_processor = TakeFirst()


class LomLifecycleItemloader(ItemLoader):
    default_item_class = LomLifecycleItem
    default_output_processor = TakeFirst()


class LomTechnicalItemLoader(ItemLoader):
    default_item_class = LomTechnicalItem
    default_output_processor = TakeFirst()


class LomAgeRangeItemLoader(ItemLoader):
    default_item_class = LomAgeRangeItem
    default_output_processor = TakeFirst()


class LomEducationalItemLoader(ItemLoader):
    default_item_class = LomEducationalItem
    default_output_processor = TakeFirst()


# class LomRightsItemLoader(ItemLoader):
#    default_item_class = LomRightsItem
#    default_output_processor = TakeFirst()
class LomClassificationItemLoader(ItemLoader):
    default_item_class = LomClassificationItem
    default_output_processor = TakeFirst()


class PermissionItemLoader(ItemLoader):
    default_item_class = PermissionItem
    default_output_processor = TakeFirst()
