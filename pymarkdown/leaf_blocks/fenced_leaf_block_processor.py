"""
Module to provide processing for the fenced leaf blocks.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quote_data import BlockQuoteData
from pymarkdown.constants import Constants
from pymarkdown.container_blocks.container_helper import ContainerHelper
from pymarkdown.inline.inline_backslash_helper import InlineBackslashHelper
from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_blocks.leaf_block_helper import LeafBlockHelper
from pymarkdown.leaf_markdown_token import FencedCodeBlockMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.stack_token import (
    FencedCodeBlockStackToken,
    ParagraphStackToken,
    StackToken,
)
from pymarkdown.tab_helper import TabHelper

POGGER = ParserLogger(logging.getLogger(__name__))


class FencedLeafBlockProcessor:
    """
    Class to provide processing for the fenced leaf blocks.
    """

    __fenced_start_tilde = "~"
    __fenced_start_backtick = "`"
    __fenced_code_block_start_characters = (
        f"{__fenced_start_tilde}{__fenced_start_backtick}"
    )

    @staticmethod
    def is_fenced_code_block(
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        skip_whitespace_check: bool = False,
    ) -> Tuple[bool, Optional[int], Optional[int], Optional[int], Optional[int]]:
        """
        Determine if we have the start of a fenced code block.
        """

        assert extracted_whitespace is not None
        after_fence_index: Optional[int] = None
        if (
            skip_whitespace_check
            or TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse,
            start_index,
            FencedLeafBlockProcessor.__fenced_code_block_start_characters,
        ):
            POGGER.debug("ifcb:collected_count>:$:<$<<", line_to_parse, start_index)
            collected_count, new_index = ParserHelper.collect_while_character(
                line_to_parse, start_index, line_to_parse[start_index]
            )
            POGGER.debug(
                "ifcb:collected_count:$, new_index:$", collected_count, new_index
            )
            assert collected_count is not None
            assert new_index is not None
            after_fence_index = new_index
            (
                non_whitespace_index,
                _,
            ) = ParserHelper.extract_ascii_whitespace(line_to_parse, new_index)

            if collected_count >= 3:
                POGGER.debug("ifcb:True")
                POGGER.debug("ifcb:collected_count=$", collected_count)
                POGGER.debug("ifcb:non_whitespace_index=$", non_whitespace_index)
                POGGER.debug("ifcb:after_fence_index=$", after_fence_index)
                return (
                    True,
                    non_whitespace_index,
                    after_fence_index,
                    collected_count,
                    new_index,
                )
        return False, None, None, None, None

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_fenced_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        original_line: str,
        detabified_original_start_index: int,
        block_quote_data: BlockQuoteData,
    ) -> Tuple[List[MarkdownToken], Optional[str]]:
        """
        Handle the parsing of a fenced code block
        """

        POGGER.debug(
            "line>>$>>index>>$>>",
            position_marker.text_to_parse,
            position_marker.index_number,
        )
        new_tokens: List[MarkdownToken] = []
        (
            is_fence_start,
            non_whitespace_index,
            after_fence_index,
            collected_count,
            new_index,
        ) = FencedLeafBlockProcessor.is_fenced_code_block(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
        )
        if is_fence_start and not parser_state.token_stack[-1].is_html_block:
            POGGER.debug("parse_fenced_code_block:fenced")
            assert collected_count is not None
            assert non_whitespace_index is not None
            assert after_fence_index is not None
            if parser_state.token_stack[-1].is_fenced_code_block:
                POGGER.debug("parse_fenced_code_block:check fence end")
                FencedLeafBlockProcessor.__check_for_fenced_end(
                    parser_state,
                    position_marker,
                    collected_count,
                    extracted_whitespace,
                    new_tokens,
                    after_fence_index,
                    original_line,
                    detabified_original_start_index,
                )
            else:
                POGGER.debug("parse_fenced_code_block:check fence start")
                assert new_index is not None
                new_tokens = FencedLeafBlockProcessor.__process_fenced_start(
                    parser_state,
                    position_marker,
                    non_whitespace_index,
                    collected_count,
                    extracted_whitespace,
                    original_line,
                    new_index,
                    block_quote_data,
                    after_fence_index,
                )
        elif parser_state.token_stack[-1].is_fenced_code_block:
            POGGER.debug("parse_fenced_code_block:already in")
            extracted_whitespace = (
                FencedLeafBlockProcessor.__parse_fenced_code_block_already_in(
                    parser_state,
                    extracted_whitespace,
                    original_line,
                    position_marker.text_to_parse,
                )
            )
        return new_tokens, extracted_whitespace

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __check_for_fenced_end(
        parser_state: ParserState,
        position_marker: PositionMarker,
        collected_count: int,
        extracted_whitespace: Optional[str],
        new_tokens: List[MarkdownToken],
        after_fence_index: int,
        original_line: str,
        detabified_original_start_index: int,
    ) -> None:
        # POGGER.debug("pfcb->end")
        # POGGER.debug("extracted_whitespace:$:", extracted_whitespace)
        # POGGER.debug("position_marker.text_to_parse:$:", position_marker.text_to_parse)
        # POGGER.debug(
        #     "len(position_marker.text_to_parse):$:", len(position_marker.text_to_parse)
        # )
        # POGGER.debug("after_fence_index:$:", after_fence_index)
        # POGGER.debug(
        #     "detabified_original_start_index:$:", detabified_original_start_index
        # )

        # POGGER.debug("original_line:$:", original_line)
        only_spaces_after_fence = True
        split_tab = False
        if ParserHelper.tab_character in original_line:
            (
                after_fence_index,
                only_spaces_after_fence,
                extracted_whitespace,
                split_tab,
            ) = FencedLeafBlockProcessor.__check_for_fenced_end_with_tab(
                original_line,
                detabified_original_start_index,
                collected_count,
                extracted_whitespace,
            )

        after_fence_and_spaces_index, extracted_spaces = ParserHelper.extract_spaces(
            position_marker.text_to_parse, after_fence_index
        )
        assert after_fence_and_spaces_index is not None
        # POGGER.debug("after_fence_and_spaces_index:$:", after_fence_and_spaces_index)

        fenced_token = cast(FencedCodeBlockStackToken, parser_state.token_stack[-1])
        # POGGER.debug("fenced_token.code_fence_character:$:", fenced_token.code_fence_character)
        # POGGER.debug("position_marker.text_to_parse[position_marker.index_number]:$:", position_marker.text_to_parse[position_marker.index_number])
        # POGGER.debug("collected_count:$:", collected_count)
        # POGGER.debug("fenced_token.fence_character_count:$:", fenced_token.fence_character_count)
        # POGGER.debug("after_fence_and_spaces_index:$:", after_fence_and_spaces_index)
        # POGGER.debug("len(position_marker.text_to_parse):$:", len(position_marker.text_to_parse))
        # POGGER.debug("only_spaces_after_fence:$:", only_spaces_after_fence)

        if (
            fenced_token.code_fence_character
            == position_marker.text_to_parse[position_marker.index_number]
            and collected_count >= fenced_token.fence_character_count
            and after_fence_and_spaces_index >= len(position_marker.text_to_parse)
            and only_spaces_after_fence
        ):
            if split_tab:
                TabHelper.adjust_block_quote_indent_for_tab(parser_state)

            assert extracted_whitespace is not None
            assert extracted_spaces is not None
            new_end_token = parser_state.token_stack[
                -1
            ].generate_close_markdown_token_from_stack_token(
                extracted_whitespace,
                extra_end_data=f"{extracted_spaces}:{collected_count}",
            )

            new_tokens.append(new_end_token)
            del parser_state.token_stack[-1]

    # pylint: enable=too-many-arguments

    @staticmethod
    def __check_for_fenced_end_with_tab(
        original_line: str,
        detabified_original_start_index: int,
        collected_count: int,
        extracted_whitespace: Optional[str],
    ) -> Tuple[int, bool, Optional[str], bool]:
        (
            after_fence_index,
            adj_end,
            fence_string,
        ) = FencedLeafBlockProcessor.__calculate_fenced_vars(
            collected_count, original_line, detabified_original_start_index
        )

        assert fence_string in original_line
        original_fence_string_index = original_line.find(fence_string)
        after_fence_in_original = original_line[
            original_fence_string_index + collected_count :
        ]

        _, after_space_in_original_index = ParserHelper.collect_while_character(
            after_fence_in_original, 0, " "
        )
        only_spaces_after_fence = after_space_in_original_index == len(
            after_fence_in_original
        )

        assert extracted_whitespace is not None

        _, adj_original_index, split_tab = TabHelper.find_tabified_string(
            original_line, extracted_whitespace + adj_end
        )

        _, new_extracted_whitespace = ParserHelper.extract_spaces(
            original_line, adj_original_index
        )

        return (
            after_fence_index,
            only_spaces_after_fence,
            new_extracted_whitespace,
            split_tab,
        )

    @staticmethod
    def __calculate_fenced_vars(
        collected_count: int, original_line: str, detabified_original_start_index: int
    ) -> Tuple[int, str, str]:
        detabified_original_line = TabHelper.detabify_string(original_line)
        adj_original_line = detabified_original_line[detabified_original_start_index:]

        after_whitespace_index, _ = ParserHelper.extract_spaces(adj_original_line, 0)
        assert after_whitespace_index is not None
        after_fence_index = after_whitespace_index + collected_count
        adj_end = adj_original_line[after_whitespace_index:]
        fence_string = adj_original_line[after_whitespace_index:after_fence_index]
        assert fence_string in original_line
        return after_fence_index, adj_end, fence_string

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_fenced_start(
        parser_state: ParserState,
        position_marker: PositionMarker,
        non_whitespace_index: int,
        collected_count: int,
        extracted_whitespace: Optional[str],
        original_line: str,
        new_index: int,
        block_quote_data: BlockQuoteData,
        after_fence_index: int,
    ) -> List[MarkdownToken]:
        POGGER.debug("pfcb->check")
        new_tokens: List[MarkdownToken] = []
        if (
            position_marker.text_to_parse[position_marker.index_number]
            == FencedLeafBlockProcessor.__fenced_start_tilde
            or FencedLeafBlockProcessor.__fenced_start_backtick
            not in position_marker.text_to_parse[non_whitespace_index:]
        ):
            POGGER.debug("pfcb->start")

            old_top_of_stack, new_tokens = FencedLeafBlockProcessor.__add_fenced_tokens(
                parser_state,
                position_marker,
                non_whitespace_index,
                collected_count,
                extracted_whitespace,
                original_line,
                new_index,
                block_quote_data,
                after_fence_index,
            )

            POGGER.debug("StackToken-->$<<", parser_state.token_stack[-1])
            POGGER.debug(
                "StackToken>start_markdown_token-->$<<",
                parser_state.token_stack[-1].matching_markdown_token,
            )

            LeafBlockHelper.correct_for_leaf_block_start_in_list(
                parser_state,
                position_marker.index_indent,
                old_top_of_stack,
                new_tokens,
            )
        return new_tokens

    # pylint: enable=too-many-arguments

    @staticmethod
    def __parse_fenced_code_block_already_in(
        parser_state: ParserState,
        extracted_whitespace: Optional[str],
        original_line: str,
        line_to_parse: str,
    ) -> Optional[str]:
        fenced_token = cast(FencedCodeBlockStackToken, parser_state.token_stack[-1])
        if fenced_token.whitespace_start_count and extracted_whitespace:
            POGGER.debug("original_line>:$:<", original_line)
            POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
            current_whitespace_length = TabHelper.calculate_length(extracted_whitespace)
            POGGER.debug("current_whitespace_length>>$", current_whitespace_length)
            whitespace_left_count = max(
                0,
                current_whitespace_length - fenced_token.whitespace_start_count,
            )
            whitespace_used_count = current_whitespace_length - whitespace_left_count
            POGGER.debug("previous_ws>>$", current_whitespace_length)
            POGGER.debug("whitespace_left>:$:<", whitespace_left_count)
            (
                do_normal_processing,
                removed_whitespace,
                whitespace_padding,
            ) = FencedLeafBlockProcessor.__parse_fenced_code_block_already_in_with_tab(
                whitespace_used_count,
                whitespace_left_count,
                original_line,
                line_to_parse,
                current_whitespace_length,
            )
            if do_normal_processing:
                removed_whitespace = ParserHelper.create_replace_with_nothing_marker(
                    ParserHelper.repeat_string(
                        ParserHelper.space_character,
                        current_whitespace_length - whitespace_left_count,
                    )
                )
                whitespace_padding = ParserHelper.repeat_string(
                    ParserHelper.space_character, whitespace_left_count
                )
            extracted_whitespace = f"{removed_whitespace}{whitespace_padding}"
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        return extracted_whitespace

    @staticmethod
    def __parse_fenced_code_block_already_in_with_tab(
        whitespace_used_count: int,
        whitespace_left_count: int,
        original_line: str,
        line_to_parse: str,
        current_whitespace_length: int,
    ) -> Tuple[bool, str, str]:
        do_normal_processing = True
        removed_whitespace = ""
        whitespace_padding = ""
        if whitespace_left_count and "\t" in original_line:
            ex_space, ex_space_index, split_tab = TabHelper.find_tabified_string(
                original_line, line_to_parse, use_proper_traverse=True
            )
            modified_ex_space_index = (
                ex_space_index + 1 if split_tab else ex_space_index
            )

            (
                detabified_ex_space,
                last_good_space_index,
                _,
            ) = TabHelper.search_for_tabbed_prefix(
                ex_space, whitespace_used_count, modified_ex_space_index
            )

            do_normal_processing = len(detabified_ex_space) == whitespace_used_count
            if not do_normal_processing:
                (
                    removed_whitespace,
                    whitespace_padding,
                ) = FencedLeafBlockProcessor.__parse_fenced_code_block_already_in_with_tab_whitespace(
                    ex_space,
                    last_good_space_index,
                    detabified_ex_space,
                    whitespace_used_count,
                    current_whitespace_length,
                )
        return do_normal_processing, removed_whitespace, whitespace_padding

    @staticmethod
    def __parse_fenced_code_block_already_in_with_tab_whitespace(
        ex_space: str,
        last_good_space_index: int,
        detabified_ex_space: str,
        whitespace_used_count: int,
        current_whitespace_length: int,
    ) -> Tuple[str, str]:
        tab_prefix = ex_space[: last_good_space_index - 1]
        split_tab_character = ex_space[last_good_space_index - 1]
        whitespace_left = detabified_ex_space[whitespace_used_count:]

        removed_whitespace = (
            ParserHelper.create_replace_with_nothing_marker(tab_prefix)
            if tab_prefix
            else ""
        )
        removed_whitespace += ParserHelper.create_replacement_markers(
            split_tab_character, whitespace_left
        )
        whitespace_padding = ParserHelper.repeat_string(
            ParserHelper.space_character,
            current_whitespace_length - len(detabified_ex_space),
        )
        return removed_whitespace, whitespace_padding

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_fenced_tokens(
        parser_state: ParserState,
        position_marker: PositionMarker,
        non_whitespace_index: int,
        collected_count: int,
        extracted_whitespace: Optional[str],
        original_line: str,
        new_index: int,
        block_quote_data: BlockQuoteData,
        after_fence_index: int,
    ) -> Tuple[StackToken, List[MarkdownToken]]:
        (
            line_to_parse,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            extracted_whitespace,
            split_tab,
            corrected_prefix_length,
            extracted_text,
            text_after_extracted_text,
        ) = FencedLeafBlockProcessor.__add_fenced_tokens_prepare(
            position_marker,
            original_line,
            new_index,
            non_whitespace_index,
            collected_count,
            extracted_whitespace,
            after_fence_index,
        )

        return FencedLeafBlockProcessor.__add_fenced_tokens_create(
            parser_state,
            position_marker,
            extracted_whitespace,
            extracted_whitespace_before_info_string,
            corrected_prefix_length,
            collected_count,
            extracted_text,
            text_after_extracted_text,
            line_to_parse,
            split_tab,
            block_quote_data,
        )

    @staticmethod
    def __add_fenced_tokens_calc(
        parser_state: ParserState, split_tab: bool, block_quote_data: BlockQuoteData
    ) -> Tuple[StackToken, List[MarkdownToken], int]:
        old_top_of_stack = parser_state.token_stack[-1]
        new_tokens, _ = parser_state.close_open_blocks_fn(
            parser_state,
            only_these_blocks=[ParagraphStackToken],
        )

        if split_tab := ContainerHelper.reduce_containers_if_required(
            parser_state, block_quote_data, new_tokens, split_tab
        ):
            TabHelper.adjust_block_quote_indent_for_tab(parser_state)
            whitespace_count_delta = -1
        else:
            whitespace_count_delta = 0

        return old_top_of_stack, new_tokens, whitespace_count_delta

    @staticmethod
    def __add_fenced_tokens_prepare(
        position_marker: PositionMarker,
        original_line: str,
        new_index: int,
        non_whitespace_index: int,
        collected_count: int,
        extracted_whitespace: Optional[str],
        after_fence_index: int,
    ) -> Tuple[str, int, Optional[str], Optional[str], bool, int, str, str]:
        (
            line_to_parse,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            extracted_whitespace,
            split_tab,
            corrected_prefix_length,
        ) = FencedLeafBlockProcessor.__add_fenced_tokens_with_tab(
            position_marker,
            original_line,
            new_index,
            non_whitespace_index,
            collected_count,
            extracted_whitespace,
            after_fence_index,
        )

        (
            _,
            proper_end_index,
        ) = ParserHelper.collect_backwards_while_one_of_characters(
            line_to_parse, -1, Constants.ascii_whitespace
        )
        adjusted_string = line_to_parse[:proper_end_index]
        non_whitespace_index = min(non_whitespace_index, len(adjusted_string))

        (
            after_extracted_text_index,
            extracted_text,
        ) = ParserHelper.extract_until_spaces(adjusted_string, non_whitespace_index)
        assert extracted_text is not None

        return (
            line_to_parse,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            extracted_whitespace,
            split_tab,
            corrected_prefix_length,
            extracted_text,
            line_to_parse[after_extracted_text_index:],
        )

    # pylint: enable=too-many-arguments
    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __add_fenced_tokens_create(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        extracted_whitespace_before_info_string: Optional[str],
        corrected_prefix_length: int,
        collected_count: int,
        extracted_text: str,
        text_after_extracted_text: str,
        line_to_parse: str,
        split_tab: bool,
        block_quote_data: BlockQuoteData,
    ) -> Tuple[StackToken, List[MarkdownToken]]:
        (
            old_top_of_stack,
            new_tokens,
            whitespace_start_count,
        ) = FencedLeafBlockProcessor.__add_fenced_tokens_calc(
            parser_state, split_tab, block_quote_data
        )

        pre_extracted_text, pre_text_after_extracted_text = (
            extracted_text,
            text_after_extracted_text,
        )

        assert extracted_text is not None
        extracted_text = InlineBackslashHelper.handle_backslashes(extracted_text)
        text_after_extracted_text = InlineBackslashHelper.handle_backslashes(
            text_after_extracted_text
        )

        if pre_extracted_text == extracted_text:
            pre_extracted_text = ""
        if pre_text_after_extracted_text == text_after_extracted_text:
            pre_text_after_extracted_text = ""

        assert extracted_whitespace is not None
        assert extracted_whitespace_before_info_string is not None
        new_token = FencedCodeBlockMarkdownToken(
            position_marker.text_to_parse[position_marker.index_number],
            collected_count,
            extracted_text,
            pre_extracted_text,
            text_after_extracted_text,
            pre_text_after_extracted_text,
            extracted_whitespace,
            extracted_whitespace_before_info_string,
            position_marker,
        )
        new_tokens.append(new_token)
        assert extracted_whitespace is not None
        whitespace_start_count += TabHelper.calculate_length(
            extracted_whitespace, corrected_prefix_length
        )
        parser_state.token_stack.append(
            FencedCodeBlockStackToken(
                code_fence_character=line_to_parse[position_marker.index_number],
                fence_character_count=collected_count,
                whitespace_start_count=whitespace_start_count,
                matching_markdown_token=new_token,
            )
        )
        return old_top_of_stack, new_tokens

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_fenced_tokens_with_tab(
        position_marker: PositionMarker,
        original_line: str,
        new_index: int,
        non_whitespace_index: int,
        collected_count: int,
        extracted_whitespace: Optional[str],
        after_fence_index: int,
    ) -> Tuple[str, int, Optional[str], Optional[str], bool, int]:
        split_tab = False
        corrected_prefix_length = 0
        line_to_parse = position_marker.text_to_parse
        if ParserHelper.tab_character in original_line:
            (
                fence_string,
                adj_original_line,
                split_tab,
                extracted_whitespace,
                corrected_prefix_length,
            ) = FencedLeafBlockProcessor.__add_fenced_tokens_with_tab_calc(
                original_line,
                line_to_parse,
                new_index,
                collected_count,
                after_fence_index,
                extracted_whitespace,
            )

            assert adj_original_line is not None

            line_to_parse = adj_original_line
            new_index = line_to_parse.find(fence_string)
            new_index += len(fence_string)

            (
                new_non_whitespace_index,
                extracted_whitespace_before_info_string,
            ) = ParserHelper.extract_ascii_whitespace(line_to_parse, new_index)
            assert new_non_whitespace_index is not None
            non_whitespace_index = new_non_whitespace_index
        else:
            (
                _,
                extracted_whitespace_before_info_string,
            ) = ParserHelper.extract_ascii_whitespace(line_to_parse, new_index)
        return (
            line_to_parse,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            extracted_whitespace,
            split_tab,
            corrected_prefix_length,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_fenced_tokens_with_tab_calc(
        original_line: str,
        line_to_parse: str,
        new_index: int,
        collected_count: int,
        after_fence_index: int,
        extracted_whitespace: Optional[str],
    ) -> Tuple[str, str, bool, Optional[str], int]:
        fence_string = line_to_parse[new_index - collected_count : new_index]
        split_tab = False
        corrected_prefix_length = 0

        adj_original_line, _, _ = TabHelper.find_detabify_string(
            original_line, line_to_parse, use_proper_traverse=True
        )

        if adj_original_line is None:
            adj_original_line = (
                FencedLeafBlockProcessor.__add_fenced_tokens_with_tab_calc_prefix(
                    line_to_parse,
                    original_line,
                    new_index,
                    collected_count,
                    after_fence_index,
                )
            )

        fence_string_index = original_line.find(fence_string)
        assert fence_string_index != -1
        if prefix := original_line[:fence_string_index]:
            assert extracted_whitespace is not None
            (
                corrected_prefix,
                corrected_suffix,
                split_tab,
            ) = TabHelper.match_tabbed_whitespace(extracted_whitespace, prefix)
            extracted_whitespace = corrected_suffix
            corrected_prefix_length = len(corrected_prefix)
        return (
            fence_string,
            adj_original_line,
            split_tab,
            extracted_whitespace,
            corrected_prefix_length,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __add_fenced_tokens_with_tab_calc_prefix(
        line_to_parse: str,
        original_line: str,
        new_index: int,
        collected_count: int,
        after_fence_index: int,
    ) -> str:
        line_suffix = line_to_parse[new_index - collected_count : after_fence_index]
        line_suffix_index = original_line.find(line_suffix)
        assert line_suffix_index != -1
        return original_line[line_suffix_index:]

    # pylint: disable=too-many-arguments
    @staticmethod
    def handle_fenced_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        leaf_token_whitespace: Optional[str],
        new_tokens: List[MarkdownToken],
        original_line: str,
        detabified_original_start_index: int,
        block_quote_data: BlockQuoteData,
    ) -> bool:
        """
        Take care of the processing for fenced code blocks.
        """
        if parser_state.token_stack[-1].was_link_definition_started:
            return False

        POGGER.debug(">>__handle_fenced_code_block>>start")
        POGGER.debug(">>leaf_token_whitespace>:$:<", leaf_token_whitespace)
        (
            fenced_tokens,
            leaf_token_whitespace,
        ) = FencedLeafBlockProcessor.parse_fenced_code_block(
            parser_state,
            position_marker,
            leaf_token_whitespace,
            original_line,
            detabified_original_start_index,
            block_quote_data,
        )
        POGGER.debug(">>leaf_token_whitespace>:$:<", leaf_token_whitespace)
        if fenced_tokens:
            new_tokens.extend(fenced_tokens)
            POGGER.debug(">>new_tokens>>$", new_tokens)
        elif parser_state.token_stack[-1].is_fenced_code_block:
            POGGER.debug(">>still in fenced block>:$:<", original_line)
            POGGER.debug(">>leaf_token_whitespace>:$:<", leaf_token_whitespace)
            assert leaf_token_whitespace is not None
            token_text = position_marker.text_to_parse[position_marker.index_number :]
            if ParserHelper.tab_character in original_line:
                (
                    leaf_token_whitespace,
                    token_text,
                ) = FencedLeafBlockProcessor.__handle_fenced_code_block_with_tab(
                    parser_state, original_line, leaf_token_whitespace, token_text
                )
            new_tokens.append(
                TextMarkdownToken(
                    token_text,
                    leaf_token_whitespace,
                    position_marker=position_marker,
                )
            )
            POGGER.debug(">>new_tokens>>$", new_tokens)
        else:
            return False
        return True

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_fenced_code_block_with_tab_and_extracted_whitespace(
        new_extracted_whitespace: str,
        adj_original_index: int,
        whitespace_start_count: int,
        extracted_whitespace: str,
    ) -> str:
        new_index = 0
        POGGER.debug("new_index>:$:<", new_index)
        while new_index < len(new_extracted_whitespace):
            before_count = new_extracted_whitespace[: new_index + 1]
            POGGER.debug("before_count>:$:<", before_count)
            detabified_before_count = TabHelper.detabify_string(
                before_count, adj_original_index
            )
            POGGER.debug("detabified_before_count>:$:<", detabified_before_count)
            detabified_before_count_length = len(detabified_before_count)
            POGGER.debug(
                "detabified_before_count_length>:$:<",
                detabified_before_count_length,
            )
            POGGER.debug("whitespace_start_count>:$:<", whitespace_start_count)
            if detabified_before_count_length >= whitespace_start_count:
                after_count = new_extracted_whitespace[len(before_count) :]
                break
            new_index += 1
            POGGER.debug("new_index>:$:<", new_index)

        POGGER.debug("new_extracted_whitespace>:$:<", new_extracted_whitespace)
        POGGER.debug(
            "detabified_before_count_length>:$:<", detabified_before_count_length
        )
        POGGER.debug("whitespace_start_count>:$:<", whitespace_start_count)
        if detabified_before_count_length < whitespace_start_count:
            assert before_count == new_extracted_whitespace
            after_count = ""
        POGGER.debug("before_count>:$:<", before_count)
        POGGER.debug("after_count>:$:<", after_count)

        POGGER.debug("new_extracted_whitespace>:$:<", new_extracted_whitespace)
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        replacement_string = (
            ParserHelper.replace_noop_character
            if len(after_count) == 0
            else after_count
        )

        new_extracted_whitespace = ParserHelper.create_replacement_markers(
            extracted_whitespace, replacement_string
        )
        POGGER.debug("new_extracted_whitespace>:$:<", new_extracted_whitespace)
        return new_extracted_whitespace

    @staticmethod
    def __handle_fenced_code_block_with_tab(
        parser_state: ParserState,
        original_line: str,
        leaf_token_whitespace: str,
        token_text: str,
    ) -> Tuple[str, str]:
        fenced_stack_token = cast(
            FencedCodeBlockStackToken, parser_state.token_stack[-1]
        )
        whitespace_start_count = fenced_stack_token.whitespace_start_count
        was_indented = False
        if not parser_state.token_stack[-2].is_document:
            last_container_token = parser_state.token_stack[-2]
            assert last_container_token.is_block_quote
            was_indented = True

        resolved_leaf_token_whitespace = ParserHelper.remove_all_from_text(
            leaf_token_whitespace
        )
        reconstructed_line = resolved_leaf_token_whitespace + token_text
        reconstructed_line_has_tab = True
        if reconstructed_line[0] == "\t":
            reconstructed_line_has_tab = False
            adj_original = reconstructed_line
            adj_original_index = original_line.find(reconstructed_line)
            assert adj_original_index != -1
            split_tab = False

            resolved_leaf_token_whitespace = TabHelper.detabify_string(
                resolved_leaf_token_whitespace, adj_original_index
            )
        else:
            (
                adj_original,
                adj_original_index,
                split_tab,
            ) = TabHelper.find_tabified_string(
                original_line, reconstructed_line, abc=True
            )

        (
            leaf_token_whitespace,
            token_text,
        ) = FencedLeafBlockProcessor.__handle_fenced_code_block_with_tab_whitespace(
            parser_state,
            leaf_token_whitespace,
            adj_original,
            adj_original_index,
            resolved_leaf_token_whitespace,
            whitespace_start_count,
            was_indented,
            reconstructed_line_has_tab,
            split_tab,
        )
        return leaf_token_whitespace, token_text

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_fenced_code_block_with_tab_whitespace(
        parser_state: ParserState,
        leaf_token_whitespace: str,
        adj_original: str,
        adj_original_index: int,
        resolved_leaf_token_whitespace: str,
        whitespace_start_count: int,
        was_indented: bool,
        reconstructed_line_has_tab: bool,
        split_tab: bool,
    ) -> Tuple[str, str]:
        space_end_index, extracted_whitespace = ParserHelper.extract_spaces(
            adj_original, 0
        )
        assert extracted_whitespace is not None
        assert space_end_index != -1

        detabified_extracted_whitespace = TabHelper.detabify_string(
            extracted_whitespace, adj_original_index
        )
        assert detabified_extracted_whitespace == resolved_leaf_token_whitespace

        new_extracted_whitespace = extracted_whitespace
        if new_extracted_whitespace and whitespace_start_count:
            assert was_indented
            new_extracted_whitespace = FencedLeafBlockProcessor.__handle_fenced_code_block_with_tab_and_extracted_whitespace(
                new_extracted_whitespace,
                adj_original_index,
                whitespace_start_count,
                extracted_whitespace,
            )

        if reconstructed_line_has_tab:
            leaf_token_whitespace = new_extracted_whitespace
        token_text = adj_original[space_end_index:]
        if split_tab:
            TabHelper.adjust_block_quote_indent_for_tab(parser_state)

        return leaf_token_whitespace, token_text

    # pylint: enable=too-many-arguments
