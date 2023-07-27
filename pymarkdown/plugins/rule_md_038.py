"""
Module to implement a plugin that looks for leading and trailing spaces within code spans.
"""
from typing import cast

from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.inline_markdown_token import InlineCodeSpanMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd038(RulePlugin):
    """
    Class to implement a plugin that looks for leading and trailing spaces within code spans.
    """

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-space-in-code",
            plugin_id="MD038",
            plugin_enabled_by_default=True,
            plugin_description="Spaces inside code span elements",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md038.md",
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_inline_code_span:
            code_span_token = cast(InlineCodeSpanMarkdownToken, token)
            has_trailing = False
            if len(code_span_token.span_text) == 1:
                has_leading = code_span_token.span_text[0] == " "
            else:
                has_leading = (
                    code_span_token.span_text[0] == " "
                    and code_span_token.span_text[1] != "`"
                )
                has_trailing = (
                    code_span_token.span_text[-1] == " "
                    and code_span_token.span_text[-2] != "`"
                )
            if has_leading != has_trailing or has_leading:
                self.report_next_token_error(context, token)
