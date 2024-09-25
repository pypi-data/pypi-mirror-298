"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import (
    BaseModel,
    Nullable,
    OptionalNullable,
    UNSET,
    UNSET_SENTINEL,
)
from enum import Enum
from pydantic import model_serializer
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class AchDepositScheduleType(str, Enum):
    r"""The type of retirement contribution."""
    TYPE_UNSPECIFIED = "TYPE_UNSPECIFIED"
    REGULAR = "REGULAR"
    EMPLOYEE = "EMPLOYEE"
    EMPLOYER = "EMPLOYER"
    RECHARACTERIZATION = "RECHARACTERIZATION"
    ROLLOVER_60_DAY = "ROLLOVER_60_DAY"
    ROLLOVER_DIRECT = "ROLLOVER_DIRECT"
    TRANSFER = "TRANSFER"
    TRUSTEE_FEE = "TRUSTEE_FEE"
    CONVERSION = "CONVERSION"
    REPAYMENT = "REPAYMENT"


class IraContributionTypedDict(TypedDict):
    r"""The ira contribution info for an IRA account"""

    tax_year: NotRequired[int]
    r"""Tax year for which the contribution is applied. Current year is always valid; prior year is only valid before tax deadline. Must be in \"YYYY\" format."""
    type: NotRequired[AchDepositScheduleType]
    r"""The type of retirement contribution."""


class IraContribution(BaseModel):
    r"""The ira contribution info for an IRA account"""

    tax_year: Optional[int] = None
    r"""Tax year for which the contribution is applied. Current year is always valid; prior year is only valid before tax deadline. Must be in \"YYYY\" format."""
    type: Optional[AchDepositScheduleType] = None
    r"""The type of retirement contribution."""


class AchDepositScheduleAmountTypedDict(TypedDict):
    r"""A cash amount in the format of decimal value"""

    value: NotRequired[str]
    r"""The decimal value, as a string; Refer to [Google’s Decimal type protocol buffer](https://github.com/googleapis/googleapis/blob/40203ca1880849480bbff7b8715491060bbccdf1/google/type/decimal.proto#L33) for details"""


class AchDepositScheduleAmount(BaseModel):
    r"""A cash amount in the format of decimal value"""

    value: Optional[str] = None
    r"""The decimal value, as a string; Refer to [Google’s Decimal type protocol buffer](https://github.com/googleapis/googleapis/blob/40203ca1880849480bbff7b8715491060bbccdf1/google/type/decimal.proto#L33) for details"""


class StartDateTypedDict(TypedDict):
    r"""The schedule start date"""

    day: NotRequired[int]
    r"""Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant."""
    month: NotRequired[int]
    r"""Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day."""
    year: NotRequired[int]
    r"""Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year."""


class StartDate(BaseModel):
    r"""The schedule start date"""

    day: Optional[int] = None
    r"""Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant."""
    month: Optional[int] = None
    r"""Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day."""
    year: Optional[int] = None
    r"""Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year."""


class AchDepositScheduleState(str, Enum):
    r"""The state of the represented schedule"""
    ACTIVE = "ACTIVE"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"


class AchDepositScheduleTimeUnit(str, Enum):
    r"""The time unit used to calculate the interval between transfers. The time period between transfers in a scheduled series is the unit of time times the multiplier"""
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"


class SchedulePropertiesTypedDict(TypedDict):
    r"""Common schedule properties"""

    occurrences: NotRequired[int]
    r"""The number of occurrences (0 indicates unlimited occurrences)"""
    start_date: NotRequired[Nullable[StartDateTypedDict]]
    r"""The schedule start date"""
    state: NotRequired[AchDepositScheduleState]
    r"""The state of the represented schedule"""
    time_unit: NotRequired[AchDepositScheduleTimeUnit]
    r"""The time unit used to calculate the interval between transfers. The time period between transfers in a scheduled series is the unit of time times the multiplier"""
    unit_multiplier: NotRequired[int]
    r"""The multiplier used to determine the length of the interval between transfers. The time period between transfers in a scheduled series is the unit of time times the multiplier"""


class ScheduleProperties(BaseModel):
    r"""Common schedule properties"""

    occurrences: Optional[int] = None
    r"""The number of occurrences (0 indicates unlimited occurrences)"""
    start_date: OptionalNullable[StartDate] = UNSET
    r"""The schedule start date"""
    state: Optional[AchDepositScheduleState] = None
    r"""The state of the represented schedule"""
    time_unit: Optional[AchDepositScheduleTimeUnit] = None
    r"""The time unit used to calculate the interval between transfers. The time period between transfers in a scheduled series is the unit of time times the multiplier"""
    unit_multiplier: Optional[int] = None
    r"""The multiplier used to determine the length of the interval between transfers. The time period between transfers in a scheduled series is the unit of time times the multiplier"""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = [
            "occurrences",
            "start_date",
            "state",
            "time_unit",
            "unit_multiplier",
        ]
        nullable_fields = ["start_date"]
        null_default_fields = []

        serialized = handler(self)

        m = {}

        for n, f in self.model_fields.items():
            k = f.alias or n
            val = serialized.get(k)

            optional_nullable = k in optional_fields and k in nullable_fields
            is_set = (
                self.__pydantic_fields_set__.intersection({n})
                or k in null_default_fields
            )  # pylint: disable=no-member

            if val is not None and val != UNSET_SENTINEL:
                m[k] = val
            elif val != UNSET_SENTINEL and (
                not k in optional_fields or (optional_nullable and is_set)
            ):
                m[k] = val

        return m


class ScheduleDetailsTypedDict(TypedDict):
    r"""The transfer schedule details"""

    amount: NotRequired[Nullable[AchDepositScheduleAmountTypedDict]]
    r"""A cash amount in the format of decimal value"""
    client_schedule_id: NotRequired[str]
    r"""External identifier supplied by the API caller. Each request must have a unique pairing of client_schedule_id and account"""
    schedule_properties: NotRequired[Nullable[SchedulePropertiesTypedDict]]
    r"""Common schedule properties"""


class ScheduleDetails(BaseModel):
    r"""The transfer schedule details"""

    amount: OptionalNullable[AchDepositScheduleAmount] = UNSET
    r"""A cash amount in the format of decimal value"""
    client_schedule_id: Optional[str] = None
    r"""External identifier supplied by the API caller. Each request must have a unique pairing of client_schedule_id and account"""
    schedule_properties: OptionalNullable[ScheduleProperties] = UNSET
    r"""Common schedule properties"""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = ["amount", "client_schedule_id", "schedule_properties"]
        nullable_fields = ["amount", "schedule_properties"]
        null_default_fields = []

        serialized = handler(self)

        m = {}

        for n, f in self.model_fields.items():
            k = f.alias or n
            val = serialized.get(k)

            optional_nullable = k in optional_fields and k in nullable_fields
            is_set = (
                self.__pydantic_fields_set__.intersection({n})
                or k in null_default_fields
            )  # pylint: disable=no-member

            if val is not None and val != UNSET_SENTINEL:
                m[k] = val
            elif val != UNSET_SENTINEL and (
                not k in optional_fields or (optional_nullable and is_set)
            ):
                m[k] = val

        return m


class AchDepositScheduleTypedDict(TypedDict):
    r"""A deposit transfer schedule using the ACH mechanism"""

    bank_relationship: NotRequired[str]
    r"""The name of the bank relationship to be used in the ACH transaction"""
    ira_contribution: NotRequired[Nullable[IraContributionTypedDict]]
    r"""The ira contribution info for an IRA account"""
    name: NotRequired[str]
    r"""The name of the ACH Deposit transfer schedule"""
    schedule_details: NotRequired[Nullable[ScheduleDetailsTypedDict]]
    r"""The transfer schedule details"""


class AchDepositSchedule(BaseModel):
    r"""A deposit transfer schedule using the ACH mechanism"""

    bank_relationship: Optional[str] = None
    r"""The name of the bank relationship to be used in the ACH transaction"""
    ira_contribution: OptionalNullable[IraContribution] = UNSET
    r"""The ira contribution info for an IRA account"""
    name: Optional[str] = None
    r"""The name of the ACH Deposit transfer schedule"""
    schedule_details: OptionalNullable[ScheduleDetails] = UNSET
    r"""The transfer schedule details"""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = [
            "bank_relationship",
            "ira_contribution",
            "name",
            "schedule_details",
        ]
        nullable_fields = ["ira_contribution", "schedule_details"]
        null_default_fields = []

        serialized = handler(self)

        m = {}

        for n, f in self.model_fields.items():
            k = f.alias or n
            val = serialized.get(k)

            optional_nullable = k in optional_fields and k in nullable_fields
            is_set = (
                self.__pydantic_fields_set__.intersection({n})
                or k in null_default_fields
            )  # pylint: disable=no-member

            if val is not None and val != UNSET_SENTINEL:
                m[k] = val
            elif val != UNSET_SENTINEL and (
                not k in optional_fields or (optional_nullable and is_set)
            ):
                m[k] = val

        return m
