"""
Module to help with the parsing of text inline elements.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.container_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.emphasis_helper import EmphasisHelper
from pymarkdown.inline.inline_handler_helper import InlineHandlerHelper
from pymarkdown.inline.inline_helper import InlineHelper
from pymarkdown.inline.inline_line_end_helper import InlineLineEndHelper
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.inline.inline_response import InlineResponse
from pymarkdown.inline.inline_tabified_text_block_helper import (
    InlineTabifiedTextBlockHelper,
)
from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_markdown_token import ParagraphMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods


class InlineTextBlockHelper:
    """
    Class to help with the parsing of text inline elements.
    """

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod  # noqa: C901
    def process_inline_text_block(  # noqa: C901
        source_text: str,
        coalesced_stack: List[MarkdownToken],
        starting_whitespace: str = "",
        whitespace_to_recombine: Optional[str] = None,
        is_setext: bool = False,
        is_para: bool = False,
        para_space: Optional[str] = None,
        line_number: int = 0,
        column_number: int = 0,
        para_owner: Optional[ParagraphMarkdownToken] = None,
        tabified_text: Optional[str] = None,
    ) -> List[MarkdownToken]:
        """
        Process a text block for any inline items.

        Note: This is one of the more heavily traffic functions in the
        parser.  Debugging should be uncommented only if needed.
        """

        (
            last_line_number,
            last_column_number,
            current_string,
            current_string_unresolved,
        ) = (line_number, column_number, "", "")
        start_index: Optional[int] = 0
        inline_blocks: List[MarkdownToken] = []
        end_string: Optional[str] = ""
        fold_space: Optional[List[str]] = None

        if whitespace_to_recombine:
            source_text, _ = ParserHelper.recombine_string_with_whitespace(
                source_text, whitespace_to_recombine
            )
        if is_para or is_setext:
            assert para_space is not None
            fold_space = para_space.split(ParserHelper.newline_character)

        assert start_index is not None
        next_index = ParserHelper.index_any_of(
            source_text,
            InlineHandlerHelper.valid_inline_text_block_sequence_starts,
            start_index,
        )
        newlines_encountered = 0
        while next_index != -1:
            old_next_index = next_index
            assert start_index is not None
            (
                line_number,
                column_number,
                end_string,
                current_string,
                current_string_unresolved,
                starting_whitespace,
                fold_space,
                last_line_number,
                last_column_number,
                start_index,
                next_index,
            ) = InlineTextBlockHelper.__handle_next_inline_character(
                source_text,
                start_index,
                next_index,
                inline_blocks,
                current_string,
                current_string_unresolved,
                line_number,
                column_number,
                para_owner,
                coalesced_stack,
                end_string,
                is_setext,
                whitespace_to_recombine,
                starting_whitespace,
                last_line_number,
                last_column_number,
                fold_space,
                tabified_text,
                newlines_encountered,
            )
            if source_text[old_next_index] == "\n":
                newlines_encountered += 1

        return InlineTextBlockHelper.__complete_inline_block_processing(
            inline_blocks,
            source_text,
            start_index,
            current_string,
            end_string,
            starting_whitespace,
            is_setext,
            last_line_number,
            last_column_number,
            tabified_text,
            newlines_encountered,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_next_inline_character(
        source_text: str,
        start_index: int,
        next_index: int,
        inline_blocks: List[MarkdownToken],
        current_string: str,
        current_string_unresolved: str,
        line_number: int,
        column_number: int,
        para_owner: Optional[ParagraphMarkdownToken],
        coalesced_stack: List[MarkdownToken],
        end_string: Optional[str],
        is_setext: bool,
        whitespace_to_recombine: Optional[str],
        starting_whitespace: str,
        last_line_number: int,
        last_column_number: int,
        fold_space: Optional[List[str]],
        tabified_text: Optional[str],
        newlines_encountered: int,
    ) -> Tuple[
        int,
        int,
        Optional[str],
        str,
        str,
        str,
        Optional[List[str]],
        int,
        int,
        Optional[int],
        int,
    ]:
        (
            reset_current_string,
            remaining_line,
            old_inline_blocks_count,
            old_inline_blocks_last_token,
            tabified_remaining_line,
            inline_request,
        ) = InlineTextBlockHelper.__handle_next_inline_character_setup(
            source_text,
            start_index,
            next_index,
            inline_blocks,
            tabified_text,
            newlines_encountered,
            current_string_unresolved,
            line_number,
            column_number,
            para_owner,
        )

        (
            inline_response,
            line_number,
            column_number,
            was_column_number_reset,
            did_line_number_change,
            whitespace_to_add,
            remaining_line,
            end_string,
            current_string,
            was_new_line,
            tabified_remaining_line,
        ) = InlineTextBlockHelper.__handle_next_special_character(
            source_text,
            next_index,
            inline_request,
            line_number,
            column_number,
            coalesced_stack,
            InlineResponse(),
            remaining_line,
            end_string,
            current_string,
            inline_blocks,
            is_setext,
            whitespace_to_recombine,
            para_owner,
            tabified_text,
            tabified_remaining_line,
        )

        (
            reset_current_string,
            remaining_line,
            end_string,
            current_string,
            current_string_unresolved,
        ) = InlineTextBlockHelper.__cleanup_after_handling(
            inline_response,
            current_string,
            current_string_unresolved,
            remaining_line,
            tabified_remaining_line,
            reset_current_string,
            end_string,
        )

        (
            reset_current_string,
            starting_whitespace,
            end_string,
        ) = InlineTextBlockHelper.__create_new_text_token(
            inline_response,
            current_string,
            inline_blocks,
            starting_whitespace,
            end_string,
            last_line_number,
            last_column_number,
            reset_current_string,
        )

        (
            line_number,
            column_number,
            fold_space,
            current_string,
            current_string_unresolved,
            last_line_number,
            last_column_number,
            new_start_index,
            next_index,
            end_string,
        ) = InlineTextBlockHelper.__handle_next_inline_character_finish_handling(
            line_number,
            column_number,
            fold_space,
            was_new_line,
            coalesced_stack,
            remaining_line,
            did_line_number_change,
            was_column_number_reset,
            reset_current_string,
            inline_blocks,
            old_inline_blocks_count,
            old_inline_blocks_last_token,
            source_text,
            whitespace_to_add,
            inline_response,
            current_string,
            current_string_unresolved,
            last_line_number,
            last_column_number,
            end_string,
        )

        return (
            line_number,
            column_number,
            end_string,
            current_string,
            current_string_unresolved,
            starting_whitespace,
            fold_space,
            last_line_number,
            last_column_number,
            new_start_index,
            next_index,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_next_inline_character_setup(
        source_text: str,
        start_index: int,
        next_index: int,
        inline_blocks: List[MarkdownToken],
        tabified_text: Optional[str],
        newlines_encountered: int,
        current_string_unresolved: str,
        line_number: int,
        column_number: int,
        para_owner: Optional[ParagraphMarkdownToken],
    ) -> Tuple[bool, str, int, Optional[MarkdownToken], Optional[str], InlineRequest]:
        (
            remaining_line,
            old_inline_blocks_count,
            old_inline_blocks_last_token,
        ) = (
            source_text[start_index:next_index],
            len(inline_blocks),
            inline_blocks[-1] if inline_blocks else None,
        )
        tabified_remaining_line: Optional[str] = None
        if tabified_text:
            tabified_remaining_line = (
                InlineTabifiedTextBlockHelper.handle_next_inline_character_tabified(
                    source_text,
                    tabified_text,
                    newlines_encountered,
                    start_index,
                    next_index,
                )
            )

        inline_request = InlineRequest(
            source_text,
            next_index,
            inline_blocks,
            remaining_line,
            tabified_remaining_line,
            current_string_unresolved,
            line_number,
            column_number,
            para_owner,
            tabified_text,
        )
        return (
            False,
            remaining_line,
            old_inline_blocks_count,
            old_inline_blocks_last_token,
            tabified_remaining_line,
            inline_request,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __complete_inline_block_processing(
        inline_blocks: List[MarkdownToken],
        source_text: str,
        start_index: Optional[int],
        current_string: str,
        end_string: Optional[str],
        starting_whitespace: str,
        is_setext: bool,
        line_number: int,
        column_number: int,
        tabified_text: Optional[str],
        newlines_encountered: int,
    ) -> List[MarkdownToken]:
        POGGER.debug("__cibp>inline_blocks>$<", inline_blocks)
        POGGER.debug("__cibp>source_text>$<", source_text)
        POGGER.debug("__cibp>start_index>$<", start_index)
        POGGER.debug("__cibp>current_string>$<", current_string)
        POGGER.debug("__cibp>end_string>$<", end_string)
        POGGER.debug(
            "__cibp>starting_whitespace>$<",
            starting_whitespace,
        )
        POGGER.debug("__cibp>is_setext>$<", is_setext)
        POGGER.debug("__cibp>line_number>$<", line_number)
        POGGER.debug("__cibp>column_number>$<", column_number)

        assert start_index is not None
        if start_index < len(source_text):
            text_to_append = source_text[start_index:]
            POGGER.debug("text_to_append>:$:<", text_to_append)

            POGGER.debug("tabified_text=>:$:<", tabified_text)
            if tabified_text:
                assert tabified_text is not None
                text_to_append = InlineTabifiedTextBlockHelper.complete_inline_block_processing_tabified(
                    source_text, start_index, tabified_text, newlines_encountered
                )
                POGGER.debug("text_to_append>:$:<", text_to_append)

            POGGER.debug("current_string>:$:<", current_string)
            POGGER.debug("text_to_append>:$:<", text_to_append)
            current_string = InlineHelper.append_text(current_string, text_to_append)
            POGGER.debug("current_string>:$:<", current_string)

        have_processed_once = len(inline_blocks) != 0 or start_index != 0
        if current_string or not have_processed_once:
            InlineTextBlockHelper.__complete_inline_block_processing_build_token(
                current_string,
                end_string,
                starting_whitespace,
                is_setext,
                inline_blocks,
                line_number,
                column_number,
            )
        POGGER.debug(">>$<<", inline_blocks)

        EmphasisHelper.resolve_inline_emphasis(inline_blocks, None)
        return inline_blocks

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_next_special_character(
        source_text: str,
        next_index: int,
        inline_request: InlineRequest,
        line_number: int,
        column_number: int,
        coalesced_stack: List[MarkdownToken],
        inline_response: InlineResponse,
        remaining_line: str,
        end_string: Optional[str],
        current_string: str,
        inline_blocks: List[MarkdownToken],
        is_setext: bool,
        whitespace_to_recombine: Optional[str],
        para_owner: Optional[ParagraphMarkdownToken],
        tabified_text: Optional[str],
        tabified_remaining_line: Optional[str],
    ) -> Tuple[
        InlineResponse,
        int,
        int,
        bool,
        bool,
        Optional[str],
        str,
        Optional[str],
        str,
        bool,
        Optional[str],
    ]:
        if InlineHandlerHelper.has_handler(source_text[next_index]):
            whitespace_to_add, was_new_line = None, False
            (
                inline_response,
                line_number,
                column_number,
                was_column_number_reset,
                did_line_number_change,
            ) = InlineHandlerHelper.process_inline_handled_character(
                source_text,
                next_index,
                inline_request,
                line_number,
                column_number,
                coalesced_stack,
            )
        else:
            was_column_number_reset, did_line_number_change = False, False
            (
                whitespace_to_add,
                remaining_line,
                end_string,
                current_string,
                was_new_line,
                tabified_remaining_line,
            ) = InlineLineEndHelper.process_inline_new_line(
                source_text,
                next_index,
                inline_response,
                remaining_line,
                end_string,
                current_string,
                inline_blocks,
                is_setext,
                line_number,
                column_number,
                coalesced_stack,
                whitespace_to_recombine,
                para_owner,
                tabified_text,
                inline_request,
                tabified_remaining_line,
            )
        return (
            inline_response,
            line_number,
            column_number,
            was_column_number_reset,
            did_line_number_change,
            whitespace_to_add,
            remaining_line,
            end_string,
            current_string,
            was_new_line,
            tabified_remaining_line,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __complete_inline_block_processing_build_token(
        current_string: str,
        end_string: Optional[str],
        starting_whitespace: str,
        is_setext: bool,
        inline_blocks: List[MarkdownToken],
        line_number: int,
        column_number: int,
    ) -> None:
        POGGER.debug("__cibp>current_string>$<", current_string)
        POGGER.debug("__cibp>starting_whitespace>$<", starting_whitespace)
        if (
            is_setext
            and end_string is None
            and (inline_blocks and inline_blocks[-1].is_inline_hard_break)
        ):
            new_index, ex_ws = ParserHelper.extract_spaces(current_string, 0)
            POGGER.debug("__cibp>new_index>$<", new_index)
            POGGER.debug("__cibp>b>$<", ex_ws)
            if new_index:
                end_string = f"{ex_ws}{ParserHelper.whitespace_split_character}"
                current_string = current_string[new_index:]
        POGGER.debug("__cibp>end_string>$<", end_string)
        inline_blocks.append(
            TextMarkdownToken(
                current_string,
                starting_whitespace,
                end_whitespace=end_string,
                line_number=line_number,
                column_number=column_number,
            )
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_new_text_token(
        inline_response: InlineResponse,
        current_string: str,
        inline_blocks: List[MarkdownToken],
        starting_whitespace: str,
        end_string: Optional[str],
        last_line_number: int,
        last_column_number: int,
        reset_current_string: bool,
    ) -> Tuple[bool, str, Optional[str]]:
        if inline_response.new_tokens:
            if current_string:
                inline_blocks.append(
                    TextMarkdownToken(
                        current_string,
                        starting_whitespace,
                        end_whitespace=end_string,
                        line_number=last_line_number,
                        column_number=last_column_number,
                    )
                )
                reset_current_string, starting_whitespace, end_string = (
                    True,
                    "",
                    None,
                )
            elif starting_whitespace:
                inline_blocks.append(
                    TextMarkdownToken(
                        "",
                        ParserHelper.create_replace_with_nothing_marker(
                            starting_whitespace
                        ),
                        line_number=last_line_number,
                        column_number=last_column_number,
                    )
                )
                starting_whitespace = ""

            inline_blocks.extend(inline_response.new_tokens)
        return reset_current_string, starting_whitespace, end_string

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __cleanup_after_handling(
        inline_response: InlineResponse,
        current_string: str,
        current_string_unresolved: str,
        remaining_line: str,
        tabified_remaining_line: Optional[str],
        reset_current_string: bool,
        end_string: Optional[str],
    ) -> Tuple[bool, str, Optional[str], str, str]:
        if inline_response.consume_rest_of_line:
            # POGGER.debug("consume_rest_of_line>>$<", remaining_line)
            (
                inline_response.new_string,
                inline_response.new_tokens,
                reset_current_string,
                remaining_line,
                end_string,
            ) = ("", [], True, "", None)
        else:
            # POGGER.debug("append_rest_of_line>>rem>>$<", remaining_line)
            proper_remaining_line = tabified_remaining_line or remaining_line
            current_string, current_string_unresolved = (
                InlineHelper.append_text(
                    current_string,
                    proper_remaining_line,
                ),
                InlineHelper.append_text(
                    current_string_unresolved, proper_remaining_line
                ),
            )
        return (
            reset_current_string,
            remaining_line,
            end_string,
            current_string,
            current_string_unresolved,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_next_inline_character_finish_handling(
        line_number: int,
        column_number: int,
        fold_space: Optional[List[str]],
        was_new_line: bool,
        coalesced_stack: List[MarkdownToken],
        remaining_line: str,
        did_line_number_change: bool,
        was_column_number_reset: bool,
        reset_current_string: bool,
        inline_blocks: List[MarkdownToken],
        old_inline_blocks_count: int,
        old_inline_blocks_last_token: Optional[MarkdownToken],
        source_text: str,
        whitespace_to_add: Optional[str],
        inline_response: InlineResponse,
        current_string: str,
        current_string_unresolved: str,
        last_line_number: int,
        last_column_number: int,
        end_string: Optional[str],
    ) -> Tuple[
        int,
        int,
        Optional[List[str]],
        str,
        str,
        int,
        int,
        Optional[int],
        int,
        Optional[str],
    ]:
        (
            line_number,
            column_number,
            fold_space,
        ) = InlineTextBlockHelper.__adjust_line_and_column_number(
            was_new_line,
            coalesced_stack,
            line_number,
            column_number,
            fold_space,
            remaining_line,
            did_line_number_change,
            was_column_number_reset,
        )

        (
            current_string,
            current_string_unresolved,
            last_line_number,
            last_column_number,
        ) = InlineTextBlockHelper.__fix_variables_before_next_loop(
            reset_current_string,
            current_string,
            current_string_unresolved,
            inline_blocks,
            old_inline_blocks_count,
            old_inline_blocks_last_token,
            last_line_number,
            last_column_number,
            line_number,
            column_number,
        )

        (
            new_start_index,
            next_index,
            end_string,
            current_string,
            current_string_unresolved,
        ) = InlineTextBlockHelper.__complete_inline_loop(
            source_text,
            inline_response.new_index,
            end_string,
            whitespace_to_add,
            current_string,
            current_string_unresolved,
            inline_response.new_string_unresolved,
            inline_response.new_string,
            inline_response.original_string,
        )
        return (
            line_number,
            column_number,
            fold_space,
            current_string,
            current_string_unresolved,
            last_line_number,
            last_column_number,
            new_start_index,
            next_index,
            end_string,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_line_and_column_number(
        was_new_line: bool,
        coalesced_stack: List[MarkdownToken],
        line_number: int,
        column_number: int,
        fold_space: Optional[List[str]],
        remaining_line: str,
        did_line_number_change: bool,
        was_column_number_reset: bool,
    ) -> Tuple[int, int, Optional[List[str]]]:
        if was_new_line:
            column_number = 1
            if coalesced_stack and coalesced_stack[-1].is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, coalesced_stack[-1])
                POGGER.debug(
                    "coalesced_list[-1]..leading_text_index=$",
                    block_quote_token.leading_text_index,
                )
                assert block_quote_token.bleading_spaces is not None
                split_leading_spaces = block_quote_token.bleading_spaces.split(
                    ParserHelper.newline_character
                )
                selected_split_length = len(
                    split_leading_spaces[block_quote_token.leading_text_index]
                )
                column_number += selected_split_length

            line_number += 1
            assert fold_space
            fold_space = fold_space[1:]
            column_number += len(fold_space[0])
        elif not was_column_number_reset:
            column_number += len(remaining_line)
        else:
            assert did_line_number_change
            if coalesced_stack and coalesced_stack[-1].is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, coalesced_stack[-1])
                POGGER.debug(
                    "coalesced_list[-1].leading_text_index=$",
                    block_quote_token.leading_text_index,
                )
                assert block_quote_token.bleading_spaces is not None
                split_leading_spaces = block_quote_token.bleading_spaces.split(
                    ParserHelper.newline_character
                )
                selected_split_length = len(
                    split_leading_spaces[block_quote_token.leading_text_index]
                )
                column_number += selected_split_length
        return line_number, column_number, fold_space

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __fix_variables_before_next_loop(
        reset_current_string: bool,
        current_string: str,
        current_string_unresolved: str,
        inline_blocks: List[MarkdownToken],
        old_inline_blocks_count: int,
        old_inline_blocks_last_token: Optional[MarkdownToken],
        last_line_number: int,
        last_column_number: int,
        line_number: int,
        column_number: int,
    ) -> Tuple[str, str, int, int]:
        if reset_current_string:
            current_string, current_string_unresolved = "", ""

        if old_inline_blocks_count != len(inline_blocks) or (
            old_inline_blocks_last_token
            and old_inline_blocks_last_token != inline_blocks[-1]
        ):
            last_line_number, last_column_number = line_number, column_number
        return (
            current_string,
            current_string_unresolved,
            last_line_number,
            last_column_number,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    # pylint: disable=too-many-arguments
    def __complete_inline_loop(
        source_text: str,
        new_index: Optional[int],
        end_string: Optional[str],
        whitespace_to_add: Optional[str],
        current_string: str,
        current_string_unresolved: str,
        new_string_unresolved: Optional[str],
        new_string: Optional[str],
        original_string: Optional[str],
    ) -> Tuple[Optional[int], int, Optional[str], str, str]:
        POGGER.debug(
            "__complete_inline_loop--current_string>>$>>",
            current_string,
        )
        POGGER.debug(
            "__complete_inline_loop--new_string>>$>>",
            new_string,
        )
        POGGER.debug(
            "__complete_inline_loop--new_string_unresolved>>$>>",
            new_string_unresolved,
        )
        POGGER.debug(
            "__complete_inline_loop--original_string>>$>>",
            original_string,
        )

        POGGER.debug(
            "__complete_inline_loop--current_string>>$>>",
            current_string,
        )
        POGGER.debug(
            "__complete_inline_loop--end_string>>$>>",
            end_string,
        )
        POGGER.debug(
            "__complete_inline_loop--whitespace_to_add>>$>>",
            whitespace_to_add,
        )
        assert new_string is not None
        if original_string is not None:
            assert not new_string_unresolved or new_string_unresolved == original_string
            replaced_string = ParserHelper.create_replacement_markers(
                original_string, InlineHelper.append_text("", new_string)
            )
            current_string = f"{current_string}{replaced_string}"
        else:
            current_string = InlineHelper.append_text(current_string, new_string)
        POGGER.debug(
            "__complete_inline_loop--current_string>>$>>",
            current_string,
        )

        POGGER.debug(
            "new_string_unresolved>>$>>",
            new_string_unresolved,
        )
        if new_string == ParserHelper.newline_character and end_string:
            split_end_string = end_string.split(ParserHelper.newline_character)
            POGGER.debug(
                "split_end_string>>$>>",
                split_end_string,
            )
            assert len(split_end_string) >= 2
            new_string = split_end_string[len(split_end_string) - 2] + new_string

        current_string_unresolved = (
            f"{current_string_unresolved}{new_string_unresolved}"
            if new_string_unresolved
            else InlineHelper.append_text(current_string_unresolved, new_string)
        )

        POGGER.debug(
            "__complete_inline_loop--current_string_unresolved>>$>>",
            current_string_unresolved,
        )

        start_index = new_index
        assert start_index is not None
        next_index = ParserHelper.index_any_of(
            source_text,
            InlineHandlerHelper.valid_inline_text_block_sequence_starts,
            start_index,
        )
        return (
            start_index,
            next_index,
            end_string,
            current_string,
            current_string_unresolved,
        )

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
