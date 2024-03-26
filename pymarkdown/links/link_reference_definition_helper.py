"""
Module to helper with the parsing of link reference definitions.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.requeue_line_info import RequeueLineInfo
from pymarkdown.links.link_reference_definition_continuation_helper import (
    LinkReferenceDefinitionContinuationHelper,
)
from pymarkdown.links.link_reference_definition_parse_helper import (
    LinkReferenceDefinitionParseHelper,
)
from pymarkdown.links.link_reference_tuple import LinkReferenceDefinitionTuple
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import LinkDefinitionStackToken

POGGER = ParserLogger(logging.getLogger(__name__))


class LinkReferenceDefinitionHelper:
    """
    Class to helper with the parsing of link reference definitions.
    """

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def process_link_reference_definition(
        parser_state: ParserState,
        position_marker: PositionMarker,
        remaining_line_to_parse: str,
        extracted_whitespace: Optional[str],
        unmodified_line_to_parse: str,
        original_stack_depth: int,
        original_document_depth: int,
        original_line: str,
        process_mode: int,
    ) -> Tuple[bool, bool, bool, Optional[RequeueLineInfo], List[MarkdownToken]]:
        """
        Process a link deference definition.  Note, this requires a lot of work to
        handle properly because of partial definitions across lines.
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
        ) = LinkReferenceDefinitionHelper.__handle_link_reference_definition_init(
            remaining_line_to_parse,
            line_to_parse,
            start_index,
            original_line,
            unmodified_line_to_parse,
        )

        (
            was_started,
            lrd_stack_token,
            original_stack_depth,
            original_document_depth,
            line_to_parse,
            extracted_whitespace,
            start_index,
        ) = LinkReferenceDefinitionHelper.__handle_link_reference_definition_started(
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
            did_complete_lrd,
            end_lrd_index,
            parsed_lrd_tuple,
            is_blank_line,
            line_to_parse,
        ) = LinkReferenceDefinitionHelper.__handle_link_reference_definition_processing(
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
            did_pause_lrd,
            force_ignore_first_as_lrd,
            new_tokens,
        ) = LinkReferenceDefinitionContinuationHelper.determine_continue_or_stop(
            parser_state,
            position_marker,
            was_started,
            remaining_line_to_parse,
            extracted_whitespace,
            unmodified_line_to_parse,
            original_stack_depth,
            original_document_depth,
            end_lrd_index,
            line_to_parse_size,
            is_blank_line,
            did_complete_lrd,
            parsed_lrd_tuple,
            lines_to_requeue,
            process_mode,
        )
        if lines_to_requeue:
            LinkReferenceDefinitionHelper.__prepare_for_requeue(
                parser_state,
                lrd_stack_token,
                did_complete_lrd,
                original_stack_depth,
                original_document_depth,
                lines_to_requeue,
            )
            requeue_line_info = RequeueLineInfo(
                lines_to_requeue, force_ignore_first_as_lrd
            )
        else:
            requeue_line_info = None

        return (
            did_complete_lrd or end_lrd_index != -1,
            did_complete_lrd,
            did_pause_lrd,
            requeue_line_info,
            new_tokens,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __handle_link_reference_definition_init(
        remaining_line_to_parse: str,
        line_to_parse: str,
        start_index: int,
        original_line: str,
        unmodified_line_to_parse: str,
    ) -> Tuple[str, str, str, int, Optional[bool]]:
        is_blank_line: Optional[bool] = not line_to_parse and not start_index

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

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_link_reference_definition_started(
        parser_state: ParserState,
        original_stack_depth: int,
        original_document_depth: int,
        line_to_parse: str,
        extracted_whitespace: Optional[str],
        start_index: int,
    ) -> Tuple[
        bool, Optional[LinkDefinitionStackToken], int, int, str, Optional[str], int
    ]:
        lrd_stack_token: Optional[LinkDefinitionStackToken] = None

        if was_started := parser_state.token_stack[-1].was_link_definition_started:
            lrd_stack_token = cast(
                LinkDefinitionStackToken, parser_state.token_stack[-1]
            )
            assert (
                lrd_stack_token.original_stack_depth is not None
                and lrd_stack_token.original_document_depth is not None
            ), "stack and document depth must both be defined."
            original_stack_depth, original_document_depth = (
                lrd_stack_token.original_stack_depth,
                lrd_stack_token.original_document_depth,
            )
            POGGER.debug(
                ">>continuation_lines>>$<<",
                lrd_stack_token.continuation_lines,
            )
            line_to_parse = lrd_stack_token.add_joined_lines_before_suffix(
                line_to_parse
            )
            (
                start_index,
                extracted_whitespace,
            ) = ParserHelper.extract_ascii_whitespace_verified(line_to_parse, 0)

            POGGER.debug(">>line_to_parse>>$<<", line_to_parse)
        return (
            was_started,
            lrd_stack_token,
            original_stack_depth,
            original_document_depth,
            line_to_parse,
            extracted_whitespace,
            start_index,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_link_reference_definition_processing(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        is_blank_line: Optional[bool],
        was_started: bool,
        line_to_parse_size: int,
        remaining_line_to_parse: str,
        lines_to_requeue: List[str],
        unmodified_line_to_parse: str,
    ) -> Tuple[
        bool, Optional[int], Optional[LinkReferenceDefinitionTuple], Optional[bool], str
    ]:
        if was_started:
            POGGER.debug(">>parse_link_reference_definition>>was_started")
            did_complete_lrd: Optional[bool] = False
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionParseHelper.parse_link_reference_definition(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            POGGER.debug(
                ">>parse_link_reference_definition>>was_started>>did_complete_lrd>>$"
                + ">>end_lrd_index>>$>>len(line_to_parse)>>$",
                did_complete_lrd,
                end_lrd_index,
                line_to_parse_size,
            )

            if not (
                did_complete_lrd
                or (
                    not is_blank_line
                    and not did_complete_lrd
                    and (end_lrd_index == line_to_parse_size)
                )
            ):
                POGGER.debug(
                    ">>parse_link_reference_definition>>was_started>>GOT HARD FAILURE"
                )
                (
                    is_blank_line,
                    line_to_parsex,
                    did_complete_lrd,
                    end_lrd_index,
                    parsed_lrd_tuple,
                ) = LinkReferenceDefinitionHelper.__process_lrd_hard_failure(
                    parser_state,
                    remaining_line_to_parse,
                    lines_to_requeue,
                    unmodified_line_to_parse,
                )
                assert line_to_parsex is not None, "TODO: check"
                line_to_parse = line_to_parsex
        else:
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionParseHelper.parse_link_reference_definition(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            POGGER.debug(
                ">>parse_link_reference_definition>>did_complete_lrd>>$>>end_lrd_index>>$>>len(line_to_parse)>>$",
                did_complete_lrd,
                end_lrd_index,
                line_to_parse_size,
            )
        assert did_complete_lrd is not None, "TODO: check"
        return (
            did_complete_lrd,
            end_lrd_index,
            parsed_lrd_tuple,
            is_blank_line,
            line_to_parse,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __prepare_for_requeue_reset_markdown_token(
        parser_state: ParserState, lrd_stack_token: LinkDefinitionStackToken
    ) -> None:
        assert (
            lrd_stack_token.last_block_quote_markdown_token_index is not None
        ), "Index must be defined by now."
        POGGER.debug(
            ">>XXXXXX>>last_block_quote_markdown_token_index:$:",
            lrd_stack_token.last_block_quote_markdown_token_index,
        )
        POGGER.debug(
            ">>XXXXXX>>st-now:$:",
            parser_state.token_document[
                lrd_stack_token.last_block_quote_markdown_token_index
            ],
        )

        del parser_state.token_document[
            lrd_stack_token.last_block_quote_markdown_token_index
        ]
        assert (
            lrd_stack_token.copy_of_last_block_quote_markdown_token is not None
        ), "Token must be defined by now."
        parser_state.token_document.insert(
            lrd_stack_token.last_block_quote_markdown_token_index,
            lrd_stack_token.copy_of_last_block_quote_markdown_token,
        )
        assert (
            lrd_stack_token.last_block_quote_stack_token is not None
        ), "Token must be defined by now."
        POGGER.debug(
            "last_block_quote_stack_token>:$:<",
            lrd_stack_token.last_block_quote_stack_token,
        )
        lrd_stack_token.last_block_quote_stack_token.reset_matching_markdown_token(
            lrd_stack_token.copy_of_last_block_quote_markdown_token
        )
        POGGER.debug(
            "last_block_quote_stack_token>:$:<",
            lrd_stack_token.last_block_quote_stack_token,
        )

    @staticmethod
    def __prepare_for_requeue_reset_document_and_stack(
        parser_state: ParserState,
        lrd_stack_token: LinkDefinitionStackToken,
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
            ">>lrd_stack_token>>copy_of_token_stack:$:",
            lrd_stack_token.copy_of_token_stack,
        )
        if len(parser_state.token_stack) >= original_stack_depth:
            while len(parser_state.token_stack) > original_stack_depth:
                del parser_state.token_stack[-1]
        else:
            while len(parser_state.token_stack):
                del parser_state.token_stack[-1]
            assert (
                lrd_stack_token.copy_of_token_stack is not None
            ), "Token must be defined by now."
            parser_state.token_stack.extend(lrd_stack_token.copy_of_token_stack)
        POGGER.debug(">>XXXXXX>>token_stack(after):$:", parser_state.token_stack)

        POGGER.debug(">>XXXXXX>>original_document_depth:$:", original_document_depth)
        POGGER.debug(
            ">>XXXXXX>>token_document_depth:$:",
            len(parser_state.token_document),
        )
        POGGER.debug(">>XXXXXX>>token_document(before):$:", parser_state.token_document)
        while len(parser_state.token_document) > original_document_depth:
            del parser_state.token_document[-1]
        POGGER.debug(">>XXXXXX>>token_document(after):$:", parser_state.token_document)

    # pylint: disable=too-many-arguments
    @staticmethod
    def __prepare_for_requeue(
        parser_state: ParserState,
        lrd_stack_token: Optional[LinkDefinitionStackToken],
        did_complete_lrd: bool,
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
        assert lrd_stack_token is not None, "TODO: check"
        POGGER.debug("lines_to_requeue:$:", lines_to_requeue)
        POGGER.debug(
            ">>XXXXXX>>copy_of_last_block_quote_markdown_token:$:",
            lrd_stack_token.copy_of_last_block_quote_markdown_token,
        )
        if not did_complete_lrd:
            if lrd_stack_token.copy_of_last_block_quote_markdown_token:
                LinkReferenceDefinitionHelper.__prepare_for_requeue_reset_markdown_token(
                    parser_state, lrd_stack_token
                )
            LinkReferenceDefinitionHelper.__prepare_for_requeue_reset_document_and_stack(
                parser_state,
                lrd_stack_token,
                original_stack_depth,
                original_document_depth,
            )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __process_lrd_hard_failure(
        parser_state: ParserState,
        remaining_line_to_parse: str,
        lines_to_requeue: List[str],
        unmodified_line_to_parse: str,
    ) -> Tuple[
        Optional[bool],
        Optional[str],
        Optional[bool],
        Optional[int],
        Optional[LinkReferenceDefinitionTuple],
    ]:
        """
        In cases of a hard failure, we have had continuations to the original line
        that make it a bit more difficult to figure out if we have an actual good
        LRD in the mix somehow.  So take lines off the end while we have lines.
        """
        (
            is_blank_line,
            line_to_parse,
            did_complete_lrd,
            end_lrd_index,
            parsed_lrd_tuple,
        ) = (None, None, None, None, None)
        link_ref_stack_token = cast(
            LinkDefinitionStackToken, parser_state.token_stack[-1]
        )

        POGGER.debug(">>remaining_line_to_parse>>add>:$<<", remaining_line_to_parse)
        POGGER.debug(">>unmodified_line_to_parse>>add>:$<<", unmodified_line_to_parse)
        assert unmodified_line_to_parse.endswith(
            remaining_line_to_parse
        ), "Current line must end with the remaining text."
        link_ref_stack_token.add_continuation_line(remaining_line_to_parse)
        link_ref_stack_token.add_unmodified_line(unmodified_line_to_parse)
        while link_ref_stack_token.continuation_lines:
            POGGER.debug(
                "continuation_lines>>$<<",
                ParserHelper.make_whitespace_visible(
                    str(link_ref_stack_token.continuation_lines)
                ),
            )
            POGGER.debug(
                "unmodified_lines>>$<<",
                ParserHelper.make_whitespace_visible(
                    str(link_ref_stack_token.unmodified_lines)
                ),
            )

            lines_to_requeue.append(link_ref_stack_token.unmodified_lines[-1])
            POGGER.debug(
                ">>continuation_line>>$",
                link_ref_stack_token.continuation_lines[-1],
            )
            POGGER.debug(
                ">>unmodified_line>>$",
                link_ref_stack_token.unmodified_lines[-1],
            )
            del link_ref_stack_token.continuation_lines[-1]
            del link_ref_stack_token.unmodified_lines[-1]
            POGGER.debug(
                ">>lines_to_requeue>>$>>",
                lines_to_requeue,
            )
            POGGER.debug(
                ">>continuation_lines>>$<<",
                link_ref_stack_token.continuation_lines,
            )
            POGGER.debug(
                ">>unmodified_lines>>$<<",
                link_ref_stack_token.unmodified_lines,
            )
            (
                is_blank_line,
                line_to_parse,
            ) = True, link_ref_stack_token.add_joined_lines_before_suffix("")
            line_to_parse = line_to_parse[:-1]
            start_index, extracted_whitespace = ParserHelper.extract_spaces_verified(
                line_to_parse, 0
            )
            POGGER.debug(">>line_to_parse>>$<<", line_to_parse)
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionParseHelper.parse_link_reference_definition(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            POGGER.debug(
                ">>parse_link_reference_definition>>was_started>>did_complete_lrd>>$"
                + ">>end_lrd_index>>$>>len(line_to_parse)>>$",
                did_complete_lrd,
                end_lrd_index,
                len(line_to_parse),
            )
            if did_complete_lrd:
                break
        return (
            is_blank_line,
            line_to_parse,
            did_complete_lrd,
            end_lrd_index,
            parsed_lrd_tuple,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def handle_link_reference_definition_leaf_block(
        parser_state: ParserState,
        outer_processed: bool,
        position_marker: PositionMarker,
        leaf_token_whitespace: Optional[str],
        remaining_line_to_parse: str,
        ignore_link_definition_start: bool,
        pre_tokens: List[MarkdownToken],
        original_line: str,
    ) -> Tuple[bool, Optional[RequeueLineInfo]]:
        """
        Take care of the processing for link reference definitions.
        """
        POGGER.debug(
            "handle_link_reference_definition>>pre_tokens>>$<<",
            pre_tokens,
        )

        if not outer_processed and not ignore_link_definition_start:
            POGGER.debug(
                "plflb-process_link_reference_definition>>outer_processed>>$",
                position_marker.text_to_parse[position_marker.index_number :],
            )
            assert (
                parser_state.original_line_to_parse is not None
            ), "Original line must be defined by now."
            (
                outer_processed,
                _,  # did_complete_lrd,
                _,  # did_pause_lrd,
                requeue_line_info,
                new_tokens,
            ) = LinkReferenceDefinitionHelper.process_link_reference_definition(
                parser_state,
                position_marker,
                remaining_line_to_parse,
                leaf_token_whitespace,
                parser_state.original_line_to_parse,
                parser_state.original_stack_depth,
                parser_state.original_document_depth,
                original_line,
                0,
            )
            if requeue_line_info:
                outer_processed = True
                POGGER.debug(
                    "plflb-process_link_reference_definition>>outer_processed>>$<lines_to_requeue<$<$",
                    outer_processed,
                    requeue_line_info.lines_to_requeue,
                    len(requeue_line_info.lines_to_requeue),
                )
            else:
                POGGER.debug(
                    "plflb-process_link_reference_definition>>outer_processed>>$<lines_to_requeue<(None)",
                    outer_processed,
                )
        else:
            requeue_line_info, new_tokens = None, []

        POGGER.debug("handle_link_reference_definition>>pre_tokens>>$<<", pre_tokens)
        pre_tokens.extend(new_tokens)
        POGGER.debug("handle_link_reference_definition>>pre_tokens>>$<<", pre_tokens)
        return outer_processed, requeue_line_info

    # pylint: enable=too-many-arguments
