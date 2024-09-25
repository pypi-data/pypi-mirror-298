"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import (
    BaseModel,
    Nullable,
    OptionalNullable,
    UNSET,
    UNSET_SENTINEL,
)
from datetime import datetime
from pydantic import model_serializer
from typing import List, Optional, TypedDict
from typing_extensions import NotRequired


class IdentityVerificationResultTypedDict(TypedDict):
    r"""A summary of the results from a identity verification check"""

    create_time: NotRequired[Nullable[datetime]]
    r"""The time the identity verification result was created"""
    customer_identification_id: NotRequired[str]
    r"""The resource identifier for the CIP service The format is \"customerIdentificationResults/{customer_identification_id}\" """
    document_ids: NotRequired[List[str]]
    r"""If identity verification result is verified by a document(s) upload, this is the document id(s) relating to that"""
    external_vendor: NotRequired[str]
    r"""The external vendor name that verified the identity verification result"""
    identity_verification_passed: NotRequired[bool]
    r"""Whether the overall identity verification check has passed or not"""
    identity_verification_types: NotRequired[List[str]]
    r"""Describes the type of Identity Verification that was performed"""
    provided_by: NotRequired[str]
    r"""Who provided the identity verification result"""


class IdentityVerificationResult(BaseModel):
    r"""A summary of the results from a identity verification check"""

    create_time: OptionalNullable[datetime] = UNSET
    r"""The time the identity verification result was created"""
    customer_identification_id: Optional[str] = None
    r"""The resource identifier for the CIP service The format is \"customerIdentificationResults/{customer_identification_id}\" """
    document_ids: Optional[List[str]] = None
    r"""If identity verification result is verified by a document(s) upload, this is the document id(s) relating to that"""
    external_vendor: Optional[str] = None
    r"""The external vendor name that verified the identity verification result"""
    identity_verification_passed: Optional[bool] = None
    r"""Whether the overall identity verification check has passed or not"""
    identity_verification_types: Optional[List[str]] = None
    r"""Describes the type of Identity Verification that was performed"""
    provided_by: Optional[str] = None
    r"""Who provided the identity verification result"""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = [
            "create_time",
            "customer_identification_id",
            "document_ids",
            "external_vendor",
            "identity_verification_passed",
            "identity_verification_types",
            "provided_by",
        ]
        nullable_fields = ["create_time"]
        null_default_fields = []

        serialized = handler(self)

        m = {}

        for n, f in self.model_fields.items():
            k = f.alias or n
            val = serialized.get(k)

            optional_nullable = k in optional_fields and k in nullable_fields
            is_set = (
                self.__pydantic_fields_set__.intersection({n})
                or k in null_default_fields
            )  # pylint: disable=no-member

            if val is not None and val != UNSET_SENTINEL:
                m[k] = val
            elif val != UNSET_SENTINEL and (
                not k in optional_fields or (optional_nullable and is_set)
            ):
                m[k] = val

        return m
