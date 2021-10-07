"""
Module to implement a plugin that ensures that top-level lists are surrounded by Blank Lines.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd032(Plugin):
    """
    Class to implement a plugin that ensures that top-level lists are surrounded by Blank Lines.
    """

    def __init__(self):
        super().__init__()
        self.__last_non_end_token = None
        self.__container_token_stack = None
        self.__end_list_end_token = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="blanks-around-lists",
            plugin_id="MD032",
            plugin_enabled_by_default=True,
            plugin_description="Lists should be surrounded by blank lines",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md032.md",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__last_non_end_token = None
        self.__container_token_stack = []
        self.__end_list_end_token = None

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if self.__end_list_end_token:
            if (
                not token.is_blank_line
                and not token.is_new_list_item
                and not token.is_list_end
            ):
                self.report_next_token_error(context, token, line_number_delta=-1)
            self.__end_list_end_token = None

        if token.is_block_quote_start:
            self.__container_token_stack.append(token)
        elif token.is_block_quote_end:
            del self.__container_token_stack[-1]
        elif token.is_list_start:

            if (
                self.__last_non_end_token
                and not (
                    self.__container_token_stack
                    and self.__container_token_stack[-1].is_list_start
                )
                and not self.__last_non_end_token.is_blank_line
            ):
                self.report_next_token_error(context, token)

            self.__container_token_stack.append(token)
        elif token.is_list_end:
            if not self.__last_non_end_token.is_blank_line:
                self.__end_list_end_token = token
                del self.__container_token_stack[-1]

        if (
            not token.is_end_token
            and not token.is_block_quote_start
            and not token.is_list_start
        ):
            self.__last_non_end_token = token
