"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class NameDetailTypedDict(TypedDict):
    r"""Name detail used for Dow Jones Profile details"""

    given_name: NotRequired[str]
    r"""Dow Jones persons first name"""
    middle_names: NotRequired[str]
    r"""Dow Jones persons middle name"""
    name_suffix: NotRequired[str]
    r"""Dow Jones persons name suffix"""
    name_type: NotRequired[str]
    r"""Dow Jones persons name type"""
    surname: NotRequired[str]
    r"""Dow Jones persons last name"""
    title_honorific: NotRequired[str]
    r"""Dow Jones persons title"""


class NameDetail(BaseModel):
    r"""Name detail used for Dow Jones Profile details"""

    given_name: Optional[str] = None
    r"""Dow Jones persons first name"""
    middle_names: Optional[str] = None
    r"""Dow Jones persons middle name"""
    name_suffix: Optional[str] = None
    r"""Dow Jones persons name suffix"""
    name_type: Optional[str] = None
    r"""Dow Jones persons name type"""
    surname: Optional[str] = None
    r"""Dow Jones persons last name"""
    title_honorific: Optional[str] = None
    r"""Dow Jones persons title"""
