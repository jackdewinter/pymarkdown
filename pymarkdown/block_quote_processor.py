"""
Module to provide processing for the block quotes.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quote_data import BlockQuoteData
from pymarkdown.container_grab_bag import ContainerGrabBag
from pymarkdown.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ListStartMarkdownToken,
)
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.requeue_line_info import RequeueLineInfo
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    FencedCodeBlockStackToken,
    HtmlBlockStackToken,
    IndentedCodeBlockStackToken,
    LinkDefinitionStackToken,
    ListStackToken,
    ParagraphStackToken,
    StackToken,
)

# pylint: disable=too-many-lines

POGGER = ParserLogger(logging.getLogger(__name__))


class BlockQuoteProcessor:
    """
    Class to provide processing for the block quotes.
    """

    __block_quote_character = ">"

    @staticmethod
    def is_block_quote_start(
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        adj_ws: Optional[str] = None,
    ) -> bool:
        """
        Determine if we have the start of a block quote section.
        """

        assert extracted_whitespace is not None
        return ParserHelper.is_length_less_than_or_equal_to(
            extracted_whitespace if adj_ws is None else adj_ws, 3
        ) and ParserHelper.is_character_at_index(
            line_to_parse, start_index, BlockQuoteProcessor.__block_quote_character
        )

    @staticmethod
    def __adjust_lazy_handling(
        parser_state: ParserState,
        line_to_parse: str,
        extracted_whitespace: Optional[str],
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
                    exclude_thematic_break=False,
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
        extracted_whitespace: Optional[str],
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

    # pylint: disable=too-many-locals
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
        adj_ws: Optional[str] = grab_bag.adj_ws
        block_quote_data: BlockQuoteData = grab_bag.block_quote_data
        container_start_bq_count: Optional[int] = grab_bag.container_start_bq_count

        (
            did_process,
            avoid_block_starts,
            did_blank,
            removed_chars_at_start,
            last_block_quote_index,
            end_of_bquote_start_index,
            text_removed_by_container,
            requeue_line_info,
            adjusted_text_to_parse,
            adjusted_index_number,
            force_list_continuation,
        ) = (
            False,
            False,
            False,
            0,
            0,
            -1,
            None,
            None,
            position_marker.text_to_parse,
            position_marker.index_number,
            False,
        )
        leaf_tokens: List[MarkdownToken] = []
        container_level_tokens: List[MarkdownToken] = []

        POGGER.debug("adjusted_index_number>>:$:", adjusted_index_number)

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
            assert container_start_bq_count is not None
            POGGER.debug("handle_block_quote_block>>block-start")
            (
                adjusted_text_to_parse,
                adjusted_index_number,
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
            ) = BlockQuoteProcessor.__handle_block_quote_section(
                parser_state,
                position_marker,
                block_quote_data,
                extracted_whitespace,
                container_start_bq_count,
            )
            POGGER.debug("force_list_continuation=$", force_list_continuation)
            POGGER.debug("adjusted_index_number>>:$:", adjusted_index_number)
            POGGER.debug(">>avoid_block_starts>>$", avoid_block_starts)
            POGGER.debug(">>text_removed_by_container>>:$:", text_removed_by_container)

            (
                did_process,
                end_of_bquote_start_index,
            ) = BlockQuoteProcessor.__handle_block_quote_block_kludges(
                parser_state,
                block_quote_data,
                leaf_tokens,
                container_level_tokens,
                adjusted_text_to_parse,
                last_block_quote_index,
                adjusted_index_number,
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

        grab_bag.block_quote_data = block_quote_data
        grab_bag.removed_chars_at_start_of_line = removed_chars_at_start
        grab_bag.did_blank = did_blank
        grab_bag.last_block_quote_index = last_block_quote_index
        grab_bag.text_removed_by_container = text_removed_by_container
        grab_bag.requeue_line_info = requeue_line_info
        grab_bag.do_force_list_continuation = force_list_continuation
        grab_bag.start_index = adjusted_index_number
        grab_bag.line_to_parse = adjusted_text_to_parse

        return (
            did_process,
            end_of_bquote_start_index,
            leaf_tokens,
            container_level_tokens,
            avoid_block_starts,
        )

    # pylint: enable=too-many-locals

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
            last_block_token.add_leading_spaces("")
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
                if (
                    parser_state.token_stack[adjusted_current_count].is_list
                    and adjusted_text_to_parse.strip()
                ):
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
        extracted_whitespace: Optional[str],
        adj_ws: Optional[str],
    ) -> Tuple[bool, Optional[RequeueLineInfo]]:

        assert extracted_whitespace is not None
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
        really_start = BlockQuoteProcessor.is_block_quote_start(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
            adj_ws=adj_ws,
        )
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
                assert eligible_stack[eligible_stack_index].is_block_quote
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

        assert eligible_stack[eligible_stack_index].is_list
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
            assert eligible_stack[eligible_stack_index].is_list
            list_token = cast(ListStackToken, eligible_stack[eligible_stack_index])
            if not list_token.indent_level > position_marker.index_number:
                break
            eligible_stack_index -= 1
        POGGER.debug("eligible_stack_index=$", eligible_stack_index)
        if eligible_stack_index >= 0:
            root_index = (
                parser_state.token_stack.index(eligible_stack[eligible_stack_index]) + 1
            )
        else:
            root_index = 0
        POGGER.debug("root_index=$", root_index)
        (container_level_tokens, _,) = parser_state.close_open_blocks_fn(
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
    def __count_block_quote_starts(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        block_quote_data: BlockQuoteData,
        is_top_of_stack_fenced_code_block: bool,
        is_top_of_stack_is_html_block: bool,
    ) -> Tuple[BlockQuoteData, int, str, int, bool]:
        """
        Having detected a block quote character (">") on a line, continue to consume
        and count while the block quote pattern is there.
        """

        (last_block_quote_index, avoid_block_starts, adjusted_line,) = (
            -1,
            False,
            line_to_parse,
        )
        if block_quote_data.stack_count == 0 and is_top_of_stack_fenced_code_block:
            start_index -= 1
        else:
            osi, oltp, current_count = start_index, line_to_parse[:], 1
            start_index += 1

            POGGER.debug(
                "block_quote_data.stack_count--$--is_top_of_stack_fenced_code_block--$",
                block_quote_data.stack_count,
                is_top_of_stack_fenced_code_block,
            )

            last_block_quote_index = start_index
            while True:
                adjusted_line, start_index = BlockQuoteProcessor.__handle_bq_whitespace(
                    adjusted_line, start_index
                )

                (
                    continue_processing,
                    avoid_block_starts,
                    start_index,
                    adjusted_line,
                    last_block_quote_index,
                    current_count,
                ) = BlockQuoteProcessor.__should_continue_processing(
                    parser_state,
                    current_count,
                    block_quote_data.stack_count,
                    is_top_of_stack_is_html_block,
                    adjusted_line,
                    start_index,
                    osi,
                    oltp,
                    is_top_of_stack_fenced_code_block,
                    avoid_block_starts,
                    last_block_quote_index,
                )
                if not continue_processing:
                    break
                current_count += 1
                start_index += 1
                last_block_quote_index = start_index

            block_quote_data = BlockQuoteData(
                current_count, block_quote_data.stack_count
            )
            POGGER.debug(
                "__count_block_quote_starts--$--$--",
                start_index,
                adjusted_line,
            )
        return (
            block_quote_data,
            start_index,
            adjusted_line,
            last_block_quote_index,
            avoid_block_starts,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_bq_whitespace(adjusted_line: str, start_index: int) -> Tuple[str, int]:
        if ParserHelper.is_character_at_index_whitespace(adjusted_line, start_index):
            start_index += 1
        return adjusted_line, start_index

    # pylint: disable=too-many-arguments
    @staticmethod
    def __should_continue_processing(
        parser_state: ParserState,
        current_count: int,
        stack_count: int,
        is_top_of_stack_is_html_block: bool,
        adjusted_line: str,
        start_index: int,
        osi: int,
        oltp: str,
        is_top_of_stack_fenced_code_block: bool,
        avoid_block_starts: bool,
        last_block_quote_index: int,
    ) -> Tuple[bool, bool, int, str, int, int]:

        continue_processing = True
        POGGER.debug(
            "current_count--$--stack_count--$--is_top_of_stack_is_html_block--$",
            current_count,
            stack_count,
            is_top_of_stack_is_html_block,
        )
        if is_top_of_stack_is_html_block:
            if current_count == stack_count:
                POGGER.debug(
                    "block quote levels don't increase during html block, ignoring"
                )
                avoid_block_starts = ParserHelper.is_character_at_index(
                    adjusted_line,
                    start_index,
                    BlockQuoteProcessor.__block_quote_character,
                )
                POGGER.debug("avoid_block_starts=$", avoid_block_starts)
                continue_processing = False
            elif current_count > stack_count:
                (
                    start_index,
                    adjusted_line,
                    last_block_quote_index,
                    avoid_block_starts,
                    current_count,
                    continue_processing,
                ) = (
                    osi,
                    oltp,
                    -1,
                    True,
                    stack_count,
                    False,
                )

        if continue_processing:
            continue_processing = False
            if is_top_of_stack_fenced_code_block and (current_count >= stack_count):
                pass
            elif start_index == len(adjusted_line):
                POGGER.debug("ran out of line")
            elif ParserHelper.is_character_at_index_not(
                adjusted_line,
                start_index,
                BlockQuoteProcessor.__block_quote_character,
            ):
                (
                    continue_processing,
                    start_index,
                ) = BlockQuoteProcessor.__is_special_double_block_case(
                    parser_state, adjusted_line, start_index, current_count, stack_count
                )
            else:
                continue_processing = True
        return (
            continue_processing,
            avoid_block_starts,
            start_index,
            adjusted_line,
            last_block_quote_index,
            current_count,
        )

    # pylint: enable=too-many-arguments
    @staticmethod
    def __is_special_double_block_case(
        parser_state: ParserState,
        adjusted_line: str,
        start_index: int,
        current_count: int,
        stack_count: int,
    ) -> Tuple[bool, int]:
        continue_processing = False
        POGGER.debug("not block>$ of :$:", start_index, adjusted_line)
        POGGER.debug("not block>:$:", adjusted_line[start_index:])
        if current_count < stack_count:
            count_to_consume, stack_index, final_stack_index = current_count, 0, 0
            while not final_stack_index and stack_index < len(parser_state.token_stack):
                stack_token = parser_state.token_stack[stack_index]
                POGGER.debug("stack>:$:$:", stack_index, stack_token)
                if stack_token.is_block_quote:
                    count_to_consume -= 1
                    if not count_to_consume:
                        final_stack_index = stack_index
                stack_index += 1
            assert not count_to_consume
            assert final_stack_index
            POGGER.debug(
                ">>stack>:$:$:",
                final_stack_index,
                parser_state.token_stack[final_stack_index],
            )
            POGGER.debug(
                "+1>>stack>:$:$:",
                final_stack_index + 1,
                parser_state.token_stack[final_stack_index + 1],
            )
            if parser_state.token_stack[final_stack_index + 1].is_block_quote:
                next_bq_index = adjusted_line.find(
                    BlockQuoteProcessor.__block_quote_character, start_index
                )
                POGGER.debug("+1>>next_bq_index:$:", next_bq_index)
                if next_bq_index != -1 and (next_bq_index - start_index) <= 3:
                    continue_processing, start_index = True, next_bq_index
        return continue_processing, start_index

    # pylint: disable=too-many-locals
    @staticmethod
    def __handle_block_quote_section(
        parser_state: ParserState,
        position_marker: PositionMarker,
        block_quote_data: BlockQuoteData,
        extracted_whitespace: Optional[str],
        container_start_bq_count: int,
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
        ) = BlockQuoteProcessor.__count_block_quote_starts(
            parser_state,
            position_marker.text_to_parse,
            position_marker.index_number,
            block_quote_data,
            parser_state.token_stack[-1].is_fenced_code_block,
            parser_state.token_stack[-1].is_html_block,
        )
        POGGER.debug("start_index>>:$:", start_index)

        POGGER.debug("token_stack--$", parser_state.token_stack)
        POGGER.debug(">>container_start_bq_count>>$", container_start_bq_count)
        POGGER.debug(
            ">>block_quote_data.current_count>>$", block_quote_data.current_count
        )
        POGGER.debug(">>block_quote_data.stack_count>>$", block_quote_data.stack_count)
        POGGER.debug(">>start_index>>$", start_index)
        POGGER.debug(">>original_start_index>>$", position_marker.index_number)
        POGGER.debug(">>avoid_block_starts>>$", avoid_block_starts)

        if last_block_quote_index != -1:
            POGGER.debug("start_index>>:$:", start_index)
            (
                line_to_parse,
                start_index,
                leaf_tokens,
                container_level_tokens,
                block_quote_data,
                removed_chars_at_start,
                did_blank,
                text_removed_by_container,
                requeue_line_info,
                force_list_continuation,
            ) = BlockQuoteProcessor.__handle_existing_block_quote(
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
            )
            POGGER.debug("force_list_continuation=$", force_list_continuation)
            POGGER.debug("start_index>>:$:", start_index)
        else:
            (
                text_removed_by_container,
                did_blank,
                removed_chars_at_start,
                requeue_line_info,
                force_list_continuation,
            ) = (None, False, 0, None, False)

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

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_existing_block_quote(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        start_index: int,
        line_to_parse: str,
        extracted_whitespace: Optional[str],
        original_start_index: int,
        container_start_bq_count: int,
        position_marker: PositionMarker,
        leaf_tokens: List[MarkdownToken],
        container_level_tokens: List[MarkdownToken],
    ) -> Tuple[
        str,
        int,
        List[MarkdownToken],
        List[MarkdownToken],
        BlockQuoteData,
        int,
        bool,
        Optional[str],
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

        force_list_continuation = False
        if not parser_state.token_stack[-1].is_fenced_code_block:
            (
                container_level_tokens,
                requeue_line_info,
                line_to_parse,
                removed_chars_at_start,
                text_removed_by_container,
                did_blank,
                leaf_tokens,
                force_list_continuation,
            ) = BlockQuoteProcessor.__handle_non_fenced_code_section(
                parser_state,
                block_quote_data,
                extracted_whitespace,
                position_marker,
                original_start_index,
                container_start_bq_count,
                line_to_parse,
                start_index,
                leaf_tokens,
            )
            POGGER.debug("force_list_continuation=$", force_list_continuation)
        else:
            did_blank, requeue_line_info, removed_chars_at_start = False, None, 0
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
        return (
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            block_quote_data,
            removed_chars_at_start,
            did_blank,
            text_removed_by_container,
            requeue_line_info,
            force_list_continuation,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_non_fenced_code_section(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        extracted_whitespace: Optional[str],
        position_marker: PositionMarker,
        original_start_index: int,
        container_start_bq_count: int,
        line_to_parse: str,
        start_index: int,
        leaf_tokens: List[MarkdownToken],
    ) -> Tuple[
        List[MarkdownToken],
        Optional[RequeueLineInfo],
        str,
        int,
        Optional[str],
        bool,
        List[MarkdownToken],
        bool,
    ]:

        did_blank, removed_chars_at_start, text_removed_by_container = False, 0, None
        POGGER.debug("handle_block_quote_section>>not fenced")
        (
            container_level_tokens,
            requeue_line_info,
            extra_consumed_whitespace,
            force_list_continuation,
        ) = BlockQuoteProcessor.__ensure_stack_at_level(
            parser_state,
            block_quote_data,
            extracted_whitespace,
            position_marker,
            original_start_index,
            container_start_bq_count,
        )
        POGGER.debug("force_list_continuation=$", force_list_continuation)
        if not requeue_line_info:
            POGGER.debug("extracted_whitespace:$:", extracted_whitespace)
            POGGER.debug("line_to_parse:$:", line_to_parse)
            POGGER.debug("start_index:$:", start_index)
            POGGER.debug(
                "position_marker.index_number:$:", position_marker.index_number
            )
            POGGER.debug(
                "position_marker.index_indent:$:", position_marker.index_indent
            )
            removed_text = f"{extracted_whitespace}{line_to_parse[position_marker.index_number : start_index]}"
            POGGER.debug(
                "==EWS[$],OSI[$],SI[$],LTP[$],RT=[$]",
                extracted_whitespace,
                original_start_index,
                position_marker.index_number,
                position_marker.text_to_parse,
                removed_text,
            )
            (
                line_to_parse,
                removed_chars_at_start,
                stack_index,
                text_removed_by_container,
            ) = (
                line_to_parse[start_index:],
                start_index,
                parser_state.find_last_block_quote_on_stack(),
                removed_text,
            )
            POGGER.debug("==REM[$],LTP[$]", removed_text, line_to_parse)

            assert stack_index != -1
            found_bq_stack_token = cast(
                BlockQuoteStackToken, parser_state.token_stack[stack_index]
            )
            assert found_bq_stack_token

            BlockQuoteProcessor.__do_block_quote_leading_spaces_adjustments(
                parser_state,
                stack_index,
                container_start_bq_count,
                block_quote_data,
                text_removed_by_container,
                found_bq_stack_token,
                removed_text,
                original_start_index,
                extra_consumed_whitespace,
                container_level_tokens,
            )
            POGGER.debug("text_removed_by_container=[$]", text_removed_by_container)
            POGGER.debug("removed_text=[$]", removed_text)
            if not line_to_parse.strip():
                did_blank, leaf_tokens = BlockQuoteProcessor.__handle_normal_blank_line(
                    parser_state,
                    block_quote_data,
                    position_marker,
                    text_removed_by_container,
                    line_to_parse,
                )
        return (
            container_level_tokens,
            requeue_line_info,
            line_to_parse,
            removed_chars_at_start,
            text_removed_by_container,
            did_blank,
            leaf_tokens,
            force_list_continuation,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_1(
        parser_state: ParserState,
        container_start_bq_count: int,
        adjusted_removed_text: str,
        text_removed_by_container: str,
        stack_index: int,
        block_quote_data: BlockQuoteData,
    ) -> str:
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
            assert count_of_actual_starts != block_quote_data.current_count
            block_quote_token = cast(
                BlockQuoteMarkdownToken, block_stack_token.matching_markdown_token
            )
            adj_leading_spaces = block_quote_token.leading_spaces
            assert adj_leading_spaces is not None
            POGGER.debug("__hbqs>>count_of_actual_starts>>$", count_of_actual_starts)
            POGGER.debug("__hbqs>>adj_leading_spaces>>:$:<", adj_leading_spaces)
            POGGER.debug(
                "__hbqs>>text_removed_by_container>>:$:<",
                text_removed_by_container,
            )

            delta = len(text_removed_by_container) - len(
                adj_leading_spaces + adjusted_removed_text
            )
            adj_leading_spaces = adj_leading_spaces + ParserHelper.repeat_string(
                ParserHelper.space_character, delta
            )
            adjusted_removed_text = adj_leading_spaces + adjusted_removed_text
            POGGER.debug("__hbqs>>adjusted_removed_text>>:$:<", adjusted_removed_text)
        return adjusted_removed_text

    # pylint: enable=too-many-arguments

    @staticmethod
    def __find_original_token(
        parser_state: ParserState, found_bq_stack_token: StackToken
    ) -> Optional[MarkdownToken]:
        original_token = None
        for block_copy_token in parser_state.block_copy:
            if not block_copy_token:
                continue

            assert found_bq_stack_token.matching_markdown_token is not None

            if (
                found_bq_stack_token.matching_markdown_token.line_number
                == block_copy_token.line_number
                and found_bq_stack_token.matching_markdown_token.column_number
                == block_copy_token.column_number
            ):
                original_token = block_copy_token
                break
        return original_token

    @staticmethod
    def __adjust_2(
        parser_state: ParserState,
        found_bq_stack_token: StackToken,
        original_removed_text: str,
        adjusted_removed_text: str,
        extra_consumed_whitespace: Optional[int],
    ) -> Tuple[bool, str]:
        POGGER.debug("original_removed_text>>:$:", original_removed_text)
        POGGER.debug("extra_consumed_whitespace>>:$:", extra_consumed_whitespace)
        POGGER.debug("parser_state.block_copy>>$", parser_state.block_copy)
        special_case = False
        if parser_state.block_copy and found_bq_stack_token:

            POGGER.debug("parser_state.block_copy>>search")
            if original_token := BlockQuoteProcessor.__find_original_token(
                parser_state, found_bq_stack_token
            ):
                original_block_quote_token = cast(
                    BlockQuoteMarkdownToken, original_token
                )
                assert found_bq_stack_token.matching_markdown_token is not None
                POGGER.debug("original_token>>$", original_block_quote_token)
                assert original_block_quote_token.leading_spaces is not None
                POGGER.debug(
                    "original_token.leading_spaces>>:$:<<",
                    original_block_quote_token.leading_spaces,
                )
                block_quote_markdown_token = cast(
                    BlockQuoteMarkdownToken,
                    found_bq_stack_token.matching_markdown_token,
                )
                current_leading_spaces = block_quote_markdown_token.leading_spaces
                assert current_leading_spaces is not None
                POGGER.debug("found_bq_stack_token.ls>>:$:<<", current_leading_spaces)
                assert current_leading_spaces.startswith(
                    original_block_quote_token.leading_spaces
                )
                POGGER.debug("original_removed_text>>:$:", original_removed_text)
                POGGER.debug("adjusted_removed_text>>:$:", adjusted_removed_text)
                if len(current_leading_spaces) > len(
                    original_block_quote_token.leading_spaces
                ):
                    current_leading_spaces = current_leading_spaces[
                        len(original_block_quote_token.leading_spaces) :
                    ]
                    POGGER.debug("current_leading_spaces>>:$:", current_leading_spaces)
                    assert current_leading_spaces[0] == "\n"
                    current_leading_spaces = current_leading_spaces[1:]
                    POGGER.debug(
                        "current_leading_spaces>>:$:($)",
                        current_leading_spaces,
                        len(current_leading_spaces),
                    )
                    special_case = True
                    if not extra_consumed_whitespace:
                        extra_consumed_whitespace = 0
                    adjusted_removed_text = original_removed_text[
                        len(current_leading_spaces) - extra_consumed_whitespace :
                    ]
        return special_case, adjusted_removed_text

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
        extra_consumed_whitespace: Optional[int],
        container_level_tokens: List[MarkdownToken],
    ) -> None:

        POGGER.debug("__hbqs>>removed_text>>:$:<", removed_text)
        POGGER.debug("__hbqs>>container_start_bq_count>>$", container_start_bq_count)
        POGGER.debug("__hbqs>>original_start_index>>$", original_start_index)
        POGGER.debug("token_stack--$", parser_state.token_stack)
        original_start_index = BlockQuoteProcessor.__block_quote_start_adjust(
            parser_state, original_start_index, container_level_tokens
        )
        original_removed_text = removed_text
        adjusted_removed_text = (
            removed_text[original_start_index:]
            if container_start_bq_count and original_start_index
            else removed_text
        )

        POGGER.debug("dbqlsa>>adjusted_removed_text>>:$:<", adjusted_removed_text)
        adjusted_removed_text = BlockQuoteProcessor.__adjust_1(
            parser_state,
            container_start_bq_count,
            adjusted_removed_text,
            text_removed_by_container,
            stack_index,
            block_quote_data,
        )

        assert found_bq_stack_token.matching_markdown_token is not None
        block_quote_token = cast(
            BlockQuoteMarkdownToken, found_bq_stack_token.matching_markdown_token
        )

        POGGER.debug("__hbqs>>adjusted_removed_text>>:$:<", adjusted_removed_text)
        POGGER.debug("token_stack--$", parser_state.token_stack)
        POGGER.debug("dbqlsa>>found_bq_stack_token>>$", found_bq_stack_token)
        POGGER.debug("dbqlsa>>bq>>$", block_quote_token)

        POGGER.debug("dbqlsa>>adjusted_removed_text>>:$:<<", adjusted_removed_text)
        special_case, adjusted_removed_text = BlockQuoteProcessor.__adjust_2(
            parser_state,
            found_bq_stack_token,
            original_removed_text,
            adjusted_removed_text,
            extra_consumed_whitespace,
        )
        POGGER.debug("dbqlsa>>adjusted_removed_text>>:$:<<", adjusted_removed_text)
        POGGER.debug("dbqlsa>>special_case>>$", special_case)

        POGGER.debug("dbqlsa>>last_block_token>>$", block_quote_token)
        POGGER.debug(
            "dbqlsa>>leading_text_index>>$", block_quote_token.leading_text_index
        )
        block_quote_token.add_leading_spaces(adjusted_removed_text, special_case)
        block_quote_token.leading_text_index += 1
        POGGER.debug("dbqlsa>>last_block_token>>$", block_quote_token)
        POGGER.debug(
            "dbqlsa>>leading_text_index>>$", block_quote_token.leading_text_index
        )

        POGGER.debug("__hbqs>>bq>>$", block_quote_token)

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_normal_blank_line(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        position_marker: PositionMarker,
        text_removed_by_container: str,
        line_to_parse: str,
    ) -> Tuple[bool, List[MarkdownToken]]:
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
        POGGER.debug("handle_block_quote_section>>leaf_tokens>>$", leaf_tokens)
        assert not (requeue_line_info and requeue_line_info.lines_to_requeue)

        # KLUDGE!
        if (
            len(parser_state.token_stack) == 3
            and parser_state.token_stack[1].is_list
            and parser_state.token_stack[2].is_block_quote
        ):
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[1].matching_markdown_token,
            )
            list_token.add_leading_spaces("")

        return True, leaf_tokens

    @staticmethod
    def __handle_fenced_code_section(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        start_index: int,
        line_to_parse: str,
        container_level_tokens: List[MarkdownToken],
    ) -> Tuple[BlockQuoteData, str, List[MarkdownToken], str]:

        POGGER.debug("handle_block_quote_section>>fenced")
        assert start_index >= 0
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
            (container_level_tokens, _,) = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[
                    FencedCodeBlockStackToken,
                ],
                was_forced=True,
            )
            block_quote_data = BlockQuoteProcessor.__decrease_stack_to_level(
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
        found_bq_token.add_leading_spaces(removed_text)
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

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_eligible_stack_hard_limit(
        parser_state: ParserState,
        current_stack_index: int,
        indent_text_count: int,
        length_of_available_whitespace: int,
        extra_consumed_whitespace: int,
        adjust_current_block_quote: bool,
        last_bq_index: int,
    ) -> Tuple[int, int, int, int]:

        assert parser_state.token_stack[current_stack_index].is_list
        list_stack_token = cast(
            ListStackToken, parser_state.token_stack[current_stack_index]
        )
        POGGER.debug(
            "indent_level:$:indent_text_count:$:",
            list_stack_token.indent_level,
            indent_text_count,
        )
        delta = list_stack_token.indent_level - indent_text_count
        POGGER.debug(
            "delta:$:length_of_available_whitespace:$:",
            delta,
            length_of_available_whitespace,
        )
        assert length_of_available_whitespace >= delta
        list_token = cast(
            ListStartMarkdownToken, list_stack_token.matching_markdown_token
        )
        adjust_for_extra_indent = list_token.indent_level - list_token.column_number - 1
        if list_stack_token.is_ordered_list:
            adjust_for_extra_indent -= len(list_token.list_start_sequence) - 1
        POGGER.debug("adjust_for_extra_indent:$:", adjust_for_extra_indent)
        current_stack_index += 1
        delta -= adjust_for_extra_indent
        indent_text_count += delta
        length_of_available_whitespace -= delta
        extra_consumed_whitespace += delta
        if adjust_current_block_quote:
            POGGER.debug(
                "__calculate_stack_hard_limit>>last_block_token>>$",
                parser_state.token_stack[last_bq_index].matching_markdown_token,
            )
            block_token = cast(
                BlockQuoteMarkdownToken,
                parser_state.token_stack[last_bq_index].matching_markdown_token,
            )
            block_token.add_leading_spaces(
                ParserHelper.repeat_string(ParserHelper.space_character, delta), True
            )
            POGGER.debug(
                "__calculate_stack_hard_limit>>last_block_token>>$", block_token
            )

        return (
            current_stack_index,
            indent_text_count,
            length_of_available_whitespace,
            extra_consumed_whitespace,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __calculate_stack_hard_limit_if_eligible(
        parser_state: ParserState,
        position_marker: PositionMarker,
        length_of_available_whitespace: int,
        adjust_current_block_quote: bool,
        last_bq_index: int,
    ) -> Tuple[Optional[int], Optional[int]]:
        POGGER.debug("eligible")
        stack_hard_limit, extra_consumed_whitespace = None, None
        assert parser_state.original_line_to_parse is not None
        if remaining_text := parser_state.original_line_to_parse[
            : -len(position_marker.text_to_parse)
        ]:
            POGGER.debug("eligible - remaining_text:$:", remaining_text)

            # use up already extracted text/ws
            current_stack_index, indent_text_count, extra_consumed_whitespace = 1, 0, 0
            assert parser_state.token_stack[current_stack_index].is_block_quote
            POGGER.debug("bq")
            start_index = remaining_text.find(">")
            assert start_index != -1
            POGGER.debug("bq-found")
            indent_text_count = start_index + 1
            assert (
                indent_text_count < len(remaining_text)
                and remaining_text[indent_text_count] == ParserHelper.space_character
            )
            POGGER.debug("bq-space-found")
            indent_text_count += 1
            current_stack_index += 1
            assert indent_text_count == len(remaining_text)

            # if there is whitespace
            (
                stack_hard_limit,
                indent_text_count,
                length_of_available_whitespace,
                extra_consumed_whitespace,
            ) = BlockQuoteProcessor.__calculate_eligible_stack_hard_limit(
                parser_state,
                current_stack_index,
                indent_text_count,
                length_of_available_whitespace,
                extra_consumed_whitespace,
                adjust_current_block_quote,
                last_bq_index,
            )
        return stack_hard_limit, extra_consumed_whitespace

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_stack_hard_limit(
        parser_state: ParserState,
        position_marker: PositionMarker,
        adjust_current_block_quote: bool,
        stack_increase_needed: bool,
        stack_decrease_needed: bool,
        block_quote_data: BlockQuoteData,
    ) -> Tuple[Optional[int], Optional[int], bool]:
        POGGER.debug(">>__calculate_stack_hard_limit>>")
        POGGER.debug("original_line_to_parse>>:$:", parser_state.original_line_to_parse)
        POGGER.debug(
            "position_marker>>[$:$]:$:",
            position_marker.index_indent,
            position_marker.index_number,
            position_marker.text_to_parse,
        )

        (
            length_of_available_whitespace,
            _,
        ) = ParserHelper.extract_spaces(position_marker.text_to_parse, 0)
        POGGER.debug("len(ws)>>:$:", length_of_available_whitespace)

        stack_hard_limit, extra_consumed_whitespace, last_bq_index = (
            None,
            None,
            parser_state.find_last_block_quote_on_stack(),
        )

        # TODO need to find a better way, stopgap
        assert parser_state.original_line_to_parse is not None
        conditional_1 = parser_state.original_line_to_parse.endswith(
            position_marker.text_to_parse
        )
        POGGER.debug(
            "conditional_1:$: = oltp:$:endswith(ttp:$:)",
            conditional_1,
            parser_state.original_line_to_parse,
            position_marker.text_to_parse,
        )
        conditional_2 = (
            len(parser_state.token_stack) > 2
            and parser_state.token_stack[1].is_block_quote
        )
        POGGER.debug(
            "conditional_2:$: = len(ts:$:) > 2 and ts[1].is_bq:$:",
            conditional_2,
            parser_state.token_stack,
            parser_state.token_stack[1].is_block_quote
            if len(parser_state.token_stack) > 2
            else None,
        )
        conditional_3 = last_bq_index != 1 or stack_increase_needed
        POGGER.debug(
            "conditional_3:$: = lbl:$: != 1 or stack_increase_needed:$:",
            conditional_3,
            last_bq_index,
            stack_increase_needed,
        )
        POGGER.debug(
            "conditional_1>>:$ and ty2:$: and ty3:$:",
            conditional_1,
            conditional_2,
            conditional_3,
        )
        force_list_continuation = False
        if conditional_1 and conditional_2 and conditional_3:
            assert length_of_available_whitespace is not None
            (
                stack_hard_limit,
                extra_consumed_whitespace,
            ) = BlockQuoteProcessor.__calculate_stack_hard_limit_if_eligible(
                parser_state,
                position_marker,
                length_of_available_whitespace,
                adjust_current_block_quote,
                last_bq_index,
            )
            if extra_consumed_whitespace is None:
                POGGER.debug(f">>>>>stack_increase_needed:{stack_increase_needed}")
                POGGER.debug(f">>>>>stack_decrease_needed:{stack_decrease_needed}")
                POGGER.debug(
                    f">>>>>adjust_current_block_quote:{adjust_current_block_quote}"
                )
                POGGER.debug(
                    ">>block_quote_data.current_count>>$",
                    block_quote_data.current_count,
                )
                POGGER.debug(
                    ">>block_quote_data.stack_count>>$", block_quote_data.stack_count
                )

                if (
                    not stack_increase_needed
                    and not stack_decrease_needed
                    and adjust_current_block_quote
                ):
                    POGGER.debug(f">>>>>last_bq_index:{last_bq_index}")
                    POGGER.debug(
                        f">>>>>parser_state.token_stack:{parser_state.token_stack}"
                    )
                    POGGER.debug(
                        f">>>>>len(parser_state.token_stack):{len(parser_state.token_stack)}"
                    )
                    force_list_continuation = (
                        last_bq_index + 1 < len(parser_state.token_stack)
                        and parser_state.token_stack[last_bq_index + 1].is_list
                        and block_quote_data.current_count
                        != block_quote_data.stack_count
                    )
        POGGER.debug(
            "<<__calculate_stack_hard_limit<<$,$",
            stack_hard_limit,
            extra_consumed_whitespace,
        )
        POGGER.debug("force_list_continuation=$", force_list_continuation)
        return stack_hard_limit, extra_consumed_whitespace, force_list_continuation

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __ensure_stack_at_level(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        extracted_whitespace: Optional[str],
        position_marker: PositionMarker,
        original_start_index: int,
        container_start_bq_count: int,
    ) -> Tuple[List[MarkdownToken], Optional[RequeueLineInfo], Optional[int], bool]:
        """
        Ensure that the block quote stack is at the proper level on the stack.
        """
        container_level_tokens: List[MarkdownToken] = []
        (
            stack_increase_needed,
            stack_decrease_needed,
        ) = BlockQuoteProcessor.__does_require_increase_or_descrease(
            parser_state, block_quote_data
        )

        POGGER.debug(
            "stack_increase_needed>>$, stack_decrease_needed=$",
            stack_increase_needed,
            stack_decrease_needed,
        )
        if stack_increase_needed or stack_decrease_needed:
            POGGER.debug(
                "token_stack>>$",
                parser_state.token_stack,
            )
            POGGER.debug("token_document>>$", parser_state.token_document)
            (
                container_level_tokens,
                requeue_line_info,
            ) = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[
                    ParagraphStackToken,
                    IndentedCodeBlockStackToken,
                    LinkDefinitionStackToken,
                    HtmlBlockStackToken,
                ],
                was_forced=True,
                caller_can_handle_requeue=True,
                requeue_reset=True,
            )
            if requeue_line_info:
                return [], requeue_line_info, None, False

            POGGER.debug("esal>>__calculate_stack_hard_limit(delta)")
            (
                stack_hard_limit,
                extra_consumed_whitespace,
                force_list_continuation,
            ) = BlockQuoteProcessor.__calculate_stack_hard_limit(
                parser_state,
                position_marker,
                False,
                stack_increase_needed,
                stack_decrease_needed,
                block_quote_data,
            )
            POGGER.debug("force_list_continuation=$", force_list_continuation)
            POGGER.debug("esal>>__calculate_stack_hard_limit>>$", stack_hard_limit)

            BlockQuoteProcessor.__decrease_stack(
                parser_state,
                container_level_tokens,
                original_start_index,
                stack_hard_limit,
            )

            (
                extracted_whitespace,
                original_start_index,
            ) = BlockQuoteProcessor.__increase_stack(
                parser_state,
                container_level_tokens,
                block_quote_data,
                position_marker,
                original_start_index,
                container_start_bq_count,
                extracted_whitespace,
            )
        else:
            POGGER.debug("esal>>__calculate_stack_hard_limit(no delta)")
            (
                stack_hard_limit,
                extra_consumed_whitespace,
                force_list_continuation,
            ) = BlockQuoteProcessor.__calculate_stack_hard_limit(
                parser_state, position_marker, True, False, False, block_quote_data
            )
            POGGER.debug("esal>>__calculate_stack_hard_limit>>$", stack_hard_limit)

        return (
            container_level_tokens,
            None,
            extra_consumed_whitespace,
            force_list_continuation,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __does_require_increase_or_descrease(
        parser_state: ParserState, block_quote_data: BlockQuoteData
    ) -> Tuple[bool, bool]:
        POGGER.debug(
            "__ensure_stack_at_level>>block_quote_data.current_count>>$>>block_quote_data.stack_count>>$",
            block_quote_data.current_count,
            block_quote_data.stack_count,
        )
        stack_increase_needed = (
            block_quote_data.current_count > block_quote_data.stack_count
        )
        if (
            not stack_increase_needed
            and block_quote_data.current_count < block_quote_data.stack_count
        ):
            POGGER.debug(
                "__ensure_stack_at_level>>possible decrease to new level",
            )
            top_token_on_stack = parser_state.token_stack[-1]
            POGGER.debug("__ensure_stack_at_level>>$", top_token_on_stack)
            stack_decrease_needed = (
                top_token_on_stack.is_indented_code_block
                or top_token_on_stack.is_html_block
                or top_token_on_stack.is_list
                or top_token_on_stack.is_block_quote
            )
            POGGER.debug(
                "__ensure_stack_at_level>>decrease to new level=$",
                stack_decrease_needed,
            )
        else:
            stack_decrease_needed = False
        return stack_increase_needed, stack_decrease_needed

    @staticmethod
    def __decrease_stack(
        parser_state: ParserState,
        container_level_tokens: List[MarkdownToken],
        original_start_index: int,
        stack_hard_limit: Optional[int],
    ) -> None:
        POGGER.debug("token_stack>>$", parser_state.token_stack)
        POGGER.debug("token_document>>$", parser_state.token_document)
        POGGER.debug(
            "container_level_tokens>>$",
            container_level_tokens,
        )
        POGGER.debug("stack_hard_limit>>$", stack_hard_limit)
        stack_conditional = stack_hard_limit is None or (
            len(parser_state.token_stack) > stack_hard_limit
        )
        POGGER.debug("stack_conditional>>$", stack_conditional)
        while stack_conditional and parser_state.token_stack[-1].is_list:
            list_stack_token = cast(ListStackToken, parser_state.token_stack[-1])
            POGGER.debug("stack>>$", list_stack_token.indent_level)
            POGGER.debug("original_start_index>>$", original_start_index)
            if original_start_index < list_stack_token.indent_level:
                close_tokens, _ = parser_state.close_open_blocks_fn(
                    parser_state,
                    include_lists=True,
                    was_forced=True,
                    until_this_index=len(parser_state.token_stack) - 1,
                )
                container_level_tokens.extend(close_tokens)
                POGGER.debug("container_level_tokens>>$", container_level_tokens)
            else:
                break  # pragma: no cover

    @staticmethod
    def __block_list_block_kludge(
        parser_state: ParserState,
        position_marker: PositionMarker,
        stack_count: int,
        block_quote_data: BlockQuoteData,
    ) -> bool:
        POGGER.debug("original_line_to_parse>>$", parser_state.original_line_to_parse)
        POGGER.debug("text_to_parse>>$", position_marker.text_to_parse)
        POGGER.debug("index_number>>$", position_marker.index_number)
        POGGER.debug("index_indent>>$", position_marker.index_indent)

        POGGER.debug("stack_count>>$", stack_count)
        POGGER.debug("block_quote_data.stack_count>>$", block_quote_data.stack_count)
        POGGER.debug(
            "block_quote_data.current_count>>$", block_quote_data.current_count
        )

        # KLUDGE!
        skip = False
        if (
            parser_state.original_line_to_parse == position_marker.text_to_parse
            and not position_marker.index_indent
        ):
            last_active_block_quote_stack_index = position_marker.text_to_parse[
                : position_marker.index_number + 1
            ].count(">")
            POGGER.debug(
                "last_active_block_quote_stack_index>>$",
                last_active_block_quote_stack_index,
            )

            text_after_current_block_quote = position_marker.text_to_parse[
                position_marker.index_number + 1 :
            ]
            found_index = next(
                (
                    char_index
                    for char_index, current_char in enumerate(
                        text_after_current_block_quote
                    )
                    if current_char not in " >"
                ),
                -1,
            )
            POGGER.debug("found_index:$", found_index)
            assert found_index < len(text_after_current_block_quote)
            whitespace_after_block_quote = text_after_current_block_quote[:found_index]
            text_after_block_quote = text_after_current_block_quote[found_index:]
            POGGER.debug(
                "whitespace_after_block_quote:$: + text_after_block_quote:$:",
                whitespace_after_block_quote,
                text_after_block_quote,
            )

            POGGER.debug("token_stack>>$", parser_state.token_stack)
            POGGER.debug(
                "token_stack[last_active_block_quote_stack_index]>>$",
                parser_state.token_stack[last_active_block_quote_stack_index],
            )
            stack_index_valid = last_active_block_quote_stack_index + 1 < len(
                parser_state.token_stack
            )
            stack_index_in_scope = last_active_block_quote_stack_index < stack_count
            more_block_quotes_present = ">" in whitespace_after_block_quote
            POGGER.debug(
                "stack_index_valid:$ and stack_index_in_scope:$ and more_block_quotes_present:$",
                stack_index_valid,
                stack_index_in_scope,
                more_block_quotes_present,
            )
            if stack_index_valid and stack_index_in_scope and more_block_quotes_present:
                POGGER.debug(
                    "xy>>$",
                    parser_state.token_stack[last_active_block_quote_stack_index + 1],
                )
                skip = parser_state.token_stack[
                    last_active_block_quote_stack_index + 1
                ].is_list
        return skip

    # pylint: disable=too-many-arguments
    @staticmethod
    def __increase_stack(
        parser_state: ParserState,
        container_level_tokens: List[MarkdownToken],
        block_quote_data: BlockQuoteData,
        position_marker: PositionMarker,
        original_start_index: int,
        container_start_bq_count: int,
        extracted_whitespace: Optional[str],
    ) -> Tuple[Optional[str], int]:
        POGGER.debug("container_level_tokens>>$", container_level_tokens)
        assert extracted_whitespace is not None
        stack_count = block_quote_data.stack_count
        while block_quote_data.current_count > stack_count:
            POGGER.debug(
                "increasing block quotes by one>>",
            )
            stack_count += 1

            adjusted_position_marker = PositionMarker(
                position_marker.line_number,
                original_start_index,
                position_marker.text_to_parse,
            )

            if container_start_bq_count:
                POGGER.debug("extracted_whitespace>>$<<", extracted_whitespace)
                POGGER.debug("container_start_bq_count>>$<<", container_start_bq_count)
                POGGER.debug("original_start_index>>$<<", original_start_index)
                extracted_whitespace = extracted_whitespace[original_start_index:]
                POGGER.debug("extracted_whitespace>>$<<", extracted_whitespace)

            assert (
                position_marker.text_to_parse[original_start_index]
                == BlockQuoteProcessor.__block_quote_character
            )
            original_start_index += 1
            if ParserHelper.is_character_at_index_whitespace(
                position_marker.text_to_parse, original_start_index
            ):
                original_start_index += 1

            new_markdown_token = BlockQuoteMarkdownToken(
                extracted_whitespace, adjusted_position_marker
            )

            container_level_tokens.append(new_markdown_token)
            parser_state.token_stack.append(BlockQuoteStackToken(new_markdown_token))

        POGGER.debug("container_level_tokens>>$", container_level_tokens)
        skip = BlockQuoteProcessor.__block_list_block_kludge(
            parser_state,
            position_marker,
            stack_count,
            block_quote_data,
        )
        if not skip:
            BlockQuoteProcessor.__decrease_stack_to_level(
                parser_state,
                block_quote_data.current_count,
                stack_count,
                container_level_tokens,
            )
        POGGER.debug(
            "container_level_tokens>>$",
            container_level_tokens,
        )

        return extracted_whitespace, original_start_index

    # pylint: enable=too-many-arguments

    @staticmethod
    def __decrease_stack_to_level(
        parser_state: ParserState,
        current_count: int,
        stack_count: int,
        container_level_tokens: List[MarkdownToken],
    ) -> BlockQuoteData:
        while current_count < stack_count:
            POGGER.debug(
                "decreasing block quotes by one>>",
            )
            stack_count -= 1
            (new_tokens, _,) = parser_state.close_open_blocks_fn(
                parser_state,
                include_block_quotes=True,
                until_this_index=len(parser_state.token_stack) - 1,
                was_forced=True,
            )
            container_level_tokens.extend(new_tokens)
        return BlockQuoteData(current_count, stack_count)
