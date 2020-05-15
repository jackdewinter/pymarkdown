"""
Module to implement a plugin that looks for multiple spaces after the hash
mark on a atx heading.
"""
from pymarkdown.markdown_token import (
    AtxHeadingMarkdownToken,
    EndMarkdownToken,
    MarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd019(Plugin):
    """
    Class to implement a plugin that looks for multiple spaces after the hash
    mark on a atx heading.
    """

    def __init__(self):
        super().__init__()
        self.__in_atx_heading = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers, atx, spaces
            plugin_name="no-multiple-space-atx",
            plugin_id="MD019",
            plugin_enabled_by_default=True,
            plugin_description="Multiple spaces after hash on atx style heading",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md019---multiple-spaces-after-hash-on-atx-style-heading

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__in_atx_heading = None

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        if isinstance(token, AtxHeadingMarkdownToken):
            self.__in_atx_heading = not token.remove_trailing_count
        elif isinstance(token, EndMarkdownToken):
            if token.type_name == MarkdownToken.token_paragraph:
                self.__in_atx_heading = False
        elif isinstance(token, TextMarkdownToken):
            if self.__in_atx_heading and len(token.extracted_whitespace) > 1:
                self.report_next_token_error(token)
