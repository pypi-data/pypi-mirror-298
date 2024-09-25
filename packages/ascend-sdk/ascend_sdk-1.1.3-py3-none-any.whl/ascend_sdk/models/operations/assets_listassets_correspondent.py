"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.models.components import (
    httpmetadata as components_httpmetadata,
    listassetsresponse as components_listassetsresponse,
)
from ascend_sdk.models.errors import status as errors_status
from ascend_sdk.types import BaseModel
from ascend_sdk.utils import FieldMetadata, PathParamMetadata, QueryParamMetadata
import pydantic
from typing import Optional, TypedDict
from typing_extensions import Annotated, NotRequired


class AssetsListAssetsCorrespondentRequestTypedDict(TypedDict):
    correspondent_id: str
    r"""The correspondent id."""
    page_size: NotRequired[int]
    r"""The maximum number of assets to return. The service may return fewer than this value. Default is 100 (subject to change) The maximum is 1000, values exceeding this will be set to 1000 (subject to change)"""
    page_token: NotRequired[str]
    r"""A page token, received from a previous `ListAssets` call. Provide this to retrieve the subsequent page. When paginating, all other parameters provided to `ListAssets` must match the call that provided the page token in order to maintain a stable result set."""
    filter_: NotRequired[str]
    r"""A CEL string to filter results; See the [CEL Search](https://developer.apexclearing.com/apex-fintech-solutions/docs/cel-search) page in Guides for more information;"""


class AssetsListAssetsCorrespondentRequest(BaseModel):
    correspondent_id: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]
    r"""The correspondent id."""
    page_size: Annotated[
        Optional[int],
        FieldMetadata(query=QueryParamMetadata(style="form", explode=True)),
    ] = None
    r"""The maximum number of assets to return. The service may return fewer than this value. Default is 100 (subject to change) The maximum is 1000, values exceeding this will be set to 1000 (subject to change)"""
    page_token: Annotated[
        Optional[str],
        FieldMetadata(query=QueryParamMetadata(style="form", explode=True)),
    ] = None
    r"""A page token, received from a previous `ListAssets` call. Provide this to retrieve the subsequent page. When paginating, all other parameters provided to `ListAssets` must match the call that provided the page token in order to maintain a stable result set."""
    filter_: Annotated[
        Optional[str],
        pydantic.Field(alias="filter"),
        FieldMetadata(query=QueryParamMetadata(style="form", explode=True)),
    ] = None
    r"""A CEL string to filter results; See the [CEL Search](https://developer.apexclearing.com/apex-fintech-solutions/docs/cel-search) page in Guides for more information;"""


class AssetsListAssetsCorrespondentResponseTypedDict(TypedDict):
    http_meta: components_httpmetadata.HTTPMetadataTypedDict
    list_assets_response: NotRequired[
        components_listassetsresponse.ListAssetsResponseTypedDict
    ]
    r"""OK"""
    status: NotRequired[errors_status.Status]
    r"""INVALID_ARGUMENT: The request is not valid, additional information may be present in the BadRequest details."""


class AssetsListAssetsCorrespondentResponse(BaseModel):
    http_meta: Annotated[
        Optional[components_httpmetadata.HTTPMetadata], pydantic.Field(exclude=True)
    ] = None
    list_assets_response: Optional[
        components_listassetsresponse.ListAssetsResponse
    ] = None
    r"""OK"""
    status: Optional[errors_status.Status] = None
    r"""INVALID_ARGUMENT: The request is not valid, additional information may be present in the BadRequest details."""
