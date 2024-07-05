"""
Module to provide processing for the block quotes.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_count_helper import BlockQuoteCountHelper
from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.block_quotes.block_quote_non_fenced_helper import (
    BlockQuoteNonFencedHelper,
)
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.requeue_line_info import RequeueLineInfo
from pymarkdown.leaf_blocks.leaf_block_processor import LeafBlockProcessor
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import (
    BlockQuoteStackToken,
    FencedCodeBlockStackToken,
    ListStackToken,
    StackToken,
)

POGGER = ParserLogger(logging.getLogger(__name__))


class BlockQuoteProcessor:
    """
    Class to provide processing for the block quotes.
    """

    @staticmethod
    def __adjust_lazy_handling(
        parser_state: ParserState,
        line_to_parse: str,
        extracted_whitespace: str,
        was_paragraph_continuation: bool,
    ) -> Tuple[bool, bool]:
        if (
            parser_state.token_stack[-1].is_paragraph
            and not parser_state.token_document[-1].is_blank_line
        ):
            was_paragraph_continuation = True
            POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)

            is_leaf_block_start = (
                LeafBlockProcessor.is_paragraph_ending_leaf_block_start(
                    parser_state,
                    line_to_parse,
                    0,
                    extracted_whitespace,
                )
            )

            POGGER.debug("is_leaf_block_start:$", is_leaf_block_start)
            if is_leaf_block_start:
                was_paragraph_continuation = False
                POGGER.debug(
                    "was_paragraph_continuation>>$", was_paragraph_continuation
                )
        else:
            is_leaf_block_start = False
        return was_paragraph_continuation, is_leaf_block_start

    # pylint: disable=too-many-arguments
    @staticmethod
    def check_for_lazy_handling(
        parser_state: ParserState,
        position_marker: PositionMarker,
        block_quote_data: BlockQuoteData,
        line_to_parse: str,
        extracted_whitespace: str,
        was_paragraph_continuation: bool,
    ) -> Tuple[List[MarkdownToken], BlockQuoteData, bool]:
        """
        Check if there is any processing to be handled during the handling of
        lazy continuation lines in block quotes.
        """
        POGGER.debug("__check_for_lazy_handling")
        container_level_tokens: List[MarkdownToken] = []
        POGGER.debug(
            "block_quote_data.current_count>$>>block_quote_data.stack_count>>$<<",
            block_quote_data.current_count,
            block_quote_data.stack_count,
        )
        if block_quote_data.current_count == 0 and block_quote_data.stack_count > 0:
            POGGER.debug("haven't processed")

            POGGER.debug("xx:$", parser_state.token_stack)
            POGGER.debug("xx:$", parser_state.token_document)
            POGGER.debug("xx:$", parser_state.original_stack_depth)
            POGGER.debug("xx:$", position_marker.line_number)

            (
                was_paragraph_continuation,
                is_leaf_block_start,
            ) = BlockQuoteProcessor.__adjust_lazy_handling(
                parser_state,
                line_to_parse,
                extracted_whitespace,
                was_paragraph_continuation,
            )
            if (
                parser_state.token_stack[-1].is_code_block
                or parser_state.token_stack[-1].is_html_block
                or is_leaf_block_start
            ):
                POGGER.debug("__check_for_lazy_handling>>code block")
                container_level_tokens, _ = parser_state.close_open_blocks_fn(
                    parser_state,
                    only_these_blocks=[
                        BlockQuoteStackToken,
                        type(parser_state.token_stack[-1]),
                    ],
                    include_block_quotes=True,
                    was_forced=True,
                )
            stack_count = parser_state.count_of_block_quotes_on_stack()
            if stack_count != block_quote_data.stack_count:
                block_quote_data = BlockQuoteData(
                    block_quote_data.current_count, stack_count
                )
        return container_level_tokens, block_quote_data, was_paragraph_continuation

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_block_quote_block_really_start(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[
        Optional[RequeueLineInfo],
        bool,
        int,
        bool,
        List[MarkdownToken],
        List[MarkdownToken],
    ]:
        assert (
            grab_bag.container_start_bq_count is not None
        ), "If starting here, we need a block quote count."
        POGGER.debug("handle_block_quote_block>>block-start")
        POGGER.debug("original_line:>:$:<", grab_bag.original_line)
        POGGER.debug(
            "container_start_bq_count:>:$:<", grab_bag.container_start_bq_count
        )
        (
            adjusted_text_to_parse,
            adjusted_index_number,
            leaf_tokens,
            container_level_tokens,
            grab_bag.block_quote_data,
            grab_bag.removed_chars_at_start_of_line,
            grab_bag.did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            requeue_line_info,
            grab_bag.do_force_list_continuation,
        ) = BlockQuoteProcessor.__handle_block_quote_section(
            parser_state,
            position_marker,
            grab_bag.block_quote_data,
            extracted_whitespace,
            grab_bag.container_start_bq_count,
            grab_bag.original_line,
        )
        POGGER.debug("force_list_continuation=$", grab_bag.do_force_list_continuation)
        POGGER.debug("adjusted_index_number>>:$:", adjusted_index_number)
        POGGER.debug(">>avoid_block_starts>>$", avoid_block_starts)
        POGGER.debug(">>text_removed_by_container>>:$:", text_removed_by_container)

        (
            did_process,
            end_of_bquote_start_index,
        ) = BlockQuoteProcessor.__handle_block_quote_block_kludges(
            parser_state,
            grab_bag.block_quote_data,
            leaf_tokens,
            container_level_tokens,
            adjusted_text_to_parse,
            last_block_quote_index,
            adjusted_index_number,
        )
        grab_bag.start_index = adjusted_index_number
        grab_bag.line_to_parse = adjusted_text_to_parse
        grab_bag.text_removed_by_container = text_removed_by_container
        grab_bag.last_block_quote_index = last_block_quote_index
        return (
            requeue_line_info,
            did_process,
            end_of_bquote_start_index,
            avoid_block_starts,
            leaf_tokens,
            container_level_tokens,
        )

    @staticmethod
    def handle_block_quote_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[bool, int, List[MarkdownToken], List[MarkdownToken], bool]:
        """
        Handle the processing of a block quote block.
        """
        POGGER.debug("handle_block_quote_block>>start")
        extracted_whitespace: Optional[str] = grab_bag.extracted_whitespace
        assert (
            extracted_whitespace is not None
        ), "Extracted whitespace must be available at this point."
        adj_ws: Optional[str] = grab_bag.adj_ws

        (
            did_process,
            avoid_block_starts,
            end_of_bquote_start_index,
        ) = (
            False,
            False,
            -1,
        )
        grab_bag.do_force_list_continuation = False
        grab_bag.did_blank = False
        grab_bag.removed_chars_at_start_of_line = 0
        grab_bag.start_index = position_marker.index_number
        grab_bag.line_to_parse = position_marker.text_to_parse
        grab_bag.text_removed_by_container = None
        grab_bag.last_block_quote_index = 0

        leaf_tokens: List[MarkdownToken] = []
        container_level_tokens: List[MarkdownToken] = []

        POGGER.debug(
            "handle_block_quote_block>>was_link_definition_started>:$:<",
            parser_state.token_stack[-1].was_link_definition_started,
        )
        POGGER.debug(
            "text_to_parse[index=$:]>:$:<",
            position_marker.index_number,
            position_marker.text_to_parse[position_marker.index_number :],
        )
        really_start, requeue_line_info = BlockQuoteProcessor.__check_if_really_start(
            parser_state, position_marker, extracted_whitespace, adj_ws
        )

        if really_start:
            assert (
                not requeue_line_info
            ), "If we need to start, we should not be requeuing a line."
            (
                requeue_line_info,
                did_process,
                end_of_bquote_start_index,
                avoid_block_starts,
                leaf_tokens,
                container_level_tokens,
            ) = BlockQuoteProcessor.__handle_block_quote_block_really_start(
                parser_state, position_marker, extracted_whitespace, grab_bag
            )
        elif (
            parser_state.token_stack[-1].was_link_definition_started
            and not requeue_line_info
        ):
            BlockQuoteProcessor.__handle_block_quote_block_lrd_kludges(parser_state)

        POGGER.debug("handle_block_quote_block>>end>>did_process>>$", did_process)
        POGGER.debug("handle_block_quote_block>>end>>leaf_tokens>>$", leaf_tokens)
        POGGER.debug(
            "handle_block_quote_block>>end>>container_level_tokens>>$",
            container_level_tokens,
        )

        grab_bag.requeue_line_info = requeue_line_info

        return (
            did_process,
            end_of_bquote_start_index,
            leaf_tokens,
            container_level_tokens,
            avoid_block_starts,
        )

    @staticmethod
    def __handle_block_quote_block_lrd_kludges(parser_state: ParserState) -> None:
        stack_index = parser_state.find_last_block_quote_on_stack()
        if stack_index > 0:
            last_block_token = cast(
                BlockQuoteMarkdownToken,
                parser_state.token_stack[stack_index].matching_markdown_token,
            )
            POGGER.debug(
                "handle_block w/ no open>>found>>$",
                last_block_token,
            )
            POGGER.debug("hbqblk>>last_block_token>>$", last_block_token)
            POGGER.debug(
                "hbqblk>>leading_text_index>>$", last_block_token.leading_text_index
            )
            last_block_token.add_bleading_spaces("")
            POGGER.debug("hbqblk>>last_block_token>>$", last_block_token)
            POGGER.debug(
                "hbqblk>>leading_text_index>>$", last_block_token.leading_text_index
            )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_block_quote_block_kludges(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        leaf_tokens: List[MarkdownToken],
        container_level_tokens: List[MarkdownToken],
        adjusted_text_to_parse: str,
        last_block_quote_index: int,
        adjusted_index_number: int,
    ) -> Tuple[bool, int]:
        POGGER.debug(
            ">>block_quote_data.current_count>>$", block_quote_data.current_count
        )
        POGGER.debug(">>block_quote_data.stack_count>>$", block_quote_data.stack_count)
        if block_quote_data.current_count:
            POGGER.debug("token_stack>$", parser_state.token_stack)
            POGGER.debug("token_document>$", parser_state.token_document)
            POGGER.debug("leaf_tokens>$", leaf_tokens)
            POGGER.debug("container_level_tokens>$", container_level_tokens)
            POGGER.debug("adjusted_text_to_parse>$<", adjusted_text_to_parse)
            adjusted_current_count = block_quote_data.current_count + 1
            if adjusted_current_count < len(parser_state.token_stack):
                POGGER.debug(
                    "token_stack[x]>$", parser_state.token_stack[adjusted_current_count]
                )
                if parser_state.token_stack[
                    adjusted_current_count
                ].is_list and adjusted_text_to_parse.strip(Constants.ascii_whitespace):
                    POGGER.debug("\n\nBOOM\n\n")
                    parser_state.nested_list_start = cast(
                        ListStackToken, parser_state.token_stack[adjusted_current_count]
                    )

        did_process = last_block_quote_index != -1
        return did_process, adjusted_index_number if did_process else -1

    # pylint: enable=too-many-arguments

    @staticmethod
    def __check_if_really_start(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        adj_ws: Optional[str],
    ) -> Tuple[bool, Optional[RequeueLineInfo]]:
        POGGER.debug(
            "handle_block_quote_block>>text>:$:<", position_marker.text_to_parse
        )
        POGGER.debug(
            "handle_block_quote_block>>extracted_whitespace>:$:<",
            extracted_whitespace,
        )
        POGGER.debug("handle_block_quote_block>>adj_ws>:$:<", adj_ws)
        requeue_line_info = None

        last_stack_index = parser_state.find_last_list_block_on_stack()
        if (
            last_stack_index
            and len(extracted_whitespace) >= position_marker.index_number
        ):
            adj_ws = extracted_whitespace[position_marker.index_number - 1 :]
        POGGER.debug("handle_block_quote_block>>adj_ws>:$:<", adj_ws)
        really_start = BlockQuoteCountHelper.is_block_quote_start(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
            adj_ws=adj_ws,
        )
        if (
            really_start
            and parser_state.token_stack[-1].is_fenced_code_block
            and parser_state.token_stack[-2].is_list
        ):
            start_index = position_marker.index_number
            POGGER.debug("start_index>>$", start_index)
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[-2].matching_markdown_token,
            )
            POGGER.debug("list_token>>$", list_token)
            POGGER.debug("list_token.indent_level>>$", list_token.indent_level)
            really_start = start_index < list_token.indent_level
            POGGER.debug("really_start>>$", really_start)

        if really_start:
            POGGER.debug(
                "handle_block_quote_block>>token_stack[depth]>:$:<",
                parser_state.token_stack,
            )
            if parser_state.token_stack[-1].is_paragraph:
                (
                    really_start,
                    requeue_line_info,
                ) = BlockQuoteProcessor.__check_if_really_start_paragraph(
                    parser_state, position_marker
                )
        return really_start, requeue_line_info

    @staticmethod
    def __check_if_really_start_paragraph(
        parser_state: ParserState, position_marker: PositionMarker
    ) -> Tuple[bool, Optional[RequeueLineInfo]]:
        current_indent, eligible_stack, eligible_stack_index = (
            0,
            parser_state.token_stack[1:-1],
            0,
        )

        POGGER.debug("handle_block_quote_block>>eligible_stack>:$:<", eligible_stack)
        while eligible_stack_index < len(eligible_stack):
            if eligible_stack[eligible_stack_index].is_list:
                (
                    current_indent,
                    requeue_line_info,
                ) = BlockQuoteProcessor.__check_if_really_start_list(
                    parser_state, position_marker, eligible_stack, eligible_stack_index
                )
                if requeue_line_info:
                    return False, requeue_line_info
            else:
                assert eligible_stack[
                    eligible_stack_index
                ].is_block_quote, (
                    "If its not a list token, it must be a block quote token."
                )
                break  # pragma: no cover
            eligible_stack_index += 1
        POGGER.debug(
            "eligible_stack_index($) < len(eligible_stack)($)",
            eligible_stack_index,
            len(eligible_stack),
        )
        POGGER.debug("current_indent($)", current_indent)
        return True, None

    @staticmethod
    def __check_if_really_start_list(
        parser_state: ParserState,
        position_marker: PositionMarker,
        eligible_stack: List[StackToken],
        eligible_stack_index: int,
    ) -> Tuple[int, Optional[RequeueLineInfo]]:
        assert eligible_stack[
            eligible_stack_index
        ].is_list, "Stack for lists should always end with list tokens."
        list_token = cast(ListStackToken, eligible_stack[eligible_stack_index])
        current_indent = list_token.indent_level
        if current_indent <= position_marker.index_number:
            return current_indent, None
        POGGER.debug("BOOYAH")
        POGGER.debug("current_indent=$", current_indent)
        POGGER.debug("index_number=$", position_marker.index_number)
        POGGER.debug("eligible_stack=$", eligible_stack)
        POGGER.debug("eligible_stack_index=$", eligible_stack_index)

        while eligible_stack_index >= 0:
            assert eligible_stack[
                eligible_stack_index
            ].is_list, "Stack for lists should always end with list tokens."
            list_token = cast(ListStackToken, eligible_stack[eligible_stack_index])
            if list_token.indent_level <= position_marker.index_number:
                break
            eligible_stack_index -= 1
        POGGER.debug("eligible_stack_index=$", eligible_stack_index)
        root_index = (
            (parser_state.token_stack.index(eligible_stack[eligible_stack_index]) + 1)
            if eligible_stack_index >= 0
            else 0
        )
        POGGER.debug("root_index=$", root_index)
        (
            container_level_tokens,
            _,
        ) = parser_state.close_open_blocks_fn(
            parser_state,
            include_block_quotes=True,
            include_lists=True,
            until_this_index=root_index,
            was_forced=True,
        )
        parser_state.token_document.extend(container_level_tokens)
        return -1, RequeueLineInfo([position_marker.text_to_parse], False)

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_block_quote_section(
        parser_state: ParserState,
        position_marker: PositionMarker,
        block_quote_data: BlockQuoteData,
        extracted_whitespace: str,
        container_start_bq_count: int,
        original_line: str,
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
        Handle the processing of a section clearly identified as having block quotes.
        """
        leaf_tokens: List[MarkdownToken] = []
        container_level_tokens: List[MarkdownToken] = []

        POGGER.debug(
            "IN>__handle_block_quote_section---$<<<",
            position_marker.text_to_parse,
        )
        POGGER.debug(
            "IN>start_index---$<<<",
            position_marker.index_number,
        )

        POGGER.debug("block_quote_data.stack_count--$", block_quote_data.stack_count)
        POGGER.debug("token_stack[-1]--$", parser_state.token_stack[-1])
        POGGER.debug("token_stack--$", parser_state.token_stack)

        POGGER.debug(
            "__handle_block_quote_section---$--$--",
            position_marker.index_number,
            position_marker.text_to_parse,
        )

        (
            block_quote_data,
            start_index,
            line_to_parse,
            last_block_quote_index,
            avoid_block_starts,
        ) = BlockQuoteCountHelper.count_block_quote_starts(
            parser_state,
            position_marker.text_to_parse,
            position_marker.index_number,
            block_quote_data,
            parser_state.token_stack[-1].is_fenced_code_block,
            parser_state.token_stack[-1].is_html_block,
        )
        POGGER.debug(
            "block_quote_data>>:curr=$:stack=$:",
            block_quote_data.current_count,
            block_quote_data.stack_count,
        )
        POGGER.debug("start_index>>:$:", start_index)
        POGGER.debug("line_to_parse>>:$:", line_to_parse)
        POGGER.debug("last_block_quote_index>>:$:", last_block_quote_index)
        POGGER.debug(">>avoid_block_starts>>$", avoid_block_starts)

        POGGER.debug("token_stack--$", parser_state.token_stack)
        POGGER.debug(">>container_start_bq_count>>$", container_start_bq_count)
        POGGER.debug(">>original_start_index>>$", position_marker.index_number)

        if last_block_quote_index != -1:
            POGGER.debug("start_index>>:$:", start_index)
            return BlockQuoteProcessor.__handle_existing_block_quote(
                parser_state,
                block_quote_data,
                start_index,
                line_to_parse,
                extracted_whitespace,
                position_marker.index_number,
                container_start_bq_count,
                position_marker,
                leaf_tokens,
                container_level_tokens,
                original_line,
                last_block_quote_index,
                avoid_block_starts,
            )

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
            None,
            False,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_existing_block_quote_fenced_special(
        parser_state: ParserState, start_index: int, block_quote_data: BlockQuoteData
    ) -> Tuple[bool, int]:
        assert parser_state.original_line_to_parse is not None
        block_quote_character_count = ParserHelper.count_characters_in_text(
            parser_state.original_line_to_parse[:start_index], ">"
        )
        assert (
            block_quote_character_count <= block_quote_data.current_count
        ), "if not, overreach"
        count_block_quotes = 0
        find_token_index = 0
        for stack_token_index, stack_token in enumerate(
            parser_state.token_stack
        ):  # pragma: no cover
            if stack_token.is_block_quote:
                count_block_quotes += 1
                if count_block_quotes == block_quote_character_count:
                    find_token_index = stack_token_index
                    break
        assert find_token_index != len(
            parser_state.token_stack
        ), "should have completed before this"
        find_token_index += 1
        process_fenced_block = parser_state.token_stack[find_token_index].is_block_quote
        return process_fenced_block, find_token_index

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_existing_block_quote_fenced_special_part_two(
        parser_state: ParserState,
        stack_index: int,
        line_to_parse: str,
        start_index: int,
        block_quote_data: BlockQuoteData,
        leaf_tokens: List[MarkdownToken],
        container_level_tokens: List[MarkdownToken],
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
        # At this point, we have a "prefix", which may be partial, that has the
        # current_count of > characters, and ends with a list. If we are here,
        # we know that previous lines have had at least one more > character and
        # counted block quote.
        assert parser_state.token_stack[
            stack_index
        ].is_list, "If not bq, must be a list."
        while parser_state.token_stack[stack_index].is_list:
            stack_index += 1
        embedded_list_stack_token = cast(
            ListStackToken, parser_state.token_stack[stack_index - 1]
        )
        block_stack_token = parser_state.token_stack[stack_index]
        block_markdown_token = cast(
            BlockQuoteMarkdownToken, block_stack_token.matching_markdown_token
        )
        list_markdown_token = cast(
            ListStartMarkdownToken, embedded_list_stack_token.matching_markdown_token
        )
        assert parser_state.original_line_to_parse is not None
        character_after_list = parser_state.original_line_to_parse[
            start_index : embedded_list_stack_token.indent_level
        ].strip()
        assert not character_after_list
        assert block_quote_data.current_count + 1 == block_quote_data.stack_count
        sd = parser_state.original_line_to_parse[embedded_list_stack_token.indent_level]
        assert sd == ">"
        last_block_quote_index = embedded_list_stack_token.indent_level + 1
        character_after_block_quote = parser_state.original_line_to_parse[
            last_block_quote_index
        ]
        assert character_after_block_quote == " "
        last_block_quote_index += 1
        # character_after_block_quote = parser_state.original_line_to_parse[last_block_quote_index]

        text_removed_by_container = parser_state.original_line_to_parse[
            :last_block_quote_index
        ]
        block_markdown_token.add_bleading_spaces(text_removed_by_container)
        if block_markdown_token.weird_kludge_one:
            block_markdown_token.weird_kludge_one += 1
        else:
            block_markdown_token.weird_kludge_one = 1
        list_markdown_token.add_leading_spaces("")
        block_quote_data = BlockQuoteData(
            block_quote_data.current_count + 1, block_quote_data.stack_count
        )
        return (
            line_to_parse[last_block_quote_index:],
            last_block_quote_index,
            leaf_tokens,
            container_level_tokens,
            block_quote_data,
            0,
            False,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            None,
            False,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_existing_block_quote(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        start_index: int,
        line_to_parse: str,
        extracted_whitespace: str,
        original_start_index: int,
        container_start_bq_count: int,
        position_marker: PositionMarker,
        leaf_tokens: List[MarkdownToken],
        container_level_tokens: List[MarkdownToken],
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
        POGGER.debug(
            "__handle_block_quote_section---block_quote_data.current_count--$--$--$--",
            block_quote_data.current_count,
            start_index,
            line_to_parse,
        )
        POGGER.debug(
            "ORIG-->WS[$]--SI[$]--[$]",
            extracted_whitespace,
            original_start_index,
            parser_state.original_line_to_parse,
        )
        POGGER.debug("NOW -->SI[$]--[$]", start_index, line_to_parse)

        if container_start_bq_count:
            POGGER.debug(
                ">>block_quote_data.current_count>>$", block_quote_data.current_count
            )
            block_quote_data = BlockQuoteData(
                block_quote_data.current_count + container_start_bq_count,
                block_quote_data.stack_count,
            )

        process_fenced_block = parser_state.token_stack[-1].is_fenced_code_block
        if (
            process_fenced_block
            and block_quote_data.current_count < block_quote_data.stack_count
        ):
            process_fenced_block, stack_index = (
                BlockQuoteProcessor.__handle_existing_block_quote_fenced_special(
                    parser_state, start_index, block_quote_data
                )
            )
            if not process_fenced_block:
                return BlockQuoteProcessor.__handle_existing_block_quote_fenced_special_part_two(
                    parser_state,
                    stack_index,
                    line_to_parse,
                    start_index,
                    block_quote_data,
                    leaf_tokens,
                    container_level_tokens,
                    avoid_block_starts,
                )
        if not process_fenced_block:
            return BlockQuoteNonFencedHelper.handle_non_fenced_code_section(
                parser_state,
                block_quote_data,
                extracted_whitespace,
                position_marker,
                original_start_index,
                container_start_bq_count,
                line_to_parse,
                start_index,
                leaf_tokens,
                original_line,
                last_block_quote_index,
                avoid_block_starts,
            )

        (
            block_quote_data,
            line_to_parse,
            container_level_tokens,
            text_removed_by_container,
        ) = BlockQuoteProcessor.__handle_fenced_code_section(
            parser_state,
            block_quote_data,
            start_index,
            line_to_parse,
            container_level_tokens,
        )

        POGGER.debug(
            "OUT>__handle_block_quote_section---$<<<",
            line_to_parse,
        )
        POGGER.debug("force_list_continuation=false")
        POGGER.debug("start_index>>:$:", start_index)
        return (
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            block_quote_data,
            0,
            False,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            None,
            False,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __handle_fenced_code_section(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        start_index: int,
        line_to_parse: str,
        container_level_tokens: List[MarkdownToken],
    ) -> Tuple[BlockQuoteData, str, List[MarkdownToken], str]:
        POGGER.debug("handle_block_quote_section>>fenced")
        assert start_index >= 0, "Index must be valid."
        removed_text, line_to_parse = (
            line_to_parse[:start_index],
            line_to_parse[start_index:],
        )

        POGGER.debug("__hbqs>>removed_text>>$", removed_text)
        POGGER.debug("__hbqs>>line_to_parse>>$", line_to_parse)
        POGGER.debug(
            "__hbqs>>block_quote_data.current_count>>$", block_quote_data.current_count
        )
        POGGER.debug(
            "__hbqs>>block_quote_data.stack_count>>$", block_quote_data.stack_count
        )

        if block_quote_data.current_count < block_quote_data.stack_count:
            (
                container_level_tokens,
                _,
            ) = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[
                    FencedCodeBlockStackToken,
                ],
                was_forced=True,
            )
            block_quote_data = BlockQuoteCountHelper.decrease_stack_to_level(
                parser_state,
                block_quote_data.current_count,
                block_quote_data.stack_count,
                container_level_tokens,
            )

        stack_index = parser_state.find_last_block_quote_on_stack()
        found_bq_stack_token = parser_state.token_stack[stack_index]
        POGGER.debug(
            "found_bq_stack_token---$<<<",
            found_bq_stack_token,
        )
        found_bq_token = cast(
            BlockQuoteMarkdownToken, found_bq_stack_token.matching_markdown_token
        )
        POGGER.debug("hfcs>>last_block_token>>$", found_bq_token)
        POGGER.debug("hfcs>>leading_text_index>>$", found_bq_token.leading_text_index)
        found_bq_token.add_bleading_spaces(removed_text)
        found_bq_token.leading_text_index += 1
        POGGER.debug("hfcs>>last_block_token>>$", found_bq_token)
        POGGER.debug("hfcs>>leading_text_index>>$", found_bq_token.leading_text_index)
        text_removed_by_container = removed_text

        return (
            block_quote_data,
            line_to_parse,
            container_level_tokens,
            text_removed_by_container,
        )
