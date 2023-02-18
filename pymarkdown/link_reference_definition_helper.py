"""
Link reference definition helper
"""
import logging
from dataclasses import dataclass
from typing import List, Optional, Tuple, cast

from pymarkdown.container_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.leaf_markdown_token import LinkReferenceDefinitionMarkdownToken
from pymarkdown.link_helper import LinkHelper
from pymarkdown.link_reference_info import LinkReferenceInfo
from pymarkdown.link_reference_titles import LinkReferenceTitles
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.requeue_line_info import RequeueLineInfo
from pymarkdown.stack_token import LinkDefinitionStackToken
from pymarkdown.tab_helper import TabHelper

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


@dataclass(frozen=True)
class LinkReferenceDefinitionTuple:
    """
    Class to hold the tuple of information for creating a Link Reference Definition.
    """

    normalized_destination: Optional[str]
    link_titles: LinkReferenceTitles
    link_info: LinkReferenceInfo


class LinkReferenceDefinitionHelper:
    """
    Class to helper with the parsing of link reference definitions.
    """

    __lrd_start_character = "["

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def process_link_reference_definition(
        parser_state: ParserState,
        position_marker: PositionMarker,
        remaining_line_to_parse: str,
        extracted_whitespace: Optional[str],
        unmodified_line_to_parse: str,
        original_stack_depth: int,
        original_document_depth: int,
        original_line: str,
        process_mode: int,
    ) -> Tuple[bool, bool, bool, Optional[RequeueLineInfo], List[MarkdownToken]]:
        """
        Process a link deference definition.  Note, this requires a lot of work to
        handle properly because of partial definitions across lines.
        """

        line_to_parse = position_marker.text_to_parse
        start_index: int = position_marker.index_number
        lines_to_requeue: List[str] = []

        POGGER.debug(">>remaining_line_to_parse>:$:<", remaining_line_to_parse)
        POGGER.debug(">>line_to_parse>:$:<", line_to_parse)
        POGGER.debug(">>start_index>:$:<", start_index)

        (
            line_to_parse,
            unmodified_line_to_parse,
            remaining_line_to_parse,
            start_index,
            is_blank_line,
        ) = LinkReferenceDefinitionHelper.__handle_link_reference_definition_init(
            remaining_line_to_parse,
            line_to_parse,
            start_index,
            original_line,
            unmodified_line_to_parse,
        )

        (
            was_started,
            lrd_stack_token,
            original_stack_depth,
            original_document_depth,
            line_to_parse,
            extracted_whitespace,
            start_index,
        ) = LinkReferenceDefinitionHelper.__handle_link_reference_definition_started(
            parser_state,
            original_stack_depth,
            original_document_depth,
            line_to_parse,
            extracted_whitespace,
            start_index,
        )

        POGGER.debug(">>line_to_parse>:$:<", line_to_parse)
        line_to_parse_size = len(line_to_parse)
        assert start_index is not None

        (
            did_complete_lrd,
            end_lrd_index,
            parsed_lrd_tuple,
            is_blank_line,
            line_to_parse,
        ) = LinkReferenceDefinitionHelper.__handle_link_reference_definition_processing(
            parser_state,
            line_to_parse,
            start_index,
            extracted_whitespace,
            is_blank_line,
            was_started,
            line_to_parse_size,
            remaining_line_to_parse,
            lines_to_requeue,
            unmodified_line_to_parse,
        )
        (
            did_pause_lrd,
            force_ignore_first_as_lrd,
            new_tokens,
        ) = LinkReferenceDefinitionHelper.__determine_continue_or_stop(
            parser_state,
            position_marker,
            was_started,
            remaining_line_to_parse,
            extracted_whitespace,
            unmodified_line_to_parse,
            original_stack_depth,
            original_document_depth,
            end_lrd_index,
            line_to_parse_size,
            is_blank_line,
            did_complete_lrd,
            parsed_lrd_tuple,
            lines_to_requeue,
            process_mode,
        )
        if lines_to_requeue:
            LinkReferenceDefinitionHelper.__prepare_for_requeue(
                parser_state,
                lrd_stack_token,
                did_complete_lrd,
                original_stack_depth,
                original_document_depth,
                lines_to_requeue,
            )
            requeue_line_info = RequeueLineInfo(
                lines_to_requeue, force_ignore_first_as_lrd
            )
        else:
            requeue_line_info = None

        return (
            did_complete_lrd or end_lrd_index != -1,
            did_complete_lrd,
            did_pause_lrd,
            requeue_line_info,
            new_tokens,
        )

    # pylint: enable=too-many-locals, too-many-arguments

    @staticmethod
    def __handle_link_reference_definition_init(
        remaining_line_to_parse: str,
        line_to_parse: str,
        start_index: int,
        original_line: str,
        unmodified_line_to_parse: str,
    ) -> Tuple[str, str, str, int, Optional[bool]]:

        is_blank_line: Optional[bool] = not line_to_parse and not start_index

        POGGER.debug(">>original_line>:$:<", original_line)
        if ParserHelper.tab_character in original_line and not is_blank_line:
            POGGER.debug(">>tabified>:$:<", original_line)

            first_character_to_parse = line_to_parse[start_index]
            POGGER.debug(">>xx>:$:<", first_character_to_parse)
            first_character_to_parse_index = original_line.find(
                first_character_to_parse
            )
            assert first_character_to_parse_index != -1

            line_to_parse = original_line[first_character_to_parse_index:]
            unmodified_line_to_parse = original_line
            remaining_line_to_parse = line_to_parse
            start_index = 0

        POGGER.debug(">>line_to_parse>:$:<", line_to_parse)
        return (
            line_to_parse,
            unmodified_line_to_parse,
            remaining_line_to_parse,
            start_index,
            is_blank_line,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_link_reference_definition_started(
        parser_state: ParserState,
        original_stack_depth: int,
        original_document_depth: int,
        line_to_parse: str,
        extracted_whitespace: Optional[str],
        start_index: int,
    ) -> Tuple[
        bool, Optional[LinkDefinitionStackToken], int, int, str, Optional[str], int
    ]:

        lrd_stack_token: Optional[LinkDefinitionStackToken] = None

        if was_started := parser_state.token_stack[-1].was_link_definition_started:
            lrd_stack_token = cast(
                LinkDefinitionStackToken, parser_state.token_stack[-1]
            )
            assert lrd_stack_token is not None
            assert lrd_stack_token.original_stack_depth is not None
            assert lrd_stack_token.original_document_depth is not None
            original_stack_depth, original_document_depth = (
                lrd_stack_token.original_stack_depth,
                lrd_stack_token.original_document_depth,
            )
            POGGER.debug(
                ">>continuation_lines>>$<<",
                lrd_stack_token.continuation_lines,
            )
            line_to_parse = lrd_stack_token.add_joined_lines_before_suffix(
                line_to_parse
            )
            (
                new_start_index,
                extracted_whitespace,
            ) = ParserHelper.extract_ascii_whitespace(line_to_parse, 0)
            assert new_start_index is not None
            start_index = new_start_index

            POGGER.debug(">>line_to_parse>>$<<", line_to_parse)
        return (
            was_started,
            lrd_stack_token,
            original_stack_depth,
            original_document_depth,
            line_to_parse,
            extracted_whitespace,
            start_index,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def __determine_continue_or_stop(
        parser_state: ParserState,
        position_marker: PositionMarker,
        was_started: bool,
        remaining_line_to_parse: str,
        extracted_whitespace: Optional[str],
        unmodified_line_to_parse: str,
        original_stack_depth: int,
        original_document_depth: int,
        end_lrd_index: Optional[int],
        line_to_parse_size: int,
        is_blank_line: Optional[bool],
        did_complete_lrd: bool,
        parsed_lrd_tuple: Optional[LinkReferenceDefinitionTuple],
        lines_to_requeue: List[str],
        process_mode: int,
    ) -> Tuple[bool, bool, List[MarkdownToken]]:

        assert is_blank_line is not None
        assert end_lrd_index is not None
        did_pause_lrd: bool = (
            end_lrd_index >= 0
            and end_lrd_index == line_to_parse_size
            and not is_blank_line
        )
        if did_pause_lrd:
            POGGER.debug(">>parse_link_reference_definition>>continuation")
            LinkReferenceDefinitionHelper.__add_line_for_lrd_continuation(
                parser_state,
                position_marker,
                was_started,
                remaining_line_to_parse,
                extracted_whitespace,
                unmodified_line_to_parse,
                original_stack_depth,
                original_document_depth,
            )
        new_tokens: List[MarkdownToken] = []
        if (not did_pause_lrd and was_started) or did_complete_lrd:
            POGGER.debug(">>parse_link_reference_definition>>was_started")
            (
                force_ignore_first_as_lrd,
                new_tokens,
                extracted_whitespace,
            ) = LinkReferenceDefinitionHelper.__stop_lrd_continuation(
                parser_state,
                did_complete_lrd,
                parsed_lrd_tuple,
                end_lrd_index,
                remaining_line_to_parse,
                is_blank_line,
                lines_to_requeue,
                extracted_whitespace,
                process_mode,
            )
        else:
            force_ignore_first_as_lrd = False
            POGGER.debug(">>parse_link_reference_definition>>other")

        POGGER.debug(">>XXXXXX>>requeue:$:", lines_to_requeue)
        POGGER.debug(">>XXXXXX>>did_complete_lrd:$:", did_complete_lrd)
        return did_pause_lrd, force_ignore_first_as_lrd, new_tokens

    # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_link_reference_definition_processing(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        is_blank_line: Optional[bool],
        was_started: bool,
        line_to_parse_size: int,
        remaining_line_to_parse: str,
        lines_to_requeue: List[str],
        unmodified_line_to_parse: str,
    ) -> Tuple[
        bool, Optional[int], Optional[LinkReferenceDefinitionTuple], Optional[bool], str
    ]:
        if was_started:
            POGGER.debug(">>parse_link_reference_definition>>was_started")
            did_complete_lrd: Optional[bool] = False
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionHelper.__parse_link_reference_definition(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            POGGER.debug(
                ">>parse_link_reference_definition>>was_started>>did_complete_lrd>>$"
                + ">>end_lrd_index>>$>>len(line_to_parse)>>$",
                did_complete_lrd,
                end_lrd_index,
                line_to_parse_size,
            )

            if not (
                did_complete_lrd
                or (
                    not is_blank_line
                    and not did_complete_lrd
                    and (end_lrd_index == line_to_parse_size)
                )
            ):
                POGGER.debug(
                    ">>parse_link_reference_definition>>was_started>>GOT HARD FAILURE"
                )
                (
                    is_blank_line,
                    line_to_parsex,
                    did_complete_lrd,
                    end_lrd_index,
                    parsed_lrd_tuple,
                ) = LinkReferenceDefinitionHelper.__process_lrd_hard_failure(
                    parser_state,
                    remaining_line_to_parse,
                    lines_to_requeue,
                    unmodified_line_to_parse,
                )
                assert line_to_parsex is not None
                line_to_parse = line_to_parsex
        else:
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionHelper.__parse_link_reference_definition(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            POGGER.debug(
                ">>parse_link_reference_definition>>did_complete_lrd>>$>>end_lrd_index>>$>>len(line_to_parse)>>$",
                did_complete_lrd,
                end_lrd_index,
                line_to_parse_size,
            )
        assert did_complete_lrd is not None
        return (
            did_complete_lrd,
            end_lrd_index,
            parsed_lrd_tuple,
            is_blank_line,
            line_to_parse,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __prepare_for_requeue_reset_markdown_token(
        parser_state: ParserState, lrd_stack_token: LinkDefinitionStackToken
    ) -> None:
        assert lrd_stack_token.last_block_quote_markdown_token_index is not None
        POGGER.debug(
            ">>XXXXXX>>last_block_quote_markdown_token_index:$:",
            lrd_stack_token.last_block_quote_markdown_token_index,
        )
        POGGER.debug(
            ">>XXXXXX>>st-now:$:",
            parser_state.token_document[
                lrd_stack_token.last_block_quote_markdown_token_index
            ],
        )

        del parser_state.token_document[
            lrd_stack_token.last_block_quote_markdown_token_index
        ]
        assert lrd_stack_token.copy_of_last_block_quote_markdown_token is not None
        parser_state.token_document.insert(
            lrd_stack_token.last_block_quote_markdown_token_index,
            lrd_stack_token.copy_of_last_block_quote_markdown_token,
        )
        assert lrd_stack_token.last_block_quote_stack_token is not None
        POGGER.debug(
            "last_block_quote_stack_token>:$:<",
            lrd_stack_token.last_block_quote_stack_token,
        )
        lrd_stack_token.last_block_quote_stack_token.reset_matching_markdown_token(
            lrd_stack_token.copy_of_last_block_quote_markdown_token
        )
        POGGER.debug(
            "last_block_quote_stack_token>:$:<",
            lrd_stack_token.last_block_quote_stack_token,
        )

    @staticmethod
    def __prepare_for_requeue_reset_document_and_stack(
        parser_state: ParserState,
        lrd_stack_token: LinkDefinitionStackToken,
        original_stack_depth: int,
        original_document_depth: int,
    ) -> None:
        POGGER.debug(">>XXXXXX>>original_stack_depth:$:", original_stack_depth)
        POGGER.debug(">>XXXXXX>>token_stack_depth:$:", len(parser_state.token_stack))
        POGGER.debug(">>XXXXXX>>token_stack(before):$:", parser_state.token_stack)
        POGGER.debug(
            ">>XXXXXX>>copy_of_token_stack:$:", parser_state.copy_of_token_stack
        )
        POGGER.debug(
            ">>lrd_stack_token>>copy_of_token_stack:$:",
            lrd_stack_token.copy_of_token_stack,
        )
        if len(parser_state.token_stack) >= original_stack_depth:
            while len(parser_state.token_stack) > original_stack_depth:
                del parser_state.token_stack[-1]
        else:
            while len(parser_state.token_stack):
                del parser_state.token_stack[-1]
            assert lrd_stack_token.copy_of_token_stack is not None
            parser_state.token_stack.extend(lrd_stack_token.copy_of_token_stack)
        POGGER.debug(">>XXXXXX>>token_stack(after):$:", parser_state.token_stack)

        POGGER.debug(">>XXXXXX>>original_document_depth:$:", original_document_depth)
        POGGER.debug(
            ">>XXXXXX>>token_document_depth:$:",
            len(parser_state.token_document),
        )
        POGGER.debug(">>XXXXXX>>token_document(before):$:", parser_state.token_document)
        while len(parser_state.token_document) > original_document_depth:
            del parser_state.token_document[-1]
        POGGER.debug(">>XXXXXX>>token_document(after):$:", parser_state.token_document)

    # pylint: disable=too-many-arguments
    @staticmethod
    def __prepare_for_requeue(
        parser_state: ParserState,
        lrd_stack_token: Optional[LinkDefinitionStackToken],
        did_complete_lrd: bool,
        original_stack_depth: int,
        original_document_depth: int,
        lines_to_requeue: List[str],
    ) -> None:
        # This works because in most cases, we add things.  However, in cases like
        # an indented code block, we process the "is it indented enough" and close
        # that block before hitting this.  As such, we have a special case to take
        # care of that.  In the future, will possibly want to do something instead of
        # original_document_depth and stack, such as passing in a copy of the both
        # elements so they can be reset on the rewind.
        # i.e. icode would go back on stack, end-icode would not be in document.
        assert lrd_stack_token is not None
        POGGER.debug("lines_to_requeue:$:", lines_to_requeue)
        POGGER.debug(
            ">>XXXXXX>>copy_of_last_block_quote_markdown_token:$:",
            lrd_stack_token.copy_of_last_block_quote_markdown_token,
        )
        if not did_complete_lrd:
            if lrd_stack_token.copy_of_last_block_quote_markdown_token:
                LinkReferenceDefinitionHelper.__prepare_for_requeue_reset_markdown_token(
                    parser_state, lrd_stack_token
                )
            LinkReferenceDefinitionHelper.__prepare_for_requeue_reset_document_and_stack(
                parser_state,
                lrd_stack_token,
                original_stack_depth,
                original_document_depth,
            )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __is_link_reference_definition(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
    ) -> bool:
        """
        Determine whether or not we have the start of a link reference definition.
        """

        if parser_state.token_stack[-1].is_paragraph:
            return False

        assert extracted_whitespace is not None
        POGGER.debug(
            "__is_link_reference_definition - extracted_whitespace:>:$:<",
            extracted_whitespace,
        )
        POGGER.debug(
            "__is_link_reference_definition - line_to_parse:>:$:<", line_to_parse
        )
        if (
            TabHelper.is_length_less_than_or_equal_to(extracted_whitespace, 3)
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse,
            start_index,
            LinkReferenceDefinitionHelper.__lrd_start_character,
        ):
            POGGER.debug("__is_link_reference_definition - potential")
            remaining_line, continue_with_lrd = line_to_parse[start_index + 1 :], True
            if (
                remaining_line
                and remaining_line[-1] == InlineHelper.backslash_character
            ):
                remaining_line_size, start_index, found_index = (
                    len(remaining_line),
                    0,
                    remaining_line.find(InlineHelper.backslash_character, start_index),
                )
                POGGER.debug(">>$<<$", remaining_line, remaining_line_size)
                POGGER.debug(">>$<<$", remaining_line, start_index)
                POGGER.debug(">>$<<", found_index)
                while found_index != -1 and found_index < (remaining_line_size - 1):
                    start_index = found_index + 2
                    POGGER.debug(">>$<<$", remaining_line, start_index)
                    found_index = remaining_line.find(
                        InlineHelper.backslash_character, start_index
                    )
                    POGGER.debug(">>$<<", found_index)
                POGGER.debug(">>>>>>>$<<", found_index)
                continue_with_lrd = found_index != remaining_line_size - 1
            return continue_with_lrd
        return False

    @staticmethod
    def __verify_link_definition_end(
        line_to_parse: str, new_index: Optional[int]
    ) -> Tuple[bool, Optional[int], Optional[str]]:
        """
        Verify that the link reference definition's ends properly.
        """

        assert new_index is not None
        POGGER.debug("look for EOL-ws>>$<<", line_to_parse[new_index:])
        new_index, ex_ws = ParserHelper.extract_ascii_whitespace(
            line_to_parse, new_index
        )
        assert new_index is not None
        POGGER.debug("look for EOL>>$<<", line_to_parse[new_index:])
        if new_index < len(line_to_parse):
            POGGER.debug(">> characters left at EOL, bailing")
            return False, -1, None
        return True, new_index, ex_ws

    # pylint: disable=too-many-locals
    @staticmethod
    def __parse_link_reference_definition(
        parser_state: ParserState,
        line_to_parse: str,
        start_index: int,
        extracted_whitespace: Optional[str],
        is_blank_line: Optional[bool],
    ) -> Tuple[bool, Optional[int], Optional[LinkReferenceDefinitionTuple]]:
        """
        Handle the parsing of what appears to be a link reference definition.
        """
        # POGGER.debug("parse_link_reference_definition:$:", line_to_parse)
        # POGGER.debug("start_index:$:", start_index)
        # POGGER.debug("extracted_whitespace:$:", extracted_whitespace)
        did_start = LinkReferenceDefinitionHelper.__is_link_reference_definition(
            parser_state, line_to_parse, start_index, extracted_whitespace
        )
        if not did_start:
            POGGER.debug("BAIL")
            return False, -1, None

        # POGGER.debug("parse_link_reference_definition")
        new_index: Optional[int] = None
        keep_going, new_index, collected_destination = LinkHelper.extract_link_label(
            line_to_parse, start_index + 1
        )
        # POGGER.debug("parse_link_reference_definition: keep_going:>:$:<", keep_going)
        # POGGER.debug("parse_link_reference_definition: new_index:>:$:<", new_index)
        # POGGER.debug(
        #     "parse_link_reference_definition: collected_destination:>:$:<",
        #     collected_destination,
        # )
        assert is_blank_line is not None
        if keep_going:
            (
                keep_going,
                new_index,
                inline_link,
                _,
                line_destination_whitespace,
                inline_raw_link,
            ) = LinkHelper.extract_link_destination(
                line_to_parse, new_index, is_blank_line
            )
            # POGGER.debug(
            #     "parse_link_reference_definition: keep_going:>:$:<", keep_going
            # )
            # POGGER.debug("parse_link_reference_definition: new_index:>:$:<", new_index)
            # POGGER.debug(
            #     "parse_link_reference_definition: inline_link:>:$:<", inline_link
            # )
            # POGGER.debug(
            #     "parse_link_reference_definition: line_destination_whitespace:>:$:<",
            #     line_destination_whitespace,
            # )
            # POGGER.debug(
            #     "parse_link_reference_definition: inline_raw_link:>:$:<",
            #     inline_raw_link,
            # )
        else:
            inline_link = None
        if keep_going:
            (
                keep_going,
                new_index,
                inline_title,
                _,
                line_title_whitespace,
                inline_raw_title,
            ) = LinkHelper.extract_link_title(line_to_parse, new_index, is_blank_line)
            # POGGER.debug(
            #     "parse_link_reference_definition: keep_going:>:$:<", keep_going
            # )
            # POGGER.debug("parse_link_reference_definition: new_index:>:$:<", new_index)
            # POGGER.debug(
            #     "parse_link_reference_definition: inline_title:>:$:<", inline_title
            # )
            # POGGER.debug(
            #     "parse_link_reference_definition: line_title_whitespace:>:$:<",
            #     line_title_whitespace,
            # )
            # POGGER.debug(
            #     "parse_link_reference_definition: inline_raw_title:>:$:<",
            #     inline_raw_title,
            # )
        else:
            inline_title = ""
        if keep_going:
            (
                keep_going,
                new_index,
                end_whitespace,
            ) = LinkReferenceDefinitionHelper.__verify_link_definition_end(
                line_to_parse, new_index
            )
        if keep_going:
            assert collected_destination is not None
            # POGGER.debug(
            #     ">>collected_destination(not normalized)>>$", collected_destination
            # )
            normalized_destination = LinkHelper.normalize_link_label(
                collected_destination
            )
            if not normalized_destination:
                keep_going, new_index = False, -1
        else:
            normalized_destination = None
        return (
            LinkReferenceDefinitionHelper.__create_lrd_token(
                new_index,
                collected_destination,
                normalized_destination,
                line_destination_whitespace,
                inline_link,
                inline_raw_link,
                inline_title,
                inline_raw_title,
                line_title_whitespace,
                end_whitespace,
            )
            if keep_going
            else (keep_going, new_index, None)
        )

    # pylint: enable=too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __create_lrd_token(
        new_index: Optional[int],
        collected_destination: Optional[str],
        normalized_destination: Optional[str],
        line_destination_whitespace: Optional[str],
        inline_link: Optional[str],
        inline_raw_link: Optional[str],
        inline_title: Optional[str],
        inline_raw_title: Optional[str],
        line_title_whitespace: Optional[str],
        end_whitespace: Optional[str],
    ) -> Tuple[bool, Optional[int], Optional[LinkReferenceDefinitionTuple]]:
        assert new_index != -1

        POGGER.debug(
            ">>collected_destination(normalized)>>$",
            normalized_destination,
        )

        if (
            not inline_title
            and line_title_whitespace
            and line_title_whitespace[-1] == ParserHelper.newline_character
        ):
            line_title_whitespace = line_title_whitespace[:-1]

        POGGER.debug(">>inline_link>>$<<", inline_link)
        POGGER.debug(">>inline_title>>$<<", inline_title)
        parsed_lrd_tuple = LinkReferenceDefinitionTuple(
            normalized_destination,
            LinkReferenceTitles(inline_link, inline_title),
            LinkReferenceInfo(
                collected_destination,
                line_destination_whitespace,
                inline_raw_link,
                line_title_whitespace,
                inline_raw_title,
                end_whitespace,
            ),
        )
        return True, new_index, parsed_lrd_tuple

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_line_for_lrd_continuation(
        parser_state: ParserState,
        position_marker: PositionMarker,
        was_started: bool,
        remaining_line_to_parse: str,
        extracted_whitespace: Optional[str],
        unmodified_line_to_parse: str,
        original_stack_depth: int,
        original_document_depth: int,
    ) -> None:
        """
        As part of processing a link reference definition, add a line to the continuation.
        """

        line_to_store = remaining_line_to_parse
        if not was_started:
            POGGER.debug(">>parse_link_reference_definition>>marking start")
            new_token = LinkDefinitionStackToken(extracted_whitespace, position_marker)
            parser_state.token_stack.append(new_token)
            new_token.original_stack_depth = original_stack_depth
            new_token.original_document_depth = original_document_depth

            new_token.last_block_quote_stack_token = (
                parser_state.last_block_quote_stack_token
            )
            new_token.last_block_quote_markdown_token_index = (
                parser_state.last_block_quote_markdown_token_index
            )
            new_token.copy_of_last_block_quote_markdown_token = (
                parser_state.copy_of_last_block_quote_markdown_token
            )
            new_token.copy_of_token_stack = parser_state.copy_of_token_stack
        else:
            new_token = cast(LinkDefinitionStackToken, parser_state.token_stack[-1])

        POGGER.debug(">>line_to_store>>add>:$<<", line_to_store)
        POGGER.debug(">>unmodified_line_to_parse>>add>:$<<", unmodified_line_to_parse)
        assert unmodified_line_to_parse.endswith(line_to_store)
        new_token.add_continuation_line(line_to_store)
        new_token.add_unmodified_line(unmodified_line_to_parse)

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __stop_lrd_continuation(
        parser_state: ParserState,
        did_complete_lrd: bool,
        parsed_lrd_tuple: Optional[LinkReferenceDefinitionTuple],
        end_lrd_index: int,
        remaining_line_to_parse: str,
        is_blank_line: bool,
        lines_to_requeue: List[str],
        extracted_whitespace: Optional[str],
        process_mode: int,
    ) -> Tuple[bool, List[MarkdownToken], Optional[str]]:
        """
        As part of processing a link reference definition, stop a continuation.
        """

        POGGER.debug(">>parse_link_reference_definition>>no longer need start")
        if did_complete_lrd:
            assert parsed_lrd_tuple
            assert parsed_lrd_tuple.normalized_destination is not None
            did_add_definition = LinkHelper.add_link_definition(
                parsed_lrd_tuple.normalized_destination, parsed_lrd_tuple.link_titles
            )
            assert not (end_lrd_index < -1 and remaining_line_to_parse)
            link_def_token = cast(
                LinkDefinitionStackToken, parser_state.token_stack[-1]
            )
            assert link_def_token.extracted_whitespace is not None
            extracted_whitespace = link_def_token.extracted_whitespace

            POGGER.debug(
                "link_def_token.extracted_whitespace>:$:<",
                link_def_token.extracted_whitespace,
            )
            POGGER.debug(
                "link_def_token.continuation_lines>:$:<",
                link_def_token.continuation_lines,
            )
            POGGER.debug(
                "link_def_token.unmodified_lines>:$:<", link_def_token.unmodified_lines
            )
            POGGER.debug("lines_to_requeue>:$:<", lines_to_requeue)

            does_any_line_have_tabs = any(
                ParserHelper.tab_character in ffg
                for ffg in link_def_token.unmodified_lines
            )
            POGGER.debug("does_any_line_have_tabs>:$:<", does_any_line_have_tabs)

            last_container_index = parser_state.find_last_container_on_stack()
            if does_any_line_have_tabs and last_container_index > 0:
                (
                    extracted_whitespace,
                    parsed_lrd_tuple,
                ) = LinkReferenceDefinitionHelper.__stop_lrd_continuation_with_tab(
                    parser_state,
                    link_def_token,
                    last_container_index,
                    lines_to_requeue,
                    process_mode,
                    extracted_whitespace,
                    parsed_lrd_tuple,
                )

            assert extracted_whitespace is not None
            assert parsed_lrd_tuple.normalized_destination is not None
            new_tokens: List[MarkdownToken] = [
                LinkReferenceDefinitionMarkdownToken(
                    did_add_definition,
                    extracted_whitespace,
                    parsed_lrd_tuple.normalized_destination,
                    parsed_lrd_tuple.link_titles,
                    parsed_lrd_tuple.link_info,
                    position_marker=link_def_token.start_position_marker,
                )
            ]
            POGGER.debug(">>link_info>>$", parsed_lrd_tuple.link_info)
            assert parsed_lrd_tuple.link_info.line_destination_whitespace is not None
            POGGER.debug(
                ">>line_destination_whitespace>>$",
                ParserHelper.make_whitespace_visible(
                    parsed_lrd_tuple.link_info.line_destination_whitespace
                ),
            )
            POGGER.debug(">>new_tokens>>$", new_tokens)
            force_ignore_first_as_lrd = len(lines_to_requeue) > 1
        else:
            new_tokens = []
            assert is_blank_line
            force_ignore_first_as_lrd = True
        del parser_state.token_stack[-1]
        return force_ignore_first_as_lrd, new_tokens, extracted_whitespace

    # pylint: enable=too-many-arguments

    @staticmethod
    def __find_line_ws(parsed_lines: str, original_lines: str) -> Tuple[str, bool, int]:
        start_text_index = original_lines.find(parsed_lines)
        assert start_text_index != -1
        POGGER.debug("start_text_index>:$:<", start_text_index)
        start_whitespace_index, _ = ParserHelper.extract_spaces_from_end(
            original_lines, start_text_index
        )
        POGGER.debug("start_whitespace_index>:$:<", start_whitespace_index)
        tabified_whitespace = original_lines[start_whitespace_index:start_text_index]
        POGGER.debug("tabified_whitespace>:$:<", tabified_whitespace)
        split_tab = bool(tabified_whitespace and tabified_whitespace[0] == "\t")
        if not split_tab:
            tabified_whitespace = tabified_whitespace[1:]
            start_whitespace_index += 1
        extracted_whitespace = tabified_whitespace
        POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        POGGER.debug("split_tab>:$:<", split_tab)
        return extracted_whitespace, split_tab, start_whitespace_index

    # pylint: disable=too-many-arguments
    @staticmethod
    def __stop_lrd_continuation_with_tab(
        parser_state: ParserState,
        link_def_token: LinkDefinitionStackToken,
        last_container_index: int,
        lines_to_requeue: List[str],
        process_mode: int,
        extracted_whitespace: Optional[str],
        parsed_lrd_tuple: LinkReferenceDefinitionTuple,
    ) -> Tuple[Optional[str], LinkReferenceDefinitionTuple]:
        POGGER.debug(
            "extracted_whitespace>:$:<",
            link_def_token.extracted_whitespace,
        )
        assert parser_state.token_stack[last_container_index].is_block_quote
        # POGGER.debug("link_def_token>:$:<", link_def_token)
        # POGGER.debug("link_def_token.last_block_quote_stack_token>:$:<", link_def_token.last_block_quote_stack_token)
        last_block_quote_index = parser_state.find_last_block_quote_on_stack()
        last_block_quote_token = parser_state.token_stack[last_block_quote_index]
        # POGGER.debug("last_block_quote_token>:$:<", last_block_quote_token)
        block_quote_token = cast(
            BlockQuoteMarkdownToken, last_block_quote_token.matching_markdown_token
        )
        # POGGER.debug("block_quote_token.leading_spaces>:$:<", block_quote_token.leading_spaces)

        POGGER.debug(
            "link_def_token.continuation_lines>:$:<", link_def_token.continuation_lines
        )
        POGGER.debug(
            "link_def_token.unmodified_lines>:$:<", link_def_token.unmodified_lines
        )

        if len(link_def_token.continuation_lines) == 1:
            extracted_whitespace = (
                LinkReferenceDefinitionHelper.__stop_lrd_continuation_with_tab_single(
                    parser_state,
                    link_def_token,
                    process_mode,
                    block_quote_token,
                    lines_to_requeue,
                )
            )
        else:
            (
                extracted_whitespace,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionHelper.__stop_lrd_continuation_with_tab_multiple(
                parser_state, extracted_whitespace, link_def_token, block_quote_token
            )

        return extracted_whitespace, parsed_lrd_tuple

    # pylint: enable=too-many-arguments

    @staticmethod
    def __stop_lrd_continuation_with_tab_single(
        parser_state: ParserState,
        link_def_token: LinkDefinitionStackToken,
        process_mode: int,
        block_quote_token: BlockQuoteMarkdownToken,
        lines_to_requeue: List[str],
    ) -> str:
        parsed_lines = link_def_token.continuation_lines[0]
        original_lines = link_def_token.unmodified_lines[0]
        # POGGER.debug("parsed_lines>:$:<", parsed_lines)
        # POGGER.debug("original_lines>:$:<", original_lines)

        (
            extracted_whitespace,
            split_tab,
            _,
        ) = LinkReferenceDefinitionHelper.__find_line_ws(parsed_lines, original_lines)

        POGGER.debug("process_mode>:$:<", process_mode)
        POGGER.debug(
            "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        )
        if process_mode == 1:
            block_quote_token.remove_last_bleading_space()
            # POGGER.debug("block_quote_token.leading_spaces>:$:<", block_quote_token.leading_spaces)
        else:
            # POGGER.debug("lines_to_requeue>:$:<", lines_to_requeue)
            for _ in lines_to_requeue:
                # POGGER.debug("block_quote_token.leading_spaces>:$:<", block_quote_token.leading_spaces)
                block_quote_token.remove_last_bleading_space()
                # POGGER.debug("block_quote_token.leading_spaces>:$:<", block_quote_token.leading_spaces)

        # POGGER.debug("block_quote_token.leading_spaces>:$:<", block_quote_token.leading_spaces)
        if split_tab:
            TabHelper.adjust_block_quote_indent_for_tab(parser_state)
        POGGER.debug(
            "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        )
        return extracted_whitespace

    # pylint: disable=too-many-locals

    @staticmethod
    def __stop_lrd_continuation_with_tab_multiple(
        parser_state: ParserState,
        extracted_whitespace: Optional[str],
        link_def_token: LinkDefinitionStackToken,
        block_quote_token: BlockQuoteMarkdownToken,
    ) -> Tuple[Optional[str], LinkReferenceDefinitionTuple]:

        split_tabs_list: List[bool] = []
        completed_lrd_text: str = ""
        alt_ws = None
        for this_line_index, this_line in enumerate(link_def_token.continuation_lines):

            original_this_line = link_def_token.unmodified_lines[this_line_index]
            POGGER.debug("this_line_index>:$:<", this_line_index)
            POGGER.debug("this_line>:$:<", this_line)
            POGGER.debug("original_this_line>:$:<", original_this_line)

            (
                extracted_ws,
                split_tab,
                start_whitespace_index,
            ) = LinkReferenceDefinitionHelper.__find_line_ws(
                this_line, original_this_line
            )

            if completed_lrd_text:
                completed_lrd_text += "\n"
            if this_line_index == 0:
                extracted_whitespace = extracted_ws
                alt_ws = TabHelper.detabify_string(
                    extracted_whitespace, start_whitespace_index
                )
            else:
                completed_lrd_text += extracted_ws
            completed_lrd_text += this_line
            split_tabs_list.append(split_tab)

        POGGER.debug("completed_lrd_text>:$:<", completed_lrd_text)
        (
            did_succeed,
            next_index,
            new_parsed_lrd_tuple,
        ) = LinkReferenceDefinitionHelper.__parse_link_reference_definition(
            parser_state, completed_lrd_text, 0, alt_ws, True
        )
        assert did_succeed
        assert len(completed_lrd_text) == next_index
        # POGGER.debug("new_parsed_lrd_tuple>:$:<", new_parsed_lrd_tuple)
        assert new_parsed_lrd_tuple is not None
        parsed_lrd_tuple = new_parsed_lrd_tuple

        LinkReferenceDefinitionHelper.__xx_multiple_fix_leading_spaces(
            block_quote_token, split_tabs_list, link_def_token
        )
        return extracted_whitespace, parsed_lrd_tuple

    # pylint: enable=too-many-locals

    @staticmethod
    def __xx_multiple_fix_leading_spaces(
        block_quote_token: BlockQuoteMarkdownToken,
        split_tabs_list: List[bool],
        link_def_token: LinkDefinitionStackToken,
    ) -> None:
        POGGER.debug("split_tabs_list>:$:<", split_tabs_list)
        POGGER.debug(
            "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        )
        assert block_quote_token.bleading_spaces is not None
        leading_spaces: List[str] = []
        for _ in link_def_token.continuation_lines:
            last_leading_space = block_quote_token.remove_last_bleading_space()
            POGGER.debug("last_leading_space>:$:<", last_leading_space)
            if last_leading_space[0] == "\n":
                last_leading_space = last_leading_space[1:]
            leading_spaces.append(last_leading_space)
        assert len(split_tabs_list) == len(leading_spaces)
        POGGER.debug("leading_spaces>:$:<", leading_spaces)
        POGGER.debug(
            "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        )
        is_first = len(block_quote_token.bleading_spaces) == 0
        for prefix_to_add in leading_spaces:
            if split_tabs_list[0]:
                prefix_to_add = prefix_to_add[:-1]
            del split_tabs_list[0]
            block_quote_token.add_bleading_spaces(prefix_to_add, is_first)
            is_first = False

    @staticmethod
    def __process_lrd_hard_failure(
        parser_state: ParserState,
        remaining_line_to_parse: str,
        lines_to_requeue: List[str],
        unmodified_line_to_parse: str,
    ) -> Tuple[
        Optional[bool],
        Optional[str],
        Optional[bool],
        Optional[int],
        Optional[LinkReferenceDefinitionTuple],
    ]:
        """
        In cases of a hard failure, we have had continuations to the original line
        that make it a bit more difficult to figure out if we have an actual good
        LRD in the mix somehow.  So take lines off the end while we have lines.
        """
        (
            is_blank_line,
            line_to_parse,
            did_complete_lrd,
            end_lrd_index,
            parsed_lrd_tuple,
        ) = (None, None, None, None, None)
        link_ref_stack_token = cast(
            LinkDefinitionStackToken, parser_state.token_stack[-1]
        )

        POGGER.debug(">>remaining_line_to_parse>>add>:$<<", remaining_line_to_parse)
        POGGER.debug(">>unmodified_line_to_parse>>add>:$<<", unmodified_line_to_parse)
        assert unmodified_line_to_parse.endswith(remaining_line_to_parse)
        link_ref_stack_token.add_continuation_line(remaining_line_to_parse)
        link_ref_stack_token.add_unmodified_line(unmodified_line_to_parse)
        while link_ref_stack_token.continuation_lines:
            POGGER.debug(
                "continuation_lines>>$<<",
                ParserHelper.make_whitespace_visible(
                    str(link_ref_stack_token.continuation_lines)
                ),
            )
            POGGER.debug(
                "unmodified_lines>>$<<",
                ParserHelper.make_whitespace_visible(
                    str(link_ref_stack_token.unmodified_lines)
                ),
            )

            lines_to_requeue.append(link_ref_stack_token.unmodified_lines[-1])
            POGGER.debug(
                ">>continuation_line>>$",
                link_ref_stack_token.continuation_lines[-1],
            )
            POGGER.debug(
                ">>unmodified_line>>$",
                link_ref_stack_token.unmodified_lines[-1],
            )
            del link_ref_stack_token.continuation_lines[-1]
            del link_ref_stack_token.unmodified_lines[-1]
            POGGER.debug(
                ">>lines_to_requeue>>$>>",
                lines_to_requeue,
            )
            POGGER.debug(
                ">>continuation_lines>>$<<",
                link_ref_stack_token.continuation_lines,
            )
            POGGER.debug(
                ">>unmodified_lines>>$<<",
                link_ref_stack_token.unmodified_lines,
            )
            (
                is_blank_line,
                line_to_parse,
            ) = True, link_ref_stack_token.add_joined_lines_before_suffix("")
            line_to_parse = line_to_parse[:-1]
            start_index, extracted_whitespace = ParserHelper.extract_spaces(
                line_to_parse, 0
            )
            assert start_index is not None
            POGGER.debug(">>line_to_parse>>$<<", line_to_parse)
            (
                did_complete_lrd,
                end_lrd_index,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionHelper.__parse_link_reference_definition(
                parser_state,
                line_to_parse,
                start_index,
                extracted_whitespace,
                is_blank_line,
            )
            POGGER.debug(
                ">>parse_link_reference_definition>>was_started>>did_complete_lrd>>$"
                + ">>end_lrd_index>>$>>len(line_to_parse)>>$",
                did_complete_lrd,
                end_lrd_index,
                len(line_to_parse),
            )
            if did_complete_lrd:
                break
        return (
            is_blank_line,
            line_to_parse,
            did_complete_lrd,
            end_lrd_index,
            parsed_lrd_tuple,
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def handle_link_reference_definition_leaf_block(
        parser_state: ParserState,
        outer_processed: bool,
        position_marker: PositionMarker,
        leaf_token_whitespace: Optional[str],
        remaining_line_to_parse: str,
        ignore_link_definition_start: bool,
        pre_tokens: List[MarkdownToken],
        original_line: str,
    ) -> Tuple[bool, Optional[RequeueLineInfo]]:
        """
        Take care of the processing for link reference definitions.
        """
        POGGER.debug(
            "handle_link_reference_definition>>pre_tokens>>$<<",
            pre_tokens,
        )

        if not outer_processed and not ignore_link_definition_start:
            POGGER.debug(
                "plflb-process_link_reference_definition>>outer_processed>>$",
                position_marker.text_to_parse[position_marker.index_number :],
            )
            assert parser_state.original_line_to_parse is not None
            (
                outer_processed,
                _,  # did_complete_lrd,
                _,  # did_pause_lrd,
                requeue_line_info,
                new_tokens,
            ) = LinkReferenceDefinitionHelper.process_link_reference_definition(
                parser_state,
                position_marker,
                remaining_line_to_parse,
                leaf_token_whitespace,
                parser_state.original_line_to_parse,
                parser_state.original_stack_depth,
                parser_state.original_document_depth,
                original_line,
                0,
            )
            if requeue_line_info:
                outer_processed = True
                POGGER.debug(
                    "plflb-process_link_reference_definition>>outer_processed>>$<lines_to_requeue<$<$",
                    outer_processed,
                    requeue_line_info.lines_to_requeue,
                    len(requeue_line_info.lines_to_requeue),
                )
            else:
                POGGER.debug(
                    "plflb-process_link_reference_definition>>outer_processed>>$<lines_to_requeue<(None)",
                    outer_processed,
                )
        else:
            requeue_line_info, new_tokens = None, []

        POGGER.debug("handle_link_reference_definition>>pre_tokens>>$<<", pre_tokens)
        pre_tokens.extend(new_tokens)
        POGGER.debug("handle_link_reference_definition>>pre_tokens>>$<<", pre_tokens)
        return outer_processed, requeue_line_info

    # pylint: enable=too-many-arguments
