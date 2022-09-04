"""
Module to provide processing for the leaf blocks.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quote_data import BlockQuoteData
from pymarkdown.constants import Constants
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_markdown_token import (
    AtxHeadingMarkdownToken,
    FencedCodeBlockMarkdownToken,
    IndentedCodeBlockMarkdownToken,
    ParagraphMarkdownToken,
    SetextHeadingMarkdownToken,
    ThematicBreakMarkdownToken,
)
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.stack_token import (
    FencedCodeBlockStackToken,
    IndentedCodeBlockStackToken,
    ListStackToken,
    ParagraphStackToken,
    StackToken,
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
    def is_fenced_code_block(
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        skip_whitespace_check: bool = False,
    ) -> Tuple[bool, Optional[int], Optional[int], Optional[str], Optional[int]]:
        """
        Determine if we have the start of a fenced code block.
        """

        assert extracted_whitespace is not None
        after_fence_index: Optional[int] = None
        if (
            skip_whitespace_check
            or ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
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
            assert collected_count is not None
            assert new_index is not None
            after_fence_index = new_index
            (
                non_whitespace_index,
                extracted_whitespace_before_info_string,
            ) = ParserHelper.extract_ascii_whitespace(line_to_parse, new_index)

            if collected_count >= 3:
                POGGER.debug("ifcb:True")
                return (
                    True,
                    non_whitespace_index,
                    after_fence_index,
                    extracted_whitespace_before_info_string,
                    collected_count,
                )
        return False, None, None, None, None

    @staticmethod
    def parse_fenced_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
    ) -> Tuple[List[MarkdownToken], Optional[str]]:
        """
        Handle the parsing of a fenced code block
        """

        POGGER.debug(
            "line>>$>>index>>$>>",
            position_marker.text_to_parse,
            position_marker.index_number,
        )
        new_tokens: List[MarkdownToken] = []
        (
            is_fence_start,
            non_whitespace_index,
            after_fence_index,
            extracted_whitespace_before_info_string,
            collected_count,
        ) = LeafBlockProcessor.is_fenced_code_block(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
        )
        if is_fence_start and not parser_state.token_stack[-1].is_html_block:
            POGGER.debug("parse_fenced_code_block:fenced")
            assert collected_count is not None
            assert non_whitespace_index is not None
            assert after_fence_index is not None
            if parser_state.token_stack[-1].is_fenced_code_block:
                POGGER.debug("parse_fenced_code_block:check fence end")
                LeafBlockProcessor.__check_for_fenced_end(
                    parser_state,
                    position_marker,
                    collected_count,
                    non_whitespace_index,
                    extracted_whitespace,
                    new_tokens,
                    after_fence_index,
                )
            else:
                POGGER.debug("parse_fenced_code_block:check fence start")
                new_tokens = LeafBlockProcessor.__process_fenced_start(
                    parser_state,
                    position_marker,
                    non_whitespace_index,
                    collected_count,
                    extracted_whitespace,
                    extracted_whitespace_before_info_string,
                )
        elif parser_state.token_stack[-1].is_fenced_code_block:
            fenced_token = cast(FencedCodeBlockStackToken, parser_state.token_stack[-1])
            if fenced_token.whitespace_start_count and extracted_whitespace:
                current_whitespace_length = ParserHelper.calculate_length(
                    extracted_whitespace
                )
                whitespace_left = max(
                    0,
                    current_whitespace_length - fenced_token.whitespace_start_count,
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

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __add_fenced_tokens(
        parser_state: ParserState,
        position_marker: PositionMarker,
        non_whitespace_index: int,
        collected_count: int,
        extracted_whitespace: Optional[str],
        extracted_whitespace_before_info_string: Optional[str],
    ) -> Tuple[StackToken, List[MarkdownToken]]:
        (_, proper_end_index,) = ParserHelper.collect_backwards_while_one_of_characters(
            position_marker.text_to_parse, -1, Constants.ascii_whitespace
        )
        adjusted_string = position_marker.text_to_parse[:proper_end_index]
        non_whitespace_index = min(non_whitespace_index, len(adjusted_string))
        (
            after_extracted_text_index,
            extracted_text,
        ) = ParserHelper.extract_until_spaces(adjusted_string, non_whitespace_index)
        assert extracted_text is not None
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

        assert extracted_text is not None
        extracted_text = InlineHelper.handle_backslashes(extracted_text)
        text_after_extracted_text = InlineHelper.handle_backslashes(
            text_after_extracted_text
        )

        if pre_extracted_text == extracted_text:
            pre_extracted_text = ""
        if pre_text_after_extracted_text == text_after_extracted_text:
            pre_text_after_extracted_text = ""

        assert extracted_whitespace is not None
        assert extracted_whitespace_before_info_string is not None
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
        assert extracted_whitespace is not None
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
        return old_top_of_stack, new_tokens

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __process_fenced_start(
        parser_state: ParserState,
        position_marker: PositionMarker,
        non_whitespace_index: int,
        collected_count: int,
        extracted_whitespace: Optional[str],
        extracted_whitespace_before_info_string: Optional[str],
    ) -> List[MarkdownToken]:

        POGGER.debug("pfcb->check")
        new_tokens: List[MarkdownToken] = []
        if (
            position_marker.text_to_parse[position_marker.index_number]
            == LeafBlockProcessor.__fenced_start_tilde
            or LeafBlockProcessor.__fenced_start_backtick
            not in position_marker.text_to_parse[non_whitespace_index:]
        ):
            POGGER.debug("pfcb->start")

            old_top_of_stack, new_tokens = LeafBlockProcessor.__add_fenced_tokens(
                parser_state,
                position_marker,
                non_whitespace_index,
                collected_count,
                extracted_whitespace,
                extracted_whitespace_before_info_string,
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

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __check_for_fenced_end(
        parser_state: ParserState,
        position_marker: PositionMarker,
        collected_count: int,
        non_whitespace_index: int,
        extracted_whitespace: Optional[str],
        new_tokens: List[MarkdownToken],
        after_fence_index: int,
    ) -> None:
        POGGER.debug("pfcb->end")
        POGGER.debug("extracted_whitespace:$:", extracted_whitespace)
        POGGER.debug("non_whitespace_index:$:", non_whitespace_index)
        POGGER.debug("position_marker.text_to_parse:$:", position_marker.text_to_parse)
        POGGER.debug(
            "len(position_marker.text_to_parse):$:", len(position_marker.text_to_parse)
        )
        POGGER.debug("after_fence_index:$:", after_fence_index)

        after_fence_and_spaces_index, extracted_spaces = ParserHelper.extract_spaces(
            position_marker.text_to_parse, after_fence_index
        )
        assert after_fence_and_spaces_index is not None
        POGGER.debug("after_fence_and_spaces_index:$:", after_fence_and_spaces_index)

        fenced_token = cast(FencedCodeBlockStackToken, parser_state.token_stack[-1])
        if (
            fenced_token.code_fence_character
            == position_marker.text_to_parse[position_marker.index_number]
            and collected_count >= fenced_token.fence_character_count
            and after_fence_and_spaces_index >= len(position_marker.text_to_parse)
        ):
            assert extracted_whitespace is not None
            assert extracted_spaces is not None
            new_end_token = parser_state.token_stack[
                -1
            ].generate_close_markdown_token_from_stack_token(
                extracted_whitespace,
                extra_end_data=f"{extracted_spaces}:{collected_count}",
            )

            new_tokens.append(new_end_token)
            del parser_state.token_stack[-1]

    # pylint: enable=too-many-arguments

    @staticmethod
    def __recalculate_whitespace(
        whitespace_to_parse: Optional[str], offset_index: int
    ) -> Tuple[int, str, str]:
        """
        Recalculate the whitespace characteristics.
        """
        assert whitespace_to_parse is not None
        POGGER.debug(
            "whitespace_to_parse>>$>>",
            whitespace_to_parse,
        )
        actual_whitespace_index = 4 + offset_index
        adj_ws = whitespace_to_parse[:actual_whitespace_index]
        left_ws = whitespace_to_parse[actual_whitespace_index:]
        POGGER.debug("actual_whitespace_index>>$", actual_whitespace_index)
        POGGER.debug("adj_ws>>$<<", adj_ws)
        POGGER.debug("left_ws>>$<<", left_ws)

        return actual_whitespace_index, adj_ws, left_ws

    @staticmethod
    def parse_indented_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        removed_chars_at_start: Optional[int],
        last_block_quote_index: int,
    ) -> List[MarkdownToken]:

        """
        Handle the parsing of an indented code block
        """

        new_tokens: List[MarkdownToken] = []

        assert extracted_whitespace is not None
        assert removed_chars_at_start is not None
        if (
            ParserHelper.is_length_greater_than_or_equal_to(
                extracted_whitespace, 4, start_index=removed_chars_at_start
            )
            and not parser_state.token_stack[-1].is_paragraph
        ):
            POGGER.debug(
                "parse_indented_code_block>>start",
            )
            if not parser_state.token_stack[-1].is_indented_code_block:
                (
                    last_block_quote_index,
                    extracted_whitespace,
                ) = LeafBlockProcessor.__create_indented_block(
                    parser_state,
                    last_block_quote_index,
                    position_marker,
                    extracted_whitespace,
                    new_tokens,
                )

            assert extracted_whitespace is not None
            new_tokens.append(
                TextMarkdownToken(
                    position_marker.text_to_parse[position_marker.index_number :],
                    extracted_whitespace,
                    position_marker=position_marker,
                )
            )
        else:
            POGGER.debug(
                "parse_indented_code_block>>not eligible",
            )
        return new_tokens

    @staticmethod
    def __create_indented_block(
        parser_state: ParserState,
        last_block_quote_index: int,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        new_tokens: List[MarkdownToken],
    ) -> Tuple[int, Optional[str]]:

        assert extracted_whitespace is not None
        line_number, column_number = position_marker.line_number, (
            position_marker.index_number
            + position_marker.index_indent
            - len(extracted_whitespace)
            + 1
        )
        (
            last_block_quote_index,
            actual_whitespace_index,
            adj_ws,
            extracted_whitespace,
        ) = LeafBlockProcessor.__prepare_for_indented_block(
            parser_state,
            last_block_quote_index,
            extracted_whitespace,
        )

        column_number += actual_whitespace_index
        POGGER.debug("column_number>>$", column_number)

        new_token = IndentedCodeBlockMarkdownToken(adj_ws, line_number, column_number)
        parser_state.token_stack.append(IndentedCodeBlockStackToken(new_token))
        new_tokens.append(new_token)
        POGGER.debug("left_ws>>$<<", extracted_whitespace)

        return last_block_quote_index, extracted_whitespace

    @staticmethod
    def __prepare_for_indented_block(
        parser_state: ParserState,
        last_block_quote_index: int,
        extracted_whitespace: Optional[str],
    ) -> Tuple[int, int, str, str]:
        POGGER.debug(">>>>$", parser_state.token_stack[-1])
        if parser_state.token_stack[-1].is_list:
            list_token = cast(ListStackToken, parser_state.token_stack[-1])
            POGGER.debug(
                ">>indent>>$",
                list_token.indent_level,
            )
            last_block_quote_index = 0

        POGGER.debug(
            "__recalculate_whitespace>>$>>$",
            extracted_whitespace,
            0,
        )
        (
            actual_whitespace_index,
            adj_ws,
            left_ws,
        ) = LeafBlockProcessor.__recalculate_whitespace(extracted_whitespace, 0)
        return (
            last_block_quote_index,
            actual_whitespace_index,
            adj_ws,
            left_ws,
        )

    @staticmethod
    def is_thematic_break(
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        skip_whitespace_check: bool = False,
        whitespace_allowed_between_characters: bool = True,
    ) -> Tuple[Optional[str], Optional[int]]:
        """
        Determine whether or not we have a thematic break.
        """

        assert extracted_whitespace is not None
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
            start_char, index, char_count, line_to_parse_size = (
                line_to_parse[start_index],
                start_index,
                0,
                len(line_to_parse),
            )

            while index < line_to_parse_size:
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
                    break  # pragma: no cover

            POGGER.debug("char_count>>$", char_count)
            POGGER.debug("index>>$", index)
            POGGER.debug("line_to_parse_size>>$", line_to_parse_size)
            if char_count >= 3 and index == line_to_parse_size:
                thematic_break_character, end_of_break_index = start_char, index

        return thematic_break_character, end_of_break_index

    @staticmethod
    def parse_thematic_break(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        block_quote_data: BlockQuoteData,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of a thematic break.
        """

        new_tokens: List[MarkdownToken] = []

        start_char, index = LeafBlockProcessor.is_thematic_break(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
        )
        if start_char:
            POGGER.debug(
                "parse_thematic_break>>start",
            )
            if parser_state.token_stack[-1].is_paragraph:
                force_paragraph_close_if_present = (
                    block_quote_data.current_count == 0
                    and block_quote_data.stack_count > 0
                )
                new_tokens, _ = parser_state.close_open_blocks_fn(
                    parser_state,
                    only_these_blocks=[ParagraphStackToken],
                    was_forced=force_paragraph_close_if_present,
                )

            assert (
                block_quote_data.current_count != 0 or block_quote_data.stack_count <= 0
            )
            # new_tokens, _ = parser_state.close_open_blocks_fn(
            #     parser_state,
            #     only_these_blocks=[BlockQuoteStackToken],
            #     include_block_quotes=True,
            #     was_forced=True,
            # )
            new_tokens.append(
                ThematicBreakMarkdownToken(
                    start_char,
                    extracted_whitespace,
                    position_marker.text_to_parse[position_marker.index_number : index],
                    position_marker=position_marker,
                )
            )
        else:
            POGGER.debug(
                "parse_thematic_break>>not eligible",
            )
        return new_tokens

    @staticmethod
    def is_atx_heading(
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        skip_whitespace_check: bool = False,
    ) -> Tuple[bool, Optional[int], Optional[int], Optional[str]]:
        """
        Determine whether or not an ATX Heading is about to start.
        """

        assert extracted_whitespace is not None
        if (
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            or skip_whitespace_check
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

            assert new_index is not None
            non_whitespace_index, _ = ParserHelper.collect_while_spaces(
                line_to_parse, new_index
            )
            extracted_whitespace_at_start = line_to_parse[
                new_index:non_whitespace_index
            ]

            assert hash_count is not None
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

    @staticmethod
    def parse_atx_headings(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of an atx heading.
        """

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
            assert extracted_whitespace_at_start is not None
            POGGER.debug(
                "parse_atx_headings>>start",
            )

            assert non_whitespace_index is not None
            (
                old_top_of_stack,
                remaining_line,
                remove_trailing_count,
                extracted_whitespace_before_end,
                extracted_whitespace_at_end,
                new_tokens,
            ) = LeafBlockProcessor.__prepare_for_create_atx_heading(
                parser_state, position_marker, [], non_whitespace_index
            )
            assert hash_count is not None
            assert extracted_whitespace is not None
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
                extracted_whitespace_at_end, extracted_whitespace_before_end
            )
            new_tokens.append(end_token)
        else:
            POGGER.debug(
                "parse_atx_headings>>not eligible",
            )
            new_tokens = []
        return new_tokens

    @staticmethod
    def __prepare_for_create_atx_heading(
        parser_state: ParserState,
        position_marker: PositionMarker,
        new_tokens: List[MarkdownToken],
        non_whitespace_index: int,
    ) -> Tuple[StackToken, str, int, str, str, List[MarkdownToken]]:
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

        new_tokens, _ = parser_state.close_open_blocks_fn(parser_state)
        (
            end_index,
            extracted_whitespace_at_end,
        ) = ParserHelper.extract_spaces_from_end(remaining_line)
        while (
            end_index > 0
            and remaining_line[end_index - 1] == LeafBlockProcessor.__atx_character
        ):
            end_index -= 1
            remove_trailing_count += 1
        if remove_trailing_count:
            if end_index > 0:
                if ParserHelper.is_character_at_index_whitespace(
                    remaining_line, end_index - 1
                ):
                    remaining_line = remaining_line[:end_index]
                    (
                        _,
                        new_non_whitespace_index,
                    ) = ParserHelper.collect_backwards_while_spaces(
                        remaining_line, len(remaining_line) - 1
                    )
                    assert new_non_whitespace_index is not None
                    end_index = new_non_whitespace_index
                    extracted_whitespace_before_end = remaining_line[end_index:]
                    remaining_line = remaining_line[:end_index]
                else:
                    extracted_whitespace_at_end, remove_trailing_count = "", 0
            else:
                remaining_line = ""
        else:
            extracted_whitespace_at_end = remaining_line[end_index:]
            remaining_line = remaining_line[:end_index]

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
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        block_quote_data: BlockQuoteData,
    ) -> List[MarkdownToken]:

        """
        Handle the parsing of an setext heading.
        """

        new_tokens: List[MarkdownToken] = []
        assert extracted_whitespace is not None
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
            POGGER.debug(
                "parse_setext_headings>>start",
            )
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
            assert collected_to_index is not None
            (
                after_whitespace_index,
                extra_whitespace_after_setext,
            ) = ParserHelper.extract_spaces(
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
        else:
            POGGER.debug(
                "parse_setext_headings>>not eligible",
            )
        return new_tokens

    @staticmethod
    def __adjust_continuation_for_active_list(
        parser_state: ParserState, position_marker: PositionMarker
    ) -> bool:
        is_paragraph_continuation: bool = (
            len(parser_state.token_stack) > 1 and parser_state.token_stack[-2].is_list
        )
        if is_paragraph_continuation:
            list_token = cast(ListStackToken, parser_state.token_stack[-2])
            POGGER.debug(
                "parser_state.original_line_to_parse>:$:<",
                parser_state.original_line_to_parse,
            )
            adj_text = position_marker.text_to_parse[position_marker.index_number :]
            assert parser_state.original_line_to_parse is not None
            assert parser_state.original_line_to_parse.endswith(adj_text)
            removed_text_length = len(parser_state.original_line_to_parse) - len(
                adj_text
            )
            POGGER.debug("removed_text_length>:$:<", removed_text_length)
            POGGER.debug("adj_text>:$:<", adj_text)
            POGGER.debug("indent_level>:$:<", list_token.indent_level)
            is_paragraph_continuation = (
                bool(adj_text) and removed_text_length < list_token.indent_level
            )
        return is_paragraph_continuation

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_setext_token(
        parser_state: ParserState,
        position_marker: PositionMarker,
        collected_to_index: int,
        new_tokens: List[MarkdownToken],
        extracted_whitespace: Optional[str],
        extra_whitespace_after_setext: Optional[str],
    ) -> None:
        token_index = len(parser_state.token_document) - 1
        while not parser_state.token_document[token_index].is_paragraph:
            token_index -= 1

        paragraph_token = cast(
            ParagraphMarkdownToken, parser_state.token_document[token_index]
        )
        assert paragraph_token.extra_data is not None
        replacement_token = SetextHeadingMarkdownToken(
            position_marker.text_to_parse[position_marker.index_number],
            collected_to_index - position_marker.index_number,
            paragraph_token.extra_data,
            position_marker,
            paragraph_token,
        )

        # This is unusual.  Normally, close_open_blocks is used to close off
        # blocks based on the stack token.  However, since the setext takes
        # the last paragraph of text (see case 61) and translates it
        # into a heading, this has to be done separately, as there is no
        # stack token to close.
        assert extra_whitespace_after_setext is not None
        assert extracted_whitespace is not None
        new_tokens.append(
            replacement_token.generate_close_markdown_token_from_markdown_token(
                extracted_whitespace, extra_whitespace_after_setext
            )
        )

        parser_state.token_document[token_index] = replacement_token
        del parser_state.token_stack[-1]

    # pylint: enable=too-many-arguments

    @staticmethod
    def correct_for_leaf_block_start_in_list(
        parser_state: ParserState,
        removed_chars_at_start: int,
        old_top_of_stack_token: StackToken,
        html_tokens: List[MarkdownToken],
        was_token_already_added_to_stack: bool = True,
    ) -> None:
        """
        Check to see that if a paragraph has been closed within a list and
        there is a leaf block token immediately following, that the right
        actions are taken.
        """

        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>removed_chars_at_start>$>>",
            removed_chars_at_start,
        )
        if not old_top_of_stack_token.is_paragraph:
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
            assert top_of_stack is not None
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
    def __handle_leaf_start(
        parser_state: ParserState,
        removed_chars_at_start: int,
        html_tokens: List[MarkdownToken],
    ) -> None:
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
            parser_state.token_stack,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

        is_remaining_list_token = True
        while is_remaining_list_token:
            assert parser_state.token_stack[-1].is_list
            list_stack_token = cast(ListStackToken, parser_state.token_stack[-1])

            POGGER.debug(">>removed_chars_at_start>>$>>", removed_chars_at_start)
            POGGER.debug(">>stack indent>>$>>", list_stack_token.indent_level)
            if removed_chars_at_start >= list_stack_token.indent_level:
                break  # pragma: no cover

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
            list_stack_token = cast(ListStackToken, parser_state.token_stack[-1])
            delta_indent = removed_chars_at_start - list_stack_token.indent_level
            POGGER.debug(
                ">>correct_for_leaf_block_start_in_list>>delta_indent>>$>>",
                delta_indent,
            )
            assert not delta_indent

    @staticmethod
    def is_paragraph_ending_leaf_block_start(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        exclude_thematic_break: bool = False,
    ) -> bool:
        """
        Determine whether we have a valid leaf block start.
        """

        is_leaf_block_start = not exclude_thematic_break
        assert not exclude_thematic_break

        is_thematic_break_start, _ = LeafBlockProcessor.is_thematic_break(
            line_to_parse,
            start_index,
            extracted_whitespace,
            skip_whitespace_check=True,
        )
        is_leaf_block_start = bool(is_thematic_break_start)
        POGGER.debug(
            "is_paragraph_ending_leaf_block_start>>is_theme_break>>$",
            is_leaf_block_start,
        )
        if not is_leaf_block_start:
            is_html_block_start, _ = HtmlHelper.is_html_block(
                line_to_parse,
                start_index,
                extracted_whitespace,
                parser_state.token_stack,
            )
            is_leaf_block_start = bool(is_html_block_start)
            POGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_html_block>>$",
                is_leaf_block_start,
            )
        if not is_leaf_block_start:
            is_leaf_block_start, _, _, _, _ = LeafBlockProcessor.is_fenced_code_block(
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
        POGGER.debug(
            "is_paragraph_ending_leaf_block_start<<$",
            is_leaf_block_start,
        )
        return is_leaf_block_start
