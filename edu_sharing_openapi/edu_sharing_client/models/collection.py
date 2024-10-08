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
from typing import Optional, Set
from typing_extensions import Self

class Collection(BaseModel):
    """
    Collection
    """ # noqa: E501
    scope: Optional[StrictStr] = None
    author_freetext: Optional[StrictStr] = Field(default=None, alias="authorFreetext")
    order_ascending: Optional[StrictBool] = Field(default=None, alias="orderAscending")
    level0: StrictBool = Field(description="false")
    title: StrictStr
    description: Optional[StrictStr] = None
    type: StrictStr
    viewtype: StrictStr
    order_mode: Optional[StrictStr] = Field(default=None, alias="orderMode")
    x: Optional[StrictInt] = None
    y: Optional[StrictInt] = None
    z: Optional[StrictInt] = None
    color: Optional[StrictStr] = None
    from_user: StrictBool = Field(description="false", alias="fromUser")
    pinned: Optional[StrictBool] = None
    child_collections_count: Optional[StrictInt] = Field(default=None, alias="childCollectionsCount")
    child_references_count: Optional[StrictInt] = Field(default=None, alias="childReferencesCount")
    __properties: ClassVar[List[str]] = ["scope", "authorFreetext", "orderAscending", "level0", "title", "description", "type", "viewtype", "orderMode", "x", "y", "z", "color", "fromUser", "pinned", "childCollectionsCount", "childReferencesCount"]

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
        """Create an instance of Collection from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Collection from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "scope": obj.get("scope"),
            "authorFreetext": obj.get("authorFreetext"),
            "orderAscending": obj.get("orderAscending"),
            "level0": obj.get("level0"),
            "title": obj.get("title"),
            "description": obj.get("description"),
            "type": obj.get("type"),
            "viewtype": obj.get("viewtype"),
            "orderMode": obj.get("orderMode"),
            "x": obj.get("x"),
            "y": obj.get("y"),
            "z": obj.get("z"),
            "color": obj.get("color"),
            "fromUser": obj.get("fromUser"),
            "pinned": obj.get("pinned"),
            "childCollectionsCount": obj.get("childCollectionsCount"),
            "childReferencesCount": obj.get("childReferencesCount")
        })
        return _obj


