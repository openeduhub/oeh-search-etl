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
from edu_sharing_client.models.job_builder import JobBuilder
from edu_sharing_client.models.job_detail_job_data_map import JobDetailJobDataMap
from edu_sharing_client.models.job_key import JobKey
from typing import Optional, Set
from typing_extensions import Self

class JobDetail(BaseModel):
    """
    JobDetail
    """ # noqa: E501
    key: Optional[JobKey] = None
    job_data_map: Optional[JobDetailJobDataMap] = Field(default=None, alias="jobDataMap")
    durable: Optional[StrictBool] = None
    persist_job_data_after_execution: Optional[StrictBool] = Field(default=None, alias="persistJobDataAfterExecution")
    concurrent_exection_disallowed: Optional[StrictBool] = Field(default=None, alias="concurrentExectionDisallowed")
    job_builder: Optional[JobBuilder] = Field(default=None, alias="jobBuilder")
    description: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["key", "jobDataMap", "durable", "persistJobDataAfterExecution", "concurrentExectionDisallowed", "jobBuilder", "description"]

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
        """Create an instance of JobDetail from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of key
        if self.key:
            _dict['key'] = self.key.to_dict()
        # override the default output from pydantic by calling `to_dict()` of job_data_map
        if self.job_data_map:
            _dict['jobDataMap'] = self.job_data_map.to_dict()
        # override the default output from pydantic by calling `to_dict()` of job_builder
        if self.job_builder:
            _dict['jobBuilder'] = self.job_builder.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of JobDetail from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "key": JobKey.from_dict(obj["key"]) if obj.get("key") is not None else None,
            "jobDataMap": JobDetailJobDataMap.from_dict(obj["jobDataMap"]) if obj.get("jobDataMap") is not None else None,
            "durable": obj.get("durable"),
            "persistJobDataAfterExecution": obj.get("persistJobDataAfterExecution"),
            "concurrentExectionDisallowed": obj.get("concurrentExectionDisallowed"),
            "jobBuilder": JobBuilder.from_dict(obj["jobBuilder"]) if obj.get("jobBuilder") is not None else None,
            "description": obj.get("description")
        })
        return _obj

