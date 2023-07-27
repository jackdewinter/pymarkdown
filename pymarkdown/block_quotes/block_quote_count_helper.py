"""
Module to provide processing for the block quotes.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.requeue_line_info import RequeueLineInfo
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    HtmlBlockStackToken,
    IndentedCodeBlockStackToken,
    LinkDefinitionStackToken,
    ListStackToken,
    ParagraphStackToken,
)
from pymarkdown.tab_helper import TabHelper
from pymarkdown.tokens.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ListStartMarkdownToken,
)

POGGER = ParserLogger(logging.getLogger(__name__))


class BlockQuoteCountHelper:
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
        return TabHelper.is_length_less_than_or_equal_to(
            extracted_whitespace if adj_ws is None else adj_ws, 3
        ) and ParserHelper.is_character_at_index(
            line_to_parse, start_index, BlockQuoteCountHelper.__block_quote_character
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def count_block_quote_starts(
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

        (
            last_block_quote_index,
            avoid_block_starts,
            adjusted_line,
        ) = (
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
                (
                    adjusted_line,
                    start_index,
                ) = BlockQuoteCountHelper.__handle_bq_whitespace(
                    adjusted_line, start_index
                )

                (
                    continue_processing,
                    avoid_block_starts,
                    start_index,
                    adjusted_line,
                    last_block_quote_index,
                    current_count,
                ) = BlockQuoteCountHelper.__should_continue_processing(
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
                    BlockQuoteCountHelper.__block_quote_character,
                )
                POGGER.debug("avoid_block_starts=$", avoid_block_starts)
                continue_processing = False
            else:
                assert current_count > stack_count
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
                POGGER.debug("out of stack")
            elif start_index == len(adjusted_line):
                POGGER.debug("ran out of line")
            elif ParserHelper.is_character_at_index_not(
                adjusted_line,
                start_index,
                BlockQuoteCountHelper.__block_quote_character,
            ):
                (
                    continue_processing,
                    start_index,
                ) = BlockQuoteCountHelper.__is_special_double_block_case(
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
            final_stack_index = BlockQuoteCountHelper.__find_double_block_case_index(
                parser_state, current_count
            )
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
                    BlockQuoteCountHelper.__block_quote_character, start_index
                )
                POGGER.debug("+1>>next_bq_index:$:", next_bq_index)
                if next_bq_index != -1 and (next_bq_index - start_index) <= 3:
                    continue_processing, start_index = True, next_bq_index
        return continue_processing, start_index

    @staticmethod
    def __find_double_block_case_index(
        parser_state: ParserState, current_count: int
    ) -> int:
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
        return final_stack_index

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
                == BlockQuoteCountHelper.__block_quote_character
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
        skip = BlockQuoteCountHelper.__block_list_block_kludge(
            parser_state,
            position_marker,
            stack_count,
            block_quote_data,
        )
        if not skip:
            BlockQuoteCountHelper.decrease_stack_to_level(
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
    def decrease_stack_to_level(
        parser_state: ParserState,
        current_count: int,
        stack_count: int,
        container_level_tokens: List[MarkdownToken],
    ) -> BlockQuoteData:
        """
        Decrease the stack to match the block quote level.
        """
        while current_count < stack_count:
            POGGER.debug(
                "decreasing block quotes by one>>",
            )
            stack_count -= 1
            (
                new_tokens,
                _,
            ) = parser_state.close_open_blocks_fn(
                parser_state,
                include_block_quotes=True,
                until_this_index=len(parser_state.token_stack) - 1,
                was_forced=True,
            )
            container_level_tokens.extend(new_tokens)
        return BlockQuoteData(current_count, stack_count)

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

    # pylint: disable=too-many-arguments
    @staticmethod
    def ensure_stack_at_level(
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
        ) = BlockQuoteCountHelper.__does_require_increase_or_descrease(
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
            ) = BlockQuoteCountHelper.__calculate_stack_hard_limit(
                parser_state,
                position_marker,
                False,
                stack_increase_needed,
                stack_decrease_needed,
                block_quote_data,
            )
            POGGER.debug("force_list_continuation=$", force_list_continuation)
            POGGER.debug("esal>>__calculate_stack_hard_limit>>$", stack_hard_limit)

            BlockQuoteCountHelper.__decrease_stack(
                parser_state,
                container_level_tokens,
                original_start_index,
                stack_hard_limit,
            )

            (
                extracted_whitespace,
                original_start_index,
            ) = BlockQuoteCountHelper.__increase_stack(
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
            ) = BlockQuoteCountHelper.__calculate_stack_hard_limit(
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
            (
                stack_hard_limit,
                extra_consumed_whitespace,
                force_list_continuation,
            ) = BlockQuoteCountHelper.__calculate_limit_and_continuation(
                parser_state,
                position_marker,
                adjust_current_block_quote,
                last_bq_index,
                stack_increase_needed,
                stack_decrease_needed,
                block_quote_data,
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
    def __calculate_limit_and_continuation(
        parser_state: ParserState,
        position_marker: PositionMarker,
        adjust_current_block_quote: bool,
        last_bq_index: int,
        stack_increase_needed: bool,
        stack_decrease_needed: bool,
        block_quote_data: BlockQuoteData,
    ) -> Tuple[Optional[int], Optional[int], bool]:
        (
            length_of_available_whitespace,
            _,
        ) = ParserHelper.extract_spaces(position_marker.text_to_parse, 0)
        POGGER.debug("len(ws)>>:$:", length_of_available_whitespace)

        assert length_of_available_whitespace is not None
        (
            stack_hard_limit,
            extra_consumed_whitespace,
        ) = BlockQuoteCountHelper.__calculate_stack_hard_limit_if_eligible(
            parser_state,
            position_marker,
            length_of_available_whitespace,
            adjust_current_block_quote,
            last_bq_index,
        )
        POGGER.debug(f">>>>>stack_increase_needed:{stack_increase_needed}")
        POGGER.debug(f">>>>>stack_decrease_needed:{stack_decrease_needed}")
        POGGER.debug(f">>>>>adjust_current_block_quote:{adjust_current_block_quote}")
        POGGER.debug(
            ">>block_quote_data.current_count>>$",
            block_quote_data.current_count,
        )
        POGGER.debug(">>block_quote_data.stack_count>>$", block_quote_data.stack_count)
        force_list_continuation = (
            extra_consumed_whitespace is None
            and not stack_increase_needed
            and not stack_decrease_needed
            and adjust_current_block_quote
        )
        if force_list_continuation:
            POGGER.debug(f">>>>>last_bq_index:{last_bq_index}")
            POGGER.debug(f">>>>>parser_state.token_stack:{parser_state.token_stack}")
            POGGER.debug(
                f">>>>>len(parser_state.token_stack):{len(parser_state.token_stack)}"
            )
            force_list_continuation = (
                last_bq_index + 1 < len(parser_state.token_stack)
                and parser_state.token_stack[last_bq_index + 1].is_list
                and block_quote_data.current_count != block_quote_data.stack_count
            )
        return stack_hard_limit, extra_consumed_whitespace, force_list_continuation

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
            ) = BlockQuoteCountHelper.__calculate_eligible_stack_hard_limit(
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
            block_token.add_bleading_spaces(
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
