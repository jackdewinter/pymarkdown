"""
Module to implement a plugin that looks for leading and trailing spaces within code spans.
"""

from typing import cast

from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd038(RulePlugin):
    """
    Class to implement a plugin that looks for leading and trailing spaces within code spans.
    """

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="no-space-in-code",
            plugin_id="MD038",
            plugin_enabled_by_default=True,
            plugin_description="Spaces inside code span elements",
            plugin_version="0.5.1",
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md038.md",
            plugin_supports_fix=True,
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if not token.is_inline_code_span:
            return
        code_span_token = cast(InlineCodeSpanMarkdownToken, token)
        if len(code_span_token.span_text) == 1:
            has_leading = code_span_token.span_text[0] == " "
            has_trailing = False
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
            if context.in_fix_mode:
                adjusted_span_text = code_span_token.span_text
                if has_leading:
                    adjusted_span_text = adjusted_span_text[1:]
                if has_trailing:
                    adjusted_span_text = adjusted_span_text[:-1]
                self.register_fix_token_request(
                    context,
                    token,
                    "next_token",
                    "span_text",
                    adjusted_span_text,
                )
            else:
                self.report_next_token_error(context, token)
