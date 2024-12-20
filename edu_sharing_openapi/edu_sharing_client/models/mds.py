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

from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from edu_sharing_client.models.create import Create
from edu_sharing_client.models.mds_group import MdsGroup
from edu_sharing_client.models.mds_list import MdsList
from edu_sharing_client.models.mds_sort import MdsSort
from edu_sharing_client.models.mds_view import MdsView
from edu_sharing_client.models.mds_widget import MdsWidget
from typing import Optional, Set
from typing_extensions import Self

class Mds(BaseModel):
    """
    Mds
    """ # noqa: E501
    name: StrictStr
    create: Optional[Create] = None
    widgets: List[MdsWidget]
    views: List[MdsView]
    groups: List[MdsGroup]
    lists: List[MdsList]
    sorts: List[MdsSort]
    __properties: ClassVar[List[str]] = ["name", "create", "widgets", "views", "groups", "lists", "sorts"]

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
        """Create an instance of Mds from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of create
        if self.create:
            _dict['create'] = self.create.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in widgets (list)
        _items = []
        if self.widgets:
            for _item_widgets in self.widgets:
                if _item_widgets:
                    _items.append(_item_widgets.to_dict())
            _dict['widgets'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in views (list)
        _items = []
        if self.views:
            for _item_views in self.views:
                if _item_views:
                    _items.append(_item_views.to_dict())
            _dict['views'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in groups (list)
        _items = []
        if self.groups:
            for _item_groups in self.groups:
                if _item_groups:
                    _items.append(_item_groups.to_dict())
            _dict['groups'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in lists (list)
        _items = []
        if self.lists:
            for _item_lists in self.lists:
                if _item_lists:
                    _items.append(_item_lists.to_dict())
            _dict['lists'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in sorts (list)
        _items = []
        if self.sorts:
            for _item_sorts in self.sorts:
                if _item_sorts:
                    _items.append(_item_sorts.to_dict())
            _dict['sorts'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Mds from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "create": Create.from_dict(obj["create"]) if obj.get("create") is not None else None,
            "widgets": [MdsWidget.from_dict(_item) for _item in obj["widgets"]] if obj.get("widgets") is not None else None,
            "views": [MdsView.from_dict(_item) for _item in obj["views"]] if obj.get("views") is not None else None,
            "groups": [MdsGroup.from_dict(_item) for _item in obj["groups"]] if obj.get("groups") is not None else None,
            "lists": [MdsList.from_dict(_item) for _item in obj["lists"]] if obj.get("lists") is not None else None,
            "sorts": [MdsSort.from_dict(_item) for _item in obj["sorts"]] if obj.get("sorts") is not None else None
        })
        return _obj

