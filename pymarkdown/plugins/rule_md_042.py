"""
Module to implement a plugin that looks for inline links with empty link URIs.
"""
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd042(RulePlugin):
    """
    Class to implement a plugin that looks for inline links with empty link URIs.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-empty-links",
            plugin_id="MD042",
            plugin_enabled_by_default=True,
            plugin_description="No empty links",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md042.md",
        )

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_inline_link or token.is_inline_image:
            stripped_link_uri = token.active_link_uri.strip()
            if not stripped_link_uri or stripped_link_uri == "#":
                self.report_next_token_error(context, token)
