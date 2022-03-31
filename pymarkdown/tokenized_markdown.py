"""
Module to provide a tokenization of a markdown-encoded string.
"""
import logging
import os
from typing import Any, Dict, List, Optional, Tuple, cast

from application_properties import ApplicationProperties

from pymarkdown.bad_tokenization_error import BadTokenizationError
from pymarkdown.coalesce_processor import CoalesceProcessor
from pymarkdown.container_block_processor import ContainerBlockProcessor
from pymarkdown.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ListStartMarkdownToken,
)
from pymarkdown.extension_manager.extension_manager import ExtensionManager
from pymarkdown.extensions.front_matter_extension import FrontMatterExtension
from pymarkdown.extensions.pragma_token import PragmaToken
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.inline_processor import InlineProcessor
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.leaf_markdown_token import BlankLineMarkdownToken
from pymarkdown.link_helper import LinkHelper
from pymarkdown.link_reference_definition_helper import LinkReferenceDefinitionHelper
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parse_block_pass_properties import ParseBlockPassProperties
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.parser_state import ParserState
from pymarkdown.position_marker import PositionMarker
from pymarkdown.requeue_line_info import RequeueLineInfo
from pymarkdown.source_providers import InMemorySourceProvider, SourceProvider
from pymarkdown.stack_token import (
    BlockQuoteStackToken,
    DocumentStackToken,
    ParagraphStackToken,
    StackToken,
)

POGGER = ParserLogger(logging.getLogger(__name__))


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

        if not resource_path:
            resource_path = os.path.join(os.path.split(__file__)[0], "resources")
        InlineHelper.initialize(resource_path)

    def apply_configuration(
        self,
        application_properties: ApplicationProperties,
        extension_manager: ExtensionManager,
    ) -> None:
        """
        Apply any configuration map.
        """
        _ = application_properties
        self.__parse_properties = ParseBlockPassProperties(extension_manager)

    def transform_from_provider(
        self, source_provider: Optional[SourceProvider]
    ) -> List[MarkdownToken]:
        """
        Transform the data from the source provider into a Markdown token stream.
        """
        self.__source_provider = source_provider
        return self.__transform()

    def transform(
        self, your_text_string: str, show_debug: bool = False
    ) -> List[MarkdownToken]:
        """
        Transform a text string in a Markdown format into a Markdown token stream.
        This function should only be used as a simplified manner of accessing the
        functionality for the purposes of testing.
        """

        logging.getLogger().setLevel(logging.DEBUG if show_debug else logging.WARNING)
        ParserLogger.sync_on_next_call()
        self.__source_provider = InMemorySourceProvider(your_text_string)
        return self.__transform()

    def __transform(self) -> List[MarkdownToken]:
        """
        Transform a markdown-encoded string into an array of tokens.
        """
        try:
            self.__tokenized_document = []
            self.__token_stack = []

            InlineProcessor.initialize()
            LinkHelper.initialize()

            POGGER.debug("\n\n>>>>>>>parse_blocks_pass>>>>>>")
            first_pass_results = self.__parse_blocks_pass()

            POGGER.debug("\n\n>>>>>>>coalesce_text_blocks>>>>>>")
            coalesced_results = CoalesceProcessor.coalesce_text_blocks(
                first_pass_results
            )

            POGGER.debug("\n\n>>>>>>>parse_inline>>>>>>")
            final_pass_results = InlineProcessor.parse_inline(coalesced_results)

            POGGER.debug("\n\n>>>>>>>final_pass_results>>>>>>")
            return final_pass_results
        except Exception as this_exception:
            raise BadTokenizationError(
                "An unhandled error occurred processing the document."
            ) from this_exception

    def __parse_blocks_pass(self) -> List[MarkdownToken]:
        """
        The first pass at the tokens is to deal with blocks.
        """

        assert self.__parse_properties is not None
        assert self.__source_provider is not None
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
            ) = (first_line_in_document is None, False, True, False)
            next_line_in_document = first_line_in_document
            while keep_on_going:
                POGGER.debug("next-line>>$", next_line_in_document)
                POGGER.debug("stack>>$", self.__token_stack)
                POGGER.debug("current_block>>$", self.__token_stack[-1])
                POGGER.debug("line_number>>$", line_number)
                POGGER.debug("---")

                parser_state = ParserState(
                    self.__token_stack,
                    self.__tokenized_document,
                    TokenizedMarkdown.__close_open_blocks,
                    self.__handle_blank_line,
                )
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
                    assert next_line_in_document is not None
                    position_marker = PositionMarker(
                        line_number, 0, next_line_in_document
                    )
                    (
                        tokens_from_line,
                        requeue_line_info,
                    ) = self.__main_pass_did_not_start_close(
                        parser_state,
                        position_marker,
                        next_line_in_document,
                        ignore_link_definition_start,
                    )

                if keep_on_going:
                    (
                        line_number,
                        ignore_link_definition_start,
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
        except AssertionError as this_exception:
            error_message = f"A project assertion failed on line {line_number} of the current document."
            raise BadTokenizationError(error_message) from this_exception

        if self.__parse_properties.pragma_lines:
            self.__tokenized_document.append(
                PragmaToken(self.__parse_properties.pragma_lines)
            )
        return self.__tokenized_document

    def __main_pass_did_start_close(
        self, parser_state: ParserState, line_number: int
    ) -> Tuple[bool, bool, List[MarkdownToken], int, bool, Optional[RequeueLineInfo]]:
        POGGER.debug("\n\ncleanup")

        was_link_definition_started_before_close = self.__token_stack[
            -1
        ].was_link_definition_started
        (tokens_from_line, requeue_line_info,) = TokenizedMarkdown.__close_open_blocks(
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
            assert was_link_definition_started_before_close
            assert requeue_line_info is not None
            assert not requeue_line_info.lines_to_requeue[0]

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

    def __main_pass_did_not_start_close(
        self,
        parser_state: ParserState,
        position_marker: PositionMarker,
        next_line_in_document: str,
        ignore_link_definition_start: bool,
    ) -> Tuple[List[MarkdownToken], Optional[RequeueLineInfo]]:
        POGGER.debug(">>>>$", self.__tokenized_document)

        if not next_line_in_document or not next_line_in_document.strip():
            POGGER.debug("call __parse_blocks_pass>>handle_blank_line")
            (tokens_from_line, requeue_line_info,) = self.__handle_blank_line(
                parser_state,
                next_line_in_document,
                from_main_transform=True,
                position_marker=position_marker,
            )
        else:
            POGGER.debug("\n\nnormal lines")
            assert self.__parse_properties is not None
            (
                tokens_from_line,
                _,
                _,
                requeue_line_info,
                _,
            ) = ContainerBlockProcessor.parse_line_for_container_blocks(
                parser_state,
                position_marker,
                ignore_link_definition_start,
                self.__parse_properties,
                0,
            )

        POGGER.debug("<<<<$", self.__tokenized_document)

        return tokens_from_line, requeue_line_info

    # pylint: disable=too-many-arguments
    def __main_pass_keep_on_going(
        self,
        line_number: int,
        requeue_line_info: Optional[RequeueLineInfo],
        requeue: List[str],
        tokens_from_line: List[MarkdownToken],
        did_start_close: bool,
        did_started_close: bool,
    ) -> Tuple[int, bool, Optional[str], bool, bool]:

        (
            line_number,
            ignore_link_definition_start,
        ) = TokenizedMarkdown.__handle_parse_increment_line(
            line_number, requeue_line_info, requeue
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
    ) -> Tuple[int, bool]:

        if requeue_line_info:
            number_of_lines_to_requeue = len(requeue_line_info.lines_to_requeue)
            POGGER.debug("\n\n---lines_to_requeue>>$", number_of_lines_to_requeue)
            line_number -= number_of_lines_to_requeue - 1

            for i in requeue_line_info.lines_to_requeue:
                requeue.insert(0, i)
            ignore_link_definition_start = requeue_line_info.force_ignore_first_as_lrd
        else:
            ignore_link_definition_start = False
            line_number += 1
        POGGER.debug("line_number>>$\n---", line_number)

        return line_number, ignore_link_definition_start

    def __determine_next_line_to_process(
        self, requeue: Optional[Any], did_start_close: bool, did_started_close: bool
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
            assert self.__source_provider is not None
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
            if not can_continue:
                break

            new_tokens.extend(adjusted_tokens)

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
            assert parser_state.original_line_to_parse is not None
            POGGER.debug(
                "cob>>original_line_to_parse>$>", parser_state.original_line_to_parse
            )
            assert not requeue_line_info.lines_to_requeue[0]
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
        if can_continue:
            if parser_state.token_stack[-1].was_link_definition_started:
                (
                    can_continue,
                    adjusted_tokens,
                    requeue_line_info,
                ) = TokenizedMarkdown.__close_open_blocks_lrd(
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
            parser_state, empty_position_marker, "", "", "", 0, 0
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
            assert not (requeue_line_info and requeue_line_info.lines_to_requeue)
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
            assert not did_pause_lrd
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
        if parser_state.token_stack[-1].is_indented_code_block:
            extra_elements.extend(
                ContainerBlockProcessor.extract_markdown_tokens_back_to_blank_line(
                    parser_state, was_forced
                )
            )

        new_tokens = [
            parser_state.token_stack[-1].generate_close_markdown_token_from_stack_token(
                was_forced=was_forced
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

        non_whitespace_index, extracted_whitespace = ParserHelper.extract_whitespace(
            input_line, 0
        )
        assert extracted_whitespace is not None
        assert non_whitespace_index is not None
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
    ) -> Tuple[List[MarkdownToken], Optional[RequeueLineInfo]]:
        """
        Handle the processing of a blank line.
        """

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

        if from_main_transform:
            POGGER.debug("hbl>>__handle_blank_line_in_block_quote")
            TokenizedMarkdown.__handle_blank_line_in_block_quote(
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
            list_token = cast(
                ListStartMarkdownToken,
                parser_state.token_stack[list_stack_index].matching_markdown_token,
            )
            POGGER.debug("hbl>>last_block_token>>$", list_token)
            list_token.add_leading_spaces("")
            POGGER.debug("hbl>>last_block_token>>$", list_token)

        POGGER.debug("hbl>>new_tokens>>$", new_tokens)
        assert non_whitespace_index == len(input_line)
        if not (requeue_line_info and requeue_line_info.force_ignore_first_as_lrd):
            new_tokens.append(
                BlankLineMarkdownToken(extracted_whitespace, position_marker)
            )
        POGGER.debug("hbl>>new_tokens>>$", new_tokens)

        return new_tokens, requeue_line_info

    @staticmethod
    def __handle_blank_line_token_stack(
        parser_state: ParserState,
    ) -> Tuple[Optional[List[MarkdownToken]], bool, Optional[RequeueLineInfo]]:
        is_processing_list, in_index = LeafBlockProcessor.check_for_list_in_process(
            parser_state
        )
        POGGER.debug(
            "hbl>>is_processing_list>>$>>in_index>>$>>last_stack>>$",
            is_processing_list,
            in_index,
            parser_state.token_stack[-1],
        )

        requeue_line_info: Optional[RequeueLineInfo] = None
        new_tokens: Optional[List[MarkdownToken]] = None
        force_default_handling: bool = parser_state.token_stack[
            -1
        ].was_link_definition_started
        if force_default_handling:
            POGGER.debug(
                "hbl>>process_link_reference_definition>>stopping link definition"
            )
            empty_position_marker = PositionMarker(-1, 0, "")
            (
                _,
                _,
                did_pause_lrd,
                requeue_line_info,
                new_tokens,
            ) = LinkReferenceDefinitionHelper.process_link_reference_definition(
                parser_state, empty_position_marker, "", "", "", 0, 0
            )
            assert not did_pause_lrd
            POGGER.debug(
                "hbl<<process_link_reference_definition>>stopping link definition"
            )
        elif parser_state.token_stack[-1].is_code_block:
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
        return new_tokens, force_default_handling, requeue_line_info

    @staticmethod
    def __handle_blank_line_in_block_quote(
        parser_state: ParserState, new_tokens: Optional[List[MarkdownToken]]
    ) -> None:

        stack_index = parser_state.find_last_container_on_stack()
        POGGER.debug_with_visible_whitespace("new_tokens>>$", new_tokens)
        POGGER.debug("stack_index>>$", stack_index)
        if new_tokens and stack_index > 0:
            POGGER.debug_with_visible_whitespace("new_tokens[-1]>>$", new_tokens[-1])
            assert new_tokens[-1].is_html_block_end and stack_index == (
                len(parser_state.token_stack) - 1
            )
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
            block_quote_token.add_leading_spaces("")
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
        assert self.__source_provider
        assert self.__parse_properties
        POGGER.debug(
            "is_front_matter_enabled>>$",
            self.__parse_properties.is_front_matter_enabled,
        )
        if (
            first_line_in_document is not None
            and self.__parse_properties.is_front_matter_enabled
        ):
            (
                first_line_in_document,
                line_number,
                requeue,
            ) = FrontMatterExtension.process_header_if_present(
                first_line_in_document,
                line_number,
                requeue,
                self.__source_provider,
                self.__tokenized_document,
            )
        return first_line_in_document, line_number, requeue
