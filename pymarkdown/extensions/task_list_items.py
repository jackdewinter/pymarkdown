"""
Module to provide for a list item that can be check off.
"""
from pymarkdown.extension_impl import ExtensionDetails


# pylint: disable=too-few-public-methods
class MarkdownTaskListItemsExtension:
    """
    Extension to implement the task list items extension.
    """

    @classmethod
    def get_details(cls):
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id="markdown-task-list-items",
            extension_name="Markdown Task List Items",
            extension_description="Allows parsing of Markdown task list items.",
            extension_enabled_by_default=False,
            extension_version="0.0.0",
            extension_interface_version=1,
            extension_url="https://github.github.com/gfm/#task-list-items-extension-",
            extension_configuration=None,
        )


# pylint: enable=too-few-public-methods
