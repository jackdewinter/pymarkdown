"""
Module to provide processing for the handling of leaf elements within container blocks.
"""

from __future__ import annotations

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.leaf_blocks.atx_leaf_block_processor import AtxLeafBlockProcessor
from pymarkdown.leaf_blocks.fenced_leaf_block_processor import FencedLeafBlockProcessor
from pymarkdown.leaf_blocks.indented_leaf_block_processor import (
    IndentedLeafBlockProcessor,
)
from pymarkdown.leaf_blocks.leaf_block_processor import LeafBlockProcessor
from pymarkdown.leaf_blocks.leaf_block_processor_paragraph import (
    LeafBlockProcessorParagraph,
)
from pymarkdown.leaf_blocks.setext_leaf_block_processor import SetextLeafBlockProcessor
from pymarkdown.leaf_blocks.table_block_processor import TableBlockHelper
from pymarkdown.leaf_blocks.thematic_leaf_block_processor import (
    ThematicLeafBlockProcessor,
)
from pymarkdown.links.link_reference_definition_helper import (
    LinkReferenceDefinitionHelper,
)
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import ListStackToken

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines
# pylint: disable=too-few-public-methods


class ContainerBlockLeafProcessor:
    """
    Class to provide processing for the handling of leaf elements within container blocks.
    """

    @staticmethod
    def handle_leaf_tokens(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        """
        Handle the handoff between processing containers and the leaf tokens.
        """
        assert (
            parser_state.original_line_to_parse is not None
        ), "Original line should be defined by this point."
        calculated_indent = len(parser_state.original_line_to_parse) - len(
            grab_bag.line_to_parse
        )
        # POGGER.debug(">>indent>>$", calculated_indent)

        assert not (
            grab_bag.indent_used_by_list
            and ">" in grab_bag.indent_used_by_list
            and parser_state.token_stack[-1].is_paragraph
            and parser_state.token_stack[-2].is_block_quote
        ), "This sequence should have been dealt with before here."

        POGGER.debug("ttp>>:$:<", position_marker.text_to_parse)
        POGGER.debug("index_number>>:$:<", position_marker.index_number)
        POGGER.debug("index_indent>>:$:<", position_marker.index_indent)
        newer_position_marker = PositionMarker(
            position_marker.line_number,
            0,
            grab_bag.line_to_parse,
            index_indent=calculated_indent,
        )
        POGGER.debug("ttp>>:$:<", newer_position_marker.text_to_parse)
        POGGER.debug("index_number>>:$:<", newer_position_marker.index_number)
        POGGER.debug("index_indent>>:$:<", newer_position_marker.index_indent)
        parser_state.mark_for_leaf_processing(grab_bag.container_tokens)

        top_of_stack = parser_state.token_stack[-1]
        ContainerBlockLeafProcessor.__process_leaf_tokens(
            parser_state,
            newer_position_marker,
            grab_bag,
        )
        if grab_bag.requeue_line_info:
            parser_state.abc(grab_bag.requeue_line_info, top_of_stack)

        parser_state.clear_after_leaf_processing()

        grab_bag.extend_container_tokens_with_leaf_tokens()

    @staticmethod
    def __process_leaf_tokens(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        """
        Main entry point from the ContainerBlockProcessor for processing leaf tokens.
        """
        assert (
            grab_bag.is_leaf_tokens_empty()
        ), "No leaf tokens should be present at this point."
        POGGER.debug("parsing leaf>>")
        # if xposition_marker.index_number != 0 and grab_bag.removed_chars_at_start_of_line:
        #     ff = False
        #     assert ff
        position_marker = PositionMarker(
            xposition_marker.line_number,
            0,
            xposition_marker.text_to_parse,
            index_indent=xposition_marker.index_indent,
        )
        # POGGER.debug("position_marker.text>>:$:<<", position_marker.text_to_parse)
        # POGGER.debug("position_marker.index>>:$:<<", position_marker.index_number)
        # POGGER.debug("position_marker.indent>>:$:<<", position_marker.index_indent)

        (
            new_index_number,
            extracted_leaf_whitespace,
        ) = ParserHelper.extract_spaces_verified(position_marker.text_to_parse, 0)

        total_ws = new_index_number + position_marker.index_indent

        last_block_index = parser_state.find_last_block_quote_on_stack()
        last_list_index = parser_state.find_last_list_block_on_stack()

        ContainerBlockLeafProcessor.__handle_special_block_quote_reduction(
            parser_state,
            last_block_index,
            last_list_index,
            grab_bag,
        )
        if grab_bag.requeue_line_info:
            POGGER.debug("requeuing after __handle_special_block_quote_reduction")
            assert (
                grab_bag.is_leaf_tokens_empty()
            ), "No leaf tokens should be present at this point."
            return

        POGGER.debug("position_marker.text>>:$:<<", position_marker.text_to_parse)
        POGGER.debug("position_marker.index>>:$:<<", position_marker.index_number)
        POGGER.debug("position_marker.indent>>:$:<<", position_marker.index_indent)
        (
            adjust_token,
            position_marker,
            extracted_leaf_whitespace,
            grab_bag.text_removed_by_container,
        ) = ContainerBlockLeafProcessor.__adjust_for_inner_list_container(
            parser_state,
            last_block_index,
            last_list_index,
            position_marker,
            grab_bag.text_removed_by_container,
            extracted_leaf_whitespace,
        )
        orig_text_removed_by_container = grab_bag.text_removed_by_container

        POGGER.debug("position_marker.text>>:$:<<", position_marker.text_to_parse)
        POGGER.debug("position_marker.index>>:$:<<", position_marker.index_number)
        POGGER.debug("position_marker.indent>>:$:<<", position_marker.index_indent)
        (
            removed_leading_space,
            actual_removed_leading_space,
            position_marker,
            new_ex,
        ) = ContainerBlockLeafProcessor.__adjust_for_list_container(
            parser_state,
            position_marker,
            last_block_index,
            last_list_index,
            extracted_leaf_whitespace,
            grab_bag,
        )

        POGGER.debug("position_marker.text>>:$:<<", position_marker.text_to_parse)
        POGGER.debug("position_marker.index>>:$:<<", position_marker.index_number)
        POGGER.debug("position_marker.indent>>:$:<<", position_marker.index_indent)
        POGGER.debug("is_leaf_tokens_empty>>:$:<<", grab_bag.is_leaf_tokens_empty())
        POGGER.debug(
            "do_skip_containers_before_leaf_blocks>>:$:<<",
            grab_bag.do_skip_containers_before_leaf_blocks,
        )
        POGGER.debug("removed_leading_space>>:$:<<", removed_leading_space)
        if (
            grab_bag.is_leaf_tokens_empty()
            and not grab_bag.do_skip_containers_before_leaf_blocks
            and not removed_leading_space
        ):
            position_marker = (
                ContainerBlockLeafProcessor.__adjust_containers_before_leaf_blocks(
                    parser_state,
                    position_marker,
                    last_block_index,
                    total_ws,
                    actual_removed_leading_space,
                    grab_bag,
                    new_ex,
                )
            )
            # POGGER.debug("position_marker.text>>:$:<<", position_marker.text_to_parse)
            # POGGER.debug("position_marker.index>>:$:<<", position_marker.index_number)

        POGGER.debug("position_marker.text>>:$:<<", position_marker.text_to_parse)
        POGGER.debug("position_marker.index>>:$:<<", position_marker.index_number)
        POGGER.debug("position_marker.indent>>:$:<<", position_marker.index_indent)
        ContainerBlockLeafProcessor.__parse_line_for_leaf_blocks(
            parser_state,
            position_marker,
            grab_bag,
        )

        ContainerBlockLeafProcessor.__process_leaf_tokens_adjust(adjust_token, grab_bag)

        ContainerBlockLeafProcessor.__post_leaf_block_adjustment(
            parser_state,
            orig_text_removed_by_container,
            position_marker.line_number,
        )

    @staticmethod
    def __process_leaf_tokens_adjust(
        adjust_token: Optional[ListStartMarkdownToken], grab_bag: ContainerGrabBag
    ) -> None:
        if (
            adjust_token is not None
            and grab_bag.leaf_tokens
            and grab_bag.leaf_tokens[0].is_end_token
        ) and grab_bag.leaf_tokens[0].is_block_quote_end:
            POGGER.debug(
                "__process_leaf_tokens>>adjust_token>>$",
                adjust_token,
            )
            adjust_token.remove_last_leading_space()
            POGGER.debug(
                "__process_leaf_tokens>>adjust_token>>$",
                adjust_token,
            )

            token_index = 1
            end_container_count = 0
            end_list_count = 0
            while token_index < len(grab_bag.leaf_tokens):
                if (
                    grab_bag.leaf_tokens[token_index].is_block_quote_end
                    or grab_bag.leaf_tokens[token_index].is_list_end
                ):
                    end_container_count += 1
                if grab_bag.leaf_tokens[token_index].is_list_end:
                    end_list_count += 1
                token_index += 1
            if end_container_count != 0 and token_index != 0 and grab_bag.bogus:
                POGGER.debug(
                    "__process_leaf_tokens>>adjust_token>>$",
                    adjust_token,
                )
                adjust_token.remove_last_leading_space()
                POGGER.debug(
                    "__process_leaf_tokens>>adjust_token>>$",
                    adjust_token,
                )

                POGGER.debug(
                    "__process_leaf_tokens>>adjust_token>>$",
                    adjust_token,
                )
                adjust_token.add_leading_spaces(grab_bag.bogus)
                POGGER.debug(
                    "__process_leaf_tokens>>adjust_token>>$",
                    adjust_token,
                )

    @staticmethod
    def __parse_line_for_leaf_blocks(
        parser_state: ParserState,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> None:
        """
        Parse the contents of a line for a leaf block.

        Note: This is one of the more heavily traffic functions in the
        parser.  Debugging should be uncommented only if needed.
        """
        POGGER.debug("parsing leaf tokens")
        POGGER.debug("Leaf Line:$:", position_marker.text_to_parse)
        POGGER.debug(
            "Indent:$:, Index:$:",
            position_marker.index_indent,
            position_marker.index_number,
        )
        POGGER.debug("original_line:$:", grab_bag.original_line)
        detabified_original_line = TabHelper.detabify_string(grab_bag.original_line)
        detabified_original_start_index = detabified_original_line.find(
            position_marker.text_to_parse
        )
        assert (
            detabified_original_start_index != -1
        ), "Text must also be found in the original line."
        POGGER.debug(
            "detabified_original_start_index:$:", detabified_original_start_index
        )

        (
            outer_processed,
            leaf_block_position_marker,
            leaf_token_whitespace,
        ) = ContainerBlockLeafProcessor.__handle_block_leaf_tokens(
            parser_state, position_marker, detabified_original_start_index, grab_bag
        )
        if not outer_processed:
            assert (
                grab_bag.removed_chars_at_start_of_line is not None
            ), "When processing these leaf elements, removed_chars_at_start_of_line must be defined by now."
            new_tokens = (
                AtxLeafBlockProcessor.parse_atx_headings(
                    parser_state,
                    leaf_block_position_marker,
                    leaf_token_whitespace,
                    grab_bag.block_quote_data,
                    grab_bag.original_line,
                    grab_bag,
                )
                or IndentedLeafBlockProcessor.parse_indented_code_block(
                    parser_state,
                    leaf_block_position_marker,
                    leaf_token_whitespace,
                    grab_bag.removed_chars_at_start_of_line,
                    grab_bag.last_block_quote_index,
                    grab_bag.original_line,
                )
                or SetextLeafBlockProcessor.parse_setext_headings(
                    parser_state,
                    leaf_block_position_marker,
                    leaf_token_whitespace,
                    grab_bag.block_quote_data,
                    grab_bag.original_line,
                )
                or ThematicLeafBlockProcessor.parse_thematic_break(
                    parser_state,
                    leaf_block_position_marker,
                    leaf_token_whitespace,
                    grab_bag.block_quote_data,
                    grab_bag.original_line,
                    grab_bag,
                )
                or LeafBlockProcessorParagraph.parse_paragraph(
                    parser_state,
                    leaf_block_position_marker,
                    leaf_token_whitespace,
                    grab_bag.block_quote_data,
                    grab_bag.text_removed_by_container,
                    grab_bag.original_line,
                )
            )
            # POGGER.debug(">>leaf--adding>>$", new_tokens)
            grab_bag.extend_leaf_tokens(new_tokens)

    @staticmethod
    def __handle_block_leaf_tokens(
        parser_state: ParserState,
        incoming_position_marker: PositionMarker,
        detabified_original_start_index: int,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[bool, PositionMarker, str]:
        POGGER.debug(
            "line>>$>>index>>$>>",
            incoming_position_marker.text_to_parse,
            incoming_position_marker.index_number,
        )
        remaining_line_to_parse = incoming_position_marker.text_to_parse[
            incoming_position_marker.index_number :
        ]
        (new_index_number, leaf_token_whitespace) = (
            ParserHelper.extract_spaces_verified(
                incoming_position_marker.text_to_parse,
                incoming_position_marker.index_number,
            )
        )
        POGGER.debug(">>leaf_token_whitespace>>:$:<<", leaf_token_whitespace)

        position_marker = PositionMarker(
            incoming_position_marker.line_number,
            new_index_number,
            incoming_position_marker.text_to_parse,
            index_indent=incoming_position_marker.index_indent,
        )

        pre_tokens = LeafBlockProcessor.close_indented_block_if_indent_not_there(
            parser_state, leaf_token_whitespace
        )

        new_tokens: List[MarkdownToken] = []
        outer_processed = FencedLeafBlockProcessor.handle_fenced_code_block(
            parser_state,
            position_marker,
            leaf_token_whitespace,
            new_tokens,
            grab_bag.original_line,
            detabified_original_start_index,
            grab_bag.block_quote_data,
            grab_bag,
        )

        ignore_lrd_start = (
            grab_bag.do_ignore_link_definition_start
            or parser_state.token_stack[-1].is_html_block
        )
        ignore_table_start = grab_bag.do_ignore_table_start

        (
            outer_processed,
            grab_bag.requeue_line_info,
        ) = LinkReferenceDefinitionHelper.handle_link_reference_definition_leaf_block(
            parser_state,
            outer_processed,
            position_marker,
            leaf_token_whitespace,
            remaining_line_to_parse,
            ignore_lrd_start,
            pre_tokens,
            grab_bag.original_line,
        )

        (
            outer_processed,
            grab_bag.requeue_line_info,
        ) = TableBlockHelper.handle_table_leaf_block(
            parser_state,
            outer_processed,
            position_marker,
            leaf_token_whitespace,
            remaining_line_to_parse,
            ignore_table_start,
            pre_tokens,
            grab_bag.original_line,
            grab_bag.requeue_line_info,
        )

        outer_processed = LeafBlockProcessor.handle_html_block(
            parser_state,
            position_marker,
            outer_processed,
            leaf_token_whitespace,
            new_tokens,
            grab_bag,
        )
        grab_bag.extend_leaf_tokens(pre_tokens)
        grab_bag.extend_leaf_tokens(new_tokens)
        return (
            outer_processed,
            position_marker,
            leaf_token_whitespace,
        )

    @staticmethod
    def __handle_special_block_quote_reduction(
        parser_state: ParserState,
        last_block_index: int,
        last_list_index: int,
        grab_bag: ContainerGrabBag,
    ) -> None:
        assert (
            grab_bag.is_leaf_tokens_empty()
        ), "No leaf tokens should be present at this point."
        real_stack_count = parser_state.count_of_block_quotes_on_stack()
        POGGER.debug(
            "stack_count>>:$:($)<",
            grab_bag.block_quote_data.stack_count,
            real_stack_count,
        )
        POGGER.debug("??? special_block_quote_reduction")
        if (
            grab_bag.block_quote_data.current_count < real_stack_count
            and not grab_bag.was_paragraph_continuation
            and last_block_index > last_list_index
            and not last_list_index
        ):
            POGGER.debug("yes special_block_quote_reduction")
            stack_delta = (
                grab_bag.block_quote_data.stack_count
                - grab_bag.block_quote_data.current_count
            )
            if parser_state.token_stack[-1].was_link_definition_started:
                stack_delta += 1
            (
                close_tokens,
                grab_bag.requeue_line_info,
            ) = parser_state.close_open_blocks_fn(
                parser_state,
                include_block_quotes=True,
                was_forced=True,
                requeue_reset=True,
                caller_can_handle_requeue=True,
                until_this_index=len(parser_state.token_stack) - stack_delta,
            )
            grab_bag.extend_leaf_tokens(close_tokens)
            if not grab_bag.requeue_line_info:
                POGGER.debug("parser_state.token_stack>>$", parser_state.token_stack)
                POGGER.debug(
                    "parser_state.token_document>>$", parser_state.token_document
                )
                grab_bag.block_quote_data = BlockQuoteData(
                    grab_bag.block_quote_data.current_count,
                    grab_bag.block_quote_data.stack_count - stack_delta,
                )

    @staticmethod
    def __xx1(
        parser_state: ParserState,
        position_marker: PositionMarker,
        text_removed_by_container: str,
        extracted_leaf_whitespace: str,
    ) -> Tuple[PositionMarker, str, str, str]:
        stack_index = 1
        removed_text_copy = text_removed_by_container[:]
        removed_text_copy_bq_count = removed_text_copy.count(">")
        bq_count = 0
        while bq_count < removed_text_copy_bq_count:
            if parser_state.token_stack[stack_index].is_block_quote:
                bq_count += 1
            stack_index += 1
        last_bq_char_index = removed_text_copy.rindex(">")
        last_bq_char_index += 1
        assert removed_text_copy[last_bq_char_index] == " "
        last_bq_char_index += 1
        assert last_bq_char_index == len(removed_text_copy)

        ws_to_use = 0
        dd = parser_state.token_stack[stack_index].matching_markdown_token
        assert dd is not None
        assert dd.is_list_start
        dd_list = cast(ListStartMarkdownToken, dd)
        indent_delta = dd_list.indent_level - len(removed_text_copy)
        if len(extracted_leaf_whitespace) >= indent_delta:
            ws_to_use += indent_delta

        if ws_to_use:
            ex_space = (
                extracted_leaf_whitespace[:ws_to_use] + ParserLogger.blah_sequence
            )
            extracted_leaf_whitespace = extracted_leaf_whitespace[ws_to_use:]
            new_position_marker = PositionMarker(
                line_number=position_marker.line_number,
                index_number=position_marker.index_number,
                text_to_parse=position_marker.text_to_parse[ws_to_use:],
                index_indent=position_marker.index_indent + ws_to_use,
            )
            position_marker = new_position_marker
            text_removed_by_container += ex_space
        else:
            ex_space = ""
        return (
            position_marker,
            extracted_leaf_whitespace,
            text_removed_by_container,
            ex_space,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_inner_list_container(
        parser_state: ParserState,
        last_block_index: int,
        last_list_index: int,
        position_marker: PositionMarker,
        text_removed_by_container: Optional[str],
        extracted_leaf_whitespace: str,
    ) -> Tuple[Optional[ListStartMarkdownToken], PositionMarker, str, Optional[str]]:
        POGGER.debug("??? adjust_for_inner_list_container")
        if last_block_index > 0 and 0 < last_list_index < last_block_index:
            POGGER.debug("yes adjust_for_inner_list_container")
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[last_list_index].matching_markdown_token,
            )
            if list_token.line_number != position_marker.line_number:
                POGGER.debug("plt-a>>last_block_token>>$", list_token)

                ex_space = ""
                if text_removed_by_container is not None and text_removed_by_container:
                    lt_indent = list_token.indent_level
                    orig_ws_len = len(text_removed_by_container)
                    if orig_ws_len < lt_indent and extracted_leaf_whitespace:

                        (
                            position_marker,
                            extracted_leaf_whitespace,
                            text_removed_by_container,
                            ex_space,
                        ) = ContainerBlockLeafProcessor.__xx1(
                            parser_state,
                            position_marker,
                            text_removed_by_container,
                            extracted_leaf_whitespace,
                        )

                POGGER.debug(
                    "__adjust_for_inner_list_container>>list_token>>$", list_token
                )
                list_token.add_leading_spaces(ex_space)
                POGGER.debug(
                    "__adjust_for_inner_list_container>>list_token>>$", list_token
                )
                return (
                    list_token,
                    position_marker,
                    extracted_leaf_whitespace,
                    text_removed_by_container,
                )
        else:
            POGGER.debug("not adjust_for_inner_list_container")
        return (
            None,
            position_marker,
            extracted_leaf_whitespace,
            text_removed_by_container,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_for_list_container_after_block_quote_special_special(
        parser_state: ParserState,
        adj_original: str,
        bq_index: int,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[str, str]:
        assert (
            grab_bag.text_removed_by_container is not None
        ), "Block quote processing means we removed at least some text."
        removed_text_length = len(grab_bag.text_removed_by_container)
        if (
            adj_original[removed_text_length - 1] == "\t"
            and adj_original[removed_text_length - 2] == ">"
        ):
            orig_prefix = adj_original[removed_text_length - 1 :]
            orig_suffix = adj_original[: removed_text_length - 1]
            xx_block_quote_token = cast(
                BlockQuoteMarkdownToken,
                parser_state.token_stack[bq_index].matching_markdown_token,
            )
            _ = xx_block_quote_token.remove_last_bleading_space()
            # assert (
            #     last_leading_space[0] == "\n"
            # ), "Removed leading space must start with \\n."
            # last_leading_space = last_leading_space[1:]

            POGGER.debug(
                "__adjust_for_list_container_after_block_quote_special_special>>block_token>>$",
                xx_block_quote_token,
            )
            xx_block_quote_token.add_bleading_spaces(">")
            POGGER.debug(
                "__adjust_for_list_container_after_block_quote_special_special>>block_token>>$",
                xx_block_quote_token,
            )
        else:
            orig_prefix = adj_original[removed_text_length:]
            orig_suffix = adj_original[:removed_text_length]
        (
            non_space_index,
            ex_ws,
        ) = ParserHelper.extract_spaces_verified(orig_prefix, 0)
        original_up_to_non_space = orig_prefix[:non_space_index]
        redone_original = orig_suffix + original_up_to_non_space
        detabified_redone_original = TabHelper.detabify_string(redone_original)

        return detabified_redone_original, ex_ws

    @staticmethod
    def __adjust_for_list_container_after_block_quote_special(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        extracted_leaf_whitespace: str,
        grab_bag: ContainerGrabBag,
    ) -> str:
        bq_index = parser_state.find_last_block_quote_on_stack()
        list_index = parser_state.find_last_list_block_on_stack()

        current_list_indent = -1
        assert (
            list_index > bq_index
        ), "If here, the list is embedded within a block quotes, and the indices must support that."
        xx_list_token = cast(
            ListStartMarkdownToken,
            parser_state.token_stack[list_index].matching_markdown_token,
        )
        current_list_indent = xx_list_token.indent_level

        assert (
            grab_bag.text_removed_by_container is not None
        ), "If here, some text must have been removed."
        reconstructed_line = (
            grab_bag.text_removed_by_container + xposition_marker.text_to_parse
        )
        (
            adj_original,
            _,
            _,
        ) = TabHelper.find_tabified_string(
            grab_bag.original_line,
            reconstructed_line,
            abc=False,
            was_indented=True,
            reconstruct_prefix=None,
        )
        (
            detabified_redone_original,
            ex_ws,
        ) = ContainerBlockLeafProcessor.__adjust_for_list_container_after_block_quote_special_special(
            parser_state, adj_original, bq_index, grab_bag
        )
        if (
            current_list_indent != -1
            and len(detabified_redone_original) >= current_list_indent
        ):
            return ex_ws
        return extracted_leaf_whitespace

    @staticmethod
    def __adjust_for_list_container_after_block_quote_kludge(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        calc_indent_level: int,
        extracted_leaf_whitespace: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[str, str, Optional[str]]:
        removed_leading_space = None
        if not (
            "\t" not in grab_bag.original_line
            or grab_bag.text_removed_by_container != "> "
        ):
            POGGER.debug("__adjust_for_list_container_after_block_quote_kludge-->1")
            new_ex = ContainerBlockLeafProcessor.__adjust_for_list_container_after_block_quote_special(
                parser_state, xposition_marker, extracted_leaf_whitespace, grab_bag
            )
        else:
            POGGER.debug("__adjust_for_list_container_after_block_quote_kludge-->2")
            new_ex = extracted_leaf_whitespace
            POGGER.debug(
                "text_removed_by_container-->:$:<", grab_bag.text_removed_by_container
            )
            POGGER.debug("adj_line_to_parse-->:$:<", grab_bag.adj_line_to_parse)
            POGGER.debug("original_line-->:$:<", grab_bag.original_line)
            POGGER.debug(
                "text_removed_by_container-->:$:<", grab_bag.text_removed_by_container
            )
            if (
                grab_bag.text_removed_by_container
                and grab_bag.adj_line_to_parse
                and grab_bag.original_line
                and grab_bag.text_removed_by_container == "> "
            ):
                recon_line = (
                    grab_bag.text_removed_by_container + grab_bag.adj_line_to_parse
                )
                if (
                    recon_line == grab_bag.original_line
                    and extracted_leaf_whitespace
                    and len(extracted_leaf_whitespace) < calc_indent_level
                ):
                    extracted_leaf_whitespace = extracted_leaf_whitespace[
                        len(grab_bag.text_removed_by_container) :
                    ]
                    removed_leading_space = grab_bag.text_removed_by_container
        return new_ex, extracted_leaf_whitespace, removed_leading_space

    @staticmethod
    def __adjust_for_list_container_after_block_quote(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        last_list_index: int,
        extracted_leaf_whitespace: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[
        Optional[ListStartMarkdownToken],
        Optional[str],
        Optional[str],
        Optional[ListStackToken],
        Optional[str],
    ]:
        list_token: Optional[ListStartMarkdownToken] = None
        POGGER.debug("yes adjust_for_list_container")
        removed_leading_space = None
        actual_removed_leading_space = None
        list_stack_token = None
        new_ex = None

        found_list_token = ContainerBlockLeafProcessor.__adjust_for_list_container_find(
            parser_state, xposition_marker
        )
        if not found_list_token:
            POGGER.debug(
                "__adjust_for_list_container_after_block_quote>>removed_leading_space>>$<<",
                removed_leading_space,
            )
            POGGER.debug(
                "__adjust_for_list_container_after_block_quote>>actual_removed_leading_space>>$<<",
                actual_removed_leading_space,
            )
            list_stack_token = cast(
                ListStackToken, parser_state.token_stack[last_list_index]
            )
            list_token = cast(
                ListStartMarkdownToken, list_stack_token.matching_markdown_token
            )
            calc_indent_level = (
                list_token.indent_level - len(grab_bag.text_removed_by_container)
                if grab_bag.text_removed_by_container
                else list_token.indent_level
            )
            if len(extracted_leaf_whitespace) > calc_indent_level:
                extracted_leaf_whitespace = extracted_leaf_whitespace[
                    :calc_indent_level
                ]

            (
                new_ex,
                extracted_leaf_whitespace,
                removed_leading_space,
            ) = ContainerBlockLeafProcessor.__adjust_for_list_container_after_block_quote_kludge(
                parser_state,
                xposition_marker,
                calc_indent_level,
                extracted_leaf_whitespace,
                grab_bag,
            )

            POGGER.debug(
                "__adjust_for_list_container_after_block_quote>>list_token>>$",
                list_token,
            )
            list_token.add_leading_spaces(new_ex)
            POGGER.debug(
                "__adjust_for_list_container_after_block_quote>>list_token>>$",
                list_token,
            )
            actual_removed_leading_space = extracted_leaf_whitespace

            if not grab_bag.container_depth and not xposition_marker.index_indent:
                removed_leading_space = extracted_leaf_whitespace
            POGGER.debug(
                "__adjust_for_list_container_after_block_quote>>removed_leading_space>>:$:<<",
                removed_leading_space,
            )
            POGGER.debug(
                "__adjust_for_list_container_after_block_quote>>actual_removed_leading_space>>:$:<<",
                actual_removed_leading_space,
            )
            POGGER.debug(
                "__adjust_for_list_container_after_block_quote>>new_ex>>:$:<<", new_ex
            )
        return (
            list_token,
            removed_leading_space,
            actual_removed_leading_space,
            list_stack_token,
            new_ex,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_list_container(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        last_block_index: int,
        last_list_index: int,
        extracted_leaf_whitespace: str,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[Optional[str], Optional[str], PositionMarker, Optional[str]]:
        POGGER.debug("??? adjust_for_list_container")
        removed_leading_space = None
        actual_removed_leading_space = None
        list_token: Optional[ListStartMarkdownToken] = None
        new_ex = None
        list_stack_token = None
        # pylint: disable=chained-comparison
        if (
            not grab_bag.was_indent_already_processed
            and last_block_index > 0
            and last_list_index > 0
            and last_list_index > last_block_index
        ):
            (
                list_token,
                removed_leading_space,
                actual_removed_leading_space,
                list_stack_token,
                new_ex,
            ) = ContainerBlockLeafProcessor.__adjust_for_list_container_after_block_quote(
                parser_state,
                xposition_marker,
                last_list_index,
                extracted_leaf_whitespace,
                grab_bag,
            )
            if new_ex:
                POGGER.debug("new_ex>>:$:<<", new_ex)
                xposition_marker = PositionMarker(
                    xposition_marker.line_number,
                    len(new_ex),
                    xposition_marker.text_to_parse,
                    index_indent=xposition_marker.index_indent,
                )
                # POGGER.debug(
                #     "position_marker.text>>:$:<<", xposition_marker.text_to_parse
                # )
                # POGGER.debug(
                #     "position_marker.index>>:$:<<", xposition_marker.index_number
                # )
                # POGGER.debug(
                #     "position_marker.indent>>:$:<<", xposition_marker.index_indent
                # )
        else:
            POGGER.debug("not adjust_for_list_container")
        # pylint: enable=chained-comparison

        if ContainerBlockLeafProcessor.__adjust_for_list_container_kludge(
            parser_state,
            xposition_marker,
            removed_leading_space,
            actual_removed_leading_space,
            list_token,
            grab_bag,
            last_list_index,
            last_block_index,
        ):
            assert actual_removed_leading_space is not None
            assert (
                grab_bag.text_removed_by_container is not None
            ), "If here, some text must have been removed."
            total_removed = len(grab_bag.text_removed_by_container) + len(
                actual_removed_leading_space
            )
            assert list_stack_token is not None
            if total_removed < list_stack_token.start_index:
                delta = len(actual_removed_leading_space)
            else:
                assert list_token is not None
                delta = list_token.indent_level - total_removed
            xposition_marker = PositionMarker(
                xposition_marker.line_number,
                xposition_marker.index_number,
                xposition_marker.text_to_parse[delta:],
                xposition_marker.index_indent,
            )
            # POGGER.debug("position_marker.text>>:$:<<", xposition_marker.text_to_parse)
            # POGGER.debug("position_marker.index>>:$:<<", xposition_marker.index_number)
            # POGGER.debug("position_marker.indent>>:$:<<", xposition_marker.index_indent)
        return (
            removed_leading_space,
            actual_removed_leading_space,
            xposition_marker,
            new_ex,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-boolean-expressions,too-many-arguments
    @staticmethod
    def __adjust_for_list_container_kludge(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        removed_leading_space: Optional[str],
        actual_removed_leading_space: Optional[str],
        list_token: Optional[ListStartMarkdownToken],
        grab_bag: ContainerGrabBag,
        last_list_index: int,
        last_block_index: int,
    ) -> bool:
        apply_fix = False
        if (
            removed_leading_space is None
            and actual_removed_leading_space
            and list_token
            and grab_bag.block_quote_data.current_count
            == grab_bag.block_quote_data.stack_count
            and grab_bag.block_quote_data.stack_count > 1
            and grab_bag.is_para_continue
        ):
            keep_searching = True
            while keep_searching and last_list_index > last_block_index:
                inner_token = cast(
                    ListStackToken, parser_state.token_stack[last_list_index]
                )
                indent_delta = inner_token.indent_level - xposition_marker.index_indent
                line_to_parse = xposition_marker.text_to_parse
                if line_to_parse[:indent_delta].strip():
                    last_list_index -= 1
                else:
                    keep_searching = False

            if last_list_index == last_block_index:
                indent_delta = 0

            after_ws_index, extracted_whitespace = ParserHelper.extract_spaces_verified(
                line_to_parse, indent_delta
            )

            apply_fix = not LeafBlockProcessor.is_paragraph_ending_leaf_block_start(
                parser_state,
                line_to_parse,
                after_ws_index,
                extracted_whitespace,
                grab_bag.original_line,
                xposition_marker.index_indent,
            )
        return apply_fix

    # pylint: enable=too-many-boolean-expressions, too-many-arguments

    @staticmethod
    def __adjust_for_list_container_find(
        parser_state: ParserState, xposition_marker: PositionMarker
    ) -> Optional[MarkdownToken]:
        found_list_token, document_index = (
            None,
            len(parser_state.token_document) - 1,
        )
        if (
            document_index >= 0
            and parser_state.token_document[document_index].line_number
            == xposition_marker.line_number
        ):
            assert (
                parser_state.token_document[document_index].is_list_start
                or parser_state.token_document[document_index].is_new_list_item
            ), "Specified token is a list token."
            found_list_token = parser_state.token_document[document_index]
        return found_list_token

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_containers_before_leaf_blocks_adjust(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        last_block_index: int,
        total_ws: int,
        actual_removed_leading_space: Optional[str],
        grab_bag: ContainerGrabBag,
        new_ex: Optional[str],
    ) -> Tuple[str, int, Optional[PositionMarker]]:
        if grab_bag.do_force_list_continuation:
            POGGER.debug(
                "actual_removed_leading_space=$=", actual_removed_leading_space
            )
            if not actual_removed_leading_space:
                actual_removed_leading_space = ""
            assert xposition_marker.text_to_parse.startswith(
                actual_removed_leading_space
            ), "Text to parse must begin with the reported leading whitespace."
            position_marker = PositionMarker(
                xposition_marker.line_number,
                0,
                xposition_marker.text_to_parse[len(actual_removed_leading_space) :],
                xposition_marker.index_indent,
            )
            return "", -1, position_marker

        POGGER.debug("yes adjust_containers_before_leaf_blocks")
        (
            current_indent_level,
            close_tokens,
        ) = ContainerBlockLeafProcessor.__calculate_current_indent_level(
            parser_state,
            last_block_index,
            total_ws,
            xposition_marker,
            grab_bag,
        )
        POGGER.debug("close_tokens>:$:<", close_tokens)
        POGGER.debug("current_indent_level>:$:<", current_indent_level)
        POGGER.debug("xposition_marker.line_number>:$:<", xposition_marker.line_number)
        POGGER.debug(
            "xposition_marker.index_number>:$:<", xposition_marker.index_number
        )
        POGGER.debug(
            "xposition_marker.text_to_parse>:$:<", xposition_marker.text_to_parse
        )
        POGGER.debug(
            "xposition_marker.index_indent>:$:<", xposition_marker.index_indent
        )
        if close_tokens:
            grab_bag.extend_container_tokens(close_tokens)

        assert (
            parser_state.original_line_to_parse is not None
        ), "Original line must have been set by this point."
        (
            new_index_indent,
            new_text_to_parse,
        ) = ContainerBlockLeafProcessor.__make_adjustments(
            parser_state, xposition_marker, current_indent_level, grab_bag, new_ex
        )
        ContainerBlockLeafProcessor.__val(parser_state, new_text_to_parse)
        return new_text_to_parse, new_index_indent, None

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_containers_before_leaf_blocks(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        last_block_index: int,
        total_ws: int,
        actual_removed_leading_space: Optional[str],
        grab_bag: ContainerGrabBag,
        new_ex: Optional[str],
    ) -> PositionMarker:
        POGGER.debug("??? adjust_containers_before_leaf_blocks")
        POGGER.debug("xposition_marker.line_number>:$:<", xposition_marker.line_number)
        POGGER.debug(
            "xposition_marker.index_number>:$:<", xposition_marker.index_number
        )
        POGGER.debug(
            "xposition_marker.text_to_parse>:$:<", xposition_marker.text_to_parse
        )
        POGGER.debug(
            "xposition_marker.index_indent>:$:<", xposition_marker.index_indent
        )
        if (
            xposition_marker.text_to_parse
            and not grab_bag.was_paragraph_continuation
            and not grab_bag.was_indent_already_processed
        ):
            (
                new_text_to_parse,
                new_index_indent,
                new_position_marker,
            ) = ContainerBlockLeafProcessor.__adjust_containers_before_leaf_blocks_adjust(
                parser_state,
                xposition_marker,
                last_block_index,
                total_ws,
                actual_removed_leading_space,
                grab_bag,
                new_ex,
            )
            if new_position_marker:
                return new_position_marker
        else:
            POGGER.debug("not adjust_containers_before_leaf_blocks")
            new_text_to_parse = xposition_marker.text_to_parse
            new_index_indent = xposition_marker.index_indent

        indent_adjust = 0
        # if actual_removed_leading_space and new_index_indent == len(
        #     actual_removed_leading_space
        # ):
        #     # indent_adjust += new_index_indent
        #     # new_index_indent = 0
        #     pass

        POGGER.debug("xposition_marker.line_number>:$:<", xposition_marker.line_number)
        POGGER.debug("xposition_marker.index_number>:$:<", indent_adjust)
        POGGER.debug("xposition_marker.text_to_parse>:$:<", new_text_to_parse)
        POGGER.debug("xposition_marker.index_indent>:$:<", new_index_indent)
        return PositionMarker(
            xposition_marker.line_number,
            indent_adjust,
            new_text_to_parse,
            new_index_indent,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __calculate_current_indent_level_list(
        parser_state: ParserState, current_stack_index: int
    ) -> int:
        stack_token = cast(
            ListStackToken, parser_state.token_stack[current_stack_index]
        )
        if stack_token.last_new_list_token:
            return stack_token.last_new_list_token.indent_level
        list_token = cast(ListStartMarkdownToken, stack_token.matching_markdown_token)
        return list_token.indent_level

    @staticmethod
    def __post_leaf_block_adjustment(
        parser_state: ParserState,
        orig_text_removed_by_container: Optional[str],
        line_number: int,
    ) -> None:
        last_block_index = parser_state.find_last_block_quote_on_stack()
        POGGER.debug("last_block_index>>:$:", last_block_index)
        if not last_block_index:
            return

        last_block_token = cast(
            BlockQuoteMarkdownToken,
            parser_state.token_stack[last_block_index].matching_markdown_token,
        )

        if (
            not orig_text_removed_by_container
        ) and last_block_token.line_number != line_number:
            POGGER.debug(
                "plt-c>>last_block_token>>$",
                last_block_token,
            )
            POGGER.debug(
                "plt-c>>leading_text_index>>$", last_block_token.leading_text_index
            )
            POGGER.debug(
                "__post_leaf_block_adjustment>>block_token>>$", last_block_token
            )
            last_block_token.add_bleading_spaces("")
            POGGER.debug(
                "__post_leaf_block_adjustment>>block_token>>$", last_block_token
            )
            last_block_token.leading_text_index += 1
            POGGER.debug("plt-c>>last_block_token>>$", last_block_token)
            POGGER.debug(
                "plt-c>>leading_text_index>>$", last_block_token.leading_text_index
            )

    @staticmethod
    def __val(parser_state: ParserState, new_text_to_parse: str) -> None:
        assert (
            parser_state.original_line_to_parse is not None
        ), "Original line must have been set by this point."
        if len(parser_state.original_line_to_parse) == len(new_text_to_parse):
            assert parser_state.original_line_to_parse.replace(
                ">", ParserHelper.space_character
            ) == new_text_to_parse.replace(">", ParserHelper.space_character), (
                "cheat=:"
                + ParserHelper.make_value_visible(parser_state.original_line_to_parse)
                + ":,new_text_to_parse=:"
                + ParserHelper.make_value_visible(new_text_to_parse)
                + ":"
            )
        else:
            is_valid = parser_state.original_line_to_parse.endswith(new_text_to_parse)
            assert is_valid, (
                "cheat=:"
                + ParserHelper.make_value_visible(parser_state.original_line_to_parse)
                + ":,new_text_to_parse=:"
                + ParserHelper.make_value_visible(new_text_to_parse)
                + ":"
            )

    @staticmethod
    def __make_adjustments(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        current_indent_level: int,
        grab_bag: ContainerGrabBag,
        new_ex: Optional[str],
    ) -> Tuple[int, str]:
        assert (
            parser_state.original_line_to_parse is not None
        ), "Original line must have been set by this point."
        POGGER.debug(
            "parser_state.original_line_to_parse>>:$:($)",
            parser_state.original_line_to_parse,
            len(parser_state.original_line_to_parse),
        )
        POGGER.debug(
            "xposition_marker.text_to_parse>>:$:($)",
            xposition_marker.text_to_parse,
            len(xposition_marker.text_to_parse),
        )
        if grab_bag.weird_adjusted_text:
            new_index_indent = len(grab_bag.weird_adjusted_text)
            grab_bag.text_removed_by_container = grab_bag.weird_adjusted_text
            new_text_to_parse = parser_state.original_line_to_parse[new_index_indent:]
        else:
            POGGER.debug("current_indent_level>>:$:<", current_indent_level)
            current_indent_level -= xposition_marker.index_indent
            POGGER.debug("current_indent_level>>:$:<", current_indent_level)
            current_indent_level = max(current_indent_level, 0)
            assert current_indent_level >= 0, "Current indent must not go below 0."

            prefix_text = xposition_marker.text_to_parse[:current_indent_level]
            new_text_to_parse = xposition_marker.text_to_parse[current_indent_level:]
            new_index_indent = len(parser_state.original_line_to_parse) - len(
                new_text_to_parse
            )
            # if False and grab_bag.text_removed_by_container and ">" in grab_bag.text_removed_by_container:
            #     new_index_indent -= xposition_marker.index_indent

            POGGER.debug("new_ex>>:$:<", new_ex)
            POGGER.debug("new_text_to_parse>>:$:<", new_text_to_parse)
            POGGER.debug("new_index_indent>>:$:<", new_index_indent)
            POGGER.debug(
                "grab_bag.text_removed_by_container>>:$:<",
                grab_bag.text_removed_by_container,
            )
            POGGER.debug("prefix_text>>:$:<", prefix_text)
            grab_bag.text_removed_by_container = (
                grab_bag.text_removed_by_container + prefix_text
                if grab_bag.text_removed_by_container
                else prefix_text
            )
            new_index_indent, new_text_to_parse = (
                ContainerBlockLeafProcessor.__make_adjustments_inner(
                    parser_state, new_index_indent, new_text_to_parse, new_ex, grab_bag
                )
            )
            POGGER.debug(
                "grab_bag.text_removed_by_container>>:$:<",
                grab_bag.text_removed_by_container,
            )
        return new_index_indent, new_text_to_parse

    @staticmethod
    def __make_adjustments_inner(
        parser_state: ParserState,
        new_index_indent: int,
        new_text_to_parse: str,
        new_ex: Optional[str],
        grab_bag: ContainerGrabBag,
    ) -> Tuple[int, str]:
        adj_text_removed = grab_bag.text_removed_by_container
        assert adj_text_removed is not None
        if (
            len(adj_text_removed) > 1
            and adj_text_removed[-1] == " "
            and adj_text_removed[-2] == ">"
        ):
            adj_text_removed = adj_text_removed[2:]
        if (
            new_ex
            and not adj_text_removed.endswith(new_ex)
            and new_text_to_parse.startswith(new_ex)
        ):
            # assert new_ex is not None
            last_container_index = parser_state.find_last_container_on_stack()
            apply_adjustment = parser_state.token_stack[last_container_index].is_list
            if apply_adjustment and "\t" in grab_bag.original_line:
                apply_adjustment = (
                    ContainerBlockLeafProcessor.__make_adjustments_inner_tab_check(
                        grab_bag, new_ex
                    )
                )
            if apply_adjustment:
                new_index_indent += len(new_ex)
                new_text_to_parse = new_text_to_parse[len(new_ex) :]
        return new_index_indent, new_text_to_parse

    @staticmethod
    def __make_adjustments_inner_tab_check(
        grab_bag: ContainerGrabBag, new_ex: str
    ) -> bool:
        assert grab_bag.text_removed_by_container is not None
        removed_text = grab_bag.text_removed_by_container + new_ex
        index = 1
        line_part = None
        while True:
            assert index < len(grab_bag.original_line)
            line_part = grab_bag.original_line[:index]
            if len(TabHelper.detabify_string(line_part)) >= len(removed_text):
                break
            index += 1
        assert line_part is not None
        return "\t" not in line_part

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_current_indent_level_loop_kludge(
        parser_state: ParserState,
        total_ws: int,
        current_indent_level: int,
        last_list_index: int,
        current_stack_index: int,
        text_removed_by_container: Optional[str],
        non_last_block_index: int,
        last_block_index: int,
        line_number: int,
    ) -> Tuple[bool, int, Optional[int], int]:
        keep_processing = (
            total_ws != current_indent_level
            if (
                last_list_index > 0
                and text_removed_by_container is None
                and len(parser_state.token_stack) - 1 == current_stack_index
            )
            else True
        )
        if keep_processing:
            last_list_index = 0
            (
                new_indent_level,
                non_last_block_index,
            ) = ContainerBlockLeafProcessor.__calculate_current_indent_level_block_quote(
                parser_state,
                current_stack_index,
                non_last_block_index,
                last_block_index,
                line_number,
                current_indent_level,
                text_removed_by_container,
            )
            keep_processing = new_indent_level is not None
        else:
            new_indent_level = None

        return keep_processing, last_list_index, new_indent_level, non_last_block_index

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __xx_part_one(
        parser_state: ParserState,
        position_marker: PositionMarker,
        current_stack_index: int,
        total_ws: int,
        current_indent_level: int,
        last_list_index: int,
        text_removed_by_container: Optional[str],
        non_last_block_index: int,
        last_block_index: int,
    ) -> Tuple[Optional[int], bool, bool, int, int, bool]:
        proposed_indent_level: Optional[int] = 0
        POGGER.debug("token:$:", parser_state.token_stack[current_stack_index])
        continue_in_loop = True
        keep_processing = True
        had_non_block_token = False
        if parser_state.token_stack[current_stack_index].is_block_quote:
            (
                keep_processing,
                last_list_index,
                new_indent_level,
                non_last_block_index,
            ) = ContainerBlockLeafProcessor.__calculate_current_indent_level_loop_kludge(
                parser_state,
                total_ws,
                current_indent_level,
                last_list_index,
                current_stack_index,
                text_removed_by_container,
                non_last_block_index,
                last_block_index,
                position_marker.line_number,
            )
            if keep_processing:
                proposed_indent_level = new_indent_level
        elif parser_state.token_stack[current_stack_index].is_list:
            last_list_index = current_stack_index
            proposed_indent_level = (
                ContainerBlockLeafProcessor.__calculate_current_indent_level_list(
                    parser_state, current_stack_index
                )
            )
        else:
            had_non_block_token = True
            continue_in_loop = False
        return (
            proposed_indent_level,
            continue_in_loop,
            keep_processing,
            last_list_index,
            non_last_block_index,
            had_non_block_token,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=chained-comparison,too-many-arguments,too-many-locals
    @staticmethod
    def __xx_part_two(
        parser_state: ParserState,
        position_marker: PositionMarker,
        proposed_indent_level: Optional[int],
        total_ws: int,
        current_stack_index: int,
        current_indent_level: int,
        adj_ws: Optional[str],
        is_para_continue: bool,
        last_list_index: int,
        last_block_index: int,
        original_line: str,
        did_hit_indent_level_threshold: bool,
        continue_in_loop: bool,
    ) -> Tuple[bool, bool, int]:
        assert (
            proposed_indent_level is not None
        ), "Proposed ident level within lists must be decided."
        if proposed_indent_level > total_ws:
            did_hit_indent_level_threshold = True
            continue_in_loop = False
            if parser_state.token_stack[current_stack_index].is_list:
                is_total_ws_in_range = (
                    total_ws > current_indent_level and total_ws < proposed_indent_level
                )
                if (
                    is_total_ws_in_range
                    and not adj_ws
                    and is_para_continue
                    and last_list_index == last_block_index + 1
                ):
                    after_ws_index, extracted_whitespace = (
                        ParserHelper.extract_spaces_verified(
                            position_marker.text_to_parse,
                            position_marker.index_number,
                        )
                    )
                    keep_going = (
                        not LeafBlockProcessor.is_paragraph_ending_leaf_block_start(
                            parser_state,
                            position_marker.text_to_parse,
                            after_ws_index,
                            extracted_whitespace,
                            original_line,
                            position_marker.index_indent,
                        )
                    )
                    if keep_going:
                        current_indent_level += len(extracted_whitespace)
        else:
            current_indent_level = proposed_indent_level
            # POGGER.debug("current_indent_level:$", current_indent_level)
        return did_hit_indent_level_threshold, continue_in_loop, current_indent_level

    # pylint: enable=chained-comparison,too-many-arguments,too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __calculate_current_indent_level_loop(
        parser_state: ParserState,
        last_block_index: int,
        total_ws: int,
        position_marker: PositionMarker,
        current_stack_index: int,
        text_removed_by_container: Optional[str],
        current_indent_level: int,
        non_last_block_index: int,
        last_list_index: int,
        had_non_block_token: bool,
        did_hit_indent_level_threshold: bool,
        adj_ws: Optional[str],
        is_para_continue: bool,
        original_line: str,
    ) -> Tuple[int, int, int, bool, bool, bool]:
        (
            proposed_indent_level,
            continue_in_loop,
            keep_processing,
            last_list_index,
            non_last_block_index,
            had_non_block_token,
        ) = ContainerBlockLeafProcessor.__xx_part_one(
            parser_state,
            position_marker,
            current_stack_index,
            total_ws,
            current_indent_level,
            last_list_index,
            text_removed_by_container,
            non_last_block_index,
            last_block_index,
        )
        POGGER.debug(
            "proposed_indent_level:$ <= total_ws:$<",
            proposed_indent_level,
            total_ws,
        )
        if continue_in_loop and keep_processing:
            did_hit_indent_level_threshold, continue_in_loop, current_indent_level = (
                ContainerBlockLeafProcessor.__xx_part_two(
                    parser_state,
                    position_marker,
                    proposed_indent_level,
                    total_ws,
                    current_stack_index,
                    current_indent_level,
                    adj_ws,
                    is_para_continue,
                    last_list_index,
                    last_block_index,
                    original_line,
                    did_hit_indent_level_threshold,
                    continue_in_loop,
                )
            )
            POGGER.debug(
                "did_hit_indent_level_threshold>:$:<", did_hit_indent_level_threshold
            )
            POGGER.debug("continue_in_loop>:$:<", continue_in_loop)
            POGGER.debug("current_indent_level>:$:<", current_indent_level)
        return (
            current_indent_level,
            non_last_block_index,
            last_list_index,
            had_non_block_token,
            did_hit_indent_level_threshold,
            continue_in_loop,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __calculate_current_indent_level(
        parser_state: ParserState,
        last_block_index: int,
        total_ws: int,
        position_marker: PositionMarker,
        grab_bag: ContainerGrabBag,
    ) -> Tuple[int, List[MarkdownToken]]:
        text_removed_by_container = grab_bag.text_removed_by_container
        current_indent_level = 0
        non_last_block_index = 0
        last_list_index = 0
        had_non_block_token = False
        did_hit_indent_level_threshold = False
        POGGER.debug("token-stack:$:", parser_state.token_stack)
        for current_stack_index in range(1, len(parser_state.token_stack)):
            POGGER.debug("<<current_indent_level:$", current_indent_level)
            (
                current_indent_level,
                non_last_block_index,
                last_list_index,
                had_non_block_token,
                did_hit_indent_level_threshold,
                continue_in_loop,
            ) = ContainerBlockLeafProcessor.__calculate_current_indent_level_loop(
                parser_state,
                last_block_index,
                total_ws,
                position_marker,
                current_stack_index,
                text_removed_by_container,
                current_indent_level,
                non_last_block_index,
                last_list_index,
                had_non_block_token,
                did_hit_indent_level_threshold,
                grab_bag.adj_ws,
                grab_bag.is_para_continue,
                grab_bag.original_line,
            )
            POGGER.debug("<<current_indent_level:$", current_indent_level)
            if not continue_in_loop:
                break
        POGGER.debug("<<current_indent_level:$", current_indent_level)
        close_tokens: List[MarkdownToken] = []
        if last_list_index:
            POGGER.debug("<<had_non_block_token:$", had_non_block_token)
            POGGER.debug("<<grab_bag.is_para_continue:$", grab_bag.is_para_continue)
            if (
                not had_non_block_token
                and did_hit_indent_level_threshold
                and not grab_bag.is_para_continue
            ):
                POGGER.debug("<<last_list_index:$", last_list_index)
                (
                    close_tokens,
                    grab_bag.requeue_line_info,
                ) = parser_state.close_open_blocks_fn(
                    parser_state,
                    include_lists=True,
                    was_forced=True,
                    until_this_index=last_list_index,
                )
                POGGER.debug("<<close_tokens:$", close_tokens)
        return current_indent_level, close_tokens

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_current_indent_level_block_quote(
        parser_state: ParserState,
        current_stack_index: int,
        non_last_block_index: int,
        last_block_index: int,
        line_number: int,
        current_indent_level: int,
        text_removed_by_container: Optional[str],
    ) -> Tuple[Optional[int], int]:
        if current_stack_index != last_block_index:
            POGGER.debug("not last bq token, skipping")
            non_last_block_index = current_stack_index
            return None, non_last_block_index

        matching_token = parser_state.token_stack[
            current_stack_index
        ].matching_markdown_token
        assert (
            matching_token is not None
        ), "Matching token is always set for containers."
        POGGER.debug("line_number=$", line_number)
        POGGER.debug(
            "matching_markdown_token.line_number=$", matching_token.line_number
        )
        POGGER.debug("non_last_block_index=$", non_last_block_index)

        valid_mark = non_last_block_index and non_last_block_index != (
            last_block_index - 1
        )
        POGGER.debug("current_indent_level=:$:", current_indent_level)
        base_indent_level = (
            current_indent_level
            if valid_mark and line_number == matching_token.line_number
            else 0
        )
        POGGER.debug("text_removed_by_container=:$:", text_removed_by_container)
        POGGER.debug("base_indent_level=:$:", base_indent_level)
        proposed_indent_level = (
            len(text_removed_by_container) if text_removed_by_container else 0
        ) + base_indent_level
        POGGER.debug("last bq token, processing:$", proposed_indent_level)
        return proposed_indent_level, non_last_block_index

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
