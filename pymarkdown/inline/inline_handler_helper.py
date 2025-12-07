"""
Module to orchestrate the handling of the different inline elements.
"""

import logging
from typing import Dict, List, Optional, Set, Tuple, cast

from typing_extensions import Protocol

from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.extension_manager.extension_manager import ExtensionManager
from pymarkdown.extensions.extended_autolinks import MarkdownExtendedAutolinksExtension
from pymarkdown.extensions.task_list_items import TaskListToken
from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.inline.emphasis_helper import EmphasisHelper
from pymarkdown.inline.inline_autolink_helper import InlineAutoLinkHelper
from pymarkdown.inline.inline_backslash_helper import InlineBackslashHelper
from pymarkdown.inline.inline_backtick_helper import InlineBacktickHelper
from pymarkdown.inline.inline_character_reference_helper import (
    InlineCharacterReferenceHelper,
)
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.inline.inline_response import InlineResponse
from pymarkdown.links.link_parse_helper import LinkParseHelper
from pymarkdown.links.link_search_helper import LinkSearchHelper
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.reference_markdown_token import ReferenceMarkdownToken
from pymarkdown.tokens.special_text_markdown_token import SpecialTextMarkdownToken

# pylint: disable=too-many-lines

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class InlineHandlerProtocol(Protocol):
    """
    Protocol to handle the various inline sequences.
    """

    def __call__(  # noqa: E704
        self,
        parser_properties: ParseBlockPassProperties,
        inline_request: InlineRequest,
    ) -> InlineResponse: ...  # pragma: no cover


# pylint: enable=too-few-public-methods


class InlineHandlerHelper:
    """
    Class to orchestrate the handling of the different inline elements.
    """

    valid_inline_text_block_sequence_starts = ""
    __valid_inline_simple_text_block_sequence_starts = ""

    __inline_character_handlers: Dict[str, InlineHandlerProtocol] = {}
    __inline_simple_character_handlers: Dict[str, InlineHandlerProtocol] = {}

    __inline_processing_needed = ""

    @staticmethod
    def initialize(extension_manager: ExtensionManager) -> None:
        """
        Initialize the inline processor subsystem.
        """
        EmphasisHelper.initialize(extension_manager)
        InlineHandlerHelper.__inline_processing_needed = (
            f"{LinkParseHelper.link_label_start}{LinkParseHelper.link_label_end}"
        )
        InlineHandlerHelper.__inline_processing_needed += (
            EmphasisHelper.get_inline_emphasis()
        )

        InlineHandlerHelper.__inline_character_handlers = {}
        InlineHandlerHelper.__inline_simple_character_handlers = {}
        InlineHandlerHelper.valid_inline_text_block_sequence_starts = (
            ParserHelper.newline_character
        )
        InlineHandlerHelper.__valid_inline_simple_text_block_sequence_starts = (
            ParserHelper.newline_character
        )

        InlineHandlerHelper.register_handlers(
            InlineBacktickHelper.code_span_bounds,
            InlineBacktickHelper.handle_inline_backtick,
        )
        InlineHandlerHelper.register_handlers(
            InlineBackslashHelper.backslash_character,
            InlineBackslashHelper.handle_inline_backslash,
            is_simple_handler=True,
        )
        InlineHandlerHelper.register_handlers(
            InlineCharacterReferenceHelper.character_reference_start_character,
            InlineCharacterReferenceHelper.handle_character_reference,
            is_simple_handler=True,
        )
        InlineHandlerHelper.register_handlers(
            InlineAutoLinkHelper.angle_bracket_start,
            InlineAutoLinkHelper.handle_angle_brackets,
        )
        for i in InlineHandlerHelper.__inline_processing_needed:
            InlineHandlerHelper.register_handlers(
                i, InlineHandlerHelper.__handle_inline_special_single_character
            )
        InlineHandlerHelper.register_handlers(
            LinkSearchHelper.image_start_sequence[0],
            InlineHandlerHelper.__handle_inline_image_link_start_character,
        )
        for i in ParserHelper.valid_characters_to_escape():
            InlineHandlerHelper.register_handlers(
                i, InlineHandlerHelper.__handle_inline_control_character
            )
        if extension_manager.is_extended_autolinks_enabled:
            InlineHandlerHelper.register_handlers(
                "h",
                MarkdownExtendedAutolinksExtension.handle_http_autolink,
            )
            InlineHandlerHelper.register_handlers(
                "w",
                MarkdownExtendedAutolinksExtension.handle_www_autolink,
            )
            InlineHandlerHelper.register_handlers(
                "@",
                MarkdownExtendedAutolinksExtension.handle_email_autolink,
            )
            InlineHandlerHelper.register_handlers(
                "x",
                MarkdownExtendedAutolinksExtension.handle_email_autolink,
            )
            InlineHandlerHelper.register_handlers(
                "m",
                MarkdownExtendedAutolinksExtension.handle_email_autolink,
            )

    @staticmethod
    def __handle_inline_control_character(
        parser_properties: ParseBlockPassProperties,
        inline_request: InlineRequest,
    ) -> InlineResponse:
        """
        Registered handler.
        """
        _ = parser_properties

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
    def has_handler(inline_character: str) -> bool:
        """
        Check to see if a handler is registered.
        """
        return inline_character in InlineHandlerHelper.__inline_character_handlers

    @staticmethod
    def __get_handler(
        inline_character: str,
    ) -> InlineHandlerProtocol:
        return InlineHandlerHelper.__inline_character_handlers[inline_character]

    @staticmethod
    def register_handlers(
        inline_character: str,
        start_token_handler: InlineHandlerProtocol,
        is_simple_handler: bool = False,
    ) -> None:
        """
        Register the handlers necessary to deal with token's start and end.
        """
        InlineHandlerHelper.__inline_character_handlers[inline_character] = (
            start_token_handler
        )
        InlineHandlerHelper.valid_inline_text_block_sequence_starts += inline_character
        if is_simple_handler:
            InlineHandlerHelper.__inline_simple_character_handlers[inline_character] = (
                start_token_handler
            )
            InlineHandlerHelper.__valid_inline_simple_text_block_sequence_starts += (
                inline_character
            )

    @staticmethod
    def process_simple_inline_fn(
        parser_properties: ParseBlockPassProperties, source_text: str
    ) -> str:
        """
        Handle a simple processing of inline text for simple replacements.
        """

        start_index, processed_parts = 0, []
        next_index = ParserHelper.index_any_of(
            source_text,
            InlineHandlerHelper.__valid_inline_simple_text_block_sequence_starts,
            start_index,
        )
        while next_index != -1:
            processed_parts.append(source_text[start_index:next_index])
            inline_request = InlineRequest(source_text, next_index)
            if (
                source_text[next_index]
                in InlineHandlerHelper.__inline_character_handlers
            ):
                proc_fn = InlineHandlerHelper.__inline_character_handlers[
                    source_text[next_index]
                ]
                # assert proc_fn is not None
                inline_response = proc_fn(parser_properties, inline_request)
                assert (
                    inline_response.new_string is not None
                ), "new_string should be defined by this point."
                assert (
                    inline_response.new_index is not None
                ), "new_index should be defined by this point."
                processed_parts.append(inline_response.new_string)
                start_index = inline_response.new_index
            else:
                processed_parts.append(ParserHelper.newline_character)
                start_index = next_index + 1
            next_index = ParserHelper.index_any_of(
                source_text,
                InlineHandlerHelper.__valid_inline_simple_text_block_sequence_starts,
                start_index,
            )

        processed_parts.append(source_text[start_index:])
        return "".join(processed_parts)

    @staticmethod
    def __handle_inline_special_single_character(
        parser_properties: ParseBlockPassProperties,
        inline_request: InlineRequest,
    ) -> InlineResponse:
        """
        Registered handler.
        """
        return InlineHandlerHelper.__handle_inline_special(
            parser_properties,
            inline_request,
            1,
            inline_request.last_container_token,
        )

    @staticmethod
    def __handle_inline_special(
        parser_properties: ParseBlockPassProperties,
        inline_request: InlineRequest,
        special_length: int,
        last_container_token: Optional[MarkdownToken],
    ) -> InlineResponse:
        """
        Handle the collection of special inline characters for later processing.
        """
        inline_response = InlineResponse()
        inline_response.new_string = ""

        assert (
            inline_request.line_number is not None
            and inline_request.column_number is not None
            and inline_request.remaining_line is not None
        ), "These fields must be defined by now."

        POGGER.debug(">>tabified_text>:$:<", inline_request.tabified_text)

        POGGER.debug(">>remaining_line>>$<<", inline_request.remaining_line)
        POGGER.debug(">>column_number>>$<<", inline_request.column_number)
        column_number = inline_request.column_number + len(
            inline_request.remaining_line
        )
        POGGER.debug(">>column_number>>$<<", column_number)

        (
            special_sequence,
            inline_response.delta_column_number,
            inline_response.new_index,
            surrounding_whitespace_pair,
            is_active,
            inline_response.new_tokens,
            inline_response.consume_rest_of_line,
            inline_response.delta_line_number,
        ) = InlineHandlerHelper.__handle_inline_special_character(
            parser_properties,
            inline_request,
            special_length,
            last_container_token,
        )
        if not inline_response.new_tokens:
            POGGER.debug(">>create>>$,$<<", inline_request.line_number, column_number)
            inline_response.new_tokens = [
                SpecialTextMarkdownToken(
                    special_sequence,
                    inline_response.delta_column_number,
                    surrounding_whitespace_pair[0],
                    surrounding_whitespace_pair[1],
                    is_active,
                    inline_request.line_number,
                    column_number,
                )
            ]

        POGGER.debug(">>delta_line>>$<<", inline_response.delta_line_number)
        POGGER.debug(">>repeat_count>>$<<", inline_response.delta_column_number)
        return inline_response

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_inline_special_character_task_list(
        parser_properties: ParseBlockPassProperties,
        para_owner: Optional[ParagraphMarkdownToken],
        special_sequence: str,
        next_index: int,
        source_text: str,
        last_container_token: Optional[MarkdownToken],
    ) -> Tuple[int, Optional[MarkdownToken]]:
        repeat_count = 0
        new_token = None
        if para_owner is None or not parser_properties.is_task_lists_enabled:
            return repeat_count, new_token
        if not (last_container_token and last_container_token.is_list_start):
            return repeat_count, new_token
        if last_container_token.line_number != para_owner.line_number:
            last_list_token = cast(ListStartMarkdownToken, last_container_token)
            if (
                last_list_token.last_new_list_token is None
                or last_list_token.last_new_list_token.line_number
                != para_owner.line_number
            ):
                return repeat_count, new_token

        if special_sequence == "[" and next_index == 0 and len(source_text) >= 4:
            is_valid_check_character = source_text[1] in [" ", "X", "x"]
            is_valid_close_character = source_text[2] == "]"
            is_followed_by_whitespace = ParserHelper.is_character_at_index_whitespace(
                source_text, 3
            )
            if (
                is_valid_check_character
                and is_valid_close_character
                and is_followed_by_whitespace
            ):
                repeat_count = 3
                new_token = TaskListToken(
                    source_text[1],
                    line_number=para_owner.line_number,
                    column_number=para_owner.column_number,
                )
        return repeat_count, new_token

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_inline_special_character(
        parser_properties: ParseBlockPassProperties,
        inline_request: InlineRequest,
        special_length: int,
        last_container_token: Optional[MarkdownToken],
    ) -> Tuple[
        str,
        int,
        int,
        Tuple[Optional[str], Optional[str]],
        bool,
        List[MarkdownToken],
        bool,
        int,
    ]:
        assert (
            inline_request.current_string_unresolved is not None
        ), "These fields must be defined by now."

        special_sequence = inline_request.source_text[
            inline_request.next_index : inline_request.next_index + special_length
        ]
        if special_length == 1:
            (
                repeat_count,
                new_token,
            ) = InlineHandlerHelper.__handle_inline_special_character_task_list(
                parser_properties,
                inline_request.para_owner,
                special_sequence,
                inline_request.next_index,
                inline_request.source_text,
                last_container_token,
            )
            new_index = inline_request.next_index + repeat_count
            if new_token is not None:
                return (
                    inline_request.source_text[inline_request.next_index : new_index],
                    repeat_count,
                    new_index,
                    (None, None),
                    True,
                    [new_token],
                    False,
                    0,
                )

            if special_sequence in EmphasisHelper.get_inline_emphasis():
                return InlineHandlerHelper.__handle_inline_special_character_emphasis(
                    inline_request.source_text,
                    inline_request.next_index,
                    special_sequence,
                )
        if special_sequence[0] == LinkParseHelper.link_label_end:
            POGGER.debug(
                "POSSIBLE LINK CLOSE_FOUND($)>>$>>",
                special_length,
                special_sequence,
            )

            return InlineHandlerHelper.__handle_link_label_end(
                parser_properties,
                inline_request,
                special_sequence,
                inline_request.current_string_unresolved,
            )
        return (
            special_sequence,
            special_length,
            inline_request.next_index + special_length,
            (None, None),
            True,
            [],
            False,
            0,
        )

    @staticmethod
    def __handle_inline_special_character_emphasis(
        source_text: str,
        next_index: int,
        special_sequence: str,
    ) -> Tuple[
        str,
        int,
        int,
        Tuple[Optional[str], Optional[str]],
        bool,
        List[MarkdownToken],
        bool,
        int,
    ]:
        repeat_count, new_index = ParserHelper.collect_while_character_verified(
            source_text, next_index, special_sequence
        )
        return (
            source_text[next_index:new_index],
            repeat_count,
            new_index,
            (
                source_text[max(0, next_index - 2) : next_index],
                source_text[new_index : min(len(source_text), new_index + 2)],
            ),
            True,
            [],
            False,
            0,
        )

    @staticmethod
    def __handle_inline_image_link_start_character(
        parser_properties: ParseBlockPassProperties,
        inline_request: InlineRequest,
    ) -> InlineResponse:
        """
        Registered handler.
        """
        if ParserHelper.are_characters_at_index(
            inline_request.source_text,
            inline_request.next_index,
            LinkSearchHelper.image_start_sequence,
        ):
            assert (
                inline_request.line_number is not None
                and inline_request.column_number is not None
                and inline_request.remaining_line is not None
                and inline_request.current_string_unresolved is not None
            ), "These four fields must be defined by now."

            inline_response = InlineHandlerHelper.__handle_inline_special(
                parser_properties,
                inline_request,
                2,
                None,
            )
            assert (
                not inline_response.consume_rest_of_line
            ), "After the processing, make sure we are not just consuming the rest of the line."
        else:
            inline_response = InlineResponse()
            (
                inline_response.new_string,
                inline_response.new_index,
                inline_response.delta_column_number,
            ) = (
                LinkSearchHelper.image_start_sequence[0],
                inline_request.next_index + 1,
                1,
            )
        return inline_response

    @staticmethod
    def __handle_link_label_end(
        parser_properties: ParseBlockPassProperties,
        inline_request: InlineRequest,
        special_sequence: str,
        current_string_unresolved: str,
    ) -> Tuple[
        str,
        int,
        int,
        Tuple[Optional[str], Optional[str]],
        bool,
        List[MarkdownToken],
        bool,
        int,
    ]:
        assert (
            inline_request.remaining_line is not None
        ), "These fields must be defined by now."
        inline_blocks = inline_request.inline_blocks

        POGGER.debug(
            ">>inline_blocks>>$<<",
            inline_blocks,
        )
        POGGER.debug(
            ">>remaining_line>>$<<",
            inline_request.remaining_line,
        )
        POGGER.debug(
            ">>tabified_remaining_line>>$<<",
            inline_request.tabified_remaining_line,
        )
        POGGER.debug(
            ">>current_string_unresolved>>$<<",
            current_string_unresolved,
        )
        POGGER.debug(
            ">>source_text[next_index=$:]>:$:<",
            inline_request.next_index,
            inline_request.source_text[inline_request.next_index :],
        )
        POGGER.debug(
            ">>source_text>:$:<",
            inline_request.source_text,
        )
        POGGER.debug(
            ">>tabified_text>>$<<",
            inline_request.tabified_text,
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
        ) = LinkSearchHelper.look_for_link_or_image(
            parser_properties,
            inline_blocks,
            inline_request.source_text,
            inline_request.next_index,
            inline_request.remaining_line,
            inline_request.tabified_remaining_line,
            current_string_unresolved,
            InlineHandlerHelper.process_simple_inline_fn,
            inline_request.tabified_text,
        )
        POGGER.debug(">>next_index>>$<<", inline_request.next_index)
        POGGER.debug(">>new_index>>$<<", new_index)
        POGGER.debug(
            ">>source_text:new_index>>$<<",
            inline_request.source_text[new_index:],
        )
        POGGER.debug(">>inline_blocks>>$<<", inline_blocks)
        POGGER.debug(">>new_token>>$<<", new_token)
        POGGER.debug(">>source_text>>$<<", inline_request.source_text[new_index:])
        POGGER.debug(">>consume_rest_of_line>>$<<", consume_rest_of_line)
        POGGER.debug(">>old_inline_blocks_count>>$<<", old_inline_blocks_count)

        return InlineHandlerHelper.__handle_link_label_end_calc(
            0,
            new_token,
            inline_blocks,
            new_index,
            inline_request.next_index,
            len(inline_request.remaining_line),
            inline_request.para_owner,
            old_inline_blocks_count,
            old_inline_blocks_last_token,
            is_active,
            consume_rest_of_line,
            special_sequence,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_link_label_end_calc(
        delta_line: int,
        new_token: Optional[MarkdownToken],
        inline_blocks: List[MarkdownToken],
        new_index: int,
        next_index: int,
        remaining_line_size: int,
        para_owner: Optional[ParagraphMarkdownToken],
        old_inline_blocks_count: int,
        old_inline_blocks_last_token: Optional[MarkdownToken],
        is_active: bool,
        consume_rest_of_line: bool,
        special_sequence: str,
    ) -> Tuple[
        str,
        int,
        int,
        Tuple[Optional[str], Optional[str]],
        bool,
        List[MarkdownToken],
        bool,
        int,
    ]:
        repeat_count = 1
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
            ) = InlineHandlerHelper.__calculate_repeat_count_and_delta_line(
                inline_blocks,
                new_token,
                new_index,
                next_index,
                remaining_line_size,
                para_owner,
                delta_line,
            )
        return (
            special_sequence,
            repeat_count,
            new_index,
            (None, None),
            is_active,
            [new_token] if new_token else [],
            consume_rest_of_line,
            delta_line,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def process_inline_handled_character(
        parser_properties: ParseBlockPassProperties,
        source_text: str,
        next_index: int,
        inline_request: InlineRequest,
        line_number: int,
        column_number: int,
        coalesced_stack: List[MarkdownToken],
        pragma_line_numbers : Set[int],
    ) -> Tuple[InlineResponse, int, int, bool, bool]:
        """
        Process the handler specified by the next character.
        """

        proc_fn = InlineHandlerHelper.__get_handler(source_text[next_index])
        # assert proc_fn is not None
        inline_response = proc_fn(parser_properties, inline_request)

        for _ in range(inline_response.delta_line_number):
            line_number += 1
            while line_number in pragma_line_numbers:
                line_number += 1

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

        return (
            inline_response,
            line_number,
            column_number,
            was_column_number_reset,
            did_line_number_change,
        )

    # pylint: enable=too-many-arguments

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
            ) = InlineHandlerHelper.__calculate_link_and_image_deltas(
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
            assert (
                end_token.start_markdown_token
            ), "End markdown tokens should have the starting token."
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
            ) = InlineHandlerHelper.__calculate_link_and_image_deltas(
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
    def __calculate_full_deltas(
        current_token: ReferenceMarkdownToken,
        para_owner: Optional[ParagraphMarkdownToken],
        delta_line: int,
        repeat_count: int,
    ) -> Tuple[int, int]:
        assert (
            current_token.ex_label is not None
        ), "All reference tokens must have a label."
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
    def __calculate_inline_reference_deltas(
        current_token: ReferenceMarkdownToken,
        para_owner: Optional[ParagraphMarkdownToken],
        split_paragraph_lines: Optional[List[str]],
        delta_line: int,
        repeat_count: int,
    ) -> Tuple[int, int]:
        active_link_title = current_token.active_link_title

        assert (
            current_token.before_title_whitespace is not None
        ), "For an inline, this must be defined."
        assert (
            current_token.before_link_whitespace is not None
        ), "For an inline, this must be defined."
        link_part_lengths = [0] * 5
        link_part_lengths[0] = len(current_token.active_link_uri) + len(
            current_token.before_title_whitespace
        )
        if current_token.inline_title_bounding_character:
            assert (
                active_link_title is not None
                and current_token.after_title_whitespace is not None
            ), "If we have an inline link, both these should be defined."

            link_part_lengths[1] = 1
            link_part_lengths[2] = len(active_link_title) + 1
            link_part_lengths[3] = len(current_token.after_title_whitespace)
        POGGER.debug(">>link_part_lengths>>$<<", link_part_lengths)

        (
            link_part_index,
            total_newlines,
        ) = InlineHandlerHelper.__calculate_inline_label(current_token)

        (
            link_part_index,
            delta_line,
            last_spaces,
        ) = InlineHandlerHelper.__calculate_inline_whitespace(
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
        ) = InlineHandlerHelper.__calculate_inline_whitespace(
            current_token.before_title_whitespace,
            "before_title_whitespace",
            1,
            link_part_index,
            delta_line,
            last_spaces,
        )

        assert active_link_title is not None, "For an inline, this must be defined."
        (
            link_part_index,
            delta_line,
            last_spaces,
            new_link_part_length,
        ) = InlineHandlerHelper.__calculate_inline_link_title(
            active_link_title, link_part_index, delta_line, last_spaces
        )
        if new_link_part_length is not None:
            link_part_lengths[2] = new_link_part_length

        assert (
            current_token.after_title_whitespace is not None
        ), "For an inline, this must be defined."
        (
            link_part_index,
            delta_line,
            last_spaces,
        ) = InlineHandlerHelper.__calculate_inline_whitespace(
            current_token.after_title_whitespace,
            "after_title_whitespace",
            4,
            link_part_index,
            delta_line,
            last_spaces,
        )

        return InlineHandlerHelper.__calculate_inline_delta_adjustments(
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
                assert (
                    para_owner is not None
                ), "If we have a paragraph, must have a paragraph token."
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
            split_paragraph_lines: Optional[List[str]] = (
                para_owner.extracted_whitespace.split(ParserHelper.newline_character)
                if para_owner
                else None
            )

            reference_token = cast(ReferenceMarkdownToken, current_token)
            POGGER.debug(">>current_token.label_type>>$<<", reference_token.label_type)
            if reference_token.label_type == Constants.link_type__inline:
                (
                    delta_line,
                    repeat_count,
                ) = InlineHandlerHelper.__calculate_inline_reference_deltas(
                    reference_token,
                    para_owner,
                    split_paragraph_lines,
                    delta_line,
                    repeat_count,
                )
            elif reference_token.label_type == Constants.link_type__full:
                delta_line, repeat_count = InlineHandlerHelper.__calculate_full_deltas(
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
                ) = InlineHandlerHelper.__calculate_shortcut_collapsed_deltas(
                    reference_token, delta_line, repeat_count
                )

        POGGER.debug(">>delta_line>>$<<repeat_count>>$<<", delta_line, repeat_count)
        return delta_line, repeat_count
