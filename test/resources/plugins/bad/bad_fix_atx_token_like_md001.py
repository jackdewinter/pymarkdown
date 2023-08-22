from typing import cast

from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class BadFixAtxTokenLikeMd001(RulePlugin):
    """
    Class to implement a sample
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="bad-xxx",
            plugin_id="MDE003",
            plugin_enabled_by_default=True,
            plugin_description="Plugin that.",
            plugin_version="0.0.0",
            plugin_supports_fix=True,
        )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        if token.is_atx_heading:
            heading_token = cast(AtxHeadingMarkdownToken, token)
            if context.in_fix_mode and heading_token.hash_count == 3:
                self.register_fix_token_request(
                    context, token, "next_token", "hash_count", 2
                )
