from dataclasses import dataclass, field
from typing import List


@dataclass
class License:
    url: str
    key: str
    version: str

    def to_alfresco(self):
        return {
            'ccm:commonlicense_key': self.key,
            'ccm:commonlicense_cc_version': self.version,
        }


@dataclass
class InternalLicense:
    key: str

    def to_alfresco(self):
        return {
            'ccm:commonlicense_key': self.key,
        }


CopyrightLaw = InternalLicense('COPYRIGHT_FREE')


@dataclass
class CustomLicense:
    description: str  #: .. todo:: mltext

    def to_alfresco(self):
        return {
            'ccm:commonlicense_key': 'CUSTOM',
            'cclom:rights_description': self.description
        }


class CreativeCommons:
    v3 = License('https://creativecommons.org/licenses/by/3.0/', 'CC_BY', '3.0')
    v4 = License('https://creativecommons.org/licenses/by/4.0/', 'CC_BY', '4.0')
    sa_v3 = License('https://creativecommons.org/licenses/by-sa/3.0/', 'CC_BY_SA', '3.0')
    sa_v4 = License('https://creativecommons.org/licenses/by-sa/4.0/', 'CC_BY_SA', '4.0')
    nc_nd_v3 = License('https://creativecommons.org/licenses/by-nc-nd/3.0/', 'CC_BY_NC_ND', '3.0')
    nc_nd_v4 = License('https://creativecommons.org/licenses/by-nc-nd/4.0/', 'CC_BY_NC_ND', '4.0')
    zero = License('https://creativecommons.org/publicdomain/zero/1.0/', 'CC_0', '1.0')
    public_domain_mark = License('https://creativecommons.org/publicdomain/mark/1.0/', 'PDM', '1.0')

    @classmethod
    def from_url(cls, url):
        if url == cls.v3.url:
            return cls.v3
        elif url == cls.v4.url:
            return cls.v4
        elif url == cls.sa_v3.url:
            return cls.sa_v3
        elif url == cls.sa_v4.url:
            return cls.sa_v4
        elif url == cls.nc_nd_v3.url:
            return cls.nc_nd_v3
        elif url == cls.nc_nd_v4.url:
            return cls.nc_nd_v4
        elif url == cls.zero.url:
            return cls.zero
        elif url == cls.public_domain_mark.url:
            return cls.public_domain_mark
        raise ValueError(f'unknown cc license url: "{url}"')


@dataclass
class Author:
    authors: List[str] = field(default_factory=list)

    def to_alfresco(self):
        return {
            'ccm:author_freetext': self.authors,
        }