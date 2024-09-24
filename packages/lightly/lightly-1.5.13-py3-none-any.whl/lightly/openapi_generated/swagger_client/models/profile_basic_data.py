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


from typing import List, Optional
try:
    # Pydantic >=v1.10.17
    from pydantic.v1 import BaseModel, Field, StrictStr, conint, conlist
except ImportError:
    # Pydantic v1
    from pydantic import BaseModel, Field, StrictStr, conint, conlist
from lightly.openapi_generated.swagger_client.models.team_basic_data import TeamBasicData

class ProfileBasicData(BaseModel):
    """
    ProfileBasicData
    """
    id: StrictStr = Field(...)
    nickname: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
    given_name: Optional[StrictStr] = Field(None, alias="givenName")
    family_name: Optional[StrictStr] = Field(None, alias="familyName")
    email: Optional[StrictStr] = None
    created_at: conint(strict=True, ge=0) = Field(..., alias="createdAt", description="unix timestamp in milliseconds")
    teams: Optional[conlist(TeamBasicData)] = None
    __properties = ["id", "nickname", "name", "givenName", "familyName", "email", "createdAt", "teams"]

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
    def from_json(cls, json_str: str) -> ProfileBasicData:
        """Create an instance of ProfileBasicData from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self, by_alias: bool = False):
        """Returns the dictionary representation of the model"""
        _dict = self.dict(by_alias=by_alias,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in teams (list)
        _items = []
        if self.teams:
            for _item in self.teams:
                if _item:
                    _items.append(_item.to_dict(by_alias=by_alias))
            _dict['teams' if by_alias else 'teams'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProfileBasicData:
        """Create an instance of ProfileBasicData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProfileBasicData.parse_obj(obj)

        # raise errors for additional fields in the input
        for _key in obj.keys():
            if _key not in cls.__properties:
                raise ValueError("Error due to additional fields (not defined in ProfileBasicData) in the input: " + str(obj))

        _obj = ProfileBasicData.parse_obj({
            "id": obj.get("id"),
            "nickname": obj.get("nickname"),
            "name": obj.get("name"),
            "given_name": obj.get("givenName"),
            "family_name": obj.get("familyName"),
            "email": obj.get("email"),
            "created_at": obj.get("createdAt"),
            "teams": [TeamBasicData.from_dict(_item) for _item in obj.get("teams")] if obj.get("teams") is not None else None
        })
        return _obj

