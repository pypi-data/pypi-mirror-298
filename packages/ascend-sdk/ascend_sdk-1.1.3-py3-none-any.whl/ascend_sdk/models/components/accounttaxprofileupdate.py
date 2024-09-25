"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from enum import Enum
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class AccountTaxProfileUpdateCostBasisLotDisposalMethod(str, Enum):
    r"""A method of determining the cost basis of an asset that has been sold or disposed of, by identifying which specific lot of the asset was sold and using the cost of that lot to calculate the cost basis; this method is commonly used for tax purposes to determine the amount of reportable capital gains or losses By default, this is set to `COST_BASIS_LOT_DISPOSAL_FIFO`"""
    COST_BASIS_LOT_DISPOSAL_METHOD_UNSPECIFIED = (
        "COST_BASIS_LOT_DISPOSAL_METHOD_UNSPECIFIED"
    )
    COST_BASIS_LOT_DISPOSAL_FIFO = "COST_BASIS_LOT_DISPOSAL_FIFO"
    COST_BASIS_LOT_DISPOSAL_LIFO = "COST_BASIS_LOT_DISPOSAL_LIFO"


class AccountTaxProfileUpdateTypedDict(TypedDict):
    r"""The account tax profile."""

    cost_basis_lot_disposal_method: NotRequired[
        AccountTaxProfileUpdateCostBasisLotDisposalMethod
    ]
    r"""A method of determining the cost basis of an asset that has been sold or disposed of, by identifying which specific lot of the asset was sold and using the cost of that lot to calculate the cost basis; this method is commonly used for tax purposes to determine the amount of reportable capital gains or losses By default, this is set to `COST_BASIS_LOT_DISPOSAL_FIFO`"""
    section_475_election: NotRequired[bool]
    r"""Indicates if the account is eligible to mark-to-market their securities and commodities holdings; Named after the related section of the IRS tax code"""


class AccountTaxProfileUpdate(BaseModel):
    r"""The account tax profile."""

    cost_basis_lot_disposal_method: Optional[
        AccountTaxProfileUpdateCostBasisLotDisposalMethod
    ] = None
    r"""A method of determining the cost basis of an asset that has been sold or disposed of, by identifying which specific lot of the asset was sold and using the cost of that lot to calculate the cost basis; this method is commonly used for tax purposes to determine the amount of reportable capital gains or losses By default, this is set to `COST_BASIS_LOT_DISPOSAL_FIFO`"""
    section_475_election: Optional[bool] = None
    r"""Indicates if the account is eligible to mark-to-market their securities and commodities holdings; Named after the related section of the IRS tax code"""
