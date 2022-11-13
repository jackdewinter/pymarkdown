"""
Module to provide processing for the leaf blocks.
"""
import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quote_data import BlockQuoteData
from pymarkdown.constants import Constants
from pymarkdown.container_grab_bag import ContainerGrabBag
from pymarkdown.container_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_block_processor_paragraph import LeafBlockProcessorParagraph
from pymarkdown.leaf_markdown_token import (
    AtxHeadingMarkdownToken,
    FencedCodeBlockMarkdownToken,
    IndentedCodeBlockMarkdownToken,
    ParagraphMarkdownToken,
    SetextHeadingMarkdownToken,
    ThematicBreakMarkdownToken,
)
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken
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
            or ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
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
            extracted_whitespace = (
                LeafBlockProcessor.__parse_fenced_code_block_already_in(
                    parser_state, extracted_whitespace
                )
            )
        return new_tokens, extracted_whitespace

    # pylint: enable=too-many-arguments

    @staticmethod
    def __parse_fenced_code_block_already_in(
        parser_state: ParserState, extracted_whitespace: Optional[str]
    ) -> Optional[str]:
        fenced_token = cast(FencedCodeBlockStackToken, parser_state.token_stack[-1])
        if fenced_token.whitespace_start_count and extracted_whitespace:
            current_whitespace_length = ParserHelper.calculate_length(
                extracted_whitespace
            )
            whitespace_left = max(
                0,
                current_whitespace_length - fenced_token.whitespace_start_count,
            )
            POGGER.debug("previous_ws>>$", current_whitespace_length)
            POGGER.debug("whitespace_left>>$", whitespace_left)
            removed_whitespace = ParserHelper.create_replace_with_nothing_marker(
                ParserHelper.repeat_string(
                    ParserHelper.space_character,
                    current_whitespace_length - whitespace_left,
                )
            )
            whitespace_padding = ParserHelper.repeat_string(
                ParserHelper.space_character, whitespace_left
            )
            extracted_whitespace = f"{removed_whitespace}{whitespace_padding}"
        return extracted_whitespace

    # pylint: disable=too-many-arguments, too-many-locals, too-many-statements
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
        if "\t" in original_line:
            before_fence_index = new_index - collected_count
            fence_string = line_to_parse[before_fence_index:new_index]
            POGGER.debug("fence_string>:$:<", fence_string)
            POGGER.debug("before_fence_index>:$:<", before_fence_index)
            POGGER.debug("after_fence_index>:$:<", after_fence_index)
            POGGER.debug("non_whitespace_index>:$:<", non_whitespace_index)
            POGGER.debug("original_line>:$:<", original_line)
            POGGER.debug("line_to_parse>:$:<", line_to_parse)
            adj_original_line, _, _ = ParserHelper.find_detabify_string(
                original_line, line_to_parse, use_proper_traverse=True
            )
            POGGER.debug("adj_original_line>:$:<", adj_original_line)
            if adj_original_line is None:
                # split
                POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)

                line_prefix = line_to_parse[:before_fence_index]
                line_suffix = line_to_parse[before_fence_index:after_fence_index]
                POGGER.debug("line_prefix>:$:<", line_prefix)
                POGGER.debug("line_suffix>:$:<", line_suffix)
                line_suffix_index = original_line.find(line_suffix)
                assert line_suffix_index != -1
                POGGER.debug("line_suffix_index>:$:<", line_suffix_index)
                adj_original_line = original_line[line_suffix_index:]
                prefix = original_line[:line_suffix_index]
                POGGER.debug("prefix>:$:<", prefix)
                POGGER.debug("adj_original_line>:$:<", adj_original_line)
                new_index = collected_count

            POGGER.debug("original_line>:$:<", original_line)
            POGGER.debug("fence_string>:$:<", fence_string)
            fence_string_index = original_line.find(fence_string)
            POGGER.debug("fence_string_index>:$:<", fence_string_index)
            assert fence_string_index != -1
            if prefix := original_line[:fence_string_index]:
                assert extracted_whitespace is not None
                (
                    corrected_prefix,
                    corrected_suffix,
                    split_tab,
                ) = ParserHelper.match_tabbed_whitespace(extracted_whitespace, prefix)
                POGGER.debug("corrected_prefix>:$:<", corrected_prefix)
                POGGER.debug("corrected_suffix>:$:<", corrected_suffix)
                extracted_whitespace = corrected_suffix
                corrected_prefix_length = len(corrected_prefix)
                POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
                POGGER.debug("corrected_prefix_length>:$:<", corrected_prefix_length)

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
        POGGER.debug(
            "extracted_whitespace_before_info_string>:$:<",
            extracted_whitespace_before_info_string,
        )
        return (
            line_to_parse,
            non_whitespace_index,
            extracted_whitespace_before_info_string,
            extracted_whitespace,
            split_tab,
            corrected_prefix_length,
        )

    # pylint: enable=too-many-arguments, too-many-locals, too-many-statements

    # pylint: disable=too-many-arguments, too-many-locals
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
        ) = LeafBlockProcessor.__add_fenced_tokens_with_tab(
            position_marker,
            original_line,
            new_index,
            non_whitespace_index,
            collected_count,
            extracted_whitespace,
            after_fence_index,
        )

        (_, proper_end_index,) = ParserHelper.collect_backwards_while_one_of_characters(
            line_to_parse, -1, Constants.ascii_whitespace
        )
        adjusted_string = line_to_parse[:proper_end_index]
        non_whitespace_index = min(non_whitespace_index, len(adjusted_string))
        (
            after_extracted_text_index,
            extracted_text,
        ) = ParserHelper.extract_until_spaces(adjusted_string, non_whitespace_index)
        assert extracted_text is not None
        text_after_extracted_text = line_to_parse[after_extracted_text_index:]

        old_top_of_stack = parser_state.token_stack[-1]
        new_tokens, _ = parser_state.close_open_blocks_fn(
            parser_state,
            only_these_blocks=[ParagraphStackToken],
        )

        whitespace_count_delta = 0
        if split_tab := LeafBlockProcessor.__reduce_containers_if_required(
            parser_state, block_quote_data, new_tokens, split_tab
        ):
            LeafBlockProcessorParagraph.adjust_block_quote_indent_for_tab(parser_state)
            whitespace_count_delta = -1

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
        whitespace_start_count = (
            ParserHelper.calculate_length(extracted_whitespace, corrected_prefix_length)
            + whitespace_count_delta
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

    # pylint: disable=too-many-locals
    @staticmethod
    def __check_for_fenced_end_with_tab(
        original_line: str,
        detabified_original_start_index: int,
        collected_count: int,
        extracted_whitespace: Optional[str],
    ) -> Tuple[int, bool, Optional[str], bool]:

        # POGGER.debug("original_line:$:", original_line)
        # POGGER.debug("detabified_original_start_index:$:", detabified_original_start_index)
        # POGGER.debug("collected_count:$:", collected_count)
        # POGGER.debug("extracted_whitespace:$:", extracted_whitespace)

        detabified_original_line = ParserHelper.detabify_string(original_line)
        # POGGER.debug("detabified_original_line:$:", detabified_original_line)
        adj_original_line = detabified_original_line[detabified_original_start_index:]
        POGGER.debug("adj_original_line:$:", adj_original_line)

        (
            after_fence_index,
            adj_end,
            fence_string,
        ) = LeafBlockProcessor.__calculate_fenced_vars(
            adj_original_line, collected_count, original_line
        )

        assert fence_string in original_line
        original_fence_string_index = original_line.find(fence_string)
        after_fence_in_original = original_line[
            original_fence_string_index + collected_count :
        ]

        _, after_space_in_original_index = ParserHelper.collect_while_character(
            after_fence_in_original, 0, " "
        )
        POGGER.debug(
            ">>after_space_in_original_index>:$:<", after_space_in_original_index
        )
        POGGER.debug(
            ">>after_fence_in_original($)>:$:<",
            len(after_fence_in_original),
            after_fence_in_original,
        )
        only_spaces_after_fence = after_space_in_original_index == len(
            after_fence_in_original
        )
        POGGER.debug(">>only_spaces_after_fence>:$:<", only_spaces_after_fence)

        assert extracted_whitespace is not None
        reconstructed_line = extracted_whitespace + adj_end
        POGGER.debug(">>original_line>:$:<", original_line)
        POGGER.debug(">>reconstructed_line>:$:<", reconstructed_line)
        adj_original, adj_original_index, _ = ParserHelper.find_detabify_string(
            original_line, reconstructed_line
        )
        POGGER.debug(">>adj_original>:$:<", adj_original)
        POGGER.debug(">>adj_original_index>:$:<", adj_original_index)
        split_tab = False
        if adj_original is None:
            reconstructed_line = f" {reconstructed_line}"
            POGGER.debug(">>reconstructed_line>:$:<", reconstructed_line)
            adj_original, adj_original_index, _ = ParserHelper.find_detabify_string(
                original_line, reconstructed_line
            )
            POGGER.debug(">>adj_original>:$:<", adj_original)
            POGGER.debug(">>adj_original_index>:$:<", adj_original_index)
            split_tab = True
        assert adj_original is not None

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

    # pylint: enable=too-many-locals

    @staticmethod
    def __calculate_fenced_vars(
        adj_original_line: str, collected_count: int, original_line: str
    ) -> Tuple[int, str, str]:
        after_whitespace_index, _ = ParserHelper.extract_spaces(adj_original_line, 0)
        assert after_whitespace_index is not None
        POGGER.debug("after_whitespace_index=$", after_whitespace_index)
        after_fence_index = after_whitespace_index + collected_count
        adj_end = adj_original_line[after_whitespace_index:]
        fence_string = adj_original_line[after_whitespace_index:after_fence_index]
        POGGER.debug("fence_string=$", fence_string)
        fence_string_index = original_line.find(fence_string)
        POGGER.debug("fence_string_index=$", fence_string_index)
        assert fence_string_index != -1
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
        POGGER.debug("pfcb->end")
        POGGER.debug("extracted_whitespace:$:", extracted_whitespace)
        POGGER.debug("position_marker.text_to_parse:$:", position_marker.text_to_parse)
        POGGER.debug(
            "len(position_marker.text_to_parse):$:", len(position_marker.text_to_parse)
        )
        POGGER.debug("after_fence_index:$:", after_fence_index)
        POGGER.debug(
            "detabified_original_start_index:$:", detabified_original_start_index
        )

        POGGER.debug("original_line:$:", original_line)
        only_spaces_after_fence = True
        split_tab = False
        if "\t" in original_line:
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
        POGGER.debug("after_fence_and_spaces_index:$:", after_fence_and_spaces_index)

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
                LeafBlockProcessorParagraph.adjust_block_quote_indent_for_tab(
                    parser_state
                )

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
                if next_character == "\t":
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
            err = ParserHelper.detabify_string(
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

    # pylint: disable=too-many-arguments, too-many-locals, too-many-statements
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
            ParserHelper.is_length_greater_than_or_equal_to(
                extracted_whitespace, 4, start_index=removed_chars_at_start
            )
            and not parser_state.token_stack[-1].is_paragraph
        ):
            POGGER.debug(
                "parse_indented_code_block>>start",
            )
            POGGER.debug("removed_chars_at_start>:$:<", removed_chars_at_start)
            POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
            POGGER.debug(
                "position_marker.text_to_parse>:$:<", position_marker.text_to_parse
            )
            POGGER.debug(
                "position_marker.text_to_parse[index_number=$]>:$:<",
                position_marker.index_number,
                position_marker.text_to_parse[position_marker.index_number :],
            )
            POGGER.debug("original_line>:$:<", original_line)

            indented_text = position_marker.text_to_parse[
                position_marker.index_number :
            ]

            POGGER.debug("last_block_quote_index>:$:<", last_block_quote_index)
            is_in_block_quote = last_block_quote_index > 0
            POGGER.debug("is_in_block_quote>:$:<", is_in_block_quote)

            POGGER.debug("last_list_start_index>:$:<", last_list_start_index)
            is_in_list = last_list_start_index > 0
            POGGER.debug("is_in_list>:$:<", is_in_list)

            tabified_extracted_space: Optional[str] = None
            xx_extracted_space = None
            xx_left_over = None
            adjust_block_quote_indent = False
            if "\t" in original_line:
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

            adj_ws = ""
            POGGER.debug("tabified_extracted_space>:$:<", tabified_extracted_space)
            if not parser_state.token_stack[-1].is_indented_code_block:
                POGGER.debug("xx_extracted_space>:$:<", xx_extracted_space)
                POGGER.debug("xx_left_over>:$:<", xx_left_over)
                (
                    last_block_quote_index,
                    extracted_whitespace,
                    adj_ws,
                    indented_text,
                ) = LeafBlockProcessor.__create_indented_block(
                    parser_state,
                    last_block_quote_index,
                    position_marker,
                    extracted_whitespace,
                    new_tokens,
                    tabified_extracted_space,
                    original_line,
                    is_in_list,
                    indented_text,
                    xx_extracted_space,
                    xx_left_over,
                )
            elif tabified_extracted_space:
                POGGER.debug("xx_extracted_space>:$:<", xx_extracted_space)
                POGGER.debug("xx_left_over>:$:<", xx_left_over)
                (_, adj_ws, left_ws,) = LeafBlockProcessor.__recalculate_whitespace(
                    extracted_whitespace, 0, tabified_extracted_space
                )
                POGGER.debug("adj_ws>:$:<", adj_ws)
                POGGER.debug("left_ws>:$:<", left_ws)
                extracted_whitespace = adj_ws

                adj_ws_length = len(adj_ws)
                indented_text = original_line[adj_ws_length:]
            elif xx_extracted_space is not None:
                POGGER.debug("xx_extracted_space>:$:<", xx_extracted_space)
                POGGER.debug("xx_left_over>:$:<", xx_left_over)
                extracted_whitespace = xx_extracted_space
                assert xx_left_over is not None
                indented_text = xx_left_over

            POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
            POGGER.debug("indented_text>:$:<", indented_text)

            if adjust_block_quote_indent:
                LeafBlockProcessorParagraph.adjust_block_quote_indent_for_tab(
                    parser_state
                )

            assert extracted_whitespace is not None
            new_tokens.append(
                TextMarkdownToken(
                    indented_text,
                    extracted_whitespace,
                    position_marker=position_marker,
                )
            )
        else:
            POGGER.debug(
                "parse_indented_code_block>>not eligible",
            )
        return new_tokens

    # pylint: enable=too-many-arguments, too-many-locals, too-many-statements

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __parse_indented_code_block_with_tab(
        parser_state: ParserState,
        position_marker: PositionMarker,
        is_in_list: bool,
        is_in_block_quote: bool,
        original_line: str,
        last_block_quote_index: int,
    ) -> Tuple[Optional[str], Optional[str], Optional[str], bool]:

        tabified_extracted_space: Optional[str] = None
        xx_extracted_space = None
        xx_left_over = None
        adjust_block_quote_indent = False

        if not is_in_list and not is_in_block_quote:
            next_character = position_marker.text_to_parse[position_marker.index_number]
            next_character_index = original_line.find(next_character)
            assert next_character_index != -1
            tabified_extracted_space = original_line[:next_character_index]
            POGGER.debug("tabified_extracted_space>:$:<", tabified_extracted_space)
        else:
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
            POGGER.debug("after_space_index>:$:<", after_space_index)
            POGGER.debug("ex_space>:$:<", ex_space)
            assert ex_space is not None
            detabified_ex_space = ParserHelper.detabify_string(
                ex_space, additional_start_delta=lead_space_len
            )
            POGGER.debug("detabified_ex_space>:$:<", detabified_ex_space)
            # assert detabified_ex_space == extracted_whitespace
            last_good_space_index = -1
            space_index = 1
            detabified_ex_space = ""
            while space_index < len(ex_space) + 1 and len(detabified_ex_space) < 4:
                POGGER.debug("space_index>:$:<", space_index)
                last_good_space_index = space_index
                space_prefix = ex_space[:space_index]
                POGGER.debug("sdf>:$:<", space_prefix)
                POGGER.debug("lead_space_len>:$:<", lead_space_len)
                detabified_ex_space = ParserHelper.detabify_string(
                    space_prefix, additional_start_delta=lead_space_len
                )
                POGGER.debug("detabified_ex_space>:$:<", detabified_ex_space)
                space_index += 1
            assert len(detabified_ex_space) >= 4
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
        return (
            tabified_extracted_space,
            xx_extracted_space,
            xx_left_over,
            adjust_block_quote_indent,
        )

    # pylint: enable=too-many-arguments, too-many-locals

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
        last_block_quote_lead_spaces = last_block_quote_token.leading_spaces
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
        if trailing_char_in_original == "\t":
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

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __create_indented_block(
        parser_state: ParserState,
        last_block_quote_index: int,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        new_tokens: List[MarkdownToken],
        tabified_extracted_space: Optional[str],
        original_line: str,
        is_in_list: bool,
        indented_text: str,
        xx_extracted_space: Optional[str],
        xx_left_over: Optional[str],
    ) -> Tuple[int, Optional[str], str, str]:

        _ = is_in_list
        # if is_in_list:
        #     tabified_extracted_space = None

        assert extracted_whitespace is not None
        line_number, column_number = position_marker.line_number, (
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

        new_token = IndentedCodeBlockMarkdownToken(adj_ws, line_number, column_number)
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
        return last_block_quote_index, extracted_whitespace, adj_ws, indented_text

    # pylint: enable=too-many-arguments, too-many-locals

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
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
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
            if "\t" in original_line:
                (
                    token_text,
                    split_tab,
                    extracted_whitespace,
                ) = ParserHelper.parse_thematic_break_with_tab(
                    original_line, token_text, extracted_whitespace
                )
            if split_tab := LeafBlockProcessor.__reduce_containers_if_required(
                parser_state, block_quote_data, new_tokens, split_tab
            ):
                LeafBlockProcessorParagraph.adjust_block_quote_indent_for_tab(
                    parser_state
                )
            LeafBlockProcessor.__reduce_containers_if_required(
                parser_state, block_quote_data, new_tokens, split_tab
            )

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
    def __reduce_containers_if_required(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        new_tokens: List[MarkdownToken],
        split_tab: bool,
    ) -> bool:

        POGGER.debug(
            "block_quote_data.current_count>>:$:<", block_quote_data.current_count
        )
        POGGER.debug("block_quote_data.stack_count>>:$:<", block_quote_data.stack_count)
        POGGER.debug("new_tokens>>:$:<", new_tokens)
        POGGER.debug("split_tab>>:$:<", split_tab)
        assert block_quote_data.current_count != 0 or block_quote_data.stack_count <= 0
        POGGER.debug("parser_state.token_stack[-1]>>:$:<", parser_state.token_stack[-1])
        # While? needs to take lists into account as well
        if (
            block_quote_data.current_count > 0
            and block_quote_data.stack_count > block_quote_data.current_count
            and parser_state.token_stack[-1].is_block_quote
        ):
            x_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                include_block_quotes=True,
                was_forced=True,
                until_this_index=len(parser_state.token_stack) - 1,
            )
            POGGER.debug("x_tokens>>:$:<", x_tokens)
            assert len(x_tokens) == 1
            first_new_token = cast(EndMarkdownToken, x_tokens[0])

            matching_start_token = cast(
                BlockQuoteMarkdownToken, first_new_token.start_markdown_token
            )
            POGGER.debug(
                "start_markdown_token.leading>>:$:<",
                matching_start_token.leading_spaces,
            )
            assert matching_start_token.leading_spaces is not None
            last_newline_index = matching_start_token.leading_spaces.rfind("\n")
            assert last_newline_index != -1
            # if last_newline_index == -1:
            #     tz =matching_start_token.leading_spaces
            # else:
            last_newline_part = matching_start_token.leading_spaces[
                last_newline_index + 1 :
            ]
            POGGER.debug("last_newline_part>>:$:<", last_newline_part)
            if split_tab:
                assert last_newline_part.endswith(" ")
                last_newline_part = last_newline_part[:-1]
                POGGER.debug("last_newline_part>>:$:<", last_newline_part)
                split_tab = False
            POGGER.debug("split_tab>>:$:<", split_tab)

            POGGER.debug("extra_end_data>>:$:<", first_new_token.extra_end_data)
            assert first_new_token.extra_end_data is None

            assert last_newline_part is not None
            first_new_token.set_extra_end_data(last_newline_part)

            new_tokens.extend(x_tokens)
        return split_tab

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
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
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

    # pylint: disable=too-many-locals
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
        if heading_found:
            assert extracted_whitespace_at_start is not None
            POGGER.debug(
                "parse_atx_headings>>start",
            )

            assert non_whitespace_index is not None
            (
                old_top_of_stack,
                remaining_line,
                remove_trailing_count,
                extracted_whitespace_before_end,
                extracted_whitespace_at_end,
                new_tokens,
                extracted_whitespace_at_start,
                extracted_whitespace,
            ) = LeafBlockProcessor.__prepare_for_create_atx_heading(
                parser_state,
                position_marker,
                [],
                non_whitespace_index,
                original_line,
                extracted_whitespace_at_start,
                extracted_whitespace,
                hash_count,
                block_quote_data,
            )
            assert hash_count is not None
            assert extracted_whitespace is not None
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
        else:
            POGGER.debug(
                "parse_atx_headings>>not eligible",
            )
            new_tokens = []
        return new_tokens

    # pylint: enable=too-many-locals

    @staticmethod
    def __prepare_for_create_atx_heading_with_tab(
        original_line: str,
        remaining_line: str,
        extracted_whitespace_at_start: str,
        extracted_whitespace: str,
        hash_count: int,
    ) -> Tuple[str, str, str, bool]:

        reconstructed_line = (
            extracted_whitespace
            + ParserHelper.repeat_string("#", hash_count)
            + extracted_whitespace_at_start
            + remaining_line
        )

        POGGER.debug(
            ">>extracted_whitespace_at_start>:$:<", extracted_whitespace_at_start
        )
        POGGER.debug(">>extracted_whitespace>:$:<", extracted_whitespace)
        POGGER.debug(">>original_line>:$:<", original_line)
        POGGER.debug(">>reconstructed_line>:$:<", reconstructed_line)
        adj_original, _, adj_original_index = ParserHelper.find_detabify_string(
            original_line, reconstructed_line, use_proper_traverse=True
        )
        POGGER.debug(">>adj_original>:$:<", adj_original)
        POGGER.debug(">>adj_original_index>:$:<", adj_original_index)
        split_tab = False
        POGGER.debug("split_tab>:$:<", split_tab)
        if adj_original is None:
            # Need to split this tab between two areas.
            reconstructed_line = f" {reconstructed_line}"
            POGGER.debug(">>reconstructed_line>:$:<", reconstructed_line)
            adj_original, _, adj_original_index = ParserHelper.find_detabify_string(
                original_line, reconstructed_line, use_proper_traverse=True
            )
            POGGER.debug(">>adj_original>:$:<", adj_original)
            POGGER.debug(">>adj_original_index>:$:<", adj_original_index)
            split_tab = True
            POGGER.debug("split_tab>:$:<", split_tab)
        assert adj_original is not None

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

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __prepare_for_create_atx_heading(
        parser_state: ParserState,
        position_marker: PositionMarker,
        new_tokens: List[MarkdownToken],
        non_whitespace_index: int,
        original_line: str,
        extracted_whitespace_at_start: str,
        extracted_whitespace: Optional[str],
        hash_count: Optional[int],
        block_quote_data: BlockQuoteData,
    ) -> Tuple[StackToken, str, int, str, str, List[MarkdownToken], str, Optional[str]]:

        (
            old_top_of_stack,
            remaining_line,
            remove_trailing_count,
            extracted_whitespace_before_end,
        ) = (
            parser_state.token_stack[-1],
            position_marker.text_to_parse[non_whitespace_index:],
            0,
            "",
        )
        POGGER.debug("remaining_line>:$:<", remaining_line)
        POGGER.debug("original_line>:$:<", original_line)
        if "\t" in original_line:
            assert extracted_whitespace is not None
            assert hash_count is not None
            (
                remaining_line,
                extracted_whitespace_at_start,
                extracted_whitespace,
                split_tab,
            ) = LeafBlockProcessor.__prepare_for_create_atx_heading_with_tab(
                original_line,
                remaining_line,
                extracted_whitespace_at_start,
                extracted_whitespace,
                hash_count,
            )
        else:
            split_tab = False
        POGGER.debug("split_tab>:$:<", split_tab)

        new_tokens, _ = parser_state.close_open_blocks_fn(parser_state)
        POGGER.debug("new_tokens>:$:<", new_tokens)
        if split_tab := LeafBlockProcessor.__reduce_containers_if_required(
            parser_state, block_quote_data, new_tokens, split_tab
        ):
            LeafBlockProcessorParagraph.adjust_block_quote_indent_for_tab(parser_state)

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
            old_top_of_stack,
            remaining_line,
            remove_trailing_count,
            extracted_whitespace_before_end,
            extracted_whitespace_at_end,
            new_tokens,
            extracted_whitespace_at_start,
            extracted_whitespace,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __parse_setext_headings_with_tab(
        original_line: str, line_to_parse: str, extracted_whitespace: str
    ) -> Tuple[str, str, bool]:

        POGGER.debug(">>extracted_whitespace>:$:<", extracted_whitespace)
        POGGER.debug(">>line_to_parse>:$:<", line_to_parse)
        reconstructed_line_to_parse = extracted_whitespace + line_to_parse
        POGGER.debug(">>reconstructed_line>:$:<", reconstructed_line_to_parse)

        POGGER.debug(">>original_line>:$:<", original_line)
        adj_original, _, _ = ParserHelper.find_detabify_string(
            original_line, reconstructed_line_to_parse
        )
        if split_tab := adj_original is None:
            POGGER.debug("split_tab>:$:<", split_tab)
            # Need to split this tab between two areas.
            reconstructed_line_to_parse = f" {reconstructed_line_to_parse}"
            POGGER.debug(
                ">>reconstructed_line_to_parse>:$:<", reconstructed_line_to_parse
            )
            adj_original, adj_original_index, _ = ParserHelper.find_detabify_string(
                original_line, reconstructed_line_to_parse
            )
            POGGER.debug(">>adj_original>:$:<", adj_original)
            POGGER.debug(">>adj_original_index>:$:<", adj_original_index)
        assert adj_original is not None

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
            ParserHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
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
            if "\t" in original_line:
                (
                    line_to_parse,
                    extracted_whitespace,
                    split_tab,
                ) = LeafBlockProcessor.__parse_setext_headings_with_tab(
                    original_line, line_to_parse, extracted_whitespace
                )

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

            if not is_paragraph_continuation and after_whitespace_index == len(
                line_to_parse
            ):
                if split_tab:
                    LeafBlockProcessorParagraph.adjust_block_quote_indent_for_tab(
                        parser_state
                    )
                LeafBlockProcessor.__create_setext_token(
                    parser_state,
                    position_marker,
                    collected_to_index + ex_ws_l,
                    new_tokens,
                    extracted_whitespace,
                    extra_whitespace_after_setext,
                )
        else:
            POGGER.debug(
                "parse_setext_headings>>not eligible",
            )
        return new_tokens

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

    @staticmethod
    def correct_for_leaf_block_start_in_list(
        parser_state: ParserState,
        removed_chars_at_start: int,
        old_top_of_stack_token: StackToken,
        html_tokens: List[MarkdownToken],
        was_token_already_added_to_stack: bool = True,
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
            parser_state, removed_chars_at_start, html_tokens
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

    @staticmethod
    def __handle_leaf_start(
        parser_state: ParserState,
        removed_chars_at_start: int,
        html_tokens: List[MarkdownToken],
    ) -> None:
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>stack>>$>>",
            parser_state.token_stack,
        )
        POGGER.debug(
            ">>correct_for_leaf_block_start_in_list>>tokens_to_add>>$>>", html_tokens
        )

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

        is_leaf_block_start = not exclude_thematic_break
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
                LeafBlockProcessor.__reduce_containers_if_required,
                LeafBlockProcessorParagraph.adjust_block_quote_indent_for_tab,
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
                LeafBlockProcessorParagraph.adjust_block_quote_indent_for_tab,
            )
            assert html_tokens
            new_tokens.extend(html_tokens)
            outer_processed = True
        else:
            POGGER.debug(">>html not encountered>>")

        return outer_processed

    # pylint: enable=too-many-arguments
