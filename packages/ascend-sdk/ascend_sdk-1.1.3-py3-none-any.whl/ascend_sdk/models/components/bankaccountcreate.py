"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from enum import Enum
from typing import TypedDict


class BankAccountCreateType(str, Enum):
    r"""The bank account type."""
    TYPE_UNSPECIFIED = "TYPE_UNSPECIFIED"
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"


class BankAccountCreateTypedDict(TypedDict):
    r"""A representation of a bank account."""

    account_number: str
    r"""The bank account number. This value will be masked in responses."""
    owner: str
    r"""The name of the bank account owner."""
    routing_number: str
    r"""The bank routing number (either ABA or BIC)."""
    type: BankAccountCreateType
    r"""The bank account type."""


class BankAccountCreate(BaseModel):
    r"""A representation of a bank account."""

    account_number: str
    r"""The bank account number. This value will be masked in responses."""
    owner: str
    r"""The name of the bank account owner."""
    routing_number: str
    r"""The bank routing number (either ABA or BIC)."""
    type: BankAccountCreateType
    r"""The bank account type."""
