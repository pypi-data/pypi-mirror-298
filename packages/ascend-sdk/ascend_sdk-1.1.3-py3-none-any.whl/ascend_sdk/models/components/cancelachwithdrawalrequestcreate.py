"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class CancelAchWithdrawalRequestCreateTypedDict(TypedDict):
    r"""Request to cancel an existing ACH withdrawal."""

    name: str
    r"""The name of the ACH withdrawal to cancel."""
    reason: NotRequired[str]
    r"""The reason why the ACH withdrawal is being canceled."""


class CancelAchWithdrawalRequestCreate(BaseModel):
    r"""Request to cancel an existing ACH withdrawal."""

    name: str
    r"""The name of the ACH withdrawal to cancel."""
    reason: Optional[str] = None
    r"""The reason why the ACH withdrawal is being canceled."""
