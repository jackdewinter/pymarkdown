from typing import Any

LOGGER: Any

class ApplicationProperties:
    def __init__(self, strict_mode: bool = ...) -> None: ...
    @property
    def separator(self): ...
    @property
    def number_of_properties(self): ...
    @property
    def property_names(self): ...
    @property
    def strict_mode(self): ...
    def enable_strict_mode(self) -> None: ...
    def load_from_dict(self, config_map) -> None: ...
    @staticmethod
    def verify_full_part_form(property_key): ...
    @staticmethod
    def verify_full_key_form(property_key): ...
    @staticmethod
    def verify_manual_property_form(string_to_verify): ...
    def set_manual_property(self, combined_string) -> None: ...
    def get_property(
        self,
        property_name,
        property_type,
        default_value: Any | None = ...,
        valid_value_fn: Any | None = ...,
        is_required: bool = ...,
        strict_mode: Any | None = ...,
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
    def property_names_under(self, key_name): ...
