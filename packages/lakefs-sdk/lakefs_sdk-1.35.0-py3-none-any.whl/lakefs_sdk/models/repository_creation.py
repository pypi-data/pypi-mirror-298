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
    from pydantic.v1 import BaseModel, Field, StrictBool, StrictStr, constr, validator
except ImportError:
    from pydantic import BaseModel, Field, StrictBool, StrictStr, constr, validator

class RepositoryCreation(BaseModel):
    """
    RepositoryCreation
    """
    name: constr(strict=True) = Field(...)
    storage_namespace: constr(strict=True) = Field(..., description="Filesystem URI to store the underlying data in (e.g. \"s3://my-bucket/some/path/\")")
    default_branch: Optional[StrictStr] = None
    sample_data: Optional[StrictBool] = False
    read_only: Optional[StrictBool] = False
    __properties = ["name", "storage_namespace", "default_branch", "sample_data", "read_only"]

    @validator('name')
    def name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-z0-9][a-z0-9-]{2,62}$", value):
            raise ValueError(r"must validate the regular expression /^[a-z0-9][a-z0-9-]{2,62}$/")
        return value

    @validator('storage_namespace')
    def storage_namespace_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^(s3|gs|https?|mem|local|transient):\/\/.*$", value):
            raise ValueError(r"must validate the regular expression /^(s3|gs|https?|mem|local|transient):\/\/.*$/")
        return value

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
    def from_json(cls, json_str: str) -> RepositoryCreation:
        """Create an instance of RepositoryCreation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RepositoryCreation:
        """Create an instance of RepositoryCreation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RepositoryCreation.parse_obj(obj)

        _obj = RepositoryCreation.parse_obj({
            "name": obj.get("name"),
            "storage_namespace": obj.get("storage_namespace"),
            "default_branch": obj.get("default_branch"),
            "sample_data": obj.get("sample_data") if obj.get("sample_data") is not None else False,
            "read_only": obj.get("read_only") if obj.get("read_only") is not None else False
        })
        return _obj


