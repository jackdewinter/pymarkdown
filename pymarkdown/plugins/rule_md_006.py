"""
Module to implement a plugin that ensures that all Unordered List Items
start at the beginning of the line.
"""
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd006(RulePlugin):
    """
    Class to implement a plugin that ensures that all Unordered List Items
    start at the beginning of the line.
    """

    def __init__(self):
        super().__init__()
        self.__token_stack = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="ul-start-left",
            plugin_id="MD006",
            plugin_enabled_by_default=False,
            plugin_description="Consider starting bulleted lists at the beginning of the line",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md006.md",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__token_stack = []

    def __calculate_expected_indent(self):
        expected_indent = 0
        if len(self.__token_stack) > 1:
            if self.__token_stack[-2].is_block_quote_start:
                split_spaces = self.__token_stack[-2].leading_spaces.split(
                    ParserHelper.newline_character
                )
                expected_indent = len(split_spaces[0]) + (
                    self.__token_stack[-2].column_number - 1
                )
            else:
                expected_indent = self.__token_stack[-2].indent_level
        return expected_indent

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_list_start or token.is_block_quote_start:
            self.__token_stack.append(token)
            if token.is_unordered_list_start:
                expected_indent = self.__calculate_expected_indent()
                if token.column_number != (1 + expected_indent):
                    self.report_next_token_error(context, token)
        elif token.is_list_end or token.is_block_quote_end:
            del self.__token_stack[-1]
        elif token.is_new_list_item:
            if self.__token_stack[-1].is_unordered_list_start:
                expected_indent = self.__calculate_expected_indent()
                if token.column_number != (1 + expected_indent):
                    self.report_next_token_error(context, token)
