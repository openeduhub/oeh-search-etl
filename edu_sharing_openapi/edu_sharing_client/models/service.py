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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from edu_sharing_client.models.audience import Audience
from edu_sharing_client.models.interface import Interface
from edu_sharing_client.models.provider import Provider
from typing import Optional, Set
from typing_extensions import Self

class Service(BaseModel):
    """
    Service
    """ # noqa: E501
    name: Optional[StrictStr] = None
    url: Optional[StrictStr] = None
    icon: Optional[StrictStr] = None
    logo: Optional[StrictStr] = None
    in_language: Optional[StrictStr] = Field(default=None, alias="inLanguage")
    type: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    audience: Optional[List[Audience]] = None
    provider: Optional[Provider] = None
    start_date: Optional[StrictStr] = Field(default=None, alias="startDate")
    interfaces: Optional[List[Interface]] = None
    about: Optional[List[StrictStr]] = None
    is_accessible_for_free: Optional[StrictBool] = Field(default=None, alias="isAccessibleForFree")
    __properties: ClassVar[List[str]] = ["name", "url", "icon", "logo", "inLanguage", "type", "description", "audience", "provider", "startDate", "interfaces", "about", "isAccessibleForFree"]

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
        """Create an instance of Service from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in audience (list)
        _items = []
        if self.audience:
            for _item_audience in self.audience:
                if _item_audience:
                    _items.append(_item_audience.to_dict())
            _dict['audience'] = _items
        # override the default output from pydantic by calling `to_dict()` of provider
        if self.provider:
            _dict['provider'] = self.provider.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in interfaces (list)
        _items = []
        if self.interfaces:
            for _item_interfaces in self.interfaces:
                if _item_interfaces:
                    _items.append(_item_interfaces.to_dict())
            _dict['interfaces'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Service from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "url": obj.get("url"),
            "icon": obj.get("icon"),
            "logo": obj.get("logo"),
            "inLanguage": obj.get("inLanguage"),
            "type": obj.get("type"),
            "description": obj.get("description"),
            "audience": [Audience.from_dict(_item) for _item in obj["audience"]] if obj.get("audience") is not None else None,
            "provider": Provider.from_dict(obj["provider"]) if obj.get("provider") is not None else None,
            "startDate": obj.get("startDate"),
            "interfaces": [Interface.from_dict(_item) for _item in obj["interfaces"]] if obj.get("interfaces") is not None else None,
            "about": obj.get("about"),
            "isAccessibleForFree": obj.get("isAccessibleForFree")
        })
        return _obj


