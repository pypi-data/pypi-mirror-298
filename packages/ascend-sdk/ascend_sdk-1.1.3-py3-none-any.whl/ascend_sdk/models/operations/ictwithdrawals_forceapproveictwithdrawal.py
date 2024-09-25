"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.models.components import (
    forceapproveictwithdrawalrequestcreate as components_forceapproveictwithdrawalrequestcreate,
    httpmetadata as components_httpmetadata,
    ictwithdrawal as components_ictwithdrawal,
)
from ascend_sdk.models.errors import status as errors_status
from ascend_sdk.types import BaseModel
from ascend_sdk.utils import FieldMetadata, PathParamMetadata, RequestMetadata
import pydantic
from typing import Optional, TypedDict
from typing_extensions import Annotated, NotRequired


class IctWithdrawalsForceApproveIctWithdrawalRequestTypedDict(TypedDict):
    account_id: str
    r"""The account id."""
    ict_withdrawal_id: str
    r"""The ictWithdrawal id."""
    force_approve_ict_withdrawal_request_create: components_forceapproveictwithdrawalrequestcreate.ForceApproveIctWithdrawalRequestCreateTypedDict


class IctWithdrawalsForceApproveIctWithdrawalRequest(BaseModel):
    account_id: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]
    r"""The account id."""
    ict_withdrawal_id: Annotated[
        str,
        pydantic.Field(alias="ictWithdrawal_id"),
        FieldMetadata(path=PathParamMetadata(style="simple", explode=False)),
    ]
    r"""The ictWithdrawal id."""
    force_approve_ict_withdrawal_request_create: Annotated[
        components_forceapproveictwithdrawalrequestcreate.ForceApproveIctWithdrawalRequestCreate,
        FieldMetadata(request=RequestMetadata(media_type="application/json")),
    ]


class IctWithdrawalsForceApproveIctWithdrawalResponseTypedDict(TypedDict):
    http_meta: components_httpmetadata.HTTPMetadataTypedDict
    ict_withdrawal: NotRequired[components_ictwithdrawal.IctWithdrawalTypedDict]
    r"""OK"""
    status: NotRequired[errors_status.Status]
    r"""INVALID_ARGUMENT: The request has an invalid argument."""


class IctWithdrawalsForceApproveIctWithdrawalResponse(BaseModel):
    http_meta: Annotated[
        Optional[components_httpmetadata.HTTPMetadata], pydantic.Field(exclude=True)
    ] = None
    ict_withdrawal: Optional[components_ictwithdrawal.IctWithdrawal] = None
    r"""OK"""
    status: Optional[errors_status.Status] = None
    r"""INVALID_ARGUMENT: The request has an invalid argument."""
