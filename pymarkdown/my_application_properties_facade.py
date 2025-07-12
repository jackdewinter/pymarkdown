"""
Module to provide some extra support to the ApplicationPropertiesFacade class.
"""

from typing import Any, Callable, Optional

from application_properties import ApplicationPropertiesFacade


class MyApplicationPropertiesFacade:
    """
    Class to provide extra functionality to the ApplicationPropertiesFacade class.
    If proven, the ultimate goal is to include this support in `application_properties`.
    """

    def __init__(self, properties_facade: ApplicationPropertiesFacade):
        self.__properties_facade = properties_facade

    def get_boolean_property_with_default(
        self,
        property_name: str,
        default_value: bool,
        is_required: bool = False,
    ) -> bool:
        """
        Get a boolean property from the configuration.
        """
        intermediate_result = self.__properties_facade.get_boolean_property(
            property_name=property_name,
            default_value=default_value,
            is_required=is_required,
        )
        assert intermediate_result is not None
        return intermediate_result

    # pylint: disable=too-many-arguments
    def get_integer_property_with_default(
        self,
        property_name: str,
        default_value: int,
        valid_value_fn: Optional[Callable[[int], Any]] = None,
        is_required: bool = False,
        strict_mode: Optional[bool] = None,
    ) -> int:
        """
        Get an integer property from the configuration.

        TODO update docstrings for App_properties to be reflective of what they are.
        """
        intermediate_result = self.__properties_facade.get_integer_property(
            property_name=property_name,
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
        )
        assert intermediate_result is not None
        return intermediate_result

    # pylint: enable=too-many-arguments
    # pylint: disable=too-many-arguments
    def get_string_property_with_default(
        self,
        property_name: str,
        default_value: str,
        valid_value_fn: Optional[Callable[[str], Any]] = None,
        is_required: bool = False,
        strict_mode: Optional[bool] = None,
    ) -> str:
        """
        Get a string property from the configuration.
        """
        intermediate_result = self.__properties_facade.get_string_property(
            property_name=property_name,
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
        )
        assert intermediate_result is not None
        return intermediate_result

    # pylint: enable=too-many-arguments

    def get_boolean_property(
        self,
        property_name: str,
        default_value: Optional[bool] = None,
        is_required: bool = False,
    ) -> Optional[bool]:
        """
        Get a boolean property from the configuration.
        """
        return self.__properties_facade.get_boolean_property(
            property_name=property_name,
            default_value=default_value,
            is_required=is_required,
        )

    # pylint: disable=too-many-arguments
    def get_integer_property(
        self,
        property_name: str,
        default_value: Optional[int] = None,
        valid_value_fn: Optional[Callable[[int], Any]] = None,
        is_required: bool = False,
        strict_mode: Optional[bool] = None,
    ) -> Optional[int]:
        """
        Get an integer property from the configuration.
        """
        return self.__properties_facade.get_integer_property(
            property_name=property_name,
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def get_string_property(
        self,
        property_name: str,
        default_value: Optional[str] = None,
        valid_value_fn: Optional[Callable[[str], Any]] = None,
        is_required: bool = False,
        strict_mode: Optional[bool] = None,
    ) -> Optional[str]:
        """
        Get a string property from the configuration.
        """
        return self.__properties_facade.get_string_property(
            property_name=property_name,
            default_value=default_value,
            valid_value_fn=valid_value_fn,
            is_required=is_required,
            strict_mode=strict_mode,
        )

    # pylint: enable=too-many-arguments
