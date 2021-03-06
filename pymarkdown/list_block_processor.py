"""
Module to provide processing for the list blocks.
"""

import logging
import string

from pymarkdown.container_markdown_token import (
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    UnorderedListStartMarkdownToken,
)
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.stack_token import OrderedListStackToken, UnorderedListStackToken

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-many-lines
class ListBlockProcessor:
    """
    Class to provide processing for the list blocks.
    """

    __ulist_start_characters = "-+*"
    __olist_start_characters = ".)"

    @staticmethod
    # pylint: disable=too-many-arguments
    def is_ulist_start(
        parser_state,
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check,
        adj_ws=None,
    ):
        """
        Determine if we have the start of an un-numbered list.
        """
        LOGGER.debug("is_ulist_start>>pre>>")
        is_start = False
        after_all_whitespace_index = -1
        if adj_ws is None:
            adj_ws = extracted_whitespace

        if (
            ParserHelper.is_length_less_than_or_equal_to(adj_ws, 3)
            or skip_whitespace_check
        ):
            is_start = ListBlockProcessor.__is_start_ulist(
                line_to_parse, start_index, extracted_whitespace
            )
        if is_start:
            (
                is_start,
                after_all_whitespace_index,
            ) = ListBlockProcessor.__is_start_phase_one(
                parser_state, line_to_parse, start_index, False
            )
        if is_start:
            is_start = ListBlockProcessor.__is_start_phase_two(
                parser_state,
                line_to_parse[start_index],
                True,
                False,
                after_all_whitespace_index,
                line_to_parse,
                start_index,
            )

        return is_start, after_all_whitespace_index, start_index, 0
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements
    @staticmethod
    def is_olist_start(
        parser_state,
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check,
        adj_ws=None,
    ):
        """
        Determine if we have the start of an numbered or ordered list.
        """

        is_start = False
        after_all_whitespace_index = -1
        index = None
        number_of_digits = None
        is_not_one = False

        if adj_ws is None:
            adj_ws = extracted_whitespace

        if (
            ParserHelper.is_length_less_than_or_equal_to(adj_ws, 3)
            or skip_whitespace_check
        ):
            (
                is_start,
                index,
                number_of_digits,
                is_not_one,
            ) = ListBlockProcessor.__is_start_olist(line_to_parse, start_index)
        if is_start:
            (
                is_start,
                after_all_whitespace_index,
            ) = ListBlockProcessor.__is_start_phase_one(
                parser_state, line_to_parse, index, is_not_one
            )
        if is_start:
            is_start = ListBlockProcessor.__is_start_phase_two(
                parser_state,
                line_to_parse[index],
                False,
                is_not_one,
                after_all_whitespace_index,
                line_to_parse,
                start_index,
            )

        return is_start, after_all_whitespace_index, index, number_of_digits

    # pylint: enable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements

    @staticmethod
    def __is_start_ulist(line_to_parse, start_index, extracted_whitespace):
        is_start = ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, ListBlockProcessor.__ulist_start_characters
        )

        # Thematic breaks have precedence, so stop a list start if we find one.
        is_break, _ = LeafBlockProcessor.is_thematic_break(
            line_to_parse, start_index, extracted_whitespace
        )
        is_start = is_start and not is_break
        return is_start

    @staticmethod
    def __is_start_olist(line_to_parse, start_index):
        index = None
        number_of_digits = None
        is_not_one = None
        is_start = ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, string.digits
        )
        if is_start:
            index = start_index
            while ParserHelper.is_character_at_index_one_of(
                line_to_parse, index, string.digits
            ):
                index += 1
            number_of_digits = index - start_index
            olist_index_number = line_to_parse[start_index:index]
            LOGGER.debug(
                "olist?%s<<count>>%s<<", olist_index_number, str(number_of_digits)
            )
            is_not_one = olist_index_number != "1"

            is_olist_start = ParserHelper.is_character_at_index_one_of(
                line_to_parse, index, ListBlockProcessor.__olist_start_characters
            )
            LOGGER.debug("is_olist_start>>%s", str(is_olist_start))
            is_start = is_olist_start and number_of_digits <= 9

        return is_start, index, number_of_digits, is_not_one

    @staticmethod
    def __is_start_phase_one(parser_state, line_to_parse, start_index, is_not_one):
        is_start = False

        after_all_whitespace_index, _ = ParserHelper.extract_whitespace(
            line_to_parse, start_index + 1
        )
        LOGGER.debug(
            "after_all_whitespace_index>>%s>>len>>%s",
            str(after_all_whitespace_index),
            str(len(line_to_parse)),
        )
        at_end_of_line = after_all_whitespace_index == len(line_to_parse)
        LOGGER.debug("at_end_of_line>>%s", str(at_end_of_line))

        is_paragraph_in_list = False
        is_in_paragraph = parser_state.token_stack[-1].is_paragraph
        if is_in_paragraph:
            is_paragraph_in_list = parser_state.token_stack[-2].is_list

        if not (
            is_in_paragraph
            and not is_paragraph_in_list
            and (at_end_of_line or is_not_one)
        ) and (
            ParserHelper.is_character_at_index_whitespace(
                line_to_parse, start_index + 1
            )
            or ((start_index + 1) == len(line_to_parse))
        ):
            is_start = True
        return is_start, after_all_whitespace_index

    # pylint: disable=too-many-arguments
    @staticmethod
    def __is_start_phase_two(
        parser_state,
        xx_seq,
        is_unordered_list,
        is_not_one,
        after_all_whitespace_index,
        line_to_parse,
        start_index,
    ):
        is_start = True

        is_in_paragraph = parser_state.token_stack[-1].is_paragraph
        LOGGER.debug("is_in_paragraph>>%s", str(is_in_paragraph))
        at_end_of_line = after_all_whitespace_index == len(line_to_parse)
        LOGGER.debug("at_end_of_line>>%s", str(at_end_of_line))

        is_first_item_in_list = False
        is_sub_list = False
        if is_in_paragraph:
            if not parser_state.token_stack[-2].is_list:
                LOGGER.debug(
                    "top of stack is not list>>%s",
                    str(parser_state.token_stack[-2]),
                )
                is_first_item_in_list = True
            elif is_unordered_list and parser_state.token_stack[-2].is_ordered_list:
                LOGGER.debug(
                    "top of stack is ordered list>>%s",
                    str(parser_state.token_stack[-2]),
                )
                is_first_item_in_list = True
            elif xx_seq != parser_state.token_stack[-2].list_character[-1]:
                LOGGER.debug(
                    "xx>>%s!=%s",
                    str(line_to_parse[start_index]),
                    str(parser_state.token_stack[-2].list_character),
                )
                is_first_item_in_list = True
            else:
                is_first_item_in_list = (
                    start_index >= parser_state.token_stack[-2].indent_level
                )
                LOGGER.debug(
                    "start_index>>%s>=%s",
                    str(start_index),
                    str(parser_state.token_stack[-2].indent_level),
                )
            LOGGER.debug("is_first_item_in_list>>%s", str(is_first_item_in_list))

            if parser_state.token_stack[-2].is_list:
                LOGGER.debug(
                    "old_indent=%s", str(parser_state.token_stack[-2].indent_level)
                )
                LOGGER.debug("new_indent=%s", str(start_index))
                is_sub_list = start_index >= parser_state.token_stack[-2].indent_level

        LOGGER.debug(
            "is_in_para>>%s>>EOL>%s>is_first>%s",
            str(is_in_paragraph),
            str(at_end_of_line),
            str(is_first_item_in_list),
        )
        if (
            is_in_paragraph
            and (at_end_of_line or is_not_one)
            and is_first_item_in_list
            and is_sub_list
        ):
            is_start = False
            LOGGER.debug("is_start>>%s", str(is_start))
        return is_start

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def handle_list_block(
        is_ulist,
        parser_state,
        did_process,
        was_container_start,
        position_marker,
        extracted_whitespace,
        adj_ws,
        stack_bq_count,
        this_bq_count,
        removed_chars_at_start,
        current_container_blocks,
    ):
        """
        Handle the processing of a ulist block.
        """
        requeue_line_info = None
        end_of_ulist_start_index = -1
        container_level_tokens = []
        adjusted_text_to_parse = position_marker.text_to_parse
        if not did_process:

            if is_ulist:
                is_start_fn = ListBlockProcessor.is_ulist_start
                create_token_fn = ListBlockProcessor.__handle_list_block_unordered
            else:
                is_start_fn = ListBlockProcessor.is_olist_start
                create_token_fn = ListBlockProcessor.__handle_list_block_ordered

            (
                started_ulist,
                end_of_ulist_start_index,
                index,
                number_of_digits,
            ) = is_start_fn(
                parser_state,
                position_marker.text_to_parse,
                position_marker.index_number,
                extracted_whitespace,
                False,
                adj_ws=adj_ws,
            )
            if started_ulist:
                LOGGER.debug("clt>>ulist-start")
                removed_chars_at_start = 0

                (
                    indent_level,
                    remaining_whitespace,
                    ws_after_marker,
                    after_marker_ws_index,
                    ws_before_marker,
                    container_level_tokens,
                    stack_bq_count,
                ) = ListBlockProcessor.__pre_list(
                    parser_state,
                    position_marker.text_to_parse,
                    index,
                    extracted_whitespace,
                    number_of_digits,
                    stack_bq_count,
                    this_bq_count,
                    adj_ws=adj_ws,
                )

                LOGGER.debug(
                    "total=%s;ws-before=%s;ws_after=%s;start_index=%s",
                    str(indent_level),
                    str(ws_before_marker),
                    str(ws_after_marker),
                    str(position_marker.index_number),
                )
                new_token, new_stack = create_token_fn(
                    position_marker,
                    indent_level,
                    extracted_whitespace,
                    ws_before_marker,
                    ws_after_marker,
                    index,
                )

                (
                    new_container_level_tokens,
                    adjusted_text_to_parse,
                    requeue_line_info,
                ) = ListBlockProcessor.__post_list(
                    parser_state,
                    new_stack,
                    new_token,
                    position_marker.text_to_parse,
                    remaining_whitespace,
                    after_marker_ws_index,
                    indent_level,
                    current_container_blocks,
                    position_marker,
                )
                if new_container_level_tokens:
                    container_level_tokens.extend(new_container_level_tokens)
                did_process = True
                was_container_start = True
        return (
            did_process,
            was_container_start,
            end_of_ulist_start_index,
            adjusted_text_to_parse,
            container_level_tokens,
            removed_chars_at_start,
            requeue_line_info,
        )
        # pylint: enable=too-many-locals, too-many-arguments

    @staticmethod
    # pylint: disable=too-many-arguments
    def __handle_list_block_unordered(
        position_marker,
        indent_level,
        extracted_whitespace,
        ws_before_marker,
        ws_after_marker,
        index,
    ):
        _ = index

        new_token = UnorderedListStartMarkdownToken(
            position_marker.text_to_parse[position_marker.index_number],
            indent_level,
            extracted_whitespace,
            position_marker,
        )
        new_stack = UnorderedListStackToken(
            indent_level,
            position_marker.text_to_parse[position_marker.index_number],
            ws_before_marker,
            ws_after_marker,
            position_marker.index_number,
            new_token,
        )
        return new_token, new_stack

    # pylint: enable=too-many-arguments

    @staticmethod
    # pylint: disable=too-many-arguments
    def __handle_list_block_ordered(
        position_marker,
        indent_level,
        extracted_whitespace,
        ws_before_marker,
        ws_after_marker,
        index,
    ):
        new_token = OrderedListStartMarkdownToken(
            position_marker.text_to_parse[index],
            position_marker.text_to_parse[position_marker.index_number : index],
            indent_level,
            extracted_whitespace,
            position_marker,
        )
        new_stack = OrderedListStackToken(
            indent_level,
            position_marker.text_to_parse[position_marker.index_number : index + 1],
            ws_before_marker,
            ws_after_marker,
            position_marker.index_number,
            new_token,
        )
        return new_token, new_stack

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-statements, too-many-locals
    @staticmethod
    def list_in_process(
        parser_state,
        line_to_parse,
        start_index,
        extracted_whitespace,
        ind,
    ):
        """
        Handle the processing of a line where there is a list in process.
        """
        container_level_tokens = []

        LOGGER.debug("!!!!!FOUND>>%s", str(parser_state.token_stack[ind]))
        LOGGER.debug("!!!!!FOUND>>%s", str(parser_state.token_stack[ind].extra_data))
        LOGGER.debug("!!!!!ALL>>%s", str(parser_state.token_stack))
        LOGGER.debug("!!!!!ALL>>%s", str(parser_state.token_document))

        requested_list_indent = parser_state.token_stack[ind].indent_level
        before_ws_length = parser_state.token_stack[ind].ws_before_marker
        LOGGER.debug(
            "!!!!!requested_list_indent>>%s,before_ws=%s",
            str(requested_list_indent),
            str(before_ws_length),
        )

        leading_space_length = ParserHelper.calculate_length(extracted_whitespace)

        started_ulist, _, _, _ = ListBlockProcessor.is_ulist_start(
            parser_state,
            line_to_parse,
            start_index,
            extracted_whitespace,
            True,
        )
        started_olist, _, _, _ = ListBlockProcessor.is_olist_start(
            parser_state,
            line_to_parse,
            start_index,
            extracted_whitespace,
            True,
        )

        allow_list_continue = True
        if leading_space_length >= 4 and (started_ulist or started_olist):
            allow_list_continue = not parser_state.token_document[-1].is_blank_line

        LOGGER.debug(
            "leading_space_length>>%s>>requested_list_indent>>%s>>is_in_paragraph>>%s",
            str(leading_space_length),
            str(requested_list_indent),
            str(parser_state.token_stack[-1].is_paragraph),
        )

        used_indent = None

        if leading_space_length >= requested_list_indent and allow_list_continue:

            LOGGER.debug("before>>%s>>", line_to_parse)
            (
                line_to_parse,
                used_indent,
            ) = ListBlockProcessor.__adjust_line_for_list_in_process(
                line_to_parse,
                start_index,
                extracted_whitespace,
                leading_space_length,
                requested_list_indent,
            )
            LOGGER.debug(
                "after>>%s>>%s>>",
                line_to_parse,
                used_indent,
            )
        else:
            LOGGER.debug(
                "requested_list_indent>>%s<<",
                str(requested_list_indent),
            )
            original_requested_list_indent = requested_list_indent
            requested_list_indent = requested_list_indent - before_ws_length
            LOGGER.debug(
                "leading_space_length>>%s>>adj requested_list_indent>>%s>>%s<<",
                str(leading_space_length),
                str(requested_list_indent),
                str(parser_state.token_stack[-1].is_paragraph),
            )

            # This needs to be in place to prevent a thematic break after a paragraph
            # within a list from being misinterpretted as a SetExt Heading.
            is_theme_break, _ = LeafBlockProcessor.is_thematic_break(
                line_to_parse,
                start_index,
                extracted_whitespace,
                skip_whitespace_check=True,
            )
            LOGGER.debug("is_theme_break>>%s", str(is_theme_break))

            if (
                parser_state.token_stack[-1].is_paragraph
                and leading_space_length >= requested_list_indent
                and allow_list_continue
                and not is_theme_break
            ):
                LOGGER.debug(
                    "1>>line_to_parse>>%s>>",
                    ParserHelper.make_value_visible(line_to_parse),
                )
                (
                    line_to_parse,
                    used_indent,
                ) = ListBlockProcessor.__adjust_line_for_list_in_process(
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    leading_space_length,
                    original_requested_list_indent,
                )
                LOGGER.debug(
                    ">>line_to_parse>>%s>>",
                    ParserHelper.make_value_visible(line_to_parse),
                )
                LOGGER.debug(
                    ">>used_indent>>%s>>", ParserHelper.make_value_visible(used_indent)
                )
            else:
                LOGGER.debug(
                    "2>>line_to_parse>>%s>>",
                    ParserHelper.make_value_visible(line_to_parse),
                )
                container_level_tokens = ListBlockProcessor.__check_for_list_closures(
                    parser_state,
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    ind,
                    leading_space_length,
                )

                LOGGER.debug(
                    "2>>__check_for_list_closures>>%s>>",
                    ParserHelper.make_value_visible(container_level_tokens),
                )
                LOGGER.debug(
                    "2>>parser_state.token_stack>>%s>>",
                    ParserHelper.make_value_visible(parser_state.token_stack),
                )
                LOGGER.debug(
                    "2>>ind>>%s>>",
                    ParserHelper.make_value_visible(ind),
                )

                found_owning_list = None
                if container_level_tokens:
                    (
                        did_find,
                        last_list_index,
                    ) = LeafBlockProcessor.check_for_list_in_process(parser_state)
                    LOGGER.debug(
                        "2>>did_find>>%s>>%s>>",
                        ParserHelper.make_value_visible(did_find),
                        ParserHelper.make_value_visible(last_list_index),
                    )
                    if did_find:
                        ind = last_list_index
                        found_owning_list = parser_state.token_stack[ind]
                else:
                    assert parser_state.token_stack[ind].is_list
                    found_owning_list = parser_state.token_stack[ind]

                if found_owning_list:
                    LOGGER.debug(">>in list>>")
                    requested_list_indent = found_owning_list.indent_level
                    if found_owning_list.last_new_list_token:
                        requested_list_indent = (
                            found_owning_list.last_new_list_token.indent_level
                        )
                    LOGGER.debug(">>line_to_parse>>%s>>", line_to_parse)
                    LOGGER.debug(
                        ">>extracted_whitespace>>%s<<", str(extracted_whitespace)
                    )
                    LOGGER.debug(">>start_index>>%s", str(start_index))
                    LOGGER.debug(
                        ">>requested_list_indent>>%s", str(requested_list_indent)
                    )
                    LOGGER.debug(">>before_ws_length>>%s", str(before_ws_length))
                    (
                        line_to_parse,
                        used_indent,
                    ) = ListBlockProcessor.__adjust_line_for_list_in_process(
                        line_to_parse,
                        start_index,
                        extracted_whitespace,
                        leading_space_length,
                        requested_list_indent,
                    )
                    LOGGER.debug(">>line_to_parse>>%s", str(line_to_parse))
                    LOGGER.debug(">>used_indent>>%s<<", str(used_indent))

        LOGGER.debug(">>used_indent>>%s<<", str(used_indent))
        if used_indent is not None:
            LOGGER.debug(
                ">>adj_before>>%s<<",
                ParserHelper.make_value_visible(
                    parser_state.token_stack[ind].matching_markdown_token
                ),
            )
            parser_state.token_stack[ind].matching_markdown_token.add_leading_spaces(
                used_indent
            )
            LOGGER.debug(
                ">>adj_after>>%s<<",
                ParserHelper.make_value_visible(
                    parser_state.token_stack[ind].matching_markdown_token
                ),
            )
        return container_level_tokens, line_to_parse, used_indent

    # pylint: enable=too-many-statements, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __pre_list(
        parser_state,
        line_to_parse,
        start_index,
        extracted_whitespace,
        marker_width_minus_one,
        stack_bq_count,
        this_bq_count,
        adj_ws,
    ):
        """
        Handle the processing of the first part of the list.
        """

        (
            after_marker_ws_index,
            after_marker_whitespace,
        ) = ParserHelper.extract_whitespace(line_to_parse, start_index + 1)
        ws_after_marker = ParserHelper.calculate_length(
            after_marker_whitespace, start_index=start_index + 1
        )
        LOGGER.debug(
            "after-marker>>%s>>total=%s", after_marker_whitespace, str(ws_after_marker)
        )

        ws_before_marker = ParserHelper.calculate_length(extracted_whitespace)
        LOGGER.debug(
            "--ws_before_marker>>%s>>marker_width_minus_one>>%s",
            str(ws_before_marker),
            str(marker_width_minus_one),
        )
        LOGGER.debug("--%s--%s", str(start_index), str(start_index + 1))

        (
            container_level_tokens,
            stack_bq_count,
        ) = ListBlockProcessor.__handle_list_nesting(
            parser_state, stack_bq_count, this_bq_count
        )
        LOGGER.debug(
            ">>>>>XX>>%s>>%s<<", str(after_marker_ws_index), str(len(line_to_parse))
        )
        if after_marker_ws_index == len(line_to_parse) and ws_after_marker:
            LOGGER.debug("BOOOOOOOM")
            LOGGER.debug(
                ">>parser_state.token_stack>>%s", str(parser_state.token_stack)
            )
            indent_level = 2 + marker_width_minus_one + len(adj_ws)
            remaining_whitespace = ws_after_marker
            ws_after_marker = 0
        else:
            if after_marker_ws_index == len(line_to_parse) and ws_after_marker == 0:
                ws_after_marker += 1

            indent_level = (
                ws_before_marker + 1 + ws_after_marker + marker_width_minus_one
            )
            remaining_whitespace = 0
            LOGGER.debug(
                "ws_after_marker>>%s<<indent_level<<%s<<rem<<%s<<",
                str(ws_after_marker),
                str(indent_level),
                str(remaining_whitespace),
            )
            if ws_after_marker > 4:
                indent_level = indent_level - ws_after_marker + 1
                remaining_whitespace = ws_after_marker - 1
                ws_after_marker = 1
                LOGGER.debug(
                    "ws_after_marker>>%s<<indent_level<<%s<<rem<<%s<<",
                    str(ws_after_marker),
                    str(indent_level),
                    str(remaining_whitespace),
                )
        LOGGER.debug(
            "ws_after_marker>>%s<<indent_level<<%s<<rem<<%s<<",
            str(ws_after_marker),
            str(indent_level),
            str(remaining_whitespace),
        )
        return (
            indent_level,
            remaining_whitespace,
            ws_after_marker,
            after_marker_ws_index,
            ws_before_marker,
            container_level_tokens,
            stack_bq_count,
        )
        # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_list_nesting(parser_state, stack_bq_count, this_bq_count):
        """
        Resolve any nesting issues with block quotes.
        """
        LOGGER.debug(
            ">>stack_bq_count>>%s>>this_bq_count>>%s",
            str(stack_bq_count),
            str(this_bq_count),
        )
        container_level_tokens = []
        while this_bq_count < stack_bq_count:

            assert not container_level_tokens
            last_block_index = parser_state.find_last_block_quote_on_stack()
            container_level_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=last_block_index,
                include_block_quotes=True,
                include_lists=True,
            )
            LOGGER.debug("container_level_tokens>>%s", str(container_level_tokens))
            stack_bq_count -= 1
        return container_level_tokens, stack_bq_count

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __post_list(
        parser_state,
        new_stack,
        new_token,
        line_to_parse,
        remaining_whitespace,
        after_marker_ws_index,
        indent_level,
        current_container_blocks,
        position_marker,
    ):
        """
        Handle the processing of the last part of the list.
        """

        LOGGER.debug("new_stack>>%s", str(new_stack))
        LOGGER.debug("indent_level>>%s", str(indent_level))

        emit_item = True
        emit_li = True
        did_find, last_list_index = LeafBlockProcessor.check_for_list_in_process(
            parser_state
        )
        if did_find:
            (
                container_level_tokens,
                emit_li,
                requeue_line_info,
            ) = ListBlockProcessor.__close_required_lists_after_start(
                parser_state,
                last_list_index,
                new_stack,
                current_container_blocks,
            )
            if requeue_line_info:
                return None, None, requeue_line_info
            emit_item = False
        else:
            LOGGER.debug(
                "NOT list-in-process>>%s",
                str(parser_state.token_stack[last_list_index]),
            )
            container_level_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state, was_forced=True
            )
        LOGGER.debug("container_level_tokens>>%s", str(container_level_tokens))

        LOGGER.debug("__post_list>>before>>%s", str(container_level_tokens))
        if emit_item or not emit_li:
            LOGGER.debug("__post_list>>adding>>%s", str(new_token))
            parser_state.token_stack.append(new_stack)
            container_level_tokens.append(new_token)
        else:
            LOGGER.debug("__post_list>>new list item>>")
            assert emit_li
            ListBlockProcessor.__post_list_use_new_list_item(
                parser_state,
                new_token,
                container_level_tokens,
                indent_level,
                position_marker,
            )
        LOGGER.debug(
            "__post_list>>rem>>%s>>after_in>>%s",
            str(remaining_whitespace),
            str(after_marker_ws_index),
        )
        line_to_parse = (
            ParserHelper.repeat_string(
                ParserHelper.space_character, remaining_whitespace
            )
            + line_to_parse[after_marker_ws_index:]
        )
        LOGGER.debug("__post_list>>after>>%s", str(container_level_tokens))

        parser_state.set_no_para_start_if_empty()
        return container_level_tokens, line_to_parse, None
        # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __post_list_use_new_list_item(
        parser_state, new_token, container_level_tokens, indent_level, position_marker
    ):
        LOGGER.debug("instead of-->%s", str(new_token))

        top_stack_item = parser_state.token_stack[-1]
        assert top_stack_item.is_list

        list_start_content = ""
        if top_stack_item.is_ordered_list:
            list_start_content = new_token.list_start_content
            LOGGER.debug("ordered->start-->%s", str(new_token.list_start_content))
        else:
            LOGGER.debug("unordered->start-->")

        new_token = NewListItemMarkdownToken(
            indent_level,
            position_marker,
            new_token.extracted_whitespace,
            list_start_content,
        )
        top_stack_item.set_last_new_list_token(new_token)
        container_level_tokens.append(new_token)

    @staticmethod
    def __close_required_lists_after_start(
        parser_state,
        last_list_index,
        new_stack,
        current_container_blocks,
    ):
        """
        After a list start, check to see if any others need closing.
        """
        LOGGER.debug(
            "list-in-process>>%s", str(parser_state.token_stack[last_list_index])
        )
        (
            container_level_tokens,
            requeue_line_info,
        ) = parser_state.close_open_blocks_fn(
            parser_state,
            until_this_index=last_list_index + 1,
            caller_can_handle_requeue=True,
        )
        if requeue_line_info and requeue_line_info.lines_to_requeue:
            LOGGER.debug(
                "__close_required_lists_after_start>>lines_to_requeue>>%s",
                ParserHelper.make_value_visible(requeue_line_info.lines_to_requeue),
            )
            LOGGER.debug(
                "__close_required_lists_after_start>>parser_state.original_line_to_parse>>%s",
                ParserHelper.make_value_visible(parser_state.original_line_to_parse),
            )
            LOGGER.debug(
                "__close_required_lists_after_start>>token_stack>>%s",
                ParserHelper.make_value_visible(parser_state.token_stack),
            )
            LOGGER.debug(
                "__close_required_lists_after_start>>token_document>>%s",
                ParserHelper.make_value_visible(parser_state.token_document),
            )
            assert not requeue_line_info.lines_to_requeue[0]
            requeue_line_info.lines_to_requeue[0] = parser_state.original_line_to_parse
            LOGGER.debug(
                "__close_required_lists_after_start>>lines_to_requeue>>%s",
                ParserHelper.make_value_visible(requeue_line_info.lines_to_requeue),
            )
            return None, None, requeue_line_info

        LOGGER.debug("old-stack>>%s<<", str(container_level_tokens))
        repeat_check = True
        emit_li = False
        while repeat_check:
            LOGGER.debug("start")
            repeat_check = False
            (
                do_not_emit,
                emit_li,
                extra_tokens,
                last_list_index,
            ) = ListBlockProcessor.__are_list_starts_equal(
                parser_state,
                last_list_index,
                new_stack,
                current_container_blocks,
            )
            LOGGER.debug("extra_tokens>>%s", str(extra_tokens))
            container_level_tokens.extend(extra_tokens)
            if do_not_emit:
                LOGGER.debug("post_list>>don't emit")
                (
                    did_find,
                    last_list_index,
                ) = LeafBlockProcessor.check_for_list_in_process(parser_state)
                LOGGER.debug(
                    "did_find>>%s--last_list_index--%s",
                    str(did_find),
                    str(last_list_index),
                )
                assert did_find
                LOGGER.debug(
                    "ARE-EQUAL>>stack>>%s>>new>>%s",
                    str(parser_state.token_stack[last_list_index]),
                    str(new_stack),
                )
                if (
                    parser_state.token_stack[last_list_index].type_name
                    == new_stack.type_name
                    or new_stack.start_index
                    > parser_state.token_stack[last_list_index].start_index
                ):
                    pass
                else:
                    repeat_check = True
            else:
                LOGGER.debug("post_list>>close open blocks and emit")
                close_tokens, _ = parser_state.close_open_blocks_fn(
                    parser_state, until_this_index=last_list_index, include_lists=True
                )
                assert close_tokens
                container_level_tokens.extend(close_tokens)

                (
                    did_find,
                    last_list_index,
                ) = LeafBlockProcessor.check_for_list_in_process(parser_state)
                LOGGER.debug(
                    "did_find>>%s--last_list_index--%s",
                    str(did_find),
                    str(last_list_index),
                )
                if did_find:
                    LOGGER.debug(
                        "ARE-EQUAL>>stack>>%s>>new>>%s",
                        str(parser_state.token_stack[last_list_index]),
                        str(new_stack),
                    )
                    if (
                        new_stack.indent_level
                        <= parser_state.token_stack[last_list_index].indent_level
                    ):
                        repeat_check = True
        return container_level_tokens, emit_li, None

    @staticmethod
    def __are_list_starts_equal(
        parser_state,
        last_list_index,
        new_stack,
        current_container_blocks,
    ):
        """
        Check to see if the list starts are equal, and hence a continuation of
        the current list.
        """

        balancing_tokens = []

        LOGGER.debug(
            "ARE-EQUAL>>stack>>%s>>new>>%s",
            str(parser_state.token_stack[last_list_index]),
            str(new_stack),
        )
        if parser_state.token_stack[last_list_index] == new_stack:
            balancing_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=last_list_index,
                include_block_quotes=True,
            )
            return True, True, balancing_tokens, last_list_index

        document_token_index = len(parser_state.token_document) - 1
        while document_token_index >= 0 and not (
            parser_state.token_document[document_token_index].is_any_list_token
        ):
            document_token_index -= 1
        assert document_token_index >= 0

        LOGGER.debug(
            "ARE-EQUAL>>Last_List_token=%s",
            str(parser_state.token_document[document_token_index]),
        )
        old_start_index = parser_state.token_document[document_token_index].indent_level

        old_last_marker_character = parser_state.token_stack[
            last_list_index
        ].list_character[-1]
        current_start_index = new_stack.ws_before_marker
        LOGGER.debug(
            "old>>%s>>%s",
            str(parser_state.token_stack[last_list_index].extra_data),
            old_last_marker_character,
        )
        LOGGER.debug(
            "new>>%s>>%s", str(new_stack.extra_data), new_stack.list_character[-1]
        )
        if (
            parser_state.token_stack[last_list_index].type_name == new_stack.type_name
            and old_last_marker_character == new_stack.list_character[-1]
        ):
            do_not_emit, emit_li = ListBlockProcessor.__process_eligible_list_start(
                parser_state,
                balancing_tokens,
                current_start_index,
                old_start_index,
                current_container_blocks,
            )
            return do_not_emit, emit_li, balancing_tokens, last_list_index

        LOGGER.debug("SUBLIST WITH DIFFERENT")
        LOGGER.debug("are_list_starts_equal>>ELIGIBLE!!!")
        LOGGER.debug(
            "are_list_starts_equal>>current_start_index>>%s>>old_start_index>>%s",
            str(current_start_index),
            str(old_start_index),
        )
        if current_start_index >= old_start_index:
            LOGGER.debug("are_list_starts_equal>>True")
            return True, False, balancing_tokens, last_list_index

        LOGGER.debug("are_list_starts_equal>>False")
        LOGGER.debug(">>%s", str(parser_state.token_stack))
        return False, False, balancing_tokens, last_list_index

    @staticmethod
    def __process_eligible_list_start(
        parser_state,
        balancing_tokens,
        current_start_index,
        old_start_index,
        current_container_blocks,
    ):
        LOGGER.debug("are_list_starts_equal>>ELIGIBLE!!!")
        LOGGER.debug(
            "are_list_starts_equal>>current_start_index>>%s>>old_start_index>>%s",
            str(current_start_index),
            str(old_start_index),
        )
        if current_start_index < old_start_index:

            LOGGER.debug("current_container_blocks>>%s", str(current_container_blocks))
            if len(current_container_blocks) > 1:
                LOGGER.debug(
                    "current_container_blocks-->%s", str(parser_state.token_stack)
                )
                last_stack_depth = parser_state.token_stack[-1].ws_before_marker
                while current_start_index < last_stack_depth:
                    last_stack_index = parser_state.token_stack.index(
                        parser_state.token_stack[-1]
                    )
                    close_tokens, _ = parser_state.close_open_blocks_fn(
                        parser_state,
                        until_this_index=last_stack_index,
                        include_lists=True,
                    )
                    assert close_tokens
                    balancing_tokens.extend(close_tokens)
                    LOGGER.debug("close_tokens>>%s", str(close_tokens))
                    last_stack_depth = parser_state.token_stack[-1].ws_before_marker

            return True, True

        LOGGER.debug("are_list_starts_equal>>True")
        return True, False

    @staticmethod
    def __adjust_line_for_list_in_process(
        line_to_parse,
        start_index,
        leading_space,
        leading_space_length,
        requested_list_indent,
    ):
        """
        Alter the current line to better represent the current level of lists.
        """
        remaining_indent = leading_space_length - requested_list_indent
        LOGGER.debug(
            "enough ws to continue; line(%s),start_index(%s),leading_space(%s)",
            line_to_parse,
            str(start_index),
            str(leading_space),
        )
        LOGGER.debug(
            "enough ws to continue; lsl(%s)-rsi(%s)=ri(%s)",
            str(leading_space_length),
            str(requested_list_indent),
            str(remaining_indent),
        )
        if ParserHelper.tab_character in leading_space:
            removed_whitespace = ParserHelper.tab_character
        else:
            removed_whitespace = leading_space[0:requested_list_indent]
        line_to_parse = (
            ParserHelper.repeat_string(ParserHelper.space_character, remaining_indent)
            + line_to_parse[start_index:]
        )
        return line_to_parse, removed_whitespace

    # pylint: disable=too-many-arguments
    @staticmethod
    def __check_for_list_closures(
        parser_state,
        line_to_parse,
        start_index,
        extracted_whitespace,
        ind,
        leading_space_length,
    ):
        """
        Check to see if the list in progress and the level of lists shown require
        the closing of some of the sublists.
        """
        container_level_tokens = []
        LOGGER.debug("ws(naa)>>line_to_parse>>%s<<", line_to_parse)
        LOGGER.debug("ws(naa)>>stack>>%s", str(parser_state.token_stack))
        LOGGER.debug("ws(naa)>>tokens>>%s", str(parser_state.token_document))

        is_leaf_block_start = LeafBlockProcessor.is_paragraph_ending_leaf_block_start(
            parser_state, line_to_parse, start_index, extracted_whitespace
        )
        if (
            not parser_state.token_stack[-1].is_paragraph or is_leaf_block_start
        ) and not parser_state.token_stack[-1].was_link_definition_started:
            LOGGER.debug("ws (normal and adjusted) not enough to continue")

            LOGGER.debug("lsl %s", str(leading_space_length))
            LOGGER.debug("lsl %s", str(parser_state.token_stack[ind]))
            search_index = ind
            LOGGER.debug(
                "lsl %s>%s",
                search_index,
                str(parser_state.token_stack[search_index - 1]),
            )
            while (
                parser_state.token_stack[search_index - 1].is_list
                and parser_state.token_stack[search_index - 1].indent_level
                > leading_space_length
            ):
                search_index -= 1
                LOGGER.debug(
                    "lsl %s>%s",
                    search_index,
                    str(parser_state.token_stack[search_index]),
                )

            LOGGER.debug("lsl %s", str(parser_state.token_stack[search_index]))

            container_level_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state, until_this_index=search_index, include_lists=True
            )
            LOGGER.debug("container_level_tokens>%s>", str(container_level_tokens))
        else:
            LOGGER.debug("ws (normal and adjusted) continue")
        return container_level_tokens

    # pylint: enable=too-many-arguments
