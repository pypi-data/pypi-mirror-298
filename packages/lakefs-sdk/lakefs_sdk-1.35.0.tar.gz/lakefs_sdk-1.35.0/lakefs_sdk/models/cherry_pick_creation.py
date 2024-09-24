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
    from pydantic.v1 import BaseModel, Field, StrictBool, StrictInt, StrictStr
except ImportError:
    from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr
from lakefs_sdk.models.commit_overrides import CommitOverrides

class CherryPickCreation(BaseModel):
    """
    CherryPickCreation
    """
    ref: StrictStr = Field(..., description="the commit to cherry-pick, given by a ref")
    parent_number: Optional[StrictInt] = Field(None, description="When cherry-picking a merge commit, the parent number (starting from 1) with which to perform the diff. The default branch is parent 1. ")
    commit_overrides: Optional[CommitOverrides] = None
    force: Optional[StrictBool] = False
    __properties = ["ref", "parent_number", "commit_overrides", "force"]

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
    def from_json(cls, json_str: str) -> CherryPickCreation:
        """Create an instance of CherryPickCreation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of commit_overrides
        if self.commit_overrides:
            _dict['commit_overrides'] = self.commit_overrides.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CherryPickCreation:
        """Create an instance of CherryPickCreation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CherryPickCreation.parse_obj(obj)

        _obj = CherryPickCreation.parse_obj({
            "ref": obj.get("ref"),
            "parent_number": obj.get("parent_number"),
            "commit_overrides": CommitOverrides.from_dict(obj.get("commit_overrides")) if obj.get("commit_overrides") is not None else None,
            "force": obj.get("force") if obj.get("force") is not None else False
        })
        return _obj


