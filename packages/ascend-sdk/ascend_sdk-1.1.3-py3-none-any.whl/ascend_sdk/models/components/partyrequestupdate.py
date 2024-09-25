"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from .phonenumberupdate import PhoneNumberUpdate, PhoneNumberUpdateTypedDict
from .postaladdressupdate import PostalAddressUpdate, PostalAddressUpdateTypedDict
from ascend_sdk.types import BaseModel
from enum import Enum
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class PartyRequestUpdateProspectusDeliveryPreference(str, Enum):
    r"""Delivery method instruction for prospectuses for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""
    DELIVERY_PREFERENCE_UNSPECIFIED = "DELIVERY_PREFERENCE_UNSPECIFIED"
    DIGITAL = "DIGITAL"
    PHYSICAL = "PHYSICAL"
    SUPPRESS = "SUPPRESS"


class PartyRequestUpdateProxyDeliveryPreference(str, Enum):
    r"""Delivery method instruction for proxy voting for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""
    DELIVERY_PREFERENCE_UNSPECIFIED = "DELIVERY_PREFERENCE_UNSPECIFIED"
    DIGITAL = "DIGITAL"
    PHYSICAL = "PHYSICAL"
    SUPPRESS = "SUPPRESS"


class PartyRequestUpdateRelationType(str, Enum):
    r"""Conveys how a person is related to account; Located on each account Party record; Examples are `PRIMARY_OWNER`, `JOINT_OWNER`, `EXECUTOR`, etc."""
    PARTY_RELATION_TYPE_UNSPECIFIED = "PARTY_RELATION_TYPE_UNSPECIFIED"
    PRIMARY_OWNER = "PRIMARY_OWNER"
    JOINT_OWNER = "JOINT_OWNER"
    CUSTODIAN = "CUSTODIAN"
    GUARDIAN_CONSERVATOR = "GUARDIAN_CONSERVATOR"
    POWER_OF_ATTORNEY = "POWER_OF_ATTORNEY"
    EXECUTOR = "EXECUTOR"
    AUTHORIZED_SIGNER = "AUTHORIZED_SIGNER"
    BENEFICIAL_OWNER = "BENEFICIAL_OWNER"
    CONTROL_PERSON = "CONTROL_PERSON"
    AUTHORIZED_REPRESENTATIVE = "AUTHORIZED_REPRESENTATIVE"
    TRUSTEE = "TRUSTEE"
    AUTH_TRUSTEE_REP = "AUTH_TRUSTEE_REP"


class PartyRequestUpdateStatementDeliveryPreference(str, Enum):
    r"""Delivery method instruction for account statements for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""
    DELIVERY_PREFERENCE_UNSPECIFIED = "DELIVERY_PREFERENCE_UNSPECIFIED"
    DIGITAL = "DIGITAL"
    PHYSICAL = "PHYSICAL"
    SUPPRESS = "SUPPRESS"


class PartyRequestUpdateTaxDocumentDeliveryPreference(str, Enum):
    r"""Delivery method instruction for tax documents for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated; Per regulation, selected tax forms will be mailed by regulation regardless of this setting"""
    DELIVERY_PREFERENCE_UNSPECIFIED = "DELIVERY_PREFERENCE_UNSPECIFIED"
    DIGITAL = "DIGITAL"
    PHYSICAL = "PHYSICAL"
    SUPPRESS = "SUPPRESS"


class PartyRequestUpdateTradeConfirmationDeliveryPreference(str, Enum):
    r"""Delivery method instruction for trade confirmations for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""
    DELIVERY_PREFERENCE_UNSPECIFIED = "DELIVERY_PREFERENCE_UNSPECIFIED"
    DIGITAL = "DIGITAL"
    PHYSICAL = "PHYSICAL"
    SUPPRESS = "SUPPRESS"


class PartyRequestUpdateTypedDict(TypedDict):
    r"""A single record representing an owner or manager of an Account. Contains fully populated Party Identity object."""

    email_address: NotRequired[str]
    r"""An email address indicated for account communications."""
    legal_entity_id: NotRequired[str]
    r"""Legal entity ID."""
    legal_natural_person_id: NotRequired[str]
    r"""Legal natural person ID."""
    mailing_address: NotRequired[PostalAddressUpdateTypedDict]
    r"""Represents a postal address, e.g. for postal delivery or payments addresses. Given a postal address, a postal service can deliver items to a premise, P.O. Box or similar. It is not intended to model geographical locations (roads, towns, mountains).

    In typical usage an address would be created via user input or from importing existing data, depending on the type of process.

    Advice on address input / editing: - Use an i18n-ready address widget such as  https://github.com/google/libaddressinput) - Users should not be presented with UI elements for input or editing of  fields outside countries where that field is used.

    For more guidance on how to use this schema, please see: https://support.google.com/business/answer/6397478
    """
    phone_number: NotRequired[PhoneNumberUpdateTypedDict]
    r"""An object representing a phone number, suitable as an API wire format.

    This representation:

    - should not be used for locale-specific formatting of a phone number, such  as \"+1 (650) 253-0000 ext. 123\" 

    - is not designed for efficient storage - may not be suitable for dialing - specialized libraries (see references)  should be used to parse the number for that purpose

    To do something meaningful with this number, such as format it for various use-cases, convert it to an `i18n.phonenumbers.PhoneNumber` object first.

    For instance, in Java this would be:

    com.google.type.PhoneNumber wireProto =    com.google.type.PhoneNumber.newBuilder().build();  com.google.i18n.phonenumbers.Phonenumber.PhoneNumber phoneNumber =    PhoneNumberUtil.getInstance().parse(wireProto.getE164Number(), \"ZZ\");  if (!wireProto.getExtension().isEmpty()) {   phoneNumber.setExtension(wireProto.getExtension());  }

    Reference(s):
    - https://github.com/google/libphonenumber
    """
    prospectus_delivery_preference: NotRequired[
        PartyRequestUpdateProspectusDeliveryPreference
    ]
    r"""Delivery method instruction for prospectuses for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""
    proxy_delivery_preference: NotRequired[PartyRequestUpdateProxyDeliveryPreference]
    r"""Delivery method instruction for proxy voting for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""
    relation_type: NotRequired[PartyRequestUpdateRelationType]
    r"""Conveys how a person is related to account; Located on each account Party record; Examples are `PRIMARY_OWNER`, `JOINT_OWNER`, `EXECUTOR`, etc."""
    statement_delivery_preference: NotRequired[
        PartyRequestUpdateStatementDeliveryPreference
    ]
    r"""Delivery method instruction for account statements for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""
    tax_document_delivery_preference: NotRequired[
        PartyRequestUpdateTaxDocumentDeliveryPreference
    ]
    r"""Delivery method instruction for tax documents for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated; Per regulation, selected tax forms will be mailed by regulation regardless of this setting"""
    trade_confirmation_delivery_preference: NotRequired[
        PartyRequestUpdateTradeConfirmationDeliveryPreference
    ]
    r"""Delivery method instruction for trade confirmations for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""


class PartyRequestUpdate(BaseModel):
    r"""A single record representing an owner or manager of an Account. Contains fully populated Party Identity object."""

    email_address: Optional[str] = None
    r"""An email address indicated for account communications."""
    legal_entity_id: Optional[str] = None
    r"""Legal entity ID."""
    legal_natural_person_id: Optional[str] = None
    r"""Legal natural person ID."""
    mailing_address: Optional[PostalAddressUpdate] = None
    r"""Represents a postal address, e.g. for postal delivery or payments addresses. Given a postal address, a postal service can deliver items to a premise, P.O. Box or similar. It is not intended to model geographical locations (roads, towns, mountains).

    In typical usage an address would be created via user input or from importing existing data, depending on the type of process.

    Advice on address input / editing: - Use an i18n-ready address widget such as  https://github.com/google/libaddressinput) - Users should not be presented with UI elements for input or editing of  fields outside countries where that field is used.

    For more guidance on how to use this schema, please see: https://support.google.com/business/answer/6397478
    """
    phone_number: Optional[PhoneNumberUpdate] = None
    r"""An object representing a phone number, suitable as an API wire format.

    This representation:

    - should not be used for locale-specific formatting of a phone number, such  as \"+1 (650) 253-0000 ext. 123\" 

    - is not designed for efficient storage - may not be suitable for dialing - specialized libraries (see references)  should be used to parse the number for that purpose

    To do something meaningful with this number, such as format it for various use-cases, convert it to an `i18n.phonenumbers.PhoneNumber` object first.

    For instance, in Java this would be:

    com.google.type.PhoneNumber wireProto =    com.google.type.PhoneNumber.newBuilder().build();  com.google.i18n.phonenumbers.Phonenumber.PhoneNumber phoneNumber =    PhoneNumberUtil.getInstance().parse(wireProto.getE164Number(), \"ZZ\");  if (!wireProto.getExtension().isEmpty()) {   phoneNumber.setExtension(wireProto.getExtension());  }

    Reference(s):
    - https://github.com/google/libphonenumber
    """
    prospectus_delivery_preference: Optional[
        PartyRequestUpdateProspectusDeliveryPreference
    ] = None
    r"""Delivery method instruction for prospectuses for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""
    proxy_delivery_preference: Optional[
        PartyRequestUpdateProxyDeliveryPreference
    ] = None
    r"""Delivery method instruction for proxy voting for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""
    relation_type: Optional[PartyRequestUpdateRelationType] = None
    r"""Conveys how a person is related to account; Located on each account Party record; Examples are `PRIMARY_OWNER`, `JOINT_OWNER`, `EXECUTOR`, etc."""
    statement_delivery_preference: Optional[
        PartyRequestUpdateStatementDeliveryPreference
    ] = None
    r"""Delivery method instruction for account statements for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""
    tax_document_delivery_preference: Optional[
        PartyRequestUpdateTaxDocumentDeliveryPreference
    ] = None
    r"""Delivery method instruction for tax documents for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated; Per regulation, selected tax forms will be mailed by regulation regardless of this setting"""
    trade_confirmation_delivery_preference: Optional[
        PartyRequestUpdateTradeConfirmationDeliveryPreference
    ] = None
    r"""Delivery method instruction for trade confirmations for a given Party record; Can be `DIGITAL`, `PHYSICAL`, `SUPPRESS`; Defaults to `DIGITAL` on account creation but may be updated"""
