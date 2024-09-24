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


from typing import Optional
try:
    # Pydantic >=v1.10.17
    from pydantic.v1 import BaseModel, Field
except ImportError:
    # Pydantic v1
    from pydantic import BaseModel, Field
from lightly.openapi_generated.swagger_client.models.docker_worker_config import DockerWorkerConfig

class DockerWorkerConfigV0DataAllOf(BaseModel):
    """
    DockerWorkerConfigV0DataAllOf
    """
    config: DockerWorkerConfig = Field(...)
    config_orig: Optional[DockerWorkerConfig] = Field(None, alias="configOrig")
    __properties = ["config", "configOrig"]

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
    def from_json(cls, json_str: str) -> DockerWorkerConfigV0DataAllOf:
        """Create an instance of DockerWorkerConfigV0DataAllOf from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self, by_alias: bool = False):
        """Returns the dictionary representation of the model"""
        _dict = self.dict(by_alias=by_alias,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of config
        if self.config:
            _dict['config' if by_alias else 'config'] = self.config.to_dict(by_alias=by_alias)
        # override the default output from pydantic by calling `to_dict()` of config_orig
        if self.config_orig:
            _dict['configOrig' if by_alias else 'config_orig'] = self.config_orig.to_dict(by_alias=by_alias)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DockerWorkerConfigV0DataAllOf:
        """Create an instance of DockerWorkerConfigV0DataAllOf from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DockerWorkerConfigV0DataAllOf.parse_obj(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in DockerWorkerConfigV0DataAllOf) in the input: " + str(obj))

        _obj = DockerWorkerConfigV0DataAllOf.parse_obj({
            "config": DockerWorkerConfig.from_dict(obj.get("config")) if obj.get("config") is not None else None,
            "config_orig": DockerWorkerConfig.from_dict(obj.get("configOrig")) if obj.get("configOrig") is not None else None
        })
        return _obj

