"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .withdrawalscheduledetailsupdate import (
    WithdrawalScheduleDetailsUpdate,
    WithdrawalScheduleDetailsUpdateTypedDict,
)
from ascend_sdk.types import BaseModel
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class AchWithdrawalScheduleUpdateTypedDict(TypedDict):
    r"""A withdrawal transfer schedule using the ACH mechanism"""

    schedule_details: NotRequired[WithdrawalScheduleDetailsUpdateTypedDict]
    r"""Details of withdrawal schedule transfers"""


class AchWithdrawalScheduleUpdate(BaseModel):
    r"""A withdrawal transfer schedule using the ACH mechanism"""

    schedule_details: Optional[WithdrawalScheduleDetailsUpdate] = None
    r"""Details of withdrawal schedule transfers"""
