"""
Module to provide for extending what is considered to be an autolink.
"""

from application_properties import ApplicationPropertiesFacade

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension


class MarkdownExtendedAutolinksExtension(ParserExtension):
    """
    Extension to implement the extended autolinks extension.
    """

    @classmethod
    def get_identifier(cls) -> str:
        """
        Get the identifier associated with this extension.
        """
        return "markdown-extended-autolinks"

    @classmethod
    def get_details(cls) -> ExtensionDetails:
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=cls.get_identifier(),
            extension_name="Markdown Extended Autolinks",
            extension_description="Allows extended parsing of Markdown Autolinks.",
            extension_enabled_by_default=False,
            extension_version=ExtensionManagerConstants.EXTENSION_VERSION_NOT_IMPLEMENTED,
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url="https://github.github.com/gfm/#autolinks-extension-",
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
