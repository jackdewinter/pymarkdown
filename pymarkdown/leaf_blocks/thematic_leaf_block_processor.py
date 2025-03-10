"""
Module to provide processing for thematic break leaf blocks.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.container_blocks.container_helper import ContainerHelper
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.leaf_blocks.leaf_block_helper import LeafBlockHelper
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.stack_token import (
    ListStackToken,
    ParagraphStackToken,
    StackToken,
)
from pymarkdown.tokens.thematic_break_markdown_token import ThematicBreakMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class ThematicLeafBlockProcessor:
    """
    Module to provide processing for thematic break leaf blocks.
    """

    __thematic_break_characters = "*_-"

    @staticmethod
    def is_thematic_break(
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: str,
        skip_whitespace_check: bool = False,
        whitespace_allowed_between_characters: bool = True,
    ) -> Tuple[Optional[str], Optional[int]]:
        """
        Determine whether or not we have a thematic break.
        """

        thematic_break_character, end_of_break_index = None, None
        is_thematic_character = ParserHelper.is_character_at_index_one_of(
            line_to_parse,
            start_index,
            ThematicLeafBlockProcessor.__thematic_break_characters,
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
    def __handle_existing_paragraph_special(
        parser_state: ParserState,
        grab_bag: ContainerGrabBag,
        new_tokens: List[MarkdownToken],
    ) -> None:
        if (
            not parser_state.token_stack[-1].is_list
            or grab_bag.text_removed_by_container is None
        ):
            return
        stack_list_token = cast(ListStackToken, parser_state.token_stack[-1])
        indent_delta = stack_list_token.indent_level - len(
            grab_bag.text_removed_by_container
        )
        if indent_delta > 0:
            stack_index = len(parser_state.token_stack) - 1
            best_stack_index = -1
            while stack_index > 0 and parser_state.token_stack[stack_index].is_list:
                new_list_stack_token = cast(
                    ListStackToken, parser_state.token_stack[stack_index]
                )
                new_indent_delta = new_list_stack_token.indent_level - len(
                    grab_bag.text_removed_by_container
                )
                if new_indent_delta <= 0:
                    break
                best_stack_index = stack_index
                stack_index -= 1
            assert best_stack_index != -1
            closed_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                was_forced=True,
                include_lists=True,
                until_this_index=best_stack_index,
            )
            new_tokens.extend(closed_tokens)
            # if parser_state.token_stack[-1].is_list:
            #     list_token = cast(
            #         ListStartMarkdownToken,
            #         parser_state.token_stack[-1].matching_markdown_token,
            #     )
            #     assert ">" in grab_bag.text_removed_by_container
            #     bq_start_index = grab_bag.text_removed_by_container.rindex(">")
            #     assert bq_start_index != len(grab_bag.text_removed_by_container) - 1
            #     # real_indent_delta = len(grab_bag.text_removed_by_container) - (
            #     #     bq_start_index + 2
            #     # )
            #     # list_token.add_leading_spaces(" " * real_indent_delta)

    @staticmethod
    def __handle_existing_paragraph(
        parser_state: ParserState,
        grab_bag: ContainerGrabBag,
        new_tokens: List[MarkdownToken],
        block_quote_data: BlockQuoteData,
    ) -> List[MarkdownToken]:
        force_paragraph_close_if_present = (
            block_quote_data.current_count == 0 and block_quote_data.stack_count > 0
        )
        new_tokens, _ = parser_state.close_open_blocks_fn(
            parser_state,
            only_these_blocks=[ParagraphStackToken],
            was_forced=force_paragraph_close_if_present,
        )
        if new_tokens and grab_bag.text_removed_by_container:
            ThematicLeafBlockProcessor.__handle_existing_paragraph_special(
                parser_state, grab_bag, new_tokens
            )
        return new_tokens

    @staticmethod
    def __handle_special_case(
        parser_state: ParserState, new_tokens: List[MarkdownToken]
    ) -> None:
        if (
            new_tokens
            and new_tokens[-1].is_list_end
            and parser_state.token_stack[-1].is_block_quote
        ):
            stack_index = len(parser_state.token_stack) - 1
            while stack_index > 0 and not parser_state.token_stack[stack_index].is_list:
                stack_index -= 1
            if stack_index != 0:
                list_end_token = cast(EndMarkdownToken, new_tokens[-1])
                last_list_markdown_token = cast(
                    ListStartMarkdownToken, list_end_token.start_markdown_token
                )
                if last_list_markdown_token.leading_spaces is not None:
                    inner_list_markdown_token = cast(
                        ListStartMarkdownToken,
                        parser_state.token_stack[stack_index].matching_markdown_token,
                    )
                    POGGER.debug(
                        "__handle_special_case>>last_list_markdown_token>>$",
                        last_list_markdown_token,
                    )
                    leading_space_to_move = (
                        last_list_markdown_token.remove_last_leading_space()
                    )
                    POGGER.debug(
                        "__handle_special_case>>last_list_markdown_token>>$",
                        last_list_markdown_token,
                    )
                    assert leading_space_to_move is not None
                    POGGER.debug(
                        "__handle_special_case>>list_token>>$",
                        inner_list_markdown_token,
                    )
                    if leading_space_to_move:
                        leading_space_to_move += ParserLogger.blah_sequence
                    inner_list_markdown_token.add_leading_spaces(leading_space_to_move)
                    POGGER.debug(
                        "__handle_special_case>>list_token>>$",
                        inner_list_markdown_token,
                    )

    @staticmethod
    def parse_thematic_break(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: str,
        block_quote_data: BlockQuoteData,
        original_line: str,
        grab_bag: ContainerGrabBag,
    ) -> List[MarkdownToken]:
        """
        Handle the parsing of a thematic break.
        """

        ex_ws = LeafBlockHelper.realize_leading_whitespace(
            parser_state, position_marker, extracted_whitespace, original_line
        )
        new_tokens: List[MarkdownToken] = []
        start_char, index = ThematicLeafBlockProcessor.is_thematic_break(
            position_marker.text_to_parse,
            position_marker.index_number,
            ex_ws,
        )
        if start_char:
            old_top_of_stack = parser_state.token_stack[-1]

            POGGER.debug(
                "parse_thematic_break>>start",
            )
            if parser_state.token_stack[-1].is_paragraph:
                new_tokens = ThematicLeafBlockProcessor.__handle_existing_paragraph(
                    parser_state, grab_bag, new_tokens, block_quote_data
                )

            ThematicLeafBlockProcessor.__handle_special_case(parser_state, new_tokens)

            token_text = position_marker.text_to_parse[
                position_marker.index_number : index
            ]
            # POGGER.debug("extracted_whitespace>>:$:<", extracted_whitespace)
            # POGGER.debug("token_text>>:$:<", token_text)
            # POGGER.debug("original_line>>:$:<", original_line)
            split_tab, split_tab_with_block_quote_suffix = False, False
            extra_whitespace_prefix: Optional[str] = None
            if ParserHelper.tab_character in original_line:
                (
                    token_text,
                    split_tab,
                    split_tab_with_block_quote_suffix,
                    extra_whitespace_prefix,
                    extracted_whitespace,
                    _,
                ) = TabHelper.parse_thematic_break_with_tab(
                    original_line, token_text, extracted_whitespace
                )
                # POGGER.debug("extra_whitespace_prefix>>:$:<", extra_whitespace_prefix)
                # POGGER.debug("extracted_whitespace>>:$:<", extracted_whitespace)

            extracted_whitespace = ThematicLeafBlockProcessor.__perform_adjusts(
                parser_state,
                position_marker,
                extra_whitespace_prefix,
                extracted_whitespace,
                old_top_of_stack,
                new_tokens,
                start_char,
                token_text,
                block_quote_data,
                split_tab,
                split_tab_with_block_quote_suffix,
                grab_bag,
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
    def __perform_adjusts(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extra_whitespace_prefix: Optional[str],
        extracted_whitespace: str,
        old_top_of_stack: StackToken,
        new_tokens: List[MarkdownToken],
        start_char: str,
        token_text: str,
        block_quote_data: BlockQuoteData,
        split_tab: bool,
        split_tab_with_block_quote_suffix: bool,
        grab_bag: ContainerGrabBag,
    ) -> str:
        if split_tab and not split_tab_with_block_quote_suffix:
            ThematicLeafBlockProcessor.__parse_thematic_break_with_suffix(
                parser_state,
                position_marker,
                extra_whitespace_prefix,
                extracted_whitespace,
                old_top_of_stack,
                new_tokens,
                start_char,
                token_text,
                block_quote_data,
            )
        else:
            split_tab, extracted_whitespace, whitespace_prefix = (
                ContainerHelper.reduce_containers_if_required(
                    parser_state,
                    position_marker,
                    block_quote_data,
                    new_tokens,
                    split_tab,
                    extracted_whitespace,
                    grab_bag,
                )
            )
            if split_tab:
                TabHelper.adjust_block_quote_indent_for_tab(parser_state)
        return extracted_whitespace

    @staticmethod
    def __parse_thematic_break_with_suffix(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extra_whitespace_prefix: Optional[str],
        extracted_whitespace: str,
        old_top_of_stack: StackToken,
        new_tokens: List[MarkdownToken],
        start_char: str,
        token_text: str,
        block_quote_data: BlockQuoteData,
    ) -> None:
        POGGER.debug("parser_state.token_stack[-1]>>:$:<", parser_state.token_stack[-1])
        POGGER.debug("parser_state.token_stack>>:$:<", parser_state.token_stack)
        POGGER.debug("parser_state.token_document>>:$:<", parser_state.token_document)
        assert parser_state.token_stack[
            -1
        ].is_list, "This should only be a list container."
        modified_whitespace = (
            extra_whitespace_prefix + extracted_whitespace
            if extra_whitespace_prefix is not None
            else extracted_whitespace
        )
        TabHelper.adjust_block_quote_indent_for_tab(parser_state, modified_whitespace)
        POGGER.debug("parser_state.token_stack>>:$:<", parser_state.token_stack)
        POGGER.debug("parser_state.token_document>>:$:<", parser_state.token_document)
        LeafBlockHelper.correct_for_leaf_block_start_in_list(
            parser_state,
            position_marker.index_indent,
            old_top_of_stack,
            new_tokens,
            block_quote_data,
            was_token_already_added_to_stack=False,
            delay_tab_match=True,
        )
        POGGER.debug("parser_state.token_stack>>:$:<", parser_state.token_stack)
        POGGER.debug("parser_state.token_document>>:$:<", parser_state.token_document)
        POGGER.debug("new_tokens>>:$:<", new_tokens)

        POGGER.debug("start_char>>:$:<", start_char)
        POGGER.debug("extracted_whitespace>>:$:<", extracted_whitespace)
        POGGER.debug("token_text>>:$:<", token_text)
