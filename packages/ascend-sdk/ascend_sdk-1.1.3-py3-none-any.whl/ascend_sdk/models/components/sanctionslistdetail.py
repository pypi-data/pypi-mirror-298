"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class SanctionsListDetailTypedDict(TypedDict):
    r"""Sanctions list detail used for Dow Jones Profile details"""

    end_day: NotRequired[str]
    r"""Dow Jones day persons will be taken off sanctions list"""
    end_month: NotRequired[str]
    r"""Dow Jones month persons will be taken off sanctions list"""
    end_year: NotRequired[str]
    r"""Dow Jones year persons will be taken off sanctions list"""
    sanctions_reference_description: NotRequired[str]
    r"""Dow Jones persons sanctions ref id"""
    start_day: NotRequired[str]
    r"""Dow Jones day persons were added to the sanctions list"""
    start_month: NotRequired[str]
    r"""Dow Jones month persons were added to the sanctions list"""
    start_year: NotRequired[str]
    r"""Dow Jones year persons were added to the sanctions list"""


class SanctionsListDetail(BaseModel):
    r"""Sanctions list detail used for Dow Jones Profile details"""

    end_day: Optional[str] = None
    r"""Dow Jones day persons will be taken off sanctions list"""
    end_month: Optional[str] = None
    r"""Dow Jones month persons will be taken off sanctions list"""
    end_year: Optional[str] = None
    r"""Dow Jones year persons will be taken off sanctions list"""
    sanctions_reference_description: Optional[str] = None
    r"""Dow Jones persons sanctions ref id"""
    start_day: Optional[str] = None
    r"""Dow Jones day persons were added to the sanctions list"""
    start_month: Optional[str] = None
    r"""Dow Jones month persons were added to the sanctions list"""
    start_year: Optional[str] = None
    r"""Dow Jones year persons were added to the sanctions list"""
