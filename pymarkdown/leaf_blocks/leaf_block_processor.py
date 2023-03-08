"""
Module to provide processing for the leaf blocks.
"""
import logging
from typing import List, Optional

from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.html.html_helper import HtmlHelper
from pymarkdown.leaf_blocks.atx_leaf_block_processor import AtxLeafBlockProcessor
from pymarkdown.leaf_blocks.fenced_leaf_block_processor import FencedLeafBlockProcessor
from pymarkdown.leaf_blocks.leaf_block_helper import LeafBlockHelper
from pymarkdown.leaf_blocks.thematic_leaf_block_processor import (
    ThematicLeafBlockProcessor,
)
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tab_helper import TabHelper

POGGER = ParserLogger(logging.getLogger(__name__))


class LeafBlockProcessor:
    """
    Class to provide processing for the leaf blocks.
    """

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

        is_thematic_break_start, _ = ThematicLeafBlockProcessor.is_thematic_break(
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
            (
                is_leaf_block_start,
                _,
                _,
                _,
                _,
            ) = FencedLeafBlockProcessor.is_fenced_code_block(
                line_to_parse, start_index, extracted_whitespace
            )
            POGGER.debug(
                "is_paragraph_ending_leaf_block_start>>is_fenced_code_block>>$",
                is_leaf_block_start,
            )
        if not is_leaf_block_start:
            is_leaf_block_start, _, _, _ = AtxLeafBlockProcessor.is_atx_heading(
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
                LeafBlockHelper.correct_for_leaf_block_start_in_list(
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
                LeafBlockHelper.extract_markdown_tokens_back_to_blank_line(
                    parser_state, False
                )
            )
            extracted_blank_line_tokens.reverse()
            pre_tokens.extend(extracted_blank_line_tokens)
        POGGER.debug(
            "__close_indented_block_if_indent_not_there>>pre_tokens>$>", pre_tokens
        )
        return pre_tokens
