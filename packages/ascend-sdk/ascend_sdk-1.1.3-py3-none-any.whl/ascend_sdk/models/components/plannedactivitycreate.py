"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from enum import Enum
from typing import List, TypedDict


class PrimaryAccountActivityType(str, Enum):
    r"""The primary account activity type"""
    PRIMARY_ACCOUNT_ACTIVITY_TYPE_UNSPECIFIED = (
        "PRIMARY_ACCOUNT_ACTIVITY_TYPE_UNSPECIFIED"
    )
    ACTIVE_TRADING = "ACTIVE_TRADING"
    SHORT_TERM_INVESTING = "SHORT_TERM_INVESTING"
    LONG_TERM_INVESTING = "LONG_TERM_INVESTING"


class WithdrawalFrequency(str, Enum):
    r"""The frequency by which cash is anticipated to be withdrawn from the account"""
    WITHDRAWAL_FREQUENCY_UNSPECIFIED = "WITHDRAWAL_FREQUENCY_UNSPECIFIED"
    FREQUENT = "FREQUENT"
    OCCASIONAL = "OCCASIONAL"
    RARE = "RARE"


class PlannedActivityCreateTypedDict(TypedDict):
    r"""Details the customer's intended trading and banking-related activities at the time of account application; informs risk checks and forms a baseline for anomalous activity detection"""

    foreign_bond_trading_countries: List[str]
    r"""The foreign bond trading countries"""
    low_priced_securities: bool
    r"""The account anticipates trading in securities trading for less than $5 per share and are typically traded over-the-counter (OTC) or through pink sheets"""
    low_priced_securities_pct: int
    r"""The percentage, by volume, of the account's trades which will involve low priced securities"""
    primary_account_activity_type: PrimaryAccountActivityType
    r"""The primary account activity type"""
    withdrawal_frequency: WithdrawalFrequency
    r"""The frequency by which cash is anticipated to be withdrawn from the account"""


class PlannedActivityCreate(BaseModel):
    r"""Details the customer's intended trading and banking-related activities at the time of account application; informs risk checks and forms a baseline for anomalous activity detection"""

    foreign_bond_trading_countries: List[str]
    r"""The foreign bond trading countries"""
    low_priced_securities: bool
    r"""The account anticipates trading in securities trading for less than $5 per share and are typically traded over-the-counter (OTC) or through pink sheets"""
    low_priced_securities_pct: int
    r"""The percentage, by volume, of the account's trades which will involve low priced securities"""
    primary_account_activity_type: PrimaryAccountActivityType
    r"""The primary account activity type"""
    withdrawal_frequency: WithdrawalFrequency
    r"""The frequency by which cash is anticipated to be withdrawn from the account"""
