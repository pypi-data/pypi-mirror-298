# coding: utf-8

"""
    lakeFS API

    lakeFS HTTP API

    The version of the OpenAPI document: 1.0.0
    Contact: services@treeverse.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
try:
    from pydantic.v1 import BaseModel, Field, StrictBool, StrictStr
except ImportError:
    from pydantic import BaseModel, Field, StrictBool, StrictStr

class CommPrefsInput(BaseModel):
    """
    CommPrefsInput
    """
    email: Optional[StrictStr] = Field(None, description="the provided email")
    feature_updates: StrictBool = Field(..., alias="featureUpdates", description="user preference to receive feature updates")
    security_updates: StrictBool = Field(..., alias="securityUpdates", description="user preference to receive security updates")
    __properties = ["email", "featureUpdates", "securityUpdates"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> CommPrefsInput:
        """Create an instance of CommPrefsInput from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CommPrefsInput:
        """Create an instance of CommPrefsInput from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CommPrefsInput.parse_obj(obj)

        _obj = CommPrefsInput.parse_obj({
            "email": obj.get("email"),
            "feature_updates": obj.get("featureUpdates"),
            "security_updates": obj.get("securityUpdates")
        })
        return _obj


