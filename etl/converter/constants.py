
class Constants:
    LICENSE_CC_ZERO_10 = 'https://creativecommons.org/publicdomain/zero/1.0/'
    LICENSE_CC_BY_SA_30 = 'https://creativecommons.org/licenses/by-sa/3.0/'
    LICENSE_CC_BY_SA_40 = 'https://creativecommons.org/licenses/by-sa/4.0/'
    LICENSE_CC_BY_40 = 'https://creativecommons.org/licenses/by/4.0/'
    LICENSE_PDM = 'https://creativecommons.org/publicdomain/mark/1.0/'

    LICENSE_MAPPINGS = {
        'https://creativecommons.org/publicdomain/zero': 'https://creativecommons.org/publicdomain/zero/1.0/',
        'https://creativecommons.org/licenses/by': 'https://creativecommons.org/licenses/by/4.0/',
        'https://creativecommons.org/licenses/by-sa': 'https://creativecommons.org/licenses/by-sa/4.0/',
        # wrong mapping (currently from edu-sharing)
        'https://creativecommons.org/licenses/pdm': 'https://creativecommons.org/publicdomain/mark/1.0/',
    }

    LICENSE_COPYRIGHT_LAW = 'COPYRIGHT_LAW'
    LICENSE_NONPUBLIC = 'NONPUBLIC'

    TYPE_MATERIAL = 'MATERIAL'    
    TYPE_TOOL = 'TOOL'
    TYPE_SOURCE = 'SOURCE'
    TYPE_LESSONPLANNING = 'LESSONPLANNING'

    SOURCE_TYPE_SPIDER = 1
    SOURCE_TYPE_EDITORIAL = 2
   
class OerType:
    NONE = 'NONE'
    MIXED = 'MIXED'
    ALL = 'ALL'
