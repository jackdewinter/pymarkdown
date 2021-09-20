"""
Module to implement a plugin that ensures that all Unordered List Items
start at the beginning of the line.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd006(Plugin):
    """
    Class to implement a plugin that ensures that all Unordered List Items
    start at the beginning of the line.
    """

    def __init__(self):
        super().__init__()
        self.__list_stack = None

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
        self.__list_stack = []

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_unordered_list_start or token.is_ordered_list_start:
            self.__list_stack.append(token)
            if (
                len(self.__list_stack) == 1
                and self.__list_stack[-1].is_unordered_list_start
                and self.__list_stack[-1].column_number != 1
            ):
                self.report_next_token_error(context, token)
        elif token.is_unordered_list_end or token.is_ordered_list_end:
            del self.__list_stack[-1]
        elif token.is_new_list_item:
            if (
                len(self.__list_stack) == 1
                and self.__list_stack[-1].is_unordered_list_start
                and token.column_number != 1
            ):
                self.report_next_token_error(context, token)
