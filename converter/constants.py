from typing import Final, Any


class Constants:
    LICENSE_CC_BY_10: Final[str] = "https://creativecommons.org/licenses/by/1.0/"
    LICENSE_CC_BY_20: Final[str] = "https://creativecommons.org/licenses/by/2.0/"
    LICENSE_CC_BY_25: Final[str] = "https://creativecommons.org/licenses/by/2.5/"
    LICENSE_CC_BY_30: Final[str] = "https://creativecommons.org/licenses/by/3.0/"
    LICENSE_CC_BY_40: Final[str] = "https://creativecommons.org/licenses/by/4.0/"
    LICENSE_CC_BY_NC_10: Final[str] = "https://creativecommons.org/licenses/by-nc/1.0/"
    LICENSE_CC_BY_NC_20: Final[str] = "https://creativecommons.org/licenses/by-nc/2.0/"
    LICENSE_CC_BY_NC_25: Final[str] = "https://creativecommons.org/licenses/by-nc/2.5/"
    LICENSE_CC_BY_NC_30: Final[str] = "https://creativecommons.org/licenses/by-nc/3.0/"
    LICENSE_CC_BY_NC_40: Final[str] = "https://creativecommons.org/licenses/by-nc/4.0/"
    LICENSE_CC_BY_NC_ND_20: Final[str] = "https://creativecommons.org/licenses/by-nc-nd/2.0/"
    LICENSE_CC_BY_NC_ND_25: Final[str] = "https://creativecommons.org/licenses/by-nc-nd/2.5/"
    LICENSE_CC_BY_NC_ND_30: Final[str] = "https://creativecommons.org/licenses/by-nc-nd/3.0/"
    LICENSE_CC_BY_NC_ND_40: Final[str] = "https://creativecommons.org/licenses/by-nc-nd/4.0/"
    LICENSE_CC_BY_NC_SA_10: Final[str] = "https://creativecommons.org/licenses/by-nc-sa/1.0/"
    LICENSE_CC_BY_NC_SA_20: Final[str] = "https://creativecommons.org/licenses/by-nc-sa/2.0/"
    LICENSE_CC_BY_NC_SA_25: Final[str] = "https://creativecommons.org/licenses/by-nc-sa/2.5/"
    LICENSE_CC_BY_NC_SA_30: Final[str] = "https://creativecommons.org/licenses/by-nc-sa/3.0/"
    LICENSE_CC_BY_NC_SA_40: Final[str] = "https://creativecommons.org/licenses/by-nc-sa/4.0/"
    LICENSE_CC_BY_ND_10: Final[str] = "https://creativecommons.org/licenses/by-nd/1.0/"
    LICENSE_CC_BY_ND_20: Final[str] = "https://creativecommons.org/licenses/by-nd/2.0/"
    LICENSE_CC_BY_ND_25: Final[str] = "https://creativecommons.org/licenses/by-nd/2.5/"
    LICENSE_CC_BY_ND_30: Final[str] = "https://creativecommons.org/licenses/by-nd/3.0/"
    LICENSE_CC_BY_ND_40: Final[str] = "https://creativecommons.org/licenses/by-nd/4.0/"
    LICENSE_CC_BY_SA_10: Final[str] = "https://creativecommons.org/licenses/by-sa/1.0/"
    LICENSE_CC_BY_SA_20: Final[str] = "https://creativecommons.org/licenses/by-sa/2.0/"
    LICENSE_CC_BY_SA_25: Final[str] = "https://creativecommons.org/licenses/by-sa/2.5/"
    LICENSE_CC_BY_SA_30: Final[str] = "https://creativecommons.org/licenses/by-sa/3.0/"
    LICENSE_CC_BY_SA_40: Final[str] = "https://creativecommons.org/licenses/by-sa/4.0/"
    LICENSE_CC_ZERO_10: Final[str] = "https://creativecommons.org/publicdomain/zero/1.0/"
    LICENSE_PDM: Final[str] = "https://creativecommons.org/publicdomain/mark/1.0/"

    VALID_LICENSE_URLS: list[str | Any] = [
        LICENSE_CC_BY_10,
        LICENSE_CC_BY_20,
        LICENSE_CC_BY_25,
        LICENSE_CC_BY_30,
        LICENSE_CC_BY_40,
        LICENSE_CC_BY_NC_10,
        LICENSE_CC_BY_NC_20,
        LICENSE_CC_BY_NC_25,
        LICENSE_CC_BY_NC_30,
        LICENSE_CC_BY_NC_40,
        LICENSE_CC_BY_NC_ND_20,
        LICENSE_CC_BY_NC_ND_25,
        LICENSE_CC_BY_NC_ND_30,
        LICENSE_CC_BY_NC_ND_40,
        LICENSE_CC_BY_NC_SA_10,
        LICENSE_CC_BY_NC_SA_20,
        LICENSE_CC_BY_NC_SA_25,
        LICENSE_CC_BY_NC_SA_30,
        LICENSE_CC_BY_NC_SA_40,
        LICENSE_CC_BY_ND_10,
        LICENSE_CC_BY_ND_20,
        LICENSE_CC_BY_ND_25,
        LICENSE_CC_BY_ND_30,
        LICENSE_CC_BY_ND_40,
        LICENSE_CC_BY_SA_10,
        LICENSE_CC_BY_SA_20,
        LICENSE_CC_BY_SA_25,
        LICENSE_CC_BY_SA_30,
        LICENSE_CC_BY_SA_40,
        LICENSE_CC_ZERO_10,
        LICENSE_PDM,
    ]
    LICENSE_MAPPINGS: dict[str, str] = {
        "https://creativecommons.org/licenses/by/1.0/": LICENSE_CC_BY_10,
        "https://creativecommons.org/licenses/by/2.0/": LICENSE_CC_BY_20,
        "https://creativecommons.org/licenses/by/2.5/": LICENSE_CC_BY_25,
        "https://creativecommons.org/licenses/by/3.0/": LICENSE_CC_BY_30,
        "https://creativecommons.org/licenses/by/4.0/": LICENSE_CC_BY_40,
        "https://creativecommons.org/licenses/by-nc/1.0/": LICENSE_CC_BY_NC_10,
        "https://creativecommons.org/licenses/by-nc/2.0/": LICENSE_CC_BY_NC_20,
        "https://creativecommons.org/licenses/by-nc/2.5/": LICENSE_CC_BY_NC_25,
        "https://creativecommons.org/licenses/by-nc/3.0/": LICENSE_CC_BY_NC_30,
        "https://creativecommons.org/licenses/by-nc/4.0/": LICENSE_CC_BY_NC_40,
        "https://creativecommons.org/licenses/by-nc-nd/2.0/": LICENSE_CC_BY_NC_ND_20,
        "https://creativecommons.org/licenses/by-nc-nd/3.0/": LICENSE_CC_BY_NC_ND_30,
        "https://creativecommons.org/licenses/by-nc-nd/4.0/": LICENSE_CC_BY_NC_ND_40,
        "https://creativecommons.org/licenses/by-nc-sa/1.0/": LICENSE_CC_BY_NC_SA_10,
        "https://creativecommons.org/licenses/by-nc-sa/2.0/": LICENSE_CC_BY_NC_SA_20,
        "https://creativecommons.org/licenses/by-nc-sa/2.5/": LICENSE_CC_BY_NC_SA_25,
        "https://creativecommons.org/licenses/by-nc-sa/3.0/": LICENSE_CC_BY_NC_SA_30,
        "https://creativecommons.org/licenses/by-nc-sa/4.0/": LICENSE_CC_BY_NC_SA_40,
        "https://creativecommons.org/licenses/by-nd/1.0/": LICENSE_CC_BY_ND_10,
        "https://creativecommons.org/licenses/by-nd/2.0/": LICENSE_CC_BY_ND_20,
        "https://creativecommons.org/licenses/by-nd/2.5/": LICENSE_CC_BY_ND_25,
        "https://creativecommons.org/licenses/by-nd/3.0/": LICENSE_CC_BY_ND_30,
        "https://creativecommons.org/licenses/by-nd/4.0/": LICENSE_CC_BY_ND_40,
        "https://creativecommons.org/licenses/by-sa/1.0/": LICENSE_CC_BY_SA_10,
        "https://creativecommons.org/licenses/by-sa/2.0/": LICENSE_CC_BY_SA_20,
        "https://creativecommons.org/licenses/by-sa/2.5/": LICENSE_CC_BY_SA_25,
        "https://creativecommons.org/licenses/by-sa/3.0/": LICENSE_CC_BY_SA_30,
        "https://creativecommons.org/licenses/by-sa/4.0/": LICENSE_CC_BY_SA_40,
        # wrong mapping (currently from edu-sharing)
        "https://creativecommons.org/publicdomain/zero/": LICENSE_CC_ZERO_10,
        "https://creativecommons.org/licenses/pdm/": LICENSE_PDM,
        "https://creativecommons.org/publicdomain/mark/1.0/": LICENSE_PDM,
    }
    # ToDo: LICENSE_MAPPINGS is only used once in pipelines.py and should be refactored asap
    LICENSE_MAPPINGS_INTERNAL: dict[str, list[str]] = {
        "CC_0": [LICENSE_CC_ZERO_10],
        "CC_BY": [LICENSE_CC_BY_40, LICENSE_CC_BY_30],
        "CC_BY_NC": [LICENSE_CC_BY_NC_40, LICENSE_CC_BY_NC_30],
        "CC_BY_NC_ND": [LICENSE_CC_BY_NC_ND_40, LICENSE_CC_BY_NC_ND_30],
        "CC_BY_NC_SA": [LICENSE_CC_BY_NC_SA_40, LICENSE_CC_BY_NC_SA_30],
        "CC_BY_ND": [LICENSE_CC_BY_ND_40, LICENSE_CC_BY_ND_30],
        "CC_BY_SA": [LICENSE_CC_BY_SA_40, LICENSE_CC_BY_SA_30],
        "PDM": [LICENSE_PDM],
    }

    LICENSE_COPYRIGHT_FREE: Final[str] = "COPYRIGHT_FREE"  # edu-sharing Frontend: "Copyright, freier Zugang"
    LICENSE_COPYRIGHT_LAW: Final[str] = "COPYRIGHT_LICENSE"  # edu-sharing Frontend: "Copyright, lizenzpflichtig"
    LICENSE_CUSTOM: Final[str] = "CUSTOM"  # Custom License, use the license description field for arbitrary values
    LICENSE_NONPUBLIC: Final[str] = "NONPUBLIC"
    LICENSE_SCHULFUNK: Final[str] = "SCHULFUNK"  # "Schulfunk (§47 UrhG)"
    LICENSE_UNTERRICHTS_UND_SCHULMEDIEN = "UNTERRICHTS_UND_LEHRMEDIEN"  # "§60b Unterrichts- und Lehrmedien"

    NEW_LRT_MATERIAL: Final[str] = "1846d876-d8fd-476a-b540-b8ffd713fedb"
    NEW_LRT_TOOL: Final[str] = "cefccf75-cba3-427d-9a0f-35b4fedcbba1"

    SOURCE_TYPE_SPIDER: int = 1
    SOURCE_TYPE_EDITORIAL: int = 2


class OerType:
    NONE = "NONE"
    MIXED = "MIXED"
    ALL = "ALL"
