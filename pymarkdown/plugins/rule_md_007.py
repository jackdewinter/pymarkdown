"""
Module to implement a plugin that ensures that nested Unordered List Items
start at predictable positions.
"""
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd007(RulePlugin):
    """
    Class to implement a plugin that ensures that nested Unordered List Items
    start at predictable positions.
    """

    def __init__(self):
        super().__init__()
        self.__container_token_stack = None
        self.__bq_line_index = None
        self.__last_leaf_token = None
        self.__indent_basis = None
        self.__start_indented = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="ul-indent",
            plugin_id="MD007",
            plugin_enabled_by_default=True,
            plugin_description="Unordered list indentation",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md007.md",
            plugin_configuration="indent,start_indented",
        )

    @classmethod
    def __validate_configuration_indent(cls, found_value):
        if found_value < 2 or found_value > 4:
            raise ValueError("Allowable values are between 2 and 4.")

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__indent_basis = self.plugin_configuration.get_integer_property(
            "indent",
            default_value=2,
            valid_value_fn=self.__validate_configuration_indent,
        )
        self.__start_indented = self.plugin_configuration.get_boolean_property(
            "start_indented",
            default_value=False,
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__container_token_stack = []

        self.__bq_line_index = {}
        self.__last_leaf_token = None

    @classmethod
    def __is_simple_delta(cls, token):
        return (
            token.is_blank_line
            or token.is_thematic_break
            or token.is_atx_heading
            or token.is_paragraph_end
        )

    @classmethod
    def __is_remember_leaf_token(cls, token):
        return (
            token.is_setext_heading
            or token.is_indented_code_block
            or token.is_html_block
        )

    @classmethod
    def __is_clear_leaf_token(cls, token):
        return (
            token.is_indented_code_block_end
            or token.is_html_block_end
            or token.is_setext_heading_end
            or token.is_fenced_code_block_end
        )

    def __manage_leaf_tokens(self, token):
        bq_delta = 0
        if self.__is_simple_delta(token):
            bq_delta = 1
        elif self.__is_remember_leaf_token(token):
            self.__last_leaf_token = token
        elif self.__is_clear_leaf_token(token):
            self.__last_leaf_token = None
            if token.is_setext_heading_end or token.is_fenced_code_block_end:
                bq_delta = 1
        elif token.is_fenced_code_block:
            bq_delta = 1
            self.__last_leaf_token = token
        elif token.is_paragraph:
            bq_delta = token.extracted_whitespace.count(ParserHelper.newline_character)
        elif token.is_link_reference_definition:
            bq_delta = (
                1
                + token.link_name_debug.count(ParserHelper.newline_character)
                + token.link_destination_whitespace.count(
                    ParserHelper.newline_character
                )
                + token.link_title_whitespace.count(ParserHelper.newline_character)
                + token.link_title_raw.count(ParserHelper.newline_character)
            )
        elif token.is_text and self.__last_leaf_token:
            if self.__last_leaf_token.is_setext_heading:
                bq_delta = (
                    token.end_whitespace.count(ParserHelper.newline_character) + 1
                )
            else:
                assert (
                    self.__last_leaf_token.is_html_block
                    or self.__last_leaf_token.is_code_block
                )
                bq_delta = token.token_text.count(ParserHelper.newline_character) + 1
        self.__bq_line_index[len(self.__container_token_stack)] += bq_delta

    def manage_container_tokens(self, token):
        """
        Manage the container tokens, especially the block quote indices.
        """
        if token.is_block_quote_start:
            self.__container_token_stack.append(token)
            self.__bq_line_index[len(self.__container_token_stack)] = 0
        elif token.is_block_quote_end:
            del self.__bq_line_index[len(self.__container_token_stack)]
            del self.__container_token_stack[-1]
        elif token.is_list_start:
            self.__container_token_stack.append(token)
        elif token.is_list_end:
            del self.__container_token_stack[-1]
        elif (
            self.__container_token_stack
            and self.__container_token_stack[-1].is_block_quote_start
        ):
            self.__manage_leaf_tokens(token)

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        # print(f">>>{token}".replace(ParserHelper.newline_character, "\\n"))
        if token.is_unordered_list_start or (
            token.is_new_list_item
            and self.__container_token_stack[-1].is_unordered_list_start
        ):
            self.__check(context, token)

        self.manage_container_tokens(token)

    def __calculate_base_column(self):
        container_base_column = 0
        block_quote_base = 0
        list_depth = 0
        if self.__container_token_stack:
            stack_index = len(self.__container_token_stack) - 1
            while stack_index >= 0:
                if not self.__container_token_stack[
                    stack_index
                ].is_unordered_list_start:
                    break
                list_depth += 1
                stack_index -= 1
            # print(f"stack_index={stack_index}")
            ignore_list_starts = False
            while stack_index >= 0:
                # print(f"stack_index>{stack_index}," + \
                #   f"token={self.__container_token_stack[t]}".replace(ParserHelper.newline_character, "\\n"))
                if self.__container_token_stack[stack_index].is_ordered_list_start:
                    if not ignore_list_starts:
                        container_base_column += self.__container_token_stack[
                            stack_index
                        ].indent_level
                    ignore_list_starts = True
                elif self.__container_token_stack[stack_index].is_block_quote_start:
                    bq_index = self.__bq_line_index[stack_index + 1]
                    split_leading_spaces = self.__container_token_stack[
                        stack_index
                    ].leading_spaces.split(ParserHelper.newline_character)
                    # print(f"bq_index={bq_index},split_leading_spaces={split_leading_spaces}")
                    # print(f"split_leading_spaces[bq_index]={split_leading_spaces[bq_index]}=")
                    if not block_quote_base:
                        block_quote_base = container_base_column + len(
                            split_leading_spaces[bq_index]
                        )
                    container_base_column += len(split_leading_spaces[bq_index])
                    ignore_list_starts = False
                # print(f"container_base_column>{container_base_column}")
                stack_index -= 1
        return container_base_column, block_quote_base, list_depth

    def __check(self, context, token):
        # print(f"{token}".replace(ParserHelper.newline_character, "\\n"))
        # print(f"{self.__container_token_stack}".replace(ParserHelper.newline_character, "\\n"))
        # print(f"{self.__bq_line_index}".replace(ParserHelper.newline_character, "\\n"))

        (
            container_base_column,
            block_quote_base,
            list_depth,
        ) = self.__calculate_base_column()
        if token.is_new_list_item:
            list_depth -= 1

        if self.__start_indented:
            list_depth += 1

        adjusted_column_number = token.column_number - 1 - container_base_column
        # print(f"adjusted_column_number={adjusted_column_number}")
        calculated_column_number = list_depth * self.__indent_basis
        # print(f"adjusted_column_number={adjusted_column_number}, calculated_column_number=" + \
        #   f"{calculated_column_number},block_quote_base={block_quote_base}")
        if adjusted_column_number != calculated_column_number:
            # print(f"container_base_column={container_base_column}")
            if block_quote_base:
                container_base_column -= block_quote_base
            elif container_base_column:
                container_base_column += 1
            extra_error_information = (
                f"Expected: {calculated_column_number+container_base_column}, "
                + f"Actual={adjusted_column_number+container_base_column}"
            )
            self.report_next_token_error(
                context, token, extra_error_information=extra_error_information
            )
