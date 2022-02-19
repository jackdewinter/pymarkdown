"""
Module to provide for a debug extension.
"""

from pymarkdown.extension_manager.extension_impl import ExtensionDetails


class DebugExtension:
    """
    Extension to provide for a debug extension.
    """

    @classmethod
    def get_details(cls):
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id="debug-extension",
            extension_name="Debug Extension",
            extension_description="Allows testing through debug.",
            extension_enabled_by_default=False,
            extension_version="0.0.0",
            extension_interface_version=1,
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
