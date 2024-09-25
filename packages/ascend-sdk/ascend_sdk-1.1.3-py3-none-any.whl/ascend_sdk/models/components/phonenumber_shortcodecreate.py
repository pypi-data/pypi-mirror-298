"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
from ascend_sdk.types import BaseModel
from typing import Optional, TypedDict
from typing_extensions import NotRequired


class PhoneNumberShortCodeCreateTypedDict(TypedDict):
    r"""An object representing a short code, which is a phone number that is typically much shorter than regular phone numbers and can be used to address messages in MMS and SMS systems, as well as for abbreviated dialing (e.g. \"Text 611 to see how many minutes you have remaining on your plan.\").

    Short codes are restricted to a region and are not internationally dialable, which means the same short code can exist in different regions, with different usage and pricing, even if those regions share the same country calling code (e.g. US and CA).
    """

    number: NotRequired[str]
    r"""Required. The short code digits, without a leading plus ('+') or country calling code, e.g. \"611\"."""
    region_code: NotRequired[str]
    r"""Required. The BCP-47 region code of the location where calls to this short code can be made, such as \"US\" and \"BB\".

    Reference(s):
    - http://www.unicode.org/reports/tr35/#unicode_region_subtag
    """


class PhoneNumberShortCodeCreate(BaseModel):
    r"""An object representing a short code, which is a phone number that is typically much shorter than regular phone numbers and can be used to address messages in MMS and SMS systems, as well as for abbreviated dialing (e.g. \"Text 611 to see how many minutes you have remaining on your plan.\").

    Short codes are restricted to a region and are not internationally dialable, which means the same short code can exist in different regions, with different usage and pricing, even if those regions share the same country calling code (e.g. US and CA).
    """

    number: Optional[str] = None
    r"""Required. The short code digits, without a leading plus ('+') or country calling code, e.g. \"611\"."""
    region_code: Optional[str] = None
    r"""Required. The BCP-47 region code of the location where calls to this short code can be made, such as \"US\" and \"BB\".

    Reference(s):
    - http://www.unicode.org/reports/tr35/#unicode_region_subtag
    """
