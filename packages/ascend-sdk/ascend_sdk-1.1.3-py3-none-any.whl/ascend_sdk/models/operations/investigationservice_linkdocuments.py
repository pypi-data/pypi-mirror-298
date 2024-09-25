"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.models.components import (
    httpmetadata as components_httpmetadata,
    linkdocumentsrequestcreate as components_linkdocumentsrequestcreate,
    linkdocumentsresponse as components_linkdocumentsresponse,
)
from ascend_sdk.models.errors import status as errors_status
from ascend_sdk.types import BaseModel
from ascend_sdk.utils import FieldMetadata, PathParamMetadata, RequestMetadata
import pydantic
from typing import Optional, TypedDict
from typing_extensions import Annotated, NotRequired


class InvestigationServiceLinkDocumentsRequestTypedDict(TypedDict):
    investigation_id: str
    r"""The investigation id."""
    link_documents_request_create: components_linkdocumentsrequestcreate.LinkDocumentsRequestCreateTypedDict


class InvestigationServiceLinkDocumentsRequest(BaseModel):
    investigation_id: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]
    r"""The investigation id."""
    link_documents_request_create: Annotated[
        components_linkdocumentsrequestcreate.LinkDocumentsRequestCreate,
        FieldMetadata(request=RequestMetadata(media_type="application/json")),
    ]


class InvestigationServiceLinkDocumentsResponseTypedDict(TypedDict):
    http_meta: components_httpmetadata.HTTPMetadataTypedDict
    link_documents_response: NotRequired[
        components_linkdocumentsresponse.LinkDocumentsResponseTypedDict
    ]
    r"""OK"""
    status: NotRequired[errors_status.Status]
    r"""INVALID_ARGUMENT: The request is not valid, additional information may be present in the BadRequest details."""


class InvestigationServiceLinkDocumentsResponse(BaseModel):
    http_meta: Annotated[
        Optional[components_httpmetadata.HTTPMetadata], pydantic.Field(exclude=True)
    ] = None
    link_documents_response: Optional[
        components_linkdocumentsresponse.LinkDocumentsResponse
    ] = None
    r"""OK"""
    status: Optional[errors_status.Status] = None
    r"""INVALID_ARGUMENT: The request is not valid, additional information may be present in the BadRequest details."""
