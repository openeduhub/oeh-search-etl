from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Tuple, Union, TypeVar, Literal

"""
This module's information is derived from the
Draft Standard for Learning Object Metadata IEEE 1484.12.1-2002 (LOM)
which in turn is summarized here:
https://docs.google.com/spreadsheets/d/13viKaA-S13jnxqOPxjwFk7hMR4JkinAkIvI2Iu39ARQ/edit#gid=355785871
"""
T = TypeVar('T')
mltext = Tuple[str, str]
Multiple = Union[List[T], T]


@dataclass
class Schema:
    """
    cclom:schema
    """
    # associations, all optional
    identifiers: Optional[List['Identifier']]  #: identifiers
    general: 'General'  #: 1. Grundlegende Informationen, die das Lernobjekt als Ganzes beschreiben.
    lifecycle: 'Lifecycle'  #: 2. Eigenschaften, die einerseits die Geschichte und den aktuellen Zustand des Lernobjektes als auch die beeinflussenden Lernobjekte beschreiben.
    meta_metadata: 'MetaMetadata'  #: 3. Merkmale der Metadatenbeschreibung an sich.
    technical: 'Technical'  #: 4. technische Voraussetzungen und Merkmale des Lernobjekts.
    educational: Optional[List['Educational']]  #: 5. Bildungsmerkmale und pädagogische Beschreibung des Lernobjekts.
    rights: 'Rights'  #: 6. Über Nutzungsbedingungen des Lernobjekts und Copyright-Fragen wird informiert.
    relation: Optional[List['Relation']]  #: 7. Beziehungen zwischen dem Lernobjekt und anderen verwandten Lernobjekten.
    annotation: Optional[List['Annotation']]  #: 8. ermöglicht Anmerkung über den Bildungsnutzen des Lernobjekts und Informationen über die Entstehung der Kommentare (wann, von wem)
    classification: Optional[List['Classification']]  #: 9. Einordnung des Lernobjekts in ein Klassifizierungssystem.


@dataclass
class General:
    """
    1. General Category (Allgemein):
    Grundlegende Informationen, die das Lernobjekt als Ganzes beschreiben.
    """

    title: Optional[mltext] = None  #: Name given to this learning object.
    language: List[str] = field(default_factory=list)  #: "The primary human language or languages used within this learning object to communicate to the intended user."
    description: List[mltext] = field(default_factory=list)  #: A textual description of the content of this learning object.
    keyword: List[mltext] = field(default_factory=list)  #: A keyword or phrase describing the topic of this learning object.
    coverage: List[mltext] = field(default_factory=list)  #: The time, culture, geography or region to which this learning object applies. (see documentation)
    structure: Optional[str] = None  #: Underlying organizational structure of this learning object Value; atomic, collection networked, hirrarchical, linear
    aggregationLevel: Optional[str] = None  #: The functional granularity of this learning; Value: 1, 2, 3, 4
    # child associations
    identifier: Optional[List['Identifier']] = None  #: A globally unique label that identifies this learning object.

    def to_alfresco(self):
        return {
            'cm:name': self.title,

            'cclom:title': self.title,
            'cclom:general_description': self.description,
            'cclom:general_language': self.language,
            'cclom:general_keyword': self.keyword,
            # 'cclom:general_identifier': self.identifier,
        }


@dataclass
class Lifecycle:
    """
    2. Lifecycle Category (Lebenszyklus):
    Eigenschaften, die einerseits die Geschichte und den aktuellen Zustand des Lernobjektes als auch die beeinflussenden Lernobjekte beschreiben.

    Does not correspond to anything within the lom standard, which would be
    version, status, contribute :O
    """
    version: mltext
    status: str
    # child assoc, type cclom:contribute
    contributors: List['contribute']  #: list of contributors

    def to_alfresco(self):
        return {
            'cclom:version': self.version,
            'cclom:status': self.status,
            'cclom:lifecycle_contribute': self.contributors,
        }

    # this was on the item:
    # role: str  #:
    # firstName: str  #:
    # lastName: str  #:
    # organization: str  #:
    # url: str  #:
    # uuid: str  #:


@dataclass
class MetaMetadata:
    """
    3. Meta-Metadata Category (Metametadaten):
    Merkmale der Metadatenbeschreibung an sich.

    not implemented

    cclom:schema_metametadata_identifier
    """
    pass


@dataclass
class Technical:
    """
    4. Technical Category (Technische Details):
    technische Voraussetzungen und Merkmale des Lernobjekts.
    """
    format: str  #: Technical datatype(s) of (all the components of) this learning object. This data element shall be used to identify the software needed to access the learning object.
    size: str  #: The size of the digital learning object in bytes (octets). The size is represented as a decimal value (radix 10). Consequently, only the digits "0" through "9" should be used. The unit is bytes, not Mbytes, GB, etc. This data element shall refer to the actual size of this learning object. If the learning object is compressed, then this data element shall refer to the uncompressed size.
    location: List[str]  #: A string that is used to access this learning object. It may be a location (e.g., Universal Resource Locator), or a method that resolves to a location (e.g., Universal Resource Identifier). The first element of this list shall be the preferable location. NOTE:This is where the learning object described by this metadata instance is physically located
    installationRemarks: List[mltext]  #: Description of how to install this learning object.
    otherPlatformRequirements: List[mltext]  #: Information about other software and hardware requirements.
    duration: str  #: Time a continuous learning object takes when played at intended speed.
    requirements: List['requirement']  #: The technical capabilities necessary for using this learning object.

    def to_alfresco(self):
        return {
            'ccm:wwwurl': self.location,

            'cclom:location': self.location,
            'cclom:size': self.size,
            'cclom:format': self.format,
            'cclom:installationremarks': self.installationRemarks,
            'cclom:otherplatformrequirements': self.otherPlatformRequirements,
            'cclom:duration': self.duration,  # TODO: document format; "PT1H30M" "PT1M45S"
            'cclom:technical_requirement': self.requirements
        }


InteractivityType = Literal['active', 'expositive', 'mixed']
# TODO: theres more for learning resource type
LearningResourceType = Literal['exercise', 'simulation', 'questionaire', 'diagram', 'figure']
Level = Literal['very low', 'low', 'medium', 'high', 'very high']
IntendedUserRole = Literal['teacher', 'author', 'learner', 'manager (State)']
Context = Literal['school', 'higher education', 'training', 'other (State)']
Difficulty = Literal['very easy', 'easy', 'medium', 'difficult', 'very difficult']


# TODO: typicalAgeRange is a tuple of 'from', 'to' values, that get's connected by a dash
# TODO: but the model docs also give examples of: "7-9","0-5", ("en","adults only")
# TODO: but that would imply mltext, but that's just text here


@dataclass
class Educational:
    """
    5. Educational Category (Pädagogische Details):
    Bildungsmerkmale und pädagogische Beschreibung des Lernobjekts.

    cclom:schema_educational
    """
    interactivityType: InteractivityType  #: Predominant mode of learning supported by this learning object. (Active, expositive, mixed)
    learning_resource_type: LearningResourceType  #: Specific kind of learning object. The most dominant kind shall be first
    interactivityLevel: Level  #: The degree of interactivity characterizing this learning object. Interactivity in this context refers to the degree to which the learner can influence the aspect or behavior of the learning object .
    semanticDensity: Level  #: The degree of conciseness of a learning object. The semantic density of a learning object may be estimated in terms of its size, span, or --in the case of self-timed resources such as audio or video - duration.The semantic density of a learning object is independent of its difficulty. It is best illustrated with examples of expositive material, although it can be used with active resources as well.
    intendedEndUserRole: List[IntendedUserRole]  #: Principal user(s) for which this learning object was designed, most dominant first.
    context: List[Context]  #: The principal environment within which the learning and use of this learning object is intended to take place.
    typicalAgeRange: str  #: Age of the typical intended user. This data element shall refer to developmental age, if that would be different from chronological age.
    difficulty: Difficulty  #: How hard it is to work with or through this learning object for the typical intended target audience. NOTE: The " typical target audience" can be characterized by data elements 5.6:Educational.Context and 5.7:Educational.TypicalAgeRange.
    typicalLearningTime: int  #: Duration in milliseconds. Approximate or typical time it takes to work with or through this learning object for the typical intended target audience. NOTE:The " typical target audience" can be characterized by data elements 5.6:Educational.Context and 5.7:Educational.TypicalAgeRange.
    description: List[mltext]  #: Comments on how this learning object is to be used.
    language: List[mltext]  #: The human language used by the typical intended user of this learning object.

    def to_alfresco(self):
        return {
            'cclom:interactivitytype': self.interactivityType,
            'cclom:learningresourcetype': self.learning_resource_type,
            'cclom:interactivitylevel': self.interactivityLevel,
            'cclom:semanticdensity': self.semanticDensity,
            'cclom:intendedenduserrole': self.intendedEndUserRole,
            'cclom:context': self.context,
            'cclom:typicalagerange': self.typicalAgeRange,
            'cclom:difficulty': self.difficulty,
            'cclom:typicallearningtime': self.typicalLearningTime,
            'cclom:educational_description': self.description,
            'cclom:educational_language': self.language,
        }


@dataclass
class Rights:
    """
    6. Rights Category (Rechte):
    Über Nutzungsbedingungen des Lernobjekts und Copyright-Fragen wird informiert.

    not implemented
    """
    pass


@dataclass
class Relation:
    """
    7. Relation Category (Verwandte Ressourcen):
    Beziehungen zwischen dem Lernobjekt und anderen verwandten Lernobjekten.

    not implemented

    cclom:schema_relation
    """
    pass


@dataclass
class Annotation:
    """
    8. Annotation Category (Anmerkung):
    ermöglicht Anmerkung über den Bildungsnutzen des Lernobjekts und Informationen über die Entstehung der Kommentare (wann, von wem)

    not implemented

    cclom:schema_annotation
    """
    pass


@dataclass
class Classification:
    """
    9. Classification Category (Klassifikation):
    Einordnung des Lernobjekts in ein Klassifizierungssystem.

    cclom:schema_classification
    """
    cost: str  #: this is from 6.1 (Rights)
    purpose: str  #: The purpose of classifying this learning object.
    taxonPath: List['taxonpath']  #: Particular therm within a tasonomy .. todo:: document taxonomyPath
    description: mltext  #: Description of the learning object relative to the stated 9.1: Classification.Purpose of this specific classification, such as discipline, idea, skill level, educational objective, etc.
    keyword: List[
        mltext]  #: Keywords and phrases descriptive of the learning object relative to the stated 9.1:Classification.Purpose of this specific classification, such as accessibility, security level, etc., most relevant first.

    def to_alfresco(self):
        return {
            'cclom:purpose': self.purpose,
            'cclom:classification_description': self.description,
            'cclom:classification_keyword': self.keyword,
            'cclom:classification_taxonpath': self.taxonPath,
        }


"""
support types:
"""

Role = Literal[
    'author', 'publisher', 'unknown', 'initiator', 'terminator', 'validator', 'editor', 'graphical_designer',
    'technical_implementer', 'content_provider', 'technical_validator', 'educational_validator', 'script_writer',
    'instructional_designer', 'subject_matter_expert',

    # LOM - DE
    'animation', 'archiv', 'aufnahmeleitung', 'aufnahmeteam',
    'ausstattung', 'autor', 'ballett', 'bearbeitete_fassung', 'bildende_kunst', 'bildschnitt', 'buch', 'chor', 'choreographie',
    'darsteller', 'design', 'dirigent', 'dvd-grafik_und_design', 'dvd-premastering', 'ensemble', 'fachberatung', 'foto', 'grafik',
    'idee', 'interpret', 'interview', 'kamera', 'kommentar', 'komponist', 'konzeption', 'libretto', 'literarische_vorlage',
    'maz-bearbeitung', 'mitwirkende', 'moderation', 'musik', 'musikalische_leitung', 'musikalische_vorlage', 'musikgruppe',
    'orchester', 'paedagogischer_sachbearbeiter_extern', 'produktionsleitung', 'projektgruppe', 'projektleitung', 'realisation',
    'redaktion', 'regie', 'schnitt', 'screen-design', 'spezialeffekte', 'sprecher', 'studio', 'synchronisation', 'synchronregie',
    'synchronsprecher', 'tanz', 'text', 'ton', 'trick', 'videotechnik', 'uebersetzung', 'uebertragung'
]

@dataclass
class contribute:
    """
    cclom:contribute
    """
    role: Role
    contributing_entity: mltext  #: .. todo:: somehow provide this text as vcard
    contribution_date: datetime

    def entity_from_vcard(self, given_name: str, family_name: str,
                          additional_name: str = None, name_prefix: str = None, name_suffix: str = None,
                          url: str = None, organization: str = None):
        import vobject
        card = vobject.vCard()
        card.add('n').value = vobject.vcard.Name(
            family_name, given_name, additional_name or '', name_prefix or '', name_suffix or '')
        if url is not None:
            card.add('url').value = url
        if organization is None:
            card.add('fn').value = f'{given_name} {family_name}'
        else:
            card.add('fn').value = organization
            card.add('org')
            # fixes a bug of split org values
            card.org.behavior = vobject.vcard.VCardBehavior.defaultBehavior
            card.org.value = organization
        self.contributing_entity = card.serialize()

    def to_alfresco(self):
        return {
            'cclom:role': f'ccm:lifecyclecontributer_{self.role}',
            'cclom:contribute_entity': self.contributing_entity,
            'cclom:contribute_date': self.contribution_date,  # .. todo:: how to format datetime?
            f'ccm:lifecyclecontributer_{self.role}': [self.contributing_entity]  #: .. todo:: this needs to be merged
        }


@dataclass
class Contributor:
    # TODO: maybe use this class to serialize to vcard
    pass


@dataclass
class taxonpath:
    """
    cclom:taxonpath

    .. todo:: format as code/monospace

    Example:
    {["12",("en","Physics")],
    ["23",("en","Acoustics")],
    ["34",("en","Instruments")],
    ["45",("en","Stethoscope")]}
    or:

    {["56",("en,"Medicine")],
    ...,
    ["45",("en","Stethoscope")]}
    """
    source: mltext
    # child association: taxon
    taxonpath_taxon: List['taxon']


@dataclass
class taxon:
    """
    cclom:taxon
    """
    id: str  #: the id
    taxon_entry: mltext  #: the value

    def to_alfresco(self):
        return {
            'cclom:id': self.id,
            'cclom:taxon_entry': self.taxon_entry
        }


@dataclass
class requirement:
    """
    cclom:requirement
    """
    requirement_orcomposite: List['orcomposite']


OperatingSystem = Literal['ms-windows', 'macos', 'unix', 'multi-os']  #: .. todo:: there are more literals allowed
Browser = Literal['ms-internet explorer', 'opera', 'amaya']  #: .. todo:: there are more literals allowed


@dataclass
class orcomposite:
    """
    cclom:orcomposite
    """
    type: Union[Literal['operating system'], Literal['browser']]  #:
    name: Union[Browser, OperatingSystem]  #: depends on type
    minimum_version: str  #: e.g. 4.2
    maximum_version: str  #: e.g. 6.2

    def to_alfresco(self):
        return {
            'cclom:type': self.type,
            'cclom:name': self.name,
            'cclom:minimum_version': self.minimum_version,
            'cclom:maximum_version': self.maximum_version,
        }


@dataclass
class Identifier:
    """
    cclom:identifier
    """
    catalog: mltext  #: DOI, handle, ISBN
    identifier: mltext  #: the identifier https://doi.org/..., hdl://10..., 978-...

    def to_alfresco(self):
        return {
            'cclom:catalog': self.catalog,
            'cclom:identifier_entry': self.identifier,
        }
