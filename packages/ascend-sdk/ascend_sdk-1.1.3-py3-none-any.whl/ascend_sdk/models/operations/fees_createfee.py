"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.models.components import (
    httpmetadata as components_httpmetadata,
    transfersfee as components_transfersfee,
    transfersfeecreate as components_transfersfeecreate,
)
from ascend_sdk.models.errors import status as errors_status
from ascend_sdk.types import BaseModel
from ascend_sdk.utils import FieldMetadata, PathParamMetadata, RequestMetadata
import pydantic
from typing import Optional, TypedDict
from typing_extensions import Annotated, NotRequired


class FeesCreateFeeRequestTypedDict(TypedDict):
    account_id: str
    r"""The account id."""
    transfers_fee_create: components_transfersfeecreate.TransfersFeeCreateTypedDict


class FeesCreateFeeRequest(BaseModel):
    account_id: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]
    r"""The account id."""
    transfers_fee_create: Annotated[
        components_transfersfeecreate.TransfersFeeCreate,
        FieldMetadata(request=RequestMetadata(media_type="application/json")),
    ]


class FeesCreateFeeResponseTypedDict(TypedDict):
    http_meta: components_httpmetadata.HTTPMetadataTypedDict
    transfers_fee: NotRequired[components_transfersfee.TransfersFeeTypedDict]
    r"""OK"""
    status: NotRequired[errors_status.Status]
    r"""INVALID_ARGUMENT: The request has an invalid argument."""


class FeesCreateFeeResponse(BaseModel):
    http_meta: Annotated[
        Optional[components_httpmetadata.HTTPMetadata], pydantic.Field(exclude=True)
    ] = None
    transfers_fee: Optional[components_transfersfee.TransfersFee] = None
    r"""OK"""
    status: Optional[errors_status.Status] = None
    r"""INVALID_ARGUMENT: The request has an invalid argument."""
