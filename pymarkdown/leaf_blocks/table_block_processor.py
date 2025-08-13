from typing import List, Optional, Tuple, cast

from pymarkdown.container_blocks.container_grab_bag import POGGER
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.requeue_line_info import RequeueLineInfo
from pymarkdown.leaf_blocks.table_block_continuation_helper import (
    TableBlockContinuationHelper,
)
from pymarkdown.leaf_blocks.table_block_parse_helper import TableParseHelper
from pymarkdown.leaf_blocks.table_block_tuple import TableTuple
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import TableBlockStackToken


class TableBlockHelper:

    @staticmethod
    def process_table_rows(
        parser_state: ParserState,
        position_marker: PositionMarker,
        remaining_line_to_parse: str,
        extracted_whitespace: str,
        unmodified_line_to_parse: str,
        original_stack_depth: int,
        original_document_depth: int,
        original_line: str,
    ) -> Tuple[bool, bool, bool, Optional[RequeueLineInfo], List[MarkdownToken]]:
        """
        Process a table row.  Note, this requires a lot of work to
        handle properly because it is not until a new line that we
        can determine if the table is correctly formed.
        """
        line_to_parse = position_marker.text_to_parse
        start_index: int = position_marker.index_number
        lines_to_requeue: List[str] = []

        POGGER.debug(">>remaining_line_to_parse>:$:<", remaining_line_to_parse)
        POGGER.debug(">>line_to_parse>:$:<", line_to_parse)
        POGGER.debug(">>start_index>:$:<", start_index)

        (
            line_to_parse,
            unmodified_line_to_parse,
            remaining_line_to_parse,
            start_index,
            is_blank_line,
        ) = TableBlockHelper.__handle_table_rows_init(
            remaining_line_to_parse,
            line_to_parse,
            start_index,
            original_line,
            unmodified_line_to_parse,
        )

        (
            was_started,
            table_stack_token,
            original_stack_depth,
            original_document_depth,
            line_to_parse,
            extracted_whitespace,
            start_index,
        ) = TableBlockHelper.__handle_table_rows_started(
            parser_state,
            original_stack_depth,
            original_document_depth,
            line_to_parse,
            extracted_whitespace,
            start_index,
        )
        POGGER.debug(">>line_to_parse>:$:<", line_to_parse)
        line_to_parse_size = len(line_to_parse)

        (
            did_complete_table,
            end_table_index,
            parsed_table_tuple,
            is_blank_line,
            line_to_parse,
        ) = TableBlockHelper.__handle_table_rows_processing(
            parser_state,
            line_to_parse,
            start_index,
            extracted_whitespace,
            is_blank_line,
            was_started,
            line_to_parse_size,
            remaining_line_to_parse,
            lines_to_requeue,
            unmodified_line_to_parse,
        )
        (
            did_pause_table,
            force_ignore_first_as_table,
            new_tokens,
        ) = TableBlockContinuationHelper.determine_continue_or_stop(
            parser_state,
            position_marker,
            was_started,
            remaining_line_to_parse,
            extracted_whitespace,
            unmodified_line_to_parse,
            original_stack_depth,
            original_document_depth,
            end_table_index,
            line_to_parse_size,
            is_blank_line,
            did_complete_table,
            parsed_table_tuple,
            lines_to_requeue,
        )
        if lines_to_requeue:
            assert (
                table_stack_token is not None
            ), "Stack token is created before determining requeue, therefore it must be declared."
            TableBlockHelper.__prepare_for_requeue(
                parser_state,
                table_stack_token,
                did_complete_table,
                original_stack_depth,
                original_document_depth,
                lines_to_requeue,
            )
            ## Different from LRD.
            # force_ignore_first_as_table = True  # TODO check this
            ## Different from LRD.
            requeue_line_info = RequeueLineInfo(
                lines_to_requeue, False, force_ignore_first_as_table
            )
            ## Different from LRD.
            parser_state.abc(requeue_line_info, table_stack_token)
            ## Different from LRD.
        else:
            requeue_line_info = None

        return (
            did_complete_table or end_table_index != -1,
            did_complete_table,
            did_pause_table,
            requeue_line_info,
            new_tokens,
        )

    @staticmethod
    def __handle_table_rows_init(
        remaining_line_to_parse: str,
        line_to_parse: str,
        start_index: int,
        original_line: str,
        unmodified_line_to_parse: str,
    ) -> Tuple[str, str, str, int, bool]:
        is_blank_line = not line_to_parse and not start_index

        POGGER.debug(">>original_line>:$:<", original_line)
        if ParserHelper.tab_character in original_line and not is_blank_line:
            POGGER.debug(">>tabified>:$:<", original_line)

            first_character_to_parse = line_to_parse[start_index]
            POGGER.debug(">>xx>:$:<", first_character_to_parse)
            first_character_to_parse_index = original_line.find(
                first_character_to_parse
            )
            assert (
                first_character_to_parse_index != -1
            ), "Character not found within string."

            line_to_parse = original_line[first_character_to_parse_index:]
            unmodified_line_to_parse = original_line
            remaining_line_to_parse = line_to_parse
            start_index = 0

        POGGER.debug(">>line_to_parse>:$:<", line_to_parse)
        return (
            line_to_parse,
            unmodified_line_to_parse,
            remaining_line_to_parse,
            start_index,
            is_blank_line,
        )

    @staticmethod
    def __handle_table_rows_started(
        parser_state: ParserState,
        original_stack_depth: int,
        original_document_depth: int,
        line_to_parse: str,
        extracted_whitespace: str,
        start_index: int,
    ) -> Tuple[bool, Optional[TableBlockStackToken], int, int, str, str, int]:
        table_stack_token: Optional[TableBlockStackToken] = None

        if was_started := parser_state.token_stack[-1].was_table_block_started:
            table_stack_token = cast(TableBlockStackToken, parser_state.token_stack[-1])
            assert (
                table_stack_token.original_stack_depth is not None
                and table_stack_token.original_document_depth is not None
            ), "stack and document depth must both be defined."
            original_stack_depth, original_document_depth = (
                table_stack_token.original_stack_depth,
                table_stack_token.original_document_depth,
            )
            POGGER.debug(
                ">>continuation_lines>>$<<",
                table_stack_token.continuation_lines,
            )
            line_to_parse = table_stack_token.add_joined_lines_before_suffix(
                line_to_parse
            )
            (
                start_index,
                extracted_whitespace,
            ) = ParserHelper.extract_ascii_whitespace_verified(line_to_parse, 0)

            POGGER.debug(">>line_to_parse>>$<<", line_to_parse)
        return (
            was_started,
            table_stack_token,
            original_stack_depth,
            original_document_depth,
            line_to_parse,
            extracted_whitespace,
            start_index,
        )

    @staticmethod
    def __handle_table_rows_processing(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        is_blank_line: bool,
        was_started: bool,
        line_to_parse_size: int,
        remaining_line_to_parse: str,
        lines_to_requeue: List[str],
        unmodified_line_to_parse: str,
    ) -> Tuple[bool, int, Optional[TableTuple], bool, str]:
        if was_started:
            POGGER.debug(">>parse_table>>was_started")

            (
                did_complete_table,
                end_table_index,
                parsed_table_tuple,
            ) = TableParseHelper.parse_table(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
                remaining_line_to_parse,
                was_started,
            )
            POGGER.debug(
                ">>parse_table>>was_started>>did_complete_table>>$"
                + ">>end_table_index>>$>>len(line_to_parse)>>$",
                did_complete_table,
                end_table_index,
                line_to_parse_size,
            )

            if not (
                did_complete_table
                or (
                    not is_blank_line
                    and not did_complete_table
                    and (end_table_index == line_to_parse_size)
                )
            ):
                POGGER.debug(">>parse_table>>was_started>>GOT HARD FAILURE")
                (
                    is_blank_line,
                    line_to_parse,
                    did_complete_table,
                    end_table_index,
                    parsed_table_tuple,
                ) = TableBlockHelper.__process_table_hard_failure(
                    parser_state,
                    remaining_line_to_parse,
                    lines_to_requeue,
                    unmodified_line_to_parse,
                    was_started,
                )
        else:
            (
                did_complete_table,
                end_table_index,
                parsed_table_tuple,
            ) = TableParseHelper.parse_table(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
                remaining_line_to_parse,
                was_started,
            )
            POGGER.debug(
                ">>parse_table>>did_complete_table>>$>>end_table_index>>$>>len(line_to_parse)>>$",
                did_complete_table,
                end_table_index,
                line_to_parse_size,
            )
        return (
            did_complete_table,
            end_table_index,
            parsed_table_tuple,
            is_blank_line,
            line_to_parse,
        )

    @staticmethod
    def __prepare_for_requeue_reset_markdown_token(
        parser_state: ParserState, table_stack_token: TableBlockStackToken
    ) -> None:
        assert (
            table_stack_token.last_block_quote_markdown_token_index is not None
        ), "Index must be defined by now."
        POGGER.debug(
            ">>XXXXXX>>last_block_quote_markdown_token_index:$:",
            table_stack_token.last_block_quote_markdown_token_index,
        )
        POGGER.debug(
            ">>XXXXXX>>st-now:$:",
            parser_state.token_document[
                table_stack_token.last_block_quote_markdown_token_index
            ],
        )

        del parser_state.token_document[
            table_stack_token.last_block_quote_markdown_token_index
        ]
        assert (
            table_stack_token.copy_of_last_block_quote_markdown_token is not None
        ), "Token must be defined by now."
        parser_state.token_document.insert(
            table_stack_token.last_block_quote_markdown_token_index,
            table_stack_token.copy_of_last_block_quote_markdown_token,
        )
        assert (
            table_stack_token.last_block_quote_stack_token is not None
        ), "Token must be defined by now."
        POGGER.debug(
            "last_block_quote_stack_token>:$:<",
            table_stack_token.last_block_quote_stack_token,
        )
        table_stack_token.last_block_quote_stack_token.reset_matching_markdown_token(
            table_stack_token.copy_of_last_block_quote_markdown_token
        )
        POGGER.debug(
            "last_block_quote_stack_token>:$:<",
            table_stack_token.last_block_quote_stack_token,
        )

    @staticmethod
    def __prepare_for_requeue_reset_document_and_stack(
        parser_state: ParserState,
        table_stack_token: TableBlockStackToken,
        original_stack_depth: int,
        original_document_depth: int,
    ) -> None:
        POGGER.debug(">>XXXXXX>>original_stack_depth:$:", original_stack_depth)
        POGGER.debug(">>XXXXXX>>token_stack_depth:$:", len(parser_state.token_stack))
        POGGER.debug(">>XXXXXX>>token_stack(before):$:", parser_state.token_stack)
        POGGER.debug(
            ">>XXXXXX>>copy_of_token_stack:$:", parser_state.copy_of_token_stack
        )
        POGGER.debug(
            ">>table_stack_token>>copy_of_token_stack:$:",
            table_stack_token.copy_of_token_stack,
        )
        if len(parser_state.token_stack) >= original_stack_depth:
            while (
                len(parser_state.token_stack) > original_stack_depth
                ## Different from LRD.
                and not parser_state.token_stack[-1].is_block_quote
                ## Different from LRD.
            ):
                del parser_state.token_stack[-1]
        else:
            while len(parser_state.token_stack):
                del parser_state.token_stack[-1]
            assert (
                table_stack_token.copy_of_token_stack is not None
            ), "Token must be defined by now."
            parser_state.token_stack.extend(table_stack_token.copy_of_token_stack)
        POGGER.debug(">>XXXXXX>>token_stack(after):$:", parser_state.token_stack)

        ## Different from LRD.
        POGGER.debug(">>XXXXXX>>original_document_depth:$:", original_document_depth)
        POGGER.debug(
            ">>XXXXXX>>token_document_depth:$:",
            len(parser_state.token_document),
        )
        POGGER.debug(">>XXXXXX>>token_document(before):$:", parser_state.token_document)
        while (
            len(parser_state.token_document) > original_document_depth
            and not parser_state.token_document[-1].is_block_quote_start
        ):
            del parser_state.token_document[-1]
        ## Different from LRD.
        POGGER.debug(">>XXXXXX>>token_document(after):$:", parser_state.token_document)

    @staticmethod
    def __prepare_for_requeue(
        parser_state: ParserState,
        table_stack_token: TableBlockStackToken,
        did_complete_table: bool,
        original_stack_depth: int,
        original_document_depth: int,
        lines_to_requeue: List[str],
    ) -> None:
        # This works because in most cases, we add things.  However, in cases like
        # an indented code block, we process the "is it indented enough" and close
        # that block before hitting this.  As such, we have a special case to take
        # care of that.  In the future, will possibly want to do something instead of
        # original_document_depth and stack, such as passing in a copy of the both
        # elements so they can be reset on the rewind.
        # i.e. icode would go back on stack, end-icode would not be in document.
        POGGER.debug("lines_to_requeue:$:", lines_to_requeue)
        POGGER.debug(
            ">>XXXXXX>>copy_of_last_block_quote_markdown_token:$:",
            table_stack_token.copy_of_last_block_quote_markdown_token,
        )
        if not did_complete_table:
            if table_stack_token.copy_of_last_block_quote_markdown_token:
                TableBlockHelper.__prepare_for_requeue_reset_markdown_token(
                    parser_state, table_stack_token
                )
            TableBlockHelper.__prepare_for_requeue_reset_document_and_stack(
                parser_state,
                table_stack_token,
                original_stack_depth,
                original_document_depth,
            )

    @staticmethod
    def __process_table_hard_failure(
        parser_state: ParserState,
        remaining_line_to_parse: str,
        lines_to_requeue: List[str],
        unmodified_line_to_parse: str,
        was_started: bool,
    ) -> Tuple[
        bool,
        str,
        bool,
        int,
        Optional[TableTuple],
    ]:
        """
        In cases of a hard failure, we have had continuations to the original line
        that make it a bit more difficult to figure out if we have an actual good
        LRD in the mix somehow.  So take lines off the end while we have lines.
        """
        (
            is_blank_line,
            line_to_parse,
            did_complete_table,
            end_table_index,
            parsed_table_tuple,
        ) = (None, None, None, None, None)
        table_stack_token = cast(TableBlockStackToken, parser_state.token_stack[-1])

        POGGER.debug(">>remaining_line_to_parse>>add>:$<<", remaining_line_to_parse)
        POGGER.debug(">>unmodified_line_to_parse>>add>:$<<", unmodified_line_to_parse)
        assert unmodified_line_to_parse.endswith(
            remaining_line_to_parse
        ), "Current line must end with the remaining text."
        ## Different from LRD.
        table_stack_token.add_continuation_line(remaining_line_to_parse)
        table_stack_token.add_unmodified_line(unmodified_line_to_parse)
        ## Different from LRD.

        ## Different from LRD.
        try_again = len(table_stack_token.continuation_lines) > 2
        if not try_again:
            is_blank_line = False
            line_to_parse = remaining_line_to_parse
            did_complete_table = False
            end_table_index = -1
        xdf = 2 if len(table_stack_token.continuation_lines) == 2 else 1
        while xdf:
            ## Different from LRD.

            lines_to_requeue.append(table_stack_token.unmodified_lines[-1])
            del table_stack_token.continuation_lines[-1]
            del table_stack_token.unmodified_lines[-1]

            ## Different from LRD.
            if try_again:
                (
                    is_blank_line,
                    line_to_parse,
                ) = True, table_stack_token.add_joined_lines_before_suffix("")
                line_to_parse = line_to_parse[:-1]
                start_index, extracted_whitespace = (
                    ParserHelper.extract_spaces_verified(line_to_parse, 0)
                )
                (
                    did_complete_table,
                    end_table_index,
                    parsed_table_tuple,
                ) = TableParseHelper.parse_table(
                    parser_state,
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    is_blank_line,
                    None,
                    was_started,
                )
            xdf -= 1
        ## Different from LRD.
        assert is_blank_line is not None, "while loop must have executed at least once."
        assert line_to_parse is not None, "while loop must have executed at least once."
        assert (
            did_complete_table is not None
        ), "while loop must have executed at least once."
        assert (
            end_table_index is not None
        ), "while loop must have executed at least once."
        return (
            is_blank_line,
            line_to_parse,
            did_complete_table,
            end_table_index,
            parsed_table_tuple,
        )

    @staticmethod
    def handle_table_leaf_block(
        parser_state: ParserState,
        outer_processed: bool,
        position_marker: PositionMarker,
        leaf_token_whitespace: str,
        remaining_line_to_parse: str,
        ignore_table_start: bool,
        pre_tokens: List[MarkdownToken],
        original_line: str,
        requeue_line_info: Optional[RequeueLineInfo],
    ) -> Tuple[bool, Optional[RequeueLineInfo]]:
        POGGER.debug(
            "handle_table_leaf_block>>pre_tokens>>$<<",
            pre_tokens,
        )

        ## Different from LRD.
        if (
            parser_state.parse_properties.is_tables_enabled
            and not outer_processed
            and not ignore_table_start
        ):
            ## Different from LRD.
            POGGER.debug(
                "handle_table_leaf_block>>outer_processed>>$",
                position_marker.text_to_parse[position_marker.index_number :],
            )
            assert (
                parser_state.original_line_to_parse is not None
            ), "Original line must be defined by now."
            (
                outer_processed,
                _,  # did_complete_table,
                _,  # did_pause_table,
                requeue_line_info,
                new_tokens,
            ) = TableBlockHelper.process_table_rows(
                parser_state,
                position_marker,
                remaining_line_to_parse,
                leaf_token_whitespace,
                parser_state.original_line_to_parse,
                parser_state.original_stack_depth,
                parser_state.original_document_depth,
                original_line,
            )
            if requeue_line_info:
                outer_processed = True
                POGGER.debug(
                    "handle_table_leaf_block>>outer_processed>>$<lines_to_requeue<$<$",
                    outer_processed,
                    requeue_line_info.lines_to_requeue,
                    len(requeue_line_info.lines_to_requeue),
                )
            else:
                POGGER.debug(
                    "handle_table_leaf_block>>outer_processed>>$<lines_to_requeue<(None)",
                    outer_processed,
                )
        else:
            ## Different from LRD.
            new_tokens = []
        ## Different from LRD.

        POGGER.debug("handle_table_leaf_block>>pre_tokens>>$<<", pre_tokens)
        pre_tokens.extend(new_tokens)
        POGGER.debug("handle_table_leaf_block>>pre_tokens>>$<<", pre_tokens)
        return outer_processed, requeue_line_info
