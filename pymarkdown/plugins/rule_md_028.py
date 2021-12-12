"""
Module to implement a plugin that ensures that Block Quote elements are surrounded by Blank Lines.
"""
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd028(RulePlugin):
    """
    Class to implement a plugin that ensures that Block Quote elements are surrounded by Blank Lines.
    """

    __look_for_end_of_block_quote = 0
    __look_for_blank_lines = 1
    __look_for_start_of_block_quote = 2

    def __init__(self):
        super().__init__()
        self.__current_state = None
        self.__found_blank_lines = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-blanks-blockquote",
            plugin_id="MD028",
            plugin_enabled_by_default=True,
            plugin_description="Blank line inside blockquote",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md028.md",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__current_state = RuleMd028.__look_for_end_of_block_quote
        self.__found_blank_lines = None

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        # print(str(self.__current_state) + "--" + str(token).replace(ParserHelper.newline_character, "\\n"))
        if self.__current_state == RuleMd028.__look_for_end_of_block_quote:
            if token.is_block_quote_end:
                self.__current_state = RuleMd028.__look_for_blank_lines
                self.__found_blank_lines = []
        elif self.__current_state == RuleMd028.__look_for_blank_lines:
            if token.is_blank_line:
                self.__current_state = RuleMd028.__look_for_start_of_block_quote
                self.__found_blank_lines.append(token)
            elif not token.is_block_quote_end:
                self.__current_state = RuleMd028.__look_for_end_of_block_quote
        else:
            assert self.__current_state == RuleMd028.__look_for_start_of_block_quote
            if token.is_block_quote_start:
                for next_blank_lines in self.__found_blank_lines:
                    self.report_next_token_error(context, next_blank_lines)
                self.__current_state = RuleMd028.__look_for_end_of_block_quote
            elif token.is_blank_line:
                self.__found_blank_lines.append(token)
            else:
                self.__current_state = RuleMd028.__look_for_end_of_block_quote
