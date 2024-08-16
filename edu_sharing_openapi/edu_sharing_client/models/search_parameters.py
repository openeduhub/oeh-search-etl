# coding: utf-8

"""
    edu-sharing Repository REST API

    The public restful API of the edu-sharing repository.

    The version of the OpenAPI document: 1.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from edu_sharing_client.models.mds_query_criteria import MdsQueryCriteria
from typing import Optional, Set
from typing_extensions import Self

class SearchParameters(BaseModel):
    """
    SearchParameters
    """ # noqa: E501
    permissions: Optional[List[StrictStr]] = None
    resolve_collections: Optional[StrictBool] = Field(default=None, alias="resolveCollections")
    resolve_usernames: Optional[StrictBool] = Field(default=None, alias="resolveUsernames")
    return_suggestions: Optional[StrictBool] = Field(default=None, alias="returnSuggestions")
    excludes: Optional[List[StrictStr]] = None
    facets: Optional[List[StrictStr]] = None
    facet_min_count: Optional[StrictInt] = Field(default=5, alias="facetMinCount")
    facet_limit: Optional[StrictInt] = Field(default=10, alias="facetLimit")
    facet_suggest: Optional[StrictStr] = Field(default=None, alias="facetSuggest")
    criteria: List[MdsQueryCriteria]
    __properties: ClassVar[List[str]] = ["permissions", "resolveCollections", "resolveUsernames", "returnSuggestions", "excludes", "facets", "facetMinCount", "facetLimit", "facetSuggest", "criteria"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of SearchParameters from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in criteria (list)
        _items = []
        if self.criteria:
            for _item_criteria in self.criteria:
                if _item_criteria:
                    _items.append(_item_criteria.to_dict())
            _dict['criteria'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SearchParameters from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "permissions": obj.get("permissions"),
            "resolveCollections": obj.get("resolveCollections"),
            "resolveUsernames": obj.get("resolveUsernames"),
            "returnSuggestions": obj.get("returnSuggestions"),
            "excludes": obj.get("excludes"),
            "facets": obj.get("facets"),
            "facetMinCount": obj.get("facetMinCount") if obj.get("facetMinCount") is not None else 5,
            "facetLimit": obj.get("facetLimit") if obj.get("facetLimit") is not None else 10,
            "facetSuggest": obj.get("facetSuggest"),
            "criteria": [MdsQueryCriteria.from_dict(_item) for _item in obj["criteria"]] if obj.get("criteria") is not None else None
        })
        return _obj


