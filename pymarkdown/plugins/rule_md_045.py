"""
Module to implement a plugin that looks for image elements that do not specify alternate text.
"""
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd045(RulePlugin):
    """
    Class to implement a plugin that looks for image elements that do not specify alternate text.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-alt-text",
            plugin_id="MD045",
            plugin_enabled_by_default=True,
            plugin_description="Images should have alternate text (alt text)",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md045.md",
        )

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_inline_image and not token.text_from_blocks.strip():
            self.report_next_token_error(context, token)
