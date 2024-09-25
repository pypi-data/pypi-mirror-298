"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .datecreate import DateCreate, DateCreateTypedDict
from .entityeddcreate import EntityEddCreate, EntityEddCreateTypedDict
from .largetradercreate import LargeTraderCreate, LargeTraderCreateTypedDict
from .postaladdresscreate import PostalAddressCreate, PostalAddressCreateTypedDict
from .taxprofilecreate import TaxProfileCreate, TaxProfileCreateTypedDict
from ascend_sdk.types import BaseModel
from enum import Enum
from typing import List, Optional, TypedDict
from typing_extensions import NotRequired


class CorporateStructure(str, Enum):
    r"""Corporate structure of the entity."""
    ENTITY_CORPORATE_STRUCTURE_UNSPECIFIED = "ENTITY_CORPORATE_STRUCTURE_UNSPECIFIED"
    CORPORATION_C_CORP = "CORPORATION_C_CORP"
    CORPORATION_S_CORP = "CORPORATION_S_CORP"
    CORPORATION_B_CORP = "CORPORATION_B_CORP"
    CORPORATION_NONPROFIT = "CORPORATION_NONPROFIT"


class EntityType(str, Enum):
    r"""The entity type."""
    ENTITY_TYPE_UNSPECIFIED = "ENTITY_TYPE_UNSPECIFIED"
    CORPORATION = "CORPORATION"
    LIMITED_LIABILITY_COMPANY = "LIMITED_LIABILITY_COMPANY"
    PARTNERSHIP = "PARTNERSHIP"
    SOLE_PROPRIETORSHIP_OR_SINGLE_MEMBER_LLC = (
        "SOLE_PROPRIETORSHIP_OR_SINGLE_MEMBER_LLC"
    )
    TRUST = "TRUST"
    ESTATE = "ESTATE"


class ExemptCustomerReason(str, Enum):
    r"""The reason the customer is exempt from verifying beneficial owners, if applicable."""
    EXEMPT_REASON_UNSPECIFIED = "EXEMPT_REASON_UNSPECIFIED"
    REGULATED_FINANCIAL_INSTITUTION = "REGULATED_FINANCIAL_INSTITUTION"
    DEPARTMENT_OR_AGENCY_OF_FEDERAL_STATE_OR_SUBDIVISION = (
        "DEPARTMENT_OR_AGENCY_OF_FEDERAL_STATE_OR_SUBDIVISION"
    )
    NON_BANK_LISTED_ENTITY = "NON_BANK_LISTED_ENTITY"
    SECTION_12_SECURITIES_EXCHANGE_ACT_1934_OR_15_D = (
        "SECTION_12_SECURITIES_EXCHANGE_ACT_1934_OR_15D"
    )
    SECTION_3_INVESTMENT_COMPANY_ACT_1940 = "SECTION_3_INVESTMENT_COMPANY_ACT_1940"
    SECTION_202_A_INVESTMENT_ADVISORS_ACT_1940 = (
        "SECTION_202A_INVESTMENT_ADVISORS_ACT_1940"
    )
    SECTION_3_SECURITIES_EXCHANGE_ACT_1934_SECTION_6_OR_17_A = (
        "SECTION_3_SECURITIES_EXCHANGE_ACT_1934_SECTION_6_OR_17A"
    )
    ANY_OTHER_SECURITIES_EXCHANGE_ACT_1934 = "ANY_OTHER_SECURITIES_EXCHANGE_ACT_1934"
    COMMODITY_FUTURES_TRADING_COMMISSION_REGISTERED = (
        "COMMODITY_FUTURES_TRADING_COMMISSION_REGISTERED"
    )
    PUBLIC_ACCOUNTING_FIRM_SECTION_102_SARBANES_OXLEY = (
        "PUBLIC_ACCOUNTING_FIRM_SECTION_102_SARBANES_OXLEY"
    )
    STATE_REGULATED_INSURANCE_COMPANY = "STATE_REGULATED_INSURANCE_COMPANY"


class LegalEntityCreateTaxIDType(str, Enum):
    r"""The nature of the U.S. Tax ID indicated in the related tax_id field; Examples include ITIN, SSN, EIN."""
    TAX_ID_TYPE_UNSPECIFIED = "TAX_ID_TYPE_UNSPECIFIED"
    TAX_ID_TYPE_SSN = "TAX_ID_TYPE_SSN"
    TAX_ID_TYPE_ITIN = "TAX_ID_TYPE_ITIN"
    TAX_ID_TYPE_EIN = "TAX_ID_TYPE_EIN"


class LegalEntityCreateTypedDict(TypedDict):
    r"""A legal entity. Legal entities are organizations, such as companies, that participate in financial transactions"""

    correspondent_id: str
    r"""The correspondent id associated with the legal entity."""
    entity_name: str
    r"""The legal entity name."""
    entity_type: EntityType
    r"""The entity type."""
    legal_address: PostalAddressCreateTypedDict
    r"""Represents a postal address, e.g. for postal delivery or payments addresses. Given a postal address, a postal service can deliver items to a premise, P.O. Box or similar. It is not intended to model geographical locations (roads, towns, mountains).

    In typical usage an address would be created via user input or from importing existing data, depending on the type of process.

    Advice on address input / editing: - Use an i18n-ready address widget such as  https://github.com/google/libaddressinput) - Users should not be presented with UI elements for input or editing of  fields outside countries where that field is used.

    For more guidance on how to use this schema, please see: https://support.google.com/business/answer/6397478
    """
    operating_regions: List[str]
    r"""The operational footprint of an entity. Operating regions encompass all countries and regions where a company has a significant business presence This includes locations with physical offices, manufacturing plants, service centers, and sales and marketing activities Regions must be provided as two-character CLDR country codes"""
    registration_region: str
    r"""The legal home of an entity. A region of registration, in the context of a corporation, refers to the specific geographic area where the corporation is legally registered and incorporated Defines the legal jurisdiction and framework under which the corporation operates, including legal regulations, tax obligations, and compliance requirements Region must be provided as a two-character CLDR country code"""
    tax_id: str
    r"""The full U.S. tax ID for a related entity; Must be provided with `EIN` tax ID type"""
    tax_id_type: LegalEntityCreateTaxIDType
    r"""The nature of the U.S. Tax ID indicated in the related tax_id field; Examples include ITIN, SSN, EIN."""
    tax_profile: TaxProfileCreateTypedDict
    r"""Tax Profile pertaining to the Legal Entity or Natural Person."""
    accredited_investor: NotRequired[bool]
    r"""Indicates whether the entity is an accredited investor. By default, this is set to `false`."""
    adviser: NotRequired[bool]
    r"""Indicates whether the entity is an adviser. By default, this is set to `false`."""
    broker_dealer: NotRequired[bool]
    r"""Indicates whether the entity is a broker dealer. By default, this is set to `false`."""
    corporate_structure: NotRequired[CorporateStructure]
    r"""Corporate structure of the entity."""
    entity_edd: NotRequired[EntityEddCreateTypedDict]
    r"""Enhanced Due Diligence for Legal Entities required when a Legal Entity is the Primary Owner on an Account."""
    exempt_customer_reason: NotRequired[ExemptCustomerReason]
    r"""The reason the customer is exempt from verifying beneficial owners, if applicable."""
    exempt_verifying_beneficial_owners: NotRequired[bool]
    r"""Indicates whether the entity is exempt from verifying beneficial owners. By default, this is set to `false`."""
    for_the_benefit_of: NotRequired[str]
    r"""If the legal entity is a trust, they may set this field to convey ownership and value to a trustee."""
    foreign_financial_institution: NotRequired[bool]
    r"""Indicates whether the entity is a foreign financial institution. By default, this is set to `false`."""
    formation_date: NotRequired[DateCreateTypedDict]
    r"""Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar. This can represent one of the following:

    * A full date, with non-zero year, month, and day values * A month and day value, with a zero year, such as an anniversary * A year on its own, with zero month and day values * A year and month value, with a zero day, such as a credit card expiration date

    Related types are [google.type.TimeOfDay][google.type.TimeOfDay] and `google.protobuf.Timestamp`.
    """
    institutional_customer: NotRequired[bool]
    r"""Indicates whether the entity is an institutional customer"""
    large_trader: NotRequired[LargeTraderCreateTypedDict]
    r"""A large trader."""
    lei_code: NotRequired[str]
    r"""The Legal Entity Identifier (LEI) is the financial industry term for a unique global identifier for legal entities participating in financial transactions"""
    regulated_investment_company: NotRequired[bool]
    r"""Indicates whether the entity is a regulated investment company. By default, this is set to `false`."""
    related_document_ids: NotRequired[List[str]]
    r"""Document ids related to the legal entity. At least one is required for RIA correspondents when creating Estate or Trust accounts."""
    revocable_trust: NotRequired[bool]
    r"""Indicates whether the trust is a revocable trust. By default, this is set to `false`."""
    subject_to_backup_withholding: NotRequired[bool]
    r"""Boolean indicator whether the LE is subject to backup withholding"""


class LegalEntityCreate(BaseModel):
    r"""A legal entity. Legal entities are organizations, such as companies, that participate in financial transactions"""

    correspondent_id: str
    r"""The correspondent id associated with the legal entity."""
    entity_name: str
    r"""The legal entity name."""
    entity_type: EntityType
    r"""The entity type."""
    legal_address: PostalAddressCreate
    r"""Represents a postal address, e.g. for postal delivery or payments addresses. Given a postal address, a postal service can deliver items to a premise, P.O. Box or similar. It is not intended to model geographical locations (roads, towns, mountains).

    In typical usage an address would be created via user input or from importing existing data, depending on the type of process.

    Advice on address input / editing: - Use an i18n-ready address widget such as  https://github.com/google/libaddressinput) - Users should not be presented with UI elements for input or editing of  fields outside countries where that field is used.

    For more guidance on how to use this schema, please see: https://support.google.com/business/answer/6397478
    """
    operating_regions: List[str]
    r"""The operational footprint of an entity. Operating regions encompass all countries and regions where a company has a significant business presence This includes locations with physical offices, manufacturing plants, service centers, and sales and marketing activities Regions must be provided as two-character CLDR country codes"""
    registration_region: str
    r"""The legal home of an entity. A region of registration, in the context of a corporation, refers to the specific geographic area where the corporation is legally registered and incorporated Defines the legal jurisdiction and framework under which the corporation operates, including legal regulations, tax obligations, and compliance requirements Region must be provided as a two-character CLDR country code"""
    tax_id: str
    r"""The full U.S. tax ID for a related entity; Must be provided with `EIN` tax ID type"""
    tax_id_type: LegalEntityCreateTaxIDType
    r"""The nature of the U.S. Tax ID indicated in the related tax_id field; Examples include ITIN, SSN, EIN."""
    tax_profile: TaxProfileCreate
    r"""Tax Profile pertaining to the Legal Entity or Natural Person."""
    accredited_investor: Optional[bool] = None
    r"""Indicates whether the entity is an accredited investor. By default, this is set to `false`."""
    adviser: Optional[bool] = None
    r"""Indicates whether the entity is an adviser. By default, this is set to `false`."""
    broker_dealer: Optional[bool] = None
    r"""Indicates whether the entity is a broker dealer. By default, this is set to `false`."""
    corporate_structure: Optional[CorporateStructure] = None
    r"""Corporate structure of the entity."""
    entity_edd: Optional[EntityEddCreate] = None
    r"""Enhanced Due Diligence for Legal Entities required when a Legal Entity is the Primary Owner on an Account."""
    exempt_customer_reason: Optional[ExemptCustomerReason] = None
    r"""The reason the customer is exempt from verifying beneficial owners, if applicable."""
    exempt_verifying_beneficial_owners: Optional[bool] = None
    r"""Indicates whether the entity is exempt from verifying beneficial owners. By default, this is set to `false`."""
    for_the_benefit_of: Optional[str] = None
    r"""If the legal entity is a trust, they may set this field to convey ownership and value to a trustee."""
    foreign_financial_institution: Optional[bool] = None
    r"""Indicates whether the entity is a foreign financial institution. By default, this is set to `false`."""
    formation_date: Optional[DateCreate] = None
    r"""Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar. This can represent one of the following:

    * A full date, with non-zero year, month, and day values * A month and day value, with a zero year, such as an anniversary * A year on its own, with zero month and day values * A year and month value, with a zero day, such as a credit card expiration date

    Related types are [google.type.TimeOfDay][google.type.TimeOfDay] and `google.protobuf.Timestamp`.
    """
    institutional_customer: Optional[bool] = None
    r"""Indicates whether the entity is an institutional customer"""
    large_trader: Optional[LargeTraderCreate] = None
    r"""A large trader."""
    lei_code: Optional[str] = None
    r"""The Legal Entity Identifier (LEI) is the financial industry term for a unique global identifier for legal entities participating in financial transactions"""
    regulated_investment_company: Optional[bool] = None
    r"""Indicates whether the entity is a regulated investment company. By default, this is set to `false`."""
    related_document_ids: Optional[List[str]] = None
    r"""Document ids related to the legal entity. At least one is required for RIA correspondents when creating Estate or Trust accounts."""
    revocable_trust: Optional[bool] = None
    r"""Indicates whether the trust is a revocable trust. By default, this is set to `false`."""
    subject_to_backup_withholding: Optional[bool] = None
    r"""Boolean indicator whether the LE is subject to backup withholding"""
