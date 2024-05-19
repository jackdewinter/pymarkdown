"""
Module to implement a plugin that looks for more than one space between either the
opening or closing hashes of an atx heading.
"""

from typing import Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class RuleMd021(RulePlugin):
    """
    Class to implement a plugin that looks for more than one space between either the
    opening or closing hashes of an atx heading.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__atx_heading_token: Optional[AtxHeadingMarkdownToken] = None
        self.__is_left_in_error = False
        self.__first_text_token: Optional[TextMarkdownToken] = None
        self.__last_token: Optional[TextMarkdownToken] = None

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="no-multiple-space-closed-atx",
            plugin_id="MD021",
            plugin_enabled_by_default=True,
            plugin_description="Multiple spaces are present inside hash characters on Atx Closed Heading.",
            plugin_version="0.5.1",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md021.md",
            plugin_supports_fix=True,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__atx_heading_token = None
        self.__first_text_token = None
        self.__last_token = None
        self.__is_left_in_error = False

    def __report(
        self, context: PluginScanContext, token: MarkdownToken, extra_end_data: str
    ) -> None:
        assert self.__atx_heading_token is not None
        if context.in_fix_mode:
            if self.__is_left_in_error:
                assert self.__first_text_token is not None
                self.register_fix_token_request(
                    context,
                    self.__first_text_token,
                    "next_token",
                    "extracted_whitespace",
                    " ",
                )
            if len(extra_end_data) > 1:
                self.register_fix_token_request(
                    context,
                    token,
                    "next_token",
                    "extra_end_data",
                    " ",
                )
        else:
            self.report_next_token_error(context, self.__atx_heading_token)

    def __handle_atx_end(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        end_token = cast(EndMarkdownToken, token)
        assert end_token.extra_end_data is not None
        extra_end_data = end_token.extra_end_data
        if "\t" in extra_end_data:
            assert self.__last_token is not None
            assert self.__last_token.is_text
            resolved_token_text = ParserHelper.remove_all_from_text(
                self.__last_token.token_text
            )
            start_index = self.__last_token.column_number - 1
            resolved_token_text = TabHelper.detabify_string(
                resolved_token_text, start_index
            )
            start_index_after_last_text_token = start_index + len(resolved_token_text)
            extra_end_data = TabHelper.detabify_string(
                extra_end_data, start_index_after_last_text_token
            )
        if self.__is_left_in_error or len(extra_end_data) > 1:
            self.__report(context, token, extra_end_data)
        self.__atx_heading_token = None
        self.__first_text_token = None
        self.__last_token = None

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_atx_heading:
            atx_token = cast(AtxHeadingMarkdownToken, token)
            if atx_token.remove_trailing_count:
                self.__atx_heading_token = atx_token
            self.__is_left_in_error = False
        elif token.is_paragraph_end:
            self.__atx_heading_token = None
        elif token.is_atx_heading_end:
            self.__handle_atx_end(context, token)
        elif token.is_text:
            text_token = cast(TextMarkdownToken, token)
            if not self.__first_text_token and self.__atx_heading_token:
                resolved_extracted_whitespace = ParserHelper.remove_all_from_text(
                    text_token.extracted_whitespace
                )
                if "\t" in resolved_extracted_whitespace:
                    start_index = (
                        self.__atx_heading_token.column_number
                        - 1
                        + self.__atx_heading_token.hash_count
                    )
                    resolved_extracted_whitespace = TabHelper.detabify_string(
                        resolved_extracted_whitespace, start_index
                    )
                if len(resolved_extracted_whitespace) > 1:
                    self.__is_left_in_error = True
                self.__first_text_token = text_token
            self.__last_token = text_token
