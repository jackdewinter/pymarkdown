"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd040(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # code, language
            plugin_name="fenced-code-language",
            plugin_id="MD040",
            plugin_enabled_by_default=True,
            plugin_description="Fenced code blocks should have a language specified",
            plugin_version="0.5.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md040---fenced-code-blocks-should-have-a-language-specified

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_fenced_code_block:
            if not token.extracted_text.strip():
                self.report_next_token_error(context, token)
