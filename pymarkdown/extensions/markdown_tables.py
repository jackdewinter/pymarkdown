"""
Module to provide for the recognition of Markdown tables.
"""

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension
from pymarkdown.my_application_properties_facade import MyApplicationPropertiesFacade


class MarkdownTablesExtension(ParserExtension):
    """
    Extension to implement the tables extension.
    """

    def get_identifier(self) -> str:
        """
        Get the identifier associated with this extension.
        """
        return "markdown-tables"

    def get_details(self) -> ExtensionDetails:
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=self.get_identifier(),
            extension_name="Markdown Tables",
            extension_description="Allows parsing of Markdown tables.",
            extension_enabled_by_default=False,
            extension_version="0.1.0",
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url="https://github.github.com/gfm/#tables-extension-",
            extension_configuration=None,
        )

    def apply_configuration(
        self, extension_specific_facade: MyApplicationPropertiesFacade
    ) -> None:
        """
        Apply any configuration required by the extension.
        """
        _ = extension_specific_facade  # pragma: no cover
