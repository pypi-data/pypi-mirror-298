"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from typing import Any


def get_discriminator(model: Any, fieldname: str, key: str) -> str:
    if isinstance(model, dict):
        try:
            return f"{model.get(key)}"
        except AttributeError as e:
            raise ValueError(
                f"Could not find discriminator key {key} in {model}"
            ) from e

    if hasattr(model, fieldname):
        return f"{getattr(model, fieldname)}"

    fieldname = fieldname.upper()
    if hasattr(model, fieldname):
        return f"{getattr(model, fieldname)}"

    raise ValueError(f"Could not find discriminator field {fieldname} in {model}")
