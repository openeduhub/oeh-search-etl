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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class ManualRegistrationData(BaseModel):
    """
    ManualRegistrationData
    """ # noqa: E501
    tool_name: Optional[StrictStr] = Field(default=None, alias="toolName")
    tool_url: Optional[StrictStr] = Field(default=None, alias="toolUrl")
    tool_description: Optional[StrictStr] = Field(default=None, alias="toolDescription")
    keyset_url: Optional[StrictStr] = Field(default=None, alias="keysetUrl")
    login_initiation_url: Optional[StrictStr] = Field(default=None, alias="loginInitiationUrl")
    redirection_urls: Optional[List[StrictStr]] = Field(default=None, alias="redirectionUrls")
    custom_parameters: Optional[List[StrictStr]] = Field(default=None, description="JSON Object where each value is a string. Custom parameters to be included in each launch to this tool. If a custom parameter is also defined at the message level, the message level value takes precedence. The value of the custom parameters may be substitution parameters as described in the LTI Core [LTI-13] specification. ", alias="customParameters")
    logo_url: Optional[StrictStr] = Field(default=None, alias="logoUrl")
    target_link_uri: StrictStr = Field(description="The default target link uri to use unless defined otherwise in the message or link definition", alias="targetLinkUri")
    target_link_uri_deep_link: Optional[StrictStr] = Field(default=None, description="The target link uri to use for DeepLing Message", alias="targetLinkUriDeepLink")
    client_name: StrictStr = Field(description="Name of the Tool to be presented to the End-User. Localized representations may be included as described in Section 2.1 of the [OIDC-Reg] specification. ", alias="clientName")
    __properties: ClassVar[List[str]] = ["toolName", "toolUrl", "toolDescription", "keysetUrl", "loginInitiationUrl", "redirectionUrls", "customParameters", "logoUrl", "targetLinkUri", "targetLinkUriDeepLink", "clientName"]

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
        """Create an instance of ManualRegistrationData from a JSON string"""
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
        """Create an instance of ManualRegistrationData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "toolName": obj.get("toolName"),
            "toolUrl": obj.get("toolUrl"),
            "toolDescription": obj.get("toolDescription"),
            "keysetUrl": obj.get("keysetUrl"),
            "loginInitiationUrl": obj.get("loginInitiationUrl"),
            "redirectionUrls": obj.get("redirectionUrls"),
            "customParameters": obj.get("customParameters"),
            "logoUrl": obj.get("logoUrl"),
            "targetLinkUri": obj.get("targetLinkUri"),
            "targetLinkUriDeepLink": obj.get("targetLinkUriDeepLink"),
            "clientName": obj.get("clientName")
        })
        return _obj


