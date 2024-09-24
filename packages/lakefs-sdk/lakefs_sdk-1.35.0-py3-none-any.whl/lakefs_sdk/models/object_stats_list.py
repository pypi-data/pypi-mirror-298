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


from typing import List
try:
    from pydantic.v1 import BaseModel, Field, conlist
except ImportError:
    from pydantic import BaseModel, Field, conlist
from lakefs_sdk.models.object_stats import ObjectStats
from lakefs_sdk.models.pagination import Pagination

class ObjectStatsList(BaseModel):
    """
    ObjectStatsList
    """
    pagination: Pagination = Field(...)
    results: conlist(ObjectStats) = Field(...)
    __properties = ["pagination", "results"]

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
    def from_json(cls, json_str: str) -> ObjectStatsList:
        """Create an instance of ObjectStatsList from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of pagination
        if self.pagination:
            _dict['pagination'] = self.pagination.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in results (list)
        _items = []
        if self.results:
            for _item in self.results:
                if _item:
                    _items.append(_item.to_dict())
            _dict['results'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ObjectStatsList:
        """Create an instance of ObjectStatsList from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ObjectStatsList.parse_obj(obj)

        _obj = ObjectStatsList.parse_obj({
            "pagination": Pagination.from_dict(obj.get("pagination")) if obj.get("pagination") is not None else None,
            "results": [ObjectStats.from_dict(_item) for _item in obj.get("results")] if obj.get("results") is not None else None
        })
        return _obj


