"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .dateupdate import DateUpdate, DateUpdateTypedDict
from .employmentupdate import EmploymentUpdate, EmploymentUpdateTypedDict
from .foreignidentificationupdate import (
    ForeignIdentificationUpdate,
    ForeignIdentificationUpdateTypedDict,
)
from .identityverificationresultupdate import (
    IdentityVerificationResultUpdate,
    IdentityVerificationResultUpdateTypedDict,
)
from .largetraderupdate import LargeTraderUpdate, LargeTraderUpdateTypedDict
from .naturalpersonfddupdate import (
    NaturalPersonFddUpdate,
    NaturalPersonFddUpdateTypedDict,
)
from .noncitizenresidencyupdate import (
    NonCitizenResidencyUpdate,
    NonCitizenResidencyUpdateTypedDict,
)
from .postaladdressupdate import PostalAddressUpdate, PostalAddressUpdateTypedDict
from .taxprofileupdate import TaxProfileUpdate, TaxProfileUpdateTypedDict
from ascend_sdk.types import BaseModel
from enum import Enum
from typing import List, Optional, TypedDict
from typing_extensions import NotRequired


class LegalNaturalPersonUpdateMaritalStatus(str, Enum):
    r"""The legal marital status of an account-holder; Used in combination with state of domicile to determine qualification for account types and beneficiary exclusion rules."""
    MARITAL_STATUS_UNSPECIFIED = "MARITAL_STATUS_UNSPECIFIED"
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    DIVORCED = "DIVORCED"
    WIDOWED = "WIDOWED"


class LegalNaturalPersonUpdateNameSuffix(str, Enum):
    r"""The suffix of a natural person; A suffix in a name is any part of the name that comes after the last name"""
    NAME_SUFFIX_UNSPECIFIED = "NAME_SUFFIX_UNSPECIFIED"
    SR = "SR"
    JR = "JR"
    III = "III"
    IV = "IV"
    V = "V"


class LegalNaturalPersonUpdateTaxIDType(str, Enum):
    r"""The nature of the U.S. Tax ID indicated in the related tax_id field; Examples include ITIN, SSN, EIN."""
    TAX_ID_TYPE_UNSPECIFIED = "TAX_ID_TYPE_UNSPECIFIED"
    TAX_ID_TYPE_SSN = "TAX_ID_TYPE_SSN"
    TAX_ID_TYPE_ITIN = "TAX_ID_TYPE_ITIN"
    TAX_ID_TYPE_EIN = "TAX_ID_TYPE_EIN"


class LegalNaturalPersonUpdateTypedDict(TypedDict):
    r"""A legal natural person. This represents the full set of data for an individual. A Customer Identification Program (CIP) may be run on legal natural persons."""

    accredited_investor: NotRequired[bool]
    r"""Indicates whether the person is an accredited investor"""
    adviser: NotRequired[bool]
    r"""Indicates whether the person is an adviser"""
    birth_date: NotRequired[DateUpdateTypedDict]
    r"""Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar. This can represent one of the following:

    * A full date, with non-zero year, month, and day values * A month and day value, with a zero year, such as an anniversary * A year on its own, with zero month and day values * A year and month value, with a zero day, such as a credit card expiration date

    Related types are [google.type.TimeOfDay][google.type.TimeOfDay] and `google.protobuf.Timestamp`.
    """
    citizenship_countries: NotRequired[List[str]]
    r"""This is used for tax (treaty) and country block list considerations Maximum list of two 2-char CLDR Code citizenship countries, e.g. US, CA"""
    control_person_company_symbols: NotRequired[str]
    r"""A list of ticker symbols in which the underlying person is a control person; control persons are defined as having significant influence over a company’s management and operations, typically through ownership of a large percentage of the company’s voting stock or through positions on the company’s board of directors or executive team"""
    correspondent_employee: NotRequired[bool]
    r"""Indicates the related owner record is an employee of the clearing broker's correspondent customer."""
    correspondent_id: NotRequired[str]
    r"""A unique identifier referencing a Correspondent; A Client may have several operating Correspondents within its purview."""
    death_date: NotRequired[DateUpdateTypedDict]
    r"""Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar. This can represent one of the following:

    * A full date, with non-zero year, month, and day values * A month and day value, with a zero year, such as an anniversary * A year on its own, with zero month and day values * A year and month value, with a zero day, such as a credit card expiration date

    Related types are [google.type.TimeOfDay][google.type.TimeOfDay] and `google.protobuf.Timestamp`.
    """
    employment: NotRequired[EmploymentUpdateTypedDict]
    r"""Object containing information pertaining to a investor's current employer including the name, address, and duration of employment."""
    family_name: NotRequired[str]
    r"""Family name of a natural person."""
    finra_associated_entity: NotRequired[str]
    r"""The name of the FINRA-associated entity the underlying natural person is affiliated with."""
    foreign_identification: NotRequired[ForeignIdentificationUpdateTypedDict]
    r"""Foreign identification"""
    given_name: NotRequired[str]
    r"""The given name of a natural person; Conventionally known as 'first name' in most English-speaking countries."""
    identity_verification_result: NotRequired[IdentityVerificationResultUpdateTypedDict]
    r"""An identity verification result that clients may supply. This result represents data and confirmation attesting to identity verification."""
    institutional_customer: NotRequired[bool]
    r"""Indicates whether the person is an institutional customer"""
    large_trader: NotRequired[LargeTraderUpdateTypedDict]
    r"""A large trader."""
    marital_status: NotRequired[LegalNaturalPersonUpdateMaritalStatus]
    r"""The legal marital status of an account-holder; Used in combination with state of domicile to determine qualification for account types and beneficiary exclusion rules."""
    middle_names: NotRequired[str]
    r"""Non-primary names representing a natural person; Name attributed to a person other than \"Given\" and \"Family\" names."""
    name_suffix: NotRequired[LegalNaturalPersonUpdateNameSuffix]
    r"""The suffix of a natural person; A suffix in a name is any part of the name that comes after the last name"""
    natural_person_fdd: NotRequired[NaturalPersonFddUpdateTypedDict]
    r"""Foreign Due Diligence for Legal Natural Persons required when a Legal Natural Person is the Primary Owner on a non-resident/non-citizen Account."""
    non_citizen_residency: NotRequired[NonCitizenResidencyUpdateTypedDict]
    r"""Non Citizenship Residency to facilitate non-Citizen lawful US residents to open domestic accounts."""
    personal_address: NotRequired[PostalAddressUpdateTypedDict]
    r"""Represents a postal address, e.g. for postal delivery or payments addresses. Given a postal address, a postal service can deliver items to a premise, P.O. Box or similar. It is not intended to model geographical locations (roads, towns, mountains).

    In typical usage an address would be created via user input or from importing existing data, depending on the type of process.

    Advice on address input / editing: - Use an i18n-ready address widget such as  https://github.com/google/libaddressinput) - Users should not be presented with UI elements for input or editing of  fields outside countries where that field is used.

    For more guidance on how to use this schema, please see: https://support.google.com/business/answer/6397478
    """
    politically_exposed_immediate_family_names: NotRequired[List[str]]
    r"""A Party's self-disclosed list of names representing family members who are politically exposed."""
    politically_exposed_organization: NotRequired[str]
    r"""A Party's self-disclosed list of named politically exposed organizations they are personally associated with."""
    subject_to_backup_withholding: NotRequired[bool]
    r"""Boolean indicator whether the LNP is subject to backup withholding"""
    tax_id: NotRequired[str]
    r"""The full U.S. tax ID for a related person; Must be provided with `ITIN` or `SSN` tax ID type"""
    tax_id_type: NotRequired[LegalNaturalPersonUpdateTaxIDType]
    r"""The nature of the U.S. Tax ID indicated in the related tax_id field; Examples include ITIN, SSN, EIN."""
    tax_profile: NotRequired[TaxProfileUpdateTypedDict]
    r"""Tax Profile pertaining to the Legal Entity or Natural Person."""


class LegalNaturalPersonUpdate(BaseModel):
    r"""A legal natural person. This represents the full set of data for an individual. A Customer Identification Program (CIP) may be run on legal natural persons."""

    accredited_investor: Optional[bool] = None
    r"""Indicates whether the person is an accredited investor"""
    adviser: Optional[bool] = None
    r"""Indicates whether the person is an adviser"""
    birth_date: Optional[DateUpdate] = None
    r"""Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar. This can represent one of the following:

    * A full date, with non-zero year, month, and day values * A month and day value, with a zero year, such as an anniversary * A year on its own, with zero month and day values * A year and month value, with a zero day, such as a credit card expiration date

    Related types are [google.type.TimeOfDay][google.type.TimeOfDay] and `google.protobuf.Timestamp`.
    """
    citizenship_countries: Optional[List[str]] = None
    r"""This is used for tax (treaty) and country block list considerations Maximum list of two 2-char CLDR Code citizenship countries, e.g. US, CA"""
    control_person_company_symbols: Optional[str] = None
    r"""A list of ticker symbols in which the underlying person is a control person; control persons are defined as having significant influence over a company’s management and operations, typically through ownership of a large percentage of the company’s voting stock or through positions on the company’s board of directors or executive team"""
    correspondent_employee: Optional[bool] = None
    r"""Indicates the related owner record is an employee of the clearing broker's correspondent customer."""
    correspondent_id: Optional[str] = None
    r"""A unique identifier referencing a Correspondent; A Client may have several operating Correspondents within its purview."""
    death_date: Optional[DateUpdate] = None
    r"""Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar. This can represent one of the following:

    * A full date, with non-zero year, month, and day values * A month and day value, with a zero year, such as an anniversary * A year on its own, with zero month and day values * A year and month value, with a zero day, such as a credit card expiration date

    Related types are [google.type.TimeOfDay][google.type.TimeOfDay] and `google.protobuf.Timestamp`.
    """
    employment: Optional[EmploymentUpdate] = None
    r"""Object containing information pertaining to a investor's current employer including the name, address, and duration of employment."""
    family_name: Optional[str] = None
    r"""Family name of a natural person."""
    finra_associated_entity: Optional[str] = None
    r"""The name of the FINRA-associated entity the underlying natural person is affiliated with."""
    foreign_identification: Optional[ForeignIdentificationUpdate] = None
    r"""Foreign identification"""
    given_name: Optional[str] = None
    r"""The given name of a natural person; Conventionally known as 'first name' in most English-speaking countries."""
    identity_verification_result: Optional[IdentityVerificationResultUpdate] = None
    r"""An identity verification result that clients may supply. This result represents data and confirmation attesting to identity verification."""
    institutional_customer: Optional[bool] = None
    r"""Indicates whether the person is an institutional customer"""
    large_trader: Optional[LargeTraderUpdate] = None
    r"""A large trader."""
    marital_status: Optional[LegalNaturalPersonUpdateMaritalStatus] = None
    r"""The legal marital status of an account-holder; Used in combination with state of domicile to determine qualification for account types and beneficiary exclusion rules."""
    middle_names: Optional[str] = None
    r"""Non-primary names representing a natural person; Name attributed to a person other than \"Given\" and \"Family\" names."""
    name_suffix: Optional[LegalNaturalPersonUpdateNameSuffix] = None
    r"""The suffix of a natural person; A suffix in a name is any part of the name that comes after the last name"""
    natural_person_fdd: Optional[NaturalPersonFddUpdate] = None
    r"""Foreign Due Diligence for Legal Natural Persons required when a Legal Natural Person is the Primary Owner on a non-resident/non-citizen Account."""
    non_citizen_residency: Optional[NonCitizenResidencyUpdate] = None
    r"""Non Citizenship Residency to facilitate non-Citizen lawful US residents to open domestic accounts."""
    personal_address: Optional[PostalAddressUpdate] = None
    r"""Represents a postal address, e.g. for postal delivery or payments addresses. Given a postal address, a postal service can deliver items to a premise, P.O. Box or similar. It is not intended to model geographical locations (roads, towns, mountains).

    In typical usage an address would be created via user input or from importing existing data, depending on the type of process.

    Advice on address input / editing: - Use an i18n-ready address widget such as  https://github.com/google/libaddressinput) - Users should not be presented with UI elements for input or editing of  fields outside countries where that field is used.

    For more guidance on how to use this schema, please see: https://support.google.com/business/answer/6397478
    """
    politically_exposed_immediate_family_names: Optional[List[str]] = None
    r"""A Party's self-disclosed list of names representing family members who are politically exposed."""
    politically_exposed_organization: Optional[str] = None
    r"""A Party's self-disclosed list of named politically exposed organizations they are personally associated with."""
    subject_to_backup_withholding: Optional[bool] = None
    r"""Boolean indicator whether the LNP is subject to backup withholding"""
    tax_id: Optional[str] = None
    r"""The full U.S. tax ID for a related person; Must be provided with `ITIN` or `SSN` tax ID type"""
    tax_id_type: Optional[LegalNaturalPersonUpdateTaxIDType] = None
    r"""The nature of the U.S. Tax ID indicated in the related tax_id field; Examples include ITIN, SSN, EIN."""
    tax_profile: Optional[TaxProfileUpdate] = None
    r"""Tax Profile pertaining to the Legal Entity or Natural Person."""
