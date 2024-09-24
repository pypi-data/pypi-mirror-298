# coding: utf-8

"""
    Lightly API

    Lightly.ai enables you to do self-supervised learning in an easy and intuitive way. The lightly.ai OpenAPI spec defines how one can interact with our REST API to unleash the full potential of lightly.ai  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: support@lightly.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional, Union
try:
    # Pydantic >=v1.10.17
    from pydantic.v1 import BaseModel, Field, confloat, conint
except ImportError:
    # Pydantic v1
    from pydantic import BaseModel, Field, confloat, conint

class DockerRunLogDockerLoad(BaseModel):
    """
    The load of the docker container when the log entry was created.
    """
    cpu: Optional[Union[confloat(le=100, ge=0, strict=True), conint(le=100, ge=0, strict=True)]] = Field(None, description="The cpu usage in percent.")
    mem: Optional[Union[confloat(le=100, ge=0, strict=True), conint(le=100, ge=0, strict=True)]] = Field(None, description="The memory usage in percent.")
    __properties = ["cpu", "mem"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"

    def to_str(self, by_alias: bool = False) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.dict(by_alias=by_alias))

    def to_json(self, by_alias: bool = False) -> str:
        """Returns the JSON representation of the model"""
        return json.dumps(self.to_dict(by_alias=by_alias))

    @classmethod
    def from_json(cls, json_str: str) -> DockerRunLogDockerLoad:
        """Create an instance of DockerRunLogDockerLoad from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self, by_alias: bool = False):
        """Returns the dictionary representation of the model"""
        _dict = self.dict(by_alias=by_alias,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DockerRunLogDockerLoad:
        """Create an instance of DockerRunLogDockerLoad from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DockerRunLogDockerLoad.parse_obj(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in DockerRunLogDockerLoad) in the input: " + str(obj))

        _obj = DockerRunLogDockerLoad.parse_obj({
            "cpu": obj.get("cpu"),
            "mem": obj.get("mem")
        })
        return _obj

