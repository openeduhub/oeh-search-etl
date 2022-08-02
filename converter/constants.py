from typing import Final, Any


class Constants:
    LICENSE_CC_BY_30: Final[str] = "https://creativecommons.org/licenses/by/3.0/"
    LICENSE_CC_BY_40: Final[str] = "https://creativecommons.org/licenses/by/4.0/"
    LICENSE_CC_BY_NC_30: Final[str] = "https://creativecommons.org/licenses/by-nc/3.0/"
    LICENSE_CC_BY_NC_40: Final[str] = "https://creativecommons.org/licenses/by-nc/4.0/"
    LICENSE_CC_BY_NC_ND_30: Final[str] = "https://creativecommons.org/licenses/by-nc-nd/3.0/"
    LICENSE_CC_BY_NC_ND_40: Final[str] = "https://creativecommons.org/licenses/by-nc-nd/4.0/"
    LICENSE_CC_BY_NC_SA_30: Final[str] = "https://creativecommons.org/licenses/by-nc-sa/3.0/"
    LICENSE_CC_BY_NC_SA_40: Final[str] = "https://creativecommons.org/licenses/by-nc-sa/4.0/"
    LICENSE_CC_BY_ND_30: Final[str] = "https://creativecommons.org/licenses/by-nd/3.0/"
    LICENSE_CC_BY_ND_40: Final[str] = "https://creativecommons.org/licenses/by-nd/4.0/"
    LICENSE_CC_BY_SA_30: Final[str] = "https://creativecommons.org/licenses/by-sa/3.0/"
    LICENSE_CC_BY_SA_40: Final[str] = "https://creativecommons.org/licenses/by-sa/4.0/"
    LICENSE_CC_ZERO_10: Final[str] = "https://creativecommons.org/publicdomain/zero/1.0/"
    LICENSE_PDM: Final[str] = "https://creativecommons.org/publicdomain/mark/1.0/"

    VALID_LICENSE_URLS: list[str | Any] = [
        LICENSE_CC_BY_30,
        LICENSE_CC_BY_40,
        LICENSE_CC_BY_NC_30,
        LICENSE_CC_BY_NC_40,
        LICENSE_CC_BY_NC_ND_30,
        LICENSE_CC_BY_NC_ND_40,
        LICENSE_CC_BY_NC_SA_30,
        LICENSE_CC_BY_NC_SA_40,
        LICENSE_CC_BY_ND_30,
        LICENSE_CC_BY_ND_40,
        LICENSE_CC_BY_SA_30,
        LICENSE_CC_BY_SA_40,
        LICENSE_CC_ZERO_10,
        LICENSE_PDM,
    ]
    LICENSE_MAPPINGS: dict[str, str] = {
        "https://creativecommons.org/licenses/by/": LICENSE_CC_BY_40,  # ToDo: outdated approximation?
        # ToDo: - CC_BY_NC (3.0 + 4.0)
        "https://creativecommons.org/licenses/by-nc-nd/3.0/": LICENSE_CC_BY_NC_ND_30,
        "https://creativecommons.org/licenses/by-nc-nd/4.0/": LICENSE_CC_BY_NC_ND_40,
        # ToDo:
        #  - CC_BY_NC_SA (3.0 + 4.0)
        #  - CC_BY_ND (3.0 + 4.0)
        #  - CC_BY_SA (3.0)
        "https://creativecommons.org/licenses/by-sa/": LICENSE_CC_BY_SA_40,  # Todo: outdated approximation?
        # wrong mapping (currently from edu-sharing)
        "https://creativecommons.org/publicdomain/zero/": LICENSE_CC_ZERO_10,
        "https://creativecommons.org/licenses/pdm/": LICENSE_PDM,
    }
    LICENSE_MAPPINGS_INTERNAL: dict[str, list[str]] = {
        "CC_0": [LICENSE_CC_ZERO_10],
        "CC_BY": [LICENSE_CC_BY_40, LICENSE_CC_BY_30],
        "CC_BY_SA": [LICENSE_CC_BY_SA_40, LICENSE_CC_BY_SA_30],
        "CC_BY_NC_ND": [LICENSE_CC_BY_NC_ND_40, LICENSE_CC_BY_NC_ND_30],
        "PDM": [LICENSE_PDM],
    }

    LICENSE_COPYRIGHT_LAW: Final[str] = "COPYRIGHT_LAW"
    LICENSE_CUSTOM: Final[str] = "CUSTOM"  # Custom License, use the license description field for arbitrary values
    LICENSE_NONPUBLIC: Final[str] = "NONPUBLIC"

    NEW_LRT_MATERIAL: Final[str] = "https://w3id.org/openeduhub/vocabs/new_lrt/1846d876-d8fd-476a-b540-b8ffd713fedb"
    NEW_LRT_TOOL: Final[str] = "https://w3id.org/openeduhub/vocabs/new_lrt/cefccf75-cba3-427d-9a0f-35b4fedcbba1"

    SOURCE_TYPE_SPIDER: int = 1
    SOURCE_TYPE_EDITORIAL: int = 2


class OerType:
    NONE = "NONE"
    MIXED = "MIXED"
    ALL = "ALL"
