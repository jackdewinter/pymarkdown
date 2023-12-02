"""
Module to provide processing for the atx heading leaf blocks.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_helper import ContainerHelper
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.leaf_blocks.leaf_block_helper import LeafBlockHelper
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import ListStackToken, StackToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class AtxLeafBlockProcessor:
    """
    Class to provide processing for the atx heading leaf blocks.
    """

    __atx_character = "#"

    @staticmethod
    def is_atx_heading(
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        skip_whitespace_check: bool = False,
    ) -> Tuple[bool, Optional[int], Optional[int], Optional[str]]:
        """
        Determine whether or not an ATX Heading is about to start.
        """

        assert extracted_whitespace is not None
        if (
            TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            or skip_whitespace_check
        ) and ParserHelper.is_character_at_index(
            line_to_parse,
            start_index,
            AtxLeafBlockProcessor.__atx_character,
        ):
            hash_count, new_index = ParserHelper.collect_while_character(
                line_to_parse,
                start_index,
                AtxLeafBlockProcessor.__atx_character,
            )

            assert new_index is not None
            non_whitespace_index, _ = ParserHelper.collect_while_spaces(
                line_to_parse, new_index
            )
            extracted_whitespace_at_start = line_to_parse[
                new_index:non_whitespace_index
            ]

            assert hash_count is not None
            if hash_count <= 6 and (
                extracted_whitespace_at_start
                or non_whitespace_index == len(line_to_parse)
            ):
                return (
                    True,
                    non_whitespace_index,
                    hash_count,
                    extracted_whitespace_at_start,
                )
        return False, None, None, None

    @staticmethod
    def parse_atx_headings(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        block_quote_data: BlockQuoteData,
        original_line: str,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of an atx heading.
        """

        (
            heading_found,
            non_whitespace_index,
            hash_count,
            extracted_whitespace_at_start,
        ) = AtxLeafBlockProcessor.is_atx_heading(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
        )
        if not heading_found:
            POGGER.debug(
                "parse_atx_headings>>not eligible",
            )
            return []

        assert non_whitespace_index is not None
        return AtxLeafBlockProcessor.__parse_atx_heading_found(
            parser_state,
            position_marker,
            original_line,
            hash_count,
            non_whitespace_index,
            block_quote_data,
            extracted_whitespace_at_start,
            extracted_whitespace,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __parse_atx_heading_found(
        parser_state: ParserState,
        position_marker: PositionMarker,
        original_line: str,
        hash_count: Optional[int],
        non_whitespace_index: int,
        block_quote_data: BlockQuoteData,
        extracted_whitespace_at_start: Optional[str],
        extracted_whitespace: Optional[str],
    ) -> List[MarkdownToken]:
        assert extracted_whitespace_at_start is not None
        POGGER.debug(
            "parse_atx_headings>>start",
        )

        (
            old_top_of_stack,
            remaining_line,
            remove_trailing_count,
            extracted_whitespace_before_end,
            extracted_whitespace_at_end,
            new_tokens,
            extracted_whitespace_at_start,
            extracted_whitespace,
            delay_tab_match,
        ) = AtxLeafBlockProcessor.__prepare_for_create_atx_heading(
            parser_state,
            position_marker,
            position_marker.text_to_parse[non_whitespace_index:],
            original_line,
            extracted_whitespace_at_start,
            extracted_whitespace,
            hash_count,
            block_quote_data,
        )
        assert hash_count is not None
        assert extracted_whitespace is not None

        POGGER.debug("extracted_whitespace>>$<<", extracted_whitespace)
        POGGER.debug("removed_chars_at_start>>$", position_marker.index_indent)
        POGGER.debug("delay_tab_match>>$", delay_tab_match)
        if delay_tab_match:
            extracted_whitespace = (
                AtxLeafBlockProcessor.__parse_atx_headings_delay_tab_match(
                    position_marker, original_line
                )
            )

        AtxLeafBlockProcessor.__parse_atx_heading_add_tokens(
            parser_state,
            position_marker,
            new_tokens,
            hash_count,
            remove_trailing_count,
            extracted_whitespace,
            old_top_of_stack,
            delay_tab_match,
            remaining_line,
            extracted_whitespace_at_start,
            extracted_whitespace_at_end,
            extracted_whitespace_before_end,
        )
        return new_tokens

    # pylint: enable=too-many-arguments
    # pylint: disable=too-many-arguments
    @staticmethod
    def __parse_atx_heading_add_tokens(
        parser_state: ParserState,
        position_marker: PositionMarker,
        new_tokens: List[MarkdownToken],
        hash_count: int,
        remove_trailing_count: int,
        extracted_whitespace: str,
        old_top_of_stack: StackToken,
        delay_tab_match: bool,
        remaining_line: str,
        extracted_whitespace_at_start: str,
        extracted_whitespace_at_end: str,
        extracted_whitespace_before_end: str,
    ) -> List[MarkdownToken]:
        start_token = AtxHeadingMarkdownToken(
            hash_count,
            remove_trailing_count,
            extracted_whitespace,
            position_marker,
        )
        new_tokens.append(start_token)

        LeafBlockHelper.correct_for_leaf_block_start_in_list(
            parser_state,
            position_marker.index_indent,
            old_top_of_stack,
            new_tokens,
            was_token_already_added_to_stack=False,
            delay_tab_match=delay_tab_match,
        )

        new_tokens.append(
            TextMarkdownToken(
                remaining_line,
                extracted_whitespace_at_start,
                position_marker=position_marker,
            )
        )
        end_token = start_token.generate_close_markdown_token_from_markdown_token(
            extracted_whitespace_at_end, extracted_whitespace_before_end
        )
        new_tokens.append(end_token)
        return new_tokens

    # pylint: enable=too-many-arguments

    @staticmethod
    def __parse_atx_headings_delay_tab_match(
        position_marker: PositionMarker, original_line: str
    ) -> str:
        _, ex_ws = ParserHelper.extract_spaces(original_line, 0)
        POGGER.debug("ex_ws>>$<<", ex_ws)
        assert ex_ws is not None

        loop_index = 0
        rep = True
        while rep and loop_index < len(ex_ws):
            loop_index += 1
            ex_ws_to_index = ex_ws[:loop_index]
            POGGER.debug("ex_ws_to_index>>$<<", ex_ws_to_index)
            ex_ws_to_index_untabbified = TabHelper.detabify_string(ex_ws_to_index)
            POGGER.debug("ex_ws_to_index_untabbified>>$<<", ex_ws_to_index_untabbified)
            POGGER.debug(
                "removed_chars=$ < len(ex_ws_to_index_untabbified)=$",
                position_marker.index_indent,
                len(ex_ws_to_index_untabbified),
            )
            rep = position_marker.index_indent > len(ex_ws_to_index_untabbified)

        POGGER.debug(
            "removed_chars=$ == len(ex_ws_to_index_untabbified)=$",
            position_marker.index_indent,
            len(ex_ws_to_index_untabbified),
        )
        extracted_whitespace = ex_ws[loop_index - 1 :]
        POGGER.debug("extracted_whitespace>>$<<", extracted_whitespace)
        return extracted_whitespace

    # pylint: disable=too-many-arguments
    @staticmethod
    def __prepare_for_create_atx_heading_with_tab(
        parser_state: ParserState,
        original_line: str,
        remaining_line: str,
        extracted_whitespace_at_start: str,
        extracted_whitespace: str,
        hash_count: int,
    ) -> Tuple[str, str, str, bool]:
        POGGER.debug(">>extracted_whitespace>:$:<", extracted_whitespace)
        POGGER.debug(
            ">>extracted_whitespace_at_start>:$:<", extracted_whitespace_at_start
        )
        reconstructed_line = (
            extracted_whitespace
            + ParserHelper.repeat_string("#", hash_count)
            + extracted_whitespace_at_start
            + remaining_line
        )

        stack_index = len(parser_state.token_stack) - 1
        while (
            stack_index != 0
            and not parser_state.token_stack[stack_index].is_list
            and not parser_state.token_stack[stack_index].is_block_quote
        ):
            stack_index -= 1
        leading_spaces = None
        if parser_state.token_stack[stack_index].is_list:
            POGGER.debug(
                ">>parser_state.token_stack[stack_index]>:$:<",
                parser_state.token_stack[stack_index],
            )
            POGGER.debug(
                ">>parser_state.token_stack[stack_index].mdt>:$:<",
                parser_state.token_stack[stack_index].matching_markdown_token,
            )
            list_markdown_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[stack_index].matching_markdown_token,
            )
            leading_spaces = list_markdown_token.leading_spaces

            # TODO This needs to be fixed at a higher level, should not be needed
            # if not leading_spaces and parser_state.token_stack[stack_index].is_ordered_list:
            #     leading_spaces = list_markdown_token.extracted_whitespace
            #     assert False
            POGGER.debug(">>leading_spaces>:$:<", leading_spaces)

        POGGER.debug(">>reconstructed_line>:$:<", reconstructed_line)
        _, adj_original_index, split_tab = TabHelper.find_tabified_string(
            original_line,
            reconstructed_line,
            use_proper_traverse=True,
            reconstruct_prefix=leading_spaces,
        )
        POGGER.debug(">>adj_original_index>:$:<", adj_original_index)

        after_pre_hash_whitespace_index, ex_whitespace = ParserHelper.extract_spaces(
            original_line, adj_original_index
        )
        POGGER.debug(
            ">>after_pre_hash_whitespace_index>:$:<", after_pre_hash_whitespace_index
        )
        POGGER.debug(">>ex_whitespace>:$:<", ex_whitespace)
        assert ex_whitespace is not None
        assert after_pre_hash_whitespace_index is not None
        extracted_whitespace = ex_whitespace

        after_post_hash_whitespace_index, ex_whitespace = ParserHelper.extract_spaces(
            original_line, after_pre_hash_whitespace_index + hash_count
        )
        assert ex_whitespace is not None
        assert after_post_hash_whitespace_index is not None
        extracted_whitespace_at_start = ex_whitespace

        remaining_line = original_line[after_post_hash_whitespace_index:]
        return (
            remaining_line,
            extracted_whitespace_at_start,
            extracted_whitespace,
            split_tab,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __prepare_for_create_atx_heading(
        parser_state: ParserState,
        position_marker: PositionMarker,
        remaining_line: str,
        original_line: str,
        extracted_whitespace_at_start: str,
        extracted_whitespace: Optional[str],
        hash_count: Optional[int],
        block_quote_data: BlockQuoteData,
    ) -> Tuple[
        StackToken, str, int, str, str, List[MarkdownToken], str, Optional[str], bool
    ]:
        (
            old_top_of_stack,
            remove_trailing_count,
        ) = (
            parser_state.token_stack[-1],
            0,
        )

        eligble_for_tab_match_delay = (
            AtxLeafBlockProcessor.__determine_eligble_for_tab_match_delay(
                parser_state, position_marker, old_top_of_stack
            )
        )

        POGGER.debug("remaining_line>:$:<", remaining_line)
        POGGER.debug("original_line>:$:<", original_line)
        if (
            ParserHelper.tab_character in original_line
            and not eligble_for_tab_match_delay
        ):
            assert extracted_whitespace is not None
            POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
            assert hash_count is not None
            (
                remaining_line,
                extracted_whitespace_at_start,
                extracted_whitespace,
                split_tab,
            ) = AtxLeafBlockProcessor.__prepare_for_create_atx_heading_with_tab(
                parser_state,
                original_line,
                remaining_line,
                extracted_whitespace_at_start,
                extracted_whitespace,
                hash_count,
            )
            POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        else:
            split_tab = False
        POGGER.debug("split_tab>:$:<", split_tab)

        new_tokens, _ = parser_state.close_open_blocks_fn(parser_state)
        POGGER.debug("new_tokens>:$:<", new_tokens)
        if ContainerHelper.reduce_containers_if_required(
            parser_state, block_quote_data, new_tokens, split_tab, extracted_whitespace
        ):
            POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
            extracted_whitespace = TabHelper.adjust_block_quote_indent_for_tab(
                parser_state, extracted_whitespace
            )
            POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)

        (
            extracted_whitespace_at_end,
            extracted_whitespace_before_end,
            remaining_line,
            remove_trailing_count,
        ) = AtxLeafBlockProcessor.__prepare_for_create_atx_heading_adjust(
            remaining_line, remove_trailing_count
        )

        return (
            old_top_of_stack,
            remaining_line,
            remove_trailing_count,
            extracted_whitespace_before_end,
            extracted_whitespace_at_end,
            new_tokens,
            extracted_whitespace_at_start,
            extracted_whitespace,
            ParserHelper.tab_character in original_line and eligble_for_tab_match_delay,
        )

    # pylint: enable=too-many-arguments
    @staticmethod
    def __determine_eligble_for_tab_match_delay(
        parser_state: ParserState,
        position_marker: PositionMarker,
        old_top_of_stack: StackToken,
    ) -> bool:
        eligble_for_tab_match_delay = False
        keep_going = len(parser_state.token_stack) >= 2
        if keep_going:
            keep_going = False
            POGGER.debug("old_top_of_stack>:$:<", old_top_of_stack)
            POGGER.debug(
                "parser_state.token_stack[-1]>:$:<", parser_state.token_stack[-1]
            )
            POGGER.debug(
                "parser_state.token_stack[-2]>:$:<", parser_state.token_stack[-2]
            )
            if old_top_of_stack.is_paragraph:
                possible_list_index = (
                    -2 if parser_state.token_stack[-1].is_paragraph else -1
                )
                if parser_state.token_stack[possible_list_index].is_list:
                    POGGER.debug("1!!!!!")
                    keep_going = True
        if keep_going:
            POGGER.debug("2!!!!!")
            assert parser_state.token_stack[possible_list_index].is_list
            list_stack_token = cast(
                ListStackToken, parser_state.token_stack[possible_list_index]
            )

            removed_chars_at_start = position_marker.index_indent
            POGGER.debug(">>removed_chars_at_start>>$>>", removed_chars_at_start)
            POGGER.debug(">>stack indent>>$>>", list_stack_token.indent_level)
            if removed_chars_at_start < list_stack_token.indent_level:
                eligble_for_tab_match_delay = True
                POGGER.debug("3!!!!!")
        return eligble_for_tab_match_delay

    @staticmethod
    def __prepare_for_create_atx_heading_adjust(
        remaining_line: str, remove_trailing_count: int
    ) -> Tuple[str, str, str, int]:
        extracted_whitespace_before_end = ""
        (
            end_index,
            extracted_whitespace_at_end,
        ) = ParserHelper.extract_spaces_from_end(remaining_line)
        while (
            end_index > 0
            and remaining_line[end_index - 1] == AtxLeafBlockProcessor.__atx_character
        ):
            end_index -= 1
            remove_trailing_count += 1
        if remove_trailing_count:
            if end_index > 0:
                if ParserHelper.is_character_at_index_whitespace(
                    remaining_line, end_index - 1
                ):
                    remaining_line = remaining_line[:end_index]
                    (
                        _,
                        new_non_whitespace_index,
                    ) = ParserHelper.collect_backwards_while_spaces(
                        remaining_line, len(remaining_line) - 1
                    )
                    assert new_non_whitespace_index is not None
                    end_index = new_non_whitespace_index
                    extracted_whitespace_before_end = remaining_line[end_index:]
                    remaining_line = remaining_line[:end_index]
                else:
                    extracted_whitespace_at_end, remove_trailing_count = "", 0
            else:
                remaining_line = ""
        else:
            extracted_whitespace_at_end = remaining_line[end_index:]
            remaining_line = remaining_line[:end_index]
        return (
            extracted_whitespace_at_end,
            extracted_whitespace_before_end,
            remaining_line,
            remove_trailing_count,
        )
