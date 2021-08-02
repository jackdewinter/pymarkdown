"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd038(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # whitespace, code
            plugin_name="no-space-in-code",
            plugin_id="MD038",
            plugin_enabled_by_default=True,
            plugin_description="Spaces inside code span elements",
            plugin_version="0.5.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md038---spaces-inside-code-span-elements

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_inline_code_span:
            has_trailing = False
            if len(token.span_text) == 1:
                has_leading = token.span_text[0] == " "
            else:
                has_leading = token.span_text[0] == " " and token.span_text[1] != "`"
                has_trailing = token.span_text[-1] == " " and token.span_text[-2] != "`"
            if has_leading != has_trailing or has_leading:
                self.report_next_token_error(context, token)
