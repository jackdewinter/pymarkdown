"""
Module to provide processing for the block quotes.
"""
import logging

from pymarkdown.container_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.parser_helper import ParserHelper, PositionMarker
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    FencedCodeBlockStackToken,
    HtmlBlockStackToken,
    IndentedCodeBlockStackToken,
    LinkDefinitionStackToken,
    ParagraphStackToken,
)

LOGGER = logging.getLogger(__name__)


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

        if ParserHelper.is_length_less_than_or_equal_to(
            adj_ws, 3
        ) and ParserHelper.is_character_at_index(
            line_to_parse, start_index, BlockQuoteProcessor.__block_quote_character
        ):
            return True
        return False

    @staticmethod
    def count_of_block_quotes_on_stack(parser_state):
        """
        Helper method to count the number of block quotes currently on the stack.
        """

        stack_bq_count = 0
        for next_item_on_stack in parser_state.token_stack:
            if next_item_on_stack.is_block_quote:
                stack_bq_count += 1

        return stack_bq_count

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
        LOGGER.debug("__check_for_lazy_handling")
        container_level_tokens = []
        LOGGER.debug(
            "this_bq_count>%s>>stack_bq_count>>%s<<",
            str(this_bq_count),
            str(stack_bq_count),
        )
        if this_bq_count == 0 and stack_bq_count > 0:
            LOGGER.debug("haven't processed")

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
                LOGGER.debug("__check_for_lazy_handling>>code block")
                assert not container_level_tokens
                container_level_tokens, _, _ = parser_state.close_open_blocks_fn(
                    parser_state,
                    only_these_blocks=[
                        BlockQuoteStackToken,
                        type(parser_state.token_stack[-1]),
                    ],
                    include_block_quotes=True,
                    was_forced=True,
                )
            else:
                LOGGER.debug("__check_for_lazy_handling>>not code block")
                LOGGER.debug(
                    "__check_for_lazy_handling>>%s", str(parser_state.token_stack)
                )

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
        LOGGER.debug("handle_block_quote_block>>start")

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

        lines_to_requeue = None
        force_ignore_first_as_lrd = None

        adjusted_text_to_parse = position_marker.text_to_parse
        adjusted_index_number = position_marker.index_number

        LOGGER.debug(
            "handle_block_quote_block>>text>:%s:<", str(position_marker.text_to_parse)
        )
        LOGGER.debug(
            "handle_block_quote_block>>extracted_whitespace>:%s:<",
            str(extracted_whitespace),
        )
        LOGGER.debug("handle_block_quote_block>>adj_ws>:%s:<", str(adj_ws))
        LOGGER.debug(
            "handle_block_quote_block>>was_link_definition_started>:%s:<",
            str(parser_state.token_stack[-1].was_link_definition_started),
        )
        if BlockQuoteProcessor.is_block_quote_start(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
            adj_ws=adj_ws,
        ):
            LOGGER.debug("handle_block_quote_block>>block-start")
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
                lines_to_requeue,
                force_ignore_first_as_lrd,
            ) = BlockQuoteProcessor.__handle_block_quote_section(
                parser_state,
                position_marker,
                stack_bq_count,
                extracted_whitespace,
            )
            LOGGER.debug(">>avoid_block_starts>>%s", str(avoid_block_starts))

            # TODO for nesting, may need to augment with this_bq_count already set.
            if this_bq_count == 0:
                this_bq_count = alt_this_bq_count
            else:
                LOGGER.debug(
                    ">>>>>>>>>>>>>>>%s>>>%s", str(this_bq_count), str(alt_this_bq_count)
                )
                this_bq_count = alt_this_bq_count

            did_process = True
            was_container_start = True
            end_of_bquote_start_index = adjusted_index_number
        elif parser_state.token_stack[-1].was_link_definition_started:
            stack_index = len(parser_state.token_stack) - 1
            last_block_token = None
            while stack_index > 0:
                if parser_state.token_stack[stack_index].is_block_quote:
                    last_block_token = parser_state.token_stack[
                        stack_index
                    ].matching_markdown_token
                stack_index -= 1
            if last_block_token:
                LOGGER.debug(
                    "handle_block w/ no open>>found>>%s",
                    ParserHelper.make_value_visible(last_block_token),
                )
                last_block_token.add_leading_spaces("")
            else:
                LOGGER.debug("handle_block w/ no open>>not found")

        LOGGER.debug("handle_block_quote_block>>end>>did_process>>%s", str(did_process))
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
            lines_to_requeue,
            force_ignore_first_as_lrd,
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

            LOGGER.debug(
                "stack_bq_count--%s--is_top_of_stack_fenced_code_block--%s",
                str(stack_bq_count),
                str(is_top_of_stack_fenced_code_block),
            )

            while True:
                if ParserHelper.is_character_at_index_whitespace(
                    adjusted_line, start_index
                ):
                    if adjusted_line[start_index] == ParserHelper.tab_character:
                        adjusted_tab_length = ParserHelper.calculate_length(
                            ParserHelper.tab_character, start_index=start_index
                        )
                        LOGGER.debug(
                            "adj--%s--", ParserHelper.make_value_visible(adjusted_line)
                        )
                        adjusted_line = (
                            adjusted_line[0:start_index]
                            + ParserHelper.repeat_string(
                                ParserHelper.space_character, adjusted_tab_length
                            )
                            + adjusted_line[start_index + 1 :]
                        )
                        LOGGER.debug(
                            "--%s--", ParserHelper.make_value_visible(adjusted_line)
                        )
                    start_index += 1

                LOGGER.debug(
                    "this_bq_count--%s--stack_bq_count--%s",
                    str(this_bq_count),
                    str(stack_bq_count),
                )
                if is_top_of_stack_is_html_block:
                    if this_bq_count == stack_bq_count:
                        LOGGER.debug(
                            "block quote levels don't increase during html block, ignoring"
                        )
                        avoid_block_starts = ParserHelper.is_character_at_index(
                            adjusted_line,
                            start_index,
                            BlockQuoteProcessor.__block_quote_character,
                        )
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

            LOGGER.debug(
                "__count_block_quote_starts--%s--%s--",
                str(start_index),
                ParserHelper.make_value_visible(adjusted_line),
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

        LOGGER.debug(
            "IN>__handle_block_quote_section---%s<<<",
            ParserHelper.make_value_visible(line_to_parse),
        )
        LOGGER.debug("stack_bq_count--%s", str(stack_bq_count))
        LOGGER.debug("token_stack[-1]--%s", str(parser_state.token_stack[-1]))

        did_blank = False
        leaf_tokens = []
        container_level_tokens = []
        removed_chars_at_start = 0

        LOGGER.debug(
            "__handle_block_quote_section---%s--%s--",
            str(start_index),
            ParserHelper.make_value_visible(line_to_parse),
        )
        original_start_index = start_index
        original_line_to_parse = line_to_parse
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
        LOGGER.debug(">>avoid_block_starts>>%s", str(avoid_block_starts))
        LOGGER.debug(
            "__handle_block_quote_section---this_bq_count--%s--%s--%s--",
            str(this_bq_count),
            str(start_index),
            ParserHelper.make_value_visible(line_to_parse),
        )
        LOGGER.debug(
            "ORIG-->WS[%s]--SI[%s]--[%s]",
            extracted_whitespace,
            str(original_start_index),
            str(original_line_to_parse),
        )
        LOGGER.debug("NOW -->SI[%s]--[%s]", str(start_index), str(line_to_parse))

        if not parser_state.token_stack[-1].is_fenced_code_block:
            LOGGER.debug("handle_block_quote_section>>not fenced")
            (
                container_level_tokens,
                stack_bq_count,
                lines_to_requeue,
                force_ignore_first_as_lrd,
            ) = BlockQuoteProcessor.__ensure_stack_at_level(
                parser_state,
                this_bq_count,
                stack_bq_count,
                extracted_whitespace,
                position_marker,
                original_start_index,
                original_line_to_parse,
            )
            if lines_to_requeue:
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
                    lines_to_requeue,
                    force_ignore_first_as_lrd,
                )

            removed_text = (
                extracted_whitespace
                + line_to_parse[position_marker.index_number : start_index]
            )
            LOGGER.debug(
                "==EWS[%s],OSI[%s],SI[%s],LTP[%s]",
                extracted_whitespace,
                str(original_start_index),
                str(position_marker.index_number),
                position_marker.text_to_parse,
            )
            line_to_parse = line_to_parse[start_index:]
            removed_chars_at_start = start_index
            LOGGER.debug("==REM[%s],LTP[%s]", str(removed_text), str(line_to_parse))

            stack_index = len(parser_state.token_stack) - 1
            while True:
                LOGGER.debug(
                    "--%s--%s",
                    str(stack_index),
                    str(parser_state.token_stack[stack_index]),
                )
                if parser_state.token_stack[stack_index].is_block_quote:
                    found_bq_stack_token = parser_state.token_stack[stack_index]
                    break
                stack_index -= 1
            found_bq_stack_token.matching_markdown_token.add_leading_spaces(
                removed_text
            )
            text_removed_by_container = removed_text

            if not line_to_parse.strip():
                LOGGER.debug("call __handle_block_quote_section>>handle_blank_line")

                LOGGER.debug("__hbqs>>this_bq_count>>%s", str(this_bq_count))
                LOGGER.debug("__hbqs>>stack_bq_count>>%s", str(stack_bq_count))

                LOGGER.debug("__hbqs>>token_stack>>%s", str(parser_state.token_stack))
                possible_list_start_index = this_bq_count + 1
                forced_close_until_index = None
                if (
                    possible_list_start_index < len(parser_state.token_stack)
                    and parser_state.token_stack[possible_list_start_index].is_list
                ):
                    forced_close_until_index = possible_list_start_index
                    LOGGER.debug(
                        "__hbqs>>fgg>>%s<<",
                        str(parser_state.token_stack[possible_list_start_index]),
                    )
                LOGGER.debug("__hbqs>>fgg>>%s", str(forced_close_until_index))

                adjusted_position_marker = PositionMarker(
                    position_marker.line_number,
                    len(text_removed_by_container),
                    position_marker.text_to_parse,
                )
                did_blank = True
                (leaf_tokens, lines_to_requeue, _,) = parser_state.handle_blank_line_fn(
                    parser_state,
                    line_to_parse,
                    from_main_transform=False,
                    forced_close_until_index=forced_close_until_index,
                    position_marker=adjusted_position_marker,
                )
                assert not lines_to_requeue
        else:
            LOGGER.debug("handle_block_quote_section>>fenced")
            removed_text = line_to_parse[0:start_index]
            line_to_parse = line_to_parse[start_index:]

            LOGGER.debug("__hbqs>>this_bq_count>>%s", str(this_bq_count))
            LOGGER.debug("__hbqs>>stack_bq_count>>%s", str(stack_bq_count))

            if this_bq_count < stack_bq_count:
                (container_level_tokens, _, _,) = parser_state.close_open_blocks_fn(
                    parser_state,
                    only_these_blocks=[
                        FencedCodeBlockStackToken,
                    ],
                    was_forced=True,
                )
                while this_bq_count < stack_bq_count:
                    stack_bq_count -= 1
                    ind = len(parser_state.token_stack) - 1
                    (new_tokens, _, _,) = parser_state.close_open_blocks_fn(
                        parser_state,
                        include_block_quotes=True,
                        until_this_index=ind,
                        was_forced=True,
                    )
                    container_level_tokens.extend(new_tokens)

            # TODO collapse?
            found_bq_stack_token = None
            for stack_index in range(len(parser_state.token_stack) - 1, -1, -1):
                LOGGER.debug(
                    "--%s--%s",
                    str(stack_index),
                    str(parser_state.token_stack[stack_index]),
                )
                if parser_state.token_stack[stack_index].is_block_quote:
                    found_bq_stack_token = parser_state.token_stack[stack_index]
                    break
            if found_bq_stack_token:
                found_bq_stack_token.matching_markdown_token.add_leading_spaces(
                    removed_text
                )

        LOGGER.debug(
            "OUT>__handle_block_quote_section---%s<<<",
            ParserHelper.make_value_visible(line_to_parse),
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
        original_line_to_parse,
    ):
        """
        Ensure that the block quote stack is at the proper level on the stack.
        """

        container_level_tokens = []
        LOGGER.debug(
            "__ensure_stack_at_level>>this_bq_count>>%s>>stack_bq_count>>%s",
            str(this_bq_count),
            str(stack_bq_count),
        )
        stack_increase_needed = False
        stack_decrease_needed = False
        if this_bq_count > stack_bq_count:
            LOGGER.debug(
                "__ensure_stack_at_level>>increase to new level",
            )
            stack_increase_needed = True
        elif this_bq_count < stack_bq_count:
            LOGGER.debug(
                "__ensure_stack_at_level>>possible decrease to new level",
            )
            top_token_on_stack = parser_state.token_stack[-1]
            LOGGER.debug("__ensure_stack_at_level>>%s", str(top_token_on_stack))
            stack_decrease_needed = (
                top_token_on_stack.is_indented_code_block
                or top_token_on_stack.is_html_block
            )
            LOGGER.debug(
                "__ensure_stack_at_level>>decrease to new level=%s",
                str(stack_decrease_needed),
            )

        if stack_increase_needed or stack_decrease_needed:
            LOGGER.debug(
                "token_stack>>%s",
                ParserHelper.make_value_visible(parser_state.token_stack),
            )
            LOGGER.debug(
                "token_document>>%s",
                ParserHelper.make_value_visible(parser_state.token_document),
            )
            (
                container_level_tokens,
                lines_to_requeue,
                force_ignore_first_as_lrd,
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
            if lines_to_requeue:
                LOGGER.debug(
                    "__ensure_stack_at_level>>lines_to_requeue>>%s",
                    ParserHelper.make_value_visible(lines_to_requeue),
                )
                LOGGER.debug(
                    "__close_required_lists_after_start>>original_line_to_parse>>%s",
                    ParserHelper.make_value_visible(original_line_to_parse),
                )
                LOGGER.debug(
                    "__ensure_stack_at_level>>token_stack>>%s",
                    ParserHelper.make_value_visible(parser_state.token_stack),
                )
                LOGGER.debug(
                    "__ensure_stack_at_level>>token_document>>%s",
                    ParserHelper.make_value_visible(parser_state.token_document),
                )
                assert not lines_to_requeue[0]
                lines_to_requeue[0] = original_line_to_parse
                LOGGER.debug(
                    "__close_required_lists_after_start>>lines_to_requeue>>%s",
                    ParserHelper.make_value_visible(lines_to_requeue),
                )
                return None, None, lines_to_requeue, force_ignore_first_as_lrd
            LOGGER.debug(
                "token_stack>>%s",
                ParserHelper.make_value_visible(parser_state.token_stack),
            )
            LOGGER.debug(
                "token_document>>%s",
                ParserHelper.make_value_visible(parser_state.token_document),
            )
            LOGGER.debug(
                "container_level_tokens>>%s",
                ParserHelper.make_value_visible(container_level_tokens),
            )
            keep_going = True
            while keep_going and parser_state.token_stack[-1].is_list:
                LOGGER.debug(
                    "stack>>%s", str(parser_state.token_stack[-1].indent_level)
                )
                LOGGER.debug("original_start_index>>%s", str(original_start_index))

                if original_start_index < parser_state.token_stack[-1].indent_level:
                    close_tokens, _, _ = parser_state.close_open_blocks_fn(
                        parser_state,
                        include_lists=True,
                        was_forced=True,
                        until_this_index=len(parser_state.token_stack) - 1,
                    )
                    container_level_tokens.extend(close_tokens)
                    LOGGER.debug(
                        "container_level_tokens>>%s",
                        ParserHelper.make_value_visible(container_level_tokens),
                    )
                else:
                    keep_going = False

            LOGGER.debug(
                "container_level_tokens>>%s",
                ParserHelper.make_value_visible(container_level_tokens),
            )
            while this_bq_count > stack_bq_count:
                LOGGER.debug(
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
            LOGGER.debug(
                "container_level_tokens>>%s",
                ParserHelper.make_value_visible(container_level_tokens),
            )
            while this_bq_count < stack_bq_count:
                LOGGER.debug(
                    "decreasing block quotes by one>>",
                )
                stack_bq_count -= 1
                ind = len(parser_state.token_stack) - 1
                (new_tokens, _, _,) = parser_state.close_open_blocks_fn(
                    parser_state,
                    include_block_quotes=True,
                    until_this_index=ind,
                    was_forced=True,
                )
                container_level_tokens.extend(new_tokens)
            LOGGER.debug(
                "container_level_tokens>>%s",
                ParserHelper.make_value_visible(container_level_tokens),
            )

        return container_level_tokens, stack_bq_count, None, None

    # pylint: enable=too-many-arguments, too-many-statements, too-many-locals
