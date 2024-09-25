"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .uploadlink import UploadLink, UploadLinkTypedDict
from ascend_sdk.types import BaseModel
from typing import List, Optional, TypedDict
from typing_extensions import NotRequired


class BatchCreateUploadLinksResponseTypedDict(TypedDict):
    r"""List of signed links to upload documents."""

    upload_link: NotRequired[List[UploadLinkTypedDict]]
    r"""The list of signed links used to upload documents"""


class BatchCreateUploadLinksResponse(BaseModel):
    r"""List of signed links to upload documents."""

    upload_link: Optional[List[UploadLink]] = None
    r"""The list of signed links used to upload documents"""
