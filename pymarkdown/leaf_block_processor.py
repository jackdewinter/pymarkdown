"""
Module to provide processing for the leaf blocks.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quote_data import BlockQuoteData
from pymarkdown.constants import Constants
from pymarkdown.container_grab_bag import ContainerGrabBag
from pymarkdown.container_helper import ContainerHelper
from pymarkdown.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ListStartMarkdownToken,
)
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_markdown_token import (
    AtxHeadingMarkdownToken,
    FencedCodeBlockMarkdownToken,
    IndentedCodeBlockMarkdownToken,
    ParagraphMarkdownToken,
    SetextHeadingMarkdownToken,
    ThematicBreakMarkdownToken,
)
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.stack_token import (
    FencedCodeBlockStackToken,
    IndentedCodeBlockStackToken,
    ListStackToken,
    ParagraphStackToken,
    StackToken,
)
from pymarkdown.tab_helper import TabHelper

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


class LeafBlockProcessor:
    """
    Class to provide processing for the leaf blocks.
    """

    __fenced_start_tilde = "~"
    __fenced_start_backtick = "`"
    __fenced_code_block_start_characters = (
        f"{__fenced_start_tilde}{__fenced_start_backtick}"
    )
    __thematic_break_characters = "*_-"
    __atx_character = "#"
    __setext_characters = "-="

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
            LeafBlockProcessor.__fenced_code_block_start_characters,
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
        ) = LeafBlockProcessor.is_fenced_code_block(
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
                LeafBlockProcessor.__check_for_fenced_end(
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
                new_tokens = LeafBlockProcessor.__process_fenced_start(
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
                LeafBlockProcessor.__parse_fenced_code_block_already_in(
                    parser_state,
                    extracted_whitespace,
                    original_line,
                    position_marker.text_to_parse,
                )
            )
        return new_tokens, extracted_whitespace

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
            ) = LeafBlockProcessor.__parse_fenced_code_block_already_in_with_tab(
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
            # POGGER.debug("ex_space>:$:<", ex_space)
            # POGGER.debug("ex_space_index>:$:<", ex_space_index)
            # POGGER.debug("split_tab>:$:<", split_tab)
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

            # POGGER.debug("detabified_ex_space>:$:<", detabified_ex_space)
            # POGGER.debug("whitespace_used>:$:<", whitespace_used_count)
            do_normal_processing = len(detabified_ex_space) == whitespace_used_count
            if not do_normal_processing:
                (
                    removed_whitespace,
                    whitespace_padding,
                ) = LeafBlockProcessor.__parse_fenced_code_block_already_in_with_tab_whitespace(
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
        # POGGER.debug("last_good_space_index>:$:<", last_good_space_index)
        tab_prefix = ex_space[: last_good_space_index - 1]
        split_tab_character = ex_space[last_good_space_index - 1]
        # POGGER.debug("tab_prefix>:$:<", tab_prefix)
        # POGGER.debug("split_tab_character>:$:<", split_tab_character)
        # wsu = detabified_ex_space[:whitespace_used_count]
        # POGGER.debug("wsu>:$:<", wsu)
        whitespace_left = detabified_ex_space[whitespace_used_count:]
        # POGGER.debug("whitespace_left>:$:<", whitespace_left)

        removed_whitespace = (
            ParserHelper.create_replace_with_nothing_marker(tab_prefix)
            if tab_prefix
            else ""
        )
        # POGGER.debug("removed_whitespace>:$:<", removed_whitespace)
        removed_whitespace += ParserHelper.create_replacement_markers(
            split_tab_character, whitespace_left
        )
        # POGGER.debug("removed_whitespace>:$:<", removed_whitespace)
        whitespace_padding = ParserHelper.repeat_string(
            ParserHelper.space_character,
            current_whitespace_length - len(detabified_ex_space),
        )
        return removed_whitespace, whitespace_padding

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
            ) = LeafBlockProcessor.__add_fenced_tokens_with_tab_calc(
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
        # POGGER.debug(
        #     "extracted_whitespace_before_info_string>:$:<",
        #     extracted_whitespace_before_info_string,
        # )
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

        # POGGER.debug("fence_string>:$:<", fence_string)
        # POGGER.debug("before_fence_index>:$:<", before_fence_index)
        # POGGER.debug("after_fence_index>:$:<", after_fence_index)
        # POGGER.debug("non_whitespace_index>:$:<", non_whitespace_index)
        # POGGER.debug("original_line>:$:<", original_line)
        # POGGER.debug("line_to_parse>:$:<", line_to_parse)
        adj_original_line, _, _ = TabHelper.find_detabify_string(
            original_line, line_to_parse, use_proper_traverse=True
        )
        # POGGER.debug("adj_original_line>:$:<", adj_original_line)

        if adj_original_line is None:
            adj_original_line = (
                LeafBlockProcessor.__add_fenced_tokens_with_tab_calc_prefix(
                    line_to_parse,
                    original_line,
                    new_index,
                    collected_count,
                    after_fence_index,
                )
            )

        # POGGER.debug("original_line>:$:<", original_line)
        # POGGER.debug("fence_string>:$:<", fence_string)
        fence_string_index = original_line.find(fence_string)
        # POGGER.debug("fence_string_index>:$:<", fence_string_index)
        assert fence_string_index != -1
        if prefix := original_line[:fence_string_index]:
            assert extracted_whitespace is not None
            (
                corrected_prefix,
                corrected_suffix,
                split_tab,
            ) = TabHelper.match_tabbed_whitespace(extracted_whitespace, prefix)
            # POGGER.debug("corrected_prefix>:$:<", corrected_prefix)
            # POGGER.debug("corrected_suffix>:$:<", corrected_suffix)
            extracted_whitespace = corrected_suffix
            corrected_prefix_length = len(corrected_prefix)
            # POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
            # POGGER.debug("corrected_prefix_length>:$:<", corrected_prefix_length)
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
        # split
        # POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)

        # line_prefix = line_to_parse[:before_fence_index]
        # POGGER.debug("line_prefix>:$:<", line_prefix)
        line_suffix = line_to_parse[new_index - collected_count : after_fence_index]
        # POGGER.debug("line_suffix>:$:<", line_suffix)
        line_suffix_index = original_line.find(line_suffix)
        assert line_suffix_index != -1
        # POGGER.debug("line_suffix_index>:$:<", line_suffix_index)
        return original_line[line_suffix_index:]

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
        # POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        # POGGER.debug("collected_count>:$:<", collected_count)
        # POGGER.debug("text_to_parse>>:$:<", position_marker.text_to_parse)
        # POGGER.debug("index_number>>:$:<", position_marker.index_number)
        # POGGER.debug("original_line>:$:<", original_line)
        # POGGER.debug("new_index>:$:<", new_index)
        # POGGER.debug("non_whitespace_index>:$:<", non_whitespace_index)

        (
            line_to_parse,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            extracted_whitespace,
            split_tab,
            corrected_prefix_length,
            extracted_text,
            text_after_extracted_text,
        ) = LeafBlockProcessor.__add_fenced_tokens_prepare(
            position_marker,
            original_line,
            new_index,
            non_whitespace_index,
            collected_count,
            extracted_whitespace,
            after_fence_index,
        )

        return LeafBlockProcessor.__add_fenced_tokens_create(
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
        ) = LeafBlockProcessor.__add_fenced_tokens_with_tab(
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
        ) = LeafBlockProcessor.__add_fenced_tokens_calc(
            parser_state, split_tab, block_quote_data
        )

        pre_extracted_text, pre_text_after_extracted_text = (
            extracted_text,
            text_after_extracted_text,
        )

        assert extracted_text is not None
        extracted_text = InlineHelper.handle_backslashes(extracted_text)
        text_after_extracted_text = InlineHelper.handle_backslashes(
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
        # POGGER.debug("extracted_whitespace = >:$:<", extracted_whitespace)
        # POGGER.debug("corrected_prefix_length = >:$:<", corrected_prefix_length)
        whitespace_start_count += TabHelper.calculate_length(
            extracted_whitespace, corrected_prefix_length
        )
        # POGGER.debug("whitespace_start_count = >:$:<", whitespace_start_count)
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
            == LeafBlockProcessor.__fenced_start_tilde
            or LeafBlockProcessor.__fenced_start_backtick
            not in position_marker.text_to_parse[non_whitespace_index:]
        ):
            POGGER.debug("pfcb->start")

            old_top_of_stack, new_tokens = LeafBlockProcessor.__add_fenced_tokens(
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

            LeafBlockProcessor.correct_for_leaf_block_start_in_list(
                parser_state,
                position_marker.index_indent,
                old_top_of_stack,
                new_tokens,
            )
        return new_tokens

    # pylint: enable=too-many-arguments
    @staticmethod
    def __check_for_fenced_end_with_tab(
        original_line: str,
        detabified_original_start_index: int,
        collected_count: int,
        extracted_whitespace: Optional[str],
    ) -> Tuple[int, bool, Optional[str], bool]:
        # POGGER.debug("detabified_original_start_index:$:", detabified_original_start_index)
        # POGGER.debug("collected_count:$:", collected_count)
        # POGGER.debug("extracted_whitespace:$:", extracted_whitespace)

        (
            after_fence_index,
            adj_end,
            fence_string,
        ) = LeafBlockProcessor.__calculate_fenced_vars(
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
        # POGGER.debug(
        #     ">>after_space_in_original_index>:$:<", after_space_in_original_index
        # )
        # POGGER.debug(
        #     ">>after_fence_in_original($)>:$:<",
        #     len(after_fence_in_original),
        #     after_fence_in_original,
        # )
        only_spaces_after_fence = after_space_in_original_index == len(
            after_fence_in_original
        )
        # POGGER.debug(">>only_spaces_after_fence>:$:<", only_spaces_after_fence)

        assert extracted_whitespace is not None

        _, adj_original_index, split_tab = TabHelper.find_tabified_string(
            original_line, extracted_whitespace + adj_end
        )

        _, new_extracted_whitespace = ParserHelper.extract_spaces(
            original_line, adj_original_index
        )

        # POGGER.debug("after_fence_index:$:", after_fence_index)
        # POGGER.debug("only_spaces_after_fence:$:", only_spaces_after_fence)
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
        # POGGER.debug("after_whitespace_index=$", after_whitespace_index)
        after_fence_index = after_whitespace_index + collected_count
        adj_end = adj_original_line[after_whitespace_index:]
        fence_string = adj_original_line[after_whitespace_index:after_fence_index]
        assert fence_string in original_line
        return after_fence_index, adj_end, fence_string

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
            ) = LeafBlockProcessor.__check_for_fenced_end_with_tab(
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
    def __recalculate_whitespace(
        whitespace_to_parse: Optional[str],
        offset_index: int,
        tabified_extracted_space: Optional[str],
    ) -> Tuple[int, str, str]:
        """
        Recalculate the whitespace characteristics.
        """
        assert whitespace_to_parse is not None
        POGGER.debug("whitespace_to_parse>>$>>", whitespace_to_parse)
        POGGER.debug("offset_index>>$>>", offset_index)
        POGGER.debug("tabified_extracted_space>>$>>", tabified_extracted_space)

        actual_whitespace_index = 4 + offset_index
        adj_ws = whitespace_to_parse[:actual_whitespace_index]
        left_ws = whitespace_to_parse[actual_whitespace_index:]
        if tabified_extracted_space:
            additional_start_delta = 0
            length_so_far = 0
            last_index = 0
            next_character_index = 0
            while (
                next_character_index < len(tabified_extracted_space)
                and length_so_far < 4
            ):
                next_character = tabified_extracted_space[next_character_index]
                POGGER.debug("next_character>:$:<", next_character)
                if next_character == ParserHelper.tab_character:
                    length_so_far = (1 + (length_so_far // 4)) * 4
                else:
                    length_so_far += 1
                last_index += 1
                POGGER.debug("length_so_far>:$:<", length_so_far)
                next_character_index += 1
            POGGER.debug("length_so_far>:$:<", length_so_far)
            assert length_so_far == 4
            POGGER.debug("last_index>:$:<", last_index)
            tabbed_prefix = tabified_extracted_space[:last_index]
            POGGER.debug("tabbed_prefix>:$:<", tabbed_prefix)
            err = TabHelper.detabify_string(
                tabbed_prefix,
                additional_start_delta=additional_start_delta,
            )
            POGGER.debug("tabbed_prefix>:$:<", tabbed_prefix)
            POGGER.debug("err>:$:<", err)
            assert len(err) == 4
            adj_ws = tabbed_prefix
            left_ws = tabified_extracted_space[last_index:]

        POGGER.debug("actual_whitespace_index>>$", actual_whitespace_index)
        POGGER.debug("adj_ws>>$<<", adj_ws)
        POGGER.debug("left_ws>>$<<", left_ws)
        return actual_whitespace_index, adj_ws, left_ws

    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_indented_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        removed_chars_at_start: Optional[int],
        last_block_quote_index: int,
        last_list_start_index: int,
        original_line: str,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of an indented code block
        """

        new_tokens: List[MarkdownToken] = []

        assert extracted_whitespace is not None
        assert removed_chars_at_start is not None
        if (
            TabHelper.is_length_greater_than_or_equal_to(
                extracted_whitespace, 4, start_index=removed_chars_at_start
            )
            and not parser_state.token_stack[-1].is_paragraph
        ):
            # POGGER.debug(
            #     "parse_indented_code_block>>start",
            # )
            # POGGER.debug("removed_chars_at_start>:$:<", removed_chars_at_start)
            # POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
            # POGGER.debug(
            #     "position_marker.text_to_parse>:$:<", position_marker.text_to_parse
            # )
            # POGGER.debug(
            #     "position_marker.text_to_parse[index_number=$]>:$:<",
            #     position_marker.index_number,
            #     position_marker.text_to_parse[position_marker.index_number :],
            # )
            # POGGER.debug("original_line>:$:<", original_line)

            indented_text = position_marker.text_to_parse[
                position_marker.index_number :
            ]

            # POGGER.debug("last_block_quote_index>:$:<", last_block_quote_index)
            is_in_block_quote = last_block_quote_index > 0
            POGGER.debug("is_in_block_quote>:$:<", is_in_block_quote)

            # POGGER.debug("last_list_start_index>:$:<", last_list_start_index)
            is_in_list = last_list_start_index > 0
            POGGER.debug("is_in_list>:$:<", is_in_list)

            tabified_extracted_space: Optional[str] = None
            xx_extracted_space, xx_left_over, adjust_block_quote_indent = (
                None,
                None,
                False,
            )
            if ParserHelper.tab_character in original_line:
                (
                    tabified_extracted_space,
                    xx_extracted_space,
                    xx_left_over,
                    adjust_block_quote_indent,
                ) = LeafBlockProcessor.__parse_indented_code_block_with_tab(
                    parser_state,
                    position_marker,
                    is_in_list,
                    is_in_block_quote,
                    original_line,
                    last_block_quote_index,
                )

            LeafBlockProcessor.__process_indented_code_block(
                parser_state,
                position_marker,
                new_tokens,
                tabified_extracted_space,
                original_line,
                xx_extracted_space,
                xx_left_over,
                adjust_block_quote_indent,
                last_block_quote_index,
                extracted_whitespace,
                indented_text,
            )
        else:
            POGGER.debug(
                "parse_indented_code_block>>not eligible",
            )
        return new_tokens

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_indented_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        new_tokens: List[MarkdownToken],
        tabified_extracted_space: Optional[str],
        original_line: str,
        xx_extracted_space: Optional[str],
        xx_left_over: Optional[str],
        adjust_block_quote_indent: bool,
        last_block_quote_index: int,
        extracted_whitespace: str,
        indented_text: str,
    ) -> None:
        # adj_ws: Optional[str] = ""
        # POGGER.debug("tabified_extracted_space>:$:<", tabified_extracted_space)
        if not parser_state.token_stack[-1].is_indented_code_block:
            # POGGER.debug("xx_extracted_space>:$:<", xx_extracted_space)
            # POGGER.debug("xx_left_over>:$:<", xx_left_over)
            (
                last_block_quote_index,
                xextracted_whitespace,
                indented_text,
            ) = LeafBlockProcessor.__create_indented_block(
                parser_state,
                last_block_quote_index,
                position_marker,
                extracted_whitespace,
                new_tokens,
                tabified_extracted_space,
                original_line,
                indented_text,
                xx_extracted_space,
                xx_left_over,
            )
            assert xextracted_whitespace is not None
            extracted_whitespace = xextracted_whitespace
        elif tabified_extracted_space:
            (_, adj_ws, _) = LeafBlockProcessor.__recalculate_whitespace(
                extracted_whitespace, 0, tabified_extracted_space
            )
            extracted_whitespace = adj_ws

            adj_ws_length = len(adj_ws)
            indented_text = original_line[adj_ws_length:]
        elif xx_extracted_space is not None:
            extracted_whitespace = xx_extracted_space
            assert xx_left_over is not None
            indented_text = xx_left_over

        # POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        # POGGER.debug("indented_text>:$:<", indented_text)

        if adjust_block_quote_indent:
            TabHelper.adjust_block_quote_indent_for_tab(parser_state)

        assert extracted_whitespace is not None
        new_tokens.append(
            TextMarkdownToken(
                indented_text,
                extracted_whitespace,
                position_marker=position_marker,
            )
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __parse_indented_code_block_with_tab(
        parser_state: ParserState,
        position_marker: PositionMarker,
        is_in_list: bool,
        is_in_block_quote: bool,
        original_line: str,
        last_block_quote_index: int,
    ) -> Tuple[Optional[str], Optional[str], Optional[str], bool]:
        if not is_in_list and not is_in_block_quote:
            next_character = position_marker.text_to_parse[position_marker.index_number]
            next_character_index = original_line.find(next_character)
            assert next_character_index != -1
            return (
                original_line[:next_character_index],
                None,
                None,
                False,
            )

        # Note not handling lists yet
        assert is_in_block_quote

        (
            last_block_quote_lead_spaces,
            adj_lead_space_len,
            adjust_block_quote_indent,
        ) = LeafBlockProcessor.__get_indented_block_with_tab_quote_properties(
            parser_state, last_block_quote_index, original_line
        )

        lead_space_len = len(last_block_quote_lead_spaces)
        POGGER.debug("lead_space_len>:$:<", lead_space_len)
        after_space_index, ex_space = ParserHelper.extract_spaces(
            original_line, lead_space_len + adj_lead_space_len
        )
        return LeafBlockProcessor.__parse_indented_code_block_with_tab_complete(
            after_space_index,
            ex_space,
            lead_space_len,
            original_line,
            adjust_block_quote_indent,
        )

    # pylint: enable=too-many-arguments
    @staticmethod
    def __parse_indented_code_block_with_tab_complete(
        after_space_index: Optional[int],
        ex_space: Optional[str],
        lead_space_len: int,
        original_line: str,
        adjust_block_quote_indent: bool,
    ) -> Tuple[Optional[str], Optional[str], Optional[str], bool]:
        POGGER.debug("after_space_index>:$:<", after_space_index)
        POGGER.debug("ex_space>:$:<", ex_space)
        assert ex_space is not None
        detabified_ex_space = TabHelper.detabify_string(
            ex_space, additional_start_delta=lead_space_len
        )
        POGGER.debug("detabified_ex_space>:$:<", detabified_ex_space)
        # assert detabified_ex_space == extracted_whitespace
        # last_good_space_index = -1
        # space_index = 1
        # detabified_ex_space = ""
        # while space_index < len(ex_space) + 1 and len(detabified_ex_space) < 4:
        #     POGGER.debug("space_index>:$:<", space_index)
        #     last_good_space_index = space_index
        #     space_prefix = ex_space[:space_index]
        #     POGGER.debug("sdf>:$:<", space_prefix)
        #     POGGER.debug("lead_space_len>:$:<", lead_space_len)
        #     detabified_ex_space = TabHelper.detabify_string(
        #         space_prefix, additional_start_delta=lead_space_len
        #     )
        #     POGGER.debug("detabified_ex_space>:$:<", detabified_ex_space)
        #     space_index += 1
        # assert len(detabified_ex_space) >= 4

        (
            detabified_ex_space,
            last_good_space_index,
            space_prefix,
        ) = TabHelper.search_for_tabbed_prefix(ex_space, 4, lead_space_len)
        assert space_prefix is not None

        if len(detabified_ex_space) == 4:
            xx_extracted_space = space_prefix
            xx_left_over = ex_space[last_good_space_index:]
        else:
            xx_extracted_space = space_prefix[:-1]
            xx_left_over = ParserHelper.create_replacement_markers(
                space_prefix[-1], detabified_ex_space[4:]
            )

        POGGER.debug("xx_extracted_space>:$:<", xx_extracted_space)
        POGGER.debug("xx_left_over>:$:<", xx_left_over)
        xx_left_over += original_line[after_space_index:]
        POGGER.debug("xx_left_over>:$:<", xx_left_over)
        return None, xx_extracted_space, xx_left_over, adjust_block_quote_indent

    @staticmethod
    def __get_indented_block_with_tab_quote_properties(
        parser_state: ParserState, last_block_quote_index: int, original_line: str
    ) -> Tuple[str, int, bool]:
        adjust_block_quote_indent = False

        POGGER.debug(
            "token_stack[last_block_quote_index]>:$:<",
            parser_state.token_stack[last_block_quote_index],
        )
        last_block_quote_token = cast(
            BlockQuoteMarkdownToken,
            parser_state.token_stack[last_block_quote_index].matching_markdown_token,
        )
        last_block_quote_lead_spaces = last_block_quote_token.bleading_spaces
        assert last_block_quote_lead_spaces is not None
        POGGER.debug("last_block_quote_lead_spaces>:$:<", last_block_quote_lead_spaces)
        lead_space_last_line_index = last_block_quote_lead_spaces.rfind("\n")
        POGGER.debug("original_line>:$:<", original_line)
        adj_lead_space_len = 0
        if lead_space_last_line_index != -1:
            last_block_quote_lead_spaces = last_block_quote_lead_spaces[
                lead_space_last_line_index + 1 :
            ]
            POGGER.debug(
                "last_block_quote_lead_spaces>:$:<", last_block_quote_lead_spaces
            )
        assert last_block_quote_lead_spaces[-1] == " "
        last_part_minus_tailing_space = last_block_quote_lead_spaces[:-1]
        POGGER.debug(
            "last_part_minus_tailing_space>:$:<", last_part_minus_tailing_space
        )
        assert original_line.startswith(last_part_minus_tailing_space)
        trailing_char_in_original = original_line[len(last_part_minus_tailing_space)]
        POGGER.debug("trailing_char_in_original>:$:<", trailing_char_in_original)
        if trailing_char_in_original == ParserHelper.tab_character:
            adjust_block_quote_indent = True
            adj_lead_space_len = -1
            assert original_line.startswith(last_part_minus_tailing_space)
        POGGER.debug("last_block_quote_lead_spaces>:$:<", last_block_quote_lead_spaces)
        # if not adjust_block_quote_indent:
        #     assert original_line.startswith(last_block_quote_lead_spaces)
        return (
            last_block_quote_lead_spaces,
            adj_lead_space_len,
            adjust_block_quote_indent,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_indented_block(
        parser_state: ParserState,
        last_block_quote_index: int,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        new_tokens: List[MarkdownToken],
        tabified_extracted_space: Optional[str],
        original_line: str,
        indented_text: str,
        xx_extracted_space: Optional[str],
        xx_left_over: Optional[str],
    ) -> Tuple[int, Optional[str], str]:
        assert extracted_whitespace is not None
        column_number = (
            position_marker.index_number
            + position_marker.index_indent
            - len(extracted_whitespace)
            + 1
        )
        POGGER.debug("last_block_quote_index>:$:<", last_block_quote_index)
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        POGGER.debug("tabified_extracted_space>:$:<", tabified_extracted_space)
        POGGER.debug("xx_extracted_space>:$:<", xx_extracted_space)
        (
            last_block_quote_index,
            actual_whitespace_index,
            adj_ws,
            extracted_whitespace,
        ) = LeafBlockProcessor.__prepare_for_indented_block(
            parser_state,
            last_block_quote_index,
            extracted_whitespace,
            tabified_extracted_space,
        )
        POGGER.debug("last_block_quote_index>:$:<", last_block_quote_index)
        POGGER.debug("actual_whitespace_index>:$:<", actual_whitespace_index)
        POGGER.debug("adj_ws>:$:<", adj_ws)
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        if xx_extracted_space is not None:
            adj_ws = xx_extracted_space
        POGGER.debug("adj_ws>:$:<", adj_ws)

        column_number += actual_whitespace_index
        POGGER.debug("column_number>>$", column_number)

        new_token = IndentedCodeBlockMarkdownToken(
            adj_ws, position_marker.line_number, column_number
        )
        parser_state.token_stack.append(IndentedCodeBlockStackToken(new_token))
        new_tokens.append(new_token)
        POGGER.debug("left_ws>>$<<", extracted_whitespace)

        POGGER.debug("xx_left_over>:$:<", xx_left_over)
        POGGER.debug("tabified_extracted_space>:$:<", tabified_extracted_space)
        if xx_left_over:
            extracted_whitespace = ""
            indented_text = xx_left_over
        if tabified_extracted_space:
            extracted_whitespace = ""
            adj_ws_length = len(adj_ws)
            indented_text = original_line[adj_ws_length:]

        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        POGGER.debug("indented_text>:$:<", indented_text)
        return last_block_quote_index, extracted_whitespace, indented_text

    # pylint: enable=too-many-arguments

    @staticmethod
    def __prepare_for_indented_block(
        parser_state: ParserState,
        last_block_quote_index: int,
        extracted_whitespace: Optional[str],
        tabified_extracted_space: Optional[str],
    ) -> Tuple[int, int, str, str]:
        POGGER.debug(">>>>$", parser_state.token_stack[-1])
        if parser_state.token_stack[-1].is_list:
            list_token = cast(ListStackToken, parser_state.token_stack[-1])
            POGGER.debug(
                ">>indent>>$",
                list_token.indent_level,
            )
            last_block_quote_index = 0

        POGGER.debug(
            "__recalculate_whitespace>>$>>$",
            extracted_whitespace,
            0,
        )
        (
            actual_whitespace_index,
            adj_ws,
            left_ws,
        ) = LeafBlockProcessor.__recalculate_whitespace(
            extracted_whitespace, 0, tabified_extracted_space
        )
        return (
            last_block_quote_index,
            actual_whitespace_index,
            adj_ws,
            left_ws,
        )

    @staticmethod
    def is_thematic_break(
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        skip_whitespace_check: bool = False,
        whitespace_allowed_between_characters: bool = True,
    ) -> Tuple[Optional[str], Optional[int]]:
        """
        Determine whether or not we have a thematic break.
        """

        assert extracted_whitespace is not None
        thematic_break_character, end_of_break_index = None, None
        is_thematic_character = ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, LeafBlockProcessor.__thematic_break_characters
        )
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        POGGER.debug("skip_whitespace_check>>$", skip_whitespace_check)
        POGGER.debug("is_thematic_character>>$", is_thematic_character)
        if (
            TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            or skip_whitespace_check
        ) and is_thematic_character:
            POGGER.debug("checking for thematic break")
            start_char, index, char_count, line_to_parse_size = (
                line_to_parse[start_index],
                start_index,
                0,
                len(line_to_parse),
            )

            while index < line_to_parse_size:
                if (
                    whitespace_allowed_between_characters
                    and ParserHelper.is_character_at_index_whitespace(
                        line_to_parse, index
                    )
                ):
                    index += 1
                elif line_to_parse[index] == start_char:
                    index += 1
                    char_count += 1
                else:
                    break  # pragma: no cover

            POGGER.debug("char_count>>$", char_count)
            POGGER.debug("index>>$", index)
            POGGER.debug("line_to_parse_size>>$", line_to_parse_size)
            if char_count >= 3 and index == line_to_parse_size:
                thematic_break_character, end_of_break_index = start_char, index

        return thematic_break_character, end_of_break_index

    @staticmethod
    def parse_thematic_break(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        block_quote_data: BlockQuoteData,
        original_line: str,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of a thematic break.
        """

        new_tokens: List[MarkdownToken] = []

        start_char, index = LeafBlockProcessor.is_thematic_break(
            position_marker.text_to_parse,
            position_marker.index_number,
            extracted_whitespace,
        )
        if start_char:
            POGGER.debug(
                "parse_thematic_break>>start",
            )
            if parser_state.token_stack[-1].is_paragraph:
                force_paragraph_close_if_present = (
                    block_quote_data.current_count == 0
                    and block_quote_data.stack_count > 0
                )
                new_tokens, _ = parser_state.close_open_blocks_fn(
                    parser_state,
                    only_these_blocks=[ParagraphStackToken],
                    was_forced=force_paragraph_close_if_present,
                )

            token_text = position_marker.text_to_parse[
                position_marker.index_number : index
            ]
            POGGER.debug("parse_thematic_break>>:$:<", token_text)
            POGGER.debug("original_line>>:$:<", original_line)
            split_tab = False
            if ParserHelper.tab_character in original_line:
                (
                    token_text,
                    split_tab,
                    extracted_whitespace,
                ) = TabHelper.parse_thematic_break_with_tab(
                    original_line, token_text, extracted_whitespace
                )
            if split_tab := ContainerHelper.reduce_containers_if_required(
                parser_state, block_quote_data, new_tokens, split_tab
            ):
                TabHelper.adjust_block_quote_indent_for_tab(parser_state)

            new_tokens.append(
                ThematicBreakMarkdownToken(
                    start_char,
                    extracted_whitespace,
                    token_text,
                    position_marker=position_marker,
                )
            )
        else:
            POGGER.debug(
                "parse_thematic_break>>not eligible",
            )
        return new_tokens

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
            LeafBlockProcessor.__atx_character,
        ):
            hash_count, new_index = ParserHelper.collect_while_character(
                line_to_parse,
                start_index,
                LeafBlockProcessor.__atx_character,
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
        ) = LeafBlockProcessor.is_atx_heading(
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
        return LeafBlockProcessor.__parse_atx_heading_found(
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
        ) = LeafBlockProcessor.__prepare_for_create_atx_heading(
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
                LeafBlockProcessor.__parse_atx_headings_delay_tab_match(
                    position_marker, original_line
                )
            )

        LeafBlockProcessor.__parse_atx_heading_add_tokens(
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

        LeafBlockProcessor.correct_for_leaf_block_start_in_list(
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
            and remaining_line[end_index - 1] == LeafBlockProcessor.__atx_character
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
            LeafBlockProcessor.__determine_eligble_for_tab_match_delay(
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
            assert hash_count is not None
            (
                remaining_line,
                extracted_whitespace_at_start,
                extracted_whitespace,
                split_tab,
            ) = LeafBlockProcessor.__prepare_for_create_atx_heading_with_tab(
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
            parser_state, block_quote_data, new_tokens, split_tab
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
        ) = LeafBlockProcessor.__prepare_for_create_atx_heading_adjust(
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
    def __parse_setext_headings_with_tab(
        original_line: str, line_to_parse: str, extracted_whitespace: str
    ) -> Tuple[str, str, bool]:
        reconstructed_line = extracted_whitespace + line_to_parse
        adj_original, _, split_tab = TabHelper.find_tabified_string(
            original_line, reconstructed_line
        )

        after_space_index, original_extracted_whitespace = ParserHelper.extract_spaces(
            adj_original, 0
        )
        assert original_extracted_whitespace is not None

        extracted_whitespace = original_extracted_whitespace
        line_to_parse = adj_original[after_space_index:]
        return line_to_parse, extracted_whitespace, split_tab

    @staticmethod
    def parse_setext_headings(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        block_quote_data: BlockQuoteData,
        original_line: str,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of an setext heading.
        """

        new_tokens: List[MarkdownToken] = []
        assert extracted_whitespace is not None
        POGGER.debug("extracted_whitespace=>:$:<", extracted_whitespace)
        if (
            TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
            and ParserHelper.is_character_at_index_one_of(
                position_marker.text_to_parse,
                position_marker.index_number,
                LeafBlockProcessor.__setext_characters,
            )
            and parser_state.token_stack[-1].is_paragraph
            and (block_quote_data.current_count == block_quote_data.stack_count)
        ):
            POGGER.debug(
                "parse_setext_headings>>start",
            )
            is_paragraph_continuation = (
                LeafBlockProcessor.__adjust_continuation_for_active_list(
                    parser_state, position_marker
                )
            )

            line_to_parse = position_marker.text_to_parse[
                position_marker.index_number :
            ]
            ex_ws_l = len(extracted_whitespace)
            POGGER.debug("line_to_parse=>:$:<", line_to_parse)
            POGGER.debug("original_line=>:$:<", original_line)
            split_tab = False
            if ParserHelper.tab_character in original_line:
                (
                    line_to_parse,
                    extracted_whitespace,
                    split_tab,
                ) = LeafBlockProcessor.__parse_setext_headings_with_tab(
                    original_line, line_to_parse, extracted_whitespace
                )

            LeafBlockProcessor.__prepare_and_create_setext_token(
                parser_state,
                position_marker,
                line_to_parse,
                is_paragraph_continuation,
                split_tab,
                new_tokens,
                extracted_whitespace,
                ex_ws_l,
            )
        else:
            POGGER.debug(
                "parse_setext_headings>>not eligible",
            )
        return new_tokens

    # pylint: disable=too-many-arguments
    @staticmethod
    def __prepare_and_create_setext_token(
        parser_state: ParserState,
        position_marker: PositionMarker,
        line_to_parse: str,
        is_paragraph_continuation: bool,
        split_tab: bool,
        new_tokens: List[MarkdownToken],
        extracted_whitespace: str,
        ex_ws_l: int,
    ) -> Tuple[int, int, str]:
        _, collected_to_index = ParserHelper.collect_while_character(
            line_to_parse,
            0,
            position_marker.text_to_parse[position_marker.index_number],
        )
        POGGER.debug(
            ">>position_marker.index_number>:$:<", position_marker.index_number
        )

        POGGER.debug(">>collected_to_index>:$:<", collected_to_index)
        assert collected_to_index is not None
        (
            after_whitespace_index,
            extra_whitespace_after_setext,
        ) = ParserHelper.extract_spaces(line_to_parse, collected_to_index)
        assert after_whitespace_index is not None
        assert extra_whitespace_after_setext is not None

        if not is_paragraph_continuation and after_whitespace_index == len(
            line_to_parse
        ):
            if split_tab:
                TabHelper.adjust_block_quote_indent_for_tab(parser_state)
            LeafBlockProcessor.__create_setext_token(
                parser_state,
                position_marker,
                collected_to_index + ex_ws_l,
                new_tokens,
                extracted_whitespace,
                extra_whitespace_after_setext,
            )
        return collected_to_index, after_whitespace_index, extra_whitespace_after_setext

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_continuation_for_active_list(
        parser_state: ParserState, position_marker: PositionMarker
    ) -> bool:
        is_paragraph_continuation: bool = (
            len(parser_state.token_stack) > 1 and parser_state.token_stack[-2].is_list
        )
        if is_paragraph_continuation:
            list_token = cast(ListStackToken, parser_state.token_stack[-2])
            POGGER.debug(
                "parser_state.original_line_to_parse>:$:<",
                parser_state.original_line_to_parse,
            )
            adj_text = position_marker.text_to_parse[position_marker.index_number :]
            assert parser_state.original_line_to_parse is not None
            assert parser_state.original_line_to_parse.endswith(adj_text)
            removed_text_length = len(parser_state.original_line_to_parse) - len(
                adj_text
            )
            POGGER.debug("removed_text_length>:$:<", removed_text_length)
            POGGER.debug("adj_text>:$:<", adj_text)
            POGGER.debug("indent_level>:$:<", list_token.indent_level)
            is_paragraph_continuation = (
                bool(adj_text) and removed_text_length < list_token.indent_level
            )
        return is_paragraph_continuation

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_setext_token(
        parser_state: ParserState,
        position_marker: PositionMarker,
        collected_to_index: int,
        new_tokens: List[MarkdownToken],
        extracted_whitespace: Optional[str],
        extra_whitespace_after_setext: Optional[str],
    ) -> None:
        token_index = len(parser_state.token_document) - 1
        while not parser_state.token_document[token_index].is_paragraph:
            token_index -= 1

        paragraph_token = cast(
            ParagraphMarkdownToken, parser_state.token_document[token_index]
        )
        assert paragraph_token.extra_data is not None
        replacement_token = SetextHeadingMarkdownToken(
            position_marker.text_to_parse[position_marker.index_number],
            collected_to_index - position_marker.index_number,
            paragraph_token.extra_data,
            position_marker,
            paragraph_token,
        )

        # This is unusual.  Normally, close_open_blocks is used to close off
        # blocks based on the stack token.  However, since the setext takes
        # the last paragraph of text (see case 61) and translates it
        # into a heading, this has to be done separately, as there is no
        # stack token to close.
        assert extra_whitespace_after_setext is not None
        assert extracted_whitespace is not None
        new_tokens.append(
            replacement_token.generate_close_markdown_token_from_markdown_token(
                extracted_whitespace, extra_whitespace_after_setext
            )
        )

        parser_state.token_document[token_index] = replacement_token
        del parser_state.token_stack[-1]

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def correct_for_leaf_block_start_in_list(
        parser_state: ParserState,
        removed_chars_at_start: int,
        old_top_of_stack_token: StackToken,
        html_tokens: List[MarkdownToken],
        was_token_already_added_to_stack: bool = True,
        delay_tab_match: bool = False,
    ) -> None:
        """
        Check to see that if a paragraph has been closed within a list and
        there is a leaf block token immediately following, that the right
        actions are taken.
        """

        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>removed_chars_at_start>$>>",
            removed_chars_at_start,
        )
        if not old_top_of_stack_token.is_paragraph:
            POGGER.debug("1")
            return

        statck_index, top_of_stack, end_of_list = (
            -2 if was_token_already_added_to_stack else -1,
            None,
            html_tokens[-1],
        )
        if not parser_state.token_stack[statck_index].is_list:
            POGGER.debug("2")
            return

        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
            parser_state.token_stack,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens>>$>>",
            parser_state.token_document,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

        if was_token_already_added_to_stack:
            top_of_stack = parser_state.token_stack[-1]
            del parser_state.token_stack[-1]
        del html_tokens[-1]

        LeafBlockProcessor.__handle_leaf_start(
            parser_state, removed_chars_at_start, html_tokens, delay_tab_match
        )

        if was_token_already_added_to_stack:
            assert top_of_stack is not None
            parser_state.token_stack.append(top_of_stack)
            POGGER.debug(
                ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
                parser_state.token_stack,
            )
        html_tokens.append(end_of_list)
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_leaf_start(
        parser_state: ParserState,
        removed_chars_at_start: int,
        html_tokens: List[MarkdownToken],
        delay_tab_match: bool,
    ) -> None:
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
            parser_state.token_stack,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

        adjust_with_leading_spaces = False
        is_remaining_list_token = True
        while is_remaining_list_token:
            assert parser_state.token_stack[-1].is_list
            list_stack_token = cast(ListStackToken, parser_state.token_stack[-1])

            POGGER.debug(">>removed_chars_at_start>>$>>", removed_chars_at_start)
            POGGER.debug(">>stack indent>>$>>", list_stack_token.indent_level)
            if removed_chars_at_start >= list_stack_token.indent_level:
                break  # pragma: no cover

            tokens_from_close, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=(len(parser_state.token_stack) - 1),
                include_lists=True,
            )
            adjust_with_leading_spaces = True
            POGGER.debug(
                ">>correct_for_leaf_block_start_in_list>>tokens_from_close>>$>>",
                tokens_from_close,
            )
            html_tokens.extend(tokens_from_close)

            is_remaining_list_token = parser_state.token_stack[-1].is_list

        if is_remaining_list_token:
            assert parser_state.token_stack[-1].is_list
            list_stack_token = cast(ListStackToken, parser_state.token_stack[-1])
            delta_indent = removed_chars_at_start - list_stack_token.indent_level
            POGGER.debug(
                ">>correct_for_leaf_block_start_in_list>>delta_indent>>$>>",
                delta_indent,
            )
            assert not delta_indent

            POGGER.debug(">>delay_tab_match>>$>>", delay_tab_match)
            # assert not delay_tab_match
            if adjust_with_leading_spaces:
                if delay_tab_match:
                    used_indent = ""
                else:
                    used_indent = ParserHelper.repeat_string(
                        " ", removed_chars_at_start
                    )
                assert list_stack_token.matching_markdown_token is not None
                list_markdown_token = cast(
                    ListStartMarkdownToken, list_stack_token.matching_markdown_token
                )
                list_markdown_token.add_leading_spaces(used_indent)

    @staticmethod
    def is_paragraph_ending_leaf_block_start(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        exclude_thematic_break: bool = False,
    ) -> bool:
        """
        Determine whether we have a valid leaf block start.
        """

        assert not exclude_thematic_break

        is_thematic_break_start, _ = LeafBlockProcessor.is_thematic_break(
            line_to_parse,
            start_index,
            extracted_whitespace,
            skip_whitespace_check=True,
        )
        is_leaf_block_start = bool(is_thematic_break_start)
        POGGER.debug(
            "is_paragraph_ending_leaf_block_start>>is_theme_break>>$",
            is_leaf_block_start,
        )
        if not is_leaf_block_start:
            is_html_block_start, _ = HtmlHelper.is_html_block(
                line_to_parse,
                start_index,
                extracted_whitespace,
                parser_state.token_stack,
            )
            is_leaf_block_start = bool(is_html_block_start)
            POGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_html_block>>$",
                is_leaf_block_start,
            )
        if not is_leaf_block_start:
            is_leaf_block_start, _, _, _, _ = LeafBlockProcessor.is_fenced_code_block(
                line_to_parse, start_index, extracted_whitespace
            )
            POGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_fenced_code_block>>$",
                is_leaf_block_start,
            )
        if not is_leaf_block_start:
            is_leaf_block_start, _, _, _ = LeafBlockProcessor.is_atx_heading(
                line_to_parse, start_index, extracted_whitespace
            )
            POGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_atx_heading>>$",
                is_leaf_block_start,
            )
        POGGER.debug(
            "is_paragraph_ending_leaf_block_start<<$",
            is_leaf_block_start,
        )
        return is_leaf_block_start

    # pylint: disable=too-many-arguments
    @staticmethod
    def handle_html_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        outer_processed: bool,
        leaf_token_whitespace: Optional[str],
        new_tokens: List[MarkdownToken],
        grab_bag: ContainerGrabBag,
    ) -> bool:
        """
        Take care of the processing for html blocks.
        """

        POGGER.debug(">>position_marker>>ttp>>$>>", position_marker.text_to_parse)
        POGGER.debug(">>position_marker>>in>>$>>", position_marker.index_number)
        POGGER.debug(">>position_marker>>ln>>$>>", position_marker.line_number)
        did_adjust_block_quote = False
        if not outer_processed and not parser_state.token_stack[-1].is_html_block:
            POGGER.debug(">>html started?>>")
            old_top_of_stack = parser_state.token_stack[-1]
            html_tokens, did_adjust_block_quote = HtmlHelper.parse_html_block(
                parser_state,
                position_marker,
                leaf_token_whitespace,
                grab_bag.block_quote_data,
                grab_bag.original_line,
            )
            if html_tokens:
                POGGER.debug(">>html started>>")
                LeafBlockProcessor.correct_for_leaf_block_start_in_list(
                    parser_state,
                    position_marker.index_indent,
                    old_top_of_stack,
                    html_tokens,
                )
            new_tokens.extend(html_tokens)
        if parser_state.token_stack[-1].is_html_block:
            POGGER.debug(">>html continued>>")
            assert leaf_token_whitespace is not None
            html_tokens = HtmlHelper.check_normal_html_block_end(
                parser_state,
                position_marker.text_to_parse,
                position_marker.index_number,
                leaf_token_whitespace,
                position_marker,
                grab_bag.original_line,
                did_adjust_block_quote,
            )
            assert html_tokens
            new_tokens.extend(html_tokens)
            outer_processed = True
        else:
            POGGER.debug(">>html not encountered>>")

        return outer_processed

    # pylint: enable=too-many-arguments

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
        ) = LeafBlockProcessor.parse_fenced_code_block(
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
                ) = LeafBlockProcessor.__handle_fenced_code_block_with_tab(
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
        # POGGER.debug("original_line>:$:<", original_line)
        # POGGER.debug("leaf_token_whitespace>:$:<", leaf_token_whitespace)
        # POGGER.debug("token_text>:$:<", token_text)

        fenced_stack_token = cast(
            FencedCodeBlockStackToken, parser_state.token_stack[-1]
        )
        whitespace_start_count = fenced_stack_token.whitespace_start_count
        # POGGER.debug("whitespace_start_count>:$:<", whitespace_start_count)
        was_indented = False
        if not parser_state.token_stack[-2].is_document:
            last_container_token = parser_state.token_stack[-2]
            # POGGER.debug("last_container_token>:$:<", last_container_token)
            assert last_container_token.is_block_quote
            # whitespace_start_count -= len(rttp)
            # POGGER.debug("whitespace_start_count>:$:<", whitespace_start_count)
            was_indented = True

        # POGGER.debug("leaf_token_whitespace>:$:<", leaf_token_whitespace)
        resolved_leaf_token_whitespace = ParserHelper.remove_all_from_text(
            leaf_token_whitespace
        )
        # POGGER.debug(
        #     "resolved_leaf_token_whitespace>:$:<", resolved_leaf_token_whitespace
        # )
        # POGGER.debug("token_text>:$:<", token_text)
        reconstructed_line = resolved_leaf_token_whitespace + token_text
        # POGGER.debug("original_line>:$:<", original_line)
        # POGGER.debug("reconstructed_line>:$:<", reconstructed_line)
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
        ) = LeafBlockProcessor.__handle_fenced_code_block_with_tab_whitespace(
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
        # POGGER.debug("adj_original>:$:<", adj_original)
        # POGGER.debug("adj_original_index>:$:<", adj_original_index)
        space_end_index, extracted_whitespace = ParserHelper.extract_spaces(
            adj_original, 0
        )
        # POGGER.debug("space_end_index>:$:<", space_end_index)
        # POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        assert extracted_whitespace is not None
        assert space_end_index != -1

        # POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        # POGGER.debug("adj_original_index>:$:<", adj_original_index)
        detabified_extracted_whitespace = TabHelper.detabify_string(
            extracted_whitespace, adj_original_index
        )
        # POGGER.debug(
        #     "detabified_extracted_whitespace>:$:<", detabified_extracted_whitespace
        # )
        assert detabified_extracted_whitespace == resolved_leaf_token_whitespace

        new_extracted_whitespace = extracted_whitespace
        # POGGER.debug("new_extracted_whitespace>:$:<", new_extracted_whitespace)
        if new_extracted_whitespace and whitespace_start_count:
            assert was_indented
            new_extracted_whitespace = LeafBlockProcessor.__handle_fenced_code_block_with_tab_and_extracted_whitespace(
                new_extracted_whitespace,
                adj_original_index,
                whitespace_start_count,
                extracted_whitespace,
            )

        # POGGER.debug("leaf_token_whitespace>:$:<", leaf_token_whitespace)
        # POGGER.debug("token_text>:$:<", token_text)
        if reconstructed_line_has_tab:
            leaf_token_whitespace = new_extracted_whitespace
        token_text = adj_original[space_end_index:]
        # POGGER.debug("leaf_token_whitespace>:$:<", leaf_token_whitespace)
        # POGGER.debug("token_text>:$:<", token_text)
        if split_tab:
            TabHelper.adjust_block_quote_indent_for_tab(parser_state)

        return leaf_token_whitespace, token_text

    # pylint: enable=too-many-arguments

    @staticmethod
    def close_indented_block_if_indent_not_there(
        parser_state: ParserState, leaf_token_whitespace: Optional[str]
    ) -> List[MarkdownToken]:
        """
        If we have an indented block going on and the current line does not
        support continuing that block, close it.
        """

        POGGER.debug(
            "__close_indented_block_if_indent_not_there>>$>",
            parser_state.token_stack[-1],
        )
        POGGER.debug("leaf_token_whitespace>>$>", leaf_token_whitespace)
        pre_tokens: List[MarkdownToken] = []
        assert leaf_token_whitespace is not None
        if parser_state.token_stack[
            -1
        ].is_indented_code_block and TabHelper.is_length_less_than_or_equal_to(
            leaf_token_whitespace, 3
        ):
            pre_tokens.append(
                parser_state.token_stack[
                    -1
                ].generate_close_markdown_token_from_stack_token()
            )
            del parser_state.token_stack[-1]

            extracted_blank_line_tokens = (
                LeafBlockProcessor.extract_markdown_tokens_back_to_blank_line(
                    parser_state, False
                )
            )
            extracted_blank_line_tokens.reverse()
            pre_tokens.extend(extracted_blank_line_tokens)
        POGGER.debug(
            "__close_indented_block_if_indent_not_there>>pre_tokens>$>", pre_tokens
        )
        return pre_tokens

    @staticmethod
    def extract_markdown_tokens_back_to_blank_line(
        parser_state: ParserState, was_forced: bool
    ) -> List[MarkdownToken]:
        """
        Extract tokens going back to the last blank line token.
        """

        pre_tokens: List[MarkdownToken] = []
        while parser_state.token_document[-1].is_blank_line:
            last_element = parser_state.token_document[-1]
            if was_forced:
                pre_tokens.insert(0, last_element)
            else:
                pre_tokens.append(last_element)
            del parser_state.token_document[-1]
        return pre_tokens
