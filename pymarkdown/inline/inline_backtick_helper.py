"""
Module to help with the parsing of bkactick inline elements.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.inline.inline_helper import InlineHelper
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.inline.inline_response import InlineResponse
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class InlineBacktickHelper:
    """
    Class to help with the parsing of bkactick inline elements.
    """

    code_span_bounds = "`"

    @staticmethod
    def handle_inline_backtick(
        parser_properties: ParseBlockPassProperties, inline_request: InlineRequest
    ) -> InlineResponse:
        """
        Handle the inline case of backticks for code spans.
        """
        _ = parser_properties

        POGGER.debug("before_collect>$", inline_request.next_index)
        POGGER.debug("inline_request.source_text>:$:<", inline_request.source_text)
        POGGER.debug("inline_request.tabified_text>:$:<", inline_request.tabified_text)
        (
            new_index,
            extracted_start_backticks,
        ) = ParserHelper.collect_while_one_of_characters_verified(
            inline_request.source_text,
            inline_request.next_index,
            InlineBacktickHelper.code_span_bounds,
        )
        POGGER.debug("after_collect>$>$", new_index, extracted_start_backticks)

        extracted_start_backticks_size, end_backtick_start_index = (
            len(extracted_start_backticks),
            inline_request.source_text.find(extracted_start_backticks, new_index),
        )
        while end_backtick_start_index != -1:
            (
                end_backticks_index,
                end_backticks_attempt,
            ) = ParserHelper.collect_while_one_of_characters_verified(
                inline_request.source_text,
                end_backtick_start_index,
                InlineBacktickHelper.code_span_bounds,
            )
            if len(end_backticks_attempt) == extracted_start_backticks_size:
                break
            end_backtick_start_index = inline_request.source_text.find(
                extracted_start_backticks, end_backticks_index
            )

        inline_response = InlineBacktickHelper.__build_backtick_response(
            inline_request,
            end_backtick_start_index,
            extracted_start_backticks,
            new_index,
            extracted_start_backticks_size,
        )

        assert (
            inline_response.new_index is not None
        ), "new_index should be defined by this point."
        POGGER.debug(
            ">>delta_line_number>>$<<",
            inline_response.delta_line_number,
        )
        POGGER.debug(
            ">>delta_column_number>>$<<",
            inline_response.delta_column_number,
        )
        if inline_response.delta_line_number == -1:
            inline_response.delta_line_number, inline_response.delta_column_number = (
                0,
                inline_response.new_index - inline_request.next_index,
            )
        return inline_response

    @staticmethod
    def __build_backtick_response(
        inline_request: InlineRequest,
        end_backtick_start_index: int,
        extracted_start_backticks: str,
        new_index: int,
        extracted_start_backticks_size: int,
    ) -> InlineResponse:
        inline_response = InlineResponse()
        inline_response.delta_line_number = -1

        if end_backtick_start_index == -1:
            inline_response.new_string, inline_response.new_index = (
                extracted_start_backticks,
                new_index,
            )
        else:
            (
                between_text,
                original_between_text,
                leading_whitespace,
                trailing_whitespace,
                inline_response.adj_newlines,
            ) = InlineBacktickHelper.__calculate_backtick_between_text(
                inline_request, new_index, end_backtick_start_index
            )

            POGGER.debug("between_text>>$<<", between_text)
            between_text = InlineHelper.append_text("", between_text)
            POGGER.debug("between_text>>$<<", between_text)
            POGGER.debug(
                "leading_whitespace>>$<<",
                leading_whitespace,
            )
            POGGER.debug(
                "trailing_whitespace>>$<<",
                trailing_whitespace,
            )
            end_backtick_start_index += extracted_start_backticks_size
            inline_response.new_string, inline_response.new_index = (
                "",
                end_backtick_start_index,
            )
            assert (
                inline_request.line_number is not None
            ), "line_number must be defined by now."
            assert (
                inline_request.column_number is not None
            ), "column_number must be defined by now."
            assert (
                inline_request.remaining_line is not None
            ), "remaining_line must be defined by now."
            new_column_number = inline_request.column_number + len(
                inline_request.remaining_line
            )
            POGGER.debug(">>new_column_number>>$", new_column_number)

            inline_response.new_tokens = [
                InlineCodeSpanMarkdownToken(
                    between_text,
                    extracted_start_backticks,
                    leading_whitespace,
                    trailing_whitespace,
                    inline_request.is_in_table,
                    inline_request.line_number,
                    new_column_number,
                )
            ]

            if ParserHelper.newline_character in original_between_text:
                (
                    inline_response.delta_line_number,
                    inline_response.delta_column_number,
                ) = ParserHelper.calculate_deltas(
                    f"{original_between_text}{extracted_start_backticks}"
                )
        return inline_response

    @staticmethod
    def __backtick_split_lines(input_string: str) -> List[str]:
        current_index = 0
        next_index, extracted_text = (
            ParserHelper.collect_while_one_of_characters_verified(
                input_string, current_index, " \t"
            )
        )
        split_array: List[str] = [extracted_text]
        # POGGER.debug("next_index:$, extracted_text>:$:<", next_index, extracted_text)
        while next_index < len(input_string):
            (
                current_index,
                extracted_text,
            ) = ParserHelper.collect_until_one_of_characters_verified(
                input_string, next_index, " \t"
            )
            split_array.append(extracted_text)
            next_index, extracted_text = (
                ParserHelper.collect_while_one_of_characters_verified(
                    input_string, current_index, " \t"
                )
            )
            split_array.append(extracted_text)
        return split_array

    @staticmethod
    def __adjust_for_injected_noops(between_text: str) -> str:

        prefix = (
            ParserHelper.escape_character
            + "\a"
            + ParserHelper.escape_character
            + ParserHelper.replace_noop_character
            + ParserHelper.escape_character
            + "\a"
        )
        suffix = ParserHelper.escape_character + "\a"
        start_index = 0
        search_index = between_text.find(prefix, start_index)
        if search_index != -1:
            string_parts = []
            while search_index != -1:
                string_parts.append(between_text[start_index:search_index])
                search_index += len(prefix)
                end_index = between_text.find(suffix, search_index)
                in_between_text = between_text[search_index:end_index]
                string_parts.append(
                    ParserHelper.create_replacement_markers(
                        ParserHelper.replace_noop_character, in_between_text
                    )
                )
                start_index = end_index + len(suffix)
                search_index = between_text.find(prefix, start_index)
            if start_index != len(between_text):
                string_parts.append(between_text[start_index:])
            between_text = "".join(string_parts)
        return between_text

    @staticmethod
    def __calculate_backtick_between_text(
        inline_request: InlineRequest, new_index: int, end_backtick_start_index: int
    ) -> Tuple[str, str, str, str, int]:
        POGGER.debug("inline_request.source_text>>$<<", inline_request.source_text)
        POGGER.debug("new_index>>$<<", new_index)
        POGGER.debug("end_backtick_start_index>>$<<", end_backtick_start_index)

        between_text = inline_request.source_text[new_index:end_backtick_start_index]

        original_between_text, leading_whitespace, trailing_whitespace = (
            between_text,
            "",
            "",
        )

        if inline_request.tabified_text:
            between_text, adj_newlines = (
                InlineBacktickHelper.__calculate_backtick_between_tabified_text(
                    inline_request, new_index, end_backtick_start_index
                )
            )
        else:
            adj_newlines = 0
        POGGER.debug(
            "after_collect>$>>$>>$<<",
            between_text,
            end_backtick_start_index,
            inline_request.source_text[end_backtick_start_index:],
        )
        POGGER.debug("between_text>>$<<", between_text)
        if (
            len(between_text) > 2
            and between_text[0]
            in [
                ParserHelper.space_character,
                ParserHelper.newline_character,
            ]
            and between_text[-1]
            in [
                ParserHelper.space_character,
                ParserHelper.newline_character,
            ]
        ):
            stripped_between_attempt = between_text[1:-1]
            if len(stripped_between_attempt.strip(" ")) != 0:
                leading_whitespace, trailing_whitespace = (
                    between_text[0],
                    between_text[-1],
                )
                between_text = stripped_between_attempt

        replaced_newline = ParserHelper.create_replacement_markers(
            ParserHelper.newline_character, ParserHelper.space_character
        )
        POGGER.debug("between_text>>$<<", between_text)
        between_text = ParserHelper.escape_special_characters(between_text)
        POGGER.debug("between_text>>$<<", between_text)
        POGGER.debug(
            "leading_whitespace>>$<<",
            leading_whitespace,
        )
        POGGER.debug(
            "trailing_whitespace>>$<<",
            trailing_whitespace,
        )

        between_text = InlineBacktickHelper.__adjust_for_injected_noops(between_text)

        between_text, leading_whitespace, trailing_whitespace = (
            between_text.replace(ParserHelper.newline_character, replaced_newline),
            leading_whitespace.replace(
                ParserHelper.newline_character, replaced_newline
            ),
            trailing_whitespace.replace(
                ParserHelper.newline_character, replaced_newline
            ),
        )
        return (
            between_text,
            original_between_text,
            leading_whitespace,
            trailing_whitespace,
            adj_newlines,
        )

    @staticmethod
    def __find_adjusted_index(
        source_text: str, new_index: int, adj_tabified_text: str, whitespace_to_add: str
    ) -> Tuple[int, int]:

        before_index_text = source_text[:new_index]
        # w2 = source_text[new_index:]
        before_index_newline_count = ParserHelper.count_newlines_in_text(
            before_index_text
        )
        if before_index_newline_count:
            last_newline_index = source_text.rindex("\n", 0, new_index) + 1
            adj_new_index = new_index - last_newline_index
        else:
            last_newline_index = 0
            adj_new_index = new_index

        # q4 = source_text.find("\n", last_newline_index)
        # if q4 == -1:
        #     q4 = len(source_text)
        # st_after_newline = source_text[last_newline_index:q4]

        tabified_start_index = (
            ParserHelper.find_nth_occurrence(
                adj_tabified_text, "\n", before_index_newline_count
            )
            + 1
        )
        # tabified_end_index = adj_tabified_text.find("\n", tabified_start_index)
        # if tabified_end_index == -1:
        #     tabified_end_index = len(adj_tabified_text)
        # tt_after_newline = adj_tabified_text[q2:q3]

        whitespace_start_index = (
            ParserHelper.find_nth_occurrence(
                whitespace_to_add, "\n", before_index_newline_count
            )
            + 1
        )
        whitespace_end_index = whitespace_to_add.find("\n", whitespace_start_index)
        if whitespace_end_index == -1:
            whitespace_end_index = len(adj_tabified_text)
        whitespace_after_newline = whitespace_to_add[
            whitespace_start_index:whitespace_end_index
        ]
        return (
            tabified_start_index + len(whitespace_after_newline) + adj_new_index,
            before_index_newline_count,
        )

    @staticmethod
    def __calc_tabified_text(
        inline_request: InlineRequest, new_index: int, end_backtick_start_index: int
    ) -> Tuple[Optional[str], Optional[str], bool, int]:
        adj_newlines = 0
        adj_tabified_text = inline_request.tabified_text
        normal_backtick_text = inline_request.source_text[
            new_index:end_backtick_start_index
        ]
        whitespace_to_add = inline_request.whitespace_to_recombine
        did_use_para_space = False
        if (
            "\n" in normal_backtick_text
            and inline_request.para_space
            and whitespace_to_add is None
        ):
            did_use_para_space = True
            whitespace_to_add = inline_request.para_space
        if "\n" in normal_backtick_text and whitespace_to_add is not None:
            assert adj_tabified_text is not None
            adj_tabified_text_newlines = ParserHelper.count_newlines_in_text(
                adj_tabified_text
            )
            whitespace_to_add_newlines = ParserHelper.count_newlines_in_text(
                whitespace_to_add
            )
            assert adj_tabified_text_newlines == whitespace_to_add_newlines

            split_adj_tabified_text = adj_tabified_text.split("\n")
            split_whitespace_to_add = whitespace_to_add.split("\n")
            for split_index, split_item in enumerate(split_adj_tabified_text):
                ffff = split_whitespace_to_add[split_index].startswith(
                    " "
                ) and split_whitespace_to_add[split_index].endswith("\t")
                split_whitespace_to_add[split_index] = (
                    split_item
                    if ffff
                    else split_whitespace_to_add[split_index] + split_item
                )
            adj_tabified_text = "\n".join(split_whitespace_to_add)
            adj_newlines = ParserHelper.count_newlines_in_text(normal_backtick_text)
        return adj_tabified_text, whitespace_to_add, did_use_para_space, adj_newlines

    @staticmethod
    def __calc_adjusted_between_text_kludge(
        inline_request: InlineRequest,
        actual_between_text: str,
        whitespace_to_add: str,
        start_line_index: int,
        end_line_index: int,
    ) -> str:
        assert inline_request.last_container_token is not None
        if inline_request.last_container_token.is_block_quote_start:
            last_block_token = cast(
                BlockQuoteMarkdownToken, inline_request.last_container_token
            )
            assert last_block_token.bleading_spaces is not None
            split_spaces = last_block_token.bleading_spaces.split("\n")
        else:
            last_list_token = cast(
                ListStartMarkdownToken, inline_request.last_container_token
            )
            assert last_list_token.leading_spaces is not None
            split_spaces = last_list_token.leading_spaces.split("\n")
        split_whitespace = whitespace_to_add.split("\n")
        # assert len(er1) == len(er2)
        for index, split_whitespace_item in enumerate(split_whitespace):
            split_spaces_item = split_spaces[index]
            if (
                split_whitespace_item == "\t"
                and not split_spaces_item
                and index > start_line_index
                and index <= end_line_index
            ):
                newline_index = (
                    ParserHelper.find_nth_occurrence(
                        actual_between_text, "\n", index - start_line_index
                    )
                    + 1
                )
                prefix = actual_between_text[:newline_index]
                suffix = actual_between_text[newline_index + 1 :]
                noop_part = ParserHelper.create_replacement_markers(
                    ParserHelper.replace_noop_character, "\t"
                )
                actual_between_text = prefix + noop_part + suffix
        return actual_between_text

    @staticmethod
    def __calc_adjusted_between_text(
        adj_newlines: int,
        inline_request: InlineRequest,
        start_index: int,
        adj_tabified_text: str,
        whitespace_to_add: str,
        end_backtick_start_index: int,
        did_use_para_space: bool,
    ) -> Tuple[str, int]:
        adj_start_index, start_line_index = InlineBacktickHelper.__find_adjusted_index(
            inline_request.source_text,
            start_index,
            adj_tabified_text,
            whitespace_to_add,
        )
        adj_end_index, end_line_index = InlineBacktickHelper.__find_adjusted_index(
            inline_request.source_text,
            end_backtick_start_index,
            adj_tabified_text,
            whitespace_to_add,
        )
        actual_between_text = adj_tabified_text[adj_start_index:adj_end_index]
        if did_use_para_space and inline_request.last_container_token:
            actual_between_text = (
                InlineBacktickHelper.__calc_adjusted_between_text_kludge(
                    inline_request,
                    actual_between_text,
                    whitespace_to_add,
                    start_line_index,
                    end_line_index,
                )
            )
        return actual_between_text, adj_newlines

    @staticmethod
    def __calculate_backtick_between_tabified_text(
        inline_request: InlineRequest, new_index: int, end_backtick_start_index: int
    ) -> Tuple[str, int]:
        POGGER.debug("inline_request.tabified_text>>$<<", inline_request.tabified_text)
        split_source_lines = InlineBacktickHelper.__backtick_split_lines(
            inline_request.source_text
        )
        POGGER.debug("split_source_lines>>$<<", split_source_lines)
        assert (
            inline_request.tabified_text is not None
        ), "tabified_text must be defined by now."
        adj_tabified_text, whitespace_to_add, did_use_para_space, adj_newlines = (
            InlineBacktickHelper.__calc_tabified_text(
                inline_request, new_index, end_backtick_start_index
            )
        )
        assert adj_tabified_text is not None
        split_tabified_lines = InlineBacktickHelper.__backtick_split_lines(
            adj_tabified_text
        )
        if len(split_tabified_lines) != len(split_source_lines):
            assert whitespace_to_add is not None
            return InlineBacktickHelper.__calc_adjusted_between_text(
                adj_newlines,
                inline_request,
                new_index,
                adj_tabified_text,
                whitespace_to_add,
                end_backtick_start_index,
                did_use_para_space,
            )

        POGGER.debug("split_tabified_lines>>$<<", split_tabified_lines)

        (
            start_array_index,
            start_delta,
            calculated_index,
        ) = InlineBacktickHelper.__find_index_in_split_lines(
            split_source_lines, new_index
        )
        POGGER.debug(
            "start_array_index=$, start_delta=$, calculated_index=$",
            start_array_index,
            start_delta,
            calculated_index,
        )
        assert (
            calculated_index + start_delta == new_index
        ), "calculations should equal current position"

        (
            end_array_index,
            end_delta,
            calculated_index,
        ) = InlineBacktickHelper.__find_index_in_split_lines(
            split_source_lines, end_backtick_start_index
        )
        POGGER.debug(
            "end_array_index=$, end_delta=$, calculated_index=$",
            end_array_index,
            end_delta,
            calculated_index,
        )
        assert (
            calculated_index + end_delta == end_backtick_start_index
        ), "calculations should equal current position"

        if start_array_index == end_array_index:
            POGGER.debug("same")
            actual_between_text = split_tabified_lines[start_array_index][
                start_delta:end_delta
            ]
        else:
            POGGER.debug("borders")
            if start_delta:
                actual_between_text = split_tabified_lines[start_array_index][
                    start_delta:
                ]
                start_array_index += 1
            else:
                actual_between_text = ""
            actual_between_text += "".join(
                split_tabified_lines[i]
                for i in range(start_array_index, end_array_index)
            )
            if end_delta:
                actual_between_text += split_tabified_lines[end_array_index][:end_delta]
        POGGER.debug("actual_between_text>:$:<", actual_between_text)
        return actual_between_text, adj_newlines

    @staticmethod
    def __find_index_in_split_lines(
        split_array: List[str], index_to_find: int
    ) -> Tuple[int, int, int]:
        start_index = 0
        _array_index = 0
        for _array_index, array_element in enumerate(split_array):  # pragma: no cover
            POGGER.debug(
                "$--$ >>:$:<<", _array_index, start_index, split_array[_array_index]
            )
            if start_index <= index_to_find < start_index + len(array_element):
                break
            start_index += len(array_element)
        assert start_index != (
            start_index + len(split_array)
        ), "For loop must stop before the end."
        delta = index_to_find - start_index
        # d_before = split_array[_array_index][:delta]
        # d_after = split_array[_array_index][delta:]
        POGGER.debug("i=$,start_index=$,delta=$", _array_index, start_index, delta)
        return _array_index, delta, start_index
