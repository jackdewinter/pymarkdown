"""
Module to provide for the recognition of Markdown tables.
"""

from application_properties import ApplicationPropertiesFacade

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension


class MarkdownTablesExtension(ParserExtension):
    """
    Extension to implement the tables extension.
    """

    @classmethod
    def get_identifier(cls) -> str:
        """
        Get the identifier associated with this extension.
        """
        return "markdown-tables"

    @classmethod
    def get_details(cls) -> ExtensionDetails:
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=cls.get_identifier(),
            extension_name="Markdown Tables",
            extension_description="Allows parsing of Markdown tables.",
            extension_enabled_by_default=False,
            extension_version=ExtensionManagerConstants.EXTENSION_VERSION_NOT_IMPLEMENTED,
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url="https://github.github.com/gfm/#tables-extension-",
            extension_configuration=None,
        )

    @classmethod
    def apply_configuration(
        cls, extension_specific_facade: ApplicationPropertiesFacade
    ) -> None:
        """
        Apply any configuration required by the extension.
        """
        _ = extension_specific_facade  # pragma: no cover
