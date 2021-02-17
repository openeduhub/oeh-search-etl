from dataclasses import dataclass


@dataclass
class ValueSpace:
    """
    The value spaces are a controlled vocabulary.
    For a complete list of vocabularies, values and definitions, visit https://vocabs.openeduhub.de/
    """
    discipline: list[str]  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/discipline/index.html
    intendedEndUserRole: list[str]  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/intendedEndUserRole/index.html
    educationalContext: list[str]  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/educationalContext/index.html
    learningResourceType: list[str]  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/learningResourceType/index.html
    sourceContentType: list[str]  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/sourceContentType/index.html
    toolCategory: list[str]  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/toolCategory/index.html
    conditionsOfAccess: list[str]  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/conditionsOfAccess/index.html
    containsAdvertisement: str  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/containsAdvertisement/index.html
    price: str  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/price/index.html
    accessibilitySummary: list[str]  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/accessibilitySummary/index.html
    dataProtectionConformity: list[str]  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/dataProtectionConformity/index.html
    fskRating: str  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/fskRating/index.html
    oer: str  #: for valid values, see: https://vocabs.openeduhub.de/w3id.org/openeduhub/vocabs/oer/index.html

    def to_alfresco(self):
        return {
            'ccm:taxonid': self.discipline,
            'ccm:educationalintendedenduserrole': self.intendedEndUserRole,
            'ccm:educationalcontext': self.educationalContext,
            'ccm:educationallearningresourcetype': self.learningResourceType,
            'ccm:sourceContentType': self.sourceContentType,
            'ccm:toolCategory': self.toolCategory,
            'ccm:conditionsOfAccess': self.conditionsOfAccess,
            'ccm:containsAdvertisement': self.containsAdvertisement,
            'ccm:price': self.price,
            'ccm:accessibilitySummary': self.accessibilitySummary,
            'ccm:dataProtectionConformity': self.dataProtectionConformity,
            'ccm:fskRating': self.fskRating,
            'ccm:license_oer': self.oer,
        }
