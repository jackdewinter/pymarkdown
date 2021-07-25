"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd005(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def __init__(self):
        super().__init__()
        self.__list_stack = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # bullet, ul, indentation
            plugin_name="list-indent",
            plugin_id="MD005",
            plugin_enabled_by_default=True,
            plugin_description="Inconsistent indentation for list items at the same level",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md005.md",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md005---inconsistent-indentation-for-list-items-at-the-same-level

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
        elif token.is_unordered_list_end or token.is_ordered_list_end:
            del self.__list_stack[-1]
        elif token.is_new_list_item:
            if self.__list_stack[-1].is_unordered_list_start:
                if self.__list_stack[-1].indent_level != token.indent_level:
                    self.report_next_token_error(context, token)
            elif self.__list_stack[-1].column_number != token.column_number:
                original_text = self.__list_stack[-1].list_start_content
                if self.__list_stack[-1].extracted_whitespace:
                    original_text += self.__list_stack[-1].extracted_whitespace
                original_text_length = len(original_text)
                current_prefix_length = len(
                    token.list_start_content + token.extracted_whitespace
                )
                if original_text_length == current_prefix_length:
                    assert token.indent_level == self.__list_stack[-1].indent_level
                else:
                    self.report_next_token_error(context, token)
