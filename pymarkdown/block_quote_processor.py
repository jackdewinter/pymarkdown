"""
Module to provide processing for the block quotes.
"""
import logging

from pymarkdown.block_quote_data import BlockQuoteData
from pymarkdown.container_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.position_marker import PositionMarker
from pymarkdown.requeue_line_info import RequeueLineInfo
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    FencedCodeBlockStackToken,
    HtmlBlockStackToken,
    IndentedCodeBlockStackToken,
    LinkDefinitionStackToken,
    ParagraphStackToken,
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
        line_to_parse, start_index, extracted_whitespace, adj_ws=None
    ):
        """
        Determine if we have the start of a block quote section.
        """

        return ParserHelper.is_length_less_than_or_equal_to(
            extracted_whitespace if adj_ws is None else adj_ws, 3
        ) and ParserHelper.is_character_at_index(
            line_to_parse, start_index, BlockQuoteProcessor.__block_quote_character
        )

    @staticmethod
    def check_for_lazy_handling(
        parser_state,
        block_quote_data,
        line_to_parse,
        extracted_whitespace,
    ):
        """
        Check if there is any processing to be handled during the handling of
        lazy continuation lines in block quotes.
        """
        POGGER.debug("__check_for_lazy_handling")
        container_level_tokens = []
        POGGER.debug(
            "block_quote_data.current_count>$>>block_quote_data.stack_count>>$<<",
            block_quote_data.current_count,
            block_quote_data.stack_count,
        )
        if block_quote_data.current_count == 0 and block_quote_data.stack_count > 0:
            POGGER.debug("haven't processed")

            is_leaf_block_start = (
                LeafBlockProcessor.is_paragraph_ending_leaf_block_start(
                    parser_state,
                    line_to_parse,
                    0,
                    extracted_whitespace,
                    exclude_thematic_break=True,
                )
            )

            if (
                parser_state.token_stack[-1].is_code_block
                or parser_state.token_stack[-1].is_html_block
                or is_leaf_block_start
            ):
                POGGER.debug("__check_for_lazy_handling>>code block")
                assert not container_level_tokens
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
        return container_level_tokens, block_quote_data

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def handle_block_quote_block(
        parser_state,
        position_marker,
        extracted_whitespace,
        adj_ws,
        block_quote_data,
        container_start_bq_count,
    ):
        """
        Handle the processing of a block quote block.
        """
        POGGER.debug("handle_block_quote_block>>start")

        (
            did_process,
            avoid_block_starts,
            did_blank,
            removed_chars_at_start,
            last_block_quote_index,
            end_of_bquote_start_index,
            text_removed_by_container,
            requeue_line_info,
            leaf_tokens,
            container_level_tokens,
            adjusted_text_to_parse,
            adjusted_index_number,
        ) = (
            False,
            False,
            False,
            0,
            0,
            -1,
            None,
            None,
            [],
            [],
            position_marker.text_to_parse,
            position_marker.index_number,
        )

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
            ) = BlockQuoteProcessor.__handle_block_quote_section(
                parser_state,
                position_marker,
                block_quote_data,
                extracted_whitespace,
                container_start_bq_count,
            )
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

        return (
            did_process,
            end_of_bquote_start_index,
            block_quote_data,
            adjusted_text_to_parse,
            adjusted_index_number,
            leaf_tokens,
            container_level_tokens,
            removed_chars_at_start,
            did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            requeue_line_info,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __handle_block_quote_block_lrd_kludges(parser_state):
        stack_index = parser_state.find_last_block_quote_on_stack()
        if stack_index > 0:
            last_block_token = parser_state.token_stack[
                stack_index
            ].matching_markdown_token
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
        parser_state,
        block_quote_data,
        leaf_tokens,
        container_level_tokens,
        adjusted_text_to_parse,
        last_block_quote_index,
        adjusted_index_number,
    ):
        adjusted_current_count = block_quote_data.current_count + 1
        POGGER.debug(
            ">>block_quote_data.current_count>>$", block_quote_data.current_count
        )
        if block_quote_data.current_count:
            POGGER.debug("token_stack>$", parser_state.token_stack)
            POGGER.debug("token_document>$", parser_state.token_document)
            POGGER.debug("leaf_tokens>$", leaf_tokens)
            POGGER.debug("container_level_tokens>$", container_level_tokens)
            POGGER.debug("adjusted_text_to_parse>$<", adjusted_text_to_parse)
            if adjusted_current_count < len(parser_state.token_stack):
                POGGER.debug(
                    "token_stack[x]>$", parser_state.token_stack[adjusted_current_count]
                )
                if (
                    parser_state.token_stack[adjusted_current_count].is_list
                    and adjusted_text_to_parse.strip()
                ):
                    POGGER.debug("\n\nBOOM\n\n")
                    parser_state.nested_list_start = parser_state.token_stack[
                        adjusted_current_count
                    ]

        did_process = last_block_quote_index != -1
        return did_process, adjusted_index_number if did_process else -1

    # pylint: enable=too-many-arguments

    @staticmethod
    def __check_if_really_start(
        parser_state, position_marker, extracted_whitespace, adj_ws
    ):
        POGGER.debug(
            "handle_block_quote_block>>text>:$:<", position_marker.text_to_parse
        )
        POGGER.debug(
            "handle_block_quote_block>>extracted_whitespace>:$:<",
            extracted_whitespace,
        )
        POGGER.debug("handle_block_quote_block>>adj_ws>:$:<", adj_ws)
        really_start, requeue_line_info = False, None

        search_index = len(parser_state.token_stack) - 1
        found_list_token = None
        while search_index > 0:
            if parser_state.token_stack[search_index].is_list:
                found_list_token = parser_state.token_stack[search_index]
                break
            search_index -= 1

        if (
            found_list_token
            and len(extracted_whitespace) >= position_marker.index_number
        ):
            adj_ws = extracted_whitespace[position_marker.index_number - 1 :]
        POGGER.debug("handle_block_quote_block>>adj_ws>:$:<", adj_ws)
        if BlockQuoteProcessor.is_block_quote_start(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
            adj_ws=adj_ws,
        ):
            really_start = True
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
    def __check_if_really_start_paragraph(parser_state, position_marker):

        current_indent, eligible_stack, eligible_stack_index, continue_matching = (
            0,
            parser_state.token_stack[1:-1],
            0,
            True,
        )

        POGGER.debug("handle_block_quote_block>>eligible_stack>:$:<", eligible_stack)
        while continue_matching and eligible_stack_index < len(eligible_stack):
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
                continue_matching = False
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
        parser_state, position_marker, eligible_stack, eligible_stack_index
    ):
        current_indent, requeue_line_info = (
            eligible_stack[eligible_stack_index].indent_level,
            None,
        )
        if current_indent > position_marker.index_number:
            POGGER.debug("BOOYAH")
            (container_level_tokens, _,) = parser_state.close_open_blocks_fn(
                parser_state,
                include_block_quotes=True,
                include_lists=eligible_stack_index + 1,
                until_this_index=-1,
                was_forced=True,
            )
            parser_state.token_document.extend(container_level_tokens)
            requeue_line_info = RequeueLineInfo([position_marker.text_to_parse], False)
        return current_indent, requeue_line_info

    @staticmethod
    def __count_block_quote_starts(
        line_to_parse,
        start_index,
        block_quote_data,
        is_top_of_stack_fenced_code_block,
        is_top_of_stack_is_html_block,
    ):
        """
        Having detected a block quote character (">") on a line, continue to consume
        and count while the block quote pattern is there.
        """

        (osi, oltp, last_block_quote_index, avoid_block_starts, adjusted_line,) = (
            start_index,
            line_to_parse[:],
            -1,
            False,
            line_to_parse,
        )
        if block_quote_data.stack_count == 0 and is_top_of_stack_fenced_code_block:
            start_index -= 1
        else:
            current_count = 1
            start_index += 1
            last_block_quote_index = start_index

            POGGER.debug(
                "block_quote_data.stack_count--$--is_top_of_stack_fenced_code_block--$",
                block_quote_data.stack_count,
                is_top_of_stack_fenced_code_block,
            )

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

    @staticmethod
    def __handle_bq_whitespace(adjusted_line, start_index):
        if ParserHelper.is_character_at_index_whitespace(adjusted_line, start_index):
            assert adjusted_line[start_index] != ParserHelper.tab_character
            start_index += 1
        return adjusted_line, start_index

    # pylint: disable=too-many-arguments
    @staticmethod
    def __should_continue_processing(
        current_count,
        stack_count,
        is_top_of_stack_is_html_block,
        adjusted_line,
        start_index,
        osi,
        oltp,
        is_top_of_stack_fenced_code_block,
        avoid_block_starts,
        last_block_quote_index,
    ):

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
                start_index, adjusted_line, last_block_quote_index = (
                    osi,
                    oltp,
                    -1,
                )
                avoid_block_starts, current_count = True, stack_count
                continue_processing = False

        if continue_processing:
            if is_top_of_stack_fenced_code_block and (current_count >= stack_count):
                continue_processing = False
            elif start_index == len(adjusted_line):
                POGGER.debug("ran out of line")
                continue_processing = False
            elif ParserHelper.is_character_at_index_not(
                adjusted_line,
                start_index,
                BlockQuoteProcessor.__block_quote_character,
            ):
                POGGER.debug("not block>$ of :$:", start_index, adjusted_line)
                continue_processing = False
        return (
            continue_processing,
            avoid_block_starts,
            start_index,
            adjusted_line,
            last_block_quote_index,
            current_count,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals
    @staticmethod
    def __handle_block_quote_section(
        parser_state,
        position_marker,
        block_quote_data,
        extracted_whitespace,
        container_start_bq_count,
    ):
        """
        Handle the processing of a section clearly identified as having block quotes.
        """
        (
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            original_start_index,
            text_removed_by_container,
            did_blank,
            removed_chars_at_start,
            requeue_line_info,
        ) = (
            position_marker.text_to_parse,
            position_marker.index_number,
            [],
            [],
            position_marker.index_number,
            None,
            False,
            0,
            None,
        )

        POGGER.debug(
            "IN>__handle_block_quote_section---$<<<",
            line_to_parse,
        )
        POGGER.debug(
            "IN>start_index---$<<<",
            start_index,
        )

        POGGER.debug("block_quote_data.stack_count--$", block_quote_data.stack_count)
        POGGER.debug("token_stack[-1]--$", parser_state.token_stack[-1])
        POGGER.debug("token_stack--$", parser_state.token_stack)

        POGGER.debug(
            "__handle_block_quote_section---$--$--",
            start_index,
            line_to_parse,
        )

        (
            block_quote_data,
            start_index,
            line_to_parse,
            last_block_quote_index,
            avoid_block_starts,
        ) = BlockQuoteProcessor.__count_block_quote_starts(
            line_to_parse,
            start_index,
            block_quote_data,
            parser_state.token_stack[-1].is_fenced_code_block,
            parser_state.token_stack[-1].is_html_block,
        )

        POGGER.debug("token_stack--$", parser_state.token_stack)
        POGGER.debug(">>container_start_bq_count>>$", container_start_bq_count)
        POGGER.debug(
            ">>block_quote_data.current_count>>$", block_quote_data.current_count
        )
        POGGER.debug(">>block_quote_data.stack_count>>$", block_quote_data.stack_count)
        POGGER.debug(">>start_index>>$", start_index)
        POGGER.debug(">>original_start_index>>$", original_start_index)
        POGGER.debug(">>avoid_block_starts>>$", avoid_block_starts)

        if last_block_quote_index == -1:
            POGGER.debug("BAIL")
        else:
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
            ) = BlockQuoteProcessor.__handle_existing_block_quote(
                parser_state,
                block_quote_data,
                start_index,
                line_to_parse,
                extracted_whitespace,
                original_start_index,
                container_start_bq_count,
                position_marker,
                leaf_tokens,
                container_level_tokens,
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
        )

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_existing_block_quote(
        parser_state,
        block_quote_data,
        start_index,
        line_to_parse,
        extracted_whitespace,
        original_start_index,
        container_start_bq_count,
        position_marker,
        leaf_tokens,
        container_level_tokens,
    ):
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

        (
            did_blank,
            requeue_line_info,
            removed_chars_at_start,
            text_removed_by_container,
        ) = (False, None, 0, None)

        if not parser_state.token_stack[-1].is_fenced_code_block:
            (
                container_level_tokens,
                requeue_line_info,
                line_to_parse,
                removed_chars_at_start,
                text_removed_by_container,
                did_blank,
                leaf_tokens,
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
        else:
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
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_non_fenced_code_section(
        parser_state,
        block_quote_data,
        extracted_whitespace,
        position_marker,
        original_start_index,
        container_start_bq_count,
        line_to_parse,
        start_index,
        leaf_tokens,
    ):
        did_blank, removed_chars_at_start, text_removed_by_container = False, 0, None
        POGGER.debug("handle_block_quote_section>>not fenced")
        (
            container_level_tokens,
            requeue_line_info,
        ) = BlockQuoteProcessor.__ensure_stack_at_level(
            parser_state,
            block_quote_data,
            extracted_whitespace,
            position_marker,
            original_start_index,
            container_start_bq_count,
        )
        if not requeue_line_info:
            POGGER.debug("token_stack--$", parser_state.token_stack)
            (
                special_case,
                special_case_adjusted_text,
            ) = BlockQuoteProcessor.__check_for_special_case(
                parser_state, container_start_bq_count, block_quote_data
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
            line_to_parse, removed_chars_at_start = (
                line_to_parse[start_index:],
                start_index,
            )
            POGGER.debug("==REM[$],LTP[$]", removed_text, line_to_parse)

            stack_index, text_removed_by_container = (
                parser_state.find_last_block_quote_on_stack(),
                removed_text,
            )
            assert stack_index != -1
            found_bq_stack_token = parser_state.token_stack[stack_index]
            assert found_bq_stack_token

            BlockQuoteProcessor.__do_block_quote_leading_spaces_adjustments(
                parser_state,
                stack_index,
                container_start_bq_count,
                block_quote_data,
                text_removed_by_container,
                special_case,
                special_case_adjusted_text,
                found_bq_stack_token,
                removed_text,
                original_start_index,
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
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __check_for_special_case(
        parser_state, container_start_bq_count, block_quote_data
    ):
        special_case, special_case_adjusted_text = False, None
        if (
            container_start_bq_count
            and block_quote_data.stack_count > 1
            and container_start_bq_count != block_quote_data.stack_count
        ):

            stack_index, block_quote_token_count = 1, 0
            while True:
                assert parser_state.token_stack[stack_index].is_block_quote
                block_quote_token_count += 1
                if block_quote_token_count == block_quote_data.stack_count:
                    break
                stack_index += 1
                assert stack_index < len(parser_state.token_stack)
            assert stack_index < len(parser_state.token_stack)
            matching_block_quote_token = parser_state.token_stack[
                stack_index
            ].matching_markdown_token
            POGGER.debug("matching_block_quote_token=:$:", matching_block_quote_token)

            assert (
                ParserHelper.newline_character
                in matching_block_quote_token.leading_spaces
            )
            last_newline_index = matching_block_quote_token.leading_spaces.rindex(
                ParserHelper.newline_character
            )
            special_case, special_case_adjusted_text = (
                True,
                matching_block_quote_token.leading_spaces[last_newline_index + 1 :],
            )
        return special_case, special_case_adjusted_text

    # pylint: disable=too-many-arguments
    @staticmethod
    def __do_block_quote_leading_spaces_adjustments(
        parser_state,
        stack_index,
        container_start_bq_count,
        block_quote_data,
        text_removed_by_container,
        special_case,
        special_case_adjusted_text,
        found_bq_stack_token,
        removed_text,
        original_start_index,
    ):

        POGGER.debug("__hbqs>>removed_text>>:$:<", removed_text)
        POGGER.debug("__hbqs>>container_start_bq_count>>$", container_start_bq_count)
        POGGER.debug("__hbqs>>original_start_index>>$", original_start_index)
        POGGER.debug("token_stack--$", parser_state.token_stack)
        adjusted_removed_text = (
            removed_text[original_start_index:]
            if container_start_bq_count and original_start_index
            else removed_text
        )

        if (
            container_start_bq_count
            and parser_state.token_stack[stack_index - 1].is_block_quote
        ):
            count_of_actual_starts = ParserHelper.count_characters_in_text(
                adjusted_removed_text, ">"
            )
            assert count_of_actual_starts != block_quote_data.current_count
            adj_leading_spaces = parser_state.token_stack[
                stack_index - 1
            ].matching_markdown_token.leading_spaces
            POGGER.debug("__hbqs>>count_of_actual_starts>>$", count_of_actual_starts)
            POGGER.debug("__hbqs>>adj_leading_spaces>>:$:<", adj_leading_spaces)
            POGGER.debug(
                "__hbqs>>len(text_removed_by_container)>>:$:<",
                len(text_removed_by_container),
            )
            while len(text_removed_by_container) > len(
                adj_leading_spaces + adjusted_removed_text
            ):
                adj_leading_spaces += " "
            adjusted_removed_text = adj_leading_spaces + adjusted_removed_text
            POGGER.debug("__hbqs>>adjusted_removed_text>>:$:<", adjusted_removed_text)
        POGGER.debug("__hbqs>>adjusted_removed_text>>:$:<", adjusted_removed_text)
        if special_case:
            POGGER.debug(
                "__hbqs>>special_case_adjusted_text>>:$:<",
                special_case_adjusted_text,
            )
            adjusted_removed_text = adjusted_removed_text[
                len(special_case_adjusted_text) :
            ]
            POGGER.debug("__hbqs>>adjusted_removed_text>>:$:<", adjusted_removed_text)
        POGGER.debug("token_stack--$", parser_state.token_stack)
        POGGER.debug("__hbqs>>found_bq_stack_token>>$", found_bq_stack_token)
        POGGER.debug("__hbqs>>bq>>$", found_bq_stack_token.matching_markdown_token)

        POGGER.debug(
            "dbqlsa>>last_block_token>>$", found_bq_stack_token.matching_markdown_token
        )
        POGGER.debug(
            "dbqlsa>>leading_text_index>>$",
            found_bq_stack_token.matching_markdown_token.leading_text_index,
        )
        found_bq_stack_token.matching_markdown_token.add_leading_spaces(
            adjusted_removed_text, special_case
        )
        found_bq_stack_token.matching_markdown_token.leading_text_index += 1
        POGGER.debug(
            "dbqlsa>>last_block_token>>$", found_bq_stack_token.matching_markdown_token
        )
        POGGER.debug(
            "dbqlsa>>leading_text_index>>$",
            found_bq_stack_token.matching_markdown_token.leading_text_index,
        )

        POGGER.debug("__hbqs>>bq>>$", found_bq_stack_token.matching_markdown_token)

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_normal_blank_line(
        parser_state,
        block_quote_data,
        position_marker,
        text_removed_by_container,
        line_to_parse,
    ):
        POGGER.debug("call __handle_block_quote_section>>handle_blank_line")

        POGGER.debug(
            "__hbqs>>block_quote_data.current_count>>$", block_quote_data.current_count
        )

        POGGER.debug("__hbqs>>token_stack>>$", parser_state.token_stack)
        possible_list_start_index = block_quote_data.current_count + 1
        if (
            possible_list_start_index < len(parser_state.token_stack)
            and parser_state.token_stack[possible_list_start_index].is_list
        ):
            POGGER.debug(
                "__hbqs>>fgg>>$<<",
                parser_state.token_stack[possible_list_start_index],
            )

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

        return True, leaf_tokens

    @staticmethod
    def __handle_fenced_code_section(
        parser_state,
        block_quote_data,
        start_index,
        line_to_parse,
        container_level_tokens,
    ):
        POGGER.debug("handle_block_quote_section>>fenced")
        assert start_index >= 0
        text_removed_by_container = None
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
        POGGER.debug(
            "hfcs>>last_block_token>>$", found_bq_stack_token.matching_markdown_token
        )
        POGGER.debug(
            "hfcs>>leading_text_index>>$",
            found_bq_stack_token.matching_markdown_token.leading_text_index,
        )
        found_bq_stack_token.matching_markdown_token.add_leading_spaces(removed_text)
        found_bq_stack_token.matching_markdown_token.leading_text_index += 1
        POGGER.debug(
            "hfcs>>last_block_token>>$", found_bq_stack_token.matching_markdown_token
        )
        POGGER.debug(
            "hfcs>>leading_text_index>>$",
            found_bq_stack_token.matching_markdown_token.leading_text_index,
        )
        text_removed_by_container = removed_text

        return (
            block_quote_data,
            line_to_parse,
            container_level_tokens,
            text_removed_by_container,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __ensure_stack_at_level(
        parser_state,
        block_quote_data,
        extracted_whitespace,
        position_marker,
        original_start_index,
        container_start_bq_count,
    ):
        """
        Ensure that the block quote stack is at the proper level on the stack.
        """
        container_level_tokens, stack_increase_needed, stack_decrease_needed = (
            [],
            False,
            False,
        )
        (
            stack_increase_needed,
            stack_decrease_needed,
        ) = BlockQuoteProcessor.__does_require_increase_or_descrease(
            parser_state, block_quote_data
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
                return None, requeue_line_info

            BlockQuoteProcessor.__decrease_stack(
                parser_state, container_level_tokens, original_start_index
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

        return container_level_tokens, None

    # pylint: enable=too-many-arguments

    @staticmethod
    def __does_require_increase_or_descrease(parser_state, block_quote_data):
        stack_increase_needed, stack_decrease_needed = False, False
        POGGER.debug(
            "__ensure_stack_at_level>>block_quote_data.current_count>>$>>block_quote_data.stack_count>>$",
            block_quote_data.current_count,
            block_quote_data.stack_count,
        )
        if block_quote_data.current_count > block_quote_data.stack_count:
            POGGER.debug(
                "__ensure_stack_at_level>>increase to new level",
            )
            stack_increase_needed = True
        elif block_quote_data.current_count < block_quote_data.stack_count:
            POGGER.debug(
                "__ensure_stack_at_level>>possible decrease to new level",
            )
            top_token_on_stack = parser_state.token_stack[-1]
            POGGER.debug("__ensure_stack_at_level>>$", top_token_on_stack)
            stack_decrease_needed = (
                top_token_on_stack.is_indented_code_block
                or top_token_on_stack.is_html_block
            )
            POGGER.debug(
                "__ensure_stack_at_level>>decrease to new level=$",
                stack_decrease_needed,
            )
        return stack_increase_needed, stack_decrease_needed

    @staticmethod
    def __decrease_stack(parser_state, container_level_tokens, original_start_index):
        POGGER.debug("token_stack>>$", parser_state.token_stack)
        POGGER.debug("token_document>>$", parser_state.token_document)
        POGGER.debug(
            "container_level_tokens>>$",
            container_level_tokens,
        )
        keep_going = True
        while keep_going and parser_state.token_stack[-1].is_list:
            POGGER.debug("stack>>$", parser_state.token_stack[-1].indent_level)
            POGGER.debug("original_start_index>>$", original_start_index)

            if original_start_index < parser_state.token_stack[-1].indent_level:
                close_tokens, _ = parser_state.close_open_blocks_fn(
                    parser_state,
                    include_lists=True,
                    was_forced=True,
                    until_this_index=len(parser_state.token_stack) - 1,
                )
                container_level_tokens.extend(close_tokens)
                POGGER.debug("container_level_tokens>>$", container_level_tokens)
            else:
                keep_going = False

    # pylint: disable=too-many-arguments
    @staticmethod
    def __increase_stack(
        parser_state,
        container_level_tokens,
        block_quote_data,
        position_marker,
        original_start_index,
        container_start_bq_count,
        extracted_whitespace,
    ):
        POGGER.debug("container_level_tokens>>$", container_level_tokens)
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
        parser_state, current_count, stack_count, container_level_tokens
    ):
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
