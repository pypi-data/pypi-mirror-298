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





class DockerRunState(str, Enum):
    """
    DockerRunState
    """

    """
    allowed enum values
    """
    STARTED = 'STARTED'
    INITIALIZING = 'INITIALIZING'
    LOADING_DATASET = 'LOADING_DATASET'
    LOADING_METADATA = 'LOADING_METADATA'
    LOADING_PREDICTION = 'LOADING_PREDICTION'
    CHECKING_CORRUPTNESS = 'CHECKING_CORRUPTNESS'
    INITIALIZING_OBJECT_CROPS = 'INITIALIZING_OBJECT_CROPS'
    COMPUTING_METADATA = 'COMPUTING_METADATA'
    TRAINING = 'TRAINING'
    EMBEDDING = 'EMBEDDING'
    EMBEDDING_OBJECT_CROPS = 'EMBEDDING_OBJECT_CROPS'
    PRETAGGING = 'PRETAGGING'
    COMPUTING_ACTIVE_LEARNING_SCORES = 'COMPUTING_ACTIVE_LEARNING_SCORES'
    SAMPLING = 'SAMPLING'
    EMBEDDING_FULL_IMAGES = 'EMBEDDING_FULL_IMAGES'
    SAVING_RESULTS = 'SAVING_RESULTS'
    UPLOADING_DATASET = 'UPLOADING_DATASET'
    GENERATING_REPORT = 'GENERATING_REPORT'
    UPLOADING_REPORT = 'UPLOADING_REPORT'
    UPLOADED_REPORT = 'UPLOADED_REPORT'
    UPLOADING_ARTIFACTS = 'UPLOADING_ARTIFACTS'
    UPLOADED_ARTIFACTS = 'UPLOADED_ARTIFACTS'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    CRASHED = 'CRASHED'
    ABORTED = 'ABORTED'

    @classmethod
    def from_json(cls, json_str: str) -> 'DockerRunState':
        """Create an instance of DockerRunState from a JSON string"""
        return DockerRunState(json.loads(json_str))


