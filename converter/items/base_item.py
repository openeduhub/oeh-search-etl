from dataclasses import dataclass
from typing import Optional, List


@dataclass
class BaseItem:
    source: str  #: spider name
    source_id: str  #: the identifier on the crawled website
    source_hash: str  #: a string to compare against, in case the item changed
    object_type: str  #: item.type?  0 = IO (Informationsobject), 1 = LS (Lernszenario)
    source_uuid: str  #: replicationsourceuuid
    notes: Optional[str] = None
    source_origin: Optional[str] = None  #: TODO currently not mapped in edu-sharing
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

