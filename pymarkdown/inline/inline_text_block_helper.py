"""
Module to help with the parsing of text inline elements.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.inline.emphasis_helper import EmphasisHelper
from pymarkdown.inline.inline_handler_helper import InlineHandlerHelper
from pymarkdown.inline.inline_helper import InlineHelper
from pymarkdown.inline.inline_line_end_helper import InlineLineEndHelper
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.inline.inline_response import InlineResponse
from pymarkdown.inline.inline_tabified_text_block_helper import (
    InlineTabifiedTextBlockHelper,
)
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods, too-many-lines


class InlineTextBlockHelper:
    """
    Class to help with the parsing of text inline elements.
    """

    @staticmethod
    def __process_inline_text_block_prepare(
        source_text: str,
        whitespace_to_recombine: Optional[str],
        is_para: bool,
        is_setext: bool,
        para_space: Optional[str],
    ) -> Tuple[str, Optional[List[str]]]:
        if whitespace_to_recombine:
            source_text, _ = ParserHelper.recombine_string_with_whitespace(
                source_text, whitespace_to_recombine
            )

        split_para_space: Optional[List[str]] = None
        if is_para or is_setext:
            assert (
                para_space is not None
            ), "If in a paragraph or setext text, para_space must be defined."
            split_para_space = para_space.split(ParserHelper.newline_character)

        return source_text, split_para_space

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod  # noqa: C901
    def process_inline_text_block(  # noqa: C901
        parser_properties: ParseBlockPassProperties,
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
        is_in_table: bool = False,
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
        start_index = 0
        inline_blocks: List[MarkdownToken] = []
        end_string: Optional[str] = ""

        source_text, split_para_space = (
            InlineTextBlockHelper.__process_inline_text_block_prepare(
                source_text, whitespace_to_recombine, is_para, is_setext, para_space
            )
        )

        next_index = ParserHelper.index_any_of(
            source_text,
            InlineHandlerHelper.valid_inline_text_block_sequence_starts,
            start_index,
        )
        newlines_encountered = 0
        while next_index != -1:
            old_next_index = next_index
            (
                line_number,
                column_number,
                end_string,
                current_string,
                current_string_unresolved,
                starting_whitespace,
                split_para_space,
                last_line_number,
                last_column_number,
                start_index,
                next_index,
                adj_newlines,
            ) = InlineTextBlockHelper.__handle_next_inline_character(
                parser_properties,
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
                split_para_space,
                tabified_text,
                newlines_encountered,
                is_in_table,
                para_space,
            )
            if adj_newlines:
                newlines_encountered += adj_newlines
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
        parser_properties: ParseBlockPassProperties,
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
        split_para_space: Optional[List[str]],
        tabified_text: Optional[str],
        newlines_encountered: int,
        is_in_table: bool,
        para_space: Optional[str] = None,
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
        int,
        int,
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
            parser_properties,
            coalesced_stack,
            current_string,
            whitespace_to_recombine,
            is_in_table,
            para_space,
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
            current_string_unresolved,
            was_new_line,
            tabified_remaining_line,
        ) = InlineTextBlockHelper.__handle_next_special_character(
            parser_properties,
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
            current_string_unresolved,
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
            split_para_space,
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
            split_para_space,
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
            split_para_space,
            last_line_number,
            last_column_number,
            new_start_index,
            next_index,
            inline_response.adj_newlines,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments,too-many-locals
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
        parse_properties: ParseBlockPassProperties,
        coalesced_stack: List[MarkdownToken],
        current_string: str,
        whitespace_to_recombine: Optional[str],
        is_in_table: bool,
        para_space: Optional[str] = None,
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

        last_container_token = coalesced_stack[-1] if coalesced_stack else None

        inline_request = InlineRequest(
            source_text,
            next_index,
            inline_blocks,
            remaining_line,
            tabified_remaining_line,
            current_string,
            current_string_unresolved,
            line_number,
            column_number,
            para_owner,
            tabified_text,
            parse_properties,
            last_container_token,
            whitespace_to_recombine,
            is_in_table,
            para_space,
        )
        return (
            False,
            remaining_line,
            old_inline_blocks_count,
            old_inline_blocks_last_token,
            tabified_remaining_line,
            inline_request,
        )

    # pylint: enable=too-many-arguments,too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __complete_inline_block_processing(
        inline_blocks: List[MarkdownToken],
        source_text: str,
        start_index: int,
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

        if start_index < len(source_text):
            text_to_append = source_text[start_index:]
            POGGER.debug("text_to_append>:$:<", text_to_append)

            POGGER.debug("tabified_text=>:$:<", tabified_text)
            if tabified_text:
                text_to_append = InlineTabifiedTextBlockHelper.complete_inline_block_processing_tabified(
                    source_text,
                    start_index,
                    tabified_text,
                    newlines_encountered,
                    inline_blocks,
                    end_string,
                )
                POGGER.debug("text_to_append>:$:<", text_to_append)

            POGGER.debug("current_string>:$:<", current_string)
            POGGER.debug("text_to_append>:$:<", text_to_append)
            current_string = InlineHelper.append_text(current_string, text_to_append)
            POGGER.debug("current_string>:$:<", current_string)

        have_processed_once = inline_blocks or start_index != 0
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

    @staticmethod
    def __handle_next_special_character_remaining_reduce(
        inline_request: InlineRequest, left_to_consume: int
    ) -> None:
        inline_block_index = len(inline_request.inline_blocks) - 1
        stop_block_token = None
        while (
            stop_block_token is None
            and inline_block_index >= 0
            and (
                inline_request.inline_blocks[inline_block_index].is_text
                or inline_request.inline_blocks[inline_block_index].is_special_text
            )
            and left_to_consume > 0
        ):
            current_block_token = cast(
                TextMarkdownToken,
                inline_request.inline_blocks[inline_block_index],
            )
            token_text_len = len(current_block_token.token_text)
            if left_to_consume <= token_text_len:
                stop_block_token = current_block_token
            else:
                left_to_consume -= token_text_len
                inline_block_index -= 1
        assert (
            inline_block_index >= 0 and stop_block_token is not None
        ), "End of loop criteria."
        if len(stop_block_token.token_text) > left_to_consume:
            left_text = stop_block_token.token_text[:-left_to_consume]
            new_token = TextMarkdownToken(
                left_text,
                stop_block_token.extracted_whitespace,
                stop_block_token.end_whitespace,
                tabified_text=stop_block_token.tabified_text,
                line_number=stop_block_token.line_number,
                column_number=stop_block_token.column_number,
            )
            inline_request.inline_blocks.insert(inline_block_index, new_token)
            inline_block_index += 1
        while len(inline_request.inline_blocks) > inline_block_index:
            del inline_request.inline_blocks[inline_block_index]

    @staticmethod
    def __handle_next_special_character_remaining(
        inline_request: InlineRequest,
        inline_response: InlineResponse,
        remaining_line: str,
        current_string: str,
        current_string_unresolved: str,
    ) -> Tuple[str, str, str]:
        left_to_consume = inline_response.reduce_remaining_line_by
        if left_to_consume <= len(remaining_line):
            remaining_line = remaining_line[: -inline_response.reduce_remaining_line_by]
        else:
            left_to_consume -= len(remaining_line)
            remaining_line = ""
            if left_to_consume <= len(current_string):
                assert current_string_unresolved.endswith(
                    current_string[-left_to_consume:]
                ), "Unresolve string must end with part of the current string."
                current_string = current_string[:-left_to_consume]
                current_string_unresolved = current_string_unresolved[:-left_to_consume]
            else:
                left_to_consume -= len(current_string)
                current_string = ""
                current_string_unresolved = ""
                InlineTextBlockHelper.__handle_next_special_character_remaining_reduce(
                    inline_request, left_to_consume
                )
        return remaining_line, current_string, current_string_unresolved

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_next_special_character(
        parser_properties: ParseBlockPassProperties,
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
        current_string_unresolved: str,
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
                parser_properties,
                source_text,
                next_index,
                inline_request,
                line_number,
                column_number,
                coalesced_stack,
            )
            if inline_response.reduce_remaining_line_by:
                (
                    remaining_line,
                    current_string,
                    current_string_unresolved,
                ) = InlineTextBlockHelper.__handle_next_special_character_remaining(
                    inline_request,
                    inline_response,
                    remaining_line,
                    current_string,
                    current_string_unresolved,
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
            current_string_unresolved,
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
        split_para_space: Optional[List[str]],
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
        int,
        int,
        Optional[str],
    ]:
        (
            line_number,
            column_number,
            split_para_space,
        ) = InlineTextBlockHelper.__adjust_line_and_column_number(
            was_new_line,
            coalesced_stack,
            line_number,
            column_number,
            split_para_space,
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

        assert (
            inline_response.new_index is not None
        ), "new_index must be defined by now."
        assert (
            inline_response.new_string is not None
        ), "new_string must be defined by now."
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
            split_para_space,
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
        split_para_space: Optional[List[str]],
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
                assert (
                    block_quote_token.bleading_spaces is not None
                ), "Bleading spaces must be defined by now."
                split_leading_spaces = block_quote_token.bleading_spaces.split(
                    ParserHelper.newline_character
                )
                selected_split_length = len(
                    split_leading_spaces[block_quote_token.leading_text_index]
                )
                column_number += selected_split_length

            line_number += 1
            assert (
                split_para_space
            ), "If we had a new line, we must have paragraph/setext text to handle."
            split_para_space = split_para_space[1:]
            column_number += len(split_para_space[0])
        elif not was_column_number_reset:
            column_number += len(remaining_line)
        else:
            assert did_line_number_change, "If here, the line number must have changed."
            if coalesced_stack and coalesced_stack[-1].is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, coalesced_stack[-1])
                POGGER.debug(
                    "coalesced_list[-1].leading_text_index=$",
                    block_quote_token.leading_text_index,
                )
                assert (
                    block_quote_token.bleading_spaces is not None
                ), "Bleading spaces must be defined by now."
                split_leading_spaces = block_quote_token.bleading_spaces.split(
                    ParserHelper.newline_character
                )
                selected_split_length = len(
                    split_leading_spaces[block_quote_token.leading_text_index]
                )
                column_number += selected_split_length
        return line_number, column_number, split_para_space

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
        new_index: int,
        end_string: Optional[str],
        whitespace_to_add: Optional[str],
        current_string: str,
        current_string_unresolved: str,
        new_string_unresolved: Optional[str],
        new_string: str,
        original_string: Optional[str],
    ) -> Tuple[int, int, Optional[str], str, str]:
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
        if original_string is not None:
            assert (
                new_string_unresolved is None
                or new_string_unresolved == original_string
            ), "new_string_unresolved must either be not defined or equal to the original_string."
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
            assert (
                len(split_end_string) >= 2
            ), "end_string must be split into at least 2 parts"
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
