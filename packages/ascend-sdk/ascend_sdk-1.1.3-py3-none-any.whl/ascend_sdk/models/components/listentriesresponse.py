"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .entry import Entry, EntryTypedDict
from ascend_sdk.types import BaseModel
from typing import List, Optional, TypedDict
from typing_extensions import NotRequired


class ListEntriesResponseTypedDict(TypedDict):
    r"""ListEntriesResponse"""

    entries: NotRequired[List[EntryTypedDict]]
    r"""An array of entries, empty if no results are found"""
    next_page_token: NotRequired[str]
    r"""The next page token returned by this call. Can be provided in another request to retrieve the subsequent page"""


class ListEntriesResponse(BaseModel):
    r"""ListEntriesResponse"""

    entries: Optional[List[Entry]] = None
    r"""An array of entries, empty if no results are found"""
    next_page_token: Optional[str] = None
    r"""The next page token returned by this call. Can be provided in another request to retrieve the subsequent page"""
