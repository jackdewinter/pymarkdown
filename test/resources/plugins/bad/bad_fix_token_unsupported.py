from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken, MarkdownTokenClass


class NotSupportedToken(MarkdownToken):
    """
    Token that is not supported and for testing purposes only.
    """

    def __init__(self) -> None:
        MarkdownToken.__init__(
            self,
            "unsupported",
            MarkdownTokenClass.SPECIAL,
        )


class BadFixTokenUnsupported(RulePlugin):
    """
    Class to implement a sample
    """

    def __init__(self):
        self.__have_fired = False

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
        if not self.__have_fired:
            self.register_fix_token_request(
                context, NotSupportedToken(), "next_token", "hash_count", 2
            )
            self.__have_fired = True
