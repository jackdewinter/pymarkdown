"""
Module to implement a plugin that looks for more than one space between either the
opening or closing hashes of an atx heading.
"""
from typing import Optional, cast

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
        self.__atx_heading_token: Optional[MarkdownToken] = None
        self.__is_left_in_error = False
        self.__first_text_token: Optional[TextMarkdownToken] = None

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="no-multiple-space-closed-atx",
            plugin_id="MD021",
            plugin_enabled_by_default=True,
            plugin_description="Multiple spaces are present inside hash characters on Atx Closed Heading.",
            plugin_version="0.5.0",
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md021.md",
            plugin_supports_fix=True,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__atx_heading_token = None
        self.__first_text_token = None
        self.__is_left_in_error = False

    def __report(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        end_token: EndMarkdownToken,
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
            if (
                end_token.extra_end_data is not None
                and len(end_token.extra_end_data) > 1
            ):
                self.register_fix_token_request(
                    context,
                    token,
                    "next_token",
                    "extra_end_data",
                    " ",
                )
        else:
            self.report_next_token_error(context, self.__atx_heading_token)

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_atx_heading:
            atx_token = cast(AtxHeadingMarkdownToken, token)
            if atx_token.remove_trailing_count:
                self.__atx_heading_token = token
            self.__is_left_in_error = False
        elif token.is_paragraph_end:
            self.__atx_heading_token = None
        elif token.is_atx_heading_end:
            end_token = cast(EndMarkdownToken, token)
            assert end_token.extra_end_data is not None
            if self.__is_left_in_error or len(end_token.extra_end_data) > 1:
                self.__report(context, token, end_token)
        elif token.is_text:
            text_token = cast(TextMarkdownToken, token)
            self.__first_text_token = text_token
            if self.__atx_heading_token and len(text_token.extracted_whitespace) > 1:
                self.__is_left_in_error = True
