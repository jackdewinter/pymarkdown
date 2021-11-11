"""
Module to implement a plugin that looks for multiple spaces after the hash
mark on an atx heading.
"""
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd019(RulePlugin):
    """
    Class to implement a plugin that looks for multiple spaces after the hash
    mark on an atx heading.
    """

    def __init__(self):
        super().__init__()
        self.__atx_heading_token = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-multiple-space-atx",
            plugin_id="MD019",
            plugin_enabled_by_default=True,
            plugin_description="Multiple spaces are present after hash character on Atx Heading.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md019.md",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__atx_heading_token = None

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_atx_heading:
            if not token.remove_trailing_count:
                self.__atx_heading_token = token
        elif token.is_paragraph_end:
            self.__atx_heading_token = None
        elif token.is_text:
            resolved_extracted_whitespace = ParserHelper.remove_all_from_text(
                token.extracted_whitespace
            )
            if self.__atx_heading_token and len(resolved_extracted_whitespace) > 1:
                self.report_next_token_error(context, self.__atx_heading_token)
