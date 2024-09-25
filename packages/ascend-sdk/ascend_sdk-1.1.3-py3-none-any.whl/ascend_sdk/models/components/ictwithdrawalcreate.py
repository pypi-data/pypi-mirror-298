"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .decimalcreate import DecimalCreate, DecimalCreateTypedDict
from .ictwithdrawal_travelrulecreate import (
    IctWithdrawalTravelRuleCreate,
    IctWithdrawalTravelRuleCreateTypedDict,
)
from .retirementdistributioncreate import (
    RetirementDistributionCreate,
    RetirementDistributionCreateTypedDict,
)
from ascend_sdk.types import BaseModel
from enum import Enum
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class IctWithdrawalCreateProgram(str, Enum):
    r"""The name of the program that the ICT withdrawal is associated with."""
    ICT_PROGRAM_UNSPECIFIED = "ICT_PROGRAM_UNSPECIFIED"
    BROKER_PARTNER = "BROKER_PARTNER"
    DEPOSIT_ONLY = "DEPOSIT_ONLY"


class IctWithdrawalCreateTypedDict(TypedDict):
    r"""An Instant Cash Transfer. Funds are moved from a customer's brokerage account to a configured Firm account."""

    client_transfer_id: str
    r"""External identifier supplied by the API caller. Each request must have a unique pairing of client_transfer_id and account."""
    program: IctWithdrawalCreateProgram
    r"""The name of the program that the ICT withdrawal is associated with."""
    travel_rule: IctWithdrawalTravelRuleCreateTypedDict
    r"""The travel rules associated with an ICT withdrawal"""
    amount: NotRequired[DecimalCreateTypedDict]
    r"""A representation of a decimal value, such as 2.5. Clients may convert values into language-native decimal formats, such as Java's [BigDecimal][] or Python's [decimal.Decimal][].

    [BigDecimal]:
    https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/math/BigDecimal.html
    [decimal.Decimal]: https://docs.python.org/3/library/decimal.html
    """
    full_disbursement: NotRequired[bool]
    r"""Whether the entire account balance is being withdrawn. This field should either be set to true or left unset if the amount field is provided."""
    retirement_distribution: NotRequired[RetirementDistributionCreateTypedDict]
    r"""A distribution from a retirement account."""


class IctWithdrawalCreate(BaseModel):
    r"""An Instant Cash Transfer. Funds are moved from a customer's brokerage account to a configured Firm account."""

    client_transfer_id: str
    r"""External identifier supplied by the API caller. Each request must have a unique pairing of client_transfer_id and account."""
    program: IctWithdrawalCreateProgram
    r"""The name of the program that the ICT withdrawal is associated with."""
    travel_rule: IctWithdrawalTravelRuleCreate
    r"""The travel rules associated with an ICT withdrawal"""
    amount: Optional[DecimalCreate] = None
    r"""A representation of a decimal value, such as 2.5. Clients may convert values into language-native decimal formats, such as Java's [BigDecimal][] or Python's [decimal.Decimal][].

    [BigDecimal]:
    https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/math/BigDecimal.html
    [decimal.Decimal]: https://docs.python.org/3/library/decimal.html
    """
    full_disbursement: Optional[bool] = None
    r"""Whether the entire account balance is being withdrawn. This field should either be set to true or left unset if the amount field is provided."""
    retirement_distribution: Optional[RetirementDistributionCreate] = None
    r"""A distribution from a retirement account."""
