"""
Module to provide for disallowing raw HTML in document.
"""

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension


class MarkdownDisallowRawHtmlExtension(ParserExtension):
    """
    Extension to implement the disallow rawhtml extension.
    """

    @classmethod
    def get_identifier(cls):
        """
        Get the identifier associated with this extension.
        """
        return "markdown-disallow_raw_html"

    @classmethod
    def get_details(cls):
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=cls.get_identifier(),
            extension_name="Markdown Disallow Raw HTML",
            extension_description="Disallows parsing of any raw HTML.",
            extension_enabled_by_default=False,
            extension_version=ExtensionManagerConstants.EXTENSION_VERSION_NOT_IMPLEMENTED,
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url="https://github.github.com/gfm/#disallowed-raw-html-extension-",
            extension_configuration=None,
        )

    @classmethod
    def apply_configuration(cls, extension_specific_facade):
        """
        Apply any configuration required by the extension.
        """
        _ = extension_specific_facade  # pragma: no cover
