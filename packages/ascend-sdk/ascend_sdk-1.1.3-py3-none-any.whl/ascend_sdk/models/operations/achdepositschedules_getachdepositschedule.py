"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.models.components import (
    achdepositschedule as components_achdepositschedule,
    httpmetadata as components_httpmetadata,
)
from ascend_sdk.models.errors import status as errors_status
from ascend_sdk.types import BaseModel
from ascend_sdk.utils import FieldMetadata, PathParamMetadata
import pydantic
from typing import Optional, TypedDict
from typing_extensions import Annotated, NotRequired


class AchDepositSchedulesGetAchDepositScheduleRequestTypedDict(TypedDict):
    account_id: str
    r"""The account id."""
    ach_deposit_schedule_id: str
    r"""The achDepositSchedule id."""


class AchDepositSchedulesGetAchDepositScheduleRequest(BaseModel):
    account_id: Annotated[
        str, FieldMetadata(path=PathParamMetadata(style="simple", explode=False))
    ]
    r"""The account id."""
    ach_deposit_schedule_id: Annotated[
        str,
        pydantic.Field(alias="achDepositSchedule_id"),
        FieldMetadata(path=PathParamMetadata(style="simple", explode=False)),
    ]
    r"""The achDepositSchedule id."""


class AchDepositSchedulesGetAchDepositScheduleResponseTypedDict(TypedDict):
    http_meta: components_httpmetadata.HTTPMetadataTypedDict
    ach_deposit_schedule: NotRequired[
        components_achdepositschedule.AchDepositScheduleTypedDict
    ]
    r"""OK"""
    status: NotRequired[errors_status.Status]
    r"""INVALID_ARGUMENT: The request has an invalid argument."""


class AchDepositSchedulesGetAchDepositScheduleResponse(BaseModel):
    http_meta: Annotated[
        Optional[components_httpmetadata.HTTPMetadata], pydantic.Field(exclude=True)
    ] = None
    ach_deposit_schedule: Optional[
        components_achdepositschedule.AchDepositSchedule
    ] = None
    r"""OK"""
    status: Optional[errors_status.Status] = None
    r"""INVALID_ARGUMENT: The request has an invalid argument."""
