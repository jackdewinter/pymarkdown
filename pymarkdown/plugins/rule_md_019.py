"""
Module to implement a plugin that looks for multiple spaces after the hash
mark on an atx heading.
"""

from typing import Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class RuleMd019(RulePlugin):
    """
    Class to implement a plugin that looks for multiple spaces after the hash
    mark on an atx heading.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__atx_heading_token: Optional[AtxHeadingMarkdownToken] = None

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="no-multiple-space-atx",
            plugin_id="MD019",
            plugin_enabled_by_default=True,
            plugin_description="Multiple spaces are present after hash character on Atx Heading.",
            plugin_version="0.5.1",
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md019.md",
            plugin_supports_fix=True,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__atx_heading_token = None

    def __report(
        self, context: PluginScanContext, text_token: TextMarkdownToken
    ) -> None:
        assert self.__atx_heading_token is not None
        if context.in_fix_mode:
            self.register_fix_token_request(
                context,
                text_token,
                "next_token",
                "extracted_whitespace",
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
            if not atx_token.remove_trailing_count:
                self.__atx_heading_token = atx_token
        elif token.is_paragraph_end:
            self.__atx_heading_token = None
        elif token.is_text:
            text_token = cast(TextMarkdownToken, token)
            resolved_extracted_whitespace = ParserHelper.remove_all_from_text(
                text_token.extracted_whitespace
            )
            if self.__atx_heading_token and "\t" in resolved_extracted_whitespace:
                start_index = (
                    self.__atx_heading_token.column_number
                    - 1
                    + self.__atx_heading_token.hash_count
                )
                resolved_extracted_whitespace = TabHelper.detabify_string(
                    resolved_extracted_whitespace, start_index
                )
            if self.__atx_heading_token and len(resolved_extracted_whitespace) > 1:
                self.__report(context, text_token)
            self.__atx_heading_token = None
