"""
Module to provide processing for the block quotes.
"""
import logging

from pymarkdown.container_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.parser_helper import ParserHelper, PositionMarker
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    FencedCodeBlockStackToken,
    HtmlBlockStackToken,
    IndentedCodeBlockStackToken,
    LinkDefinitionStackToken,
    ParagraphStackToken,
)

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

        if adj_ws is None:
            adj_ws = extracted_whitespace

        return ParserHelper.is_length_less_than_or_equal_to(
            adj_ws, 3
        ) and ParserHelper.is_character_at_index(
            line_to_parse, start_index, BlockQuoteProcessor.__block_quote_character
        )

    @staticmethod
    def check_for_lazy_handling(
        parser_state,
        this_bq_count,
        stack_bq_count,
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
            "this_bq_count>$>>stack_bq_count>>$<<",
            this_bq_count,
            stack_bq_count,
        )
        if this_bq_count == 0 and stack_bq_count > 0:
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
            else:
                POGGER.debug("__check_for_lazy_handling>>not code block")
                POGGER.debug("__check_for_lazy_handling>>$", parser_state.token_stack)

        return container_level_tokens

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    @staticmethod
    def handle_block_quote_block(
        parser_state,
        position_marker,
        extracted_whitespace,
        adj_ws,
        this_bq_count,
        stack_bq_count,
    ):
        """
        Handle the processing of a block quote block.
        """
        POGGER.debug("handle_block_quote_block>>start")

        did_process = False
        was_container_start = False
        avoid_block_starts = False
        did_blank = False
        text_removed_by_container = None
        end_of_bquote_start_index = -1
        leaf_tokens = []
        container_level_tokens = []
        removed_chars_at_start = 0
        last_block_quote_index = 0

        requeue_line_info = None

        adjusted_text_to_parse = position_marker.text_to_parse
        adjusted_index_number = position_marker.index_number

        POGGER.debug(
            "handle_block_quote_block>>text>:$:<", position_marker.text_to_parse
        )
        POGGER.debug(
            "handle_block_quote_block>>extracted_whitespace>:$:<",
            extracted_whitespace,
        )
        POGGER.debug("handle_block_quote_block>>adj_ws>:$:<", adj_ws)
        POGGER.debug(
            "handle_block_quote_block>>was_link_definition_started>:$:<",
            parser_state.token_stack[-1].was_link_definition_started,
        )
        if BlockQuoteProcessor.is_block_quote_start(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
            adj_ws=adj_ws,
        ):
            POGGER.debug("handle_block_quote_block>>block-start")
            (
                adjusted_text_to_parse,
                adjusted_index_number,
                leaf_tokens,
                container_level_tokens,
                stack_bq_count,
                alt_this_bq_count,
                removed_chars_at_start,
                did_blank,
                last_block_quote_index,
                text_removed_by_container,
                avoid_block_starts,
                requeue_line_info,
            ) = BlockQuoteProcessor.__handle_block_quote_section(
                parser_state,
                position_marker,
                stack_bq_count,
                extracted_whitespace,
            )
            POGGER.debug(">>avoid_block_starts>>$", avoid_block_starts)

            # TODO for nesting, may need to augment with this_bq_count already set.
            if this_bq_count == 0:
                this_bq_count = alt_this_bq_count
            else:
                POGGER.debug(">>>>>>>>>>>>>>>$>>>$", this_bq_count, alt_this_bq_count)
                this_bq_count = alt_this_bq_count

            if last_block_quote_index != -1:
                did_process = True
                was_container_start = True
                end_of_bquote_start_index = adjusted_index_number
            else:
                did_process = False
                was_container_start = False
                end_of_bquote_start_index = -1
        elif parser_state.token_stack[-1].was_link_definition_started:
            stack_index = parser_state.find_last_block_quote_on_stack()
            if stack_index > 0:
                last_block_token = parser_state.token_stack[
                    stack_index
                ].matching_markdown_token
                POGGER.debug(
                    "handle_block w/ no open>>found>>$",
                    last_block_token,
                )
                last_block_token.add_leading_spaces("")
            else:
                POGGER.debug("handle_block w/ no open>>not found")

        POGGER.debug("handle_block_quote_block>>end>>did_process>>$", did_process)
        return (
            did_process,
            was_container_start,
            end_of_bquote_start_index,
            this_bq_count,
            stack_bq_count,
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

    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-locals

    @staticmethod
    def __count_block_quote_starts(
        line_to_parse,
        start_index,
        stack_bq_count,
        is_top_of_stack_fenced_code_block,
        is_top_of_stack_is_html_block,
    ):
        """
        Having detected a block quote character (">") on a line, continue to consume
        and count while the block quote pattern is there.
        """

        osi = start_index
        oltp = line_to_parse

        this_bq_count = 0
        last_block_quote_index = -1
        avoid_block_starts = False
        adjusted_line = line_to_parse
        if stack_bq_count == 0 and is_top_of_stack_fenced_code_block:
            start_index -= 1
        else:
            this_bq_count += 1
            start_index += 1
            last_block_quote_index = start_index

            POGGER.debug(
                "stack_bq_count--$--is_top_of_stack_fenced_code_block--$",
                stack_bq_count,
                is_top_of_stack_fenced_code_block,
            )

            while True:
                if ParserHelper.is_character_at_index_whitespace(
                    adjusted_line, start_index
                ):
                    if adjusted_line[start_index] == ParserHelper.tab_character:
                        adjusted_tab_length = ParserHelper.calculate_length(
                            ParserHelper.tab_character, start_index=start_index
                        )
                        POGGER.debug("adj--$--", adjusted_line)
                        adjusted_line = (
                            adjusted_line[0:start_index]
                            + ParserHelper.repeat_string(
                                ParserHelper.space_character, adjusted_tab_length
                            )
                            + adjusted_line[start_index + 1 :]
                        )
                        POGGER.debug("--$--", adjusted_line)
                    start_index += 1

                POGGER.debug(
                    "this_bq_count--$--stack_bq_count--$--is_top_of_stack_is_html_block--$",
                    this_bq_count,
                    stack_bq_count,
                    is_top_of_stack_is_html_block,
                )
                if is_top_of_stack_is_html_block:
                    if this_bq_count == stack_bq_count:
                        POGGER.debug(
                            "block quote levels don't increase during html block, ignoring"
                        )
                        avoid_block_starts = ParserHelper.is_character_at_index(
                            adjusted_line,
                            start_index,
                            BlockQuoteProcessor.__block_quote_character,
                        )
                        POGGER.debug("avoid_block_starts=$", avoid_block_starts)
                        break
                    if this_bq_count > stack_bq_count:
                        start_index = osi
                        adjusted_line = oltp
                        last_block_quote_index = -1
                        avoid_block_starts = True
                        this_bq_count = stack_bq_count
                        break

                if is_top_of_stack_fenced_code_block and (
                    this_bq_count >= stack_bq_count
                ):
                    break

                if start_index == len(
                    adjusted_line
                ) or ParserHelper.is_character_at_index_not(
                    adjusted_line,
                    start_index,
                    BlockQuoteProcessor.__block_quote_character,
                ):
                    break
                this_bq_count += 1
                start_index += 1
                last_block_quote_index = start_index

            POGGER.debug(
                "__count_block_quote_starts--$--$--",
                start_index,
                adjusted_line,
            )
        return (
            this_bq_count,
            start_index,
            adjusted_line,
            last_block_quote_index,
            avoid_block_starts,
        )

    # pylint: disable=too-many-locals, too-many-statements
    @staticmethod
    def __handle_block_quote_section(
        parser_state,
        position_marker,
        stack_bq_count,
        extracted_whitespace,
    ):
        """
        Handle the processing of a section clearly identified as having block quotes.
        """
        # TODO work on removing these
        line_to_parse = position_marker.text_to_parse
        start_index = position_marker.index_number

        text_removed_by_container = None

        POGGER.debug(
            "IN>__handle_block_quote_section---$<<<",
            line_to_parse,
        )
        POGGER.debug("stack_bq_count--$", stack_bq_count)
        POGGER.debug("token_stack[-1]--$", parser_state.token_stack[-1])

        did_blank = False
        leaf_tokens = []
        container_level_tokens = []
        removed_chars_at_start = 0

        POGGER.debug(
            "__handle_block_quote_section---$--$--",
            start_index,
            line_to_parse,
        )
        original_start_index = start_index
        (
            this_bq_count,
            start_index,
            line_to_parse,
            last_block_quote_index,
            avoid_block_starts,
        ) = BlockQuoteProcessor.__count_block_quote_starts(
            line_to_parse,
            start_index,
            stack_bq_count,
            parser_state.token_stack[-1].is_fenced_code_block,
            parser_state.token_stack[-1].is_html_block,
        )
        POGGER.debug(">>start_index>>$", start_index)
        POGGER.debug(">>original_start_index>>$", original_start_index)
        if last_block_quote_index == -1:
            POGGER.debug("BAIL")
            return (
                line_to_parse,
                start_index,
                leaf_tokens,
                container_level_tokens,
                stack_bq_count,
                this_bq_count,
                removed_chars_at_start,
                did_blank,
                last_block_quote_index,
                text_removed_by_container,
                avoid_block_starts,
                None,
            )

        POGGER.debug(">>avoid_block_starts>>$", avoid_block_starts)
        POGGER.debug(
            "__handle_block_quote_section---this_bq_count--$--$--$--",
            this_bq_count,
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

        if not parser_state.token_stack[-1].is_fenced_code_block:
            POGGER.debug("handle_block_quote_section>>not fenced")
            (
                container_level_tokens,
                stack_bq_count,
                requeue_line_info,
            ) = BlockQuoteProcessor.__ensure_stack_at_level(
                parser_state,
                this_bq_count,
                stack_bq_count,
                extracted_whitespace,
                position_marker,
                original_start_index,
            )
            if requeue_line_info:
                return (
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    requeue_line_info,
                )

            removed_text = (
                extracted_whitespace
                + line_to_parse[position_marker.index_number : start_index]
            )
            POGGER.debug(
                "==EWS[$],OSI[$],SI[$],LTP[$]",
                extracted_whitespace,
                original_start_index,
                position_marker.index_number,
                position_marker.text_to_parse,
            )
            line_to_parse = line_to_parse[start_index:]
            removed_chars_at_start = start_index
            POGGER.debug("==REM[$],LTP[$]", removed_text, line_to_parse)

            stack_index = parser_state.find_last_block_quote_on_stack()
            assert stack_index != -1
            found_bq_stack_token = parser_state.token_stack[stack_index]
            found_bq_stack_token.matching_markdown_token.add_leading_spaces(
                removed_text
            )
            text_removed_by_container = removed_text

            if not line_to_parse.strip():
                POGGER.debug("call __handle_block_quote_section>>handle_blank_line")

                POGGER.debug("__hbqs>>this_bq_count>>$", this_bq_count)
                POGGER.debug("__hbqs>>stack_bq_count>>$", stack_bq_count)

                POGGER.debug("__hbqs>>token_stack>>$", parser_state.token_stack)
                possible_list_start_index = this_bq_count + 1
                forced_close_until_index = None
                if (
                    possible_list_start_index < len(parser_state.token_stack)
                    and parser_state.token_stack[possible_list_start_index].is_list
                ):
                    forced_close_until_index = possible_list_start_index
                    POGGER.debug(
                        "__hbqs>>fgg>>$<<",
                        parser_state.token_stack[possible_list_start_index],
                    )
                POGGER.debug("__hbqs>>fgg>>$", forced_close_until_index)

                adjusted_position_marker = PositionMarker(
                    position_marker.line_number,
                    len(text_removed_by_container),
                    position_marker.text_to_parse,
                )
                did_blank = True
                (leaf_tokens, requeue_line_info) = parser_state.handle_blank_line_fn(
                    parser_state,
                    line_to_parse,
                    from_main_transform=False,
                    forced_close_until_index=forced_close_until_index,
                    position_marker=adjusted_position_marker,
                )
                assert not (requeue_line_info and requeue_line_info.lines_to_requeue)
        else:
            POGGER.debug("handle_block_quote_section>>fenced")
            assert start_index >= 0
            removed_text = line_to_parse[0:start_index]
            line_to_parse = line_to_parse[start_index:]

            POGGER.debug("__hbqs>>removed_text>>$", removed_text)
            POGGER.debug("__hbqs>>line_to_parse>>$", line_to_parse)
            POGGER.debug("__hbqs>>this_bq_count>>$", this_bq_count)
            POGGER.debug("__hbqs>>stack_bq_count>>$", stack_bq_count)

            if this_bq_count < stack_bq_count:
                (container_level_tokens, _,) = parser_state.close_open_blocks_fn(
                    parser_state,
                    only_these_blocks=[
                        FencedCodeBlockStackToken,
                    ],
                    was_forced=True,
                )
                stack_bq_count = BlockQuoteProcessor.__decrease_stack_to_level(
                    parser_state, this_bq_count, stack_bq_count, container_level_tokens
                )

            stack_index = parser_state.find_last_block_quote_on_stack()
            found_bq_stack_token = parser_state.token_stack[stack_index]
            POGGER.debug(
                "found_bq_stack_token---$<<<",
                found_bq_stack_token,
            )
            found_bq_stack_token.matching_markdown_token.add_leading_spaces(
                removed_text
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
            stack_bq_count,
            this_bq_count,
            removed_chars_at_start,
            did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            None,
        )

    # pylint: enable=too-many-locals, too-many-statements

    # pylint: disable=too-many-arguments, too-many-statements, too-many-locals
    @staticmethod
    def __ensure_stack_at_level(
        parser_state,
        this_bq_count,
        stack_bq_count,
        extracted_whitespace,
        position_marker,
        original_start_index,
    ):
        """
        Ensure that the block quote stack is at the proper level on the stack.
        """

        container_level_tokens = []
        POGGER.debug(
            "__ensure_stack_at_level>>this_bq_count>>$>>stack_bq_count>>$",
            this_bq_count,
            stack_bq_count,
        )
        stack_increase_needed = False
        stack_decrease_needed = False
        if this_bq_count > stack_bq_count:
            POGGER.debug(
                "__ensure_stack_at_level>>increase to new level",
            )
            stack_increase_needed = True
        elif this_bq_count < stack_bq_count:
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
            )
            if requeue_line_info and requeue_line_info.lines_to_requeue:
                # TODO is this common?
                POGGER.debug(
                    "__ensure_stack_at_level>>lines_to_requeue>>$",
                    requeue_line_info.lines_to_requeue,
                )
                POGGER.debug(
                    "__close_required_lists_after_start>>parser_state.original_line_to_parse>>$",
                    parser_state.original_line_to_parse,
                )
                POGGER.debug(
                    "__ensure_stack_at_level>>token_stack>>$",
                    parser_state.token_stack,
                )
                POGGER.debug(
                    "__ensure_stack_at_level>>token_document>>$",
                    parser_state.token_document,
                )
                assert not requeue_line_info.lines_to_requeue[0]
                requeue_line_info.lines_to_requeue[
                    0
                ] = parser_state.original_line_to_parse
                POGGER.debug(
                    "__close_required_lists_after_start>>lines_to_requeue>>$",
                    requeue_line_info.lines_to_requeue,
                )
                return None, None, requeue_line_info
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

            POGGER.debug("container_level_tokens>>$", container_level_tokens)
            while this_bq_count > stack_bq_count:
                POGGER.debug(
                    "increasing block quotes by one>>",
                )
                stack_bq_count += 1

                adjusted_position_marker = PositionMarker(
                    position_marker.line_number,
                    original_start_index,
                    position_marker.text_to_parse,
                )

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
                parser_state.token_stack.append(
                    BlockQuoteStackToken(new_markdown_token)
                )
            POGGER.debug("container_level_tokens>>$", container_level_tokens)
            stack_bq_count = BlockQuoteProcessor.__decrease_stack_to_level(
                parser_state, this_bq_count, stack_bq_count, container_level_tokens
            )
            POGGER.debug(
                "container_level_tokens>>$",
                container_level_tokens,
            )

        return container_level_tokens, stack_bq_count, None

    @staticmethod
    def __decrease_stack_to_level(
        parser_state, this_bq_count, stack_bq_count, container_level_tokens
    ):
        while this_bq_count < stack_bq_count:
            POGGER.debug(
                "decreasing block quotes by one>>",
            )
            stack_bq_count -= 1
            (new_tokens, _,) = parser_state.close_open_blocks_fn(
                parser_state,
                include_block_quotes=True,
                until_this_index=len(parser_state.token_stack) - 1,
                was_forced=True,
            )
            container_level_tokens.extend(new_tokens)
        return stack_bq_count

    # pylint: enable=too-many-arguments, too-many-statements, too-many-locals
