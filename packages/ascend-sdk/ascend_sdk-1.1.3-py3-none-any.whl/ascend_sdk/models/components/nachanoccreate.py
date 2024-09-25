"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from enum import Enum
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class Code(str, Enum):
    r"""The notice of change reason code."""
    CODE_UNSPECIFIED = "CODE_UNSPECIFIED"
    C01 = "C01"
    C02 = "C02"
    C03 = "C03"
    C04 = "C04"
    C05 = "C05"
    C06 = "C06"
    C07 = "C07"
    C08 = "C08"
    C09 = "C09"
    C13 = "C13"
    C14 = "C14"
    C61 = "C61"
    C62 = "C62"
    C63 = "C63"
    C64 = "C64"
    C65 = "C65"
    C66 = "C66"
    C67 = "C67"
    C68 = "C68"
    C69 = "C69"


class UpdatedBankAccountType(str, Enum):
    r"""The updated bank account type. Should only be set when the code is for an incorrect transaction code."""
    TYPE_UNSPECIFIED = "TYPE_UNSPECIFIED"
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"


class NachaNocCreateTypedDict(TypedDict):
    r"""A notice of change (NOC) on an ACH transfer from the Nacha network."""

    code: Code
    r"""The notice of change reason code."""
    updated_bank_account_number: NotRequired[str]
    r"""The updated bank account number. Should only be set when the code is for an incorrect DFI account number."""
    updated_bank_account_type: NotRequired[UpdatedBankAccountType]
    r"""The updated bank account type. Should only be set when the code is for an incorrect transaction code."""
    updated_bank_routing_number: NotRequired[str]
    r"""The updated bank routing number. Should only be set when the code is for an incorrect routing number."""


class NachaNocCreate(BaseModel):
    r"""A notice of change (NOC) on an ACH transfer from the Nacha network."""

    code: Code
    r"""The notice of change reason code."""
    updated_bank_account_number: Optional[str] = None
    r"""The updated bank account number. Should only be set when the code is for an incorrect DFI account number."""
    updated_bank_account_type: Optional[UpdatedBankAccountType] = None
    r"""The updated bank account type. Should only be set when the code is for an incorrect transaction code."""
    updated_bank_routing_number: Optional[str] = None
    r"""The updated bank routing number. Should only be set when the code is for an incorrect routing number."""
