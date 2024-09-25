"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from enum import Enum
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class NonCitizenResidencyUpdateResidencyStatus(str, Enum):
    RESIDENCY_STATUS_UNSPECIFIED = "RESIDENCY_STATUS_UNSPECIFIED"
    US_PERMANENT_RESIDENT = "US_PERMANENT_RESIDENT"
    US_TEMPORARY_RESIDENT = "US_TEMPORARY_RESIDENT"
    US_NON_RESIDENT = "US_NON_RESIDENT"


class NonCitizenResidencyUpdateTypedDict(TypedDict):
    r"""Non Citizenship Residency to facilitate non-Citizen lawful US residents to open domestic accounts."""

    residency_status: NotRequired[NonCitizenResidencyUpdateResidencyStatus]


class NonCitizenResidencyUpdate(BaseModel):
    r"""Non Citizenship Residency to facilitate non-Citizen lawful US residents to open domestic accounts."""

    residency_status: Optional[NonCitizenResidencyUpdateResidencyStatus] = None
