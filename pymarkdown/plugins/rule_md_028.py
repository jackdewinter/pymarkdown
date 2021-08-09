"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd028(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
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
            # blockquote, whitespace
            plugin_name="no-blanks-blockquote",
            plugin_id="MD028",
            plugin_enabled_by_default=True,
            plugin_description="Blank line inside blockquote",
            plugin_version="0.5.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md028---blank-line-inside-blockquote

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
        # print(str(self.__current_state) + "--" + str(token).replace("\n", "\\n"))
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
