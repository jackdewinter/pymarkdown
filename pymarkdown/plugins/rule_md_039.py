"""
Module to implement a plugin that looks for spaces within link labels.
"""

from typing import cast

from pymarkdown.general.constants import Constants
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.link_reference_definition_markdown_token import (
    LinkReferenceDefinitionMarkdownToken,
)
from pymarkdown.tokens.link_start_markdown_token import LinkStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RuleMd039(RulePlugin):
    """
    Class to implement a plugin that looks for spaces within link labels.
    """

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="no-space-in-links",
            plugin_id="MD039",
            plugin_enabled_by_default=True,
            plugin_description="Spaces inside link text",
            plugin_version="0.5.2",
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md039.md",
            plugin_supports_fix=True,
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_inline_link or token.is_inline_image:
            link_token = cast(LinkStartMarkdownToken, token)
            stripped_text_from_blocks = link_token.text_from_blocks.strip(
                Constants.ascii_whitespace
            )
            if link_token.text_from_blocks != stripped_text_from_blocks:
                if context.in_fix_mode:
                    self.register_fix_token_request(
                        context,
                        token,
                        "next_token",
                        "text_from_blocks",
                        stripped_text_from_blocks,
                    )
                else:
                    self.report_next_token_error(context, token)
        elif token.is_link_reference_definition:
            link_def_token = cast(LinkReferenceDefinitionMarkdownToken, token)
            assert link_def_token.link_name_debug is not None
            stripped_text_from_blocks = link_def_token.link_name_debug.strip(
                Constants.ascii_whitespace
            )
            if link_def_token.link_name_debug != stripped_text_from_blocks:
                if context.in_fix_mode:
                    self.register_fix_token_request(
                        context,
                        token,
                        "next_token",
                        "link_name_debug",
                        stripped_text_from_blocks,
                    )
                else:
                    self.report_next_token_error(context, token)
