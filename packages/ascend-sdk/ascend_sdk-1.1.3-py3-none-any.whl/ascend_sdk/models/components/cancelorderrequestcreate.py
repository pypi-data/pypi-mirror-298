"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from typing import TypedDict


class CancelOrderRequestCreateTypedDict(TypedDict):
    r"""The message to request cancellation of an existing order"""

    name: str
    r"""Format: accounts/{account_id}/orders/{order_id}"""


class CancelOrderRequestCreate(BaseModel):
    r"""The message to request cancellation of an existing order"""

    name: str
    r"""Format: accounts/{account_id}/orders/{order_id}"""
