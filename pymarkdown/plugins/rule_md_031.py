"""
Module to implement a plugin that ensures that blank lines surround fenced block quotes.
"""
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd031(RulePlugin):
    """
    Class to implement a plugin that ensures that blank lines surround fenced block quotes.
    """

    def __init__(self):
        super().__init__()
        self.__trigger_in_list_items = None
        self.__end_fenced_code_block_token = None
        self.__last_non_end_token = None
        self.__container_token_stack = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="blanks-around-fences",
            plugin_id="MD031",
            plugin_enabled_by_default=True,
            plugin_description="Fenced code blocks should be surrounded by blank lines",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md031.md",
            plugin_configuration="list_items",
        )

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__trigger_in_list_items = self.plugin_configuration.get_boolean_property(
            "list_items", default_value=True
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_non_end_token = None
        self.__end_fenced_code_block_token = None
        self.__container_token_stack = []

    def __handle_fenced_code_block(self, context, token):
        can_trigger = True
        if (
            self.__container_token_stack
            and self.__container_token_stack[-1].is_list_start
        ):
            can_trigger = self.__trigger_in_list_items
        if (
            self.__last_non_end_token
            and not self.__last_non_end_token.is_blank_line
            and can_trigger
        ):
            self.report_next_token_error(context, token)

    def __handle_end_fenced_code_block(self, context, token):
        can_trigger = True
        if (
            self.__container_token_stack
            and self.__container_token_stack[-1].is_list_start
        ):
            can_trigger = self.__trigger_in_list_items
        if not token.is_blank_line and can_trigger:
            line_number_delta = (
                self.__last_non_end_token.token_text.count(
                    ParserHelper.newline_character
                )
                + 2
            )
            column_number_delta = (
                self.__end_fenced_code_block_token.start_markdown_token.column_number
            )
            if (
                self.__end_fenced_code_block_token.start_markdown_token.extracted_whitespace
            ):
                column_number_delta -= len(
                    self.__end_fenced_code_block_token.start_markdown_token.extracted_whitespace
                )
            if self.__end_fenced_code_block_token.extracted_whitespace:
                column_number_delta += len(
                    self.__end_fenced_code_block_token.extracted_whitespace
                )
            column_number_delta = -(column_number_delta)
            self.report_next_token_error(
                context,
                self.__end_fenced_code_block_token.start_markdown_token,
                line_number_delta=line_number_delta,
                column_number_delta=column_number_delta,
            )
        self.__end_fenced_code_block_token = None

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if self.__end_fenced_code_block_token and not token.is_end_token:
            self.__handle_end_fenced_code_block(context, token)

        if token.is_block_quote_start:
            self.__container_token_stack.append(token)
        elif token.is_block_quote_end:
            del self.__container_token_stack[-1]
        elif token.is_list_start:
            self.__container_token_stack.append(token)
        elif token.is_list_end:
            del self.__container_token_stack[-1]
        elif token.is_fenced_code_block:
            self.__handle_fenced_code_block(context, token)
        elif token.is_fenced_code_block_end:
            self.__end_fenced_code_block_token = token

        if (
            not token.is_end_token
            and not token.is_block_quote_start
            and not token.is_list_start
        ):
            self.__last_non_end_token = token
