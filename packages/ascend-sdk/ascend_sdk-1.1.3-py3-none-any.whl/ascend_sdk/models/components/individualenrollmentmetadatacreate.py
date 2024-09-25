"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from enum import Enum
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class IndividualEnrollmentMetadataCreateDividendReinvestmentPlan(str, Enum):
    r"""Option to auto-enroll in Dividend Reinvestment; defaults to true"""
    AUTO_ENROLL_DIVIDEND_REINVESTMENT_UNSPECIFIED = (
        "AUTO_ENROLL_DIVIDEND_REINVESTMENT_UNSPECIFIED"
    )
    DIVIDEND_REINVESTMENT_ENROLL = "DIVIDEND_REINVESTMENT_ENROLL"
    DIVIDEND_REINVESTMENT_DECLINE = "DIVIDEND_REINVESTMENT_DECLINE"


class IndividualEnrollmentMetadataCreateFdicCashSweep(str, Enum):
    r"""Option to auto-enroll in FDIC cash sweep; defaults to true"""
    AUTO_ENROLL_FDIC_CASH_SWEEP_UNSPECIFIED = "AUTO_ENROLL_FDIC_CASH_SWEEP_UNSPECIFIED"
    FDIC_CASH_SWEEP_ENROLL = "FDIC_CASH_SWEEP_ENROLL"
    FDIC_CASH_SWEEP_DECLINE = "FDIC_CASH_SWEEP_DECLINE"


class IndividualEnrollmentMetadataCreateTypedDict(TypedDict):
    r"""Enrollment metadata for Individual accounts enrollment type"""

    dividend_reinvestment_plan: NotRequired[
        IndividualEnrollmentMetadataCreateDividendReinvestmentPlan
    ]
    r"""Option to auto-enroll in Dividend Reinvestment; defaults to true"""
    fdic_cash_sweep: NotRequired[IndividualEnrollmentMetadataCreateFdicCashSweep]
    r"""Option to auto-enroll in FDIC cash sweep; defaults to true"""


class IndividualEnrollmentMetadataCreate(BaseModel):
    r"""Enrollment metadata for Individual accounts enrollment type"""

    dividend_reinvestment_plan: Optional[
        IndividualEnrollmentMetadataCreateDividendReinvestmentPlan
    ] = None
    r"""Option to auto-enroll in Dividend Reinvestment; defaults to true"""
    fdic_cash_sweep: Optional[IndividualEnrollmentMetadataCreateFdicCashSweep] = None
    r"""Option to auto-enroll in FDIC cash sweep; defaults to true"""
