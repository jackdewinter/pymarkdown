"""
Module to provide for recognizing a strikethrough sequence.
"""

from application_properties import ApplicationPropertiesFacade

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension


class MarkdownStrikeThroughExtension(ParserExtension):
    """
    Extension to implement the strikethrough extension.
    """

    def get_identifier(self) -> str:
        """
        Get the identifier associated with this extension.
        """
        return "markdown-strikethrough"

    def get_details(self) -> ExtensionDetails:
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=self.get_identifier(),
            extension_name="Markdown Strikethrough",
            extension_description="Allows parsing of Markdown strikethrough.",
            extension_enabled_by_default=False,
            extension_version="0.5.0",
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url="https://github.github.com/gfm/#strikethrough-extension-",
            extension_configuration=None,
        )

    def apply_configuration(
        self, extension_specific_facade: ApplicationPropertiesFacade
    ) -> None:
        """
        Apply any configuration required by the extension.
        """
        _ = extension_specific_facade  # pragma: no cover
