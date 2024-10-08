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

from pydantic import BaseModel, ConfigDict, Field, StrictBool
from typing import Any, ClassVar, Dict, List, Optional
from edu_sharing_client.models.node import Node
from edu_sharing_client.models.person import Person
from typing import Optional, Set
from typing_extensions import Self

class SharingInfo(BaseModel):
    """
    SharingInfo
    """ # noqa: E501
    password_matches: Optional[StrictBool] = Field(default=None, alias="passwordMatches")
    password: Optional[StrictBool] = None
    expired: Optional[StrictBool] = None
    invited_by: Optional[Person] = Field(default=None, alias="invitedBy")
    node: Optional[Node] = None
    __properties: ClassVar[List[str]] = ["passwordMatches", "password", "expired", "invitedBy", "node"]

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
        """Create an instance of SharingInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of invited_by
        if self.invited_by:
            _dict['invitedBy'] = self.invited_by.to_dict()
        # override the default output from pydantic by calling `to_dict()` of node
        if self.node:
            _dict['node'] = self.node.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SharingInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "passwordMatches": obj.get("passwordMatches"),
            "password": obj.get("password"),
            "expired": obj.get("expired"),
            "invitedBy": Person.from_dict(obj["invitedBy"]) if obj.get("invitedBy") is not None else None,
            "node": Node.from_dict(obj["node"]) if obj.get("node") is not None else None
        })
        return _obj


