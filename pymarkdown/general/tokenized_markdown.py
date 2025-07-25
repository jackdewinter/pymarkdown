"""
Module to provide a tokenization of a markdown-encoded string.
"""

import logging
import os
from typing import List, Optional, Tuple, cast

from application_properties import ApplicationProperties

from pymarkdown.coalesce.coalesce_processor import CoalesceProcessor
from pymarkdown.container_blocks.container_block_processor import (
    ContainerBlockProcessor,
)
from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.extension_manager.extension_manager import ExtensionManager
from pymarkdown.extensions.front_matter_extension import FrontMatterExtension
from pymarkdown.extensions.pragma_token import PragmaToken
from pymarkdown.general.bad_tokenization_error import BadTokenizationError
from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.requeue_line_info import RequeueLineInfo
from pymarkdown.general.source_providers import InMemorySourceProvider, SourceProvider
from pymarkdown.html.html_helper import HtmlHelper
from pymarkdown.inline.inline_character_reference_helper import (
    InlineCharacterReferenceHelper,
)
from pymarkdown.inline.inline_processor import InlineProcessor
from pymarkdown.leaf_blocks.leaf_block_helper import LeafBlockHelper
from pymarkdown.leaf_blocks.leaf_block_processor_paragraph import (
    LeafBlockProcessorParagraph,
)
from pymarkdown.leaf_blocks.table_block_processor import TableBlockHelper
from pymarkdown.links.link_parse_helper import LinkParseHelper
from pymarkdown.links.link_reference_definition_helper import (
    LinkReferenceDefinitionHelper,
)
from pymarkdown.tokens.blank_line_markdown_token import BlankLineMarkdownToken
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.end_of_stream_token import EndOfStreamToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import (
    BlockQuoteStackToken,
    DocumentStackToken,
    ParagraphStackToken,
    StackToken,
)

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-many-lines


class TokenizedMarkdown:
    """
    Class to provide a tokenization of a markdown-encoded string.
    """

    def __init__(self, resource_path: Optional[str] = None) -> None:
        """
        Initializes a new instance of the TokenizedMarkdown class.
        """

        self.__tokenized_document: List[MarkdownToken] = []
        self.__token_stack: List[StackToken] = []
        self.__parse_properties: Optional[ParseBlockPassProperties] = None
        self.__source_provider: Optional[SourceProvider] = None
        self.__extension_manager: Optional[ExtensionManager] = None

        if not resource_path:
            resource_path = os.path.join(os.path.split(__file__)[0], "..", "resources")
            resource_path = os.path.abspath(resource_path)
        InlineCharacterReferenceHelper.initialize(resource_path)

    def apply_configuration(
        self,
        application_properties: ApplicationProperties,
        extension_manager: ExtensionManager,
    ) -> None:
        """
        Apply any configuration map.
        """
        _ = application_properties
        self.__extension_manager = extension_manager
        self.__parse_properties = ParseBlockPassProperties(extension_manager)

    def transform_from_provider(
        self,
        source_provider: Optional[SourceProvider],
        do_add_end_of_stream_token: bool = False,
    ) -> List[MarkdownToken]:
        """
        Transform the data from the source provider into a Markdown token stream.
        """
        self.__source_provider = source_provider
        return self.__transform(do_add_end_of_stream_token)

    def transform(
        self,
        your_text_string: str,
        show_debug: bool = False,
        do_add_end_of_stream_token: bool = False,
    ) -> List[MarkdownToken]:
        """
        Transform a text string in a Markdown format into a Markdown token stream.
        This function should only be used as a simplified manner of accessing the
        functionality for the purposes of testing.
        """

        logging.getLogger().setLevel(logging.DEBUG if show_debug else logging.WARNING)
        ParserLogger.sync_on_next_call()
        self.__source_provider = InMemorySourceProvider(your_text_string)
        return self.__transform(do_add_end_of_stream_token)

    def __transform(self, do_add_end_of_stream_token: bool) -> List[MarkdownToken]:
        """
        Transform a markdown-encoded string into an array of tokens.
        """
        try:
            self.__tokenized_document = []
            self.__token_stack = []

            assert (
                self.__extension_manager is not None
            ), "Extension manager must be initialized by this point."
            InlineProcessor.initialize(self.__extension_manager)
            LinkParseHelper.initialize()

            POGGER.debug("\n\n>>>>>>>parse_blocks_pass>>>>>>")
            first_pass_results = self.__parse_blocks_pass(do_add_end_of_stream_token)

            POGGER.debug("\n\n>>>>>>>coalesce_text_blocks>>>>>>")
            coalesced_results = CoalesceProcessor.coalesce_text_blocks(
                first_pass_results
            )

            POGGER.debug("\n\n>>>>>>>parse_inline>>>>>>")
            assert (
                self.__parse_properties is not None
            ), "Parse properties must be defined by this point."
            final_pass_results = InlineProcessor.parse_inline(
                coalesced_results, self.__parse_properties
            )

            final_coalesced_results = CoalesceProcessor.coalesce_text_blocks(
                final_pass_results, only_change_text_blocks=True
            )
            POGGER.debug("\n\n>>>>>>>final_pass_results>>>>>>")
            return final_coalesced_results
        except Exception as this_exception:
            raise BadTokenizationError(
                "An unhandled error occurred processing the document."
            ) from this_exception

    def __parse_blocks_pass(
        self, do_add_end_of_stream_token: bool
    ) -> List[MarkdownToken]:
        """
        The first pass at the tokens is to deal with blocks.
        """

        assert (
            self.__parse_properties is not None
        ), "Parse properties must be defined by this point."
        assert (
            self.__source_provider is not None
        ), "Source provider must be defined by this point."
        self.__token_stack = [DocumentStackToken()]
        self.__tokenized_document = []
        self.__parse_properties.pragma_lines = {}

        POGGER.debug("---")
        try:
            first_line_in_document, line_number = (
                self.__source_provider.get_next_line(),
                1,
            )
            POGGER.debug("---$---", first_line_in_document)
            (
                first_line_in_document,
                line_number,
                requeue,
            ) = self.__process_front_matter_header_if_present(
                first_line_in_document, line_number, []
            )
            (
                did_start_close,
                did_started_close,
                keep_on_going,
                ignore_link_definition_start,
                ignore_table_start,
            ) = (first_line_in_document is None, False, True, False, False)
            next_line_in_document = first_line_in_document
            while keep_on_going:
                (
                    keep_on_going,
                    did_start_close,
                    did_started_close,
                    ignore_link_definition_start,
                    ignore_table_start,
                    requeue,
                    line_number,
                    next_line_in_document,
                ) = self.__parse_blocks_pass_next_line(
                    next_line_in_document,
                    line_number,
                    requeue,
                    did_start_close,
                    did_started_close,
                    ignore_link_definition_start,
                    ignore_table_start,
                )
        except AssertionError as this_exception:
            error_message = f"A project assertion failed on line {line_number} of the current document."
            raise BadTokenizationError(error_message) from this_exception

        if do_add_end_of_stream_token:
            self.__tokenized_document.append(EndOfStreamToken(line_number))

        if self.__parse_properties.pragma_lines:
            self.__tokenized_document.append(
                PragmaToken(self.__parse_properties.pragma_lines)
            )
        return self.__tokenized_document

    # pylint: disable=too-many-arguments
    def __parse_blocks_pass_next_line(
        self,
        next_line_in_document: Optional[str],
        line_number: int,
        requeue: List[str],
        did_start_close: bool,
        did_started_close: bool,
        ignore_link_definition_start: bool,
        ignore_table_start: bool,
    ) -> Tuple[bool, bool, bool, bool, bool, List[str], int, Optional[str]]:
        POGGER.debug("next-line>>$", next_line_in_document)
        POGGER.debug("stack>>$", self.__token_stack)
        POGGER.debug("current_block>>$", self.__token_stack[-1])
        POGGER.debug("line_number>>$", line_number)
        POGGER.debug("---")

        assert (
            self.__parse_properties is not None
        ), "Parse properties must be defined by this point."
        parser_state = ParserState(
            self.__token_stack,
            self.__tokenized_document,
            TokenizedMarkdown.__close_open_blocks,
            self.__handle_blank_line,
            self.__parse_properties,
        )
        keep_on_going = True
        if did_start_close:
            (
                did_started_close,
                did_start_close,
                tokens_from_line,
                line_number,
                keep_on_going,
                requeue_line_info,
            ) = self.__main_pass_did_start_close(parser_state, line_number)
        else:
            assert (
                next_line_in_document is not None
            ), "If not closing, must have a next line to process."
            position_marker = PositionMarker(line_number, 0, next_line_in_document)
            (
                tfl,
                requeue_line_info,
            ) = self.__main_pass_did_not_start_close(
                parser_state,
                position_marker,
                next_line_in_document,
                ignore_link_definition_start,
                ignore_table_start,
            )
            assert tfl is not None, "Markdown token list cannot be empty."
            tokens_from_line = tfl

        if keep_on_going:
            (
                line_number,
                ignore_link_definition_start,
                ignore_table_start,
                next_line_in_document,
                did_start_close,
                did_started_close,
            ) = self.__main_pass_keep_on_going(
                line_number,
                requeue_line_info,
                requeue,
                tokens_from_line,
                did_start_close,
                did_started_close,
            )
        return (
            keep_on_going,
            did_start_close,
            did_started_close,
            ignore_link_definition_start,
            ignore_table_start,
            requeue,
            line_number,
            next_line_in_document,
        )

    # pylint: enable=too-many-arguments

    def __main_pass_did_start_close(
        self, parser_state: ParserState, line_number: int
    ) -> Tuple[bool, bool, List[MarkdownToken], int, bool, Optional[RequeueLineInfo]]:
        POGGER.debug("\n\ncleanup")

        was_link_definition_started_before_close = self.__token_stack[
            -1
        ].was_link_definition_started
        was_table_started_before_close = self.__token_stack[-1].was_table_block_started

        (
            tokens_from_line,
            requeue_line_info,
        ) = TokenizedMarkdown.__close_open_blocks(
            parser_state,
            self.__tokenized_document,
            include_block_quotes=True,
            include_lists=True,
            caller_can_handle_requeue=True,
            was_forced=True,
        )
        if not self.__tokenized_document:
            self.__tokenized_document.extend(tokens_from_line)

        keep_on_going = bool(requeue_line_info and requeue_line_info.lines_to_requeue)
        did_start_close = not keep_on_going
        if keep_on_going:
            assert (
                was_link_definition_started_before_close
                or was_table_started_before_close
            ), "LRD parsing or Table parsing must have been started."
            assert (
                requeue_line_info is not None
                and not requeue_line_info.lines_to_requeue[0]
            ), "Cannot handling requeing"

            del requeue_line_info.lines_to_requeue[0]
            line_number -= 1

            tokens_from_line = []
        return (
            True,
            did_start_close,
            tokens_from_line,
            line_number,
            keep_on_going,
            requeue_line_info,
        )

    # pylint: disable=too-many-arguments
    def __main_pass_did_not_start_close(
        self,
        parser_state: ParserState,
        position_marker: PositionMarker,
        next_line_in_document: str,
        ignore_link_definition_start: bool,
        ignore_table_start: bool,
    ) -> Tuple[Optional[List[MarkdownToken]], Optional[RequeueLineInfo]]:
        POGGER.debug(">>>>$", self.__tokenized_document)

        if not next_line_in_document or not next_line_in_document.strip(
            Constants.ascii_whitespace
        ):
            POGGER.debug("call __parse_blocks_pass>>handle_blank_line")
            (
                tokens_from_line,
                requeue_line_info,
            ) = self.__handle_blank_line(
                parser_state,
                next_line_in_document,
                from_main_transform=True,
                position_marker=position_marker,
            )
        else:
            POGGER.debug("\n\nnormal lines")
            assert (
                self.__parse_properties is not None
            ), "Parse properties must be defined by this point."
            (
                tokens_from_line,
                _,
                _,
                requeue_line_info,
                _,
                _,
            ) = ContainerBlockProcessor.parse_line_for_container_blocks(
                parser_state,
                position_marker,
                ignore_link_definition_start,
                ignore_table_start,
                self.__parse_properties,
                0,
            )

        POGGER.debug("<<<<$", self.__tokenized_document)

        return tokens_from_line, requeue_line_info

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __main_pass_keep_on_going(
        self,
        line_number: int,
        requeue_line_info: Optional[RequeueLineInfo],
        requeue: List[str],
        tokens_from_line: List[MarkdownToken],
        did_start_close: bool,
        did_started_close: bool,
    ) -> Tuple[int, bool, bool, Optional[str], bool, bool]:
        (line_number, ignore_link_definition_start, ignore_table_start) = (
            TokenizedMarkdown.__handle_parse_increment_line(
                line_number, requeue_line_info, requeue
            )
        )

        POGGER.debug(
            "---\nbefore>>$",
            self.__tokenized_document,
        )
        POGGER.debug("before>>$", tokens_from_line)
        self.__tokenized_document.extend(tokens_from_line)
        POGGER.debug(
            "after>>$",
            self.__tokenized_document,
        )
        if requeue:
            POGGER.debug("requeue>>$", requeue)
        POGGER.debug("---")

        (
            next_line_in_document,
            did_start_close,
            did_started_close,
        ) = self.__determine_next_line_to_process(
            requeue, did_start_close, did_started_close
        )
        return (
            line_number,
            ignore_link_definition_start,
            ignore_table_start,
            next_line_in_document,
            did_start_close,
            did_started_close,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_parse_increment_line(
        line_number: int,
        requeue_line_info: Optional[RequeueLineInfo],
        requeue: List[str],
    ) -> Tuple[int, bool, bool]:
        if requeue_line_info:
            number_of_lines_to_requeue = len(requeue_line_info.lines_to_requeue)
            POGGER.debug("\n\n---lines_to_requeue>>$", number_of_lines_to_requeue)
            line_number -= number_of_lines_to_requeue - 1

            for i in requeue_line_info.lines_to_requeue:
                requeue.insert(0, i)
            ignore_link_definition_start = requeue_line_info.force_ignore_first_as_lrd
            ignore_table_start = requeue_line_info.force_ignore_first_as_table
        else:
            ignore_link_definition_start = False
            ignore_table_start = False
            line_number += 1
        POGGER.debug("line_number>>$\n---", line_number)

        return line_number, ignore_link_definition_start, ignore_table_start

    def __determine_next_line_to_process(
        self, requeue: List[str], did_start_close: bool, did_started_close: bool
    ) -> Tuple[Optional[str], bool, bool]:
        """
        For the parse_blocks_pass function, determine the next token to parse.
        """

        next_line_in_document: Optional[str] = None
        if requeue:
            POGGER.debug(">>Requeues present")
            next_line_in_document = requeue[0]
            del requeue[0]
            POGGER.debug(">>Requeue>>$", next_line_in_document)
            POGGER.debug(">>Requeues left>>$", requeue)
        elif did_started_close:
            did_start_close = True
        else:
            assert (
                self.__source_provider is not None
            ), "Source provider must be defined by this point."
            next_line_in_document = self.__source_provider.get_next_line()
            if next_line_in_document is None:
                did_start_close = True

        return next_line_in_document, did_start_close, did_started_close

    @staticmethod
    def __close_open_blocks_log_args(
        include_block_quotes: bool,
        include_lists: bool,
        until_this_index: int,
        caller_can_handle_requeue: bool,
        was_forced: bool,
    ) -> None:
        if include_block_quotes:
            POGGER.debug("cob-include_block_quotes>>$", include_block_quotes)
        if include_lists:
            POGGER.debug("cob-include_lists>>$", include_lists)
        if until_this_index != -1:
            POGGER.debug("cob-until_this_index>>$", until_this_index)
        if caller_can_handle_requeue:
            POGGER.debug("cob-caller_can_handle_requeue>>$", caller_can_handle_requeue)
        if was_forced:
            POGGER.debug("cob-was_forced>>$", was_forced)

    # pylint: disable=too-many-arguments
    @staticmethod
    def __close_open_blocks(  # noqa: C901
        parser_state: ParserState,
        destination_array: Optional[List[MarkdownToken]] = None,
        only_these_blocks: Optional[List[type]] = None,
        include_block_quotes: bool = False,
        include_lists: bool = False,
        until_this_index: int = -1,
        caller_can_handle_requeue: bool = False,
        requeue_reset: bool = False,
        was_forced: bool = False,
    ) -> Tuple[List[MarkdownToken], Optional[RequeueLineInfo]]:
        """
        Close any open blocks that are currently on the stack.
        """

        requeue_line_info = None
        new_tokens = destination_array or []
        POGGER.debug("cob-start>>$", parser_state.token_stack)
        POGGER.debug(
            "cob-start>>$",
            parser_state.token_document,
        )
        if only_these_blocks:
            POGGER.debug("cob-only_these_blocks>>$", only_these_blocks)
        TokenizedMarkdown.__close_open_blocks_log_args(
            include_block_quotes,
            include_lists,
            until_this_index,
            caller_can_handle_requeue,
            was_forced,
        )
        while not parser_state.token_stack[-1].is_document:
            was_close_forced = was_forced

            (
                can_continue,
                adjusted_tokens,
                requeue_line_info,
                was_close_forced,
            ) = TokenizedMarkdown.__process_next_close_element(
                parser_state,
                was_close_forced,
                caller_can_handle_requeue,
                until_this_index,
                include_lists,
                include_block_quotes,
                only_these_blocks,
            )
            new_tokens.extend(adjusted_tokens)
            if not can_continue:
                break

        POGGER.debug("cob-end>>$", parser_state.token_stack)
        POGGER.debug("cob-end>>$", parser_state.token_document)
        POGGER.debug("cob-end>>new_tokens>>$", new_tokens)
        if caller_can_handle_requeue:
            TokenizedMarkdown.__log_requeue(
                requeue_line_info, requeue_reset, parser_state
            )
        return new_tokens, requeue_line_info

    # pylint: enable=too-many-arguments
    @staticmethod
    def __log_requeue(
        requeue_line_info: Optional[RequeueLineInfo],
        requeue_reset: bool,
        parser_state: ParserState,
    ) -> None:
        if not requeue_line_info:
            POGGER.debug("requeue_line_info>>no requeue")
            return
        POGGER.debug(
            "cob>>lines_to_requeue>>$",
            requeue_line_info.lines_to_requeue,
        )
        if requeue_reset:
            assert (
                parser_state.original_line_to_parse is not None
            ), "Original line to parse must be defined by this point."
            POGGER.debug(
                "cob>>original_line_to_parse>$>", parser_state.original_line_to_parse
            )
            # assert not requeue_line_info.lines_to_requeue[
            #     0
            # ], "Resetting implies something must have been there to reset."
            requeue_line_info.lines_to_requeue[0] = parser_state.original_line_to_parse
            POGGER.debug(
                "cob>>(adjusted)lines_to_requeue>>$",
                requeue_line_info.lines_to_requeue,
            )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_next_close_element(
        parser_state: ParserState,
        was_close_forced: bool,
        caller_can_handle_requeue: bool,
        until_this_index: int,
        include_lists: bool,
        include_block_quotes: bool,
        only_these_blocks: Optional[List[type]],
    ) -> Tuple[bool, List[MarkdownToken], Optional[RequeueLineInfo], bool]:
        requeue_line_info = None

        POGGER.debug("cob>>$", parser_state.token_stack)
        can_continue, was_close_forced = TokenizedMarkdown.__can_close_continue(
            parser_state,
            only_these_blocks,
            include_block_quotes,
            include_lists,
            until_this_index,
            was_close_forced,
        )
        POGGER.debug("can_continue>>$", can_continue)
        POGGER.debug("was_close_forced>>$", was_close_forced)
        if can_continue:
            if parser_state.token_stack[-1].was_link_definition_started:
                (
                    can_continue,
                    adjusted_tokens,
                    requeue_line_info,
                ) = TokenizedMarkdown.__close_open_blocks_lrd(
                    parser_state, caller_can_handle_requeue
                )
            elif parser_state.token_stack[-1].was_table_block_started:
                (
                    can_continue,
                    adjusted_tokens,
                    requeue_line_info,
                ) = TokenizedMarkdown.__close_open_blocks_table(
                    parser_state, caller_can_handle_requeue
                )
            else:
                adjusted_tokens = TokenizedMarkdown.__close_open_blocks_normal(
                    parser_state, was_close_forced
                )
        else:
            adjusted_tokens = []
        return can_continue, adjusted_tokens, requeue_line_info, was_close_forced

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __can_close_continue(
        parser_state: ParserState,
        only_these_blocks: Optional[List[type]],
        include_block_quotes: bool,
        include_lists: bool,
        until_this_index: int,
        was_close_forced: bool,
    ) -> Tuple[bool, bool]:
        can_continue = True
        if only_these_blocks:
            POGGER.debug("cob-only-type>>$", only_these_blocks)
            POGGER.debug("cob-only-type>>$", type(parser_state.token_stack[-1]))
            can_continue = type(parser_state.token_stack[-1]) in only_these_blocks
            if not can_continue:
                POGGER.debug("cob>>not in only")
        elif not include_block_quotes and parser_state.token_stack[-1].is_block_quote:
            POGGER.debug("cob>>not block quotes")
            can_continue = False
        elif not include_lists and parser_state.token_stack[-1].is_list:
            POGGER.debug("cob>>not lists")
            can_continue = False
        elif until_this_index != -1:
            token_stack_size = len(parser_state.token_stack)
            POGGER.debug(
                "NOT ME!!!!$<<$<<",
                until_this_index,
                token_stack_size,
            )
            if until_this_index >= token_stack_size:
                can_continue = False
            else:
                was_close_forced = True

        POGGER.debug("cob>>can_continue=$", can_continue)
        POGGER.debug("cob>>was_close_forced=$", was_close_forced)
        return can_continue, was_close_forced

    # pylint: enable=too-many-arguments

    @staticmethod
    def __close_open_blocks_normal(
        parser_state: ParserState, was_close_forced: bool
    ) -> List[MarkdownToken]:
        POGGER.debug(
            "cob-rem>>$",
            parser_state.token_document,
        )
        adjusted_tokens = TokenizedMarkdown.__remove_top_element_from_stack(
            parser_state, was_close_forced
        )
        POGGER.debug(
            "cob-rem<<$",
            parser_state.token_document,
        )
        POGGER.debug("cob-adj<<$", adjusted_tokens)
        return adjusted_tokens

    @staticmethod
    def __close_open_blocks_lrd(
        parser_state: ParserState, caller_can_handle_requeue: bool
    ) -> Tuple[bool, List[MarkdownToken], Optional[RequeueLineInfo]]:
        POGGER.debug("cob->process_link_reference_definition>>stopping link definition")
        empty_position_marker = PositionMarker(-1, 0, "")
        (
            outer_processed,
            did_complete_lrd,
            did_pause_lrd,
            requeue_line_info,
            adjusted_tokens,
        ) = LinkReferenceDefinitionHelper.process_link_reference_definition(
            parser_state, empty_position_marker, "", "", "", 0, 0, "", 1
        )

        POGGER.debug("BOOOM: caller_can_handle_requeue=$", caller_can_handle_requeue)
        can_continue = not (
            caller_can_handle_requeue
            and requeue_line_info
            and requeue_line_info.lines_to_requeue
        )
        if not can_continue:
            POGGER.debug("BOOOM-->break")
        else:
            assert not (
                requeue_line_info and requeue_line_info.lines_to_requeue
            ), "Cannot requeue at this point."
            POGGER.debug(
                "cob->process_link_reference_definition>>outer_processed>>$",
                outer_processed,
            )
            POGGER.debug(
                "cob->process_link_reference_definition>>did_complete_lrd>>$",
                did_complete_lrd,
            )
            POGGER.debug(
                "cob->process_link_reference_definition>>adjusted_tokens>>$",
                adjusted_tokens,
            )
            assert not did_pause_lrd, "LRD parsing must not be paused."
        return can_continue, adjusted_tokens, requeue_line_info

    @staticmethod
    def __close_open_blocks_table(
        parser_state: ParserState, caller_can_handle_requeue: bool
    ) -> Tuple[bool, List[MarkdownToken], Optional[RequeueLineInfo]]:
        POGGER.debug("cob->process_table>>stopping table")
        empty_position_marker = PositionMarker(-1, 0, "")
        (
            outer_processed,
            did_complete_table,
            did_pause_table,
            requeue_line_info,
            adjusted_tokens,
        ) = TableBlockHelper.process_table_rows(
            parser_state, empty_position_marker, "", "", "", 0, 0, "", 1
        )

        POGGER.debug("BOOOM: caller_can_handle_requeue=$", caller_can_handle_requeue)
        can_continue = not (
            caller_can_handle_requeue
            and requeue_line_info
            and requeue_line_info.lines_to_requeue
        )
        if not can_continue:
            POGGER.debug("BOOOM-->break")
        else:
            assert not (
                requeue_line_info and requeue_line_info.lines_to_requeue
            ), "Cannot requeue at this point."
            POGGER.debug(
                "cob->process_table>>outer_processed>>$",
                outer_processed,
            )
            POGGER.debug(
                "cob->process_table>>did_complete_table>>$",
                did_complete_table,
            )
            POGGER.debug(
                "cob->process_table>>adjusted_tokens>>$",
                adjusted_tokens,
            )
            assert not did_pause_table, "Table parsing must not be paused."
        return can_continue, adjusted_tokens, requeue_line_info

    @staticmethod
    def __remove_top_element_from_stack(
        parser_state: ParserState, was_forced: bool
    ) -> List[MarkdownToken]:
        """
        Once it is decided that we need to remove the top element from the stack,
        make sure to do it uniformly.
        """

        POGGER.debug("cob->top_element->$", parser_state.token_stack[-1])
        POGGER.debug("cob->was_forced->$", was_forced)
        extra_elements = []
        extra_end_data = None
        if parser_state.token_stack[-1].is_indented_code_block:
            extra_elements.extend(
                LeafBlockHelper.extract_markdown_tokens_back_to_blank_line(
                    parser_state, was_forced
                )
            )
        elif parser_state.token_stack[-1].is_fenced_code_block:
            extra_end_data = ":"

        new_tokens = [
            parser_state.token_stack[-1].generate_close_markdown_token_from_stack_token(
                was_forced=was_forced, extra_end_data=extra_end_data
            ),
            *extra_elements,
        ]

        del parser_state.token_stack[-1]
        return new_tokens

    @staticmethod
    def __handle_blank_line_init(
        from_main_transform: bool, input_line: str
    ) -> Tuple[Optional[List[type]], bool, int, str]:
        do_include_block_quotes = from_main_transform
        close_only_these_blocks: Optional[List[type]] = (
            None if from_main_transform else [ParagraphStackToken]
        )

        POGGER.debug("hbl>>from_main_transform>>$", from_main_transform)
        POGGER.debug("hbl>>close_only_these_blocks>>$", close_only_these_blocks)
        POGGER.debug("hbl>>do_include_block_quotes>>$", do_include_block_quotes)

        (
            non_whitespace_index,
            extracted_whitespace,
        ) = ParserHelper.extract_ascii_whitespace_verified(input_line, 0)
        return (
            close_only_these_blocks,
            do_include_block_quotes,
            non_whitespace_index,
            extracted_whitespace,
        )

    @staticmethod
    def __handle_blank_line(
        parser_state: ParserState,
        input_line: str,
        from_main_transform: bool,
        position_marker: Optional[PositionMarker] = None,
    ) -> Tuple[Optional[List[MarkdownToken]], Optional[RequeueLineInfo]]:
        """
        Handle the processing of a blank line.
        """
        assert position_marker is not None
        parser_state.mark_start_information(position_marker)

        (
            close_only_these_blocks,
            do_include_block_quotes,
            non_whitespace_index,
            extracted_whitespace,
        ) = TokenizedMarkdown.__handle_blank_line_init(from_main_transform, input_line)

        (
            new_tokens,
            force_default_handling,
            requeue_line_info,
        ) = TokenizedMarkdown.__handle_blank_line_token_stack(parser_state)
        if requeue_line_info:
            return new_tokens, requeue_line_info

        if from_main_transform:
            POGGER.debug("hbl>>__handle_blank_line_in_block_quote")
            TokenizedMarkdown.__handle_blank_line_in_block_quote(
                parser_state, new_tokens
            )
            new_tokens = TokenizedMarkdown.__handle_blank_line_close_first_quote(
                parser_state, new_tokens
            )

        if force_default_handling or new_tokens is None:
            POGGER.debug("hbl>>default blank handling-->cob")
            n_tokens, _ = TokenizedMarkdown.__close_open_blocks(
                parser_state,
                only_these_blocks=close_only_these_blocks,
                include_block_quotes=do_include_block_quotes,
                was_forced=True,
            )
            if new_tokens:
                new_tokens.extend(n_tokens)
            else:
                new_tokens = n_tokens

        list_stack_index = parser_state.find_last_list_block_on_stack()
        block_stack_index = parser_state.find_last_block_quote_on_stack()
        POGGER.debug("list_stack_index>>$", list_stack_index)
        POGGER.debug("block_stack_index>>$", block_stack_index)
        if list_stack_index > 0 and list_stack_index > block_stack_index:

            TokenizedMarkdown.__handle_blank_line_bravo(parser_state, block_stack_index)

            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[list_stack_index].matching_markdown_token,
            )
            POGGER.debug("hbl>>last_block_token>>$", list_token)
            list_token.add_leading_spaces("")
            POGGER.debug("hbl>>last_block_token>>$", list_token)

        POGGER.debug("hbl>>new_tokens>>$", new_tokens)
        assert non_whitespace_index == len(
            input_line
        ), "Index must be set to the end of the line, since processing has completed."
        new_tokens.append(BlankLineMarkdownToken(extracted_whitespace, position_marker))
        POGGER.debug("hbl>>new_tokens>>$", new_tokens)

        return new_tokens, None

    @staticmethod
    def __handle_blank_line_bravo(
        parser_state: ParserState, block_stack_index: int
    ) -> None:
        search_index = 0
        next_index = block_stack_index - 1
        while next_index > 0:
            if parser_state.token_stack[next_index].is_list:
                search_index = next_index
                break
            next_index -= 1
        if search_index:
            found_markdown_token = parser_state.token_stack[
                next_index
            ].matching_markdown_token
            assert found_markdown_token is not None
            block_copy_token = next(  # pragma: no cover
                (
                    j
                    for j in parser_state.block_copy
                    if (
                        j is not None
                        and j.line_number == found_markdown_token.line_number
                        and j.column_number == found_markdown_token.column_number
                    )
                ),
                None,
            )

            # assert on next line was if statement with rest of function in if block
            assert block_copy_token is not None
            assert found_markdown_token.is_list_start
            found_markdown_list_token = cast(
                ListStartMarkdownToken, found_markdown_token
            )
            found_markdown_token_leading_spaces = (
                found_markdown_list_token.leading_spaces
            )
            assert block_copy_token.is_list_start
            block_copy_list_token = cast(ListStartMarkdownToken, block_copy_token)
            block_copy_token_leading_spaces = block_copy_list_token.leading_spaces
            are_same = (
                found_markdown_token_leading_spaces == block_copy_token_leading_spaces
            )
            assert not are_same
            POGGER.debug(
                "__handle_blank_line_bravo>>found_markdown_list_token>>$",
                found_markdown_list_token,
            )
            found_markdown_list_token.remove_last_leading_space()
            POGGER.debug(
                "__handle_blank_line_bravo>>found_markdown_list_token>>$",
                found_markdown_list_token,
            )

    @staticmethod
    def __handle_blank_line_token_stack(
        parser_state: ParserState,
    ) -> Tuple[Optional[List[MarkdownToken]], bool, Optional[RequeueLineInfo]]:
        (
            is_processing_list,
            in_index,
        ) = LeafBlockProcessorParagraph.check_for_list_in_process(parser_state)
        # POGGER.debug(
        #     "hbl>>is_processing_list>>$>>in_index>>$>>last_stack>>$",
        #     is_processing_list,
        #     in_index,
        #     parser_state.token_stack[-1],
        # )

        requeue_line_info: Optional[RequeueLineInfo] = None
        new_tokens: Optional[List[MarkdownToken]] = None
        force_default_handling = False
        last_stack_token = None

        force_default_handling, last_stack_token, requeue_line_info, new_tokens = (
            TokenizedMarkdown.__handle_blank_line_token_stack_multiline_block(
                parser_state
            )
        )
        if not force_default_handling:
            if parser_state.token_stack[-1].is_code_block:
                if parser_state.count_of_block_quotes_on_stack():
                    POGGER.debug("hbl>>code block within block quote")
                else:
                    POGGER.debug("hbl>>code block")
                    new_tokens = []
            elif parser_state.token_stack[-1].is_html_block:
                POGGER.debug("hbl>>check_blank_html_block_end")
                new_tokens = HtmlHelper.check_blank_html_block_end(parser_state)
                POGGER.debug("hbl<<check_blank_html_block_end")
            elif (
                is_processing_list
                and parser_state.token_document[-1].is_blank_line
                and parser_state.token_document[-2].is_list_start
            ):
                POGGER.debug("hbl>>double blank in list")
                new_tokens, _ = TokenizedMarkdown.__close_open_blocks(
                    parser_state, until_this_index=in_index, include_lists=True
                )
                POGGER.debug("hbl<<double blank in list")

        if requeue_line_info and last_stack_token is not None:
            parser_state.abc(requeue_line_info, last_stack_token)

        return new_tokens, force_default_handling, requeue_line_info

    @staticmethod
    def __handle_blank_line_token_stack_multiline_block(
        parser_state: ParserState,
    ) -> Tuple[
        bool,
        Optional[StackToken],
        Optional[RequeueLineInfo],
        Optional[List[MarkdownToken]],
    ]:

        force_default_handling = False
        last_stack_token = None
        requeue_line_info: Optional[RequeueLineInfo] = None
        new_tokens: Optional[List[MarkdownToken]] = None

        if parser_state.token_stack[-1].was_link_definition_started:
            force_default_handling = True
            last_stack_token = parser_state.token_stack[-1]
            POGGER.debug(
                "hbl>>process_link_reference_definition>>stopping link definition"
            )
            empty_position_marker = PositionMarker(-1, 0, "")
            assert parser_state.original_line_to_parse is not None
            (
                _,
                _,
                did_pause_lrd,
                requeue_line_info,
                new_tokens,
            ) = LinkReferenceDefinitionHelper.process_link_reference_definition(
                parser_state,
                empty_position_marker,
                "",
                "",
                "",
                0,
                0,
                parser_state.original_line_to_parse,
                2,
            )
            assert not did_pause_lrd, "LRD parsing must not be paused."
            POGGER.debug(
                "hbl<<process_link_reference_definition>>stopping link definition"
            )
        elif parser_state.token_stack[-1].was_table_block_started:
            force_default_handling = True
            last_stack_token = parser_state.token_stack[-1]
            POGGER.debug("hbl>>process_table>>stopping table")
            unmod = parser_state.original_line_to_parse
            assert unmod is not None
            empty_position_marker = PositionMarker(-1, 0, "")
            (
                _,
                _,
                did_pause_lrd,
                requeue_line_info,
                new_tokens,
            ) = TableBlockHelper.process_table_rows(
                parser_state, empty_position_marker, "", "", unmod, 0, 0, "", 2
            )
            assert not did_pause_lrd, "Table parsing must not be paused."
            POGGER.debug("hbl<<process_table>>stopping table")
        return force_default_handling, last_stack_token, requeue_line_info, new_tokens

    @staticmethod
    def __handle_blank_line_close_first_quote(
        parser_state: ParserState, new_tokens: Optional[List[MarkdownToken]]
    ) -> Optional[List[MarkdownToken]]:

        stack_index = 1
        while (
            stack_index < len(parser_state.token_stack)
            and not parser_state.token_stack[stack_index].is_block_quote
        ):
            stack_index += 1

        close_tokens, _ = parser_state.close_open_blocks_fn(
            parser_state,
            include_block_quotes=True,
            include_lists=True,
            until_this_index=stack_index,
            was_forced=True,
        )
        POGGER.debug("close_tokens>>$", close_tokens)
        if new_tokens is not None:
            new_tokens.extend(close_tokens)
        elif close_tokens:
            new_tokens = close_tokens
        return new_tokens

    @staticmethod
    def __handle_blank_line_in_block_quote(
        parser_state: ParserState, new_tokens: Optional[List[MarkdownToken]]
    ) -> None:
        # assert not new_tokens or (new_tokens and not new_tokens[-1].is_link_reference_definition)
        # assert new_tokens is None or len(new_tokens) <= 1
        if new_tokens and len(new_tokens) == 1 and new_tokens[0].is_list_end:
            return
        stack_index = parser_state.find_last_container_on_stack()
        if parser_state.token_stack[stack_index].is_list:
            return
        POGGER.debug_with_visible_whitespace("new_tokens>>$", new_tokens)
        POGGER.debug("stack_index>>$", stack_index)
        if new_tokens and stack_index > 0:
            POGGER.debug_with_visible_whitespace("new_tokens[-1]>>$", new_tokens[-1])
            assert (
                new_tokens[-1].is_html_block_end
                or new_tokens[-1].is_link_reference_definition
                or new_tokens[-1].is_table_end
            ) and stack_index == (
                len(parser_state.token_stack) - 1
            ), "If here, must be in the right context."
            close_tokens, _ = parser_state.close_open_blocks_fn(
                parser_state,
                only_these_blocks=[BlockQuoteStackToken],
                include_block_quotes=True,
            )
            POGGER.debug("close_tokens>>$", close_tokens)
            new_tokens.extend(close_tokens)

        stack_index = parser_state.find_last_container_on_stack()
        POGGER.debug(
            "blank>>bq_start>>$",
            parser_state.token_stack[stack_index],
        )
        if stack_index > 0 and parser_state.token_stack[stack_index].is_block_quote:
            block_quote_token = cast(
                BlockQuoteMarkdownToken,
                parser_state.token_stack[stack_index].matching_markdown_token,
            )
            POGGER.debug("hblibq>>last_block_token>>$", block_quote_token)
            POGGER.debug(
                "hblibq>>leading_text_index>>$", block_quote_token.leading_text_index
            )
            block_quote_token.add_bleading_spaces("")
            POGGER.debug("hblibq>>last_block_token>>$", block_quote_token)
            POGGER.debug(
                "hblibq>>leading_text_index>>$", block_quote_token.leading_text_index
            )

    def __process_front_matter_header_if_present(
        self,
        first_line_in_document: Optional[str],
        line_number: int,
        requeue: List[str],
    ) -> Tuple[Optional[str], int, List[str]]:
        assert self.__source_provider, "Source provider must be defined by this point."
        assert (
            self.__parse_properties
        ), "Parse properties must be defined by this point."
        POGGER.debug(
            "is_front_matter_enabled>>$",
            self.__parse_properties.is_front_matter_enabled,
        )
        if (
            first_line_in_document is not None
            and self.__parse_properties.is_front_matter_enabled
        ):
            assert (
                self.__extension_manager is not None
            ), "Extension manager must be initialized by this point."
            raw_extension = self.__extension_manager.get_extension_instance(
                FrontMatterExtension().get_identifier()
            )
            front_matter_extension = cast(FrontMatterExtension, raw_extension)
            (
                first_line_in_document,
                line_number,
                requeue,
            ) = front_matter_extension.process_header_if_present(
                first_line_in_document,
                line_number,
                requeue,
                self.__source_provider,
                self.__tokenized_document,
            )
        return first_line_in_document, line_number, requeue
