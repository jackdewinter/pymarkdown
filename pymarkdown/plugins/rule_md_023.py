"""
Module to implement a plugin that looks for headings that do not start at the
beginning of the line.
"""
from pymarkdown.markdown_token import (
    AtxHeadingMarkdownToken,
    EndMarkdownToken,
    MarkdownToken,
    SetextHeadingMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd023(Plugin):
    """
    Class to implement a plugin that looks for headings that do not start at the
    beginning of the line.
    """

    def __init__(self):
        super().__init__()
        self.__setext_start_token = None
        self.__any_leading_whitespace_detected = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers, spaces
            plugin_name="heading-start-left, header-start-left",
            plugin_id="MD023",
            plugin_enabled_by_default=True,
            plugin_description="Headings must start at the beginning of the line",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md023---headings-must-start-at-the-beginning-of-the-line

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__setext_start_token = None
        self.__any_leading_whitespace_detected = False

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        if isinstance(token, (AtxHeadingMarkdownToken)):
            if token.extracted_whitespace:
                self.report_next_token_error(token)
        elif isinstance(token, (SetextHeadingMarkdownToken)):
            self.__setext_start_token = token
            self.__any_leading_whitespace_detected = bool(token.remaining_line)
        elif isinstance(token, (TextMarkdownToken)):
            if self.__setext_start_token and not self.__any_leading_whitespace_detected:
                if token.end_whitespace and " " in token.end_whitespace:
                    self.__any_leading_whitespace_detected = True
        elif isinstance(token, EndMarkdownToken):
            if token.type_name in (MarkdownToken.token_setext_heading,):
                if token.extracted_whitespace:
                    self.__any_leading_whitespace_detected = True

                if self.__any_leading_whitespace_detected:
                    self.report_next_token_error(self.__setext_start_token)
                self.__setext_start_token = None
