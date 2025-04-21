"""
Module to provide processing for non-fenced-code-block sections.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_count_helper import BlockQuoteCountHelper
from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.requeue_line_info import RequeueLineInfo
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import BlockQuoteStackToken, ListStackToken

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-few-public-methods


class BlockQuoteNonFencedHelper:
    """
    Class to provide processing for non-fenced-code-block sections.
    """

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def handle_non_fenced_code_section(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        extracted_whitespace: str,
        position_marker: PositionMarker,
        original_start_index: int,
        container_start_bq_count: int,
        line_to_parse: str,
        start_index: int,
        leaf_tokens: List[MarkdownToken],
        original_line: str,
        last_block_quote_index: int,
        avoid_block_starts: bool,
    ) -> Tuple[
        str,
        int,
        List[MarkdownToken],
        List[MarkdownToken],
        BlockQuoteData,
        int,
        bool,
        int,
        Optional[str],
        bool,
        Optional[RequeueLineInfo],
        bool,
    ]:
        """
        Handle a non-fenced code block within a block quote.
        """

        POGGER.debug("handle_block_quote_section>>not fenced")
        (
            container_level_tokens,
            requeue_line_info,
            force_list_continuation,
            block_quote_data,
        ) = BlockQuoteCountHelper.ensure_stack_at_level(
            parser_state,
            block_quote_data,
            extracted_whitespace,
            position_marker,
            original_start_index,
            container_start_bq_count,
        )
        POGGER.debug("force_list_continuation=$", force_list_continuation)
        if requeue_line_info:
            return (
                line_to_parse,
                start_index,
                leaf_tokens,
                container_level_tokens,
                block_quote_data,
                0,
                False,
                last_block_quote_index,
                None,
                avoid_block_starts,
                requeue_line_info,
                force_list_continuation,
            )
        # POGGER.debug("extracted_whitespace:$:", extracted_whitespace)
        # POGGER.debug("line_to_parse:$:", line_to_parse)
        # POGGER.debug("start_index:$:", start_index)
        # POGGER.debug(
        #     "position_marker.index_number:$:", position_marker.index_number
        # )
        # POGGER.debug(
        #     "position_marker.index_indent:$:", position_marker.index_indent
        # )
        removed_text = f"{extracted_whitespace}{line_to_parse[position_marker.index_number : start_index]}"
        # POGGER.debug(
        #     "==EWS[$],OSI[$],SI[$],LTP[$],RT=[$]",
        #     extracted_whitespace,
        #     original_start_index,
        #     position_marker.index_number,
        #     position_marker.text_to_parse,
        #     removed_text,
        # )

        (
            line_to_parse,
            removed_chars_at_start,
            text_removed_by_container,
            did_blank,
            leaf_tokens,
            requeue_line_info,
        ) = BlockQuoteNonFencedHelper.__handle_non_fenced_code_section_no_requeue(
            parser_state,
            position_marker,
            line_to_parse,
            start_index,
            removed_text,
            container_start_bq_count,
            block_quote_data,
            original_start_index,
            # extra_consumed_whitespace,
            container_level_tokens,
            original_line,
        )
        return (
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            block_quote_data,
            removed_chars_at_start,
            did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            requeue_line_info,
            force_list_continuation,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_non_fenced_code_section_no_requeue(
        parser_state: ParserState,
        position_marker: PositionMarker,
        line_to_parse: str,
        start_index: int,
        removed_text: str,
        container_start_bq_count: int,
        block_quote_data: BlockQuoteData,
        original_start_index: int,
        # extra_consumed_whitespace: Optional[int],
        container_level_tokens: List[MarkdownToken],
        original_line: str,
    ) -> Tuple[str, int, str, bool, List[MarkdownToken], Optional[RequeueLineInfo]]:
        (
            line_to_parse,
            stack_index,
        ) = (
            line_to_parse[start_index:],
            parser_state.find_last_block_quote_on_stack(),
        )
        POGGER.debug("==REM[$],LTP[$]", removed_text, line_to_parse)

        assert (
            stack_index != -1
        ), "There must be a block quote on the stack if we are in here."
        found_bq_stack_token = cast(
            BlockQuoteStackToken, parser_state.token_stack[stack_index]
        )
        is_not_blank_line = bool(line_to_parse.strip(Constants.ascii_whitespace))

        BlockQuoteNonFencedHelper.__do_block_quote_leading_spaces_adjustments(
            parser_state,
            stack_index,
            container_start_bq_count,
            block_quote_data,
            removed_text,
            found_bq_stack_token,
            removed_text,
            original_start_index,
            # extra_consumed_whitespace,
            container_level_tokens,
            original_line,
            is_not_blank_line,
            position_marker,
        )
        POGGER.debug("text_removed_by_container=[$]", removed_text)
        POGGER.debug("removed_text=[$]", removed_text)
        if is_not_blank_line:
            return (line_to_parse, start_index, removed_text, False, [], None)
        did_blank, leaf_tokens, requeue_line_info = (
            BlockQuoteNonFencedHelper.__handle_normal_blank_line(
                parser_state,
                block_quote_data,
                position_marker,
                removed_text,
                line_to_parse,
            )
        )
        return (
            line_to_parse,
            start_index,
            removed_text,
            did_blank,
            leaf_tokens,
            requeue_line_info,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __do_block_quote_leading_spaces_adjustments(
        parser_state: ParserState,
        stack_index: int,
        container_start_bq_count: int,
        block_quote_data: BlockQuoteData,
        text_removed_by_container: str,
        found_bq_stack_token: BlockQuoteStackToken,
        removed_text: str,
        original_start_index: int,
        container_level_tokens: List[MarkdownToken],
        original_line: str,
        is_not_blank_line: bool,
        position_marker: PositionMarker,
    ) -> None:
        POGGER.debug("__hbqs>>removed_text>>:$:<", removed_text)
        POGGER.debug("__hbqs>>container_start_bq_count>>$", container_start_bq_count)
        POGGER.debug("__hbqs>>original_start_index>>$", original_start_index)
        POGGER.debug("token_stack--$", parser_state.token_stack)
        original_start_index = BlockQuoteNonFencedHelper.__block_quote_start_adjust(
            parser_state, original_start_index, container_level_tokens
        )
        # original_removed_text = removed_text
        adjusted_removed_text = (
            removed_text[original_start_index:]
            if container_start_bq_count and original_start_index
            else removed_text
        )

        POGGER.debug("dbqlsa>>adjusted_removed_text>>:$:<", adjusted_removed_text)
        (
            adjusted_removed_text,
            tabbed_removed_text,
        ) = BlockQuoteNonFencedHelper.__adjust_1(
            parser_state,
            container_start_bq_count,
            adjusted_removed_text,
            text_removed_by_container,
            stack_index,
            block_quote_data,
            original_line,
        )
        POGGER.debug("dbqlsa>>adjusted_removed_text>>:$:<", adjusted_removed_text)
        POGGER.debug("dbqlsa>>tabbed_removed_text>>:$:<", tabbed_removed_text)

        POGGER.debug("__hbqs>>adjusted_removed_text>>:$:<", adjusted_removed_text)
        POGGER.debug("__hbqs>>tabbed_removed_text>>:$:<", tabbed_removed_text)
        POGGER.debug("token_stack--$", parser_state.token_stack)
        POGGER.debug("token_document--$", parser_state.token_document)
        POGGER.debug("dbqlsa>>found_bq_stack_token>>$", found_bq_stack_token)

        POGGER.debug("dbqlsa>>adjusted_removed_text>>:$:<<", adjusted_removed_text)
        special_case = False
        POGGER.debug("dbqlsa>>adjusted_removed_text>>:$:<<", adjusted_removed_text)
        POGGER.debug("dbqlsa>>special_case>>$", special_case)

        BlockQuoteNonFencedHelper.__do_block_quote_leading_spaces_adjustments_adjust_bleading(
            parser_state,
            found_bq_stack_token,
            tabbed_removed_text,
            adjusted_removed_text,
            special_case,
            is_not_blank_line,
            stack_index,
            position_marker,
            text_removed_by_container,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_normal_blank_line(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        position_marker: PositionMarker,
        text_removed_by_container: str,
        line_to_parse: str,
    ) -> Tuple[bool, List[MarkdownToken], Optional[RequeueLineInfo]]:
        POGGER.debug("call __handle_block_quote_section>>handle_blank_line")

        POGGER.debug(
            "__hbqs>>block_quote_data.current_count>>$", block_quote_data.current_count
        )
        POGGER.debug("__hbqs>>token_stack>>$", parser_state.token_stack)

        adjusted_position_marker = PositionMarker(
            position_marker.line_number,
            len(text_removed_by_container),
            position_marker.text_to_parse,
        )
        (leaf_tokens, requeue_line_info) = parser_state.handle_blank_line_fn(
            parser_state,
            line_to_parse,
            from_main_transform=False,
            position_marker=adjusted_position_marker,
        )
        assert (
            leaf_tokens is not None
        ), "Handling of blank lines always produces tokens."
        POGGER.debug("handle_block_quote_section>>leaf_tokens>>$", leaf_tokens)
        # assert not (
        #     requeue_line_info and requeue_line_info.lines_to_requeue
        # ), "No handling of requeuing available here."

        return True, leaf_tokens, requeue_line_info

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_1(
        parser_state: ParserState,
        container_start_bq_count: int,
        adjusted_removed_text: str,
        text_removed_by_container: str,
        stack_index: int,
        block_quote_data: BlockQuoteData,
        original_line: str,
    ) -> Tuple[str, Optional[str]]:
        POGGER.debug("__hbqs>>container_start_bq_count>>$", container_start_bq_count)
        POGGER.debug(
            "__hbqs>>token_stack[stack_index - 1]>>$",
            parser_state.token_stack[stack_index - 1],
        )
        if (
            container_start_bq_count
            and parser_state.token_stack[stack_index - 1].is_block_quote
        ):
            block_stack_token = cast(
                BlockQuoteStackToken, parser_state.token_stack[stack_index - 1]
            )
            count_of_actual_starts = ParserHelper.count_characters_in_text(
                adjusted_removed_text, ">"
            )
            assert (
                count_of_actual_starts != block_quote_data.current_count
            ), "Block quote start counts are expected to be different"
            block_quote_token = cast(
                BlockQuoteMarkdownToken, block_stack_token.matching_markdown_token
            )
            adj_leading_spaces = block_quote_token.bleading_spaces
            assert adj_leading_spaces is not None, "Leading spaces should not be None."
            POGGER.debug("__hbqs>>count_of_actual_starts>>$", count_of_actual_starts)
            POGGER.debug("__hbqs>>original_line>:$:<", original_line)
            POGGER.debug(
                "__hbqs>>adj_leading_spaces>>:$:$:<",
                len(adj_leading_spaces),
                adj_leading_spaces,
            )
            POGGER.debug(
                "__hbqs>>adjusted_removed_text>>:$:$:<",
                len(adjusted_removed_text),
                adjusted_removed_text,
            )
            POGGER.debug(
                "__hbqs>>text_removed_by_container>>:$:$:<",
                len(text_removed_by_container),
                text_removed_by_container,
            )
            last_line_index = adj_leading_spaces.rfind("\n")
            if last_line_index != -1:
                adj_leading_spaces = adj_leading_spaces[last_line_index + 1 :]

            delta = len(text_removed_by_container) - len(
                adj_leading_spaces + adjusted_removed_text
            )
            adj_leading_spaces = adj_leading_spaces + ParserHelper.repeat_string(
                ParserHelper.space_character, delta
            )
            adjusted_removed_text = adj_leading_spaces + adjusted_removed_text

            POGGER.debug("__hbqs>>adjusted_removed_text>>:$:<", adjusted_removed_text)

        POGGER.debug("__hbqs>>adjusted_removed_text>>:$:<", adjusted_removed_text)
        tabbed_removed_text = BlockQuoteNonFencedHelper.__adjust_1_with_tab(
            original_line, adjusted_removed_text
        )
        return (adjusted_removed_text, tabbed_removed_text)

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_1_with_tab(
        original_line: str, adjusted_removed_text: str
    ) -> Optional[str]:
        tabbed_removed_text = None

        if "\t" in original_line:
            POGGER.debug("original_line>>:$:<", original_line)
            detabified_original_line = TabHelper.detabify_string(original_line)
            POGGER.debug("detabified_original_line>>:$:<", detabified_original_line)
            assert detabified_original_line.startswith(
                adjusted_removed_text
            ), "Detabbified line must start with the text that was removed."
            original_line_index = 1
            while original_line_index < len(original_line):
                original_line_prefix = original_line[:original_line_index]
                POGGER.debug("original_line_prefix>>:$:<", original_line_prefix)
                detabified_original_line_prefix = TabHelper.detabify_string(
                    original_line_prefix
                )
                POGGER.debug(
                    "detabified_original_line_prefix>>:$:<",
                    detabified_original_line_prefix,
                )
                if detabified_original_line_prefix == adjusted_removed_text:
                    break
                original_line_index += 1
            POGGER.debug(
                "original_line_prefix>>:$:< == detabified_original_line_prefix>>:$:<",
                original_line_prefix,
                detabified_original_line_prefix,
            )
            if (
                adjusted_removed_text != original_line_prefix
                and detabified_original_line_prefix == adjusted_removed_text
            ):
                tabbed_removed_text = original_line_prefix
        return tabbed_removed_text

    @staticmethod
    def __block_quote_start_adjust(
        parser_state: ParserState,
        original_start_index: int,
        container_level_tokens: List[MarkdownToken],
    ) -> int:
        POGGER.debug("container_level_tokens--$", container_level_tokens)
        if container_level_tokens:
            start_index = len(parser_state.token_stack) - 1
            while start_index and not parser_state.token_stack[start_index].is_list:
                start_index -= 1
            if start_index:
                list_token = cast(ListStackToken, parser_state.token_stack[start_index])
                POGGER.debug("token_stack[start_index]--$", list_token)
                POGGER.debug(
                    "list_token.last_new_list_token--$",
                    list_token.last_new_list_token,
                )
                if (
                    list_token.last_new_list_token
                    and list_token.last_new_list_token.line_number
                    == container_level_tokens[0].line_number
                ):
                    POGGER.debug("BOOM")
                    indent_delta = (
                        list_token.last_new_list_token.indent_level
                        - list_token.last_new_list_token.column_number
                    ) - 1
                    if list_token.is_ordered_list:
                        indent_delta -= len(
                            list_token.last_new_list_token.list_start_content
                        )
                    POGGER.debug("indent_delta=:$:", indent_delta)
                    original_start_index -= indent_delta
        return original_start_index

    @staticmethod
    def __do_block_quote_leading_spaces_adjustments_adjust_bleading_part_1(
        parser_state: ParserState,
        stack_index: int,
        block_quote_token: BlockQuoteMarkdownToken,
    ) -> None:
        previous_stack_token = parser_state.token_stack[stack_index - 1]
        if previous_stack_token.is_block_quote:
            previous_markdown_token = cast(
                BlockQuoteMarkdownToken, previous_stack_token.matching_markdown_token
            )
            assert previous_markdown_token is not None
            if (
                previous_markdown_token.line_number == block_quote_token.line_number
                and previous_markdown_token.bleading_spaces == ""
            ):
                block_quote_token.weird_kludge_three = True
            if block_quote_token.leading_text_index == 1:
                assert previous_markdown_token.bleading_spaces is not None
                split_bleading_spaces = previous_markdown_token.bleading_spaces.split(
                    "\n"
                )
                block_quote_token.weird_kludge_four = (
                    previous_markdown_token.line_number,
                    previous_markdown_token.column_number,
                    previous_markdown_token.leading_text_index - 1,
                    split_bleading_spaces[
                        previous_markdown_token.leading_text_index - 1
                    ],
                )

    @staticmethod
    def __do_block_quote_leading_spaces_adjustments_adjust_bleading_part_2(
        parser_state: ParserState,
        position_marker: PositionMarker,
        stack_index: int,
        found_bq_stack_token: BlockQuoteStackToken,
    ) -> None:
        assert parser_state.token_stack[stack_index] == found_bq_stack_token
        found_list_stack_index = 0
        for search_index in range(stack_index, 0, -1):
            if (
                parser_state.token_stack[search_index].is_list
                and not found_list_stack_index
            ):
                found_list_stack_index = search_index
        if found_list_stack_index:
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[
                    found_list_stack_index
                ].matching_markdown_token,
            )
            if position_marker.line_number != list_token.line_number:
                POGGER.debug(
                    "__do_block_quote_leading_spaces_adjustments_adjust_bleading>>list_token>>$",
                    list_token,
                )
                list_token.add_leading_spaces("")
                POGGER.debug(
                    "__do_block_quote_leading_spaces_adjustments_adjust_bleading>>list_token>>$",
                    list_token,
                )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __do_block_quote_leading_spaces_adjustments_adjust_bleading(
        parser_state: ParserState,
        found_bq_stack_token: BlockQuoteStackToken,
        tabbed_removed_text: Optional[str],
        adjusted_removed_text: str,
        special_case: bool,
        is_not_blank_line: bool,
        stack_index: int,
        position_marker: PositionMarker,
        text_removed_by_container: str,
    ) -> None:
        assert (
            found_bq_stack_token.matching_markdown_token is not None
        ), "Block quote stack tokens always have matching markdown tokens."
        block_quote_token = cast(
            BlockQuoteMarkdownToken, found_bq_stack_token.matching_markdown_token
        )
        POGGER.debug("dbqlsa>>last_block_token>>$", block_quote_token)
        POGGER.debug(
            "dbqlsa>>leading_text_index>>$", block_quote_token.leading_text_index
        )
        POGGER.debug("dbqlsa>>bq>>$", block_quote_token)
        POGGER.debug("dbqlsa>>tabbed_removed_text>>$", tabbed_removed_text)

        adjusted_removed_text = BlockQuoteNonFencedHelper.__check_for_kludge(
            parser_state,
            block_quote_token,
            stack_index,
            text_removed_by_container,
            adjusted_removed_text,
        )

        if not block_quote_token.weird_kludge_five:
            BlockQuoteNonFencedHelper.__do_block_quote_leading_spaces_adjustments_adjust_bleading_kludge(
                parser_state, block_quote_token, stack_index, adjusted_removed_text
            )
        POGGER.debug(
            "__do_block_quote_leading_spaces_adjustments_adjust_bleading>>block_token>>$",
            block_quote_token,
        )
        block_quote_token.add_bleading_spaces(
            adjusted_removed_text,
            special_case,
            tabbed_removed_text,
        )
        POGGER.debug(
            "__do_block_quote_leading_spaces_adjustments_adjust_bleading>>block_token>>$",
            block_quote_token,
        )

        # This checks to see if, when the first line of a block quote is encountered, if the
        # inner block quote exists and its bleading spaces are blank. If so, then the current
        # block quote was arrived at through group of block quotes together, not on building
        # on the inner block quote. If that was the case, the inner block quote would have at
        # least the bleading space from processing that block quote.  This does not mean anything
        # to the parser, but when reconstructing the Markdown, this is an important distinction.
        block_quote_token.leading_text_index += 1
        if stack_index > 1:
            BlockQuoteNonFencedHelper.__do_block_quote_leading_spaces_adjustments_adjust_bleading_part_1(
                parser_state, stack_index, block_quote_token
            )

        POGGER.debug("dbqlsa>>last_block_token>>$", block_quote_token)
        POGGER.debug(
            "dbqlsa>>leading_text_index>>$", block_quote_token.leading_text_index
        )
        if not is_not_blank_line:
            BlockQuoteNonFencedHelper.__do_block_quote_leading_spaces_adjustments_adjust_bleading_part_2(
                parser_state, position_marker, stack_index, found_bq_stack_token
            )

        POGGER.debug("__hbqs>>bq>>$", block_quote_token)

    # pylint: enable=too-many-arguments

    @staticmethod
    def __do_block_quote_leading_spaces_adjustments_adjust_bleading_kludge(
        parser_state: ParserState,
        block_quote_token: BlockQuoteMarkdownToken,
        stack_index: int,
        adjusted_removed_text: str,
    ) -> None:

        assert block_quote_token.leading_text_index == 0
        search_index = stack_index - 1
        while (
            search_index > 0
            and not parser_state.token_stack[search_index].is_block_quote
        ):
            search_index -= 1
        if search_index:  # and search_index + 1 == stack_index:
            search_token = parser_state.token_stack[
                search_index
            ].matching_markdown_token
            assert search_token is not None
            found_token = parser_state.token_stack[search_index].matching_markdown_token
            assert found_token is not None
            bq_token = cast(BlockQuoteMarkdownToken, found_token)
            assert bq_token.bleading_spaces is not None
            split_spaces = bq_token.bleading_spaces.split("\n")
            if len(split_spaces) > 1:
                last_split_space = split_spaces[-1]
                if (
                    adjusted_removed_text != last_split_space
                    and adjusted_removed_text.startswith(last_split_space)
                ):
                    block_quote_token.weird_kludge_six = True

    @staticmethod
    def __check_for_kludge(
        parser_state: ParserState,
        block_quote_token: BlockQuoteMarkdownToken,
        stack_index: int,
        text_removed_by_container: str,
        adjusted_removed_text: str,
    ) -> str:
        if not block_quote_token.bleading_spaces and stack_index > 3:
            continue_with_adjustment = (
                parser_state.token_stack[stack_index - 1].is_list
                and parser_state.token_stack[stack_index - 2].is_list
                and parser_state.token_stack[stack_index - 3].is_block_quote
            )
            if continue_with_adjustment:
                lists_new_list_token = cast(
                    ListStackToken, parser_state.token_stack[stack_index - 1]
                ).last_new_list_token
                if lists_new_list_token is not None:
                    continue_with_adjustment = (
                        block_quote_token.line_number
                        != lists_new_list_token.line_number
                    )
                else:
                    bq_inner_token = parser_state.token_stack[
                        stack_index - 3
                    ].matching_markdown_token
                    assert bq_inner_token is not None
                    continue_with_adjustment = (
                        block_quote_token.line_number != bq_inner_token.line_number
                    )
            if continue_with_adjustment:
                assert parser_state.original_line_to_parse is not None
                adjusted_removed_text = parser_state.original_line_to_parse[
                    : len(text_removed_by_container)
                ]
        return adjusted_removed_text


# pylint: enable=too-few-public-methods
