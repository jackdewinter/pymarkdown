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
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    FencedCodeBlockStackToken,
    IndentedCodeBlockStackToken,
    ParagraphStackToken,
)

LOGGER = logging.getLogger(__name__)

# pylint: disable=too-many-lines


class LeafBlockProcessor:
    """
    Class to provide processing for the leaf blocks.
    """

    __fenced_start_tilde = "~"
    __fenced_start_backtick = "`"
    __fenced_code_block_start_characters = (
        __fenced_start_tilde + __fenced_start_backtick
    )
    __thematic_break_characters = "*_-"
    __atx_character = "#"
    __setext_characters = "-="

    @staticmethod
    def is_fenced_code_block(line_to_parse, start_index, extracted_whitespace):
        """
        Determine if we have the start of a fenced code block.
        """

        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse,
            start_index,
            LeafBlockProcessor.__fenced_code_block_start_characters,
        ):
            LOGGER.debug(
                "ifcb:collected_count>>%s<<%s<<", line_to_parse, str(start_index)
            )
            collected_count, new_index = ParserHelper.collect_while_character(
                line_to_parse, start_index, line_to_parse[start_index]
            )
            LOGGER.debug("ifcb:collected_count:%s", str(collected_count))
            (
                non_whitespace_index,
                extracted_whitespace_before_info_string,
            ) = ParserHelper.extract_whitespace(line_to_parse, new_index)

            if collected_count >= 3:
                LOGGER.debug("ifcb:True")
                return (
                    True,
                    non_whitespace_index,
                    extracted_whitespace_before_info_string,
                    collected_count,
                )
        return False, None, None, None

    # pylint: disable=too-many-locals
    @staticmethod
    def parse_fenced_code_block(
        parser_state,
        position_marker,
        extracted_whitespace,
    ):
        """
        Handle the parsing of a fenced code block
        """

        LOGGER.debug(
            "line>>%s>>index>>%s>>",
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
                LOGGER.debug("pfcb->end")

                if (
                    parser_state.token_stack[-1].code_fence_character
                    == position_marker.text_to_parse[position_marker.index_number]
                    and collected_count
                    >= parser_state.token_stack[-1].fence_character_count
                    and non_whitespace_index >= len(position_marker.text_to_parse)
                ):
                    new_end_token = parser_state.token_stack[
                        -1
                    ].generate_close_markdown_token_from_stack_token(
                        extracted_whitespace, extra_end_data=str(collected_count)
                    )
                    new_tokens.append(new_end_token)
                    del parser_state.token_stack[-1]
            else:
                LOGGER.debug("pfcb->check")
                if (
                    position_marker.text_to_parse[position_marker.index_number]
                    == LeafBlockProcessor.__fenced_start_tilde
                    or LeafBlockProcessor.__fenced_start_backtick
                    not in position_marker.text_to_parse[non_whitespace_index:]
                ):
                    LOGGER.debug("pfcb->start")
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
                    new_tokens, _, _ = parser_state.close_open_blocks_fn(
                        parser_state,
                        only_these_blocks=[ParagraphStackToken],
                    )

                    pre_extracted_text = extracted_text
                    pre_text_after_extracted_text = text_after_extracted_text

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
                    LOGGER.debug("StackToken-->%s<<", str(parser_state.token_stack[-1]))
                    LOGGER.debug(
                        "StackToken>start_markdown_token-->%s<<",
                        str(parser_state.token_stack[-1].matching_markdown_token),
                    )

                    LeafBlockProcessor.correct_for_leaf_block_start_in_list(
                        parser_state,
                        position_marker.index_indent,
                        old_top_of_stack,
                        new_tokens,
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
            LOGGER.debug("previous_ws>>%s", str(current_whitespace_length))
            LOGGER.debug("whitespace_left>>%s", str(whitespace_left))
            removed_whitespace = ParserHelper.create_replace_with_nothing_marker(
                ParserHelper.repeat_string(
                    ParserHelper.space_character,
                    current_whitespace_length - whitespace_left,
                )
            )
            extracted_whitespace = removed_whitespace + ParserHelper.repeat_string(
                ParserHelper.space_character, whitespace_left
            )
        return new_tokens, extracted_whitespace

    # pylint: enable=too-many-locals

    @staticmethod
    def __adjust_for_list_start(
        parser_state,
        last_list_start_index,
        last_block_quote_index,
    ):
        did_process = False
        LOGGER.debug("last_list_start_index>>%s>>", str(last_list_start_index))
        LOGGER.debug(
            "parser_state.original_line_to_parse>>%s>>",
            ParserHelper.make_value_visible(parser_state.original_line_to_parse),
        )
        offset_index = 0
        if last_list_start_index:
            new_index, extracted_whitespace = ParserHelper.extract_whitespace_from_end(
                parser_state.original_line_to_parse, last_list_start_index
            )
            LOGGER.debug("new_index>>%s>>", str(new_index))
            LOGGER.debug(
                "extracted_whitespace>>%s>>",
                ParserHelper.make_value_visible(extracted_whitespace),
            )
            if ParserHelper.tab_character in extracted_whitespace:
                last_block_quote_index = new_index
                offset_index = 1
                did_process = True
        return did_process, offset_index, last_block_quote_index

    # pylint: disable=too-many-locals
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

        did_process = False
        special_parse_start_index = 0
        whitespace_to_parse = extracted_whitespace
        block_quote_adjust_delta = 0

        LOGGER.debug(
            "last_block_quote_index>>%s>>force_me>>%s",
            str(last_block_quote_index),
            str(force_me),
        )
        if last_block_quote_index or force_me:
            LOGGER.debug(
                "original_line_to_parse>[%s]>>last_block_quote_index>>%s",
                ParserHelper.make_value_visible(parser_state.original_line_to_parse),
                str(last_block_quote_index),
            )
            (
                block_quote_after_whitespace_index,
                during_original_whitespace,
            ) = ParserHelper.extract_whitespace(
                parser_state.original_line_to_parse, last_block_quote_index
            )
            LOGGER.debug(
                "during_original_whitespace>[%s]",
                ParserHelper.make_value_visible(during_original_whitespace),
            )
            if ParserHelper.tab_character in during_original_whitespace:

                did_process = True
                LOGGER.debug(
                    ".text_to_parse>[%s]",
                    ParserHelper.make_value_visible(position_marker),
                )
                LOGGER.debug(".index_number>>%s", str(position_marker.index_number))
                LOGGER.debug(".index_indent>>%s", str(position_marker.index_indent))
                LOGGER.debug("last_block_quote_index>>%s", str(last_block_quote_index))

                # Make sure everything after the whitespace remains the same.
                text_after_original_whitespace = parser_state.original_line_to_parse[
                    block_quote_after_whitespace_index:
                ]
                text_after_whitespace = position_marker.text_to_parse[
                    position_marker.index_number :
                ]
                LOGGER.debug(
                    "text_after_original_whitespace>[%s]",
                    ParserHelper.make_value_visible(text_after_original_whitespace),
                )
                LOGGER.debug(
                    "text_after_whitespace>[%s]",
                    ParserHelper.make_value_visible(text_after_whitespace),
                )
                assert text_after_original_whitespace == text_after_whitespace

                # Make sure the whitespace is within expected bounds.
                during_current_whitespace = position_marker.text_to_parse[
                    position_marker.index_number
                    - len(extracted_whitespace) : position_marker.index_number
                ]
                LOGGER.debug(
                    "during_current_whitespace>[%s]",
                    ParserHelper.make_value_visible(during_current_whitespace),
                )
                LOGGER.debug(
                    "during_original_whitespace>[%s]",
                    ParserHelper.make_value_visible(during_original_whitespace),
                )

                current_whitespace_length = len(during_current_whitespace)
                original_whitespace_length = (
                    ParserHelper.calculate_length(
                        during_original_whitespace, start_index=last_block_quote_index
                    )
                    - 1
                )
                LOGGER.debug(
                    "current_whitespace_length[%s],original_whitespace_length[%s]",
                    str(current_whitespace_length),
                    str(original_whitespace_length),
                )
                assert current_whitespace_length <= original_whitespace_length

                special_parse_start_index = last_block_quote_index + 1
                if during_original_whitespace[0] == ParserHelper.tab_character:
                    whitespace_to_parse = during_original_whitespace
                    if (
                        len(during_original_whitespace) > 1
                        and during_original_whitespace[1] == ParserHelper.tab_character
                    ):
                        block_quote_adjust_delta = -1
                else:
                    whitespace_to_parse = during_original_whitespace[1:]

        return (
            did_process,
            special_parse_start_index,
            whitespace_to_parse,
            block_quote_adjust_delta,
        )

    # pylint: enable=too-many-locals

    @staticmethod
    def __recalculate_whitespace(
        special_parse_start_index, whitespace_to_parse, offset_index
    ):
        """
        Recalculate the whitespace characteristics.
        """

        accumulated_whitespace_count = 0
        actual_whitespace_index = 0
        abc = 4 + offset_index

        relative_whitespace_index = special_parse_start_index - offset_index
        LOGGER.debug(
            "whitespace_to_parse>>%s>>",
            ParserHelper.make_value_visible(whitespace_to_parse),
        )
        LOGGER.debug("special_parse_start_index>>%s>>", str(special_parse_start_index))
        LOGGER.debug(
            "in>>index>>%s(%s)>>accumulated_whitespace_count>>%s",
            str(actual_whitespace_index),
            str(actual_whitespace_index + special_parse_start_index),
            str(accumulated_whitespace_count),
        )
        while accumulated_whitespace_count < abc:
            if (
                whitespace_to_parse[actual_whitespace_index]
                == ParserHelper.tab_character
            ):
                LOGGER.debug(
                    ">>relative_whitespace_index>>%s", str(relative_whitespace_index)
                )
                delta_whitespace = 4 - (relative_whitespace_index % 4)
            else:
                delta_whitespace = 1
            LOGGER.debug(">>delta_whitespace>>%s", str(delta_whitespace))
            accumulated_whitespace_count += delta_whitespace
            relative_whitespace_index += delta_whitespace
            actual_whitespace_index += 1
            LOGGER.debug(
                ">>index>>%s(%s)>>accumulated_whitespace_count>>%s",
                str(actual_whitespace_index),
                str(actual_whitespace_index + special_parse_start_index),
                str(accumulated_whitespace_count),
            )

        LOGGER.debug(
            "out>>index>>%s(%s)>>accumulated_whitespace_count>>%s",
            str(actual_whitespace_index),
            str(actual_whitespace_index + special_parse_start_index),
            str(accumulated_whitespace_count),
        )

        adj_ws = whitespace_to_parse[0:actual_whitespace_index]
        left_ws = whitespace_to_parse[actual_whitespace_index:]
        LOGGER.debug(
            "accumulated_whitespace_count>>%s", str(accumulated_whitespace_count)
        )
        LOGGER.debug("actual_whitespace_index>>%s", str(actual_whitespace_index))
        LOGGER.debug("adj_ws>>%s<<", ParserHelper.make_value_visible(adj_ws))
        LOGGER.debug("left_ws>>%s<<", ParserHelper.make_value_visible(left_ws))
        LOGGER.debug("offset_index>>%s<<", str(offset_index))

        return accumulated_whitespace_count, actual_whitespace_index, adj_ws, left_ws

    # pylint: disable=too-many-arguments, too-many-locals
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
                LOGGER.debug(">>__adjust_for_list_start")
                (
                    did_process,
                    offset_index,
                    last_block_quote_index,
                ) = LeafBlockProcessor.__adjust_for_list_start(
                    parser_state,
                    last_list_start_index,
                    last_block_quote_index,
                )
                LOGGER.debug("<<__adjust_for_list_start<<%s", str(did_process))

                force_me = False
                kludge_adjust = 0
                if not did_process:
                    LOGGER.debug(">>>>%s", str(parser_state.token_stack[-1]))
                    if parser_state.token_stack[-1].is_list:
                        LOGGER.debug(
                            ">>indent>>%s",
                            parser_state.token_stack[-1].indent_level,
                        )
                        last_block_quote_index = 0
                        kludge_adjust = 1
                        force_me = True

                LOGGER.debug(">>__adjust_for_block_quote_start")
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
                LOGGER.debug("<<__adjust_for_block_quote_start<<%s", str(did_process))

                LOGGER.debug(
                    "__recalculate_whitespace>>%s>>%s",
                    whitespace_to_parse,
                    str(offset_index),
                )
                (
                    accumulated_whitespace_count,
                    actual_whitespace_index,
                    adj_ws,
                    left_ws,
                ) = LeafBlockProcessor.__recalculate_whitespace(
                    special_parse_start_index, whitespace_to_parse, offset_index
                )

                # TODO revisit with tabs
                line_number = position_marker.line_number
                column_number = (
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
                    LOGGER.debug(
                        "column_number(%s)=actual_whitespace_index(%s)+special_parse_start_index(%s)+block_quote_adjust_delta(%s)",
                        str(column_number),
                        str(actual_whitespace_index),
                        str(special_parse_start_index),
                        str(block_quote_adjust_delta),
                    )
                    excess_whitespace_count = (
                        accumulated_whitespace_count - 4 - offset_index
                    )
                    LOGGER.debug(
                        "excess_whitespace_count(%s)=accumulated_whitespace_count(%s)-4-offset_index(%s)",
                        str(excess_whitespace_count),
                        str(accumulated_whitespace_count),
                        str(offset_index),
                    )
                    LOGGER.debug(
                        "before>>%s>>", ParserHelper.make_value_visible(left_ws)
                    )
                    if excess_whitespace_count:
                        excess_whitespace_count -= kludge_adjust
                        left_ws = (
                            ParserHelper.repeat_string(
                                ParserHelper.space_character, excess_whitespace_count
                            )
                            + left_ws
                        )
                    LOGGER.debug(
                        "after>>%s>>", ParserHelper.make_value_visible(left_ws)
                    )
                else:
                    column_number += actual_whitespace_index
                LOGGER.debug("column_number>>%s", str(column_number))

                new_token = IndentedCodeBlockMarkdownToken(
                    adj_ws, line_number, column_number
                )
                parser_state.token_stack.append(IndentedCodeBlockStackToken(new_token))
                new_tokens.append(new_token)
                extracted_whitespace = left_ws
                LOGGER.debug(
                    "left_ws>>%s<<",
                    ParserHelper.make_value_visible(extracted_whitespace),
                )
            new_tokens.append(
                TextMarkdownToken(
                    position_marker.text_to_parse[position_marker.index_number :],
                    extracted_whitespace,
                    position_marker=position_marker,
                )
            )
        return new_tokens

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def is_thematic_break(
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check=False,
    ):
        """
        Determine whether or not we have a thematic break.
        """

        thematic_break_character = None
        end_of_break_index = None
        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            or skip_whitespace_check
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, LeafBlockProcessor.__thematic_break_characters
        ):
            start_char = line_to_parse[start_index]
            index = start_index

            char_count = 0
            repeat_loop = True
            while repeat_loop and index < len(line_to_parse):
                if ParserHelper.is_character_at_index_whitespace(line_to_parse, index):
                    index += 1
                elif line_to_parse[index] == start_char:
                    index += 1
                    char_count += 1
                else:
                    repeat_loop = False

            if char_count >= 3 and index == len(line_to_parse):
                thematic_break_character = start_char
                end_of_break_index = index

        return thematic_break_character, end_of_break_index

    @staticmethod
    def parse_thematic_break(
        parser_state,
        position_marker,
        extracted_whitespace,
        this_bq_count,
        stack_bq_count,
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
            # TODO why not use close?
            force_paragraph_close_if_present = False
            if this_bq_count == 0 and stack_bq_count > 0:
                force_paragraph_close_if_present = True
            if parser_state.token_stack[-1].is_paragraph:
                new_tokens.append(
                    parser_state.token_stack[
                        -1
                    ].generate_close_markdown_token_from_stack_token(
                        was_forced=force_paragraph_close_if_present
                    )
                )
                del parser_state.token_stack[-1]
            if this_bq_count == 0 and stack_bq_count > 0:
                new_tokens, _, _ = parser_state.close_open_blocks_fn(
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
    def is_atx_heading(line_to_parse, start_index, extracted_whitespace):
        """
        Determine whether or not an ATX Heading is about to start.
        """

        if ParserHelper.is_length_less_than_or_equal_to(
            extracted_whitespace, 3
        ) and ParserHelper.is_character_at_index(
            line_to_parse,
            start_index,
            LeafBlockProcessor.__atx_character,
        ):
            hash_count, new_index = ParserHelper.collect_while_character(
                line_to_parse,
                start_index,
                LeafBlockProcessor.__atx_character,
            )
            (
                non_whitespace_index,
                extracted_whitespace_at_start,
            ) = ParserHelper.extract_whitespace(line_to_parse, new_index)

            if hash_count <= 6 and (
                extracted_whitespace_at_start
                or non_whitespace_index == len(line_to_parse)
            ):
                return (
                    True,
                    non_whitespace_index,
                    hash_count,
                    extracted_whitespace_at_start,
                )
        return False, None, None, None

    # pylint: disable=too-many-locals
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
            LOGGER.debug(
                "parse_atx_headings>>start",
            )

            old_top_of_stack = parser_state.token_stack[-1]

            new_tokens, _, _ = parser_state.close_open_blocks_fn(
                parser_state, new_tokens
            )
            remaining_line = position_marker.text_to_parse[non_whitespace_index:]
            (
                end_index,
                extracted_whitespace_at_end,
            ) = ParserHelper.extract_whitespace_from_end(remaining_line)
            remove_trailing_count = 0
            while (
                end_index > 0
                and remaining_line[end_index - 1] == LeafBlockProcessor.__atx_character
            ):
                end_index -= 1
                remove_trailing_count += 1
            extracted_whitespace_before_end = ""
            if remove_trailing_count:
                if end_index > 0:
                    if ParserHelper.is_character_at_index_whitespace(
                        remaining_line, end_index - 1
                    ):
                        remaining_line = remaining_line[:end_index]
                        (
                            end_index,
                            extracted_whitespace_before_end,
                        ) = ParserHelper.extract_whitespace_from_end(remaining_line)
                        remaining_line = remaining_line[:end_index]
                    else:
                        extracted_whitespace_at_end = ""
                        remove_trailing_count = 0
                else:
                    remaining_line = ""
            else:
                extracted_whitespace_at_end = remaining_line[end_index:]
                remaining_line = remaining_line[0:end_index]
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

    # pylint: enable=too-many-locals

    @staticmethod
    def parse_setext_headings(
        parser_state,
        position_marker,
        extracted_whitespace,
        this_bq_count,
        stack_bq_count,
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
            and (this_bq_count == stack_bq_count)
        ):
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
            if after_whitespace_index == len(position_marker.text_to_parse):

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
        return new_tokens

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    @staticmethod
    def parse_paragraph(
        parser_state,
        position_marker,
        extracted_whitespace,
        this_bq_count,
        stack_bq_count,
        text_removed_by_container,
        force_it,
    ):
        """
        Handle the parsing of a paragraph.
        """
        new_tokens = []

        if parser_state.no_para_start_if_empty and position_marker.index_number >= len(
            position_marker.text_to_parse
        ):
            LOGGER.debug("Escaping paragraph due to empty w/ blank")
            return [
                BlankLineMarkdownToken(
                    extracted_whitespace, position_marker, len(extracted_whitespace)
                )
            ]

        LOGGER.debug(
            "parse_paragraph>stack_bq_count>%s>this_bq_count>%s<",
            str(stack_bq_count),
            str(this_bq_count),
        )

        top_list_token = None
        top_block_token = None
        for stack_index in range(len(parser_state.token_stack) - 1, 0, -1):
            if parser_state.token_stack[stack_index].is_list:
                top_list_token = parser_state.token_stack[stack_index]
                break
            if parser_state.token_stack[stack_index].is_block_quote:
                top_block_token = parser_state.token_stack[stack_index]
                break

        adjusted_whitespace_length = 0
        LOGGER.debug(">>list-owners>>%s", str(top_list_token))
        LOGGER.debug(">>block-owners>>%s", str(top_block_token))
        if top_block_token:
            LeafBlockProcessor.__adjust_paragraph_for_block_quotes(
                top_block_token,
                extracted_whitespace,
                text_removed_by_container,
                force_it,
                parser_state.token_document,
            )

        if top_list_token:
            adjusted_whitespace_length = LeafBlockProcessor.__adjust_paragraph_for_list(
                top_list_token, extracted_whitespace
            )

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
            new_tokens, _, _ = parser_state.close_open_blocks_fn(
                parser_state, until_this_index=last_list_index
            )

        if stack_bq_count != 0 and this_bq_count == 0:
            new_tokens, _, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[BlockQuoteStackToken],
                include_block_quotes=True,
            )

        if adjusted_whitespace_length:
            LOGGER.debug(">>GGHHJJ!!>>%s>>", str(adjusted_whitespace_length))
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

        new_tokens.append(
            TextMarkdownToken(
                position_marker.text_to_parse[position_marker.index_number :],
                extracted_whitespace,
                position_marker=position_marker,
            )
        )
        return new_tokens

    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-locals

    @staticmethod
    def __adjust_paragraph_for_list(top_list_token, extracted_whitespace):
        ex_ws_length = len(extracted_whitespace)
        LOGGER.debug(">>owners-indent>>%s", str(top_list_token.indent_level))
        LOGGER.debug(">>ws_before_marker>>%s", str(top_list_token.ws_before_marker))
        LOGGER.debug(">>ws_after_marker>>%s", str(top_list_token.ws_after_marker))
        LOGGER.debug(
            ">>last_new_list_token>>%s", str(top_list_token.last_new_list_token)
        )
        LOGGER.debug(">>extracted_whitespace>>%s", str(ex_ws_length))

        dominant_indent = top_list_token.indent_level
        if top_list_token.last_new_list_token:
            dominant_indent = top_list_token.last_new_list_token.indent_level
        LOGGER.debug(">>dominant_indent>>%s>>", str(dominant_indent))

        original_list_indent = top_list_token.indent_level - 2
        indent_delta = 0
        if top_list_token.ws_after_marker > 1:
            indent_delta = top_list_token.ws_after_marker - 1
        original_text_indent = (
            ex_ws_length
            + top_list_token.indent_level
            - top_list_token.ws_before_marker
            - indent_delta
        )
        LOGGER.debug(">>original_list_indent>>%s>>", str(original_list_indent))
        LOGGER.debug(">>original_text_indent>%s>>", str(original_text_indent))
        adjusted_whitespace_length = 0
        if dominant_indent > original_text_indent >= 4:
            adjusted_whitespace_length = dominant_indent - original_text_indent
        return adjusted_whitespace_length

    @staticmethod
    def __adjust_paragraph_for_block_quotes(
        top_block_token,
        extracted_whitespace,
        text_removed_by_container,
        force_it,
        token_document,
    ):
        LOGGER.debug(
            ">>list-owners>>%s", ParserHelper.make_value_visible(token_document)
        )
        number_of_block_quotes = 0
        end_index = len(token_document) - 1
        while token_document[end_index].is_block_quote_end:
            number_of_block_quotes += 1
            end_index -= 1
        if (
            number_of_block_quotes > 0
            and token_document[end_index].is_fenced_code_block_end
        ):
            LOGGER.debug(">>block quote does not need adjusting")
        else:
            LOGGER.debug(
                ">>top_block_token.md>>%s",
                ParserHelper.make_value_visible(
                    top_block_token.matching_markdown_token
                ),
            )
            LOGGER.debug(
                ">>top_block_token.lsi>>%s",
                ParserHelper.make_value_visible(
                    top_block_token.matching_markdown_token.leading_text_index
                ),
            )
            LOGGER.debug(">>extracted_whitespace>>%s>>", extracted_whitespace)
            LOGGER.debug(
                ">>text_removed_by_container>>[%s]>>",
                ParserHelper.make_value_visible(text_removed_by_container),
            )
            LOGGER.debug(
                ">>force_it>>[%s]>>",
                str(force_it),
            )
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

        LOGGER.debug(">>__xx>>removed_chars_at_start>%s>>", str(removed_chars_at_start))
        if not old_top_of_stack.is_paragraph:
            LOGGER.debug("1")
            return html_tokens

        statck_index = -1
        if was_token_already_added_to_stack:
            statck_index = -2
        if not parser_state.token_stack[statck_index].is_list:
            LOGGER.debug("2")
            return html_tokens

        LOGGER.debug(">>__xx>>stack>>%s>>", str(parser_state.token_stack))
        LOGGER.debug(">>__xx>>tokens>>%s>>", str(parser_state.token_document))
        LOGGER.debug(">>__xx>>tokens_to_add>>%s>>", str(html_tokens))

        top_of_stack = None
        if was_token_already_added_to_stack:
            top_of_stack = parser_state.token_stack[-1]
            del parser_state.token_stack[-1]
        end_of_list = html_tokens[-1]
        del html_tokens[-1]

        LOGGER.debug(">>__xx>>stack>>%s>>", str(parser_state.token_stack))
        LOGGER.debug(">>__xx>>tokens_to_add>>%s>>", str(html_tokens))

        repeat_loop = True
        while repeat_loop:
            assert parser_state.token_stack[-1].is_list

            LOGGER.debug(">>removed_chars_at_start>>%s>>", str(removed_chars_at_start))
            LOGGER.debug(
                ">>stack indent>>%s>>", str(parser_state.token_stack[-1].indent_level)
            )
            if removed_chars_at_start >= parser_state.token_stack[-1].indent_level:
                repeat_loop = False
            else:
                tokens_from_close, _, _ = parser_state.close_open_blocks_fn(
                    parser_state,
                    until_this_index=(len(parser_state.token_stack) - 1),
                    include_lists=True,
                )
                LOGGER.debug(">>__xx>>tokens_from_close>>%s>>", str(tokens_from_close))
                html_tokens.extend(tokens_from_close)

        assert parser_state.token_stack[-1].is_list
        last_indent = parser_state.token_stack[-1].indent_level
        delta_indent = removed_chars_at_start - last_indent
        LOGGER.debug(">>__xx>>delta_indent>>%s>>", str(delta_indent))
        assert not delta_indent

        if was_token_already_added_to_stack:
            parser_state.token_stack.append(top_of_stack)
            LOGGER.debug(">>__xx>>stack>>%s>>", str(parser_state.token_stack))
        html_tokens.append(end_of_list)
        LOGGER.debug(">>__xx>>tokens_to_add>>%s>>", str(html_tokens))

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
            LOGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_theme_break>>%s",
                str(is_leaf_block_start),
            )
        if not is_leaf_block_start:
            is_leaf_block_start, _ = HtmlHelper.is_html_block(
                line_to_parse,
                start_index,
                extracted_whitespace,
                parser_state.token_stack,
            )
            is_leaf_block_start = bool(is_leaf_block_start)
            LOGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_html_block>>%s",
                str(is_leaf_block_start),
            )
        if not is_leaf_block_start:
            is_leaf_block_start, _, _, _ = LeafBlockProcessor.is_fenced_code_block(
                line_to_parse, start_index, extracted_whitespace
            )
            is_leaf_block_start = bool(is_leaf_block_start)
            LOGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_fenced_code_block>>%s",
                str(is_leaf_block_start),
            )
        if not is_leaf_block_start:
            is_leaf_block_start, _, _, _ = LeafBlockProcessor.is_atx_heading(
                line_to_parse, start_index, extracted_whitespace
            )
            is_leaf_block_start = bool(is_leaf_block_start)
            LOGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_atx_heading>>%s",
                str(is_leaf_block_start),
            )
        return is_leaf_block_start
