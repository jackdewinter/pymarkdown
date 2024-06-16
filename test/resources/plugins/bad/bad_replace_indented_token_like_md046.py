from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken


class BadReplaceIndentedTokenLikeMd046(RulePlugin):
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
        if token.is_indented_code_block and context.in_fix_mode:
            self.register_replace_tokens_request(context, token, token, [token])
