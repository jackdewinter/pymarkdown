"""
Module to provide for the recognition of Markdown tables.
"""

from pymarkdown.extension_manager.extension_impl import ExtensionDetails


# pylint: disable=too-few-public-methods
class MarkdownTablesExtension:
    """
    Extension to implement the tables extension.
    """

    @classmethod
    def get_details(cls):
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id="markdown-tables",
            extension_name="Markdown Tables",
            extension_description="Allows parsing of Markdown tables.",
            extension_enabled_by_default=False,
            extension_version="0.0.0",
            extension_interface_version=1,
            extension_url="https://github.github.com/gfm/#tables-extension-",
            extension_configuration=None,
        )


# pylint: enable=too-few-public-methods
