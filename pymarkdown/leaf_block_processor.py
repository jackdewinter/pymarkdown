"""
Module to provide processing for the leaf blocks.
"""
import logging

from pymarkdown.html_helper import HtmlHelper
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_markdown_token import (
    AtxHeadingMarkdownToken,
    BlankLineMarkdownToken,
    FencedCodeBlockMarkdownToken,
    IndentedCodeBlockMarkdownToken,
    ParagraphMarkdownToken,
    SetextHeadingMarkdownToken,
    ThematicBreakMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    FencedCodeBlockStackToken,
    IndentedCodeBlockStackToken,
    ParagraphStackToken,
)

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


class LeafBlockProcessor:
    """
    Class to provide processing for the leaf blocks.
    """

    __fenced_start_tilde = "~"
    __fenced_start_backtick = "`"
    __fenced_code_block_start_characters = (
        f"{__fenced_start_tilde}{__fenced_start_backtick}"
    )
    __thematic_break_characters = "*_-"
    __atx_character = "#"
    __setext_characters = "-="

    @staticmethod
    def is_fenced_code_block(line_to_parse, start_index, extracted_whitespace, skip_whitespace_check=False):
        """
        Determine if we have the start of a fenced code block.
        """

        if (
            skip_whitespace_check or ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse,
            start_index,
            LeafBlockProcessor.__fenced_code_block_start_characters,
        ):
            POGGER.debug("ifcb:collected_count>>$<<$<<", line_to_parse, start_index)
            collected_count, new_index = ParserHelper.collect_while_character(
                line_to_parse, start_index, line_to_parse[start_index]
            )
            POGGER.debug("ifcb:collected_count:$", collected_count)
            (
                non_whitespace_index,
                extracted_whitespace_before_info_string,
            ) = ParserHelper.extract_whitespace(line_to_parse, new_index)

            if collected_count >= 3:
                POGGER.debug("ifcb:True")
                return (
                    True,
                    non_whitespace_index,
                    extracted_whitespace_before_info_string,
                    collected_count,
                )
        return False, None, None, None

    @staticmethod
    def parse_fenced_code_block(
        parser_state,
        position_marker,
        extracted_whitespace,
    ):
        """
        Handle the parsing of a fenced code block
        """

        POGGER.debug(
            "line>>$>>index>>$>>",
            position_marker.text_to_parse,
            position_marker.index_number,
        )
        new_tokens = []
        (
            is_fence_start,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            collected_count,
        ) = LeafBlockProcessor.is_fenced_code_block(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
        )
        if is_fence_start and not parser_state.token_stack[-1].is_html_block:
            if parser_state.token_stack[-1].is_fenced_code_block:
                LeafBlockProcessor.__check_for_fenced_end(
                    parser_state,
                    position_marker,
                    collected_count,
                    non_whitespace_index,
                    extracted_whitespace,
                    new_tokens,
                )
            else:
                new_tokens = LeafBlockProcessor.__process_fenced_start(
                    parser_state,
                    position_marker,
                    non_whitespace_index,
                    collected_count,
                    extracted_whitespace,
                    extracted_whitespace_before_info_string,
                )
        elif (
            parser_state.token_stack[-1].is_fenced_code_block
            and parser_state.token_stack[-1].whitespace_start_count
            and extracted_whitespace
        ):

            current_whitespace_length = ParserHelper.calculate_length(
                extracted_whitespace
            )
            whitespace_left = max(
                0,
                current_whitespace_length
                - parser_state.token_stack[-1].whitespace_start_count,
            )
            POGGER.debug("previous_ws>>$", current_whitespace_length)
            POGGER.debug("whitespace_left>>$", whitespace_left)
            removed_whitespace = ParserHelper.create_replace_with_nothing_marker(
                ParserHelper.repeat_string(
                    ParserHelper.space_character,
                    current_whitespace_length - whitespace_left,
                )
            )
            whitespace_padding = ParserHelper.repeat_string(
                ParserHelper.space_character, whitespace_left
            )
            extracted_whitespace = f"{removed_whitespace}{whitespace_padding}"
        return new_tokens, extracted_whitespace

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_fenced_start(
        parser_state,
        position_marker,
        non_whitespace_index,
        collected_count,
        extracted_whitespace,
        extracted_whitespace_before_info_string,
    ):

        POGGER.debug("pfcb->check")
        new_tokens = []
        if (
            position_marker.text_to_parse[position_marker.index_number]
            == LeafBlockProcessor.__fenced_start_tilde
            or LeafBlockProcessor.__fenced_start_backtick
            not in position_marker.text_to_parse[non_whitespace_index:]
        ):
            POGGER.debug("pfcb->start")
            (
                after_extracted_text_index,
                extracted_text,
            ) = ParserHelper.extract_until_whitespace(
                position_marker.text_to_parse, non_whitespace_index
            )
            text_after_extracted_text = position_marker.text_to_parse[
                after_extracted_text_index:
            ]

            old_top_of_stack = parser_state.token_stack[-1]
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[ParagraphStackToken],
            )

            pre_extracted_text, pre_text_after_extracted_text = (
                extracted_text,
                text_after_extracted_text,
            )

            extracted_text = InlineHelper.handle_backslashes(
                extracted_text, add_text_signature=False
            )
            text_after_extracted_text = InlineHelper.handle_backslashes(
                text_after_extracted_text, add_text_signature=False
            )

            if pre_extracted_text == extracted_text:
                pre_extracted_text = ""
            if pre_text_after_extracted_text == text_after_extracted_text:
                pre_text_after_extracted_text = ""

            new_token = FencedCodeBlockMarkdownToken(
                position_marker.text_to_parse[position_marker.index_number],
                collected_count,
                extracted_text,
                pre_extracted_text,
                text_after_extracted_text,
                pre_text_after_extracted_text,
                extracted_whitespace,
                extracted_whitespace_before_info_string,
                position_marker,
            )
            new_tokens.append(new_token)
            parser_state.token_stack.append(
                FencedCodeBlockStackToken(
                    code_fence_character=position_marker.text_to_parse[
                        position_marker.index_number
                    ],
                    fence_character_count=collected_count,
                    whitespace_start_count=ParserHelper.calculate_length(
                        extracted_whitespace
                    ),
                    matching_markdown_token=new_token,
                )
            )
            POGGER.debug("StackToken-->$<<", parser_state.token_stack[-1])
            POGGER.debug(
                "StackToken>start_markdown_token-->$<<",
                parser_state.token_stack[-1].matching_markdown_token,
            )

            LeafBlockProcessor.correct_for_leaf_block_start_in_list(
                parser_state,
                position_marker.index_indent,
                old_top_of_stack,
                new_tokens,
            )
        return new_tokens

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __check_for_fenced_end(
        parser_state,
        position_marker,
        collected_count,
        non_whitespace_index,
        extracted_whitespace,
        new_tokens,
    ):
        POGGER.debug("pfcb->end")

        if (
            parser_state.token_stack[-1].code_fence_character
            == position_marker.text_to_parse[position_marker.index_number]
            and collected_count >= parser_state.token_stack[-1].fence_character_count
            and non_whitespace_index >= len(position_marker.text_to_parse)
        ):
            new_end_token = parser_state.token_stack[
                -1
            ].generate_close_markdown_token_from_stack_token(
                extracted_whitespace, extra_end_data=str(collected_count)
            )
            new_tokens.append(new_end_token)
            del parser_state.token_stack[-1]

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_for_list_start(
        parser_state,
        last_list_start_index,
        last_block_quote_index,
    ):
        did_process, offset_index = False, 0
        POGGER.debug("last_list_start_index>>$>>", last_list_start_index)
        POGGER.debug(
            "parser_state.original_line_to_parse>>$>>",
            parser_state.original_line_to_parse,
        )
        if last_list_start_index:
            new_index, extracted_whitespace = ParserHelper.extract_whitespace_from_end(
                parser_state.original_line_to_parse, last_list_start_index
            )
            POGGER.debug("new_index>>$>>", new_index)
            POGGER.debug("extracted_whitespace>>$>>", extracted_whitespace)
            if ParserHelper.tab_character in extracted_whitespace:
                did_process, last_block_quote_index, offset_index = True, new_index, 1
        return did_process, offset_index, last_block_quote_index

    @staticmethod
    def __adjust_for_block_quote_start(
        force_me,
        parser_state,
        last_block_quote_index,
        position_marker,
        extracted_whitespace,
    ):
        """
        Block quotes cause indents, which need to be handled specifically.
        """

        (
            did_process,
            special_parse_start_index,
            whitespace_to_parse,
            block_quote_adjust_delta,
        ) = (False, 0, extracted_whitespace, 0)
        POGGER.debug(
            "last_block_quote_index>>$>>force_me>>$",
            last_block_quote_index,
            force_me,
        )
        if last_block_quote_index or force_me:
            POGGER.debug(
                "original_line_to_parse>[$]>>last_block_quote_index>>$",
                parser_state.original_line_to_parse,
                last_block_quote_index,
            )
            (
                block_quote_after_whitespace_index,
                during_original_whitespace,
            ) = ParserHelper.extract_whitespace(
                parser_state.original_line_to_parse, last_block_quote_index
            )
            POGGER.debug(
                "during_original_whitespace>[$]",
                during_original_whitespace,
            )
            if ParserHelper.tab_character in during_original_whitespace:
                (
                    special_parse_start_index,
                    whitespace_to_parse,
                    block_quote_adjust_delta,
                ) = LeafBlockProcessor.__block_quote_start_with_tab(
                    parser_state,
                    position_marker,
                    block_quote_after_whitespace_index,
                    last_block_quote_index,
                    extracted_whitespace,
                    during_original_whitespace,
                )
                did_process = True

        return (
            did_process,
            special_parse_start_index,
            whitespace_to_parse,
            block_quote_adjust_delta,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __block_quote_start_with_tab(
        parser_state,
        position_marker,
        block_quote_after_whitespace_index,
        last_block_quote_index,
        extracted_whitespace,
        during_original_whitespace,
    ):
        block_quote_adjust_delta = 0

        POGGER.debug(
            ".text_to_parse>[$]",
            position_marker,
        )
        POGGER.debug(".index_number>>$", position_marker.index_number)
        POGGER.debug(".index_indent>>$", position_marker.index_indent)
        POGGER.debug("last_block_quote_index>>$", last_block_quote_index)

        # Make sure everything after the whitespace remains the same.
        text_after_original_whitespace, text_after_whitespace = (
            parser_state.original_line_to_parse[block_quote_after_whitespace_index:],
            position_marker.text_to_parse[position_marker.index_number :],
        )
        POGGER.debug(
            "text_after_original_whitespace>[$]", text_after_original_whitespace
        )
        POGGER.debug(
            "text_after_whitespace>[$]",
            text_after_whitespace,
        )
        assert text_after_original_whitespace == text_after_whitespace

        # Make sure the whitespace is within expected bounds.
        during_current_whitespace = position_marker.text_to_parse[
            position_marker.index_number
            - len(extracted_whitespace) : position_marker.index_number
        ]
        POGGER.debug(
            "during_current_whitespace>[$]",
            during_current_whitespace,
        )
        POGGER.debug(
            "during_original_whitespace>[$]",
            during_original_whitespace,
        )

        current_whitespace_length, original_whitespace_length = len(
            during_current_whitespace
        ), (
            ParserHelper.calculate_length(
                during_original_whitespace, start_index=last_block_quote_index
            )
            - 1
        )
        POGGER.debug(
            "current_whitespace_length[$],original_whitespace_length[$]",
            current_whitespace_length,
            original_whitespace_length,
        )
        assert current_whitespace_length <= original_whitespace_length

        special_parse_start_index = last_block_quote_index + 1
        if during_original_whitespace[0] == ParserHelper.tab_character:
            whitespace_to_parse = during_original_whitespace
            if (
                current_whitespace_length > 1
                and whitespace_to_parse[1] == ParserHelper.tab_character
            ):
                block_quote_adjust_delta = -1
        else:
            whitespace_to_parse = during_original_whitespace[1:]
        return special_parse_start_index, whitespace_to_parse, block_quote_adjust_delta

    # pylint: enable=too-many-arguments

    @staticmethod
    def __recalculate_whitespace(
        special_parse_start_index, whitespace_to_parse, offset_index
    ):
        """
        Recalculate the whitespace characteristics.
        """

        (
            accumulated_whitespace_count,
            actual_whitespace_index,
            abc,
            relative_whitespace_index,
        ) = (0, 0, 4 + offset_index, special_parse_start_index - offset_index)

        POGGER.debug(
            "whitespace_to_parse>>$>>",
            whitespace_to_parse,
        )
        POGGER.debug("special_parse_start_index>>$>>", special_parse_start_index)
        POGGER.debug(
            "in>>index>>$($)>>accumulated_whitespace_count>>$",
            actual_whitespace_index,
            actual_whitespace_index + special_parse_start_index,
            accumulated_whitespace_count,
        )
        while accumulated_whitespace_count < abc:
            if (
                whitespace_to_parse[actual_whitespace_index]
                == ParserHelper.tab_character
            ):
                POGGER.debug(
                    ">>relative_whitespace_index>>$", relative_whitespace_index
                )
                delta_whitespace = 4 - (relative_whitespace_index % 4)
            else:
                delta_whitespace = 1
            POGGER.debug(">>delta_whitespace>>$", delta_whitespace)
            accumulated_whitespace_count += delta_whitespace
            relative_whitespace_index += delta_whitespace
            actual_whitespace_index += 1
            POGGER.debug(
                ">>index>>$($)>>accumulated_whitespace_count>>$",
                actual_whitespace_index,
                (actual_whitespace_index + special_parse_start_index),
                accumulated_whitespace_count,
            )

        POGGER.debug(
            "out>>index>>$($)>>accumulated_whitespace_count>>$",
            actual_whitespace_index,
            (actual_whitespace_index + special_parse_start_index),
            accumulated_whitespace_count,
        )

        adj_ws = whitespace_to_parse[0:actual_whitespace_index]
        left_ws = whitespace_to_parse[actual_whitespace_index:]
        POGGER.debug("accumulated_whitespace_count>>$", accumulated_whitespace_count)
        POGGER.debug("actual_whitespace_index>>$", actual_whitespace_index)
        POGGER.debug("adj_ws>>$<<", adj_ws)
        POGGER.debug("left_ws>>$<<", left_ws)
        POGGER.debug("offset_index>>$<<", offset_index)

        return accumulated_whitespace_count, actual_whitespace_index, adj_ws, left_ws

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_indented_code_block(
        parser_state,
        position_marker,
        extracted_whitespace,
        removed_chars_at_start,
        last_block_quote_index,
        last_list_start_index,
    ):
        """
        Handle the parsing of an indented code block
        """

        new_tokens = []

        if (
            ParserHelper.is_length_greater_than_or_equal_to(
                extracted_whitespace, 4, start_index=removed_chars_at_start
            )
            and not parser_state.token_stack[-1].is_paragraph
        ):
            if not parser_state.token_stack[-1].is_indented_code_block:
                (
                    last_block_quote_index,
                    extracted_whitespace,
                ) = LeafBlockProcessor.__create_indented_block(
                    parser_state,
                    last_list_start_index,
                    last_block_quote_index,
                    position_marker,
                    extracted_whitespace,
                    new_tokens,
                )

            new_tokens.append(
                TextMarkdownToken(
                    position_marker.text_to_parse[position_marker.index_number :],
                    extracted_whitespace,
                    position_marker=position_marker,
                )
            )
        return new_tokens

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __create_indented_block(
        parser_state,
        last_list_start_index,
        last_block_quote_index,
        position_marker,
        extracted_whitespace,
        new_tokens,
    ):
        (
            offset_index,
            last_block_quote_index,
            kludge_adjust,
            special_parse_start_index,
            block_quote_adjust_delta,
            accumulated_whitespace_count,
            actual_whitespace_index,
            adj_ws,
            left_ws,
        ) = LeafBlockProcessor.__prepare_for_indented_block(
            parser_state,
            last_list_start_index,
            last_block_quote_index,
            position_marker,
            extracted_whitespace,
        )

        line_number, column_number = position_marker.line_number, (
            position_marker.index_number
            + position_marker.index_indent
            - len(extracted_whitespace)
            + 1
        )
        if special_parse_start_index:
            column_number = (
                actual_whitespace_index
                + special_parse_start_index
                + block_quote_adjust_delta
            )
            POGGER.debug(
                "column_number($)=actual_whitespace_index($)+special_parse_start_index($)+block_quote_adjust_delta($)",
                column_number,
                actual_whitespace_index,
                special_parse_start_index,
                block_quote_adjust_delta,
            )
            excess_whitespace_count = accumulated_whitespace_count - 4 - offset_index
            POGGER.debug(
                "excess_whitespace_count($)=accumulated_whitespace_count($)-4-offset_index($)",
                excess_whitespace_count,
                accumulated_whitespace_count,
                offset_index,
            )
            POGGER.debug("before>>$>>", left_ws)
            if excess_whitespace_count:
                excess_whitespace_count -= kludge_adjust
                left_ws_padding = ParserHelper.repeat_string(
                    ParserHelper.space_character, excess_whitespace_count
                )
                left_ws = f"{left_ws_padding}{left_ws}"
            POGGER.debug("after>>$>>", left_ws)
        else:
            column_number += actual_whitespace_index
        POGGER.debug("column_number>>$", column_number)

        new_token = IndentedCodeBlockMarkdownToken(adj_ws, line_number, column_number)
        parser_state.token_stack.append(IndentedCodeBlockStackToken(new_token))
        new_tokens.append(new_token)
        extracted_whitespace = left_ws
        POGGER.debug("left_ws>>$<<", extracted_whitespace)

        return last_block_quote_index, extracted_whitespace

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-locals
    @staticmethod
    def __prepare_for_indented_block(
        parser_state,
        last_list_start_index,
        last_block_quote_index,
        position_marker,
        extracted_whitespace,
    ):
        POGGER.debug(">>__adjust_for_list_start")
        (
            did_process,
            offset_index,
            last_block_quote_index,
        ) = LeafBlockProcessor.__adjust_for_list_start(
            parser_state,
            last_list_start_index,
            last_block_quote_index,
        )
        POGGER.debug("<<__adjust_for_list_start<<$", did_process)

        force_me, kludge_adjust = False, 0
        if not did_process:
            POGGER.debug(">>>>$", parser_state.token_stack[-1])
            if parser_state.token_stack[-1].is_list:
                POGGER.debug(
                    ">>indent>>$",
                    parser_state.token_stack[-1].indent_level,
                )
                last_block_quote_index, kludge_adjust, force_me = 0, 1, True

        POGGER.debug(">>__adjust_for_block_quote_start")
        (
            did_process,
            special_parse_start_index,
            whitespace_to_parse,
            block_quote_adjust_delta,
        ) = LeafBlockProcessor.__adjust_for_block_quote_start(
            force_me,
            parser_state,
            last_block_quote_index,
            position_marker,
            extracted_whitespace,
        )
        POGGER.debug("<<__adjust_for_block_quote_start<<$", did_process)

        POGGER.debug(
            "__recalculate_whitespace>>$>>$",
            whitespace_to_parse,
            offset_index,
        )
        (
            accumulated_whitespace_count,
            actual_whitespace_index,
            adj_ws,
            left_ws,
        ) = LeafBlockProcessor.__recalculate_whitespace(
            special_parse_start_index, whitespace_to_parse, offset_index
        )
        return (
            offset_index,
            last_block_quote_index,
            kludge_adjust,
            special_parse_start_index,
            block_quote_adjust_delta,
            accumulated_whitespace_count,
            actual_whitespace_index,
            adj_ws,
            left_ws,
        )

    # pylint: enable=too-many-locals

    @staticmethod
    def is_thematic_break(
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check=False,
        whitespace_allowed_between_characters=True,
    ):
        """
        Determine whether or not we have a thematic break.
        """

        thematic_break_character, end_of_break_index = None, None
        is_thematic_character = ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, LeafBlockProcessor.__thematic_break_characters
        )
        POGGER.debug("skip_whitespace_check>>$", skip_whitespace_check)
        POGGER.debug("is_thematic_character>>$", is_thematic_character)
        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            or skip_whitespace_check
        ) and is_thematic_character:
            start_char, index, char_count, repeat_loop, line_to_parse_size = (
                line_to_parse[start_index],
                start_index,
                0,
                True,
                len(line_to_parse),
            )
            while repeat_loop and index < line_to_parse_size:
                if (
                    whitespace_allowed_between_characters
                    and ParserHelper.is_character_at_index_whitespace(
                        line_to_parse, index
                    )
                ):
                    index += 1
                elif line_to_parse[index] == start_char:
                    index += 1
                    char_count += 1
                else:
                    repeat_loop = False

            POGGER.debug("char_count>>$", char_count)
            POGGER.debug("index>>$", index)
            POGGER.debug("line_to_parse_size>>$", line_to_parse_size)
            if char_count >= 3 and index == line_to_parse_size:
                thematic_break_character, end_of_break_index = start_char, index

        return thematic_break_character, end_of_break_index

    @staticmethod
    def parse_thematic_break(
        parser_state,
        position_marker,
        extracted_whitespace,
        block_quote_data,
    ):
        """
        Handle the parsing of a thematic break.
        """

        new_tokens = []

        start_char, index = LeafBlockProcessor.is_thematic_break(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
        )
        if start_char:
            if parser_state.token_stack[-1].is_paragraph:
                force_paragraph_close_if_present = (
                    block_quote_data.current_count == 0
                    and block_quote_data.stack_count > 0
                )
                new_tokens, _ = parser_state.close_open_blocks_fn(
                    parser_state,
                    destination_array=new_tokens,
                    only_these_blocks=[ParagraphStackToken],
                    was_forced=force_paragraph_close_if_present,
                )
            if block_quote_data.current_count == 0 and block_quote_data.stack_count > 0:
                new_tokens, _ = parser_state.close_open_blocks_fn(
                    parser_state,
                    destination_array=new_tokens,
                    only_these_blocks=[BlockQuoteStackToken],
                    include_block_quotes=True,
                    was_forced=True,
                )
            new_tokens.append(
                ThematicBreakMarkdownToken(
                    start_char,
                    extracted_whitespace.replace(ParserHelper.tab_character, "    "),
                    position_marker.text_to_parse[
                        position_marker.index_number : index
                    ].replace(ParserHelper.tab_character, "    "),
                    position_marker=position_marker,
                )
            )
        return new_tokens

    @staticmethod
    def is_atx_heading(line_to_parse, start_index, extracted_whitespace, skip_whitespace_check=False):
        """
        Determine whether or not an ATX Heading is about to start.
        """

        if (ParserHelper.is_length_less_than_or_equal_to(
            extracted_whitespace, 3
        ) or skip_whitespace_check )and ParserHelper.is_character_at_index(
            line_to_parse,
            start_index,
            LeafBlockProcessor.__atx_character,
        ):
            hash_count, new_index = ParserHelper.collect_while_character(
                line_to_parse,
                start_index,
                LeafBlockProcessor.__atx_character,
            )

            non_whitespace_index = ParserHelper.collect_while_character(
                line_to_parse, new_index, " "
            )
            extracted_whitespace_at_start = line_to_parse[
                new_index : non_whitespace_index[1]
            ]

            if hash_count <= 6 and (
                extracted_whitespace_at_start
                or non_whitespace_index[1] == len(line_to_parse)
            ):
                return (
                    True,
                    non_whitespace_index[1],
                    hash_count,
                    extracted_whitespace_at_start,
                )
        return False, None, None, None

    @staticmethod
    def parse_atx_headings(parser_state, position_marker, extracted_whitespace):
        """
        Handle the parsing of an atx heading.
        """

        new_tokens = []

        (
            heading_found,
            non_whitespace_index,
            hash_count,
            extracted_whitespace_at_start,
        ) = LeafBlockProcessor.is_atx_heading(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
        )
        if heading_found:
            POGGER.debug(
                "parse_atx_headings>>start",
            )

            (
                old_top_of_stack,
                remaining_line,
                remove_trailing_count,
                extracted_whitespace_before_end,
                extracted_whitespace_at_end,
                new_tokens,
            ) = LeafBlockProcessor.__prepare_for_create_atx_heading(
                parser_state, position_marker, new_tokens, non_whitespace_index
            )
            start_token = AtxHeadingMarkdownToken(
                hash_count,
                remove_trailing_count,
                extracted_whitespace,
                position_marker,
            )
            new_tokens.append(start_token)

            LeafBlockProcessor.correct_for_leaf_block_start_in_list(
                parser_state,
                position_marker.index_indent,
                old_top_of_stack,
                new_tokens,
                was_token_already_added_to_stack=False,
            )

            new_tokens.append(
                TextMarkdownToken(
                    remaining_line,
                    extracted_whitespace_at_start,
                    position_marker=position_marker,
                )
            )
            end_token = start_token.generate_close_markdown_token_from_markdown_token(
                extracted_whitespace_at_end, extracted_whitespace_before_end, False
            )
            new_tokens.append(end_token)
        return new_tokens

    @staticmethod
    def __prepare_for_create_atx_heading(
        parser_state, position_marker, new_tokens, non_whitespace_index
    ):
        (
            old_top_of_stack,
            remaining_line,
            remove_trailing_count,
            extracted_whitespace_before_end,
        ) = (
            parser_state.token_stack[-1],
            position_marker.text_to_parse[non_whitespace_index:],
            0,
            "",
        )

        new_tokens, _ = parser_state.close_open_blocks_fn(parser_state, new_tokens)
        (
            end_index,
            extracted_whitespace_at_end,
        ) = ParserHelper.extract_whitespace_from_end(remaining_line)
        while (
            end_index > 0
            and remaining_line[end_index - 1] == LeafBlockProcessor.__atx_character
        ):
            end_index -= 1
            remove_trailing_count += 1
        if remove_trailing_count:
            if end_index > 0:
                if ParserHelper.is_character_at_index(
                    remaining_line, end_index - 1, " "
                ):
                    remaining_line = remaining_line[:end_index]
                    non_whitespace_index = (
                        ParserHelper.collect_backwards_while_character(
                            remaining_line, len(remaining_line) - 1, " "
                        )
                    )
                    end_index = non_whitespace_index[1]
                    extracted_whitespace_before_end = remaining_line[end_index:]
                    remaining_line = remaining_line[:end_index]
                else:
                    extracted_whitespace_at_end, remove_trailing_count = "", 0
            else:
                remaining_line = ""
        else:
            extracted_whitespace_at_end = remaining_line[end_index:]
            remaining_line = remaining_line[0:end_index]

        return (
            old_top_of_stack,
            remaining_line,
            remove_trailing_count,
            extracted_whitespace_before_end,
            extracted_whitespace_at_end,
            new_tokens,
        )

    @staticmethod
    def parse_setext_headings(
        parser_state,
        position_marker,
        extracted_whitespace,
        block_quote_data,
    ):
        """
        Handle the parsing of an setext heading.
        """

        new_tokens = []
        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            and ParserHelper.is_character_at_index_one_of(
                position_marker.text_to_parse,
                position_marker.index_number,
                LeafBlockProcessor.__setext_characters,
            )
            and parser_state.token_stack[-1].is_paragraph
            and (block_quote_data.current_count == block_quote_data.stack_count)
        ):
            is_paragraph_continuation = (
                LeafBlockProcessor.__adjust_continuation_for_active_list(
                    parser_state, position_marker
                )
            )

            _, collected_to_index = ParserHelper.collect_while_character(
                position_marker.text_to_parse,
                position_marker.index_number,
                position_marker.text_to_parse[position_marker.index_number],
            )
            (
                after_whitespace_index,
                extra_whitespace_after_setext,
            ) = ParserHelper.extract_whitespace(
                position_marker.text_to_parse, collected_to_index
            )

            if not is_paragraph_continuation and after_whitespace_index == len(
                position_marker.text_to_parse
            ):
                LeafBlockProcessor.__create_setext_token(
                    parser_state,
                    position_marker,
                    collected_to_index,
                    new_tokens,
                    extracted_whitespace,
                    extra_whitespace_after_setext,
                )
        return new_tokens

    @staticmethod
    def __adjust_continuation_for_active_list(parser_state, position_marker):
        is_paragraph_continuation = False
        if len(parser_state.token_stack) > 1 and parser_state.token_stack[-2].is_list:
            POGGER.debug(
                "parser_state.original_line_to_parse>:$:<",
                parser_state.original_line_to_parse,
            )
            adj_text = position_marker.text_to_parse[position_marker.index_number :]
            assert parser_state.original_line_to_parse.endswith(adj_text)
            removed_text_length = len(parser_state.original_line_to_parse) - len(
                adj_text
            )
            POGGER.debug("removed_text_length>:$:<", removed_text_length)
            POGGER.debug("adj_text>:$:<", adj_text)
            POGGER.debug("indent_level>:$:<", parser_state.token_stack[-2].indent_level)
            if (
                adj_text
                and removed_text_length < parser_state.token_stack[-2].indent_level
            ):
                is_paragraph_continuation = True
        return is_paragraph_continuation

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_setext_token(
        parser_state,
        position_marker,
        collected_to_index,
        new_tokens,
        extracted_whitespace,
        extra_whitespace_after_setext,
    ):
        token_index = len(parser_state.token_document) - 1
        while not parser_state.token_document[token_index].is_paragraph:
            token_index -= 1

        replacement_token = SetextHeadingMarkdownToken(
            position_marker.text_to_parse[position_marker.index_number],
            collected_to_index - position_marker.index_number,
            parser_state.token_document[token_index].extra_data,
            position_marker,
            parser_state.token_document[token_index],
        )

        # This is unusual.  Normally, close_open_blocks is used to close off
        # blocks based on the stack token.  However, since the setext takes
        # the last paragraph of text (see case 61) and translates it
        # into a heading, this has to be done separately, as there is no
        # stack token to close.
        new_tokens.append(
            replacement_token.generate_close_markdown_token_from_markdown_token(
                extracted_whitespace, extra_whitespace_after_setext, False
            )
        )

        parser_state.token_document[token_index] = replacement_token
        del parser_state.token_stack[-1]

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_paragraph(
        parser_state,
        position_marker,
        extracted_whitespace,
        block_quote_data,
        text_removed_by_container,
        force_it,
    ):
        """
        Handle the parsing of a paragraph.
        """
        if parser_state.no_para_start_if_empty and position_marker.index_number >= len(
            position_marker.text_to_parse
        ):
            POGGER.debug("Escaping paragraph due to empty w/ blank")
            POGGER.debug("position_marker.text_to_parse=:$:", position_marker.text_to_parse)
            POGGER.debug("position_marker.index_number=:$:", position_marker.index_number)
            POGGER.debug("position_marker.index_indent=:$:", position_marker.index_indent)
            return [
                BlankLineMarkdownToken(
                    extracted_whitespace, position_marker, len(extracted_whitespace)
                )
            ]

        POGGER.debug(
            "parse_paragraph>block_quote_data.stack_count>$>block_quote_data.current_count>$<",
            block_quote_data.stack_count,
            block_quote_data.current_count,
        )

        container_index, adjusted_whitespace_length = (
            parser_state.find_last_container_on_stack(),
            0,
        )
        if container_index > 0:
            adjusted_whitespace_length = (
                LeafBlockProcessor.__adjust_paragraph_for_containers(
                    parser_state,
                    container_index,
                    position_marker,
                    text_removed_by_container,
                    force_it,
                    extracted_whitespace,
                    adjusted_whitespace_length,
                )
            )

        new_tokens, extracted_whitespace = LeafBlockProcessor.__handle_paragraph_prep(
            parser_state,
            block_quote_data,
            adjusted_whitespace_length,
            position_marker,
            extracted_whitespace,
        )

        new_tokens.append(
            TextMarkdownToken(
                position_marker.text_to_parse[position_marker.index_number :],
                extracted_whitespace,
                position_marker=position_marker,
            )
        )
        return new_tokens

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_paragraph_prep(
        parser_state,
        block_quote_data,
        adjusted_whitespace_length,
        position_marker,
        extracted_whitespace,
    ):

        new_tokens = []

        # In cases where the list ended on the same line as we are processing, the
        # container tokens will not yet be added to the token_document.  As such,
        # make sure to construct a "proper" list that takes those into account
        # before checking to see if this is an issue.
        adjusted_document = parser_state.token_document[:]
        if parser_state.same_line_container_tokens:
            adjusted_document.extend(parser_state.same_line_container_tokens)

        if (
            len(adjusted_document) >= 2
            and adjusted_document[-1].is_blank_line
            and adjusted_document[-2].is_any_list_token
        ):

            did_find, last_list_index = LeafBlockProcessor.check_for_list_in_process(
                parser_state
            )
            assert did_find
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state, until_this_index=last_list_index
            )

        if block_quote_data.stack_count != 0 and block_quote_data.current_count == 0:
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[BlockQuoteStackToken],
                include_block_quotes=True,
            )

        if adjusted_whitespace_length:
            POGGER.debug(">>GGHHJJ!!>>$>>", adjusted_whitespace_length)
            extracted_whitespace = ParserHelper.repeat_string(
                ParserHelper.blech_character, adjusted_whitespace_length
            )

        if not parser_state.token_stack[-1].is_paragraph:
            new_paragraph_token = ParagraphMarkdownToken(
                extracted_whitespace, position_marker
            )
            parser_state.token_stack.append(ParagraphStackToken(new_paragraph_token))
            new_tokens.append(new_paragraph_token)
            extracted_whitespace = ""
        return new_tokens, extracted_whitespace

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_paragraph_for_containers(
        parser_state,
        container_index,
        position_marker,
        text_removed_by_container,
        force_it,
        extracted_whitespace,
        adjusted_whitespace_length,
    ):
        POGGER.debug(">>extracted_whitespace>>:$:<<", extracted_whitespace)
        POGGER.debug(">>adjusted_whitespace_length>>$", adjusted_whitespace_length)
        top_block_token = None
        if parser_state.token_stack[container_index].is_block_quote:
            top_block_token = parser_state.token_stack[container_index]
            POGGER.debug(">>container_index>>$", container_index)
            POGGER.debug(">>block-owners>>$", top_block_token)
            POGGER.debug(
                ">>token_stack>>$",
                ParserHelper.make_value_visible(parser_state.token_stack),
            )
            POGGER.debug(">>line_number>>$", position_marker.line_number)

            if (
                container_index + 1 == len(parser_state.token_stack)
                and position_marker.line_number
                == top_block_token.matching_markdown_token.line_number
                and container_index > 0
                and parser_state.token_stack[container_index - 1].is_list
            ):
                POGGER.debug(
                    ">>list-owners>>$",
                    ParserHelper.make_value_visible(
                        parser_state.token_stack[
                            container_index - 1
                        ].matching_markdown_token
                    ),
                )
                apply_paragraph_adjustment = not (
                    position_marker.line_number
                    == parser_state.token_stack[
                        container_index - 1
                    ].matching_markdown_token.line_number
                )
            else:
                apply_paragraph_adjustment = True

            if apply_paragraph_adjustment:
                LeafBlockProcessor.__adjust_paragraph_for_block_quotes(
                    top_block_token,
                    text_removed_by_container,
                    force_it,
                    parser_state.token_document,
                )
        else:
            top_list_token = parser_state.token_stack[container_index]
            POGGER.debug(">>list-owners>>$", top_list_token)
            adjusted_whitespace_length = LeafBlockProcessor.__adjust_paragraph_for_list(
                top_list_token, extracted_whitespace
            )
        return adjusted_whitespace_length

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_paragraph_for_list(top_list_token, extracted_whitespace):
        ex_ws_length = len(extracted_whitespace)
        POGGER.debug(">>owners-indent>>$", top_list_token.indent_level)
        POGGER.debug(">>ws_before_marker>>$", top_list_token.ws_before_marker)
        POGGER.debug(">>ws_after_marker>>$", top_list_token.ws_after_marker)
        POGGER.debug(">>last_new_list_token>>$", top_list_token.last_new_list_token)
        POGGER.debug(">>extracted_whitespace>>$", ex_ws_length)

        dominant_indent, original_list_indent, indent_delta = (
            (
                top_list_token.last_new_list_token.indent_level
                if top_list_token.last_new_list_token
                else top_list_token.indent_level
            ),
            top_list_token.indent_level - 2,
            (
                top_list_token.ws_after_marker - 1
                if top_list_token.ws_after_marker > 1
                else 0
            ),
        )
        POGGER.debug(">>dominant_indent>>$>>", dominant_indent)
        original_text_indent = (
            ex_ws_length
            + top_list_token.indent_level
            - top_list_token.ws_before_marker
            - indent_delta
        )
        POGGER.debug(">>original_list_indent>>$>>", original_list_indent)
        POGGER.debug(">>original_text_indent>$>>", original_text_indent)
        return (
            dominant_indent - original_text_indent
            if dominant_indent > original_text_indent >= 4
            else 0
        )

    @staticmethod
    def __adjust_paragraph_for_block_quotes(
        top_block_token,
        text_removed_by_container,
        force_it,
        token_document,
    ):
        POGGER.debug(">>list-owners>>$", token_document)
        POGGER.debug(">>text_removed_by_container>>$<<", text_removed_by_container)
        POGGER.debug(">>force_it>>$<<", force_it)
        number_of_block_quote_ends, end_index = 0, len(token_document) - 1
        while token_document[end_index].is_block_quote_end:
            number_of_block_quote_ends += 1
            end_index -= 1
        if not (
            number_of_block_quote_ends > 0
            and token_document[end_index].is_fenced_code_block_end
        ):
            if text_removed_by_container is None:
                top_block_token.matching_markdown_token.add_leading_spaces("")
            elif force_it:
                top_block_token.matching_markdown_token.add_leading_spaces(
                    text_removed_by_container
                )

    @staticmethod
    def check_for_list_in_process(parser_state):
        """
        From the end of the stack, check to see if there is already a list in progress.
        """

        stack_index = len(parser_state.token_stack) - 1

        while stack_index >= 0 and not parser_state.token_stack[stack_index].is_list:
            stack_index -= 1

        return stack_index >= 0, stack_index

    @staticmethod
    def correct_for_leaf_block_start_in_list(
        parser_state,
        removed_chars_at_start,
        old_top_of_stack,
        html_tokens,
        was_token_already_added_to_stack=True,
    ):
        """
        Check to see that if a paragraph has been closed within a list and
        there is a leaf block token immediately following, that the right
        actions are taken.
        """

        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>removed_chars_at_start>$>>",
            removed_chars_at_start,
        )
        if not old_top_of_stack.is_paragraph:
            POGGER.debug("1")
            return

        statck_index, top_of_stack, end_of_list = (
            -2 if was_token_already_added_to_stack else -1,
            None,
            html_tokens[-1],
        )
        if not parser_state.token_stack[statck_index].is_list:
            POGGER.debug("2")
            return

        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
            parser_state.token_stack,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens>>$>>",
            parser_state.token_document,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

        if was_token_already_added_to_stack:
            top_of_stack = parser_state.token_stack[-1]
            del parser_state.token_stack[-1]
        del html_tokens[-1]

        LeafBlockProcessor.__handle_leaf_start(
            parser_state, removed_chars_at_start, html_tokens
        )

        if was_token_already_added_to_stack:
            parser_state.token_stack.append(top_of_stack)
            POGGER.debug(
                ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
                parser_state.token_stack,
            )
        html_tokens.append(end_of_list)
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

    @staticmethod
    def __handle_leaf_start(parser_state, removed_chars_at_start, html_tokens):
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
            parser_state.token_stack,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

        repeat_loop, is_remaining_list_token = True, True
        while repeat_loop and is_remaining_list_token:
            assert parser_state.token_stack[-1].is_list

            POGGER.debug(">>removed_chars_at_start>>$>>", removed_chars_at_start)
            POGGER.debug(
                ">>stack indent>>$>>", parser_state.token_stack[-1].indent_level
            )
            if removed_chars_at_start >= parser_state.token_stack[-1].indent_level:
                repeat_loop = False
            else:
                tokens_from_close, _ = parser_state.close_open_blocks_fn(
                    parser_state,
                    until_this_index=(len(parser_state.token_stack) - 1),
                    include_lists=True,
                )
                POGGER.debug(
                    ">>correct_for_leaf_block_start_in_list>>tokens_from_close>>$>>",
                    tokens_from_close,
                )
                html_tokens.extend(tokens_from_close)

                is_remaining_list_token = parser_state.token_stack[-1].is_list

        if is_remaining_list_token:
            assert parser_state.token_stack[-1].is_list
            delta_indent = (
                removed_chars_at_start - parser_state.token_stack[-1].indent_level
            )
            POGGER.debug(
                ">>correct_for_leaf_block_start_in_list>>delta_indent>>$>>",
                delta_indent,
            )
            assert not delta_indent

    @staticmethod
    def is_paragraph_ending_leaf_block_start(
        parser_state,
        line_to_parse,
        start_index,
        extracted_whitespace,
        exclude_thematic_break=False,
    ):
        """
        Determine whether we have a valid leaf block start.
        """

        is_leaf_block_start = False
        if not exclude_thematic_break:
            is_leaf_block_start, _ = LeafBlockProcessor.is_thematic_break(
                line_to_parse,
                start_index,
                extracted_whitespace,
                skip_whitespace_check=True,
            )
            is_leaf_block_start = bool(is_leaf_block_start)
            POGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_theme_break>>$",
                is_leaf_block_start,
            )
        if not is_leaf_block_start:
            is_leaf_block_start, _ = HtmlHelper.is_html_block(
                line_to_parse,
                start_index,
                extracted_whitespace,
                parser_state.token_stack,
            )
            is_leaf_block_start = bool(is_leaf_block_start)
            POGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_html_block>>$",
                is_leaf_block_start,
            )
        if not is_leaf_block_start:
            is_leaf_block_start, _, _, _ = LeafBlockProcessor.is_fenced_code_block(
                line_to_parse, start_index, extracted_whitespace
            )
            POGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_fenced_code_block>>$",
                is_leaf_block_start,
            )
        if not is_leaf_block_start:
            is_leaf_block_start, _, _, _ = LeafBlockProcessor.is_atx_heading(
                line_to_parse, start_index, extracted_whitespace
            )
            POGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_atx_heading>>$",
                is_leaf_block_start,
            )
        return is_leaf_block_start
