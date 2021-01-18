class Constants:
    LICENSE_CC_ZERO_10 = "https://creativecommons.org/publicdomain/zero/1.0/"
    LICENSE_CC_BY_SA_30 = "https://creativecommons.org/licenses/by-sa/3.0/"
    LICENSE_CC_BY_SA_40 = "https://creativecommons.org/licenses/by-sa/4.0/"
    LICENSE_CC_BY_30 = "https://creativecommons.org/licenses/by/3.0/"
    LICENSE_CC_BY_40 = "https://creativecommons.org/licenses/by/4.0/"
    LICENSE_CC_BY_NC_ND_30 = "https://creativecommons.org/licenses/by-nc-nd/3.0/"
    LICENSE_CC_BY_NC_ND_40 = "https://creativecommons.org/licenses/by-nc-nd/4.0/"
    LICENSE_PDM = "https://creativecommons.org/publicdomain/mark/1.0/"

    VALID_LICENSE_URLS = [
        LICENSE_CC_ZERO_10,
        LICENSE_CC_BY_SA_30,
        LICENSE_CC_BY_SA_40,
        LICENSE_CC_BY_30,
        LICENSE_CC_BY_40,
        LICENSE_CC_BY_NC_ND_30,
        LICENSE_CC_BY_NC_ND_40,
        LICENSE_PDM,
    ]
    LICENSE_MAPPINGS = {
        "https://creativecommons.org/publicdomain/zero/": LICENSE_CC_ZERO_10,
        "https://creativecommons.org/licenses/by/": LICENSE_CC_BY_40,
        "https://creativecommons.org/licenses/by-sa/": LICENSE_CC_BY_SA_40,
        # wrong mapping (currently from edu-sharing)
        "https://creativecommons.org/licenses/pdm/": LICENSE_PDM,
        "https://creativecommons.org/licenses/by-nc-nd/3.0/": LICENSE_CC_BY_NC_ND_30,
        "https://creativecommons.org/licenses/by-nc-nd/4.0/": LICENSE_CC_BY_NC_ND_40,
    }
    LICENSE_MAPPINGS_INTERNAL = {
        "CC_0": [LICENSE_CC_ZERO_10],
        "CC_BY": [LICENSE_CC_BY_40, LICENSE_CC_BY_30],
        "CC_BY_SA": [LICENSE_CC_BY_SA_40, LICENSE_CC_BY_SA_30],
        "CC_BY_NC_ND": [LICENSE_CC_BY_NC_ND_40, LICENSE_CC_BY_NC_ND_30],
        "PDM": [LICENSE_PDM],
    }

    LICENSE_COPYRIGHT_LAW = "COPYRIGHT_LAW"
    LICENSE_CUSTOM = "CUSTOM" # Custom License, use the license description field for arbitrary values
    LICENSE_NONPUBLIC = "NONPUBLIC"

    TYPE_MATERIAL = "MATERIAL"
    TYPE_TOOL = "TOOL"
    TYPE_SOURCE = "SOURCE"
    TYPE_LESSONPLANNING = "LESSONPLANNING"

    SOURCE_TYPE_SPIDER = 1
    SOURCE_TYPE_EDITORIAL = 2


class OerType:
    NONE = "NONE"
    MIXED = "MIXED"
    ALL = "ALL"
