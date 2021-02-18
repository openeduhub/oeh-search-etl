from dataclasses import dataclass
from typing import Optional, List
from .lom import Schema
from .valuespace import ValueSpace


@dataclass
class BaseItem:
    uuid: str  #: explicit uuid of the element, only set this if you actually know the uuid of the internal document
    hash: str
    collection: List[str]  #: id of collections this entry should be placed into
    # type: str
    # origin: str  #:
    response: ResponseItem
    ranking: str
    fulltext: str
    thumbnail: str
    last_modified: str
    lom: Schema
    valuespaces: ValueSpace
    permissions: PermissionItem
    license: LicenseItem
    publisher: str
    notes: str
    source: str  #: spider name
    source_id: str  #: the identifier on the crawled website
    source_hash: str  #: a string to compare against, in case the item changed
    object_type: str  #: item.type?  0 = IO (Informationsobject), 1 = LS (Lernszenario)
    source_uuid: str
    source_origin: Optional[str] = None  #: in case it was fetched from a referatorium, this is the real origin name
    # in case we're using the file pipeline
    image_urls: Optional[List[str]] = None
    images: Optional[List[str]] = None

    def to_alfresco(self):
        return {
            'ccm:replicationsource': self.source,
            'ccm:replicationsourceid': self.source_id,
            'ccm:replicationsourcehash': self.source_hash,
            'ccm:objecttype': self.object_type,
            'ccm:replicationsourceuuid': self.source_uuid,
            'ccm:notes': self.notes,
            'ccm:replicationsourceorigin': self.source_origin,
            'cm:edu_metadataset': 'mds_oeh',
            'cm:edu_forcemetadataset': 'true',
        }

