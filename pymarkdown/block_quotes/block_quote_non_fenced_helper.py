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
from pymarkdown.tokens.stack_token import (
    BlockQuoteStackToken,
    ListStackToken,
    StackToken,
)

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
        extracted_whitespace: Optional[str],
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
            extra_consumed_whitespace,
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
        ) = BlockQuoteNonFencedHelper.__handle_non_fenced_code_section_no_requeue(
            parser_state,
            position_marker,
            line_to_parse,
            start_index,
            removed_text,
            container_start_bq_count,
            block_quote_data,
            original_start_index,
            extra_consumed_whitespace,
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
            None,
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
        extra_consumed_whitespace: Optional[int],
        container_level_tokens: List[MarkdownToken],
        original_line: str,
    ) -> Tuple[str, int, str, bool, List[MarkdownToken]]:
        (
            line_to_parse,
            stack_index,
        ) = (
            line_to_parse[start_index:],
            parser_state.find_last_block_quote_on_stack(),
        )
        POGGER.debug("==REM[$],LTP[$]", removed_text, line_to_parse)

        assert stack_index != -1
        found_bq_stack_token = cast(
            BlockQuoteStackToken, parser_state.token_stack[stack_index]
        )
        assert found_bq_stack_token

        BlockQuoteNonFencedHelper.__do_block_quote_leading_spaces_adjustments(
            parser_state,
            stack_index,
            container_start_bq_count,
            block_quote_data,
            removed_text,
            found_bq_stack_token,
            removed_text,
            original_start_index,
            extra_consumed_whitespace,
            container_level_tokens,
            original_line,
        )
        POGGER.debug("text_removed_by_container=[$]", removed_text)
        POGGER.debug("removed_text=[$]", removed_text)
        if line_to_parse.strip(Constants.ascii_whitespace):
            return (
                line_to_parse,
                start_index,
                removed_text,
                False,
                [],
            )
        did_blank, leaf_tokens = BlockQuoteNonFencedHelper.__handle_normal_blank_line(
            parser_state,
            block_quote_data,
            position_marker,
            removed_text,
            line_to_parse,
        )
        return (
            line_to_parse,
            start_index,
            removed_text,
            did_blank,
            leaf_tokens,
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
        extra_consumed_whitespace: Optional[int],
        container_level_tokens: List[MarkdownToken],
        original_line: str,
    ) -> None:
        POGGER.debug("__hbqs>>removed_text>>:$:<", removed_text)
        POGGER.debug("__hbqs>>container_start_bq_count>>$", container_start_bq_count)
        POGGER.debug("__hbqs>>original_start_index>>$", original_start_index)
        POGGER.debug("token_stack--$", parser_state.token_stack)
        original_start_index = BlockQuoteNonFencedHelper.__block_quote_start_adjust(
            parser_state, original_start_index, container_level_tokens
        )
        original_removed_text = removed_text
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
        special_case, adjusted_removed_text = BlockQuoteNonFencedHelper.__adjust_2(
            parser_state,
            found_bq_stack_token,
            original_removed_text,
            adjusted_removed_text,
            extra_consumed_whitespace,
            tabbed_removed_text,
        )
        POGGER.debug("dbqlsa>>adjusted_removed_text>>:$:<<", adjusted_removed_text)
        POGGER.debug("dbqlsa>>special_case>>$", special_case)

        BlockQuoteNonFencedHelper.__do_block_quote_leading_spaces_adjustments_adjust_bleading(
            found_bq_stack_token,
            tabbed_removed_text,
            adjusted_removed_text,
            special_case,
        )

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

        assert leaf_tokens is not None
        return True, leaf_tokens

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
            assert count_of_actual_starts != block_quote_data.current_count
            block_quote_token = cast(
                BlockQuoteMarkdownToken, block_stack_token.matching_markdown_token
            )
            adj_leading_spaces = block_quote_token.bleading_spaces
            assert adj_leading_spaces is not None
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
            assert detabified_original_line.startswith(adjusted_removed_text)
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
    def __do_block_quote_leading_spaces_adjustments_adjust_bleading(
        found_bq_stack_token: BlockQuoteStackToken,
        tabbed_removed_text: Optional[str],
        adjusted_removed_text: str,
        special_case: bool,
    ) -> None:
        assert found_bq_stack_token.matching_markdown_token is not None
        block_quote_token = cast(
            BlockQuoteMarkdownToken, found_bq_stack_token.matching_markdown_token
        )
        POGGER.debug("dbqlsa>>last_block_token>>$", block_quote_token)
        POGGER.debug(
            "dbqlsa>>leading_text_index>>$", block_quote_token.leading_text_index
        )
        POGGER.debug("dbqlsa>>bq>>$", block_quote_token)
        POGGER.debug("dbqlsa>>tabbed_removed_text>>$", tabbed_removed_text)

        block_quote_token.add_bleading_spaces(
            adjusted_removed_text,
            special_case,
            tabbed_removed_text,
        )
        block_quote_token.leading_text_index += 1
        POGGER.debug("dbqlsa>>last_block_token>>$", block_quote_token)
        POGGER.debug(
            "dbqlsa>>leading_text_index>>$", block_quote_token.leading_text_index
        )

        POGGER.debug("__hbqs>>bq>>$", block_quote_token)

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_2(
        parser_state: ParserState,
        found_bq_stack_token: StackToken,
        original_removed_text: str,
        adjusted_removed_text: str,
        extra_consumed_whitespace: Optional[int],
        tabbed_removed_text: Optional[str],
    ) -> Tuple[bool, str]:
        POGGER.debug("original_removed_text>>:$:", original_removed_text)
        POGGER.debug("extra_consumed_whitespace>>:$:", extra_consumed_whitespace)
        POGGER.debug("parser_state.block_copy>>$", parser_state.block_copy)
        special_case = False
        olad = adjusted_removed_text
        if parser_state.block_copy and found_bq_stack_token:
            POGGER.debug("parser_state.block_copy>>search")
            if original_token := BlockQuoteNonFencedHelper.__find_original_token(
                parser_state, found_bq_stack_token
            ):
                original_block_quote_token = cast(
                    BlockQuoteMarkdownToken, original_token
                )
                assert found_bq_stack_token.matching_markdown_token is not None
                POGGER.debug("original_token>>$", original_block_quote_token)
                assert original_block_quote_token.bleading_spaces is not None
                POGGER.debug(
                    "original_token.bleading_spaces>>:$:<<",
                    original_block_quote_token.bleading_spaces,
                )
                block_quote_markdown_token = cast(
                    BlockQuoteMarkdownToken,
                    found_bq_stack_token.matching_markdown_token,
                )
                current_leading_spaces = block_quote_markdown_token.bleading_spaces
                assert current_leading_spaces is not None
                POGGER.debug("found_bq_stack_token.ls>>:$:<<", current_leading_spaces)
                assert current_leading_spaces.startswith(
                    original_block_quote_token.bleading_spaces
                )
                (
                    special_case,
                    adjusted_removed_text,
                ) = BlockQuoteNonFencedHelper.__adjust_2_fix_leading_spaces(
                    special_case,
                    adjusted_removed_text,
                    original_removed_text,
                    original_block_quote_token,
                    current_leading_spaces,
                    extra_consumed_whitespace,
                )

        if tabbed_removed_text:
            assert olad == adjusted_removed_text
        return special_case, adjusted_removed_text

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_2_fix_leading_spaces(
        special_case: bool,
        adjusted_removed_text: str,
        original_removed_text: str,
        original_block_quote_token: BlockQuoteMarkdownToken,
        current_leading_spaces: str,
        extra_consumed_whitespace: Optional[int],
    ) -> Tuple[bool, str]:
        POGGER.debug("original_removed_text>>:$:", original_removed_text)
        POGGER.debug("adjusted_removed_text>>:$:", adjusted_removed_text)
        assert original_block_quote_token.bleading_spaces is not None
        if len(current_leading_spaces) > len(
            original_block_quote_token.bleading_spaces
        ):
            current_leading_spaces = current_leading_spaces[
                len(original_block_quote_token.bleading_spaces) :
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


# pylint: enable=too-few-public-methods
