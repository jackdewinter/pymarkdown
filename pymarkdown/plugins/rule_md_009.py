"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager import Plugin, PluginDetails


# pylint: disable=too-many-instance-attributes
class RuleMd009(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def __init__(self):
        super().__init__()
        self.__leaf_tokens = None
        self.__leaf_owner_tokens = None
        self.__line_index = None
        self.__leaf_token_index = None
        self.__inline_token_index = None
        self.__container_token_stack = None
        self.__break_spaces = None
        self.__strict_mode = None
        self.__list_item_empty_lines_mode = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # whitespace
            plugin_name="no-trailing-spaces",
            plugin_id="MD009",
            plugin_enabled_by_default=True,
            plugin_description="Trailing spaces",
            plugin_version="0.5.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md007---unordered-list-indentation
        # Parameters: br_spaces, list_item_empty_lines, strict (number; default 2, boolean; default false, boolean; default false)

    @classmethod
    def __validate_break_spaces(cls, found_value):
        if found_value < 0:
            raise ValueError("Allowable values are greater than or equal to 0.")

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__break_spaces = self.plugin_configuration.get_integer_property(
            "br_spaces",
            default_value=2,
            valid_value_fn=self.__validate_break_spaces,
        )
        if self.__break_spaces < 2:
            self.__break_spaces = 0
        self.__strict_mode = self.plugin_configuration.get_boolean_property(
            "strict",
            default_value=False,
        )
        self.__list_item_empty_lines_mode = (
            self.plugin_configuration.get_boolean_property(
                "list_item_empty_lines",
                default_value=False,
            )
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__leaf_tokens = []
        self.__leaf_owner_tokens = []
        self.__line_index = 1
        self.__leaf_token_index = 0
        self.__inline_token_index = 0
        self.__container_token_stack = []

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """
        if (
            self.__leaf_token_index + 1 < len(self.__leaf_tokens)
            and self.__line_index
            == self.__leaf_tokens[self.__leaf_token_index + 1].line_number
            and self.__leaf_tokens[self.__leaf_token_index + 1].is_leaf
        ):
            self.__leaf_token_index = self.__inline_token_index + 1
            self.__inline_token_index = self.__leaf_token_index
        if (
            self.__inline_token_index + 1 < len(self.__leaf_tokens)
            and self.__line_index
            == self.__leaf_tokens[self.__inline_token_index + 1].line_number
        ):
            self.__inline_token_index += 1

        if (
            not self.__leaf_tokens[self.__leaf_token_index].is_code_block
            and line
            and line[-1] == " "
        ):

            (
                first_non_whitespace_index,
                extracted_whitespace,
            ) = ParserHelper.extract_whitespace_from_end(line)
            extracted_whitespace_length = len(extracted_whitespace)

            is_list_empty_line = (
                self.__list_item_empty_lines_mode
                and self.__leaf_owner_tokens[self.__leaf_token_index]
                and self.__leaf_owner_tokens[self.__leaf_token_index].is_list_start
                and first_non_whitespace_index == 0
            )

            if extracted_whitespace_length != self.__break_spaces or (
                self.__strict_mode and not is_list_empty_line
            ):

                if self.__strict_mode or self.__break_spaces < 2:
                    extra_error_information = "0"
                else:
                    extra_error_information = f"0 or {self.__break_spaces}"
                extra_error_information = f"Expected: {extra_error_information}; Actual: {extracted_whitespace_length}"
                self.report_next_line_error(
                    context,
                    first_non_whitespace_index + 1,
                    extra_error_information=extra_error_information,
                )

        self.__line_index += 1

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        _ = context

        if token.is_block_quote_start or token.is_list_start:
            self.__container_token_stack.append(token)
        elif token.is_block_quote_end or token.is_list_end:
            del self.__container_token_stack[-1]
        elif token.is_blank_line or token.is_leaf or token.is_inline_hard_break:
            self.__leaf_tokens.append(token)
            if self.__container_token_stack:
                self.__leaf_owner_tokens.append(self.__container_token_stack[-1])
            else:
                self.__leaf_owner_tokens.append(None)


# pylint: enable=too-many-instance-attributes
