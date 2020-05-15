"""
Module to implement a plugin that looks for text in a paragraph where a line starts
with what could be an atx heading, except there is no spaces between the hashes and
the text of the heading.
"""
import re

from pymarkdown.markdown_token import (
    EndMarkdownToken,
    MarkdownToken,
    ParagraphMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd018(Plugin):
    """
    Class to implement a plugin that looks for text in a paragraph where a line starts
    with what could be an atx heading, except there is no spaces between the hashes and
    the text of the heading.
    """

    def __init__(self):
        super().__init__()
        self.__last_paragraph_token = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers, atx, spaces
            plugin_name="no-missing-space-atx",
            plugin_id="MD018",
            plugin_enabled_by_default=True,
            plugin_description="No space after hash on atx style heading",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md018---no-space-after-hash-on-atx-style-heading

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_paragraph_token = None

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        if isinstance(token, ParagraphMarkdownToken):
            self.__last_paragraph_token = token
        elif isinstance(token, EndMarkdownToken):
            if token.type_name == MarkdownToken.token_paragraph:
                self.__last_paragraph_token = None
        elif isinstance(token, TextMarkdownToken) and self.__last_paragraph_token:
            split_whitespace = self.__last_paragraph_token.extracted_whitespace.split(
                "\n"
            )
            split_text = token.token_text.split("\n")
            assert len(split_whitespace) == len(split_text)

            for split_index, next_text in enumerate(split_text):
                combined_text = split_whitespace[split_index] + next_text
                if re.search(r"^\s{0,3}#{1,6}\S", combined_text) and not re.search(
                    r"#\s*$", combined_text
                ):
                    self.report_next_token_error(token)
