"""
Module to implement a plugin that looks for text in a paragraph where a line starts
with what could be a closed atx heading, except there is no spaces between the hashes
and the text of the heading, either at the start, end, or both.
"""
import re

from pymarkdown.markdown_token import (
    AtxHeadingMarkdownToken,
    ParagraphMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd020(Plugin):
    """
    Class to implement a plugin that looks for text in a paragraph where a line starts
    with what could be a closed atx heading, except there is no spaces between the hashes
    and the text of the heading, either at the start, end, or both.
    """

    def __init__(self):
        super().__init__()
        self.__last_paragraph_token = None
        self.__is_in_normal_atx = None
        self.__last_atx_token = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers, atx_closed, spaces
            plugin_name="no-missing-space-closed-atx",
            plugin_id="MD020",
            plugin_enabled_by_default=True,
            plugin_description="No space inside hashes on closed atx style heading",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md020---no-space-inside-hashes-on-closed-atx-style-heading

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_paragraph_token = None
        self.__is_in_normal_atx = False
        self.__last_atx_token = None

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        if not (token.is_atx_heading_end) and self.__is_in_normal_atx:
            self.__last_atx_token = token

        if isinstance(token, ParagraphMarkdownToken):
            self.__last_paragraph_token = token
        elif isinstance(token, AtxHeadingMarkdownToken):
            self.__is_in_normal_atx = True
        elif token.is_paragraph_end:
            self.__last_paragraph_token = None
        elif token.is_atx_heading_end:
            if self.__is_in_normal_atx and isinstance(
                self.__last_atx_token, TextMarkdownToken
            ):
                if self.__last_atx_token.token_text.endswith("#"):
                    self.report_next_token_error(token)
            self.__is_in_normal_atx = False
        elif isinstance(token, TextMarkdownToken) and self.__last_paragraph_token:
            split_whitespace = self.__last_paragraph_token.extracted_whitespace.split(
                "\n"
            )
            split_text = token.token_text.split("\n")
            assert len(split_whitespace) == len(split_text)

            for split_index, next_text in enumerate(split_text):
                combined_text = split_whitespace[split_index] + next_text
                if re.search(r"^\s{0,3}#{1,6}.*#+\s*$", combined_text):
                    self.report_next_token_error(token)
