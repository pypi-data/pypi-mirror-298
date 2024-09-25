"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .bankaccountupdate import BankAccountUpdate, BankAccountUpdateTypedDict
from ascend_sdk.types import BaseModel
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class BankRelationshipUpdateTypedDict(TypedDict):
    r"""A relationship between a bank account and an Apex account."""

    bank_account: NotRequired[BankAccountUpdateTypedDict]
    r"""A representation of a bank account."""
    nickname: NotRequired[str]
    r"""The nickname of the bank relationship."""
    plaid_processor_token: NotRequired[str]
    r"""A processor token from Plaid (vendor). Required if using `PLAID_TOKEN` verification method."""


class BankRelationshipUpdate(BaseModel):
    r"""A relationship between a bank account and an Apex account."""

    bank_account: Optional[BankAccountUpdate] = None
    r"""A representation of a bank account."""
    nickname: Optional[str] = None
    r"""The nickname of the bank relationship."""
    plaid_processor_token: Optional[str] = None
    r"""A processor token from Plaid (vendor). Required if using `PLAID_TOKEN` verification method."""
