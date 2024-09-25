"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class IdentificationDetailTypedDict(TypedDict):
    r"""Identification details used for Dow Jones Profile details"""

    id_notes: NotRequired[str]
    r"""Notes relating to identification"""
    id_type: NotRequired[str]
    r"""Identification type"""
    id_value: NotRequired[str]
    r"""Identification value"""


class IdentificationDetail(BaseModel):
    r"""Identification details used for Dow Jones Profile details"""

    id_notes: Optional[str] = None
    r"""Notes relating to identification"""
    id_type: Optional[str] = None
    r"""Identification type"""
    id_value: Optional[str] = None
    r"""Identification value"""
