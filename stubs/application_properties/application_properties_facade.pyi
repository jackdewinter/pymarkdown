from typing import Any

from application_properties.application_properties import (
    ApplicationProperties as ApplicationProperties,
)

LOGGER: Any

class ApplicationPropertiesFacade:
    def __init__(self, base_properties, property_prefix) -> None: ...
    def get_property(
        self,
        property_name,
        property_type,
        default_value: Any | None = ...,
        valid_value_fn: Any | None = ...,
        is_required: bool = ...,
        strict_mode: bool = ...,
    ): ...
    def get_boolean_property(
        self,
        property_name,
        default_value: Any | None = ...,
        is_required: bool = ...,
        strict_mode: Any | None = ...,
    ): ...
    def get_integer_property(
        self,
        property_name,
        default_value: Any | None = ...,
        valid_value_fn: Any | None = ...,
        is_required: bool = ...,
        strict_mode: Any | None = ...,
    ): ...
    def get_string_property(
        self,
        property_name,
        default_value: Any | None = ...,
        valid_value_fn: Any | None = ...,
        is_required: bool = ...,
        strict_mode: Any | None = ...,
    ): ...
    @property
    def property_names(self): ...
    def property_names_under(self, key_name): ...
