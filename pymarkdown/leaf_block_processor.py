"""
Module to provide processing for the leaf blocks.
"""
import logging
from typing import List, Optional, Tuple

from pymarkdown.block_quote_data import BlockQuoteData
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
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
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
    def is_fenced_code_block(
        line_to_parse, start_index, extracted_whitespace, skip_whitespace_check=False
    ):
        """
        Determine if we have the start of a fenced code block.
        """

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

            extracted_text = InlineHelper.handle_backslashes(extracted_text)
            text_after_extracted_text = InlineHelper.handle_backslashes(
                text_after_extracted_text
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
        POGGER.debug("last_list_start_index>>$>>", last_list_start_index)
        POGGER.debug(
            "parser_state.original_line_to_parse>>$>>",
            parser_state.original_line_to_parse,
        )
        return last_block_quote_index

    @staticmethod
    def __recalculate_whitespace(whitespace_to_parse, offset_index):
        """
        Recalculate the whitespace characteristics.
        """
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

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_indented_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        removed_chars_at_start: Optional[int],
        last_block_quote_index: int,
        last_list_start_index: int,
    ) -> List[MarkdownToken]:

        """
        Handle the parsing of an indented code block
        """

        new_tokens: List[MarkdownToken] = []

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

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_indented_block(
        parser_state,
        last_list_start_index,
        last_block_quote_index,
        position_marker,
        extracted_whitespace,
        new_tokens,
    ):
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
            last_list_start_index,
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

    # pylint: enable=too-many-arguments

    @staticmethod
    def __prepare_for_indented_block(
        parser_state,
        last_list_start_index,
        last_block_quote_index,
        extracted_whitespace,
    ):
        POGGER.debug(">>__adjust_for_list_start")
        (last_block_quote_index) = LeafBlockProcessor.__adjust_for_list_start(
            parser_state,
            last_list_start_index,
            last_block_quote_index,
        )

        POGGER.debug(">>>>$", parser_state.token_stack[-1])
        if parser_state.token_stack[-1].is_list:
            POGGER.debug(
                ">>indent>>$",
                parser_state.token_stack[-1].indent_level,
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
        return new_tokens

    @staticmethod
    def is_atx_heading(
        line_to_parse, start_index, extracted_whitespace, skip_whitespace_check=False
    ):
        """
        Determine whether or not an ATX Heading is about to start.
        """

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
                parser_state, position_marker, [], non_whitespace_index
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
                extracted_whitespace_at_end, extracted_whitespace_before_end
            )
            new_tokens.append(end_token)
        else:
            new_tokens = []
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

        new_tokens, _ = parser_state.close_open_blocks_fn(parser_state)
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
        is_paragraph_continuation = (
            len(parser_state.token_stack) > 1 and parser_state.token_stack[-2].is_list
        )
        if is_paragraph_continuation:
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
            is_paragraph_continuation = (
                adj_text
                and removed_text_length < parser_state.token_stack[-2].indent_level
            )
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
                extracted_whitespace, extra_whitespace_after_setext
            )
        )

        parser_state.token_document[token_index] = replacement_token
        del parser_state.token_stack[-1]

    # pylint: enable=too-many-arguments

    @staticmethod
    def parse_paragraph(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        block_quote_data: BlockQuoteData,
        text_removed_by_container: str,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of a paragraph.
        """
        POGGER.debug(">>text_removed_by_container>>:$:<<", text_removed_by_container)
        assert extracted_whitespace is not None
        if parser_state.no_para_start_if_empty and position_marker.index_number >= len(
            position_marker.text_to_parse
        ):
            POGGER.debug("Escaping paragraph due to empty w/ blank")
            POGGER.debug(
                "position_marker.text_to_parse=:$:", position_marker.text_to_parse
            )
            POGGER.debug(
                "position_marker.index_number=:$:", position_marker.index_number
            )
            POGGER.debug(
                "position_marker.index_indent=:$:", position_marker.index_indent
            )
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
                    extracted_whitespace,
                    adjusted_whitespace_length,
                )
            )

        new_tokens, extracted_whitespace = LeafBlockProcessor.__handle_paragraph_prep(
            parser_state,
            block_quote_data,
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

    @staticmethod
    def __handle_paragraph_prep(
        parser_state,
        block_quote_data,
        position_marker,
        extracted_whitespace,
    ):

        # In cases where the list ended on the same line as we are processing, the
        # container tokens will not yet be added to the token_document.  As such,
        # make sure to construct a "proper" list that takes those into account
        # before checking to see if this is an issue.
        adjusted_document = parser_state.token_document[:]
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
        elif block_quote_data.stack_count != 0 and block_quote_data.current_count == 0:
            new_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[BlockQuoteStackToken],
                include_block_quotes=True,
            )
        else:
            new_tokens = []

        if not parser_state.token_stack[-1].is_paragraph:
            new_paragraph_token = ParagraphMarkdownToken(
                extracted_whitespace, position_marker
            )
            parser_state.token_stack.append(ParagraphStackToken(new_paragraph_token))
            new_tokens.append(new_paragraph_token)
            extracted_whitespace = ""
        return new_tokens, extracted_whitespace

    @staticmethod
    def __adjust_paragraph_for_containers(
        parser_state,
        container_index,
        extracted_whitespace,
        adjusted_whitespace_length,
    ):
        if not parser_state.token_stack[container_index].is_block_quote:
            top_list_token = parser_state.token_stack[container_index]
            POGGER.debug(">>list-owners>>$", top_list_token)
            adjusted_whitespace_length = LeafBlockProcessor.__adjust_paragraph_for_list(
                top_list_token, extracted_whitespace
            )
        POGGER.debug(">>adjusted_whitespace_length>>$", adjusted_whitespace_length)
        return adjusted_whitespace_length

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
    def check_for_list_in_process(parser_state: ParserState) -> Tuple[bool, int]:
        """
        From the end of the stack, check to see if there is already a list in progress.
        """

        stack_index = len(parser_state.token_stack) - 1

        while stack_index >= 0 and not parser_state.token_stack[stack_index].is_list:
            stack_index -= 1

        return stack_index >= 0, stack_index

    @staticmethod
    def correct_for_leaf_block_start_in_list(
        parser_state: ParserState,
        removed_chars_at_start: int,
        old_top_of_stack_token: MarkdownToken,
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

        is_remaining_list_token = True
        while is_remaining_list_token:
            assert parser_state.token_stack[-1].is_list

            POGGER.debug(">>removed_chars_at_start>>$>>", removed_chars_at_start)
            POGGER.debug(
                ">>stack indent>>$>>", parser_state.token_stack[-1].indent_level
            )
            if removed_chars_at_start >= parser_state.token_stack[-1].indent_level:
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
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        exclude_thematic_break: bool = False,
    ) -> bool:
        """
        Determine whether we have a valid leaf block start.
        """

        # TODO Can be Removed?
        POGGER.debug(
            "is_paragraph_ending_leaf_block_start, ex=$", exclude_thematic_break
        )
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
        POGGER.debug(
            "is_paragraph_ending_leaf_block_start<<$",
            is_leaf_block_start,
        )
        return is_leaf_block_start
