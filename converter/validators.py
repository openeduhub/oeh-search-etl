from schematics import Model
from schematics.types import *


class LicenseItemValidator(Model):
    url = URLType()
    internal = StringType(required=False)
    description = StringType(required=False)
    oer = StringType(required=False)
    author = StringType(required=False)
    expirationDate = DateType(required=False)


class ValuespaceItemValidator(Model):
    intendedEndUserRole = ListType(StringType)
    discipline = ListType(StringType)
    educationalContext = ListType(StringType)
    learningResourceType = ListType(StringType)
    sourceContentType = ListType(StringType)
    toolCategory = ListType(StringType)

    conditionsOfAccess = ListType(StringType)
    containsAdvertisement = ListType(StringType)
    price = ListType(StringType)
    accessibilitySummary = ListType(StringType)
    dataProtectionConformity = ListType(StringType)
    fskRating = ListType(StringType)
    oer = ListType(StringType)


class ResponseItemValidator(Model):
    status = StringType()
    url = URLType()
    html = StringType()
    text = StringType()
    headers = StringType()
    cookies = StringType()
    har = StringType()


class LomGeneralItemValidator(Model):
    identifier = StringType(required=True)
    title = StringType(required=True)
    language = StringType()
    keyword = ListType(StringType)
    coverage = StringType()
    structure = StringType()
    aggregationLevel = StringType()
    description = StringType(required=True)


class LomLifecycleItemValidator(Model):
    role = StringType()
    firstName = StringType()
    lastName = StringType()
    # TODO: research which structure is used for organization (dict? string?)
    organization = BaseType()
    email = StringType()
    url = StringType()
    uuid = StringType()
    date = StringType()


class LomTechnicalItemValidator(Model):
    format = StringType()
    size = StringType()
    location = StringType()
    requirement = StringType()
    installationRemarks = StringType()
    otherPlatformRequirements = StringType()
    duration = StringType()


class LomEducationalItemValidator(Model):
    interactivityType = StringType()
    interactivityLevel = StringType()
    semanticDensity = StringType()
    intendedEndUserRole = ListType(StringType)
    typicalAgeRange = ListType(StringType)
    difficulty = StringType()
    typicalLearningTime = StringType()
    language = StringType()


class LomClassificationItemValidator(Model):
    cost = StringType()
    purpose = StringType()
    taxonPath = ListType(StringType)
    description = StringType()
    keyword = StringType()


class LomBaseItemValidator(Model):
    general = PolyModelType(LomGeneralItemValidator, required=True)
    lifecycle = ListType(ModelType(LomLifecycleItemValidator), required=True)
    technical = PolyModelType(LomTechnicalItemValidator, required=True)
    educational = PolyModelType(LomEducationalItemValidator, required=True)
    classification = PolyModelType(LomClassificationItemValidator)


class BaseItemValidator(Model):
    sourceId = StringType(required=True)
    hash = StringType(required=True)
    lastModified = StringType(required=True)
    license = PolyModelType(LicenseItemValidator)
    # lom = PolyModelType(LomBaseItemValidator)
    lom = DictType(field=DictType(field=StringType))
    response = PolyModelType(ResponseItemValidator)
    # TODO: BaseType validates with anything, find a better model for base64 'bytes'-class
    thumbnail = DictType(StringType, coerce_key=BaseType)
    type = StringType(required=False)
    valuespaces = PolyModelType(ValuespaceItemValidator)
