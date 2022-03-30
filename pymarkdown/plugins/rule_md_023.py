"""
Module to implement a plugin that looks for headings that do not start at the
beginning of the line.
"""
from typing import Optional, cast

from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_markdown_token import (
    AtxHeadingMarkdownToken,
    SetextHeadingMarkdownToken,
)
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd023(RulePlugin):
    """
    Class to implement a plugin that looks for headings that do not start at the
    beginning of the line.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__setext_start_token: Optional[SetextHeadingMarkdownToken] = None
        self.__any_leading_whitespace_detected = False
        self.__seen_first_line_of_setext = False

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="heading-start-left, header-start-left",
            plugin_id="MD023",
            plugin_enabled_by_default=True,
            plugin_description="Headings must start at the beginning of the line.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md023.md",
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__setext_start_token = None
        self.__any_leading_whitespace_detected = False
        self.__seen_first_line_of_setext = False

    def __handle_atx_heading(
        self, context: PluginScanContext, token: AtxHeadingMarkdownToken
    ) -> None:
        if token.extracted_whitespace:
            self.report_next_token_error(context, token)

    def __handle_setext_heading(self, token: SetextHeadingMarkdownToken) -> None:
        self.__setext_start_token = token
        self.__any_leading_whitespace_detected = bool(token.extracted_whitespace)
        self.__seen_first_line_of_setext = False

    def __handle_setext_heading_end(
        self, context: PluginScanContext, token: EndMarkdownToken
    ) -> None:
        if token.extracted_whitespace:
            self.__any_leading_whitespace_detected = True

        if self.__any_leading_whitespace_detected:
            assert self.__setext_start_token is not None
            self.report_next_token_error(context, self.__setext_start_token)
        self.__setext_start_token = None

    def __handle_text(self, token: TextMarkdownToken) -> None:
        if (
            self.__setext_start_token
            and not self.__any_leading_whitespace_detected
            and token.end_whitespace
        ):
            split_end_whitespace = token.end_whitespace.split(
                ParserHelper.newline_character
            )
            for next_split in split_end_whitespace:
                if self.__seen_first_line_of_setext:
                    split_next_split = next_split.split(
                        ParserHelper.whitespace_split_character
                    )
                    if len(split_next_split) == 2 and split_next_split[0]:
                        self.__any_leading_whitespace_detected = True
                else:
                    self.__seen_first_line_of_setext = True

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_atx_heading:
            atx_token = cast(AtxHeadingMarkdownToken, token)
            self.__handle_atx_heading(context, atx_token)
        elif token.is_setext_heading:
            setext_token = cast(SetextHeadingMarkdownToken, token)
            self.__handle_setext_heading(setext_token)
        elif token.is_text:
            text_token = cast(TextMarkdownToken, token)
            self.__handle_text(text_token)
        elif token.is_setext_heading_end:
            end_token = cast(EndMarkdownToken, token)
            self.__handle_setext_heading_end(context, end_token)
