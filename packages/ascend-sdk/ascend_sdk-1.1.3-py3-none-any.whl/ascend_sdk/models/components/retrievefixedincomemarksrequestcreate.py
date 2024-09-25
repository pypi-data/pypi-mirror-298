"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .retrievefixedincomemarksrequest_securityidentifierscreate import (
    RetrieveFixedIncomeMarksRequestSecurityIdentifiersCreate,
    RetrieveFixedIncomeMarksRequestSecurityIdentifiersCreateTypedDict,
)
from ascend_sdk.types import BaseModel
from typing import List, TypedDict


class RetrieveFixedIncomeMarksRequestCreateTypedDict(TypedDict):
    r"""Request object for retrieving fixed income marks"""

    parent: str
    r"""The parent resource where this price will be sourced under. Format: correspondents/{correspondent_id}"""
    security_identifiers: List[
        RetrieveFixedIncomeMarksRequestSecurityIdentifiersCreateTypedDict
    ]
    r"""Identifiers specifying for which assets mark data should be returned. A maximum of 100 identifiers are allowed. At least one identifier must be provided in the request."""


class RetrieveFixedIncomeMarksRequestCreate(BaseModel):
    r"""Request object for retrieving fixed income marks"""

    parent: str
    r"""The parent resource where this price will be sourced under. Format: correspondents/{correspondent_id}"""
    security_identifiers: List[RetrieveFixedIncomeMarksRequestSecurityIdentifiersCreate]
    r"""Identifiers specifying for which assets mark data should be returned. A maximum of 100 identifiers are allowed. At least one identifier must be provided in the request."""
