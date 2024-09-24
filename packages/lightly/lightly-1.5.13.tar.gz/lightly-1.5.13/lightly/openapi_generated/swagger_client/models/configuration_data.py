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


from typing import List
try:
    # Pydantic >=v1.10.17
    from pydantic.v1 import BaseModel, Field, StrictStr, conint, conlist, constr, validator
except ImportError:
    # Pydantic v1
    from pydantic import BaseModel, Field, StrictStr, conint, conlist, constr, validator
from lightly.openapi_generated.swagger_client.models.configuration_entry import ConfigurationEntry

class ConfigurationData(BaseModel):
    """
    ConfigurationData
    """
    id: constr(strict=True) = Field(..., description="MongoDB ObjectId")
    name: StrictStr = Field(...)
    configs: conlist(ConfigurationEntry) = Field(...)
    created_at: conint(strict=True, ge=0) = Field(..., alias="createdAt", description="unix timestamp in milliseconds")
    last_modified_at: conint(strict=True, ge=0) = Field(..., alias="lastModifiedAt", description="unix timestamp in milliseconds")
    __properties = ["id", "name", "configs", "createdAt", "lastModifiedAt"]

    @validator('id')
    def id_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[a-f0-9]{24}$", value):
            raise ValueError(r"must validate the regular expression /^[a-f0-9]{24}$/")
        return value

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
    def from_json(cls, json_str: str) -> ConfigurationData:
        """Create an instance of ConfigurationData from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self, by_alias: bool = False):
        """Returns the dictionary representation of the model"""
        _dict = self.dict(by_alias=by_alias,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in configs (list)
        _items = []
        if self.configs:
            for _item in self.configs:
                if _item:
                    _items.append(_item.to_dict(by_alias=by_alias))
            _dict['configs' if by_alias else 'configs'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ConfigurationData:
        """Create an instance of ConfigurationData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ConfigurationData.parse_obj(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in ConfigurationData) in the input: " + str(obj))

        _obj = ConfigurationData.parse_obj({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "configs": [ConfigurationEntry.from_dict(_item) for _item in obj.get("configs")] if obj.get("configs") is not None else None,
            "created_at": obj.get("createdAt"),
            "last_modified_at": obj.get("lastModifiedAt")
        })
        return _obj

