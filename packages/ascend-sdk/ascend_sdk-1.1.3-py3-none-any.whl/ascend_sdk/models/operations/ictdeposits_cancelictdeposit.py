"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.models.components import (
    cancelictdepositrequestcreate as components_cancelictdepositrequestcreate,
    httpmetadata as components_httpmetadata,
    ictdeposit as components_ictdeposit,
)
from ascend_sdk.models.errors import status as errors_status
from ascend_sdk.types import BaseModel
from ascend_sdk.utils import FieldMetadata, PathParamMetadata, RequestMetadata
import pydantic
from typing import Optional, TypedDict
from typing_extensions import Annotated, NotRequired


class IctDepositsCancelIctDepositRequestTypedDict(TypedDict):
    account_id: str
    r"""The account id."""
    ict_deposit_id: str
    r"""The ictDeposit id."""
    cancel_ict_deposit_request_create: components_cancelictdepositrequestcreate.CancelIctDepositRequestCreateTypedDict


class IctDepositsCancelIctDepositRequest(BaseModel):
    account_id: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]
    r"""The account id."""
    ict_deposit_id: Annotated[
        str,
        pydantic.Field(alias="ictDeposit_id"),
        FieldMetadata(path=PathParamMetadata(style="simple", explode=False)),
    ]
    r"""The ictDeposit id."""
    cancel_ict_deposit_request_create: Annotated[
        components_cancelictdepositrequestcreate.CancelIctDepositRequestCreate,
        FieldMetadata(request=RequestMetadata(media_type="application/json")),
    ]


class IctDepositsCancelIctDepositResponseTypedDict(TypedDict):
    http_meta: components_httpmetadata.HTTPMetadataTypedDict
    ict_deposit: NotRequired[components_ictdeposit.IctDepositTypedDict]
    r"""OK"""
    status: NotRequired[errors_status.Status]
    r"""INVALID_ARGUMENT: The request has an invalid argument."""


class IctDepositsCancelIctDepositResponse(BaseModel):
    http_meta: Annotated[
        Optional[components_httpmetadata.HTTPMetadata], pydantic.Field(exclude=True)
    ] = None
    ict_deposit: Optional[components_ictdeposit.IctDeposit] = None
    r"""OK"""
    status: Optional[errors_status.Status] = None
    r"""INVALID_ARGUMENT: The request has an invalid argument."""
