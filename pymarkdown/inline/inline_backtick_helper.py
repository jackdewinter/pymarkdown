"""
Module to help with the parsing of bkactick inline elements.
"""

import logging
from typing import List, Tuple

from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.inline.inline_helper import InlineHelper
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.inline.inline_response import InlineResponse
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)

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

        assert inline_response.new_index is not None
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
            assert inline_request.line_number is not None
            assert inline_request.column_number is not None
            assert inline_request.remaining_line is not None
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
    def __calculate_backtick_between_text(
        inline_request: InlineRequest, new_index: int, end_backtick_start_index: int
    ) -> Tuple[str, str, str, str]:
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
            between_text = (
                InlineBacktickHelper.__calculate_backtick_between_tabified_text(
                    inline_request, new_index, end_backtick_start_index
                )
            )
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
        )

    @staticmethod
    def __calculate_backtick_between_tabified_text(
        inline_request: InlineRequest, new_index: int, end_backtick_start_index: int
    ) -> str:
        POGGER.debug("inline_request.tabified_text>>$<<", inline_request.tabified_text)
        split_source_lines = InlineBacktickHelper.__backtick_split_lines(
            inline_request.source_text
        )
        POGGER.debug("split_source_lines>>$<<", split_source_lines)
        assert inline_request.tabified_text is not None
        split_tabified_lines = InlineBacktickHelper.__backtick_split_lines(
            inline_request.tabified_text
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
        assert calculated_index + start_delta == new_index

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
        assert calculated_index + end_delta == end_backtick_start_index

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
        return actual_between_text

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
        assert start_index != (start_index + len(split_array))
        delta = index_to_find - start_index
        POGGER.debug("i=$,start_index=$,delta=$", _array_index, start_index, delta)
        return _array_index, delta, start_index
