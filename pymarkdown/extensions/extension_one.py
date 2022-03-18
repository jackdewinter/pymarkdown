"""
Module to provide for a debug extension.
"""

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager import ExtensionManagerConstants
from pymarkdown.extension_manager.parser_extension import ParserExtension


class DebugExtension(ParserExtension):
    """
    Extension to provide for a debug extension.
    """

    @classmethod
    def get_identifier(cls):
        """
        Get the identifier associated with this extension.
        """
        return "debug-extension"

    @classmethod
    def get_details(cls):
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=cls.get_identifier(),
            extension_name="Debug Extension",
            extension_description="Allows testing through debug.",
            extension_enabled_by_default=False,
            extension_version=ExtensionManagerConstants.EXTENSION_VERSION_NOT_IMPLEMENTED,
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url=None,
            extension_configuration=None,
        )

    @classmethod
    def apply_configuration(cls, extension_specific_facade):
        """
        Apply any configuration required by the extension.
        """
        debug_mode = extension_specific_facade.get_integer_property(
            "debug_mode", default_value=0
        )
        if debug_mode == 1:
            raise Exception("blah")
        if debug_mode == 2:
            raise ValueError("blah")
