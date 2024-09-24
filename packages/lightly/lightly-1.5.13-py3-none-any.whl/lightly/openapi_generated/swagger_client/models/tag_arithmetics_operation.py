# coding: utf-8

"""
    Lightly API

    Lightly.ai enables you to do self-supervised learning in an easy and intuitive way. The lightly.ai OpenAPI spec defines how one can interact with our REST API to unleash the full potential of lightly.ai  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: support@lightly.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import json
import pprint
import re  # noqa: F401
from enum import Enum
from aenum import no_arg  # type: ignore





class TagArithmeticsOperation(str, Enum):
    """
    The possible arithmetic operations that can be done between multiple tags.
    """

    """
    allowed enum values
    """
    UNION = 'UNION'
    INTERSECTION = 'INTERSECTION'
    DIFFERENCE = 'DIFFERENCE'

    @classmethod
    def from_json(cls, json_str: str) -> 'TagArithmeticsOperation':
        """Create an instance of TagArithmeticsOperation from a JSON string"""
        return TagArithmeticsOperation(json.loads(json_str))


