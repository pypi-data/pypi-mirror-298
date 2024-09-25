"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.models.components import (
    deactivateenrollmentrequestcreate as components_deactivateenrollmentrequestcreate,
    enrollment as components_enrollment,
    httpmetadata as components_httpmetadata,
)
from ascend_sdk.models.errors import status as errors_status
from ascend_sdk.types import BaseModel
from ascend_sdk.utils import FieldMetadata, PathParamMetadata, RequestMetadata
import pydantic
from typing import Optional, TypedDict
from typing_extensions import Annotated, NotRequired


class AccountsDeactivateEnrollmentRequestTypedDict(TypedDict):
    account_id: str
    r"""The account id."""
    deactivate_enrollment_request_create: components_deactivateenrollmentrequestcreate.DeactivateEnrollmentRequestCreateTypedDict


class AccountsDeactivateEnrollmentRequest(BaseModel):
    account_id: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]
    r"""The account id."""
    deactivate_enrollment_request_create: Annotated[
        components_deactivateenrollmentrequestcreate.DeactivateEnrollmentRequestCreate,
        FieldMetadata(request=RequestMetadata(media_type="application/json")),
    ]


class AccountsDeactivateEnrollmentResponseTypedDict(TypedDict):
    http_meta: components_httpmetadata.HTTPMetadataTypedDict
    enrollment: NotRequired[components_enrollment.EnrollmentTypedDict]
    r"""OK"""
    status: NotRequired[errors_status.Status]
    r"""INVALID_ARGUMENT: The request is not valid, additional information may be present in the BadRequest details."""


class AccountsDeactivateEnrollmentResponse(BaseModel):
    http_meta: Annotated[
        Optional[components_httpmetadata.HTTPMetadata], pydantic.Field(exclude=True)
    ] = None
    enrollment: Optional[components_enrollment.Enrollment] = None
    r"""OK"""
    status: Optional[errors_status.Status] = None
    r"""INVALID_ARGUMENT: The request is not valid, additional information may be present in the BadRequest details."""
