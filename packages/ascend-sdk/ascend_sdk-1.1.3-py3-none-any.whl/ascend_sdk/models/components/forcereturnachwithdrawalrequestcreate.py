"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .nachareturncreate import NachaReturnCreate, NachaReturnCreateTypedDict
from ascend_sdk.types import BaseModel
from typing import TypedDict


class ForceReturnAchWithdrawalRequestCreateTypedDict(TypedDict):
    r"""Request to force a Nacha return on a completed ACH withdrawal. FOR TESTING ONLY!"""

    nacha_return: NachaReturnCreateTypedDict
    r"""A return on an ACH transfer from the Nacha network."""
    name: str
    r"""The name of the ACH withdrawal to force a Nacha return on."""


class ForceReturnAchWithdrawalRequestCreate(BaseModel):
    r"""Request to force a Nacha return on a completed ACH withdrawal. FOR TESTING ONLY!"""

    nacha_return: NachaReturnCreate
    r"""A return on an ACH transfer from the Nacha network."""
    name: str
    r"""The name of the ACH withdrawal to force a Nacha return on."""
