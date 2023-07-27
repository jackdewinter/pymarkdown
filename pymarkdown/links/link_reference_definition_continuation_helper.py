"""
Module to helper with determining whether to continue with the link reference definitions.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.links.link_parse_helper import LinkParseHelper
from pymarkdown.links.link_reference_definition_parse_helper import (
    LinkReferenceDefinitionParseHelper,
)
from pymarkdown.links.link_reference_tuple import LinkReferenceDefinitionTuple
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tab_helper import TabHelper
from pymarkdown.tokens.container_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.leaf_markdown_token import LinkReferenceDefinitionMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import LinkDefinitionStackToken

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-few-public-methods


class LinkReferenceDefinitionContinuationHelper:
    """
    Class to helper with determining whether to continue with the link reference definitions.
    """

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    @staticmethod
    def determine_continue_or_stop(
        parser_state: ParserState,
        position_marker: PositionMarker,
        was_started: bool,
        remaining_line_to_parse: str,
        extracted_whitespace: Optional[str],
        unmodified_line_to_parse: str,
        original_stack_depth: int,
        original_document_depth: int,
        end_lrd_index: Optional[int],
        line_to_parse_size: int,
        is_blank_line: Optional[bool],
        did_complete_lrd: bool,
        parsed_lrd_tuple: Optional[LinkReferenceDefinitionTuple],
        lines_to_requeue: List[str],
        process_mode: int,
    ) -> Tuple[bool, bool, List[MarkdownToken]]:
        """
        Determine whether to continue with the processing of the LRD.
        """
        assert is_blank_line is not None
        assert end_lrd_index is not None
        did_pause_lrd: bool = (
            end_lrd_index >= 0
            and end_lrd_index == line_to_parse_size
            and not is_blank_line
        )
        if did_pause_lrd:
            POGGER.debug(">>parse_link_reference_definition>>continuation")
            LinkReferenceDefinitionContinuationHelper.__add_line_for_lrd_continuation(
                parser_state,
                position_marker,
                was_started,
                remaining_line_to_parse,
                extracted_whitespace,
                unmodified_line_to_parse,
                original_stack_depth,
                original_document_depth,
            )
        if not did_pause_lrd and was_started or did_complete_lrd:
            return LinkReferenceDefinitionContinuationHelper.__stop_lrd_continuation(
                parser_state,
                did_complete_lrd,
                parsed_lrd_tuple,
                end_lrd_index,
                remaining_line_to_parse,
                is_blank_line,
                lines_to_requeue,
                extracted_whitespace,
                process_mode,
                did_pause_lrd,
            )

        POGGER.debug(">>parse_link_reference_definition>>other")
        return did_pause_lrd, False, []

    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __stop_lrd_continuation(
        parser_state: ParserState,
        did_complete_lrd: bool,
        parsed_lrd_tuple: Optional[LinkReferenceDefinitionTuple],
        end_lrd_index: int,
        remaining_line_to_parse: str,
        is_blank_line: bool,
        lines_to_requeue: List[str],
        extracted_whitespace: Optional[str],
        process_mode: int,
        did_pause_lrd: bool,
    ) -> Tuple[bool, bool, List[MarkdownToken]]:
        """
        As part of processing a link reference definition, stop a continuation.
        """

        POGGER.debug(">>parse_link_reference_definition>>no longer need start")
        if did_complete_lrd:
            assert parsed_lrd_tuple
            assert parsed_lrd_tuple.normalized_destination is not None
            did_add_definition = LinkParseHelper.add_link_definition(
                parsed_lrd_tuple.normalized_destination, parsed_lrd_tuple.link_titles
            )
            assert not (end_lrd_index < -1 and remaining_line_to_parse)
            link_def_token = cast(
                LinkDefinitionStackToken, parser_state.token_stack[-1]
            )
            assert link_def_token.extracted_whitespace is not None
            extracted_whitespace = link_def_token.extracted_whitespace

            POGGER.debug(
                "link_def_token.extracted_whitespace>:$:<",
                link_def_token.extracted_whitespace,
            )
            POGGER.debug(
                "link_def_token.continuation_lines>:$:<",
                link_def_token.continuation_lines,
            )
            POGGER.debug(
                "link_def_token.unmodified_lines>:$:<", link_def_token.unmodified_lines
            )
            POGGER.debug("lines_to_requeue>:$:<", lines_to_requeue)

            does_any_line_have_tabs = any(
                ParserHelper.tab_character in ffg
                for ffg in link_def_token.unmodified_lines
            )
            POGGER.debug("does_any_line_have_tabs>:$:<", does_any_line_have_tabs)

            last_container_index = parser_state.find_last_container_on_stack()
            if does_any_line_have_tabs and last_container_index > 0:
                (
                    extracted_whitespace,
                    parsed_lrd_tuple,
                ) = LinkReferenceDefinitionContinuationHelper.__stop_lrd_continuation_with_tab(
                    parser_state,
                    link_def_token,
                    last_container_index,
                    lines_to_requeue,
                    process_mode,
                    extracted_whitespace,
                    parsed_lrd_tuple,
                )

            assert extracted_whitespace is not None
            assert parsed_lrd_tuple.normalized_destination is not None
            new_tokens: List[MarkdownToken] = [
                LinkReferenceDefinitionMarkdownToken(
                    did_add_definition,
                    extracted_whitespace,
                    parsed_lrd_tuple.normalized_destination,
                    parsed_lrd_tuple.link_titles,
                    parsed_lrd_tuple.link_info,
                    position_marker=link_def_token.start_position_marker,
                )
            ]
            POGGER.debug(">>link_info>>$", parsed_lrd_tuple.link_info)
            assert parsed_lrd_tuple.link_info.line_destination_whitespace is not None
            POGGER.debug(
                ">>line_destination_whitespace>>$",
                ParserHelper.make_whitespace_visible(
                    parsed_lrd_tuple.link_info.line_destination_whitespace
                ),
            )
            POGGER.debug(">>new_tokens>>$", new_tokens)
            del parser_state.token_stack[-1]
            return did_pause_lrd, len(lines_to_requeue) > 1, new_tokens

        assert is_blank_line
        del parser_state.token_stack[-1]
        return did_pause_lrd, True, []

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __stop_lrd_continuation_with_tab(
        parser_state: ParserState,
        link_def_token: LinkDefinitionStackToken,
        last_container_index: int,
        lines_to_requeue: List[str],
        process_mode: int,
        extracted_whitespace: Optional[str],
        parsed_lrd_tuple: LinkReferenceDefinitionTuple,
    ) -> Tuple[Optional[str], LinkReferenceDefinitionTuple]:
        POGGER.debug(
            "extracted_whitespace>:$:<",
            link_def_token.extracted_whitespace,
        )
        assert parser_state.token_stack[last_container_index].is_block_quote
        last_block_quote_index = parser_state.find_last_block_quote_on_stack()
        last_block_quote_token = parser_state.token_stack[last_block_quote_index]
        block_quote_token = cast(
            BlockQuoteMarkdownToken, last_block_quote_token.matching_markdown_token
        )

        POGGER.debug(
            "link_def_token.continuation_lines>:$:<", link_def_token.continuation_lines
        )
        POGGER.debug(
            "link_def_token.unmodified_lines>:$:<", link_def_token.unmodified_lines
        )

        if len(link_def_token.continuation_lines) == 1:
            extracted_whitespace = LinkReferenceDefinitionContinuationHelper.__stop_lrd_continuation_with_tab_single(
                parser_state,
                link_def_token,
                process_mode,
                block_quote_token,
                lines_to_requeue,
            )
        else:
            (
                extracted_whitespace,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionContinuationHelper.__stop_lrd_continuation_with_tab_multiple(
                parser_state, extracted_whitespace, link_def_token, block_quote_token
            )

        return extracted_whitespace, parsed_lrd_tuple

    # pylint: enable=too-many-arguments

    @staticmethod
    def __stop_lrd_continuation_with_tab_single(
        parser_state: ParserState,
        link_def_token: LinkDefinitionStackToken,
        process_mode: int,
        block_quote_token: BlockQuoteMarkdownToken,
        lines_to_requeue: List[str],
    ) -> str:
        parsed_lines = link_def_token.continuation_lines[0]
        original_lines = link_def_token.unmodified_lines[0]

        (
            extracted_whitespace,
            split_tab,
            _,
        ) = LinkReferenceDefinitionContinuationHelper.__find_line_ws(
            parsed_lines, original_lines
        )

        POGGER.debug("process_mode>:$:<", process_mode)
        POGGER.debug(
            "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        )
        if process_mode == 1:
            block_quote_token.remove_last_bleading_space()
        else:
            for _ in lines_to_requeue:
                block_quote_token.remove_last_bleading_space()

        if split_tab:
            TabHelper.adjust_block_quote_indent_for_tab(parser_state)
        POGGER.debug(
            "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        )
        return extracted_whitespace

    @staticmethod
    def __stop_lrd_continuation_with_tab_multiple(
        parser_state: ParserState,
        extracted_whitespace: Optional[str],
        link_def_token: LinkDefinitionStackToken,
        block_quote_token: BlockQuoteMarkdownToken,
    ) -> Tuple[Optional[str], LinkReferenceDefinitionTuple]:
        split_tabs_list: List[bool] = []
        completed_lrd_text: str = ""
        alt_ws: Optional[str] = None
        for this_line_index, this_line in enumerate(link_def_token.continuation_lines):
            (
                completed_lrd_text,
                extracted_whitespace,
                alt_ws,
            ) = LinkReferenceDefinitionContinuationHelper.__stop_lrd_continuation_with_tab_multiple_loop(
                link_def_token,
                this_line_index,
                this_line,
                completed_lrd_text,
                extracted_whitespace,
                alt_ws,
                split_tabs_list,
            )

        POGGER.debug("completed_lrd_text>:$:<", completed_lrd_text)
        (
            did_succeed,
            next_index,
            new_parsed_lrd_tuple,
        ) = LinkReferenceDefinitionParseHelper.parse_link_reference_definition(
            parser_state, completed_lrd_text, 0, alt_ws, True
        )
        assert did_succeed
        assert len(completed_lrd_text) == next_index
        assert new_parsed_lrd_tuple is not None
        parsed_lrd_tuple = new_parsed_lrd_tuple

        LinkReferenceDefinitionContinuationHelper.__xx_multiple_fix_leading_spaces(
            block_quote_token, split_tabs_list, link_def_token
        )
        return extracted_whitespace, parsed_lrd_tuple

    # pylint: disable=too-many-arguments
    @staticmethod
    def __stop_lrd_continuation_with_tab_multiple_loop(
        link_def_token: LinkDefinitionStackToken,
        this_line_index: int,
        this_line: str,
        completed_lrd_text: str,
        extracted_whitespace: Optional[str],
        alt_ws: Optional[str],
        split_tabs_list: List[bool],
    ) -> Tuple[str, Optional[str], Optional[str]]:
        original_this_line = link_def_token.unmodified_lines[this_line_index]
        POGGER.debug("this_line_index>:$:<", this_line_index)
        POGGER.debug("this_line>:$:<", this_line)
        POGGER.debug("original_this_line>:$:<", original_this_line)

        (
            extracted_ws,
            split_tab,
            start_whitespace_index,
        ) = LinkReferenceDefinitionContinuationHelper.__find_line_ws(
            this_line, original_this_line
        )

        if completed_lrd_text:
            completed_lrd_text += "\n"
        if this_line_index == 0:
            extracted_whitespace = extracted_ws
            alt_ws = TabHelper.detabify_string(
                extracted_whitespace, start_whitespace_index
            )
        else:
            completed_lrd_text += extracted_ws
        completed_lrd_text += this_line
        split_tabs_list.append(split_tab)
        return completed_lrd_text, extracted_whitespace, alt_ws

    # pylint: enable=too-many-arguments

    @staticmethod
    def __find_line_ws(parsed_lines: str, original_lines: str) -> Tuple[str, bool, int]:
        start_text_index = original_lines.find(parsed_lines)
        assert start_text_index != -1
        POGGER.debug("start_text_index>:$:<", start_text_index)
        start_whitespace_index, _ = ParserHelper.extract_spaces_from_end(
            original_lines, start_text_index
        )
        POGGER.debug("start_whitespace_index>:$:<", start_whitespace_index)
        tabified_whitespace = original_lines[start_whitespace_index:start_text_index]
        POGGER.debug("tabified_whitespace>:$:<", tabified_whitespace)
        split_tab = bool(tabified_whitespace and tabified_whitespace[0] == "\t")
        if not split_tab:
            tabified_whitespace = tabified_whitespace[1:]
            start_whitespace_index += 1
        extracted_whitespace = tabified_whitespace
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        POGGER.debug("split_tab>:$:<", split_tab)
        return extracted_whitespace, split_tab, start_whitespace_index

    @staticmethod
    def __xx_multiple_fix_leading_spaces(
        block_quote_token: BlockQuoteMarkdownToken,
        split_tabs_list: List[bool],
        link_def_token: LinkDefinitionStackToken,
    ) -> None:
        POGGER.debug("split_tabs_list>:$:<", split_tabs_list)
        POGGER.debug(
            "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        )
        assert block_quote_token.bleading_spaces is not None
        leading_spaces: List[str] = []
        for _ in link_def_token.continuation_lines:
            last_leading_space = block_quote_token.remove_last_bleading_space()
            POGGER.debug("last_leading_space>:$:<", last_leading_space)
            if last_leading_space[0] == "\n":
                last_leading_space = last_leading_space[1:]
            leading_spaces.append(last_leading_space)
        assert len(split_tabs_list) == len(leading_spaces)
        POGGER.debug("leading_spaces>:$:<", leading_spaces)
        POGGER.debug(
            "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        )
        is_first = len(block_quote_token.bleading_spaces) == 0
        for prefix_to_add in leading_spaces:
            if split_tabs_list[0]:
                prefix_to_add = prefix_to_add[:-1]
            del split_tabs_list[0]
            block_quote_token.add_bleading_spaces(prefix_to_add, is_first)
            is_first = False

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_line_for_lrd_continuation(
        parser_state: ParserState,
        position_marker: PositionMarker,
        was_started: bool,
        remaining_line_to_parse: str,
        extracted_whitespace: Optional[str],
        unmodified_line_to_parse: str,
        original_stack_depth: int,
        original_document_depth: int,
    ) -> None:
        """
        As part of processing a link reference definition, add a line to the continuation.
        """

        line_to_store = remaining_line_to_parse
        if not was_started:
            POGGER.debug(">>parse_link_reference_definition>>marking start")
            new_token = LinkDefinitionStackToken(extracted_whitespace, position_marker)
            parser_state.token_stack.append(new_token)
            new_token.original_stack_depth = original_stack_depth
            new_token.original_document_depth = original_document_depth

            new_token.last_block_quote_stack_token = (
                parser_state.last_block_quote_stack_token
            )
            new_token.last_block_quote_markdown_token_index = (
                parser_state.last_block_quote_markdown_token_index
            )
            new_token.copy_of_last_block_quote_markdown_token = (
                parser_state.copy_of_last_block_quote_markdown_token
            )
            new_token.copy_of_token_stack = parser_state.copy_of_token_stack
        else:
            new_token = cast(LinkDefinitionStackToken, parser_state.token_stack[-1])

        POGGER.debug(">>line_to_store>>add>:$<<", line_to_store)
        POGGER.debug(">>unmodified_line_to_parse>>add>:$<<", unmodified_line_to_parse)
        assert unmodified_line_to_parse.endswith(line_to_store)
        new_token.add_continuation_line(line_to_store)
        new_token.add_unmodified_line(unmodified_line_to_parse)

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
