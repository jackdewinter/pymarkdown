"""
Module to implement a plugin that ensures that specific proper names have
the correct capitalization.
"""
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_details import PluginDetails
from pymarkdown.rule_plugin import RulePlugin


class RuleMd044(RulePlugin):
    """
    Class to implement a plugin that ensures that specific proper names have
    the correct capitalization.
    """

    def __init__(self):
        super().__init__()
        self.__proper_name_list = None
        self.__check_in_code_blocks = None
        self.__is_in_code_block = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="proper-names",
            plugin_id="MD044",
            plugin_enabled_by_default=True,
            plugin_description="Proper names should have the correct capitalization",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md044.md",
            plugin_configuration="names,code_blocks",
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__is_in_code_block = False

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__check_in_code_blocks = self.plugin_configuration.get_boolean_property(
            "code_blocks", default_value=True
        )
        self.__proper_name_list = []
        names = self.plugin_configuration.get_string_property(
            "names",
            default_value="",
        ).strip()
        if names:
            lower_list = []
            for next_name in names.split(","):
                next_name = next_name.strip()
                if not next_name:
                    raise ValueError(
                        "Elements in the comma-separated list cannot be empty."
                    )
                if next_name.lower() in lower_list:
                    raise ValueError(
                        f"Element `{next_name}` is already present in the list as `{self.__proper_name_list[lower_list.index(next_name.lower())]}`."
                    )
                lower_list.append(next_name.lower())
                self.__proper_name_list.append(next_name)

    # pylint: disable=too-many-arguments
    def __check_for_proper_match(
        self,
        original_source,
        found_index,
        required_capitalization,
        context,
        token,
        line_adjust,
        col_adjust,
    ):

        original_found_text = original_source[
            found_index : found_index + len(required_capitalization)
        ]
        after_found_index = found_index + len(required_capitalization)

        is_character_before_match = False
        if found_index > 0:
            is_character_before_match = original_source[found_index - 1].isalnum()

        is_character_after_match = False
        if after_found_index < len(original_source):
            is_character_after_match = original_source[after_found_index].isalnum()

        if not is_character_after_match and not is_character_before_match:
            assert len(original_found_text) == len(required_capitalization)
            if original_found_text != required_capitalization:
                extra_data = f"Expected: {required_capitalization}; Actual: {original_found_text}"
                self.report_next_token_error(
                    context,
                    token,
                    extra_error_information=extra_data,
                    line_number_delta=line_adjust,
                    column_number_delta=col_adjust,
                )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __search_for_matches(
        self,
        string_to_check,
        context,
        token,
        same_line_offset=0,
        start_x_offset=0,
        start_y_offset=0,
    ):

        string_to_check = ParserHelper.remove_all_from_text(string_to_check)
        string_to_check_lower = string_to_check.lower()
        for next_name in self.__proper_name_list:
            next_name_lower = next_name.lower()
            search_start = 0
            found_index = string_to_check_lower.find(next_name_lower, search_start)
            while found_index != -1:
                col_adjust, line_adjust = ParserHelper.adjust_for_newlines(
                    string_to_check_lower, search_start, found_index
                )
                if line_adjust == 0 and start_y_offset == 0:
                    col_adjust -= same_line_offset
                line_adjust += start_y_offset
                if col_adjust == 0 and start_x_offset:
                    col_adjust += (
                        -start_x_offset
                        if start_x_offset > 0
                        else -(-start_x_offset - 1)
                    )
                    col_adjust = -col_adjust
                elif col_adjust > 0 and start_x_offset:
                    col_adjust += -start_x_offset - 1
                    col_adjust = -col_adjust
                self.__check_for_proper_match(
                    string_to_check,
                    found_index,
                    next_name,
                    context,
                    token,
                    line_adjust,
                    col_adjust,
                )

                search_start = found_index + len(next_name)
                found_index = string_to_check_lower.find(next_name_lower, search_start)

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __adjust_for_newlines_and_search(
        self,
        context,
        token,
        link_body_text,
        full_link_text,
        string_to_check,
        same_line_offset,
    ):

        start_x_offset = 0
        start_y_offset = 0
        if "\n" in link_body_text:
            start_x_offset, start_y_offset = ParserHelper.adjust_for_newlines(
                full_link_text, 0, len(full_link_text)
            )
        self.__search_for_matches(
            string_to_check,
            context,
            token,
            same_line_offset,
            start_x_offset,
            start_y_offset,
        )

    # pylint: enable=too-many-arguments

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if not self.__proper_name_list:
            return
        if token.is_text:
            if not self.__is_in_code_block or self.__check_in_code_blocks:
                self.__search_for_matches(token.token_text, context, token)
        elif token.is_inline_code_span:
            same_line_offset = len(token.extracted_start_backticks) + len(
                token.leading_whitespace
            )
            self.__search_for_matches(token.span_text, context, token, same_line_offset)
        elif token.is_inline_link_end:
            if token.start_markdown_token.label_type == "inline":
                link_body = "".join(
                    [
                        token.start_markdown_token.before_link_whitespace,
                        token.start_markdown_token.active_link_uri,
                        token.start_markdown_token.before_title_whitespace,
                        token.start_markdown_token.inline_title_bounding_character,
                    ]
                )
                full_link_text = "".join(
                    [
                        "[",
                        token.start_markdown_token.text_from_blocks,
                        "](",
                        link_body,
                    ]
                )
                same_line_offset = len(full_link_text) + 1
                self.__adjust_for_newlines_and_search(
                    context,
                    token.start_markdown_token,
                    link_body,
                    full_link_text,
                    token.start_markdown_token.active_link_title,
                    same_line_offset,
                )
        elif token.is_inline_image:
            same_line_offset = -2
            self.__search_for_matches(
                token.text_from_blocks, context, token, same_line_offset
            )

            if token.label_type == "inline":
                link_body = "".join(
                    [
                        token.before_link_whitespace,
                        token.active_link_uri,
                        token.before_title_whitespace,
                        token.inline_title_bounding_character,
                    ]
                )
                full_link_text = f"![{token.text_from_blocks}]({link_body}"
                same_line_offset = len(full_link_text) + 1
                self.__adjust_for_newlines_and_search(
                    context,
                    token,
                    link_body,
                    full_link_text,
                    token.active_link_title,
                    same_line_offset,
                )
        elif token.is_link_reference_definition:
            link_name = token.link_name_debug or token.link_name
            same_line_offset = -1
            self.__search_for_matches(link_name, context, token, same_line_offset)

            full_link_text = "".join(
                [
                    "[",
                    link_name,
                    "]:",
                    token.link_destination_whitespace,
                    token.link_destination,
                    token.link_title_whitespace,
                    "'",
                ]
            )
            same_line_offset = -(len(full_link_text) - 1)
            self.__adjust_for_newlines_and_search(
                context,
                token,
                full_link_text,
                full_link_text,
                token.link_title_raw,
                same_line_offset,
            )
        elif token.is_code_block:
            self.__is_in_code_block = True
        elif token.is_code_block_end:
            self.__is_in_code_block = False
