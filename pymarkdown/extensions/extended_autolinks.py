"""
Module to provide for extending what is considered to be an autolink.
"""

from pymarkdown.extension_manager.extension_impl import ExtensionDetails


# pylint: disable=too-few-public-methods
class MarkdownExtendedAutolinksExtension:
    """
    Extension to implement the extended autolinks extension.
    """

    @classmethod
    def get_details(cls):
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id="markdown-extended-autolinks",
            extension_name="Markdown Extended Autolinks",
            extension_description="Allows extended parsing of Markdown Autolinks.",
            extension_enabled_by_default=False,
            extension_version="0.0.0",
            extension_interface_version=1,
            extension_url="https://github.github.com/gfm/#autolinks-extension-",
            extension_configuration=None,
        )


# pylint: enable=too-few-public-methods
