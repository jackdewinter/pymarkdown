"""
Module to provide for disallowing raw HTML in document.
"""

from pymarkdown.extension_manager.extension_impl import ExtensionDetails


# pylint: disable=too-few-public-methods
class MarkdownDisallowRawHtmlExtension:
    """
    Extension to implement the disallow rawhtml extension.
    """

    @classmethod
    def get_details(cls):
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id="markdown-disallow_raw_html",
            extension_name="Markdown Disallow Raw HTML",
            extension_description="Disallows parsing of any raw HTML.",
            extension_enabled_by_default=False,
            extension_version="0.0.0",
            extension_interface_version=1,
            extension_url="https://github.github.com/gfm/#disallowed-raw-html-extension-",
            extension_configuration=None,
        )


# pylint: enable=too-few-public-methods
