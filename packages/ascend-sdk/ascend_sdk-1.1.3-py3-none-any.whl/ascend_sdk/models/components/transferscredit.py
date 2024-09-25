"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import (
    BaseModel,
    Nullable,
    OptionalNullable,
    UNSET,
    UNSET_SENTINEL,
)
from datetime import datetime
from enum import Enum
from pydantic import model_serializer
from typing import Any, Dict, Optional, TypedDict
from typing_extensions import NotRequired


class TransfersCreditAmountTypedDict(TypedDict):
    r"""The amount of the credit being issued to the investor"""

    value: NotRequired[str]
    r"""The decimal value, as a string; Refer to [Google’s Decimal type protocol buffer](https://github.com/googleapis/googleapis/blob/40203ca1880849480bbff7b8715491060bbccdf1/google/type/decimal.proto#L33) for details"""


class TransfersCreditAmount(BaseModel):
    r"""The amount of the credit being issued to the investor"""

    value: Optional[str] = None
    r"""The decimal value, as a string; Refer to [Google’s Decimal type protocol buffer](https://github.com/googleapis/googleapis/blob/40203ca1880849480bbff7b8715491060bbccdf1/google/type/decimal.proto#L33) for details"""


class TransfersCreditStateState(str, Enum):
    r"""The high level state of a transfer, one of:
    - `PROCESSING` - The transfer is being processed and will be posted if successful.
    - `PENDING_REVIEW` - The transfer is pending review and will continue processing if approved.
    - `POSTED` - The transfer has been posted to the ledger and will be completed at the end of the processing window if not canceled first.
    - `COMPLETED` - The transfer has been batched and completed.
    - `REJECTED` - The transfer was rejected.
    - `CANCELED` - The transfer was canceled.
    - `RETURNED` - The transfer was returned.
    - `POSTPONED` - The transfer is postponed and will resume processing during the next processing window.
    """
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    PROCESSING = "PROCESSING"
    PENDING_REVIEW = "PENDING_REVIEW"
    POSTED = "POSTED"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    CANCELED = "CANCELED"
    RETURNED = "RETURNED"
    POSTPONED = "POSTPONED"


class TransfersCreditStateTypedDict(TypedDict):
    r"""The current state of the credit"""

    actor: NotRequired[str]
    r"""The user or service that triggered the state update."""
    message: NotRequired[str]
    r"""Additional description of the transfer state."""
    metadata: NotRequired[Nullable[Dict[str, Any]]]
    r"""Additional metadata relating to the transfer state. Included data depends on the state, e.g.:
    - Rejection reasons are included when the `state` is `REJECTED`
    - Reason and comment are included when `state` is `CANCELED`
    """
    state: NotRequired[TransfersCreditStateState]
    r"""The high level state of a transfer, one of:
    - `PROCESSING` - The transfer is being processed and will be posted if successful.
    - `PENDING_REVIEW` - The transfer is pending review and will continue processing if approved.
    - `POSTED` - The transfer has been posted to the ledger and will be completed at the end of the processing window if not canceled first.
    - `COMPLETED` - The transfer has been batched and completed.
    - `REJECTED` - The transfer was rejected.
    - `CANCELED` - The transfer was canceled.
    - `RETURNED` - The transfer was returned.
    - `POSTPONED` - The transfer is postponed and will resume processing during the next processing window.
    """
    update_time: NotRequired[Nullable[datetime]]
    r"""The time of the state update."""


class TransfersCreditState(BaseModel):
    r"""The current state of the credit"""

    actor: Optional[str] = None
    r"""The user or service that triggered the state update."""
    message: Optional[str] = None
    r"""Additional description of the transfer state."""
    metadata: OptionalNullable[Dict[str, Any]] = UNSET
    r"""Additional metadata relating to the transfer state. Included data depends on the state, e.g.:
    - Rejection reasons are included when the `state` is `REJECTED`
    - Reason and comment are included when `state` is `CANCELED`
    """
    state: Optional[TransfersCreditStateState] = None
    r"""The high level state of a transfer, one of:
    - `PROCESSING` - The transfer is being processed and will be posted if successful.
    - `PENDING_REVIEW` - The transfer is pending review and will continue processing if approved.
    - `POSTED` - The transfer has been posted to the ledger and will be completed at the end of the processing window if not canceled first.
    - `COMPLETED` - The transfer has been batched and completed.
    - `REJECTED` - The transfer was rejected.
    - `CANCELED` - The transfer was canceled.
    - `RETURNED` - The transfer was returned.
    - `POSTPONED` - The transfer is postponed and will resume processing during the next processing window.
    """
    update_time: OptionalNullable[datetime] = UNSET
    r"""The time of the state update."""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = ["actor", "message", "metadata", "state", "update_time"]
        nullable_fields = ["metadata", "update_time"]
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


class TransfersCreditType(str, Enum):
    r"""The type of the credit being issued"""
    TYPE_UNSPECIFIED = "TYPE_UNSPECIFIED"
    PROMOTIONAL = "PROMOTIONAL"
    WRITE_OFF = "WRITE_OFF"
    REIMBURSEMENT = "REIMBURSEMENT"


class TransfersCreditTypedDict(TypedDict):
    r"""A transfer using the CREDIT mechanism. Funds are moved from a firm account to a customer's brokerage account"""

    amount: NotRequired[Nullable[TransfersCreditAmountTypedDict]]
    r"""The amount of the credit being issued to the investor"""
    client_transfer_id: NotRequired[str]
    r"""External identifier supplied by the API caller. Each request must have a unique pairing of client_transfer_id and account"""
    description: NotRequired[str]
    r"""Optional description information that will attach to this transaction"""
    name: NotRequired[str]
    r"""Full name of the credit resource, which contains account id and credit transaction id"""
    state: NotRequired[Nullable[TransfersCreditStateTypedDict]]
    r"""The current state of the credit"""
    type: NotRequired[TransfersCreditType]
    r"""The type of the credit being issued"""


class TransfersCredit(BaseModel):
    r"""A transfer using the CREDIT mechanism. Funds are moved from a firm account to a customer's brokerage account"""

    amount: OptionalNullable[TransfersCreditAmount] = UNSET
    r"""The amount of the credit being issued to the investor"""
    client_transfer_id: Optional[str] = None
    r"""External identifier supplied by the API caller. Each request must have a unique pairing of client_transfer_id and account"""
    description: Optional[str] = None
    r"""Optional description information that will attach to this transaction"""
    name: Optional[str] = None
    r"""Full name of the credit resource, which contains account id and credit transaction id"""
    state: OptionalNullable[TransfersCreditState] = UNSET
    r"""The current state of the credit"""
    type: Optional[TransfersCreditType] = None
    r"""The type of the credit being issued"""

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        optional_fields = [
            "amount",
            "client_transfer_id",
            "description",
            "name",
            "state",
            "type",
        ]
        nullable_fields = ["amount", "state"]
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
