"""
Inline processing
"""
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, cast

from pymarkdown.constants import Constants
from pymarkdown.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ListStartMarkdownToken,
)
from pymarkdown.emphasis_helper import EmphasisHelper
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.inline_markdown_token import (
    RawHtmlMarkdownToken,
    ReferenceMarkdownToken,
    SpecialTextMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.inline_request import InlineRequest
from pymarkdown.inline_response import InlineResponse
from pymarkdown.leaf_markdown_token import (
    AtxHeadingMarkdownToken,
    ParagraphMarkdownToken,
)
from pymarkdown.link_helper import LinkHelper
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


class InlineProcessor:
    """
    Handle the inline processing of the token stream.
    """

    __valid_inline_text_block_sequence_starts = ""
    __valid_inline_simple_text_block_sequence_starts = ""
    __inline_processing_needed = (
        f"{EmphasisHelper.inline_emphasis}{LinkHelper.link_label_start}"
        + f"{LinkHelper.link_label_end}"
    )
    __inline_character_handlers: Dict[str, Optional[Any]] = {}
    __inline_simple_character_handlers: Dict[str, Optional[Any]] = {}

    """
    Class to provide helper functions for parsing html.
    """

    @staticmethod
    def initialize() -> None:
        """
        Initialize the inline processor subsystem.
        """
        InlineProcessor.__inline_character_handlers = {}
        InlineProcessor.__inline_simple_character_handlers = {}
        InlineProcessor.__valid_inline_text_block_sequence_starts = (
            ParserHelper.newline_character
        )
        InlineProcessor.__valid_inline_simple_text_block_sequence_starts = (
            ParserHelper.newline_character
        )

        InlineProcessor.register_handlers(
            InlineHelper.code_span_bounds, InlineHelper.handle_inline_backtick
        )
        InlineProcessor.register_handlers(
            InlineHelper.backslash_character,
            InlineHelper.handle_inline_backslash,
            is_simple_handler=True,
        )
        InlineProcessor.register_handlers(
            InlineHelper.character_reference_start_character,
            InlineHelper.handle_character_reference,
            is_simple_handler=True,
        )
        InlineProcessor.register_handlers(
            InlineHelper.angle_bracket_start, InlineHelper.handle_angle_brackets
        )
        for i in InlineProcessor.__inline_processing_needed:
            InlineProcessor.register_handlers(
                i, InlineProcessor.__handle_inline_special_single_character
            )
        InlineProcessor.register_handlers(
            LinkHelper.image_start_sequence[0],
            InlineProcessor.__handle_inline_image_link_start_character,
        )
        for i in ParserHelper.valid_characters_to_escape():
            InlineProcessor.register_handlers(
                i, InlineProcessor.__handle_inline_control_character
            )

    @staticmethod
    def __handle_inline_control_character(
        inline_request: InlineRequest,
    ) -> InlineResponse:
        inline_response = InlineResponse()
        (
            inline_response.new_index,
            inline_response.new_string,
            inline_response.delta_column_number,
        ) = (
            inline_request.next_index + 1,
            f"{ParserHelper.escape_character}{inline_request.source_text[inline_request.next_index]}",
            1,
        )
        return inline_response

    @staticmethod
    def register_handlers(
        inline_character: str,
        start_token_handler: Callable[[InlineRequest], InlineResponse],
        is_simple_handler: bool = False,
    ) -> None:
        """
        Register the handlers necessary to deal with token's start and end.
        """
        InlineProcessor.__inline_character_handlers[
            inline_character
        ] = start_token_handler
        InlineProcessor.__valid_inline_text_block_sequence_starts += inline_character
        if is_simple_handler:
            InlineProcessor.__inline_simple_character_handlers[
                inline_character
            ] = start_token_handler
            InlineProcessor.__valid_inline_simple_text_block_sequence_starts += (
                inline_character
            )

    @staticmethod
    def parse_inline(coalesced_results: List[MarkdownToken]) -> List[MarkdownToken]:
        """
        Parse and resolve any inline elements.
        """
        POGGER.info("coalesced_results")
        POGGER.info("-----")
        for next_token in coalesced_results:
            POGGER.info(">>$<<", next_token)
        POGGER.info("-----")

        coalesced_stack: List[MarkdownToken] = []
        current_token = coalesced_results[0]
        coalesced_list: List[MarkdownToken] = []
        coalesced_list.extend(coalesced_results[:1])

        POGGER.debug("STACK?:$", current_token)
        if current_token.is_container:
            POGGER.debug("STACK:$", coalesced_stack)
            coalesced_stack.append(current_token)
            POGGER.debug("STACK-ADD:$", current_token)
            POGGER.debug("STACK:$", coalesced_stack)
            if current_token.is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, current_token)
                block_quote_token.leading_text_index = 0
                POGGER.info("-->last->block->$", block_quote_token.leading_text_index)
            else:
                POGGER.info("-->not bq-")

        for coalesce_index in range(1, len(coalesced_results)):
            InlineProcessor.__process_next_coalesce_item(
                coalesced_results, coalesce_index, coalesced_list, coalesced_stack
            )
        return coalesced_list

    @staticmethod
    def __adjust_stack(
        coalesced_results: List[MarkdownToken],
        coalesced_stack: List[MarkdownToken],
        coalesce_index: int,
    ) -> None:
        current_token = coalesced_results[coalesce_index]
        POGGER.debug("STACK?:$", current_token)
        if current_token.is_container and not current_token.is_new_list_item:
            POGGER.debug("STACK:$", coalesced_stack)
            coalesced_stack.append(current_token)
            POGGER.debug("STACK-ADD:$", current_token)
            POGGER.debug("STACK:$", coalesced_stack)
            if current_token.is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, current_token)
                block_quote_token.leading_text_index = 0
                POGGER.info("-->last->block->$", block_quote_token.leading_text_index)
            else:
                POGGER.info("-->not bq-")

        elif current_token.is_list_end or current_token.is_block_quote_end:
            POGGER.debug("STACK:$", coalesced_stack)
            del coalesced_stack[-1]
            POGGER.debug(
                "STACK-REMOVE:$",
                current_token,
            )
            POGGER.debug("STACK:$", coalesced_stack)

    @staticmethod
    def __process_next_coalesce_item(
        coalesced_results: List[MarkdownToken],
        coalesce_index: int,
        coalesced_list: List[MarkdownToken],
        coalesced_stack: List[MarkdownToken],
    ) -> None:
        POGGER.info("coalesced_results:$<", coalesced_list[-1])
        POGGER.info("coalesced_stack:$<", coalesced_stack)
        for i in range(len(coalesced_stack) - 1, -1, -1):
            if coalesced_stack[i].is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, coalesced_stack[i])
                POGGER.info(
                    "$-->last->block->$", i, block_quote_token.leading_text_index
                )
        if coalesced_results[coalesce_index].is_text and (
            coalesced_list[-1].is_paragraph
            or coalesced_list[-1].is_setext_heading
            or coalesced_list[-1].is_atx_heading
            or coalesced_list[-1].is_code_block
        ):
            if coalesced_list[-1].is_code_block:
                processed_tokens = InlineProcessor.__parse_code_block(
                    coalesced_results, coalesce_index, coalesced_list, coalesced_stack
                )
            elif coalesced_list[-1].is_setext_heading:
                processed_tokens = InlineProcessor.__parse_setext_heading(
                    coalesced_results, coalesce_index, coalesced_stack
                )
            elif coalesced_list[-1].is_atx_heading:
                processed_tokens = InlineProcessor.__parse_atx_heading(
                    coalesced_results, coalesce_index, coalesced_stack, coalesced_list
                )
            else:
                processed_tokens = InlineProcessor.__parse_paragraph(
                    coalesced_list, coalesced_results, coalesce_index, coalesced_stack
                )
            coalesced_list.extend(processed_tokens)
        else:
            coalesced_list.append(coalesced_results[coalesce_index])

        InlineProcessor.__adjust_stack(
            coalesced_results, coalesced_stack, coalesce_index
        )

    @staticmethod
    def __parse_paragraph(
        coalesced_list: List[MarkdownToken],
        coalesced_results: List[MarkdownToken],
        coalesce_index: int,
        coalesced_stack: List[MarkdownToken],
    ) -> List[MarkdownToken]:
        assert coalesced_list[-1].is_paragraph
        paragraph_token = cast(ParagraphMarkdownToken, coalesced_list[-1])
        assert coalesced_results[coalesce_index].is_text
        text_token = cast(TextMarkdownToken, coalesced_results[coalesce_index])
        POGGER.debug(
            ">>before_add_ws>>$>>add>>$>>",
            coalesced_list[-1],
            text_token.extracted_whitespace,
        )
        paragraph_token.add_whitespace(text_token.extracted_whitespace)
        POGGER.debug(">>after_add_ws>>$", coalesced_list[-1])
        POGGER.debug(
            ">>text_token>>$", ParserHelper.make_whitespace_visible(str(text_token))
        )
        POGGER.debug(
            "text_token.token_text>:$:<",
            ParserHelper.make_whitespace_visible(str(text_token.token_text)),
        )
        return InlineProcessor.__process_inline_text_block(
            text_token.token_text,
            coalesced_stack,
            is_para=True,
            para_space=text_token.extracted_whitespace,
            line_number=text_token.line_number,
            column_number=text_token.column_number,
            para_owner=paragraph_token,
            tabified_text=text_token.tabified_text,
        )

    @staticmethod
    def __parse_atx_heading(
        coalesced_results: List[MarkdownToken],
        coalesce_index: int,
        coalesced_stack: List[MarkdownToken],
        coalesced_list: List[MarkdownToken],
    ) -> List[MarkdownToken]:

        assert coalesced_results[coalesce_index].is_text
        text_token = cast(TextMarkdownToken, coalesced_results[coalesce_index])
        POGGER.debug("atx-block>>$<<", text_token)
        POGGER.debug(
            "atx-block-text>>$<<",
            text_token.token_text,
        )
        POGGER.debug(
            "atx-block-ws>>$<<",
            text_token.extracted_whitespace,
        )

        assert coalesced_list[-1].is_atx_heading
        atx_token = cast(AtxHeadingMarkdownToken, coalesced_list[-1])
        POGGER.debug(">>text_token>>$", text_token)
        return InlineProcessor.__process_inline_text_block(
            text_token.token_text,
            coalesced_stack,
            text_token.extracted_whitespace,
            line_number=text_token.line_number,
            column_number=text_token.column_number
            + len(text_token.extracted_whitespace)
            + atx_token.hash_count,
        )

    @staticmethod
    def __parse_setext_heading(
        coalesced_results: List[MarkdownToken],
        coalesce_index: int,
        coalesced_stack: List[MarkdownToken],
    ) -> List[MarkdownToken]:

        assert coalesced_results[coalesce_index].is_text
        text_token = cast(TextMarkdownToken, coalesced_results[coalesce_index])
        POGGER.debug(">>text_token>>$", text_token)
        processed_tokens = InlineProcessor.__process_inline_text_block(
            text_token.token_text,
            coalesced_stack,
            whitespace_to_recombine=text_token.extracted_whitespace,
            is_setext=True,
            para_space=text_token.extracted_whitespace,
            line_number=text_token.line_number,
            column_number=text_token.column_number,
        )
        POGGER.debug(
            "processed_tokens>>$",
            processed_tokens,
        )
        return processed_tokens

    @staticmethod
    def __parse_code_block(
        coalesced_results: List[MarkdownToken],
        coalesce_index: int,
        coalesced_list: List[MarkdownToken],
        coalesced_stack: List[MarkdownToken],
    ) -> List[MarkdownToken]:

        assert coalesced_results[coalesce_index].is_text
        text_token = cast(TextMarkdownToken, coalesced_results[coalesce_index])
        encoded_text = InlineHelper.append_text("", text_token.token_text)
        if coalesced_list[-1].is_fenced_code_block:
            line_number_delta, new_column_number = 1, 1

            POGGER.info("coalesced_stack:$<", coalesced_stack)
            if coalesced_stack:
                list_token = cast(ListStartMarkdownToken, coalesced_stack[-1])
                assert list_token.leading_spaces
                split_leading_spaces = list_token.leading_spaces.split(
                    ParserHelper.newline_character
                )
                new_column_number += (
                    (len(split_leading_spaces[1]))
                    if len(split_leading_spaces) >= 2
                    else (len(split_leading_spaces[0]))
                )
            else:
                leading_whitespace = text_token.extracted_whitespace
                POGGER.debug(">>$<<", text_token)
                assert ParserHelper.newline_character not in leading_whitespace
                POGGER.info(
                    "leading_whitespace:$<",
                    leading_whitespace,
                )
                leading_whitespace = ParserHelper.remove_all_from_text(
                    leading_whitespace
                )
                POGGER.info("leading_whitespace:$<", leading_whitespace)
                new_column_number += len(leading_whitespace)
        else:
            line_number_delta, new_column_number = (
                0,
                coalesced_list[-1].column_number,
            )
        processed_tokens: List[MarkdownToken] = [
            TextMarkdownToken(
                encoded_text,
                text_token.extracted_whitespace,
                line_number=coalesced_list[-1].line_number + line_number_delta,
                column_number=new_column_number,
            )
        ]
        POGGER.debug(
            "new Text>>$>>",
            processed_tokens,
        )
        return processed_tokens

    @staticmethod
    def __handle_inline_special_single_character(
        inline_request: InlineRequest,
    ) -> InlineResponse:
        return InlineProcessor.__handle_inline_special(
            inline_request.source_text,
            inline_request.next_index,
            inline_request.inline_blocks,
            1,
            inline_request.remaining_line,
            inline_request.tabified_remaining_line,
            inline_request.current_string_unresolved,
            inline_request.line_number,
            inline_request.column_number,
            inline_request.para_owner,
            inline_request.tabified_text,
        )

    @staticmethod
    def __handle_inline_image_link_start_character(
        inline_request: InlineRequest,
    ) -> InlineResponse:
        if ParserHelper.are_characters_at_index(
            inline_request.source_text,
            inline_request.next_index,
            LinkHelper.image_start_sequence,
        ):
            inline_response = InlineProcessor.__handle_inline_special(
                inline_request.source_text,
                inline_request.next_index,
                inline_request.inline_blocks,
                2,
                inline_request.remaining_line,
                inline_request.tabified_remaining_line,
                inline_request.current_string_unresolved,
                inline_request.line_number,
                inline_request.column_number,
                inline_request.para_owner,
                inline_request.tabified_text,
            )
            assert not inline_response.consume_rest_of_line
        else:
            inline_response = InlineResponse()
            (
                inline_response.new_string,
                inline_response.new_index,
                inline_response.delta_column_number,
            ) = (LinkHelper.image_start_sequence[0], inline_request.next_index + 1, 1)
        return inline_response

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_inline_special(
        source_text: str,
        next_index: int,
        inline_blocks: List[MarkdownToken],
        special_length: int,
        remaining_line: Optional[str],
        tabified_remaining_line: Optional[str],
        current_string_unresolved: Optional[str],
        line_number: Optional[int],
        column_number: Optional[int],
        para_owner: Optional[ParagraphMarkdownToken],
        tabified_text: Optional[str],
    ) -> InlineResponse:
        """
        Handle the collection of special inline characters for later processing.
        """
        assert remaining_line is not None
        assert column_number is not None
        assert current_string_unresolved is not None

        POGGER.debug(">>tabified_text>:$:<", tabified_text)
        remaining_line_size = len(remaining_line)
        POGGER.debug(">>column_number>>$<<", column_number)
        POGGER.debug(">>remaining_line>>$<<", remaining_line)
        column_number += remaining_line_size
        POGGER.debug(">>column_number>>$<<", column_number)

        (
            special_sequence,
            repeat_count,
            new_index,
            preceding_two,
            following_two,
            is_active,
            new_token,
            consume_rest_of_line,
            delta_line,
        ) = InlineProcessor.__handle_inline_special_character(
            special_length,
            inline_blocks,
            remaining_line,
            tabified_remaining_line,
            current_string_unresolved,
            source_text,
            next_index,
            para_owner,
            remaining_line_size,
            tabified_text,
        )

        if not new_token:
            assert line_number is not None
            assert repeat_count is not None
            POGGER.debug(">>create>>$,$<<", line_number, column_number)
            new_token = SpecialTextMarkdownToken(
                special_sequence,
                repeat_count,
                preceding_two,
                following_two,
                is_active,
                line_number,
                column_number,
            )

        POGGER.debug(">>delta_line>>$<<", delta_line)
        POGGER.debug(">>repeat_count>>$<<", repeat_count)
        assert repeat_count is not None
        inline_response = InlineResponse()
        (
            inline_response.new_string,
            inline_response.new_index,
            inline_response.new_tokens,
            inline_response.consume_rest_of_line,
            inline_response.delta_line_number,
            inline_response.delta_column_number,
        ) = ("", new_index, [new_token], consume_rest_of_line, delta_line, repeat_count)
        return inline_response

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_inline_special_character(
        special_length: int,
        inline_blocks: List[MarkdownToken],
        remaining_line: str,
        tabified_remaining_line: Optional[str],
        current_string_unresolved: str,
        source_text: str,
        next_index: int,
        para_owner: Optional[ParagraphMarkdownToken],
        remaining_line_size: int,
        tabified_text: Optional[str],
    ) -> Tuple[
        str,
        Optional[int],
        int,
        Optional[str],
        Optional[str],
        bool,
        Optional[MarkdownToken],
        bool,
        int,
    ]:
        (
            preceding_two,
            following_two,
            is_active,
            new_token,
            consume_rest_of_line,
            delta_line,
        ) = (None, None, True, None, False, 0)
        repeat_count: Optional[int] = 1
        special_sequence = source_text[next_index : next_index + special_length]
        if special_length == 1 and special_sequence in EmphasisHelper.inline_emphasis:
            repeat_count, new_index = ParserHelper.collect_while_character(
                source_text, next_index, special_sequence
            )
            assert new_index is not None
            special_sequence, preceding_two, following_two = (
                source_text[next_index:new_index],
                source_text[max(0, next_index - 2) : next_index],
                source_text[new_index : min(len(source_text), new_index + 2)],
            )
        elif special_sequence[0] == LinkHelper.link_label_end:
            POGGER.debug(
                "POSSIBLE LINK CLOSE_FOUND($)>>$>>",
                special_length,
                special_sequence,
            )
            assert repeat_count is not None
            (
                new_index,
                is_active,
                new_token,
                consume_rest_of_line,
                repeat_count,
                delta_line,
            ) = InlineProcessor.__handle_link_label_end(
                inline_blocks,
                remaining_line,
                tabified_remaining_line,
                current_string_unresolved,
                source_text,
                next_index,
                para_owner,
                remaining_line_size,
                delta_line,
                repeat_count,
                tabified_text,
            )
        else:
            repeat_count, new_index = special_length, next_index + special_length
        return (
            special_sequence,
            repeat_count,
            new_index,
            preceding_two,
            following_two,
            is_active,
            new_token,
            consume_rest_of_line,
            delta_line,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_link_label_end(
        inline_blocks: List[MarkdownToken],
        remaining_line: str,
        tabified_remaining_line: Optional[str],
        current_string_unresolved: str,
        source_text: str,
        next_index: int,
        para_owner: Optional[ParagraphMarkdownToken],
        remaining_line_size: int,
        delta_line: int,
        repeat_count: int,
        tabified_text: Optional[str],
    ) -> Tuple[int, bool, Optional[MarkdownToken], bool, int, int]:
        POGGER.debug(
            ">>inline_blocks>>$<<",
            inline_blocks,
        )
        POGGER.debug(
            ">>remaining_line>>$<<",
            remaining_line,
        )
        POGGER.debug(
            ">>tabified_remaining_line>>$<<",
            tabified_remaining_line,
        )
        POGGER.debug(
            ">>current_string_unresolved>>$<<",
            current_string_unresolved,
        )
        POGGER.debug(
            ">>source_text[next_index=$:]>:$:<",
            next_index,
            source_text[next_index:],
        )
        POGGER.debug(
            ">>source_text>:$:<",
            source_text,
        )
        POGGER.debug(
            ">>tabified_text>>$<<",
            tabified_text,
        )
        POGGER.debug("")
        old_inline_blocks_count, old_inline_blocks_last_token = (
            len(inline_blocks),
            inline_blocks[-1] if inline_blocks else None,
        )

        (
            new_index,
            is_active,
            new_token,
            consume_rest_of_line,
        ) = LinkHelper.look_for_link_or_image(
            inline_blocks,
            source_text,
            next_index,
            remaining_line,
            tabified_remaining_line,
            current_string_unresolved,
            InlineProcessor.__process_simple_inline_fn,
            tabified_text,
        )
        POGGER.debug(">>next_index>>$<<", next_index)
        POGGER.debug(">>new_index>>$<<", new_index)
        POGGER.debug(
            ">>source_text:new_index>>$<<",
            source_text[new_index:],
        )
        POGGER.debug(">>inline_blocks>>$<<", inline_blocks)
        POGGER.debug(">>new_token>>$<<", new_token)
        POGGER.debug(">>source_text>>$<<", source_text[new_index:])
        POGGER.debug(">>consume_rest_of_line>>$<<", consume_rest_of_line)
        POGGER.debug(">>old_inline_blocks_count>>$<<", old_inline_blocks_count)

        new_inline_blocks_count = len(inline_blocks)
        POGGER.debug(">>new_inline_blocks_count>>$<<", new_inline_blocks_count)

        if (
            new_token
            or old_inline_blocks_count != new_inline_blocks_count
            or (inline_blocks and old_inline_blocks_last_token != inline_blocks[-1])
        ):
            (
                delta_line,
                repeat_count,
            ) = InlineProcessor.__calculate_repeat_count_and_delta_line(
                inline_blocks,
                new_token,
                new_index,
                next_index,
                remaining_line_size,
                para_owner,
                delta_line,
            )
        return (
            new_index,
            is_active,
            new_token,
            consume_rest_of_line,
            repeat_count,
            delta_line,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_repeat_count_and_delta_line(
        inline_blocks: List[MarkdownToken],
        new_token: Optional[MarkdownToken],
        new_index: int,
        next_index: int,
        remaining_line_size: int,
        para_owner: Optional[ParagraphMarkdownToken],
        delta_line: int,
    ) -> Tuple[int, int]:

        if inline_blocks[-1].is_inline_image:
            repeat_count = (new_index - next_index) + remaining_line_size
            (
                delta_line,
                repeat_count,
            ) = InlineProcessor.__calculate_link_and_image_deltas(
                para_owner, inline_blocks[-1], delta_line, repeat_count
            )
            POGGER.debug(">>delta_line>>$<<", delta_line)
            POGGER.debug(">>repeat_count>>$<<", repeat_count)
        elif new_token and new_token.is_inline_link_end:
            end_token = cast(EndMarkdownToken, new_token)
            POGGER.debug(
                ">>new_token.start_markdown_token>>$<<",
                end_token.start_markdown_token,
            )
            assert end_token.start_markdown_token
            repeat_count = new_index - next_index
            POGGER.debug(">>delta_line>>$<<", delta_line)
            POGGER.debug(">>repeat_count>>$<<", repeat_count)
            if para_owner:
                POGGER.debug(
                    ">>para_owner.rehydrate_index>>$<<",
                    para_owner.rehydrate_index,
                )
            (
                delta_line,
                repeat_count,
            ) = InlineProcessor.__calculate_link_and_image_deltas(
                para_owner,
                end_token.start_markdown_token,
                delta_line,
                repeat_count,
            )
            if para_owner:
                POGGER.debug(
                    ">>para_owner.rehydrate_index>>$<<",
                    para_owner.rehydrate_index,
                )
            POGGER.debug(">>delta_line>>$<<", delta_line)
            POGGER.debug(">>repeat_count>>$<<", repeat_count)
        else:
            repeat_count = new_index - next_index
            POGGER.debug(">>repeat_count>>$<<", repeat_count)
        return delta_line, repeat_count

    # pylint: enable=too-many-arguments

    @staticmethod
    def __process_simple_inline_fn(source_text: str) -> str:
        """
        Handle a simple processing of inline text for simple replacements.
        """

        POGGER.debug(">>source_text>>$", source_text)
        start_index, processed_parts = 0, []
        POGGER.debug(
            ">>__valid_inline_simple_text_block_sequence_starts>>$",
            InlineProcessor.__valid_inline_simple_text_block_sequence_starts,
        )
        next_index = ParserHelper.index_any_of(
            source_text,
            InlineProcessor.__valid_inline_simple_text_block_sequence_starts,
            start_index,
        )
        POGGER.debug(">>next_index>>$", next_index)
        while next_index != -1:
            processed_parts.append(source_text[start_index:next_index])
            inline_request = InlineRequest(source_text, next_index)
            if source_text[next_index] in InlineProcessor.__inline_character_handlers:
                POGGER.debug(
                    "handler(before)>>$<<",
                    source_text[next_index],
                )
                POGGER.debug("current_string_unresolved>>$<<", processed_parts)
                proc_fn = InlineProcessor.__inline_character_handlers[
                    source_text[next_index]
                ]
                assert proc_fn is not None
                inline_response = proc_fn(inline_request)
                processed_parts.append(inline_response.new_string)
                POGGER.debug("handler(after)>>$<<", source_text[next_index])
                POGGER.debug(
                    "delta_line_number>>$<<", inline_response.delta_line_number
                )
                POGGER.debug("delta_column>>$<<", inline_response.delta_column_number)
                start_index = inline_response.new_index
            else:
                processed_parts.append(ParserHelper.newline_character)
                start_index = next_index + 1
            next_index = ParserHelper.index_any_of(
                source_text,
                InlineProcessor.__valid_inline_simple_text_block_sequence_starts,
                start_index,
            )

        processed_parts.append(source_text[start_index:])
        return "".join(processed_parts)

    @staticmethod
    def __calculate_full_deltas(
        current_token: ReferenceMarkdownToken,
        para_owner: Optional[ParagraphMarkdownToken],
        delta_line: int,
        repeat_count: int,
    ) -> Tuple[int, int]:
        assert current_token.ex_label is not None
        if newline_count := ParserHelper.count_newlines_in_text(current_token.ex_label):
            POGGER.debug(">>ex_label")
            delta_line += newline_count
            if para_owner:
                POGGER.debug(
                    ">>para_owner.rehydrate_index>>$<<", para_owner.rehydrate_index
                )
                para_owner.rehydrate_index += newline_count
                POGGER.debug(
                    ">>para_owner.rehydrate_index>>$<<", para_owner.rehydrate_index
                )
            POGGER.debug("full>>ex_label>>newline_count>>$", newline_count)

            last_line_of_label = ParserHelper.calculate_last_line(
                current_token.ex_label
            )
            repeat_count = -(len(last_line_of_label) + 2)
        return delta_line, repeat_count

    @staticmethod
    def __calculate_inline_deltas(
        current_token: ReferenceMarkdownToken,
        para_owner: Optional[ParagraphMarkdownToken],
        split_paragraph_lines: Optional[List[str]],
        delta_line: int,
        repeat_count: int,
    ) -> Tuple[int, int]:
        assert current_token.is_inline_link or current_token.is_inline_image
        active_link_title = current_token.active_link_title

        assert current_token.before_title_whitespace is not None
        link_part_lengths = [0] * 5
        link_part_lengths[0] = len(current_token.active_link_uri) + len(
            current_token.before_title_whitespace
        )
        if current_token.inline_title_bounding_character:
            assert active_link_title is not None
            assert current_token.after_title_whitespace is not None

            link_part_lengths[1] = 1
            link_part_lengths[2] = len(active_link_title) + 1
            link_part_lengths[3] = len(current_token.after_title_whitespace)
        POGGER.debug(">>link_part_lengths>>$<<", link_part_lengths)

        (link_part_index, total_newlines) = InlineProcessor.__calculate_inline_label(
            current_token
        )

        assert current_token.before_link_whitespace is not None
        (
            link_part_index,
            delta_line,
            last_spaces,
        ) = InlineProcessor.__calculate_inline_whitespace(
            current_token.before_link_whitespace,
            "before_link_whitespace",
            0,
            link_part_index,
            delta_line,
            "",
        )

        (
            link_part_index,
            delta_line,
            last_spaces,
        ) = InlineProcessor.__calculate_inline_whitespace(
            current_token.before_title_whitespace,
            "before_title_whitespace",
            1,
            link_part_index,
            delta_line,
            last_spaces,
        )

        assert active_link_title is not None
        (
            link_part_index,
            delta_line,
            last_spaces,
            new_link_part_length,
        ) = InlineProcessor.__calculate_inline_link_title(
            active_link_title, link_part_index, delta_line, last_spaces
        )
        if new_link_part_length is not None:
            link_part_lengths[2] = new_link_part_length

        assert current_token.after_title_whitespace is not None
        (
            link_part_index,
            delta_line,
            last_spaces,
        ) = InlineProcessor.__calculate_inline_whitespace(
            current_token.after_title_whitespace,
            "after_title_whitespace",
            4,
            link_part_index,
            delta_line,
            last_spaces,
        )

        return InlineProcessor.__calculate_inline_delta_adjustments(
            link_part_index,
            total_newlines,
            delta_line,
            repeat_count,
            para_owner,
            split_paragraph_lines,
            link_part_lengths,
            last_spaces,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_inline_delta_adjustments(
        link_part_index: int,
        total_newlines: int,
        delta_line: int,
        repeat_count: int,
        para_owner: Optional[ParagraphMarkdownToken],
        split_paragraph_lines: Optional[List[str]],
        link_part_lengths: List[int],
        last_spaces: str,
    ) -> Tuple[int, int]:

        POGGER.debug(">>link_part_index>>$<<", link_part_index)
        POGGER.debug(">>total_newlines>>$<<", total_newlines)
        POGGER.debug(">>delta_line>>$<<", delta_line)

        if para_owner:
            POGGER.debug(
                ">>para_owner.rehydrate_index>>$<<", para_owner.rehydrate_index
            )
            para_owner.rehydrate_index += delta_line
            POGGER.debug(
                ">>para_owner.rehydrate_index>>$<<", para_owner.rehydrate_index
            )
        if link_part_index >= 0:
            if split_paragraph_lines:
                assert para_owner is not None
                link_part_lengths[4] = len(
                    split_paragraph_lines[para_owner.rehydrate_index]
                )
            else:
                link_part_lengths[4] = len(
                    ParserHelper.calculate_last_line(last_spaces)
                )
            link_part_lengths[:link_part_index] = [0] * link_part_index
            repeat_count = -(2 + sum(link_part_lengths))
            POGGER.debug(">>link_part_lengths>>$<<", link_part_lengths)
            POGGER.debug(">>repeat_count>>$<<", delta_line)
        return delta_line, repeat_count

    # pylint: enable=too-many-arguments

    @staticmethod
    def __calculate_inline_label(current_token: MarkdownToken) -> Tuple[int, int]:

        reference_token = cast(ReferenceMarkdownToken, current_token)
        total_newlines = ParserHelper.count_newlines_in_text(
            reference_token.text_from_blocks
        )
        link_part_index = -1 if total_newlines else -2
        return link_part_index, total_newlines

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_inline_whitespace(
        sample_string: str,
        sample_name: str,
        new_link_part_index: int,
        link_part_index: int,
        delta_line: int,
        last_spaces: str,
    ) -> Tuple[int, int, str]:
        if newline_count := ParserHelper.count_newlines_in_text(sample_string):
            POGGER.debug(">>$", sample_name)
            link_part_index, delta_line, last_spaces = (
                new_link_part_index,
                delta_line + newline_count,
                sample_string[:],
            )
        return link_part_index, delta_line, last_spaces

    # pylint: enable=too-many-arguments

    @staticmethod
    def __calculate_inline_link_title(
        active_link_title: str, link_part_index: int, delta_line: int, last_spaces: str
    ) -> Tuple[int, int, str, Optional[int]]:
        if newline_count := ParserHelper.count_newlines_in_text(active_link_title):
            POGGER.debug(">>active_link_title")
            _, delta_column_number = ParserHelper.calculate_deltas(active_link_title)
            link_part_index, delta_line, last_spaces, new_link_part_length = (
                2,
                delta_line + newline_count,
                "",
                -delta_column_number,
            )
        else:
            new_link_part_length = None
        return link_part_index, delta_line, last_spaces, new_link_part_length

    @staticmethod
    def __calculate_shortcut_collapsed_deltas(
        current_token: ReferenceMarkdownToken, delta_line: int, repeat_count: int
    ) -> Tuple[int, int]:
        """
        Tests test_reference_links_extra_03jx and test_reference_links_extra_03ja added
        to ensure that this is correct.  Those tests confirm that any newlines in the
        label are already accounted for, and as such, do not require any further
        modifications.
        """
        _ = current_token
        return delta_line, repeat_count

    @staticmethod
    def __calculate_link_and_image_deltas(
        para_owner: Optional[ParagraphMarkdownToken],
        current_token: MarkdownToken,
        delta_line: int,
        repeat_count: int,
    ) -> Tuple[int, int]:
        POGGER.debug(">>delta_line>>$<<", delta_line)
        POGGER.debug(">>repeat_count>>$<<", repeat_count)

        if ParserHelper.newline_character in str(current_token):
            POGGER.debug(">>para_owner>>$<<", para_owner)
            split_paragraph_lines: Optional[List[str]] = None
            if para_owner:
                POGGER.debug(
                    ">>para_owner.rehydrate_index>>$<<", para_owner.rehydrate_index
                )
                split_paragraph_lines = para_owner.extracted_whitespace.split(
                    ParserHelper.newline_character
                )
                POGGER.debug(">>split_paragraph_lines>>$<<", split_paragraph_lines)

            reference_token = cast(ReferenceMarkdownToken, current_token)
            POGGER.debug(">>current_token.label_type>>$<<", reference_token.label_type)
            if reference_token.label_type == Constants.link_type__inline:
                delta_line, repeat_count = InlineProcessor.__calculate_inline_deltas(
                    reference_token,
                    para_owner,
                    split_paragraph_lines,
                    delta_line,
                    repeat_count,
                )
            elif reference_token.label_type == Constants.link_type__full:
                delta_line, repeat_count = InlineProcessor.__calculate_full_deltas(
                    reference_token, para_owner, delta_line, repeat_count
                )
            else:
                assert reference_token.label_type in (
                    Constants.link_type__shortcut,
                    Constants.link_type__collapsed,
                ), f"Label type '{reference_token.label_type}' not handled."
                (
                    delta_line,
                    repeat_count,
                ) = InlineProcessor.__calculate_shortcut_collapsed_deltas(
                    reference_token, delta_line, repeat_count
                )

        POGGER.debug(">>delta_line>>$<<repeat_count>>$<<", delta_line, repeat_count)
        return delta_line, repeat_count

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod  # noqa: C901
    def __process_inline_text_block(  # noqa: C901
        source_text: str,
        coalesced_stack: List[MarkdownToken],
        starting_whitespace: str = "",
        whitespace_to_recombine: Optional[str] = None,
        is_setext: bool = False,
        is_para: bool = False,
        para_space: Optional[str] = None,
        line_number: int = 0,
        column_number: int = 0,
        para_owner: Optional[ParagraphMarkdownToken] = None,
        tabified_text: Optional[str] = None,
    ) -> List[MarkdownToken]:
        """
        Process a text block for any inline items.

        Note: This is one of the more heavily traffic functions in the
        parser.  Debugging should be uncommented only if needed.
        """

        (
            last_line_number,
            last_column_number,
            current_string,
            current_string_unresolved,
        ) = (line_number, column_number, "", "")
        start_index: Optional[int] = 0
        inline_blocks: List[MarkdownToken] = []
        end_string: Optional[str] = ""
        fold_space: Optional[List[str]] = None

        # POGGER.debug(
        #     "__process_inline_text_block>>source_text>:$:<",
        #     source_text,
        # )
        # POGGER.debug(
        #    "__process_inline_text_block>>starting_whitespace>>$>",
        #    starting_whitespace,
        # )
        # POGGER.debug(
        #     "__process_inline_text_block>>whitespace_to_recombine>:$:<",
        #     whitespace_to_recombine,
        # )
        # POGGER.debug(
        #     "__process_inline_text_block>>line_number>>$>",
        #     line_number,
        # )
        # POGGER.debug(
        #     "__process_inline_text_block>>column_number>>$>",
        #     column_number,
        # )
        if whitespace_to_recombine:
            source_text, _ = ParserHelper.recombine_string_with_whitespace(
                source_text, whitespace_to_recombine
            )
        # POGGER.debug(
        #     "__process_inline_text_block>>source_text>>$",
        #     source_text,
        # )
        # POGGER.debug(
        #     ">>Token_start>>$,$<<",
        #     last_line_number,
        #     last_column_number,
        # )
        # POGGER.debug("__process_inline_text_block>>is_para>>$", is_para)
        if is_para or is_setext:
            assert para_space is not None
            fold_space = para_space.split(ParserHelper.newline_character)
        # POGGER.debug("__process_inline_text_block>>fold_space>>$", fold_space)

        # POGGER.debug(
        #     "starts>$<", InlineProcessor.__valid_inline_text_block_sequence_starts
        # )
        # POGGER.debug("look>$<", source_text[start_index:])
        assert start_index is not None
        next_index = ParserHelper.index_any_of(
            source_text,
            InlineProcessor.__valid_inline_text_block_sequence_starts,
            start_index,
        )
        newlines_encountered = 0
        # POGGER.debug("newlines_encountered>$<", newlines_encountered)
        # POGGER.debug("__process_inline_text_block>>is_setext>>$", is_setext)
        # POGGER.debug(
        #     "__process_inline_text_block>>$>>$",
        #     source_text,
        #     start_index,
        # )
        while next_index != -1:

            # POGGER.debug(
            #     "\n\n>>Token_start>>$,$<<",
            #     last_line_number,
            #     last_column_number,
            # )
            # POGGER.debug("line_number>>$>",line_number)
            # POGGER.debug("column_number>>$>", column_number)
            # POGGER.debug(">>inline_blocks>>$<<", inline_blocks)
            # POGGER.debug(">>current_string>>$<<", current_string)
            # POGGER.debug(">>current_string_unresolved>>$<<", current_string_unresolved)
            # POGGER.debug(">>current_string_unresolved>>$<<", current_string_unresolved)
            # POGGER.debug(">>end_string>>$<<", end_string)
            # POGGER.debug(
            #     ">>source_text[]>>$<<$<<",
            #     source_text[next_index],
            #     source_text[next_index:],
            # )

            old_next_index = next_index
            assert start_index is not None
            (
                line_number,
                column_number,
                end_string,
                current_string,
                current_string_unresolved,
                starting_whitespace,
                fold_space,
                last_line_number,
                last_column_number,
                start_index,
                next_index,
            ) = InlineProcessor.__handle_next_inline_character(
                source_text,
                start_index,
                next_index,
                inline_blocks,
                current_string,
                current_string_unresolved,
                line_number,
                column_number,
                para_owner,
                coalesced_stack,
                end_string,
                is_setext,
                whitespace_to_recombine,
                starting_whitespace,
                last_line_number,
                last_column_number,
                fold_space,
                tabified_text,
                newlines_encountered,
            )
            # POGGER.debug("old_next_index>$<", old_next_index)
            # POGGER.debug("source_text>:$:<", source_text)
            # POGGER.debug("source_text[]>:$:<", source_text[old_next_index])
            # POGGER.debug("newlines_encountered>$<", newlines_encountered)
            if source_text[old_next_index] == "\n":
                newlines_encountered += 1
            # POGGER.debug("newlines_encountered>$<", newlines_encountered)

        # POGGER.debug("<<__complete_inline_block_processing<<")
        # POGGER.debug(
        #     "<<__complete_inline_block_processing<<end_string<<$<<",
        #     end_string,
        # )

        return InlineProcessor.__complete_inline_block_processing(
            inline_blocks,
            source_text,
            start_index,
            current_string,
            end_string,
            starting_whitespace,
            is_setext,
            last_line_number,
            last_column_number,
            tabified_text,
            newlines_encountered,
        )

    # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_next_inline_character(
        source_text: str,
        start_index: int,
        next_index: int,
        inline_blocks: List[MarkdownToken],
        current_string: str,
        current_string_unresolved: str,
        line_number: int,
        column_number: int,
        para_owner: Optional[ParagraphMarkdownToken],
        coalesced_stack: List[MarkdownToken],
        end_string: Optional[str],
        is_setext: bool,
        whitespace_to_recombine: Optional[str],
        starting_whitespace: str,
        last_line_number: int,
        last_column_number: int,
        fold_space: Optional[List[str]],
        tabified_text: Optional[str],
        newlines_encountered: int,
    ) -> Tuple[
        int,
        int,
        Optional[str],
        str,
        str,
        str,
        Optional[List[str]],
        int,
        int,
        Optional[int],
        int,
    ]:

        (
            reset_current_string,
            remaining_line,
            old_inline_blocks_count,
            old_inline_blocks_last_token,
        ) = (
            False,
            source_text[start_index:next_index],
            len(inline_blocks),
            inline_blocks[-1] if inline_blocks else None,
        )

        # POGGER.debug("__process_inline_text_block>>$,$", start_index, next_index)
        # POGGER.debug("__process_inline_text_block>:$:<", remaining_line)
        # POGGER.debug("so far>:$:<", source_text[start_index:])
        # POGGER.debug("newlines_encountered>:$:<", newlines_encountered)
        tabified_remaining_line: Optional[str] = None
        if tabified_text:
            # POGGER.debug("tabified_text>:$:<", tabified_text)
            # POGGER.debug("char>:$:<", source_text[next_index])
            adj_original_line = InlineProcessor.__handle_next_inline_character_tabified(
                source_text,
                tabified_text,
                newlines_encountered,
                start_index,
                next_index,
            )
            tabified_remaining_line = adj_original_line
            # POGGER.debug("tabified_remaining_line>:$:<", tabified_remaining_line)

        inline_request = InlineRequest(
            source_text,
            next_index,
            inline_blocks,
            remaining_line,
            tabified_remaining_line,
            current_string_unresolved,
            line_number,
            column_number,
            para_owner,
            tabified_text,
        )

        # POGGER.debug("current_string>:$:<", current_string)
        # POGGER.debug("remaining_line>:$:<", remaining_line)
        # POGGER.debug("tabified_remaining_line>:$:<", tabified_remaining_line)

        (
            inline_response,
            line_number,
            column_number,
            was_column_number_reset,
            did_line_number_change,
            whitespace_to_add,
            remaining_line,
            end_string,
            current_string,
            was_new_line,
            tabified_remaining_line,
        ) = InlineProcessor.__handle_next_special_character(
            source_text,
            next_index,
            inline_request,
            line_number,
            column_number,
            coalesced_stack,
            InlineResponse(),
            remaining_line,
            end_string,
            current_string,
            inline_blocks,
            is_setext,
            whitespace_to_recombine,
            para_owner,
            tabified_text,
            tabified_remaining_line,
        )

        # POGGER.debug("current_string>:$:<", current_string)
        # POGGER.debug("remaining_line>:$:<", remaining_line)
        # POGGER.debug("tabified_remaining_line>:$:<", tabified_remaining_line)

        (
            reset_current_string,
            remaining_line,
            end_string,
            current_string,
            current_string_unresolved,
        ) = InlineProcessor.__cleanup_after_handling(
            inline_response,
            current_string,
            current_string_unresolved,
            remaining_line,
            tabified_remaining_line,
            reset_current_string,
            end_string,
        )

        # POGGER.debug("current_string>:$:<", current_string)
        # POGGER.debug("remaining_line>:$:<", remaining_line)
        # POGGER.debug("tabified_remaining_line>:$:<", tabified_remaining_line)

        (
            reset_current_string,
            starting_whitespace,
            end_string,
        ) = InlineProcessor.__create_new_text_token(
            inline_response,
            current_string,
            inline_blocks,
            starting_whitespace,
            end_string,
            last_line_number,
            last_column_number,
            reset_current_string,
        )

        (
            line_number,
            column_number,
            fold_space,
            current_string,
            current_string_unresolved,
            last_line_number,
            last_column_number,
            new_start_index,
            next_index,
            end_string,
        ) = InlineProcessor.__handle_next_inline_character_finish_handling(
            line_number,
            column_number,
            fold_space,
            was_new_line,
            coalesced_stack,
            remaining_line,
            did_line_number_change,
            was_column_number_reset,
            reset_current_string,
            inline_blocks,
            old_inline_blocks_count,
            old_inline_blocks_last_token,
            source_text,
            whitespace_to_add,
            inline_response,
            current_string,
            current_string_unresolved,
            last_line_number,
            last_column_number,
            end_string,
        )

        # POGGER.debug("current_string>:$:<", current_string)
        return (
            line_number,
            column_number,
            end_string,
            current_string,
            current_string_unresolved,
            starting_whitespace,
            fold_space,
            last_line_number,
            last_column_number,
            new_start_index,
            next_index,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_next_inline_character_finish_handling(
        line_number: int,
        column_number: int,
        fold_space: Optional[List[str]],
        was_new_line: bool,
        coalesced_stack: List[MarkdownToken],
        remaining_line: str,
        did_line_number_change: bool,
        was_column_number_reset: bool,
        reset_current_string: bool,
        inline_blocks: List[MarkdownToken],
        old_inline_blocks_count: int,
        old_inline_blocks_last_token: Optional[MarkdownToken],
        source_text: str,
        whitespace_to_add: Optional[str],
        inline_response: InlineResponse,
        current_string: str,
        current_string_unresolved: str,
        last_line_number: int,
        last_column_number: int,
        end_string: Optional[str],
    ) -> Tuple[
        int,
        int,
        Optional[List[str]],
        str,
        str,
        int,
        int,
        Optional[int],
        int,
        Optional[str],
    ]:
        (
            line_number,
            column_number,
            fold_space,
        ) = InlineProcessor.__adjust_line_and_column_number(
            was_new_line,
            coalesced_stack,
            line_number,
            column_number,
            fold_space,
            remaining_line,
            did_line_number_change,
            was_column_number_reset,
        )

        # POGGER.debug("current_string>:$:<", current_string)
        (
            current_string,
            current_string_unresolved,
            last_line_number,
            last_column_number,
        ) = InlineProcessor.__fix_variables_before_next_loop(
            reset_current_string,
            current_string,
            current_string_unresolved,
            inline_blocks,
            old_inline_blocks_count,
            old_inline_blocks_last_token,
            last_line_number,
            last_column_number,
            line_number,
            column_number,
        )

        # POGGER.debug("current_string>:$:<", current_string)
        (
            new_start_index,
            next_index,
            end_string,
            current_string,
            current_string_unresolved,
        ) = InlineProcessor.__complete_inline_loop(
            source_text,
            inline_response.new_index,
            end_string,
            whitespace_to_add,
            current_string,
            current_string_unresolved,
            inline_response.new_string_unresolved,
            inline_response.new_string,
            inline_response.original_string,
        )
        return (
            line_number,
            column_number,
            fold_space,
            current_string,
            current_string_unresolved,
            last_line_number,
            last_column_number,
            new_start_index,
            next_index,
            end_string,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __xdg(tabified_text: str, newlines_encountered: int) -> Tuple[str, int]:
        line_start_index = 0
        for _ in range(newlines_encountered):
            line_end_index = tabified_text.find("\n", line_start_index)
            line_start_index = line_end_index + 1
        POGGER.debug("line_start_index>:$:<", line_start_index)
        line_end_index = tabified_text.find("\n", line_start_index)
        return (
            tabified_text[line_start_index:line_end_index]
            if line_end_index != -1
            else tabified_text[line_start_index:],
            line_start_index,
        )

    # pylint: disable=too-many-locals
    @staticmethod
    def __handle_next_inline_character_tabified(
        source_text: str,
        tabified_text: str,
        newlines_encountered: int,
        start_index: int,
        next_index: int,
    ) -> Optional[str]:

        adj_tabified_text, _ = InlineProcessor.__xdg(
            tabified_text, newlines_encountered
        )
        POGGER.debug("adj_tabified_text>:$:<", adj_tabified_text)

        adj_source_text, line_start_index = InlineProcessor.__xdg(
            source_text, newlines_encountered
        )
        POGGER.debug("adj_source_text>:$:<", adj_source_text)

        current_line_source_text = source_text[start_index:next_index]
        POGGER.debug("source_text>:$:<", source_text)
        POGGER.debug("current_line_source_text>:$:<", current_line_source_text)

        stop_character = source_text[next_index]
        if stop_character != "\n":
            POGGER.debug("stop_character>:$:<", stop_character)

            found_in_source_text_count = 0
            found_in_source_text_index = source_text.find(
                stop_character, line_start_index
            )
            POGGER.debug(
                "source_text[$]>:$:<",
                found_in_source_text_index,
                source_text[found_in_source_text_index:],
            )
            while found_in_source_text_index != next_index:
                found_in_source_text_count += 1
                found_in_source_text_index = source_text.find(
                    stop_character, found_in_source_text_index + 1
                )
                POGGER.debug(
                    "source_text[$]>:$:<",
                    found_in_source_text_index,
                    source_text[found_in_source_text_index:],
                )
            POGGER.debug("found_in_source_text_count>:$:<", found_in_source_text_count)
            POGGER.debug(
                "source_text[$]>:$:<",
                found_in_source_text_index,
                source_text[found_in_source_text_index:],
            )

            found_in_tabified_text_count = 0
            stop_character_in_tabified_index = adj_tabified_text.find(stop_character)
            POGGER.debug(
                "adj_tabified_text[$]>:$:<",
                stop_character_in_tabified_index,
                adj_tabified_text[stop_character_in_tabified_index:],
            )
            while found_in_tabified_text_count != found_in_source_text_count:
                found_in_tabified_text_count += 1
                stop_character_in_tabified_index = adj_tabified_text.find(
                    stop_character, stop_character_in_tabified_index + 1
                )
                POGGER.debug(
                    "adj_tabified_text[$]>:$:<",
                    stop_character_in_tabified_index,
                    adj_tabified_text[stop_character_in_tabified_index:],
                )
                assert stop_character_in_tabified_index != -1
            POGGER.debug(
                "found_in_tabified_text_count>:$:<", found_in_tabified_text_count
            )
            POGGER.debug(
                "adj_tabified_text[$]>:$:<",
                stop_character_in_tabified_index,
                adj_tabified_text[stop_character_in_tabified_index:],
            )
            assert adj_tabified_text[stop_character_in_tabified_index] == stop_character

            (
                current_line_leading_space_index,
                current_line_leading_space,
            ) = ParserHelper.extract_spaces(current_line_source_text, 0)
            POGGER.debug(
                "current_line_leading_space_index>:$:<, current_line_leading_space>:$:<",
                current_line_leading_space_index,
                current_line_leading_space,
            )
            assert current_line_leading_space_index is not None

            word_stop_characters = " \t" + stop_character
            (
                current_line_first_word_index,
                current_line_first_word,
            ) = ParserHelper.collect_until_one_of_characters(
                current_line_source_text,
                current_line_leading_space_index,
                word_stop_characters,
            )
            POGGER.debug(
                "current_line_first_word_index>:$:<, current_line_first_word>:$:<",
                current_line_first_word_index,
                current_line_first_word,
            )

            if current_line_leading_space_index == current_line_first_word_index:
                tabified_start_index, _ = ParserHelper.extract_spaces_from_end(
                    adj_tabified_text, stop_character_in_tabified_index
                )
            else:
                assert current_line_first_word is not None
                tabified_start_index = InlineProcessor.__pdff(
                    current_line_source_text,
                    current_line_first_word,
                    current_line_leading_space_index,
                    adj_tabified_text,
                    stop_character_in_tabified_index,
                    current_line_leading_space,
                )
            return adj_tabified_text[
                tabified_start_index:stop_character_in_tabified_index
            ]

        ex_original_line, _ = ParserHelper.find_detabify_string_ex(
            adj_tabified_text, current_line_source_text
        )
        assert ex_original_line is not None
        return ex_original_line

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __pdff(
        current_line_source_text: str,
        current_line_first_word: str,
        current_line_leading_space_index: Optional[int],
        adj_tabified_text: str,
        stop_character_in_tabified_index: int,
        current_line_leading_space: Optional[str],
    ) -> int:
        first_word_index = current_line_source_text.rfind(current_line_first_word)
        POGGER.debug("first_word_index>:$:<", first_word_index)
        first_word_count = 0
        while (
            first_word_index != current_line_leading_space_index
            and first_word_index > 0
        ):
            first_word_index = current_line_source_text.rfind(
                current_line_first_word, 0, first_word_index - 1
            )
            POGGER.debug("first_word_index>:$:<", first_word_index)
            first_word_count += 1
        POGGER.debug("first_word_count>:$:<", first_word_count)
        assert first_word_index == current_line_leading_space_index

        tabified_start_index = adj_tabified_text.rfind(
            current_line_first_word, 0, stop_character_in_tabified_index
        )
        POGGER.debug(
            "tabified_start_index=$,stop=$..>:$:<",
            tabified_start_index,
            stop_character_in_tabified_index,
            adj_tabified_text[tabified_start_index:stop_character_in_tabified_index],
        )
        for _ in range(first_word_count):
            tabified_start_index = adj_tabified_text.rfind(
                current_line_first_word, 0, tabified_start_index - 1
            )
            POGGER.debug(
                "tabified_start_index=$,stop=$..>:$:<",
                tabified_start_index,
                stop_character_in_tabified_index,
                adj_tabified_text[
                    tabified_start_index:stop_character_in_tabified_index
                ],
            )
            assert tabified_start_index <= stop_character_in_tabified_index

        if current_line_leading_space:
            POGGER.debug(
                "adj_tabified_text[$:]>:$:<",
                tabified_start_index,
                adj_tabified_text[tabified_start_index:],
            )
            tabified_start_index, _ = ParserHelper.extract_spaces_from_end(
                adj_tabified_text, tabified_start_index
            )
            POGGER.debug(
                "adj_tabified_text[$:]>:$:<",
                tabified_start_index,
                adj_tabified_text[tabified_start_index:],
            )

        assert tabified_start_index is not None
        return tabified_start_index

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __handle_next_special_character(
        source_text: str,
        next_index: int,
        inline_request: InlineRequest,
        line_number: int,
        column_number: int,
        coalesced_stack: List[MarkdownToken],
        inline_response: InlineResponse,
        remaining_line: str,
        end_string: Optional[str],
        current_string: str,
        inline_blocks: List[MarkdownToken],
        is_setext: bool,
        whitespace_to_recombine: Optional[str],
        para_owner: Optional[ParagraphMarkdownToken],
        tabified_text: Optional[str],
        tabified_remaining_line: Optional[str],
    ) -> Tuple[
        InlineResponse,
        int,
        int,
        bool,
        bool,
        Optional[str],
        str,
        Optional[str],
        str,
        bool,
        Optional[str],
    ]:

        if source_text[next_index] in InlineProcessor.__inline_character_handlers:
            whitespace_to_add, was_new_line = None, False
            (
                inline_response,
                line_number,
                column_number,
                was_column_number_reset,
                did_line_number_change,
            ) = InlineProcessor.__process_inline_handled_character(
                source_text,
                next_index,
                inline_request,
                line_number,
                column_number,
                coalesced_stack,
            )
        else:
            was_column_number_reset, did_line_number_change = False, False
            (
                whitespace_to_add,
                remaining_line,
                end_string,
                current_string,
                was_new_line,
                tabified_remaining_line,
            ) = InlineProcessor.__process_inline_new_line(
                source_text,
                next_index,
                inline_response,
                remaining_line,
                end_string,
                current_string,
                inline_blocks,
                is_setext,
                line_number,
                column_number,
                coalesced_stack,
                whitespace_to_recombine,
                para_owner,
                tabified_text,
                inline_request,
                tabified_remaining_line,
            )
        return (
            inline_response,
            line_number,
            column_number,
            was_column_number_reset,
            did_line_number_change,
            whitespace_to_add,
            remaining_line,
            end_string,
            current_string,
            was_new_line,
            tabified_remaining_line,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __cleanup_after_handling(
        inline_response: InlineResponse,
        current_string: str,
        current_string_unresolved: str,
        remaining_line: str,
        tabified_remaining_line: Optional[str],
        reset_current_string: bool,
        end_string: Optional[str],
    ) -> Tuple[bool, str, Optional[str], str, str]:
        # POGGER.debug(
        #     "new_string-->$<--",
        #     inline_response.new_string,
        # )
        # POGGER.debug("new_index-->$<--", inline_response.new_index)
        # POGGER.debug(
        #     "new_tokens-->$<--",
        #     inline_response.new_tokens,
        # )
        # POGGER.debug(
        #     "new_string_unresolved-->$<--",
        #     inline_response.new_string_unresolved,
        # )
        # POGGER.debug(
        #     "consume_rest_of_line-->$<--",
        #     inline_response.consume_rest_of_line,
        # )
        # POGGER.debug(
        #     "original_string-->$<--",
        #     inline_response.original_string,
        # )

        if inline_response.consume_rest_of_line:
            # POGGER.debug("consume_rest_of_line>>$<", remaining_line)
            (
                inline_response.new_string,
                inline_response.new_tokens,
                reset_current_string,
                remaining_line,
                end_string,
            ) = ("", [], True, "", None)
            # POGGER.debug(
            #     "9<<end_string<<$<<",
            #     end_string,
            # )
        else:
            # POGGER.debug("append_rest_of_line>>rem>>$<", remaining_line)
            # POGGER.debug("append_rest_of_line>>cur>>$<", current_string)
            # POGGER.debug(
            #     "append_rest_of_line>>cur_un>>$<", current_string_unresolved
            # )
            proper_remaining_line = tabified_remaining_line or remaining_line
            current_string, current_string_unresolved = (
                InlineHelper.append_text(
                    current_string,
                    proper_remaining_line,
                ),
                InlineHelper.append_text(
                    current_string_unresolved, proper_remaining_line
                ),
            )
        return (
            reset_current_string,
            remaining_line,
            end_string,
            current_string,
            current_string_unresolved,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __fix_variables_before_next_loop(
        reset_current_string: bool,
        current_string: str,
        current_string_unresolved: str,
        inline_blocks: List[MarkdownToken],
        old_inline_blocks_count: int,
        old_inline_blocks_last_token: Optional[MarkdownToken],
        last_line_number: int,
        last_column_number: int,
        line_number: int,
        column_number: int,
    ) -> Tuple[str, str, int, int]:
        # POGGER.debug(
        #     "starting_whitespace>>$<<",
        #     starting_whitespace,
        # )
        # POGGER.debug(
        #     "inline_blocks>>$<<",
        #     inline_blocks,
        # )
        # POGGER.debug("reset_current_string>>$<<", reset_current_string)

        if reset_current_string:
            current_string, current_string_unresolved = "", ""
        # POGGER.debug("pos>>$,$<<", line_number, column_number)
        # POGGER.debug("last>>$,$<<", last_line_number, last_column_number)

        # POGGER.debug(
        #     "old>>$>>now>>$<<",
        #     old_inline_blocks_count,
        #     inline_blocks_size,
        # )
        if old_inline_blocks_count != len(inline_blocks) or (
            old_inline_blocks_last_token
            and old_inline_blocks_last_token != inline_blocks[-1]
        ):
            last_line_number, last_column_number = line_number, column_number
        # POGGER.debug("last>>$,$<<", last_line_number, last_column_number)
        # POGGER.debug(
        #     ">>Token_start>>$,$<<",
        #     last_line_number,
        #     last_column_number,
        # )
        return (
            current_string,
            current_string_unresolved,
            last_line_number,
            last_column_number,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __adjust_line_and_column_number(
        was_new_line: bool,
        coalesced_stack: List[MarkdownToken],
        line_number: int,
        column_number: int,
        fold_space: Optional[List[str]],
        remaining_line: str,
        did_line_number_change: bool,
        was_column_number_reset: bool,
    ) -> Tuple[int, int, Optional[List[str]]]:
        # POGGER.debug(
        #     "l/c(before)>>$,$<<",
        #     line_number,
        #     column_number,
        # )
        # POGGER.debug("l/c(was_new_line)>>$<<", was_new_line)
        if was_new_line:
            # POGGER.debug("l/c(before)>>newline")
            column_number = 1
            if coalesced_stack and coalesced_stack[-1].is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, coalesced_stack[-1])
                POGGER.debug(
                    "coalesced_list[-1]..leading_text_index=$",
                    block_quote_token.leading_text_index,
                )
                assert block_quote_token.leading_spaces is not None
                split_leading_spaces = block_quote_token.leading_spaces.split(
                    ParserHelper.newline_character
                )
                selected_split_length = len(
                    split_leading_spaces[block_quote_token.leading_text_index]
                )
                # POGGER.debug("l/c(before)>>newline-->$", selected_split_length)
                column_number += selected_split_length

            line_number += 1
            assert fold_space
            # POGGER.debug("fold_space(before)>>$<<", fold_space)
            fold_space = fold_space[1:]
            # POGGER.debug("fold_space(after)>>$<<", fold_space)
            column_number += len(fold_space[0])
        elif not was_column_number_reset:
            column_number += len(remaining_line)
        else:
            assert did_line_number_change
            if coalesced_stack and coalesced_stack[-1].is_block_quote_start:
                block_quote_token = cast(BlockQuoteMarkdownToken, coalesced_stack[-1])
                POGGER.debug(
                    "coalesced_list[-1].leading_text_index=$",
                    block_quote_token.leading_text_index,
                )
                assert block_quote_token.leading_spaces is not None
                split_leading_spaces = block_quote_token.leading_spaces.split(
                    ParserHelper.newline_character
                )
                selected_split_length = len(
                    split_leading_spaces[block_quote_token.leading_text_index]
                )
                # POGGER.debug("l/c(before)>>newline-->$", selected_split_length)
                column_number += selected_split_length
        # POGGER.debug(
        #     "l/c(after)>>$,$<<",
        #     line_number,
        #     column_number,
        # )
        return line_number, column_number, fold_space

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_new_text_token(
        inline_response: InlineResponse,
        current_string: str,
        inline_blocks: List[MarkdownToken],
        starting_whitespace: str,
        end_string: Optional[str],
        last_line_number: int,
        last_column_number: int,
        reset_current_string: bool,
    ) -> Tuple[bool, str, Optional[str]]:
        # POGGER.debug(
        #     "current_string>>$<<",
        #     current_string,
        # )
        # POGGER.debug(
        #     "current_string_unresolved>>$<<",
        #     current_string_unresolved,
        # )
        # POGGER.debug(
        #     "inline_blocks>>$<<",
        #     inline_blocks,
        # )
        # POGGER.debug(
        #     "inline_response.new_tokens>>$<<",
        #     inline_response.new_tokens,
        # )
        # POGGER.debug(
        #     "starting_whitespace>>$<<",
        #     starting_whitespace,
        # )
        if inline_response.new_tokens:
            if current_string:
                # POGGER.debug(">>>text1")
                inline_blocks.append(
                    TextMarkdownToken(
                        current_string,
                        starting_whitespace,
                        end_whitespace=end_string,
                        line_number=last_line_number,
                        column_number=last_column_number,
                    )
                )
                # POGGER.debug("new Text>>$>>", inline_blocks)
                reset_current_string, starting_whitespace, end_string = (
                    True,
                    "",
                    None,
                )
                # POGGER.debug(
                #     "4<<end_string<<$<<",
                #     end_string,
                # )
            elif starting_whitespace:
                # POGGER.debug(">>>starting whitespace")
                inline_blocks.append(
                    TextMarkdownToken(
                        "",
                        ParserHelper.create_replace_with_nothing_marker(
                            starting_whitespace
                        ),
                        line_number=last_line_number,
                        column_number=last_column_number,
                    )
                )
                # POGGER.debug("new Text>>$>>", inline_blocks)
                starting_whitespace = ""

            inline_blocks.extend(inline_response.new_tokens)
        return reset_current_string, starting_whitespace, end_string

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_inline_handled_character(
        source_text: str,
        next_index: int,
        inline_request: InlineRequest,
        line_number: int,
        column_number: int,
        coalesced_stack: List[MarkdownToken],
    ) -> Tuple[InlineResponse, int, int, bool, bool]:
        # POGGER.debug(
        #     "handler(before)>>$<<",
        #     source_text[next_index],
        # )
        # POGGER.debug(
        #     "current_string_unresolved>>$<<",
        #     current_string_unresolved,
        # )
        # POGGER.debug("remaining_line>>$<<", remaining_line)
        # POGGER.debug("line_number>>$<<", line_number)
        # POGGER.debug("column_number>>$<<", column_number)
        proc_fn = InlineProcessor.__inline_character_handlers[source_text[next_index]]
        assert proc_fn is not None
        inline_response = proc_fn(inline_request)
        # POGGER.debug(
        #     "handler(after)>>$<<",
        #     source_text[next_index],
        # )
        # POGGER.debug(
        #     "delta_line_number>>$<<", inline_response.delta_line_number
        # )
        # POGGER.debug("delta_column>>$<<", inline_response.delta_column_number)

        line_number += inline_response.delta_line_number
        did_line_number_change = bool(inline_response.delta_line_number)
        was_column_number_reset = inline_response.delta_column_number < 0
        column_number = (
            -inline_response.delta_column_number
            if was_column_number_reset
            else column_number + inline_response.delta_column_number
        )

        if (
            coalesced_stack
            and coalesced_stack[-1].is_block_quote_start
            and (
                inline_response.new_tokens
                and inline_response.new_tokens[-1].is_inline_raw_html
            )
        ):
            raw_html_token = cast(RawHtmlMarkdownToken, inline_response.new_tokens[-1])
            newline_count = ParserHelper.count_newlines_in_text(raw_html_token.raw_tag)
            POGGER.debug("newline_count in raw-html>>$>", newline_count)

            block_quote_token = cast(BlockQuoteMarkdownToken, coalesced_stack[-1])
            block_quote_token.leading_text_index += newline_count

            # POGGER.debug("line_number>>$>",line_number)
            # POGGER.debug("column_number>>$>", column_number)
            # POGGER.debug("handler(after)>>$,$<<", line_number, column_number)
            # POGGER.debug(
            #     "handler(after)>>new_tokens>>$<<",
            #     inline_response.new_tokens,
            # )
        return (
            inline_response,
            line_number,
            column_number,
            was_column_number_reset,
            did_line_number_change,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __process_inline_new_line(
        source_text: str,
        next_index: int,
        inline_response: InlineResponse,
        remaining_line: str,
        end_string: Optional[str],
        current_string: str,
        inline_blocks: List[MarkdownToken],
        is_setext: bool,
        line_number: int,
        column_number: int,
        coalesced_stack: List[MarkdownToken],
        whitespace_to_recombine: Optional[str],
        para_owner: Optional[ParagraphMarkdownToken],
        tabified_text: Optional[str],
        inline_request: InlineRequest,
        tabified_remaining_line: Optional[str],
    ) -> Tuple[Optional[str], str, Optional[str], str, bool, Optional[str]]:

        assert source_text[next_index] == ParserHelper.newline_character
        # POGGER.debug("end_string>:$:<", end_string)
        # POGGER.debug("remaining_line>:$:<", remaining_line)
        # POGGER.debug("tabified_text>:$:<", tabified_text)
        # POGGER.debug(
        #     "inline_request.tabified_remaining_line>:$:<",
        #     inline_request.tabified_remaining_line,
        # )
        (
            inline_response.new_string,
            whitespace_to_add,
            inline_response.new_tokens,
            remaining_line,
            end_string,
            current_string,
        ) = InlineHelper.handle_line_end(
            remaining_line,
            end_string,
            current_string,
            inline_blocks,
            is_setext,
            line_number,
            column_number,
            coalesced_stack,
            tabified_text,
            inline_request,
        )
        inline_response.new_index = next_index + 1
        # POGGER.debug("end_string>:$:<", end_string)
        # POGGER.debug("remaining_line>:$:<", remaining_line)
        # POGGER.debug(
        #     "handle_line_end>>new_tokens>>$<<",
        #     inline_response.new_tokens,
        # )

        if not inline_response.new_tokens:
            # POGGER.debug("ws")
            end_string = InlineProcessor.__add_recombined_whitespace(
                bool(whitespace_to_recombine),
                source_text,
                inline_response,
                end_string,
                is_setext,
            )
            # POGGER.debug(
            #     "3<<end_string<<$<<",
            #     end_string,
            # )
            # POGGER.debug("ws>$<", end_string)
        # POGGER.debug(
        #     "handle_line_end>>$<<", source_text[inline_response.new_index :]
        # )
        # POGGER.debug(
        #     "end_string(after)>>$<<",
        #     end_string,
        # )
        # POGGER.debug(">>line_number>>$<<", line_number)
        # POGGER.debug(">>column_number>>$<<", column_number)
        if para_owner:
            # POGGER.debug(">>para_owner.rehydrate_index>>$<<", para_owner.rehydrate_index)
            para_owner.rehydrate_index += 1
            # POGGER.debug(">>para_owner.rehydrate_index>>$<<", para_owner.rehydrate_index)

        if tabified_remaining_line and end_string and len(end_string) > 1:
            assert end_string is not None
            # POGGER.debug("end_string>$<", end_string)
            # POGGER.debug("tabified_remaining_line>$<", tabified_remaining_line)
            assert end_string[-1] == "\n"
            end_suffix = end_string[:-1]
            newline_index = end_suffix.rfind("\n")
            if newline_index != -1:
                end_suffix = end_suffix[newline_index + 1 :]
            assert tabified_remaining_line.endswith(end_suffix)
            if end_suffix:
                tabified_remaining_line = tabified_remaining_line[: -(len(end_suffix))]
            # POGGER.debug("tabified_remaining_line>$<", tabified_remaining_line)

        return (
            whitespace_to_add,
            remaining_line,
            end_string,
            current_string,
            True,
            tabified_remaining_line,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __add_recombined_whitespace(
        did_recombine: bool,
        source_text: str,
        inline_response: InlineResponse,
        end_string: Optional[str],
        is_setext: bool,
    ) -> Optional[str]:

        POGGER.debug("__arw>>did_recombine>>$>>", did_recombine)
        POGGER.debug(
            "__arw>>end_string>>$>>",
            end_string,
        )
        if did_recombine:
            POGGER.debug(
                "__arw>>source_text>>$>>",
                source_text,
            )
            assert inline_response.new_index is not None
            new_index, extracted_whitespace = ParserHelper.extract_spaces(
                source_text, inline_response.new_index
            )
            POGGER.debug("__arw>>$>>", source_text[: inline_response.new_index])
            POGGER.debug("__arw>>$>>", source_text[inline_response.new_index :])
            POGGER.debug(
                "__arw>>extracted_whitespace>>$>>",
                extracted_whitespace,
            )
            if extracted_whitespace:
                inline_response.new_index = new_index
                assert end_string is not None
                assert is_setext
                end_string = f"{end_string}{extracted_whitespace}{ParserHelper.whitespace_split_character}"
                POGGER.debug(
                    "__arw>>end_string>>$>>",
                    end_string,
                )
        return end_string

    @staticmethod
    # pylint: disable=too-many-arguments
    def __complete_inline_loop(
        source_text: str,
        new_index: Optional[int],
        end_string: Optional[str],
        whitespace_to_add: Optional[str],
        current_string: str,
        current_string_unresolved: str,
        new_string_unresolved: Optional[str],
        new_string: Optional[str],
        original_string: Optional[str],
    ) -> Tuple[Optional[int], int, Optional[str], str, str]:
        # POGGER.debug("5<<end_string<<$<<", end_string)
        # POGGER.debug(
        #     "<<current_string<<$<<",
        #     current_string,
        # )
        # POGGER.debug(
        #     "<<current_string_unresolved<<$<<",
        #     current_string_unresolved,
        # )

        POGGER.debug(
            "__complete_inline_loop--current_string>>$>>",
            current_string,
        )
        POGGER.debug(
            "__complete_inline_loop--new_string>>$>>",
            new_string,
        )
        POGGER.debug(
            "__complete_inline_loop--new_string_unresolved>>$>>",
            new_string_unresolved,
        )
        POGGER.debug(
            "__complete_inline_loop--original_string>>$>>",
            original_string,
        )

        POGGER.debug(
            "__complete_inline_loop--current_string>>$>>",
            current_string,
        )
        POGGER.debug(
            "__complete_inline_loop--end_string>>$>>",
            end_string,
        )
        POGGER.debug(
            "__complete_inline_loop--whitespace_to_add>>$>>",
            whitespace_to_add,
        )
        assert new_string is not None
        if original_string is not None:
            assert not new_string_unresolved or new_string_unresolved == original_string
            replaced_string = ParserHelper.create_replacement_markers(
                original_string, InlineHelper.append_text("", new_string)
            )
            current_string = f"{current_string}{replaced_string}"
        else:
            current_string = InlineHelper.append_text(current_string, new_string)
        POGGER.debug(
            "__complete_inline_loop--current_string>>$>>",
            current_string,
        )

        # POGGER.debug(
        #     "new_string>>$>>",
        #     new_string,
        # )
        POGGER.debug(
            "new_string_unresolved>>$>>",
            new_string_unresolved,
        )
        # POGGER.debug(
        #     "current_string_unresolved>>$>>",
        #     current_string_unresolved,
        # )
        if new_string == ParserHelper.newline_character and end_string:
            split_end_string = end_string.split(ParserHelper.newline_character)
            POGGER.debug(
                "split_end_string>>$>>",
                split_end_string,
            )
            assert len(split_end_string) >= 2
            new_string = split_end_string[len(split_end_string) - 2] + new_string

        current_string_unresolved = (
            f"{current_string_unresolved}{new_string_unresolved}"
            if new_string_unresolved
            else InlineHelper.append_text(current_string_unresolved, new_string)
        )

        POGGER.debug(
            "__complete_inline_loop--current_string_unresolved>>$>>",
            current_string_unresolved,
        )

        start_index = new_index
        assert start_index is not None
        next_index = ParserHelper.index_any_of(
            source_text,
            InlineProcessor.__valid_inline_text_block_sequence_starts,
            start_index,
        )
        # POGGER.debug("6<<end_string<<$<<", end_string)
        # POGGER.debug(
        #     "<<current_string<<$<<",
        #     current_string,
        # )
        # POGGER.debug(
        #     "<<current_string_unresolved<<$<<",
        #     current_string_unresolved,
        # )
        return (
            start_index,
            next_index,
            end_string,
            current_string,
            current_string_unresolved,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    # pylint: disable=too-many-arguments
    def __complete_inline_block_processing(
        inline_blocks: List[MarkdownToken],
        source_text: str,
        start_index: Optional[int],
        current_string: str,
        end_string: Optional[str],
        starting_whitespace: str,
        is_setext: bool,
        line_number: int,
        column_number: int,
        tabified_text: Optional[str],
        newlines_encountered: int,
    ) -> List[MarkdownToken]:
        POGGER.debug("__cibp>inline_blocks>$<", inline_blocks)
        POGGER.debug("__cibp>source_text>$<", source_text)
        POGGER.debug("__cibp>start_index>$<", start_index)
        POGGER.debug("__cibp>current_string>$<", current_string)
        POGGER.debug("__cibp>end_string>$<", end_string)
        POGGER.debug(
            "__cibp>starting_whitespace>$<",
            starting_whitespace,
        )
        POGGER.debug("__cibp>is_setext>$<", is_setext)
        POGGER.debug("__cibp>line_number>$<", line_number)
        POGGER.debug("__cibp>column_number>$<", column_number)

        assert start_index is not None
        if start_index < len(source_text):

            text_to_append = source_text[start_index:]
            POGGER.debug("text_to_append>:$:<", text_to_append)

            POGGER.debug("tabified_text=>:$:<", tabified_text)
            if tabified_text:
                assert tabified_text is not None
                text_to_append = (
                    InlineProcessor.__complete_inline_block_processing_tabified(
                        source_text, start_index, tabified_text, newlines_encountered
                    )
                )
                POGGER.debug("text_to_append>:$:<", text_to_append)

            POGGER.debug("current_string>:$:<", current_string)
            POGGER.debug("text_to_append>:$:<", text_to_append)
            current_string = InlineHelper.append_text(current_string, text_to_append)
            POGGER.debug("current_string>:$:<", current_string)

        have_processed_once = len(inline_blocks) != 0 or start_index != 0
        if current_string or not have_processed_once:
            (
                current_string,
                end_string,
            ) = InlineProcessor.__complete_inline_block_processing_build_token(
                current_string,
                end_string,
                starting_whitespace,
                is_setext,
                inline_blocks,
                line_number,
                column_number,
            )
        POGGER.debug(">>$<<", inline_blocks)

        EmphasisHelper.resolve_inline_emphasis(inline_blocks, None)
        return inline_blocks

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals
    @staticmethod
    def __complete_inline_block_processing_tabified(
        source_text: str,
        start_index: int,
        tabified_text: str,
        newlines_encountered: int,
    ) -> str:

        source_text_spaces_index, source_text_spaces = ParserHelper.extract_spaces(
            source_text, start_index
        )
        POGGER.debug(
            "source_text_spaces_index=>:$:<, source_text_spaces=>:$:<",
            source_text_spaces_index,
            source_text_spaces,
        )
        assert source_text_spaces_index is not None
        (
            source_text_word_index,
            source_text_word,
        ) = ParserHelper.collect_until_one_of_characters(
            source_text, source_text_spaces_index, " \t"
        )
        POGGER.debug(
            "source_text_word_index=>:$:<, source_text_word=>:$:<",
            source_text_word_index,
            source_text_word,
        )
        assert source_text_word is not None

        current_line_source_text, current_line_start_index = InlineProcessor.__xdf(
            source_text, newlines_encountered
        )
        POGGER.debug("current_line_source_text>:$:<", current_line_source_text)
        POGGER.debug("current_line_start_index>:$:<", current_line_start_index)

        find_word_count = 0
        word_index = current_line_source_text.find(source_text_word, 0)
        adj_word_index = word_index + current_line_start_index
        POGGER.debug(
            "[$]-->current_line_source_text[$:]>:$:<",
            find_word_count,
            word_index,
            current_line_source_text[word_index:],
        )
        POGGER.debug(
            "adj_word_index=$ != source_text_spaces_index=$",
            adj_word_index,
            source_text_spaces_index,
        )
        while adj_word_index != source_text_spaces_index:
            find_word_count += 1
            word_index = current_line_source_text.find(source_text_word, word_index + 1)
            adj_word_index = word_index + current_line_start_index
            POGGER.debug(
                "[$]-->current_line_source_text[$:]>:$:<",
                find_word_count,
                word_index,
                current_line_source_text[word_index:],
            )
            POGGER.debug(
                "adj_word_index=$ != source_text_spaces_index=$",
                adj_word_index,
                source_text_spaces_index,
            )
        POGGER.debug(
            "[$]-->current_line_source_text[$:]>:$:<",
            find_word_count,
            word_index,
            current_line_source_text[word_index:],
        )

        current_line_tabified_text, _ = InlineProcessor.__xdf(
            tabified_text, newlines_encountered
        )
        POGGER.debug("current_line_tabified_text>:$:<", current_line_tabified_text)

        POGGER.debug("source_text_word>:$:<", source_text_word)
        found_word_index = current_line_tabified_text.find(source_text_word)
        POGGER.debug(
            "[$]-->current_line_source_text[$:]>:$:<",
            0,
            found_word_index,
            current_line_tabified_text[found_word_index:],
        )
        for found_word_count in range(find_word_count):
            found_word_index = current_line_tabified_text.find(
                source_text_word, found_word_index + 1
            )
            POGGER.debug(
                "[$]-->current_line_source_text[$:]>:$:<",
                found_word_count,
                found_word_index,
                current_line_tabified_text[found_word_index:],
            )
            assert found_word_index != -1

        if source_text_spaces:
            POGGER.debug(
                "current_line_source_text[$:]>:$:<",
                found_word_index,
                current_line_tabified_text[found_word_index:],
            )
            found_word_index, _ = ParserHelper.extract_spaces_from_end(
                current_line_tabified_text, found_word_index
            )
            POGGER.debug(
                "current_line_source_text[$:]>:$:<",
                found_word_index,
                current_line_tabified_text[found_word_index:],
            )

        return current_line_tabified_text[found_word_index:]

    # pylint: enable=too-many-locals

    @staticmethod
    def __xdf(tabified_text: str, newlines_encountered: int) -> Tuple[str, int]:

        # POGGER.debug("newlines_encountered=>:$:<", newlines_encountered)
        # POGGER.debug("tabified_text>:$:<", tabified_text)
        start_index = 0
        for _ in range(newlines_encountered):
            next_index = tabified_text.find("\n", start_index)
            assert next_index != -1
            start_index = next_index + 1
        # POGGER.debug("start_index>:$:<", start_index)
        # POGGER.debug("tabified_text[start_index:]>:$:<", tabified_text[start_index:])

        next_index = tabified_text.find("\n", start_index)
        # POGGER.debug("next_index>:$:<", next_index)
        assert next_index == -1
        # if next_index != -1:
        #     start_index = next_index + 1

        return tabified_text[start_index:], start_index

    # pylint: disable=too-many-arguments
    @staticmethod
    def __complete_inline_block_processing_build_token(
        current_string: str,
        end_string: Optional[str],
        starting_whitespace: str,
        is_setext: bool,
        inline_blocks: List[MarkdownToken],
        line_number: int,
        column_number: int,
    ) -> Tuple[str, Optional[str]]:
        POGGER.debug("__cibp>current_string>$<", current_string)
        POGGER.debug("__cibp>starting_whitespace>$<", starting_whitespace)
        if (
            is_setext
            and end_string is None
            and (inline_blocks and inline_blocks[-1].is_inline_hard_break)
        ):
            new_index, ex_ws = ParserHelper.extract_spaces(current_string, 0)
            POGGER.debug("__cibp>new_index>$<", new_index)
            POGGER.debug("__cibp>b>$<", ex_ws)
            if new_index:
                end_string = f"{ex_ws}{ParserHelper.whitespace_split_character}"
                current_string = current_string[new_index:]
        POGGER.debug("__cibp>end_string>$<", end_string)
        inline_blocks.append(
            TextMarkdownToken(
                current_string,
                starting_whitespace,
                end_whitespace=end_string,
                line_number=line_number,
                column_number=column_number,
            )
        )
        return current_string, end_string

    # pylint: enable=too-many-arguments
