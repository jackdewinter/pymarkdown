"""
Module to provide processing for the container blocks.
"""
from __future__ import annotations

import copy
import logging
from typing import TYPE_CHECKING, List, Optional, Tuple, cast

from pymarkdown.block_quote_data import BlockQuoteData
from pymarkdown.block_quote_processor import BlockQuoteProcessor
from pymarkdown.container_indices import ContainerIndices
from pymarkdown.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ListStartMarkdownToken,
)
from pymarkdown.extensions.pragma_token import PragmaExtension
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.link_reference_definition_helper import LinkReferenceDefinitionHelper
from pymarkdown.list_block_processor import ListBlockProcessor
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.requeue_line_info import RequeueLineInfo
from pymarkdown.stack_token import ListStackToken, StackToken

if TYPE_CHECKING:  # pragma: no cover
    from pymarkdown.parse_block_pass_properties import ParseBlockPassProperties

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


class ContainerBlockProcessor:
    """
    Class to provide processing for the container blocks.
    """

    # pylint: disable=too-many-arguments
    @staticmethod
    def __setup(
        parser_state: ParserState,
        position_marker: PositionMarker,
        container_depth: int,
        foobar: Optional[int],
        init_bq: Optional[int],
        parser_properties: ParseBlockPassProperties,
    ) -> Tuple[
        PositionMarker,
        List[StackToken],
        Optional[str],
        Optional[BlockQuoteData],
        int,
        Optional[str],
        bool,
        bool,
    ]:

        POGGER.debug(">>")
        POGGER.debug(">>")
        POGGER.debug(">>container_depth>>:$:", container_depth)
        if ContainerBlockProcessor.__look_for_pragmas(
            position_marker,
            container_depth,
            parser_properties,
        ):
            return position_marker, [], None, None, -1, None, True, False

        position_marker = ContainerBlockProcessor.__prepare_container_start_variables(
            parser_state,
            position_marker,
            container_depth,
        )

        (
            current_container_blocks,
            adj_ws,
            block_quote_data,
            start_index,
            extracted_whitespace,
        ) = ContainerBlockProcessor.__prepare_container_start_variables2(
            parser_state, position_marker, foobar, init_bq, container_depth
        )

        is_not_in_root_list = not (
            parser_state.token_stack
            and len(parser_state.token_stack) >= 2
            and parser_state.token_stack[1].is_list
        )

        return (
            position_marker,
            current_container_blocks,
            adj_ws,
            block_quote_data,
            start_index,
            extracted_whitespace,
            False,
            is_not_in_root_list,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_line_for_container_blocks(
        parser_state: ParserState,
        position_marker: PositionMarker,
        ignore_link_definition_start: bool,
        parser_properties: ParseBlockPassProperties,
        container_start_bq_count: int,
        container_depth: int = 0,
        foobar: Optional[int] = None,
        init_bq: Optional[int] = None,
    ) -> Tuple[
        List[MarkdownToken],
        Optional[str],
        Optional[int],
        Optional[RequeueLineInfo],
        bool,
        bool,
    ]:
        """
        Parse the line, taking care to handle any container blocks before deciding
        whether or not to pass the (remaining parts of the) line to the leaf block
        processor.

        Note: This is one of the more heavily traffic functions in the
        parser.  Debugging should be uncommented only if needed.
        """

        (
            position_marker,
            current_container_blocks,
            adj_ws,
            block_quote_data,
            start_index,
            extracted_whitespace,
            did_find_pragma,
            is_not_in_root_list,
        ) = ContainerBlockProcessor.__setup(
            parser_state,
            position_marker,
            container_depth,
            foobar,
            init_bq,
            parser_properties,
        )
        if did_find_pragma:
            return [], None, None, None, False, False
        # POGGER.debug("start_index>>$", start_index)
        # POGGER.debug("position_marker.index_number>>$", position_marker.index_number)

        # POGGER.debug(">>extracted_whitespace>>:$:", extracted_whitespace)
        # POGGER.debug(">>parser_state.token_stack:$", parser_state.token_stack)
        # POGGER.debug(">>container_depth=$", container_depth)
        # POGGER.debug(">>extracted_whitespace=:$:", extracted_whitespace)
        # POGGER.debug(">>is_not_in_root_list=:$:", is_not_in_root_list)
        assert extracted_whitespace is not None
        assert block_quote_data is not None
        force_list_continuation = False
        removed_chars_at_start: Optional[int] = None
        if (
            not container_depth
            and len(extracted_whitespace) >= 4
            and is_not_in_root_list
        ):
            POGGER.debug("indent")
            (
                can_continue,
                line_to_parse,
                start_index,
                was_paragraph_continuation,
                used_indent,
                text_removed_by_container,
                container_level_tokens,
                leaf_tokens,
                removed_chars_at_start,
                last_block_quote_index,
                last_list_start_index,
                skip_containers_before_leaf_blocks,
                indent_already_processed,
                was_other_paragraph_continuation,
                did_blank,
                force_leaf_token_parse,
            ) = ContainerBlockProcessor.__handle_indented_block_start(
                parser_state, position_marker
            )
        else:
            (
                can_continue,
                container_level_tokens,
                used_indent,
                line_to_parse,
                start_index,
                text_removed_by_container,
                leaf_tokens,
                removed_chars_at_start,
                last_block_quote_index,
                last_list_start_index,
                requeue_line_info,
                block_quote_data,
                extracted_whitespace,
                flags,
                force_list_continuation,
            ) = ContainerBlockProcessor.__handle_non_leaf_block(
                parser_state,
                position_marker,
                container_depth,
                extracted_whitespace,
                start_index,
                adj_ws,
                block_quote_data,
                container_start_bq_count,
                current_container_blocks,
                parser_properties,
            )
            (
                did_blank,
                was_other_paragraph_continuation,
                indent_already_processed,
                force_leaf_token_parse,
                skip_containers_before_leaf_blocks,
                was_paragraph_continuation,
            ) = flags

        # POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)
        # POGGER.debug(
        #     "was_other_paragraph_continuation>>$", was_other_paragraph_continuation
        # )

        # POGGER.debug("line_to_parse>>$", line_to_parse)
        # POGGER.debug("start_index>>$", start_index)

        # POGGER.debug("indent_already_processed=$", indent_already_processed)
        # POGGER.debug("force_leaf_token_parse=$", force_leaf_token_parse)
        # POGGER.debug("did_blank=$", did_blank)
        if (
            can_continue and not skip_containers_before_leaf_blocks and not did_blank
        ) or force_leaf_token_parse:
            # POGGER.debug(">>text_removed_by_container>>:$:", text_removed_by_container)
            # POGGER.debug(
            #     ">>was_paragraph_continuation>>:$:", was_paragraph_continuation
            # )
            requeue_line_info = ContainerBlockProcessor.__handle_leaf_tokens(
                parser_state,
                position_marker,
                line_to_parse,
                used_indent,
                text_removed_by_container,
                start_index,
                container_level_tokens,
                leaf_tokens,
                block_quote_data,
                removed_chars_at_start,
                ignore_link_definition_start,
                last_block_quote_index,
                last_list_start_index,
                was_paragraph_continuation,
                skip_containers_before_leaf_blocks,
                indent_already_processed,
                container_depth,
                force_list_continuation,
            )
            # POGGER.debug(
            #     ">>was_paragraph_continuation>>:$:", was_paragraph_continuation
            # )

        _ = was_other_paragraph_continuation
        return (
            container_level_tokens,
            line_to_parse,
            block_quote_data.current_count,
            requeue_line_info,
            did_blank,
            force_list_continuation,
        )
        # pylint: enable=too-many-locals
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_non_leaf_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        container_depth: int,
        extracted_whitespace: Optional[str],
        start_index: int,
        adj_ws: Optional[str],
        block_quote_data: BlockQuoteData,
        container_start_bq_count: int,
        current_container_blocks: List[StackToken],
        parser_properties: ParseBlockPassProperties,
    ) -> Tuple[
        bool,
        List[MarkdownToken],
        Optional[str],
        str,
        int,
        str,
        List[MarkdownToken],
        Optional[int],
        int,
        int,
        Optional[RequeueLineInfo],
        BlockQuoteData,
        Optional[str],
        Tuple[bool, bool, bool, bool, bool, bool],
        bool,
    ]:

        (
            line_to_parse,
            was_paragraph_continuation,
            text_removed_by_container,
            removed_chars_at_start,
            last_block_quote_index,
            last_list_start_index,
            did_blank,
            requeue_line_info,
            was_other_paragraph_continuation,
        ) = (None, False, None, None, None, None, False, None, False)
        leaf_tokens: List[MarkdownToken] = []

        is_para_continue = (
            bool(
                parser_state.token_stack
                and len(parser_state.token_stack) >= 2
                and parser_state.token_stack[-1].is_paragraph
            )
            and not parser_state.token_document[-1].is_blank_line
        )

        (
            can_continue,
            have_pre_processed_indent,
            container_level_tokens,
            skip_containers_before_leaf_blocks,
            used_pre_indent,
            indent_already_processed,
            force_leaf_token_parse,
            container_used_indent,
        ) = ContainerBlockProcessor.__handle_pre_processed_indent(
            parser_state,
            position_marker,
            container_depth,
            extracted_whitespace,
            is_para_continue,
        )
        # POGGER.debug("start_index>>$", start_index)
        # POGGER.debug("container_used_indent>>$", container_used_indent)
        # POGGER.debug("container_depth>>$", container_depth)
        # POGGER.debug("position_marker.index_number>>$", position_marker.index_number)
        # POGGER.debug("extracted_whitespace>:$:", extracted_whitespace)

        # TODO? test_nested_three_block_max_unordered_max_block_max_empty_with_li
        #
        # if False and position_marker.index_number == -1 and container_depth and start_index > container_used_indent and container_used_indent >= 0:
        #     start_index = container_used_indent
        #     extracted_whitespace = extracted_whitespace[container_used_indent:]
        #     POGGER.debug("start_index>>$", start_index)
        #     POGGER.debug("extracted_whitespace>:$:", extracted_whitespace)
        #     adj_ws = extracted_whitespace

        # POGGER.debug(
        #     "skip_containers_before_leaf_blocks:$:", skip_containers_before_leaf_blocks
        # )
        # POGGER.debug("have_pre_processed_indent:$:", have_pre_processed_indent)
        # POGGER.debug("indent_already_processed=$", indent_already_processed)
        if have_pre_processed_indent:
            (
                can_continue,
                line_to_parse,
                start_index,
                was_paragraph_continuation,
                used_indent,
                text_removed_by_container,
                removed_chars_at_start,
                last_block_quote_index,
                last_list_start_index,
                requeue_line_info,
                container_used_indent,
            ) = (
                True,
                position_marker.text_to_parse[used_pre_indent:],
                used_pre_indent,
                False,
                None,
                "",
                used_pre_indent,
                -1,
                -1,
                None,
                -1,
            )
            leaf_tokens = []
            # POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)
            # POGGER.debug("line_to_parse>>$", line_to_parse)
            # POGGER.debug("start_index>>$", start_index)
        # POGGER.debug(
        #     "not can_continue=$ and not skip_containers_before_leaf_blocks=$",
        #     can_continue,
        #     skip_containers_before_leaf_blocks,
        # )
        force_list_continuation = False
        if not can_continue and not skip_containers_before_leaf_blocks:
            # POGGER.debug("container_used_indent>>$", container_used_indent)
            # POGGER.debug("start_index>>$", start_index)
            # POGGER.debug("parser_state.token_document=$", parser_state.token_document)
            (
                block_quote_data,
                line_to_parse,
                start_index,
                leaf_tokens,
                container_level_tokens,
                removed_chars_at_start,
                last_block_quote_index,
                text_removed_by_container,
                can_continue,
                last_list_start_index,
                used_indent,
                was_paragraph_continuation,
                did_blank,
                requeue_line_info,
                indent_already_processed,
                extracted_whitespace,
                force_list_continuation,
            ) = ContainerBlockProcessor.__handle_normal_containers(
                parser_state,
                position_marker,
                extracted_whitespace,
                adj_ws,
                block_quote_data,
                start_index,
                container_start_bq_count,
                current_container_blocks,
                container_depth,
                parser_properties,
                container_used_indent,
                indent_already_processed,
            )
            # POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)
        # POGGER.debug("line_to_parse>>$", line_to_parse)
        # POGGER.debug("start_index>>$", start_index)
        # POGGER.debug("indent_already_processed=$", indent_already_processed)
        flags = (
            did_blank,
            was_other_paragraph_continuation,
            indent_already_processed,
            force_leaf_token_parse,
            skip_containers_before_leaf_blocks,
            was_paragraph_continuation,
        )
        return (  # type: ignore
            can_continue,
            container_level_tokens,
            used_indent,
            line_to_parse,
            start_index,
            text_removed_by_container,
            leaf_tokens,
            removed_chars_at_start,
            last_block_quote_index,
            last_list_start_index,
            requeue_line_info,
            block_quote_data,
            extracted_whitespace,
            flags,
            force_list_continuation,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __calculate_container_used_indent(
        parser_state: ParserState,
        position_marker: PositionMarker,
        container_depth: int,
        extracted_whitespace: Optional[str],
    ) -> Tuple[int, Optional[str]]:
        POGGER.debug("original_line_to_parse:$:", parser_state.original_line_to_parse)
        POGGER.debug("extracted_whitespace:$:", extracted_whitespace)
        POGGER.debug("text_to_parse=:$:", position_marker.text_to_parse)
        POGGER.debug("parser_state.token_stack=:$:", parser_state.token_stack)
        stack_index = 1
        container_used_indent = 0
        assert parser_state.original_line_to_parse is not None
        while stack_index <= container_depth:
            if parser_state.token_stack[stack_index].is_block_quote:
                container_used_indent = parser_state.original_line_to_parse.find(">")
                assert container_used_indent != -1
                assert (
                    parser_state.original_line_to_parse[container_used_indent + 1]
                    == " "
                )
                container_used_indent += 1

                # TODO add tests with no space between `>` and next block
                assert (
                    container_used_indent < len(parser_state.original_line_to_parse)
                    and parser_state.original_line_to_parse[container_used_indent]
                    == " "
                )
                container_used_indent += 1
            else:
                assert parser_state.token_stack[stack_index].is_list
                list_token = cast(
                    ListStartMarkdownToken, parser_state.token_stack[stack_index]
                )
                delta = list_token.indent_level - container_used_indent
                POGGER.debug("delta=:$:", delta)
                container_used_indent += delta
            POGGER.debug("container_used_indent=:$:", container_used_indent)
            stack_index += 1
        assert stack_index > container_depth
        _, extracted_whitespace = ParserHelper.extract_whitespace(
            parser_state.original_line_to_parse, container_used_indent
        )
        POGGER.debug("container_used_indent=:$:", container_used_indent)
        POGGER.debug("extracted_whitespace=:$:", extracted_whitespace)
        return container_used_indent, extracted_whitespace

    # pylint: disable=too-many-boolean-expressions
    @staticmethod
    def __special_list_block_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
    ) -> Tuple[bool, bool, bool, bool, int]:

        skip_containers_before_leaf_blocks = False
        did_indent_processing = False
        have_pre_processed_indent = False
        force_leaf_token_parse = False
        used_indent = -1
        if (
            parser_state.token_stack[1].is_list
            and parser_state.token_stack[2].is_block_quote
            and parser_state.token_stack[3].is_block_quote
            and parser_state.token_stack[4].is_paragraph
            and parser_state.token_stack[1].matching_markdown_token
            and parser_state.token_stack[3].matching_markdown_token
            and parser_state.token_stack[1].matching_markdown_token.line_number
            == parser_state.token_stack[3].matching_markdown_token.line_number
        ):
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[1].matching_markdown_token,
            )
            container_used_indent = list_token.indent_level
            POGGER.debug("container_used_indent:$:", container_used_indent)
            assert extracted_whitespace is not None
            extracted_whitespace_length = len(extracted_whitespace)
            POGGER.debug(
                "extracted_whitespace:$:($)",
                extracted_whitespace,
                extracted_whitespace_length,
            )
            POGGER.debug("text_to_parse=:$:", position_marker.text_to_parse)
            POGGER.debug(
                "text_to_parse[rt]=:$:",
                position_marker.text_to_parse[extracted_whitespace_length],
            )
            POGGER.debug("index_number=:$:", position_marker.index_number)
            if (
                container_used_indent != extracted_whitespace_length
                and position_marker.text_to_parse[extracted_whitespace_length] == ">"
                and extracted_whitespace_length - container_used_indent >= 4
            ):
                list_token.add_leading_spaces(
                    extracted_whitespace[:container_used_indent]
                )
                skip_containers_before_leaf_blocks = True
                did_indent_processing = True
                have_pre_processed_indent = True
                force_leaf_token_parse = True
                used_indent = container_used_indent
            POGGER.debug(
                "skip_containers_before_leaf_blocks:$:",
                skip_containers_before_leaf_blocks,
            )
        return (
            skip_containers_before_leaf_blocks,
            did_indent_processing,
            have_pre_processed_indent,
            force_leaf_token_parse,
            used_indent,
        )

    # pylint: enable=too-many-boolean-expressions

    @staticmethod
    def __determine_leading_whitespace_preprocessing(
        parser_state: ParserState,
        position_marker: PositionMarker,
        container_depth: int,
        extracted_whitespace: Optional[str],
        is_para_continue: bool,
    ) -> Tuple[bool, bool, bool, bool, int, List[MarkdownToken], bool, int]:

        assert extracted_whitespace is not None
        (
            did_indent_processing,
            indent_already_processed,
            skip_containers_before_leaf_blocks,
            have_pre_processed_indent,
            container_used_indent,
            used_indent,
            force_leaf_token_parse,
        ) = (False, False, False, False, 0, -1, False)
        container_level_tokens: List[MarkdownToken] = []
        POGGER.debug("is_para_continue:$:", is_para_continue)
        if is_para_continue and not container_depth:
            (
                skip_containers_before_leaf_blocks,
                did_indent_processing,
                have_pre_processed_indent,
                force_leaf_token_parse,
                used_indent,
            ) = ContainerBlockProcessor.__special_list_block_block(
                parser_state, position_marker, extracted_whitespace
            )
        elif not is_para_continue:
            POGGER.debug(
                "position_marker.index_number:$:", position_marker.index_number
            )
            POGGER.debug("container_depth:$:", container_depth)
            POGGER.debug("extracted_whitespace:$:", extracted_whitespace)
            if position_marker.index_number == -1 and container_depth:
                (
                    container_used_indent,
                    extracted_whitespace,
                ) = ContainerBlockProcessor.__calculate_container_used_indent(
                    parser_state, position_marker, container_depth, extracted_whitespace
                )
                assert extracted_whitespace is not None
            POGGER.debug("container_used_indent:$:", container_used_indent)
            POGGER.debug("extracted_whitespace:$:", extracted_whitespace)
            if len(extracted_whitespace) >= 4:
                POGGER.debug(">>leading_whitespace_processing")
                (
                    have_pre_processed_indent,
                    used_indent,
                    container_level_tokens,
                ) = ContainerBlockProcessor.__handle_leading_whitespace(
                    parser_state,
                    position_marker,
                    extracted_whitespace,
                    container_depth,
                    container_used_indent,
                )
                (
                    did_indent_processing,
                    skip_containers_before_leaf_blocks,
                    indent_already_processed,
                ) = (True, False, bool(container_depth))
            POGGER.debug("indent_already_processed=$", indent_already_processed)
            POGGER.debug("have_pre_processed_indent=$", have_pre_processed_indent)
            POGGER.debug("used_indent=$", used_indent)
            POGGER.debug("container_level_tokens=$", container_level_tokens)
            POGGER.debug("parser_state.token_document=$", parser_state.token_document)
        return (
            did_indent_processing,
            indent_already_processed,
            skip_containers_before_leaf_blocks,
            have_pre_processed_indent,
            used_indent,
            container_level_tokens,
            force_leaf_token_parse,
            container_used_indent,
        )

    # pylint: disable=too-many-locals
    @staticmethod
    def __handle_pre_processed_indent(
        parser_state: ParserState,
        position_marker: PositionMarker,
        container_depth: int,
        extracted_whitespace: Optional[str],
        is_para_continue: bool,
    ) -> Tuple[bool, bool, List[MarkdownToken], bool, int, bool, bool, int]:
        # POGGER.debug("normal")
        # POGGER.debug(
        #     "container_depth=$ == len(containers)=$ - 1",
        #     container_depth,
        #     len(parser_state.token_stack) - 1,
        # )
        # POGGER.debug("text_to_parse=:$:", position_marker.text_to_parse)
        # POGGER.debug("index_number=:$:", position_marker.index_number)
        # POGGER.debug("index_indent=:$:", position_marker.index_indent)

        (
            can_continue,
            did_indent_processing,
            indent_already_processed,
            force_leaf_token_parse,
            container_used_indent,
        ) = (False, False, False, False, -1)

        need_trailing_indent_processing = (
            container_depth >= len(parser_state.token_stack) - 1
            and position_marker.index_number == -1
        )
        # POGGER.debug(
        #     "need_trailing_indent_processing($) = container_depth($) >= len(token)-1($) and index_number($) == -1",
        #     need_trailing_indent_processing,
        #     container_depth,
        #     len(parser_state.token_stack) - 1,
        #     position_marker.index_number,
        # )
        # POGGER.debug("token-stack:$", parser_state.token_stack)
        assert extracted_whitespace is not None
        need_leading_whitespace_processing = (
            container_depth < (len(parser_state.token_stack) - 1)
            and len(extracted_whitespace) >= 4
            and not (
                parser_state.token_stack[-1].is_html_block
                or parser_state.token_stack[-1].is_fenced_code_block
            )
        )
        # POGGER.debug(
        #     "need_leading_whitespace_processing($) = "
        #     + "not is_para_continue($) and container_depth($) < (len(parser_state.token_stack) - 1)($)"
        #     + " and len(extracted_whitespace)($) >= 4",
        #     need_leading_whitespace_processing,
        #     is_para_continue,
        #     container_depth,
        #     len(parser_state.token_stack) - 1,
        #     len(extracted_whitespace),
        # )
        if need_trailing_indent_processing:
            POGGER.debug(">>trailing_indent_processing")
            (
                have_pre_processed_indent,
                container_level_tokens,
                skip_containers_before_leaf_blocks,
                used_indent,
                did_indent_processing,
            ) = ContainerBlockProcessor.__handle_trailing_indent_with_block_quote(
                parser_state, extracted_whitespace
            )
            # POGGER.debug("have_pre_processed_indent:$:", have_pre_processed_indent)
        elif need_leading_whitespace_processing:
            POGGER.debug(">>leading_whitespace_preprocessing")

            (
                did_indent_processing,
                indent_already_processed,
                skip_containers_before_leaf_blocks,
                have_pre_processed_indent,
                used_indent,
                container_level_tokens,
                force_leaf_token_parse,
                container_used_indent,
            ) = ContainerBlockProcessor.__determine_leading_whitespace_preprocessing(
                parser_state,
                position_marker,
                container_depth,
                extracted_whitespace,
                is_para_continue,
            )
            POGGER.debug("container_used_indent:$:", container_used_indent)
            POGGER.debug("have_pre_processed_indent:$:", have_pre_processed_indent)
            POGGER.debug(
                "skip_containers_before_leaf_blocks:$:",
                skip_containers_before_leaf_blocks,
            )
        # POGGER.debug("did_indent_processing:$:",did_indent_processing)
        if not did_indent_processing:
            (
                have_pre_processed_indent,
                skip_containers_before_leaf_blocks,
                container_level_tokens,
                used_indent,
            ) = (False, False, [], -1)
            # POGGER.debug("have_pre_processed_indent:$:", have_pre_processed_indent)

        # Case 3: list item start or block quote character, needs to be calculated from non-zero level
        # POGGER.debug("have_pre_processed_indent:$:", have_pre_processed_indent)
        return (
            can_continue,
            have_pre_processed_indent,
            container_level_tokens,
            skip_containers_before_leaf_blocks,
            used_indent,
            indent_already_processed,
            force_leaf_token_parse,
            container_used_indent,
        )

    # pylint: enable=too-many-locals

    @staticmethod
    def __handle_trailing_indent_with_block_quote(
        parser_state: ParserState, extracted_whitespace: Optional[str]
    ) -> Tuple[bool, List[MarkdownToken], bool, int, bool]:

        used_indent, did_indent_processing = -1, True
        assert extracted_whitespace is not None
        for stack_index in range(1, len(parser_state.token_stack)):
            POGGER.debug(
                "$>stack:$:", stack_index, parser_state.token_stack[stack_index]
            )
            inner_token = parser_state.token_stack[stack_index].matching_markdown_token
            assert inner_token is not None
            POGGER.debug(
                "$>token:$:",
                stack_index,
                inner_token,
            )
            if inner_token.is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, inner_token)
                assert block_quote_token.leading_spaces is not None
                split_spaces = block_quote_token.leading_spaces.split("\n")
                used_indent = len(split_spaces[-1])
            else:
                assert inner_token.is_list_start
                list_token = cast(ListStartMarkdownToken, inner_token)
                used_indent = list_token.indent_level
        delta = len(extracted_whitespace) - used_indent
        POGGER.debug("len(ws)=$", len(extracted_whitespace))
        POGGER.debug("len(containers)=$", used_indent)
        have_pre_processed_indent = used_indent != -1 and delta >= 4
        return (
            have_pre_processed_indent,
            [],
            have_pre_processed_indent,
            used_indent,
            did_indent_processing,
        )

    @staticmethod
    def __handle_leading_whitespace_loop(
        parser_state: ParserState,
        i: int,
        remaining_whitespace: str,
        used_indent: int,
        container_used_indent: int,
    ) -> Tuple[bool, int, str, int]:
        stack_index = 0
        # POGGER.debug(
        #     "$>remaining_whitespace:$:($)",
        #     i,
        #     remaining_whitespace,
        #     len(remaining_whitespace),
        # )
        # POGGER.debug("$>used_indent:$:", i, used_indent)
        # POGGER.debug("$>container_used_indent:$:", i, container_used_indent)
        # POGGER.debug("$>stack:$:", i, parser_state.token_stack[i])
        # POGGER.debug(
        #     "$>token:$:", i, parser_state.token_stack[i].matching_markdown_token
        # )
        inner_token = parser_state.token_stack[i].matching_markdown_token
        assert inner_token is not None
        if inner_token.is_block_quote_start:
            start_bq_index = remaining_whitespace.find(">")
            if start_bq_index < 0 or start_bq_index >= 4:
                # POGGER.debug("1-->$>start_bq_index:$:", i, start_bq_index)
                # POGGER.debug("$>remaining_whitespace:$:", i, remaining_whitespace)
                if len(remaining_whitespace) >= 4:
                    stack_index = i
                return True, stack_index, remaining_whitespace, used_indent
            raise AssertionError()
        if not inner_token.is_list_start:
            # POGGER.debug("2-->")
            if len(remaining_whitespace) >= 4:
                stack_index = (
                    i + 1 if parser_state.token_stack[i].is_indented_code_block else i
                )
            return True, stack_index, remaining_whitespace, used_indent
        assert inner_token.is_list_start
        list_token = cast(ListStartMarkdownToken, inner_token)
        remaining_indent = list_token.indent_level - (
            used_indent + container_used_indent
        )
        # POGGER.debug("$>remaining_indent:$:", i, remaining_indent)
        left_whitespace = remaining_whitespace[:remaining_indent]
        # POGGER.debug("$>left_whitespace:$:", i, left_whitespace)
        if len(left_whitespace) < remaining_indent:
            if len(remaining_whitespace) >= 4:
                stack_index = i
            # POGGER.debug("3-->")
            return True, stack_index, remaining_whitespace, used_indent
        remaining_whitespace = remaining_whitespace[remaining_indent:]
        used_indent = list_token.indent_level
        return False, stack_index, remaining_whitespace, used_indent

    # pylint: disable=too-many-locals
    @staticmethod
    def __handle_leading_whitespace(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        container_depth: int,
        container_used_indent: int,
    ) -> Tuple[bool, int, List[MarkdownToken]]:
        assert extracted_whitespace is not None
        used_indent, stack_index, remaining_whitespace = 0, 0, extracted_whitespace[:]
        POGGER.debug(">remaining_whitespace:$:", remaining_whitespace)
        for i in range(container_depth + 1, len(parser_state.token_stack)):
            (
                do_break,
                stack_index,
                remaining_whitespace,
                used_indent,
            ) = ContainerBlockProcessor.__handle_leading_whitespace_loop(
                parser_state,
                i,
                remaining_whitespace,
                used_indent,
                container_used_indent,
            )
            # POGGER.debug(">do_break:$:", do_break)
            # POGGER.debug(">stack_index:$:", stack_index)
            # POGGER.debug(">remaining_whitespace:$:", remaining_whitespace)
            # POGGER.debug(">used_indent:$:", used_indent)
            if do_break:
                # POGGER.debug(">break!")
                break
        POGGER.debug(">stack_index:$:", stack_index)
        POGGER.debug(">container_used_indent:$:", container_used_indent)
        if stack_index:
            have_pre_processed_indent = True
            container_level_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                include_lists=True,
                include_block_quotes=True,
                was_forced=True,
                until_this_index=stack_index,
            )
            ind = parser_state.find_last_container_on_stack()
            if parser_state.token_stack[ind].is_list:
                ind2 = parser_state.find_last_block_quote_on_stack()
                block_quote_end_index = container_used_indent + 1 if ind2 else 0
                # POGGER.debug(">ind2:$:", ind2)
                extra_indent = 1 if container_depth else 0
                list_token = cast(
                    ListStartMarkdownToken,
                    parser_state.token_stack[ind].matching_markdown_token,
                )
                list_token.add_leading_spaces(
                    position_marker.text_to_parse[
                        block_quote_end_index : used_indent + extra_indent
                    ]
                )

            # POGGER.debug(">text_to_parse:$:", position_marker.text_to_parse)
            # POGGER.debug(">xx:$:", used_indent)
            # POGGER.debug(
            #     ">text_to_parse[used_indent:]:$:",
            #     position_marker.text_to_parse[used_indent:],
            # )
        else:
            have_pre_processed_indent, used_indent, container_level_tokens = (
                False,
                -1,
                [],
            )
        POGGER.debug(">have_pre_processed_indent:$:", have_pre_processed_indent)
        POGGER.debug(">used_indent:$:", used_indent)
        return have_pre_processed_indent, used_indent, container_level_tokens

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-locals
    @staticmethod
    def __handle_indented_block_start(
        parser_state: ParserState, position_marker: PositionMarker
    ) -> Tuple[
        bool,
        str,
        int,
        bool,
        Optional[str],
        str,
        List[MarkdownToken],
        List[MarkdownToken],
        int,
        int,
        int,
        bool,
        bool,
        bool,
        bool,
        bool,
    ]:
        (
            can_continue,
            line_to_parse,
            start_index,
            was_paragraph_continuation,
            used_indent,
            text_removed_by_container,
            container_level_tokens,
            removed_chars_at_start,
            last_block_quote_index,
            last_list_start_index,
            indent_already_processed,
            was_other_paragraph_continuation,
            did_blank,
            force_leaf_token_parse,
        ) = (
            True,
            position_marker.text_to_parse,
            position_marker.index_number,
            False,
            None,
            "",
            [],
            0,
            -1,
            -1,
            False,
            False,
            False,
            False,
        )
        leaf_tokens: List[MarkdownToken] = []
        POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)
        POGGER.debug("parser_state.token_stack>>$", parser_state.token_stack)
        is_paragraph_continuation = (
            parser_state.token_stack and parser_state.token_stack[-1].is_paragraph
        )
        list_index = parser_state.find_last_list_block_on_stack()
        block_index = parser_state.find_last_block_quote_on_stack()
        POGGER.debug("list_index>>$", list_index)
        POGGER.debug("block_index>>$", block_index)
        if is_paragraph_continuation and block_index > list_index:
            was_paragraph_continuation = True
        if is_paragraph_continuation and block_index < list_index:
            was_other_paragraph_continuation = True
        POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)
        if (
            not is_paragraph_continuation
            and parser_state.token_stack
            and len(parser_state.token_stack) >= 2
            and parser_state.token_stack[1].is_block_quote
        ):
            x_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                include_lists=True,
                include_block_quotes=True,
            )
            # POGGER.debug("x_tokens=:$:", x_tokens)
            container_level_tokens = x_tokens
        return (
            can_continue,
            line_to_parse,
            start_index,
            was_paragraph_continuation,
            used_indent,
            text_removed_by_container,
            container_level_tokens,
            leaf_tokens,
            removed_chars_at_start,
            last_block_quote_index,
            last_list_start_index,
            False,
            indent_already_processed,
            was_other_paragraph_continuation,
            did_blank,
            force_leaf_token_parse,
        )

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_normal_containers(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        adj_ws: Optional[str],
        block_quote_data: BlockQuoteData,
        start_index: int,
        container_start_bq_count: int,
        current_container_blocks: List[StackToken],
        container_depth: int,
        parser_properties: ParseBlockPassProperties,
        container_used_indent: int,
        indent_already_processed: bool,
    ) -> Tuple[
        BlockQuoteData,
        str,
        int,
        List[MarkdownToken],
        List[MarkdownToken],
        Optional[int],
        int,
        Optional[str],
        bool,
        int,
        Optional[str],
        bool,
        bool,
        Optional[RequeueLineInfo],
        bool,
        Optional[str],
        bool,
    ]:
        (
            end_container_indices,
            did_process,
            block_quote_data,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            removed_chars_at_start,
            did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            requeue_line_info,
            indent_already_processed,
            extracted_whitespace,
            force_list_continuation,
        ) = ContainerBlockProcessor.__check_for_container_starts(
            parser_state,
            position_marker,
            extracted_whitespace,
            adj_ws,
            block_quote_data,
            start_index,
            container_start_bq_count,
            current_container_blocks,
            container_used_indent,
            container_depth,
            indent_already_processed,
        )
        POGGER.debug("force_list_continuation=$", force_list_continuation)
        # POGGER.debug("line_to_parse>>$", line_to_parse)
        # POGGER.debug("start_index>>$", start_index)
        # POGGER.debug(">>text_removed_by_container>>:$:", text_removed_by_container)
        # POGGER.debug("container_level_tokens>>$>>", container_level_tokens)

        if requeue_line_info or did_blank:
            return (
                block_quote_data,
                line_to_parse,
                -1,
                [],
                container_level_tokens,
                None,
                -1,
                None,
                False,
                -1,
                None,
                False,
                did_blank,
                requeue_line_info,
                indent_already_processed,
                extracted_whitespace,
                False,
            )

        # POGGER.debug(">>text_removed_by_container>>:$:", text_removed_by_container)
        (
            can_continue,
            line_to_parse,
            leaf_tokens,
            container_level_tokens,
            block_quote_data,
            last_list_start_index,
            text_removed_by_container,
            did_blank,
            nested_force_list_continuation,
        ) = ContainerBlockProcessor.__handle_nested_blocks(
            parser_state,
            container_depth,
            block_quote_data,
            parser_properties,
            end_container_indices,
            leaf_tokens,
            container_level_tokens,
            did_process,
            avoid_block_starts,
            start_index,
            removed_chars_at_start,
            text_removed_by_container,
            position_marker,
            line_to_parse,
            last_block_quote_index,
        )
        if force_list_continuation:
            POGGER.debug(
                "nested_force_list_continuation=$", nested_force_list_continuation
            )
            assert not nested_force_list_continuation
        # POGGER.debug("line_to_parse>>$", line_to_parse)
        # POGGER.debug("start_index>>$", start_index)
        # POGGER.debug(">>text_removed_by_container>>:$:", text_removed_by_container)
        # POGGER.debug(">>can_continue>>:$:", can_continue)
        if can_continue:
            (
                can_continue,
                did_process,
                line_to_parse,
                container_level_tokens,
                used_indent,
                block_quote_data,
                requeue_line_info,
                was_paragraph_continuation,
            ) = ContainerBlockProcessor.__handle_block_continuations(
                parser_state,
                position_marker,
                did_process,
                line_to_parse,
                start_index,
                container_level_tokens,
                extracted_whitespace,
                leaf_tokens,
                block_quote_data,
                container_start_bq_count,
            )
            # POGGER.debug("line_to_parse>>$", line_to_parse)
            # POGGER.debug("start_index>>$", start_index)
        else:
            used_indent, was_paragraph_continuation = None, False
        # POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)
        return (
            block_quote_data,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            removed_chars_at_start,
            last_block_quote_index,
            text_removed_by_container,
            can_continue,
            last_list_start_index,
            used_indent,
            was_paragraph_continuation,
            did_blank,
            requeue_line_info,
            indent_already_processed,
            extracted_whitespace,
            force_list_continuation,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __prepare_container_start_variables(
        parser_state: ParserState,
        position_marker: PositionMarker,
        container_depth: int,
    ) -> PositionMarker:
        # POGGER.debug("Stack Depth:$:", parser_state.original_stack_depth)
        # POGGER.debug("Document Depth:$:", parser_state.original_document_depth)
        if container_depth:
            return position_marker

        if ParserHelper.tab_character in position_marker.text_to_parse:
            line_to_parse = ParserHelper.detabify_string(position_marker.text_to_parse)
            POGGER.debug("Before tab replacement:$:", position_marker.text_to_parse)
            POGGER.debug("After tab replacement :$:", line_to_parse)
            position_marker = PositionMarker(
                position_marker.line_number,
                position_marker.index_number,
                line_to_parse,
                position_marker.index_indent,
            )

        parser_state.mark_start_information(position_marker)

        parser_state.copy_of_token_stack = []
        parser_state.copy_of_token_stack.extend(parser_state.token_stack)

        parser_state.block_copy = [
            copy.deepcopy(i.matching_markdown_token)
            for i in parser_state.token_stack
            if not i.is_document
        ]

        return position_marker

    @staticmethod
    def __prepare_container_start_variables2(
        parser_state: ParserState,
        position_marker: PositionMarker,
        foobar: Optional[int],
        init_bq: Optional[int],
        container_depth: int,
    ) -> Tuple[List[StackToken], Optional[str], BlockQuoteData, int, Optional[str]]:
        # Debug to be used for block quotes if needed.
        # POGGER.debug(
        #    "Last Block Quote:$:",
        #    parser_state.last_block_quote_stack_token,
        # )
        # POGGER.debug(
        #    "Last Block Quote:$:",
        #    parser_state.last_block_quote_markdown_token_index,
        # )
        # POGGER.debug(
        #    "Last Block Quote:$:", parser_state.copy_of_last_block_quote_markdown_token
        # )

        start_index, extracted_whitespace = ParserHelper.extract_whitespace(
            position_marker.text_to_parse, 0
        )
        assert start_index is not None
        (
            current_container_blocks,
            adj_ws,
            block_quote_data,
        ) = ContainerBlockProcessor.__calculate_for_container_blocks(
            parser_state,
            position_marker.text_to_parse,
            extracted_whitespace,
            foobar,
            init_bq,
            container_depth,
        )
        return (
            current_container_blocks,
            adj_ws,
            block_quote_data,
            start_index,
            extracted_whitespace,
        )

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_block_continuations(
        parser_state: ParserState,
        position_marker: PositionMarker,
        did_process: bool,
        line_to_parse: str,
        start_index: int,
        container_level_tokens: List[MarkdownToken],
        extracted_whitespace: Optional[str],
        leaf_tokens: List[MarkdownToken],
        block_quote_data: BlockQuoteData,
        container_start_bq_count: int,
    ) -> Tuple[
        bool,
        bool,
        str,
        List[MarkdownToken],
        Optional[str],
        BlockQuoteData,
        Optional[RequeueLineInfo],
        bool,
    ]:
        # POGGER.debug_with_visible_whitespace(
        #     ">>__process_list_in_progress>>$>>",
        #     line_to_parse,
        # )
        if not did_process:
            (
                did_process,
                line_to_parse,
                container_level_tokens,
                used_indent,
                requeue_line_info,
                was_paragraph_continuation,
            ) = ContainerBlockProcessor.__process_list_in_progress(
                parser_state,
                line_to_parse,
                start_index,
                container_level_tokens,
                extracted_whitespace,
            )
            # POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)
            if not requeue_line_info:
                # POGGER.debug_with_visible_whitespace(
                #     ">>__process_list_in_progress>>$>>", line_to_parse
                # )
                # POGGER.debug("container_start_bq_count>>$", container_start_bq_count)
                # POGGER.debug("block_quote_data.current_count>>$", block_quote_data.current_count)
                # POGGER.debug("block_quote_data.stack_count>>$", block_quote_data.stack_count)
                (
                    block_quote_data,
                    was_paragraph_continuation,
                ) = ContainerBlockProcessor.__process_lazy_lines(
                    parser_state,
                    position_marker,
                    leaf_tokens,
                    block_quote_data,
                    line_to_parse,
                    container_level_tokens,
                    container_start_bq_count,
                    was_paragraph_continuation,
                )
                # POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)
        else:
            requeue_line_info, used_indent, was_paragraph_continuation = (
                None,
                None,
                False,
            )
            # POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)

            is_paragraph_continuation = (
                parser_state.token_stack and parser_state.token_stack[-1].is_paragraph
            )
            list_index = parser_state.find_last_list_block_on_stack()
            block_index = parser_state.find_last_block_quote_on_stack()
            # POGGER.debug("is_paragraph_continuation($) and block_index($) > list_index($)",
            #     is_paragraph_continuation, block_index, list_index)
            if is_paragraph_continuation and block_index > list_index:
                was_paragraph_continuation = True
            # POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)

        return (
            not requeue_line_info,
            did_process,
            line_to_parse,
            container_level_tokens,
            used_indent,
            block_quote_data,
            requeue_line_info,
            was_paragraph_continuation,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __check_for_container_starts(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        adj_ws: Optional[str],
        block_quote_data: BlockQuoteData,
        start_index: int,
        container_start_bq_count: int,
        current_container_blocks: List[StackToken],
        container_used_indent: int,
        container_depth: int,
        indent_already_processed: bool,
    ) -> Tuple[
        ContainerIndices,
        bool,
        BlockQuoteData,
        str,
        int,
        List[MarkdownToken],
        List[MarkdownToken],
        int,
        bool,
        int,
        Optional[str],
        bool,
        Optional[RequeueLineInfo],
        bool,
        Optional[str],
        bool,
    ]:

        # POGGER.debug(f"cfcs>extracted_whitespace>:{extracted_whitespace}:")
        # POGGER.debug(f"cfcs>adj_ws>:{adj_ws}:")

        # POGGER.debug("block_quote_data.current_count>>$", block_quote_data.current_count)

        POGGER.debug("container_used_indent>>$", container_used_indent)
        POGGER.debug("start_index>>$", start_index)

        end_container_indices = ContainerIndices(-1, -1, -1)
        parser_state.nested_list_start = None
        (
            can_continue,
            did_process,
            end_container_indices.block_index,
            block_quote_data,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            removed_chars_at_start,
            did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            requeue_line_info,
            force_list_continuation,
        ) = ContainerBlockProcessor.__get_block_start_index(
            position_marker,
            parser_state,
            extracted_whitespace,
            adj_ws,
            block_quote_data,
            start_index,
            container_start_bq_count,
        )
        POGGER.debug("force_list_continuation=$", force_list_continuation)
        POGGER.debug(">>text_removed_by_container>>:$:", text_removed_by_container)
        if can_continue:
            # POGGER.debug("block_quote_data.current_count>>$", block_quote_data.current_count)
            # POGGER.debug("block_quote_data.stack_count>>$", block_quote_data.stack_count)
            # POGGER.debug(">>avoid_block_starts>>$", avoid_block_starts)
            # POGGER.debug(">>did_process>>$", did_process)

            (
                did_process,
                end_container_indices.ulist_index,
                line_to_parse,
                removed_chars_at_start,
                block_quote_data,
                requeue_line_info,
                indent_already_processed,
                extracted_whitespace,
            ) = ContainerBlockProcessor.__get_list_start_index(
                position_marker,
                line_to_parse,
                start_index,
                True,
                parser_state,
                did_process,
                extracted_whitespace,
                adj_ws,
                block_quote_data,
                removed_chars_at_start,
                current_container_blocks,
                container_level_tokens,
                container_depth,
                indent_already_processed,
            )
            can_continue = not requeue_line_info
            if not can_continue:
                POGGER.debug(
                    ">>requeuing lines after looking for ordered list start. returning."
                )

        if can_continue:
            # POGGER.debug("block_quote_data.current_count>>$", block_quote_data.current_count)
            # POGGER.debug("block_quote_data.stack_count>>$", block_quote_data.stack_count)
            # POGGER.debug("was_container_start>>$", was_container_start)
            (
                did_process,
                end_container_indices.olist_index,
                line_to_parse,
                removed_chars_at_start,
                block_quote_data,
                requeue_line_info,
                indent_already_processed,
                extracted_whitespace,
            ) = ContainerBlockProcessor.__get_list_start_index(
                position_marker,
                line_to_parse,
                start_index,
                False,
                parser_state,
                did_process,
                extracted_whitespace,
                adj_ws,
                block_quote_data,
                removed_chars_at_start,
                current_container_blocks,
                container_level_tokens,
                container_depth,
                indent_already_processed,
            )
            if requeue_line_info:
                POGGER.debug(
                    ">>requeuing lines after looking for unordered list start. returning."
                )

        return (
            end_container_indices,
            did_process,
            block_quote_data,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            removed_chars_at_start,
            did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            requeue_line_info,
            indent_already_processed,
            extracted_whitespace,
            force_list_continuation,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_nested_blocks(
        parser_state: ParserState,
        container_depth: int,
        block_quote_data: BlockQuoteData,
        parser_properties: ParseBlockPassProperties,
        end_container_indices: ContainerIndices,
        leaf_tokens: List[MarkdownToken],
        container_level_tokens: List[MarkdownToken],
        was_container_start: bool,
        avoid_block_starts: bool,
        start_index: int,
        removed_chars_at_start: int,
        text_removed_by_container: Optional[str],
        position_marker: PositionMarker,
        line_to_parse: str,
        last_block_quote_index: int,
    ) -> Tuple[
        bool,
        str,
        List[MarkdownToken],
        List[MarkdownToken],
        BlockQuoteData,
        int,
        Optional[str],
        bool,
        bool,
    ]:

        # POGGER.debug("block_quote_data.current_count>>$", block_quote_data.current_count)
        # POGGER.debug("block_quote_data.stack_count>>$", block_quote_data.stack_count)

        # POGGER.debug("last_block_quote_index>>$", last_block_quote_index)
        # POGGER.debug("indices>>$", end_container_indices)
        # POGGER.debug("line_to_parse(after containers)>>$", line_to_parse)
        # POGGER.debug("was_container_start>>$", was_container_start)

        last_list_start_index = 0
        if end_container_indices.block_index != -1:
            assert last_block_quote_index in (
                end_container_indices.block_index - 1,
                end_container_indices.block_index,
            )
        elif end_container_indices.olist_index != -1:
            last_list_start_index = end_container_indices.olist_index
        elif end_container_indices.ulist_index != -1:
            last_list_start_index = end_container_indices.ulist_index

        if not parser_state.token_stack[-1].is_fenced_code_block:
            new_position_marker = PositionMarker(
                position_marker.line_number, start_index, line_to_parse
            )
            # POGGER.debug("block_quote_data.current_count>>$", block_quote_data.current_count)
            # POGGER.debug("block_quote_data.stack_count>>$", block_quote_data.stack_count)
            # POGGER.debug("was_container_start>>$", was_container_start)
            (
                line_to_parse,
                leaf_tokens,
                container_level_tokens,
                block_quote_data,
                did_process_blank_line,
                nested_removed_text,
                was_indent_text_added,
                force_list_continuation,
            ) = ContainerBlockProcessor.__handle_nested_container_blocks(
                parser_state,
                container_depth,
                block_quote_data,
                new_position_marker,
                parser_properties,
                end_container_indices,
                leaf_tokens,
                container_level_tokens,
                was_container_start,
                avoid_block_starts,
                start_index,
                removed_chars_at_start,
                text_removed_by_container,
            )
            # POGGER.debug_with_visible_whitespace("line_to_parse>>$>>", line_to_parse)
            # POGGER.debug("block_quote_data.current_count>>$", block_quote_data.current_count)
            # POGGER.debug("block_quote_data.stack_count>>$", block_quote_data.stack_count)
        else:
            (
                did_process_blank_line,
                nested_removed_text,
                was_indent_text_added,
                force_list_continuation,
            ) = (False, None, False, False)

        # POGGER.debug("olist->container_level_tokens->$", container_level_tokens)
        # POGGER.debug("removed_chars_at_start>>>$", removed_chars_at_start)
        POGGER.debug("text_removed_by_container>>>:$:", text_removed_by_container)
        POGGER.debug_with_visible_whitespace(
            "nested_removed_text>>>:$:", nested_removed_text
        )
        if nested_removed_text is not None:
            text_removed_by_container = nested_removed_text
        POGGER.debug("text_removed_by_container>>>:$:", text_removed_by_container)
        can_continue = not (
            container_depth or did_process_blank_line or was_indent_text_added
        )
        POGGER.debug(
            ">>can_continue>>:$: = not(container_depth($) or "
            + "did_process_blank_line($) or was_indent_text_added($))",
            can_continue,
            container_depth,
            did_process_blank_line,
            was_indent_text_added,
        )
        return (
            can_continue,
            line_to_parse,
            leaf_tokens,
            container_level_tokens,
            block_quote_data,
            last_list_start_index,
            text_removed_by_container,
            did_process_blank_line,
            force_list_continuation,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_leaf_tokens(
        parser_state: ParserState,
        position_marker: PositionMarker,
        line_to_parse: str,
        used_indent: Optional[str],
        text_removed_by_container: str,
        start_index: int,
        container_level_tokens: List[MarkdownToken],
        leaf_tokens: List[MarkdownToken],
        block_quote_data: BlockQuoteData,
        removed_chars_at_start: Optional[int],
        ignore_link_definition_start: bool,
        last_block_quote_index: int,
        last_list_start_index: int,
        was_paragraph_continuation: bool,
        skip_containers_before_leaf_blocks: bool,
        indent_already_processed: bool,
        container_depth: int,
        force_list_continuation: bool,
    ) -> Optional[RequeueLineInfo]:
        # POGGER.debug("line_to_parse>>$", line_to_parse)
        # POGGER.debug("start_index>>$", start_index)
        # POGGER.debug_with_visible_whitespace("text>>$>>", line_to_parse)
        # POGGER.debug("container_level_tokens>>$>>", container_level_tokens)
        # POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)

        assert parser_state.original_line_to_parse is not None
        calculated_indent = len(parser_state.original_line_to_parse) - len(
            line_to_parse
        )
        # POGGER.debug(">>indent>>$", calculated_indent)

        assert not (
            used_indent
            and parser_state.token_stack[-1].is_paragraph
            and parser_state.token_stack[-2].is_block_quote
            and ">" in used_indent
        )

        newer_position_marker = PositionMarker(
            position_marker.line_number,
            start_index,
            line_to_parse,
            index_indent=calculated_indent,
        )
        parser_state.mark_for_leaf_processing(container_level_tokens)
        leaf_tokens, requeue_line_info = ContainerBlockProcessor.__process_leaf_tokens(
            parser_state,
            leaf_tokens,
            newer_position_marker,
            block_quote_data,
            removed_chars_at_start,
            ignore_link_definition_start,
            last_block_quote_index,
            last_list_start_index,
            text_removed_by_container,
            was_paragraph_continuation,
            skip_containers_before_leaf_blocks,
            indent_already_processed,
            container_depth,
            force_list_continuation,
        )
        parser_state.clear_after_leaf_processing()

        container_level_tokens.extend(leaf_tokens)
        return requeue_line_info

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    # pylint: disable=too-many-locals, too-many-arguments
    def __get_block_start_index(
        position_marker: PositionMarker,
        parser_state: ParserState,
        extracted_whitespace: Optional[str],
        adj_ws: Optional[str],
        block_quote_data: BlockQuoteData,
        start_index: int,
        container_start_bq_count: int,
    ) -> Tuple[
        bool,
        bool,
        int,
        BlockQuoteData,
        str,
        int,
        List[MarkdownToken],
        List[MarkdownToken],
        int,
        bool,
        int,
        str,
        bool,
        Optional[RequeueLineInfo],
        bool,
    ]:
        POGGER.debug("text_to_parse>$<", position_marker.text_to_parse)
        POGGER.debug("index_number>$<", position_marker.index_number)
        POGGER.debug("index_indent>$<", position_marker.index_indent)
        new_position_marker = PositionMarker(
            position_marker.line_number, start_index, position_marker.text_to_parse
        )
        POGGER.debug("text_to_parse>$<", new_position_marker.text_to_parse)
        POGGER.debug("index_number>$<", new_position_marker.index_number)
        POGGER.debug("start_index>>:$:", start_index)
        (
            did_process,
            block_index,
            block_quote_data,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            removed_chars_at_start,
            did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            requeue_line_info,
            force_list_continuation,
        ) = BlockQuoteProcessor.handle_block_quote_block(
            parser_state,
            new_position_marker,
            extracted_whitespace,
            adj_ws,
            block_quote_data,
            container_start_bq_count,
        )
        POGGER.debug("force_list_continuation>>:$:", force_list_continuation)
        POGGER.debug("start_index>>:$:", start_index)
        # POGGER.debug("container_start_bq_count>>:$", container_start_bq_count)
        # POGGER.debug("block_quote_data.current_count>>:$", block_quote_data.current_count)
        # POGGER.debug("block_quote_data.stack_count>>$", block_quote_data.stack_count)
        # POGGER.debug("did_process>>$", did_process)
        POGGER.debug("text>>:$:>>", line_to_parse)
        # POGGER.debug(">>container_level_tokens>>$", container_level_tokens)
        # POGGER.debug(">>leaf_tokens>>$", leaf_tokens)

        if requeue_line_info:
            POGGER.debug(">>requeuing lines after looking for block start. returning.")

        if did_blank:
            POGGER.debug(">>already handled blank line. returning.")
            container_level_tokens.extend(leaf_tokens)

        POGGER.debug(">>text_removed_by_container>>:$:", text_removed_by_container)
        POGGER.debug(">>start_index>>:$:", start_index)
        return (  # type: ignore
            not requeue_line_info and not did_blank,
            did_process,
            block_index,
            block_quote_data,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            removed_chars_at_start,
            did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            requeue_line_info,
            force_list_continuation,
        )

    # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def __get_list_start_index(
        position_marker: PositionMarker,
        line_to_parse: str,
        start_index: int,
        is_ulist: bool,
        parser_state: ParserState,
        did_process: bool,
        extracted_whitespace: Optional[str],
        adj_ws: Optional[str],
        block_quote_data: BlockQuoteData,
        removed_chars_at_start: int,
        current_container_blocks: List[StackToken],
        container_level_tokens: List[MarkdownToken],
        container_depth: int,
        indent_already_processed: bool,
    ) -> Tuple[
        bool,
        int,
        str,
        int,
        BlockQuoteData,
        Optional[RequeueLineInfo],
        bool,
        Optional[str],
    ]:
        """
        Note: This is one of the more heavily traffic functions in the
        parser.  Debugging should be uncommented only if needed.
        """
        new_position_marker = PositionMarker(
            position_marker.line_number, start_index, line_to_parse
        )

        POGGER.debug(
            "pre-list>>#$#$#$#",
            position_marker.index_number,
            position_marker.index_indent,
            position_marker.text_to_parse,
        )
        POGGER.debug(
            "pre-list>>#$#$#$#",
            new_position_marker.index_number,
            new_position_marker.index_indent,
            new_position_marker.text_to_parse,
        )
        if not did_process:
            (
                did_process,
                new_list_index,
                new_line_to_parse,
                resultant_tokens,
                removed_chars_at_start,
                block_quote_data,
                requeue_line_info,
                indent_already_processed,
                extracted_whitespace,
            ) = ListBlockProcessor.handle_list_block(
                is_ulist,
                parser_state,
                new_position_marker,
                extracted_whitespace,
                adj_ws,
                block_quote_data,
                removed_chars_at_start,
                current_container_blocks,
                container_depth,
                indent_already_processed,
            )
            # POGGER.debug_with_visible_whitespace("handle_list_block>$", resultant_tokens)
            if requeue_line_info:
                return (
                    False,
                    -1,
                    line_to_parse,
                    removed_chars_at_start,
                    block_quote_data,
                    requeue_line_info,
                    indent_already_processed,
                    extracted_whitespace,
                )
            assert new_line_to_parse is not None
            line_to_parse = new_line_to_parse
            container_level_tokens.extend(resultant_tokens)
        else:
            new_list_index = -1
        POGGER.debug(
            "post-ulist>>#$#$#$#",
            position_marker.index_number,
            position_marker.index_indent,
            position_marker.text_to_parse,
        )
        POGGER.debug(
            "post-ulist>>#$#$#$#",
            new_position_marker.index_number,
            new_position_marker.index_indent,
            new_position_marker.text_to_parse,
        )
        POGGER.debug("text>>$>>", line_to_parse)

        return (
            did_process,
            new_list_index,
            line_to_parse,
            removed_chars_at_start,
            block_quote_data,
            None,
            indent_already_processed,
            extracted_whitespace,
        )

    # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_for_container_blocks(
        parser_state: ParserState,
        line_to_parse: str,
        extracted_whitespace: Optional[str],
        foobar: Optional[int],
        init_bq: Optional[int],
        container_depth: int,
    ) -> Tuple[List[StackToken], Optional[str], BlockQuoteData]:
        """
        Perform some calculations that will be needed for parsing the container blocks.
        """
        current_container_blocks: List[StackToken] = [
            ind for ind in parser_state.token_stack if ind.is_list
        ]

        adj_ws = ContainerBlockProcessor.__calculate_adjusted_whitespace(
            parser_state,
            current_container_blocks,
            line_to_parse,
            extracted_whitespace,
            container_depth,
            foobar=foobar,
        )

        return (
            current_container_blocks,
            adj_ws,
            BlockQuoteData(
                0 if init_bq is None else init_bq,
                parser_state.count_of_block_quotes_on_stack(),
            ),
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __look_back_in_document_for_block_quote(
        parser_state: ParserState, token_index: int
    ) -> Optional[BlockQuoteMarkdownToken]:
        other_block_quote_token, other_token_index = None, token_index
        while other_token_index >= 0:
            if parser_state.token_document[other_token_index].is_block_quote_start:
                other_block_quote_token = cast(
                    BlockQuoteMarkdownToken,
                    parser_state.token_document[other_token_index],
                )
                break
            other_token_index -= 1
        POGGER.debug_with_visible_whitespace(
            "PLFCB>>other_block_quote_token>>$",
            other_block_quote_token,
        )
        return other_block_quote_token

    @staticmethod
    def __calculate_adjusted_whitespace_kludge_without_found(
        parser_state: ParserState, token_index: int, container_depth: int
    ) -> Tuple[bool, int]:
        other_block_quote_token = (
            ContainerBlockProcessor.__look_back_in_document_for_block_quote(
                parser_state, token_index
            )
        )

        # Check to see if out first block token is the same as our first.
        # if not, do not use it as a base.
        #
        # Note; may need to be tweaked for extra levels.
        if not container_depth and other_block_quote_token:
            POGGER.debug(
                "parser_state.token_stack[1]>>:$:", parser_state.token_stack[1]
            )
            if (
                parser_state.token_stack[1].matching_markdown_token
                != other_block_quote_token
            ):
                other_block_quote_token = None

        if other_block_quote_token:
            POGGER.debug("PLFCB>>other_block_quote_token>>:$:", other_block_quote_token)
            POGGER.debug(
                "PLFCB>>other_block_quote_token.leading_text_index>>:$:",
                other_block_quote_token.leading_text_index,
            )
            leading_spaces = other_block_quote_token.calculate_next_leading_space_part(
                increment_index=False, delta=-1
            )
            POGGER.debug("PLFCB>>leading_spaces>>:$:", leading_spaces)
            POGGER.debug("PLFCB>>other_block_quote_token>>:$:", other_block_quote_token)
            POGGER.debug(
                "PLFCB>>other_block_quote_token.leading_text_index>>:$:",
                other_block_quote_token.leading_text_index,
            )
            force_reline = True
            old_start_index = len(leading_spaces)
        else:
            force_reline = False
            list_token = cast(
                ListStartMarkdownToken, parser_state.token_document[token_index]
            )
            old_start_index = list_token.indent_level
        return force_reline, old_start_index

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_adjusted_whitespace_kludge(
        parser_state: ParserState,
        token_index: int,
        extracted_whitespace: Optional[str],
        previous_ws_len: int,
        found_block_quote_token: Optional[BlockQuoteMarkdownToken],
        line_to_parse: str,
        adj_ws: Optional[str],
        container_depth: int,
    ) -> Optional[str]:

        assert extracted_whitespace is not None
        force_reline, ws_len = (
            False,
            ParserHelper.calculate_length(extracted_whitespace) + previous_ws_len,
        )
        if found_block_quote_token:
            leading_spaces = found_block_quote_token.calculate_next_leading_space_part(
                increment_index=False, delta=-1, allow_overflow=True
            )
            POGGER.debug("PLFCB>>leading_spaces>>:$:", leading_spaces)
            old_start_index = len(leading_spaces)
        else:
            (
                force_reline,
                old_start_index,
            ) = ContainerBlockProcessor.__calculate_adjusted_whitespace_kludge_without_found(
                parser_state, token_index, container_depth
            )
        POGGER.debug(
            "old_start_index>>$>>ws_len>>$>>force_reline>>$",
            old_start_index,
            ws_len,
            force_reline,
        )
        if force_reline or ws_len >= old_start_index:
            POGGER.debug("RELINE:$:", line_to_parse)
            adj_ws = extracted_whitespace[old_start_index:]
            POGGER.debug("extracted_whitespace:$:", extracted_whitespace)
            POGGER.debug("adj_ws:$: old_start_index:$:", adj_ws, old_start_index)
        return adj_ws

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_adjusted_whitespace(
        parser_state: ParserState,
        current_container_blocks: List[StackToken],
        line_to_parse: str,
        extracted_whitespace: Optional[str],
        container_depth: int,
        foobar: Optional[int] = None,
        previous_ws_len: int = 0,
    ) -> Optional[str]:
        """
        Based on the last container on the stack, determine what the adjusted whitespace is.
        """

        adj_ws, stack_index = (
            extracted_whitespace,
            parser_state.find_last_list_block_on_stack(),
        )
        assert extracted_whitespace is not None
        if stack_index <= 0:
            POGGER.debug("PLFCB>>No Started lists")
            assert not current_container_blocks
            if foobar is None:
                POGGER.debug("PLFCB>>No Started Block Quote")
            else:
                POGGER.debug("PLFCB>>Started Block Quote")
                adj_ws = extracted_whitespace[foobar:]
        else:
            assert current_container_blocks
            POGGER.debug(
                "PLFCB>>Started list-last stack>>$",
                parser_state.token_stack,
            )
            POGGER.debug(
                "PLFCB>>Started list-last stack>>$",
                parser_state.token_stack[stack_index],
            )
            token_index = len(parser_state.token_document) - 1

            found_block_quote_token: Optional[BlockQuoteMarkdownToken] = None
            while token_index >= 0 and not (
                parser_state.token_document[token_index].is_any_list_token
            ):
                if (
                    not found_block_quote_token
                    and parser_state.token_document[token_index].is_block_quote_start
                ):
                    found_block_quote_token = cast(
                        BlockQuoteMarkdownToken,
                        parser_state.token_document[token_index],
                    )
                token_index -= 1
            POGGER.debug(
                "PLFCB>>Started list-last token>>$",
                parser_state.token_document[token_index],
            )
            POGGER.debug_with_visible_whitespace(
                "PLFCB>>found_block_quote_token>>$",
                found_block_quote_token,
            )
            if found_block_quote_token:
                POGGER.debug(
                    "PLFCB>>leading_text_index>>$",
                    found_block_quote_token.leading_text_index,
                )
            assert token_index >= 0

            POGGER.debug(f"caw>adj_ws>:{adj_ws}:")
            adj_ws = ContainerBlockProcessor.__calculate_adjusted_whitespace_kludge(
                parser_state,
                token_index,
                extracted_whitespace,
                previous_ws_len,
                found_block_quote_token,
                line_to_parse,
                adj_ws,
                container_depth,
            )
            POGGER.debug(f"caw>adj_ws>:{adj_ws}:")

        POGGER.debug(f"cfcs>extracted_whitespace>:{extracted_whitespace}:")
        POGGER.debug(f"cfcs>adj_ws>:{adj_ws}:")
        return adj_ws

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_nested_container_blocks(
        parser_state: ParserState,
        container_depth: int,
        block_quote_data: BlockQuoteData,
        position_marker: PositionMarker,
        parser_properties: ParseBlockPassProperties,
        end_container_indices: ContainerIndices,
        leaf_tokens: List[MarkdownToken],
        container_level_tokens: List[MarkdownToken],
        was_container_start: bool,
        avoid_block_starts: bool,
        start_index: int,
        removed_chars_at_start: int,
        text_removed_by_container: Optional[str],
    ) -> Tuple[
        str,
        List[MarkdownToken],
        List[MarkdownToken],
        BlockQuoteData,
        bool,
        Optional[str],
        bool,
        bool,
    ]:
        """
        Handle the processing of nested container blocks, as they can contain
        themselves and get somewhat messy.
        """
        did_process_blank_line, adjusted_text_to_parse = (
            False,
            position_marker.text_to_parse,
        )

        POGGER.debug("adjusted_text_to_parse>$<", adjusted_text_to_parse)
        POGGER.debug("index_number>$<", position_marker.index_number)
        POGGER.debug("index_indent>$<", position_marker.index_indent)
        POGGER.debug("start_index>$<", start_index)
        POGGER.debug("parser_state.nested_list_start>$", parser_state.nested_list_start)
        POGGER.debug("was_container_start>$", was_container_start)

        if was_container_start and position_marker.text_to_parse:
            assert container_depth < 10
            nested_container_starts = (
                ContainerBlockProcessor.__get_nested_container_starts(
                    parser_state,
                    position_marker.text_to_parse,
                    end_container_indices,
                    avoid_block_starts,
                    start_index,
                    removed_chars_at_start,
                    text_removed_by_container,
                )
            )
            POGGER.debug(
                "__handle_nested_container_blocks>nested_container_starts>>:$:<<",
                nested_container_starts,
            )
            POGGER.debug("check next container_start>leaf_tokens>>$", leaf_tokens)
            POGGER.debug(
                "check next container_start>container_level_tokens>>$",
                container_level_tokens,
            )

            adj_line_to_parse = position_marker.text_to_parse
            POGGER.debug("check next container_start>pre>>$<<", adj_line_to_parse)

            (
                start_index,
                indent_level_delta,
                adj_line_to_parse,
                already_adjusted,
                active_container_index,
            ) = ContainerBlockProcessor.__check_for_nested_list_start(
                parser_state,
                end_container_indices,
                nested_container_starts,
                adj_line_to_parse,
                block_quote_data,
                start_index,
            )
            # POGGER.debug_with_visible_whitespace("line_to_parse>>$>>", adj_line_to_parse)

            assert not leaf_tokens
            (
                adj_line_to_parse,
                adjusted_text_to_parse,
            ) = ContainerBlockProcessor.__do_nested_cleanup(
                parser_state,
                block_quote_data,
                indent_level_delta,
                already_adjusted,
                adj_line_to_parse,
                container_level_tokens,
                active_container_index,
                adjusted_text_to_parse,
            )
            container_level_tokens = []
            # POGGER.debug_with_visible_whitespace("adj_line_to_parse>>$>>", adj_line_to_parse)
            # POGGER.debug_with_visible_whitespace("adjusted_text_to_parse>>$>>", adjusted_text_to_parse)

            (
                did_process_blank_line,
                block_quote_data,
                adjusted_text_to_parse,
                nested_removed_text,
                was_indent_text_added,
                force_list_continuation,
            ) = ContainerBlockProcessor.__check_for_next_container(
                parser_state,
                nested_container_starts,
                block_quote_data,
                adjusted_text_to_parse,
                adj_line_to_parse,
                end_container_indices,
                position_marker,
                container_depth,
                parser_properties,
            )
        else:
            nested_removed_text, was_indent_text_added, force_list_continuation = (
                None,
                False,
                False,
            )

        # POGGER.debug_with_visible_whitespace("adjusted_text_to_parse>>$>>", adjusted_text_to_parse)
        return (
            adjusted_text_to_parse,
            leaf_tokens,
            container_level_tokens,
            block_quote_data,
            did_process_blank_line,
            nested_removed_text,
            was_indent_text_added,
            force_list_continuation,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __check_for_nested_list_start(
        parser_state: ParserState,
        end_container_indices: ContainerIndices,
        nested_container_starts: ContainerIndices,
        adj_line_to_parse: str,
        block_quote_data: BlockQuoteData,
        start_index: int,
    ) -> Tuple[int, int, str, bool, int]:

        active_container_index = max(
            end_container_indices.ulist_index,
            end_container_indices.olist_index,
            end_container_indices.block_index,
        )
        POGGER.debug(
            "check next container_start>max>>$>>bq>>$",
            active_container_index,
            end_container_indices.block_index,
        )
        indent_level_delta, already_adjusted = 0, False
        if (
            end_container_indices.block_index != -1
            and not nested_container_starts.ulist_index
            and not nested_container_starts.olist_index
        ):
            assert active_container_index == end_container_indices.block_index
            POGGER.debug(
                "parser_state.nested_list_start>>$<<",
                parser_state.nested_list_start,
            )
            POGGER.debug("adj_line_to_parse>>$<<", adj_line_to_parse)
            POGGER.debug(
                "parser_state.token_document>>$<<", parser_state.token_document
            )
            if parser_state.nested_list_start and adj_line_to_parse.strip():

                # POGGER.debug_with_visible_whitespace("line_to_parse>>$>>", adj_line_to_parse)
                (
                    start_index,
                    indent_level,
                    indent_was_adjusted,
                    indent_level_delta,
                ) = ContainerBlockProcessor.__calculate_initial_list_adjustments(
                    parser_state, adj_line_to_parse, end_container_indices
                )
                # POGGER.debug_with_visible_whitespace("line_to_parse>>$>>", adj_line_to_parse)
                (
                    adj_line_to_parse,
                    already_adjusted,
                ) = ContainerBlockProcessor.__adjust_line_2(
                    parser_state,
                    end_container_indices,
                    start_index,
                    indent_level,
                    nested_container_starts,
                    adj_line_to_parse,
                    indent_was_adjusted,
                    block_quote_data,
                )
                # POGGER.debug_with_visible_whitespace("line_to_parse>>$>>", adj_line_to_parse)
        return (
            start_index,
            indent_level_delta,
            adj_line_to_parse,
            already_adjusted,
            active_container_index,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __calculate_initial_list_adjustments(
        parser_state: ParserState,
        adj_line_to_parse: str,
        end_container_indices: ContainerIndices,
    ) -> Tuple[int, int, bool, int]:

        start_index, _ = ParserHelper.extract_whitespace(adj_line_to_parse, 0)
        assert start_index is not None
        POGGER.debug(
            "end_container_indices.block_index>>$<<",
            end_container_indices.block_index,
        )
        POGGER.debug("start_index>>$<<", start_index)

        assert parser_state.nested_list_start is not None
        assert parser_state.nested_list_start.matching_markdown_token is not None
        POGGER.debug(
            "parser_state.nested_list_start.matching_markdown_token>>$<<",
            parser_state.nested_list_start.matching_markdown_token,
        )
        list_start_token_index = parser_state.token_document.index(
            parser_state.nested_list_start.matching_markdown_token
        )
        POGGER.debug(
            "list_start_token_index>>$<<",
            list_start_token_index,
        )
        if list_start_token_index < (len(parser_state.token_document) - 1):
            token_after_list_start = parser_state.token_document[
                list_start_token_index + 1
            ]
            POGGER.debug(
                "token_after_list_start>>$<<",
                token_after_list_start,
            )
            assert (
                parser_state.nested_list_start.matching_markdown_token.line_number
                == token_after_list_start.line_number
            )
            column_number_delta = (
                token_after_list_start.column_number
                - parser_state.nested_list_start.matching_markdown_token.column_number
            )
        else:
            column_number_delta = 0
        POGGER.debug(
            "column_number_delta>>$<<",
            column_number_delta,
        )
        indent_level_delta, indent_level, adjusted_indent_level = (
            0,
            parser_state.nested_list_start.indent_level,
            column_number_delta + end_container_indices.block_index,
        )
        POGGER.debug(
            "adjusted_indent_level>>$<<  indent_level>$",
            adjusted_indent_level,
            indent_level,
        )
        indent_was_adjusted = indent_level != adjusted_indent_level
        if indent_level > adjusted_indent_level:
            indent_level_delta = indent_level - adjusted_indent_level
        indent_level = column_number_delta + end_container_indices.block_index

        return start_index, indent_level, indent_was_adjusted, indent_level_delta

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_line_2(
        parser_state: ParserState,
        end_container_indices: ContainerIndices,
        start_index: int,
        indent_level: int,
        nested_container_starts: ContainerIndices,
        adj_line_to_parse: str,
        indent_was_adjusted: bool,
        block_quote_data: BlockQuoteData,
    ) -> Tuple[str, bool]:
        already_adjusted = False
        # POGGER.debug_with_visible_whitespace("line_to_parse>>$>>", adj_line_to_parse)
        if (
            parser_state.token_document[-1].is_blank_line
            and (end_container_indices.block_index + start_index) < indent_level
        ):
            POGGER.debug("\n\nBOOM\n\n")

            y_tokens = []
            while parser_state.token_document[-1].is_blank_line:
                y_tokens.append(parser_state.token_document[-1])
                del parser_state.token_document[-1]

            x_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                include_lists=True,
            )
            parser_state.token_document.extend(x_tokens)
            parser_state.token_document.extend(y_tokens)
        elif (
            not nested_container_starts.block_index
            and adj_line_to_parse
            and adj_line_to_parse[0] == " "
            and indent_was_adjusted
            and parser_state.nested_list_start
        ):

            assert parser_state.nested_list_start is not None
            POGGER.debug("adj_line_to_parse>:$:<", adj_line_to_parse)
            # POGGER.debug(
            #     "parser_state.nested_list_start>:$:<",
            #     parser_state.nested_list_start.matching_markdown_token.extracted_whitespace,
            # )

            POGGER.debug(
                "block_quote_data.current_count:$, block_quote_data.stack_count:$",
                block_quote_data.current_count,
                block_quote_data.stack_count,
            )

            POGGER.debug("adj_line_to_parse>:$:<", adj_line_to_parse)
        return adj_line_to_parse, already_adjusted

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __do_nested_cleanup(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        delta: int,
        already_adjusted: bool,
        adj_line_to_parse: str,
        container_level_tokens: List[MarkdownToken],
        active_container_index: int,
        adjusted_text_to_parse: str,
    ) -> Tuple[str, str]:
        POGGER.debug(
            "check next container_start>mid>>block_quote_data.stack_count>>$<<block_quote_data.current_count<<$",
            block_quote_data.stack_count,
            block_quote_data.current_count,
        )
        if delta or already_adjusted:
            POGGER.debug(
                "check next container_start>already adjusted<<$<<",
                adj_line_to_parse,
            )
            adjusted_text_to_parse = adj_line_to_parse
        else:
            POGGER.debug("check next container_start>post<<$<<", adj_line_to_parse)
            POGGER.debug("active_container_index<<$<<", active_container_index)
            adjustment_filler = ParserHelper.repeat_string(
                ParserHelper.space_character, active_container_index
            )
            adj_line_to_parse = f"{adjustment_filler}{adj_line_to_parse}"
            POGGER.debug("check next container_start>post<<$<<", adj_line_to_parse)

        parser_state.token_document.extend(container_level_tokens)
        return adj_line_to_parse, adjusted_text_to_parse

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __check_for_next_container(
        parser_state: ParserState,
        nested_container_starts: ContainerIndices,
        block_quote_data: BlockQuoteData,
        adjusted_text_to_parse: str,
        adj_line_to_parse: str,
        end_container_indices: ContainerIndices,
        position_marker: PositionMarker,
        container_depth: int,
        parser_properties: ParseBlockPassProperties,
    ) -> Tuple[bool, BlockQuoteData, str, Optional[str], bool, bool]:

        POGGER.debug("check next container_start>stack>>$", parser_state.token_stack)
        POGGER.debug(
            "check next container_start>tokenized_document>>$",
            parser_state.token_document,
        )

        if (
            nested_container_starts.ulist_index
            or nested_container_starts.olist_index
            or nested_container_starts.block_index
        ):
            POGGER.debug(
                "check next container_start>nested_container",
            )
            (
                adjusted_text_to_parse,
                block_quote_data,
                did_process_blank_line,
                nested_removed_text,
                was_indent_text_added,
                force_list_continuation,
            ) = ContainerBlockProcessor.__look_for_container_blocks(
                parser_state,
                adj_line_to_parse,
                end_container_indices.block_index,
                container_depth,
                block_quote_data,
                position_marker,
                parser_properties,
            )
        else:
            (
                did_process_blank_line,
                nested_removed_text,
                was_indent_text_added,
                force_list_continuation,
            ) = (False, None, False, False)
        parser_state.set_no_para_start_if_empty()

        return (
            did_process_blank_line,
            block_quote_data,
            adjusted_text_to_parse,
            nested_removed_text,
            was_indent_text_added,
            force_list_continuation,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __get_nested_container_starts(
        parser_state: ParserState,
        line_to_parse: str,
        end_container_indices: ContainerIndices,
        avoid_block_starts: bool,
        start_index: int,
        removed_chars_at_start: int,
        text_removed_by_container: Optional[str],
    ) -> ContainerIndices:
        POGGER.debug(
            "__handle_nested_container_blocks>stack>>:$:<<",
            line_to_parse,
        )
        POGGER.debug(
            "__handle_nested_container_blocks>end_container_indices>>:$:<<",
            end_container_indices,
        )

        POGGER.debug("check next container_start>")
        POGGER.debug("check next container_start>start_index>$", start_index)
        POGGER.debug(
            "check next container_start>removed_chars_at_start:$:",
            removed_chars_at_start,
        )
        POGGER.debug(
            "check next container_start>text_removed_by_container:$:",
            text_removed_by_container,
        )
        POGGER.debug("check next container_start>stack>>$", parser_state.token_stack)

        _, ex_ws_test = ParserHelper.extract_whitespace(line_to_parse, 0)
        assert ex_ws_test is not None

        whitespace_scan_start_index = 0
        for token_stack_item in parser_state.token_stack:
            if token_stack_item.is_list:
                list_stack_token = cast(ListStackToken, token_stack_item)
                if list_stack_token.ws_before_marker <= len(ex_ws_test):
                    whitespace_scan_start_index = list_stack_token.ws_before_marker

        after_ws_index, ex_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, whitespace_scan_start_index
        )
        if not ex_whitespace:
            ex_whitespace = ""
            after_ws_index = whitespace_scan_start_index

        assert after_ws_index is not None

        nested_ulist_start, _, _, _ = ListBlockProcessor.is_ulist_start(
            parser_state, line_to_parse, after_ws_index, ex_whitespace, False
        )
        nested_olist_start, _, _, _ = ListBlockProcessor.is_olist_start(
            parser_state, line_to_parse, after_ws_index, ex_whitespace, False
        )
        nested_block_start = (
            False
            if avoid_block_starts
            else BlockQuoteProcessor.is_block_quote_start(
                line_to_parse, after_ws_index, ex_whitespace
            )
        )
        POGGER.debug(
            "check next container_start>ulist>$>index>$",
            nested_ulist_start,
            end_container_indices.ulist_index,
        )
        POGGER.debug(
            "check next container_start>olist>$>index>$",
            nested_olist_start,
            end_container_indices.olist_index,
        )
        POGGER.debug(
            "check next container_start>bquote>$>index>$",
            nested_block_start,
            end_container_indices.block_index,
        )

        POGGER.debug(
            "__handle_nested_container_blocks>end_container_indices>>:$:<<",
            end_container_indices,
        )

        POGGER.debug("check next container_start>stack>>$", parser_state.token_stack)

        return ContainerIndices(
            nested_ulist_start, nested_olist_start, nested_block_start
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __calculate_nested_removed_text(
        parser_state: ParserState, previous_document_length: int
    ) -> Optional[str]:
        nested_removed_text = None
        POGGER.debug("__calculate_nested_removed_text")
        if previous_document_length != len(parser_state.token_document):
            POGGER.debug(
                "\ncheck next container_start>added tokens:$:",
                parser_state.token_document[previous_document_length:],
            )
            if parser_state.token_document[-1].is_block_quote_start:
                block_quote_token = cast(
                    BlockQuoteMarkdownToken, parser_state.token_document[-1]
                )
                assert block_quote_token.leading_spaces is not None
                split_spaces = block_quote_token.leading_spaces.split(
                    ParserHelper.newline_character
                )
                nested_removed_text = str(split_spaces[-1])
        if not nested_removed_text:
            last_container_index = parser_state.find_last_container_on_stack()
            if (
                last_container_index > 0
                and parser_state.token_stack[last_container_index].is_block_quote
            ):
                block_quote_token = cast(
                    BlockQuoteMarkdownToken,
                    parser_state.token_stack[
                        last_container_index
                    ].matching_markdown_token,
                )
                assert block_quote_token.leading_spaces is not None
                split_spaces = block_quote_token.leading_spaces.split(
                    ParserHelper.newline_character
                )
                nested_removed_text = str(split_spaces[-1])
        POGGER.debug("__calculate_nested_removed_text<<:$:", nested_removed_text)
        return nested_removed_text

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __look_for_container_blocks(
        parser_state: ParserState,
        adj_line_to_parse: str,
        end_of_bquote_start_index: int,
        container_depth: int,
        block_quote_data: BlockQuoteData,
        position_marker: PositionMarker,
        parser_properties: ParseBlockPassProperties,
    ) -> Tuple[str, BlockQuoteData, bool, Optional[str], bool, bool]:

        """
        Look for container blocks that we can use.
        """
        POGGER.debug("check next container_start>recursing")
        POGGER.debug("check next container_start>>$\n", adj_line_to_parse)
        POGGER.debug("block_quote_data.current_count>$", block_quote_data.current_count)
        adj_block, position_marker = (
            None if end_of_bquote_start_index == -1 else end_of_bquote_start_index,
            PositionMarker(position_marker.line_number, -1, adj_line_to_parse),
        )
        # index_indent= start_index (passed down)
        new_container_depth = container_depth + 1
        # if new_container_depth < len(parser_state.token_stack) - 1:
        #     POGGER.debug("parser_state.token_document>$", parser_state.token_stack[new_container_depth + 1])
        #     if parser_state.token_stack[new_container_depth + 1].is_list:
        #         POGGER.debug("list")
        #         df = position_marker.index_indent
        #         _, ex_ws = ParserHelper.extract_whitespace(adj_line_to_parse, 0)
        #         dg = len(ex_ws)
        #         dh = parser_state.token_stack[new_container_depth + 1].indent_level
        #         delta = dh - df
        #         POGGER.debug("list-delta:$ >= dg:$", delta, dg)
        #         if delta > 0 and dg >= delta:
        #             POGGER.debug("eligible")
        #             new_container_depth += 1
        #             position_marker = PositionMarker(position_marker.line_number, -1,
        #               adj_line_to_parse[delta:], index_indent=xx+delta)
        #     POGGER.debug("position_marker[$,$]->:$:", position_marker.index_indent,
        # position_marker.index_number, position_marker.text_to_parse)

        POGGER.debug("\n\nRECURSING\n")
        # POGGER.debug("parser_state.token_document>$", parser_state.token_document)
        previous_document_length = len(parser_state.token_document)
        (
            produced_inner_tokens,
            line_to_parse,
            current_bq_count_increment,
            requeue_line_info,
            did_process_blank_line,
            force_list_continuation,
        ) = ContainerBlockProcessor.parse_line_for_container_blocks(
            parser_state,
            position_marker,
            False,
            parser_properties,
            block_quote_data.current_count,
            container_depth=new_container_depth,
            foobar=adj_block,
            init_bq=block_quote_data.current_count,
        )
        assert not requeue_line_info or not requeue_line_info.lines_to_requeue
        assert line_to_parse is not None

        POGGER.debug("\nRECURSED\n\n")

        # POGGER.debug("previous_document_length=$", previous_document_length)
        nested_removed_text = ContainerBlockProcessor.__calculate_nested_removed_text(
            parser_state, previous_document_length
        )
        POGGER.debug("check next container_start>stack>>$", parser_state.token_stack)
        POGGER.debug(
            "check next container_start>tokenized_document>>$",
            parser_state.token_document,
        )
        POGGER.debug("check next container_start>line_parse>>$", line_to_parse)
        if current_bq_count_increment:
            # POGGER.debug(
            #     "block_quote_data.current_count>$", block_quote_data.current_count
            # )
            block_quote_data = BlockQuoteData(
                block_quote_data.current_count + current_bq_count_increment,
                parser_state.count_of_block_quotes_on_stack(),
            )
            # POGGER.debug(
            #     "block_quote_data.current_count>$", block_quote_data.current_count
            # )

        POGGER.debug("produced_inner_tokens=$", produced_inner_tokens)
        was_indent_text_added = bool(
            parser_state.token_stack[-1].is_indented_code_block
            and produced_inner_tokens
            and len(produced_inner_tokens) == 1
            and produced_inner_tokens[0].is_text
        )
        POGGER.debug("was_indent_text_added=$", was_indent_text_added)

        # POGGER.debug("parser_state.token_document>$", parser_state.token_document)
        parser_state.token_document.extend(produced_inner_tokens)
        POGGER.debug("parser_state.token_document>$", parser_state.token_document)
        # POGGER.debug("did_process_blank_line>$", did_process_blank_line)

        return (
            line_to_parse,
            block_quote_data,
            did_process_blank_line,
            nested_removed_text,
            was_indent_text_added,
            force_list_continuation,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __process_list_in_progress(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        container_level_tokens: List[MarkdownToken],
        extracted_whitespace: Optional[str],
    ) -> Tuple[
        bool, str, List[MarkdownToken], Optional[str], Optional[RequeueLineInfo], bool
    ]:

        did_process, ind = LeafBlockProcessor.check_for_list_in_process(parser_state)
        if did_process:
            assert not container_level_tokens
            POGGER.debug("clt>>list-in-progress")
            POGGER.debug("clt>>line_to_parse>>:$:>>", line_to_parse)
            (
                container_level_tokens,
                line_to_parse,
                used_indent,
                requeue_line_info,
                was_paragraph_continuation,
            ) = ListBlockProcessor.list_in_process(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                ind,
            )
            POGGER.debug(
                "clt>>was_paragraph_continuation>>:$:>>", was_paragraph_continuation
            )
            POGGER.debug("clt>>line_to_parse>>:$:>>", line_to_parse)
            POGGER.debug("clt>>used_indent>>:$:>>", used_indent)
            POGGER.debug("clt>>requeue_line_info>>:$:>>", requeue_line_info)
        else:
            used_indent, requeue_line_info, was_paragraph_continuation = (
                None,
                None,
                False,
            )

        return (
            did_process,
            line_to_parse,
            container_level_tokens,
            used_indent,
            requeue_line_info,
            was_paragraph_continuation,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_lazy_lines(
        parser_state: ParserState,
        position_marker: PositionMarker,
        leaf_tokens: List[MarkdownToken],
        block_quote_data: BlockQuoteData,
        line_to_parse: str,
        container_level_tokens: List[MarkdownToken],
        container_start_bq_count: int,
        was_paragraph_continuation: bool,
    ) -> Tuple[BlockQuoteData, bool]:

        POGGER.debug("LINE-lazy>$", line_to_parse)
        assert not leaf_tokens
        POGGER.debug("clt>>lazy-check")

        POGGER.debug("__process_lazy_lines>>ltp>$", line_to_parse)
        after_ws_index, ex_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, 0
        )
        remaining_line = line_to_parse[after_ws_index:]
        POGGER.debug("container_start_bq_count>>:$", container_start_bq_count)
        POGGER.debug(
            "__process_lazy_lines>>block_quote_data.current_count>$<",
            block_quote_data.current_count,
        )
        POGGER.debug(
            "__process_lazy_lines>>block_quote_data.stack_count>$<",
            block_quote_data.stack_count,
        )
        POGGER.debug("__process_lazy_lines>>mod->ltp>$<", remaining_line)
        POGGER.debug("__process_lazy_lines>>mod->ews>$<", ex_whitespace)

        (
            lazy_tokens,
            block_quote_data,
            was_paragraph_continuation,
        ) = BlockQuoteProcessor.check_for_lazy_handling(
            parser_state,
            position_marker,
            block_quote_data,
            remaining_line,
            ex_whitespace,
            was_paragraph_continuation,
        )
        # POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)

        container_level_tokens.extend(lazy_tokens)
        return block_quote_data, was_paragraph_continuation

    # pylint: enable=too-many-arguments

    @staticmethod
    def __adjust_for_inner_list_container(
        parser_state: ParserState,
        last_block_index: int,
        last_list_index: int,
        current_line_number: int,
    ) -> None:
        POGGER.debug("??? adjust_for_inner_list_container")
        if last_block_index > 0 and 0 < last_list_index < last_block_index:
            POGGER.debug("yes adjust_for_inner_list_container")
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[last_list_index].matching_markdown_token,
            )
            if list_token.line_number != current_line_number:
                POGGER.debug("plt-a>>last_block_token>>$", list_token)
                list_token.add_leading_spaces("")
                POGGER.debug(
                    "plt-a>>last_block_token>>$",
                    list_token,
                )
        else:
            POGGER.debug("not adjust_for_inner_list_container")

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
            )
            found_list_token = parser_state.token_document[document_index]
        return found_list_token

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_for_list_container(
        parser_state: ParserState,
        last_block_index: int,
        last_list_index: int,
        text_removed_by_container: str,
        extracted_whitespace: Optional[str],
        xposition_marker: PositionMarker,
        indent_already_processed: bool,
        container_depth: int,
    ) -> Tuple[Optional[str], Optional[str]]:
        POGGER.debug("??? adjust_for_list_container")
        removed_leading_space = None
        actual_removed_leading_space = None
        assert extracted_whitespace is not None
        # pylint: disable=chained-comparison
        if (
            not indent_already_processed
            and last_block_index > 0
            and last_list_index > 0
            and last_list_index > last_block_index
        ):
            # pylint: enable=chained-comparison
            POGGER.debug("yes adjust_for_list_container")
            found_list_token = ContainerBlockProcessor.__adjust_for_list_container_find(
                parser_state, xposition_marker
            )
            # POGGER.debug("line_number>>:$:<", xposition_marker.line_number)
            # POGGER.debug("column_number>>:$:<", xposition_marker.index_number)
            # POGGER.debug("found_list_token>>:$:<", found_list_token)

            if not found_list_token:
                list_token = cast(
                    ListStartMarkdownToken,
                    parser_state.token_stack[last_list_index].matching_markdown_token,
                )
                calc_indent_level = list_token.indent_level
                if text_removed_by_container:
                    calc_indent_level -= len(text_removed_by_container)
                # POGGER.debug("calc_indent_level>>:$:<", calc_indent_level)
                # POGGER.debug("extracted_whitespace>>:$:<", extracted_whitespace)
                if len(extracted_whitespace) > calc_indent_level:
                    extracted_whitespace = extracted_whitespace[:calc_indent_level]
                    # POGGER.debug("extracted_whitespace>>:$:<", extracted_whitespace)
                # POGGER.debug(
                #     "parser_state.token_document>>$", parser_state.token_document
                # )

                # POGGER.debug(
                #     "plt-b>>last_block_token>>$",
                #     parser_state.token_stack[last_list_index].matching_markdown_token,
                # )
                list_token.add_leading_spaces(extracted_whitespace)
                actual_removed_leading_space = extracted_whitespace

                # POGGER.debug(
                #     "xposition_marker($:$)>>$",
                #     xposition_marker.index_number,
                #     xposition_marker.index_indent,
                #     xposition_marker.text_to_parse,
                # )
                # POGGER.debug("orig:$:", parser_state.original_line_to_parse)

                if not container_depth and not xposition_marker.index_indent:
                    removed_leading_space = extracted_whitespace
                # POGGER.debug(
                #     "plt-b>>last_block_token>>$",
                #     parser_state.token_stack[last_list_index].matching_markdown_token,
                # )
                # POGGER.debug(
                #     "parser_state.token_document>>$", parser_state.token_document
                # )
        else:
            POGGER.debug("not adjust_for_list_container")
        # POGGER.debug("removed_leading_space:$:", removed_leading_space)
        return removed_leading_space, actual_removed_leading_space

    # pylint: enable=too-many-arguments

    @staticmethod
    def __post_leaf_block_adjustment(
        parser_state: ParserState,
        text_removed_by_container: str,
        orig_text_removed_by_container: str,
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

        POGGER.debug("text_removed_by_container>>:$:", text_removed_by_container)
        POGGER.debug(
            "orig_text_removed_by_container>>:$:", orig_text_removed_by_container
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
            last_block_token.add_leading_spaces("")
            last_block_token.leading_text_index += 1
            POGGER.debug("plt-c>>last_block_token>>$", last_block_token)
            POGGER.debug(
                "plt-c>>leading_text_index>>$", last_block_token.leading_text_index
            )

    @staticmethod
    def __calculate_current_indent_level_list(
        parser_state: ParserState, stack_index: int
    ) -> int:
        stack_token = cast(ListStackToken, parser_state.token_stack[stack_index])
        if stack_token.last_new_list_token:
            return stack_token.last_new_list_token.indent_level
        list_token = cast(ListStartMarkdownToken, stack_token.matching_markdown_token)
        return list_token.indent_level

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_current_indent_level_block_quote(
        parser_state: ParserState,
        stack_index: int,
        non_last_block_index: int,
        last_block_index: int,
        line_number: int,
        current_indent_level: int,
        text_removed_by_container: str,
    ) -> Tuple[Optional[int], int]:
        if stack_index != last_block_index:
            POGGER.debug("not last bq token, skipping")
            non_last_block_index = stack_index
            return None, non_last_block_index

        matching_token = parser_state.token_stack[stack_index].matching_markdown_token
        assert matching_token is not None
        POGGER.debug("line_number=$", line_number)
        POGGER.debug(
            "matching_markdown_token.line_number=$", matching_token.line_number
        )
        POGGER.debug("non_last_block_index=$", non_last_block_index)

        valid_mark = non_last_block_index and non_last_block_index != (
            last_block_index - 1
        )
        base_indent_level = (
            current_indent_level
            if valid_mark and line_number == matching_token.line_number
            else 0
        )
        proposed_indent_level = (
            len(text_removed_by_container) if text_removed_by_container else 0
        ) + base_indent_level
        POGGER.debug("last bq token, processing:$", proposed_indent_level)
        return proposed_indent_level, non_last_block_index

    # pylint: enable=too-many-arguments

    @staticmethod
    def __calculate_current_indent_level(
        parser_state: ParserState,
        last_block_index: int,
        text_removed_by_container: str,
        total_ws: int,
        line_number: int,
    ) -> int:
        current_indent_level = 0
        non_last_block_index = 0
        POGGER.debug_with_visible_whitespace("token-stack:$:", parser_state.token_stack)
        for stack_index in range(1, len(parser_state.token_stack)):
            proposed_indent_level = 0
            POGGER.debug_with_visible_whitespace(
                "token:$:", parser_state.token_stack[stack_index]
            )
            if parser_state.token_stack[stack_index].is_block_quote:
                (
                    new_indent_level,
                    non_last_block_index,
                ) = ContainerBlockProcessor.__calculate_current_indent_level_block_quote(
                    parser_state,
                    stack_index,
                    non_last_block_index,
                    last_block_index,
                    line_number,
                    current_indent_level,
                    text_removed_by_container,
                )
                if new_indent_level is None:
                    continue
                proposed_indent_level = new_indent_level
            elif parser_state.token_stack[stack_index].is_list:
                proposed_indent_level = (
                    ContainerBlockProcessor.__calculate_current_indent_level_list(
                        parser_state, stack_index
                    )
                )
            else:
                break
            POGGER.debug(
                "proposed_indent_level:$ <= total_ws:$<",
                proposed_indent_level,
                total_ws,
            )
            if proposed_indent_level > total_ws:
                break
            current_indent_level = proposed_indent_level
            POGGER.debug("current_indent_level:$", current_indent_level)
        POGGER.debug("<<current_indent_level:$", current_indent_level)
        return current_indent_level

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_containers_before_leaf_blocks(
        parser_state: ParserState,
        xposition_marker: PositionMarker,
        was_paragraph_continuation: bool,
        last_block_index: int,
        text_removed_by_container: str,
        total_ws: int,
        indent_already_processed: bool,
        force_list_continuation: bool,
        actual_removed_leading_space: Optional[str],
    ) -> Tuple[PositionMarker, str]:

        POGGER.debug("??? adjust_containers_before_leaf_blocks")
        if (
            xposition_marker.text_to_parse
            and not was_paragraph_continuation
            and not indent_already_processed
        ):
            POGGER.debug("force_list_continuation = $", force_list_continuation)
            if force_list_continuation:
                POGGER.debug(
                    "xposition_marker.text_to_parse=$", xposition_marker.text_to_parse
                )
                POGGER.debug(
                    "xposition_marker.index_number=$", xposition_marker.index_number
                )
                POGGER.debug("text_removed_by_container=$=", text_removed_by_container)
                POGGER.debug(
                    "actual_removed_leading_space=$=", actual_removed_leading_space
                )
                if not actual_removed_leading_space:
                    actual_removed_leading_space = ""
                assert xposition_marker.text_to_parse.startswith(
                    actual_removed_leading_space
                )
                position_marker = PositionMarker(
                    xposition_marker.line_number,
                    0,
                    xposition_marker.text_to_parse[len(actual_removed_leading_space) :],
                    xposition_marker.index_indent,
                )
                return position_marker, text_removed_by_container

            POGGER.debug("yes adjust_containers_before_leaf_blocks")
            current_indent_level = (
                ContainerBlockProcessor.__calculate_current_indent_level(
                    parser_state,
                    last_block_index,
                    text_removed_by_container,
                    total_ws,
                    xposition_marker.line_number,
                )
            )

            # POGGER.debug("total_ws>>:$:<", total_ws)
            # POGGER.debug("current_indent_level>>:$:<", current_indent_level)
            current_indent_level -= xposition_marker.index_indent
            # total_ws -= xposition_marker.index_indent
            # POGGER.debug("total_ws>>:$:<", total_ws)
            # POGGER.debug("current_indent_level>>:$:<", current_indent_level)

            assert current_indent_level >= 0
            prefix_text = xposition_marker.text_to_parse[:current_indent_level]
            new_text_to_parse = xposition_marker.text_to_parse[current_indent_level:]
            new_index_indent = xposition_marker.index_indent + current_indent_level

            # POGGER.debug(
            #     "original_line_to_parse>>:$:<", parser_state.original_line_to_parse
            # )
            assert parser_state.original_line_to_parse is not None
            if len(parser_state.original_line_to_parse) == len(new_text_to_parse):
                assert parser_state.original_line_to_parse.replace(
                    ">", " "
                ) == new_text_to_parse.replace(">", " "), (
                    "cheat=:"
                    + ParserHelper.make_value_visible(
                        parser_state.original_line_to_parse
                    )
                    + ":,new_text_to_parse=:"
                    + ParserHelper.make_value_visible(new_text_to_parse)
                    + ":"
                )
            else:
                is_valid = parser_state.original_line_to_parse.endswith(
                    new_text_to_parse
                )
                # if not is_valid and new_text_to_parse[0] == " ":
                #     new_parse = ">" + new_text_to_parse[1:]
                #     is_valid = parser_state.original_line_to_parse.endswith(new_parse)
                assert is_valid, (
                    "cheat=:"
                    + ParserHelper.make_value_visible(
                        parser_state.original_line_to_parse
                    )
                    + ":,new_text_to_parse=:"
                    + ParserHelper.make_value_visible(new_text_to_parse)
                    + ":"
                )
            new_index_indent = len(parser_state.original_line_to_parse) - len(
                new_text_to_parse
            )

            POGGER.debug("new_text_to_parse>>:$:<", new_text_to_parse)
            POGGER.debug("new_index_indent>>:$:<", new_index_indent)
            text_removed_by_container = (
                text_removed_by_container + prefix_text
                if text_removed_by_container
                else prefix_text
            )
        else:
            POGGER.debug("not adjust_containers_before_leaf_blocks")
            new_text_to_parse = xposition_marker.text_to_parse
            new_index_indent = xposition_marker.index_indent

        # POGGER.debug("parser_state.token_document>>$", parser_state.token_document)
        position_marker = PositionMarker(
            xposition_marker.line_number,
            0,
            new_text_to_parse,
            new_index_indent,
        )
        return position_marker, text_removed_by_container

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_special_block_quote_reduction(
        parser_state: ParserState,
        block_quote_data: BlockQuoteData,
        last_block_index: int,
        last_list_index: int,
        was_paragraph_continuation: bool,
    ) -> Tuple[List[MarkdownToken], Optional[RequeueLineInfo]]:
        real_stack_count = parser_state.count_of_block_quotes_on_stack()
        POGGER.debug("current_count>>:$:<", block_quote_data.current_count)
        POGGER.debug(
            "stack_count>>:$:($)<", block_quote_data.stack_count, real_stack_count
        )
        POGGER.debug("??? special_block_quote_reduction")
        if (
            block_quote_data.current_count < real_stack_count
            and not was_paragraph_continuation
            and last_block_index > last_list_index
            and not last_list_index
        ):
            POGGER.debug("yes special_block_quote_reduction")
            stack_delta = block_quote_data.stack_count - block_quote_data.current_count
            close_tokens, requeue_line_info = parser_state.close_open_blocks_fn(
                parser_state,
                include_block_quotes=True,
                was_forced=True,
                requeue_reset=True,
                caller_can_handle_requeue=True,
                until_this_index=len(parser_state.token_stack) - stack_delta,
            )
            if requeue_line_info:
                return [], requeue_line_info
            POGGER.debug("parser_state.token_stack>>$", parser_state.token_stack)
            POGGER.debug("parser_state.token_document>>$", parser_state.token_document)
            POGGER.debug("close_tokens>>:$:<", close_tokens)
            block_quote_data = BlockQuoteData(
                block_quote_data.current_count,
                block_quote_data.stack_count - stack_delta,
            )
        else:
            POGGER.debug("not special_block_quote_reduction")
            close_tokens = []
        return close_tokens, None

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __process_leaf_tokens(
        parser_state: ParserState,
        leaf_tokens: List[MarkdownToken],
        xposition_marker: PositionMarker,
        block_quote_data: BlockQuoteData,
        removed_chars_at_start: Optional[int],
        ignore_link_definition_start: bool,
        last_block_quote_index: int,
        last_list_start_index: int,
        text_removed_by_container: str,
        was_paragraph_continuation: bool,
        skip_containers_before_leaf_blocks: bool,
        indent_already_processed: bool,
        container_depth: int,
        force_list_continuation: bool,
    ) -> Tuple[List[MarkdownToken], Optional[RequeueLineInfo]]:
        assert not leaf_tokens
        POGGER.debug("parsing leaf>>")
        # POGGER.debug("was_paragraph_continuation>>$", was_paragraph_continuation)
        position_marker = PositionMarker(
            xposition_marker.line_number,
            0,
            xposition_marker.text_to_parse,
            index_indent=xposition_marker.index_indent,
        )

        # POGGER.debug("ttp>>:$:<", position_marker.text_to_parse)
        # POGGER.debug("index_number>>:$:<", position_marker.index_number)
        # POGGER.debug("index_indent>>:$:<", position_marker.index_indent)
        # POGGER.debug("removed_chars_at_start>>:$:<", removed_chars_at_start)

        (
            new_index_number,
            extracted_whitespace,
        ) = ParserHelper.extract_whitespace(position_marker.text_to_parse, 0)
        # POGGER.debug("new_index_number>>:$:<", new_index_number)
        # POGGER.debug("extracted_whitespace>>:$:<", extracted_whitespace)
        # POGGER.debug("text_removed_by_container>>:$:<", text_removed_by_container)
        assert new_index_number is not None
        total_ws = new_index_number + position_marker.index_indent

        last_block_index = parser_state.find_last_block_quote_on_stack()
        last_list_index = parser_state.find_last_list_block_on_stack()
        # POGGER.debug("last_block_index>>:$:<", last_block_index)
        # POGGER.debug(
        #     "last_block.token>>:$:<",
        #     parser_state.token_stack[last_block_index].matching_markdown_token,
        # )
        # POGGER.debug("last_list_index>>:$:<", last_list_index)
        # POGGER.debug(
        #     "last_list.token>>:$:<",
        #     parser_state.token_stack[last_list_index].matching_markdown_token,
        # )

        (
            close_tokens,
            requeue_line_info,
        ) = ContainerBlockProcessor.__handle_special_block_quote_reduction(
            parser_state,
            block_quote_data,
            last_block_index,
            last_list_index,
            was_paragraph_continuation,
        )
        if requeue_line_info:
            POGGER.debug("requeuing after __handle_special_block_quote_reduction")
            return close_tokens, requeue_line_info

        orig_text_removed_by_container = text_removed_by_container

        ContainerBlockProcessor.__adjust_for_inner_list_container(
            parser_state,
            last_block_index,
            last_list_index,
            position_marker.line_number,
        )

        (
            removed_leading_space,
            actual_removed_leading_space,
        ) = ContainerBlockProcessor.__adjust_for_list_container(
            parser_state,
            last_block_index,
            last_list_index,
            text_removed_by_container,
            extracted_whitespace,
            position_marker,
            indent_already_processed,
            container_depth,
        )
        # POGGER.debug("removed_leading_space:$:", removed_leading_space)
        if removed_leading_space:
            position_marker = PositionMarker(
                position_marker.line_number,
                len(removed_leading_space),
                position_marker.text_to_parse,
                index_indent=position_marker.index_indent,
            )

        # POGGER.debug(
        #     "position_marker($:$)>>$",
        #     position_marker.index_number,
        #     position_marker.index_indent,
        #     position_marker.text_to_parse,
        # )
        if (
            not close_tokens
            and not skip_containers_before_leaf_blocks
            and not removed_leading_space
        ):
            (
                position_marker,
                text_removed_by_container,
            ) = ContainerBlockProcessor.__adjust_containers_before_leaf_blocks(
                parser_state,
                position_marker,
                was_paragraph_continuation,
                last_block_index,
                text_removed_by_container,
                total_ws,
                indent_already_processed,
                force_list_continuation,
                actual_removed_leading_space,
            )

        # POGGER.debug(
        #     "parsing leaf($:$)>>$",
        #     position_marker.index_number,
        #     position_marker.index_indent,
        #     position_marker.text_to_parse,
        # )
        # POGGER.debug(
        #     ">>orig_text_removed_by_container>>:$:<<", orig_text_removed_by_container
        # )
        POGGER.debug("parsing leaf tokens")
        (
            leaf_tokens,
            requeue_line_info,
        ) = ContainerBlockProcessor.__parse_line_for_leaf_blocks(
            parser_state,
            position_marker,
            block_quote_data,
            removed_chars_at_start,
            ignore_link_definition_start,
            last_block_quote_index,
            last_list_start_index,
            text_removed_by_container,
        )
        POGGER.debug("parsed leaf>>$", leaf_tokens)

        ContainerBlockProcessor.__post_leaf_block_adjustment(
            parser_state,
            text_removed_by_container,
            orig_text_removed_by_container,
            position_marker.line_number,
        )

        close_tokens.extend(leaf_tokens)
        return close_tokens, requeue_line_info

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __close_indented_block_if_indent_not_there(
        parser_state: ParserState, extracted_whitespace: Optional[str]
    ) -> List[MarkdownToken]:

        POGGER.debug(
            "__close_indented_block_if_indent_not_there>>$>",
            parser_state.token_stack[-1],
        )
        POGGER.debug(
            "__close_indented_block_if_indent_not_there>>$>", extracted_whitespace
        )
        pre_tokens: List[MarkdownToken] = []
        assert extracted_whitespace is not None
        if parser_state.token_stack[
            -1
        ].is_indented_code_block and ParserHelper.is_length_less_than_or_equal_to(
            extracted_whitespace, 3
        ):
            pre_tokens.append(
                parser_state.token_stack[
                    -1
                ].generate_close_markdown_token_from_stack_token()
            )
            del parser_state.token_stack[-1]

            extracted_blank_line_tokens = (
                ContainerBlockProcessor.extract_markdown_tokens_back_to_blank_line(
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
    def __handle_fenced_code_block(
        parser_state: ParserState,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        new_tokens: List[MarkdownToken],
    ) -> bool:
        """
        Take care of the processing for fenced code blocks.
        """
        if parser_state.token_stack[-1].was_link_definition_started:
            return False

        (
            fenced_tokens,
            extracted_whitespace,
        ) = LeafBlockProcessor.parse_fenced_code_block(
            parser_state,
            position_marker,
            extracted_whitespace,
        )
        if fenced_tokens:
            new_tokens.extend(fenced_tokens)
        elif parser_state.token_stack[-1].is_fenced_code_block:
            assert extracted_whitespace is not None
            new_tokens.append(
                TextMarkdownToken(
                    position_marker.text_to_parse[position_marker.index_number :],
                    extracted_whitespace,
                    position_marker=position_marker,
                )
            )
        else:
            return False
        return True

    @staticmethod
    def __handle_html_block(
        parser_state: ParserState,
        outer_processed: bool,
        position_marker: PositionMarker,
        extracted_whitespace: Optional[str],
        new_tokens: List[MarkdownToken],
    ) -> bool:
        """
        Take care of the processing for html blocks.
        """

        POGGER.debug(">>position_marker>>ttp>>$>>", position_marker.text_to_parse)
        POGGER.debug(">>position_marker>>in>>$>>", position_marker.index_number)
        POGGER.debug(">>position_marker>>ln>>$>>", position_marker.line_number)
        if not outer_processed and not parser_state.token_stack[-1].is_html_block:
            POGGER.debug(">>html started?>>")
            old_top_of_stack = parser_state.token_stack[-1]
            html_tokens = HtmlHelper.parse_html_block(
                parser_state,
                position_marker,
                extracted_whitespace,
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
            assert extracted_whitespace is not None
            html_tokens = HtmlHelper.check_normal_html_block_end(
                parser_state,
                position_marker.text_to_parse,
                position_marker.index_number,
                extracted_whitespace,
                position_marker,
            )
            assert html_tokens
            new_tokens.extend(html_tokens)
            outer_processed = True

        return outer_processed

    @staticmethod
    def __handle_block_leaf_tokens(
        parser_state: ParserState,
        incoming_position_marker: PositionMarker,
        new_tokens: List[MarkdownToken],
        ignore_link_definition_start: bool,
    ) -> Tuple[
        List[MarkdownToken],
        bool,
        Optional[RequeueLineInfo],
        PositionMarker,
        Optional[str],
    ]:

        POGGER.debug(
            "line>>$>>index>>$>>",
            incoming_position_marker.text_to_parse,
            incoming_position_marker.index_number,
        )
        remaining_line_to_parse = incoming_position_marker.text_to_parse[
            incoming_position_marker.index_number :
        ]
        (new_index_number, extracted_whitespace,) = ParserHelper.extract_whitespace(
            incoming_position_marker.text_to_parse,
            incoming_position_marker.index_number,
        )
        assert new_index_number is not None
        POGGER.debug(">>__handle_block_leaf_tokens>>ex_ws>>:$:<<", extracted_whitespace)

        position_marker = PositionMarker(
            incoming_position_marker.line_number,
            new_index_number,
            incoming_position_marker.text_to_parse,
            index_indent=incoming_position_marker.index_indent,
        )

        pre_tokens = ContainerBlockProcessor.__close_indented_block_if_indent_not_there(
            parser_state, extracted_whitespace
        )

        outer_processed = ContainerBlockProcessor.__handle_fenced_code_block(
            parser_state,
            position_marker,
            extracted_whitespace,
            new_tokens,
        )

        ignore_lrd_start = (
            ignore_link_definition_start or parser_state.token_stack[-1].is_html_block
        )

        (
            outer_processed,
            requeue_line_info,
        ) = LinkReferenceDefinitionHelper.handle_link_reference_definition_leaf_block(
            parser_state,
            outer_processed,
            position_marker,
            extracted_whitespace,
            remaining_line_to_parse,
            ignore_lrd_start,
            pre_tokens,
        )

        outer_processed = ContainerBlockProcessor.__handle_html_block(
            parser_state,
            outer_processed,
            position_marker,
            extracted_whitespace,
            new_tokens,
        )
        return (
            pre_tokens,
            outer_processed,
            requeue_line_info,
            position_marker,
            extracted_whitespace,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __parse_line_for_leaf_blocks(
        parser_state: ParserState,
        position_marker: PositionMarker,
        block_quote_data: BlockQuoteData,
        removed_chars_at_start: Optional[int],
        ignore_link_definition_start: bool,
        last_block_quote_index: int,
        last_list_start_index: int,
        text_removed_by_container: str,
    ) -> Tuple[List[MarkdownToken], Optional[RequeueLineInfo]]:
        """
        Parse the contents of a line for a leaf block.

        Note: This is one of the more heavily traffic functions in the
        parser.  Debugging should be uncommented only if needed.
        """
        POGGER.debug("Leaf Line:$:", position_marker.text_to_parse)
        POGGER.debug(">>text_removed_by_container>>:$:<<", text_removed_by_container)
        # POGGER.debug("block_quote_data.current_count:$:", block_quote_data.current_count)
        new_tokens: List[MarkdownToken] = []

        (
            pre_tokens,
            outer_processed,
            requeue_line_info,
            leaf_block_position_marker,
            extracted_whitespace,
        ) = ContainerBlockProcessor.__handle_block_leaf_tokens(
            parser_state,
            position_marker,
            new_tokens,
            ignore_link_definition_start,
        )

        if not outer_processed:
            assert not new_tokens
            new_tokens = (
                LeafBlockProcessor.parse_atx_headings(
                    parser_state, leaf_block_position_marker, extracted_whitespace
                )
                or LeafBlockProcessor.parse_indented_code_block(
                    parser_state,
                    leaf_block_position_marker,
                    extracted_whitespace,
                    removed_chars_at_start,
                    last_block_quote_index,
                    last_list_start_index,
                )
                or LeafBlockProcessor.parse_setext_headings(
                    parser_state,
                    leaf_block_position_marker,
                    extracted_whitespace,
                    block_quote_data,
                )
                or LeafBlockProcessor.parse_thematic_break(
                    parser_state,
                    leaf_block_position_marker,
                    extracted_whitespace,
                    block_quote_data,
                )
                or LeafBlockProcessor.parse_paragraph(
                    parser_state,
                    leaf_block_position_marker,
                    extracted_whitespace,
                    block_quote_data,
                    text_removed_by_container,
                )
            )
        # POGGER.debug(">>leaf--adding>>$", new_tokens)
        pre_tokens.extend(new_tokens)
        # POGGER.debug(">>leaf--added>>$", pre_tokens)
        return pre_tokens, requeue_line_info

    # pylint: enable=too-many-arguments

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

    @staticmethod
    def __look_for_pragmas(
        position_marker: PositionMarker,
        container_depth: int,
        parser_properties: ParseBlockPassProperties,
    ) -> bool:

        _, extracted_whitespace = ParserHelper.extract_whitespace(
            position_marker.text_to_parse, 0
        )
        return (
            PragmaExtension.look_for_pragmas(
                position_marker,
                position_marker.text_to_parse,
                container_depth,
                extracted_whitespace,
                parser_properties,
            )
            if parser_properties.is_pragmas_enabled
            else False
        )
