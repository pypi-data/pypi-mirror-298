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
    from pydantic.v1 import BaseModel, Field, StrictStr, conint
except ImportError:
    # Pydantic v1
    from pydantic import BaseModel, Field, StrictStr, conint
from lightly.openapi_generated.swagger_client.models.docker_run_log_docker_load import DockerRunLogDockerLoad
from lightly.openapi_generated.swagger_client.models.docker_run_log_level import DockerRunLogLevel
from lightly.openapi_generated.swagger_client.models.docker_run_state import DockerRunState

class DockerRunLogEntryData(BaseModel):
    """
    DockerRunLogEntryData
    """
    ts: conint(strict=True, ge=0) = Field(..., description="unix timestamp in milliseconds")
    level: DockerRunLogLevel = Field(...)
    group: Optional[StrictStr] = Field(None, description="The logger name/group of the log entry.")
    origin: Optional[StrictStr] = Field(None, description="The origin/filename+loc from where a log entry was created from.")
    msg: StrictStr = Field(..., description="The actual log message.")
    state: DockerRunState = Field(...)
    load: Optional[DockerRunLogDockerLoad] = None
    __properties = ["ts", "level", "group", "origin", "msg", "state", "load"]

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
    def from_json(cls, json_str: str) -> DockerRunLogEntryData:
        """Create an instance of DockerRunLogEntryData from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self, by_alias: bool = False):
        """Returns the dictionary representation of the model"""
        _dict = self.dict(by_alias=by_alias,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of load
        if self.load:
            _dict['load' if by_alias else 'load'] = self.load.to_dict(by_alias=by_alias)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DockerRunLogEntryData:
        """Create an instance of DockerRunLogEntryData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DockerRunLogEntryData.parse_obj(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in DockerRunLogEntryData) in the input: " + str(obj))

        _obj = DockerRunLogEntryData.parse_obj({
            "ts": obj.get("ts"),
            "level": obj.get("level"),
            "group": obj.get("group"),
            "origin": obj.get("origin"),
            "msg": obj.get("msg"),
            "state": obj.get("state"),
            "load": DockerRunLogDockerLoad.from_dict(obj.get("load")) if obj.get("load") is not None else None
        })
        return _obj

