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


from typing import Dict, Optional
try:
    from pydantic.v1 import BaseModel, Field, StrictStr
except ImportError:
    from pydantic import BaseModel, Field, StrictStr

class CommitOverrides(BaseModel):
    """
    CommitOverrides
    """
    message: Optional[StrictStr] = Field(None, description="replace the commit message")
    metadata: Optional[Dict[str, StrictStr]] = Field(None, description="replace the metadata of the commit")
    __properties = ["message", "metadata"]

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
    def from_json(cls, json_str: str) -> CommitOverrides:
        """Create an instance of CommitOverrides from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CommitOverrides:
        """Create an instance of CommitOverrides from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CommitOverrides.parse_obj(obj)

        _obj = CommitOverrides.parse_obj({
            "message": obj.get("message"),
            "metadata": obj.get("metadata")
        })
        return _obj


