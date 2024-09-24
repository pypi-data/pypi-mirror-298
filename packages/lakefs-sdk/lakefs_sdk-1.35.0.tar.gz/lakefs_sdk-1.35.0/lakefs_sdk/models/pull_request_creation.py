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



try:
    from pydantic.v1 import BaseModel, Field, StrictStr
except ImportError:
    from pydantic import BaseModel, Field, StrictStr

class PullRequestCreation(BaseModel):
    """
    PullRequestCreation
    """
    title: StrictStr = Field(...)
    description: StrictStr = Field(...)
    source_branch: StrictStr = Field(...)
    destination_branch: StrictStr = Field(...)
    __properties = ["title", "description", "source_branch", "destination_branch"]

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
    def from_json(cls, json_str: str) -> PullRequestCreation:
        """Create an instance of PullRequestCreation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PullRequestCreation:
        """Create an instance of PullRequestCreation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PullRequestCreation.parse_obj(obj)

        _obj = PullRequestCreation.parse_obj({
            "title": obj.get("title"),
            "description": obj.get("description"),
            "source_branch": obj.get("source_branch"),
            "destination_branch": obj.get("destination_branch")
        })
        return _obj


