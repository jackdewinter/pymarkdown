"""
Module to provide for a debug extension.
"""

from application_properties import ApplicationPropertiesFacade

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension


class ExceptionTestException(Exception):
    """
    Custom exception for the DebugExtension class.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class DebugExtension(ParserExtension):
    """
    Extension to provide for a debug extension.
    """

    def get_identifier(self) -> str:
        """
        Get the identifier associated with this extension.
        """
        return "debug-extension"

    def get_details(self) -> ExtensionDetails:
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=self.get_identifier(),
            extension_name="Debug Extension",
            extension_description="Allows testing through debug.",
            extension_enabled_by_default=False,
            extension_version=ExtensionManagerConstants.EXTENSION_VERSION_NOT_IMPLEMENTED,
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url=None,
            extension_configuration=None,
        )

    def apply_configuration(
        self, extension_specific_facade: ApplicationPropertiesFacade
    ) -> None:
        """
        Apply any configuration required by the extension.
        """
        debug_mode = extension_specific_facade.get_integer_property(
            "debug_mode", default_value=0
        )
        if debug_mode == 1:
            raise ExceptionTestException("blah")
        if debug_mode == 2:
            raise ValueError("blah")
