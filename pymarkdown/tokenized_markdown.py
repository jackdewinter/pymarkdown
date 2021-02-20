"""
Module to provide a tokenization of a markdown-encoded string.
"""
import logging
import os

from pymarkdown.bad_tokenization_error import BadTokenizationError
from pymarkdown.coalesce_processor import CoalesceProcessor
from pymarkdown.container_block_processor import ContainerBlockProcessor
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.inline_processor import InlineProcessor
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.leaf_markdown_token import BlankLineMarkdownToken
from pymarkdown.link_helper import LinkHelper
from pymarkdown.link_reference_definition_helper import LinkReferenceDefinitionHelper
from pymarkdown.parser_helper import ParserHelper, ParserState, PositionMarker
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.source_providers import InMemorySourceProvider
from pymarkdown.stack_token import DocumentStackToken, ParagraphStackToken

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class TokenizedMarkdown:
    """
    Class to provide a tokenization of a markdown-encoded string.
    """

    def __init__(self, resource_path=None):
        """
        Initializes a new instance of the TokenizedMarkdown class.
        """

        self.tokenized_document, self.stack, self.source_provider = None, None, None

        if not resource_path:
            resource_path = os.path.join(os.path.split(__file__)[0], "resources")
        InlineHelper.initialize(resource_path)

    def transform_from_provider(self, source_provider):
        """
        Transform the data from the source provider into a Markdown token stream.
        """
        self.source_provider = source_provider
        return self.__transform()

    def transform(self, your_text_string, show_debug=False):
        """
        Transform a text string in a Markdown format into a Markdown token stream.
        This function should only be used as a simplified manner of accessing the
        functionality for the purposes of testing.
        """

        root_logger = logging.getLogger()
        if show_debug:
            root_logger.setLevel(logging.DEBUG)
        else:
            root_logger.setLevel(logging.WARNING)
        self.source_provider = InMemorySourceProvider(your_text_string)
        return self.__transform()

    def __transform(self):
        """
        Transform a markdown-encoded string into an array of tokens.
        """
        try:
            self.tokenized_document, self.stack = None, []

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

    # pylint: disable=too-many-statements,too-many-locals,too-many-branches
    def __parse_blocks_pass(self):
        """
        The first pass at the tokens is to deal with blocks.
        """

        self.stack = [DocumentStackToken()]

        self.tokenized_document = []
        token_to_use = self.source_provider.get_next_line()
        did_start_close = False
        did_started_close = False
        requeue = []
        ignore_link_definition_start = False
        POGGER.debug("---$---", token_to_use)
        POGGER.debug("---")
        line_number = 1
        try:
            keep_on_going = True
            while keep_on_going:
                POGGER.debug("next-line>>$", token_to_use)
                POGGER.debug("stack>>$", self.stack)
                POGGER.debug("current_block>>$", self.stack[-1])
                POGGER.debug("line_number>>$", line_number)
                POGGER.debug("---")

                position_marker = PositionMarker(line_number, 0, token_to_use)
                parser_state = ParserState(
                    self.stack,
                    self.tokenized_document,
                    TokenizedMarkdown.__close_open_blocks,
                    self.__handle_blank_line,
                )
                if did_start_close:
                    POGGER.debug("\n\ncleanup")

                    was_link_definition_started_before_close = self.stack[
                        -1
                    ].was_link_definition_started

                    did_started_close = True
                    (
                        tokens_from_line,
                        requeue_line_info,
                    ) = TokenizedMarkdown.__close_open_blocks(
                        parser_state,
                        self.tokenized_document,
                        include_block_quotes=True,
                        include_lists=True,
                        caller_can_handle_requeue=True,
                        was_forced=True,
                    )
                    if tokens_from_line and not self.tokenized_document:
                        self.tokenized_document.extend(tokens_from_line)

                    if not (requeue_line_info and requeue_line_info.lines_to_requeue):
                        keep_on_going = False
                    else:
                        assert was_link_definition_started_before_close
                        assert not requeue_line_info.lines_to_requeue[0]

                        del requeue_line_info.lines_to_requeue[0]
                        line_number -= 1

                        did_start_close = False
                        tokens_from_line = None
                else:
                    POGGER.debug(">>>>$", self.tokenized_document)

                    if not token_to_use or not token_to_use.strip():
                        POGGER.debug("call __parse_blocks_pass>>handle_blank_line")
                        (
                            tokens_from_line,
                            requeue_line_info,
                        ) = self.__handle_blank_line(
                            parser_state,
                            token_to_use,
                            from_main_transform=True,
                            position_marker=position_marker,
                        )
                    else:
                        POGGER.debug("\n\nnormal lines")
                        (
                            tokens_from_line,
                            _,
                            requeue_line_info,
                        ) = ContainerBlockProcessor.parse_line_for_container_blocks(
                            parser_state,
                            position_marker,
                            ignore_link_definition_start,
                        )

                    POGGER.debug("<<<<$", self.tokenized_document)

                if keep_on_going:
                    line_number, ignore_link_definition_start = TokenizedMarkdown.__xx(
                        line_number, requeue_line_info, requeue
                    )

                    POGGER.debug(
                        "---\nbefore>>$",
                        self.tokenized_document,
                    )
                    POGGER.debug("before>>$", tokens_from_line)
                    if tokens_from_line:
                        self.tokenized_document.extend(tokens_from_line)
                    POGGER.debug(
                        "after>>$",
                        self.tokenized_document,
                    )
                    if requeue:
                        POGGER.debug("requeue>>$", requeue)
                    POGGER.debug("---")

                    (
                        token_to_use,
                        did_start_close,
                        did_started_close,
                    ) = self.__determine_next_token_process(
                        requeue, did_start_close, did_started_close
                    )
        except AssertionError as this_exception:
            error_message = (
                "A project assertion failed on line "
                + str(line_number)
                + " of the current document."
            )
            raise BadTokenizationError(error_message) from this_exception

        return self.tokenized_document

    # pylint: enable=too-many-statements,too-many-locals,too-many-branches

    @staticmethod
    def __xx(line_number, requeue_line_info, requeue):

        if requeue_line_info and requeue_line_info.lines_to_requeue:
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

    def __determine_next_token_process(
        self, requeue, did_start_close, did_started_close
    ):
        """
        For the parse_blocks_pass function, determine the next token to parse.
        """

        token_to_use = None
        if requeue:
            POGGER.debug(">>Requeues present")
            token_to_use = requeue[0]
            del requeue[0]
            POGGER.debug(">>Requeue>>$", token_to_use)
            POGGER.debug(">>Requeues left>>$", requeue)
        elif did_started_close:
            did_start_close = True
        else:
            token_to_use = self.source_provider.get_next_line()
            if token_to_use is None:
                did_start_close = True

        return token_to_use, did_start_close, did_started_close

    # pylint: disable=too-many-arguments,too-many-locals,too-many-statements, too-many-branches
    @staticmethod
    def __close_open_blocks(  # noqa: C901
        parser_state,
        destination_array=None,
        only_these_blocks=None,
        include_block_quotes=False,
        include_lists=False,
        until_this_index=-1,
        caller_can_handle_requeue=False,
        was_forced=False,
    ):
        """
        Close any open blocks that are currently on the stack.
        """

        new_tokens = []
        requeue_line_info = None
        if destination_array:
            new_tokens = destination_array

        POGGER.debug("cob-start>>$", parser_state.token_stack)
        POGGER.debug(
            "cob-start>>$",
            parser_state.token_document,
        )
        if destination_array:
            POGGER.debug(
                "cob-destination_array>>$",
                destination_array,
            )
        if only_these_blocks:
            POGGER.debug("cob-only_these_blocks>>$", only_these_blocks)
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
        while not parser_state.token_stack[-1].is_document:

            was_close_forced = was_forced
            POGGER.debug("cob>>$", parser_state.token_stack)
            if only_these_blocks:
                POGGER.debug("cob-only-type>>$", only_these_blocks)
                POGGER.debug("cob-only-type>>$", type(parser_state.token_stack[-1]))
                # pylint: disable=unidiomatic-typecheck
                if type(parser_state.token_stack[-1]) not in only_these_blocks:
                    POGGER.debug("cob>>not in only")
                    break
                # pylint: enable=unidiomatic-typecheck
            if not include_block_quotes and parser_state.token_stack[-1].is_block_quote:
                POGGER.debug("cob>>not block quotes")
                break
            if not include_lists and parser_state.token_stack[-1].is_list:
                POGGER.debug("cob>>not lists")
                break
            if until_this_index != -1:
                token_stack_size = len(parser_state.token_stack)
                POGGER.debug(
                    "NOT ME!!!!$<<$<<",
                    until_this_index,
                    token_stack_size,
                )
                if until_this_index >= token_stack_size:
                    break
                was_close_forced = True

            if parser_state.token_stack[-1].was_link_definition_started:
                POGGER.debug(
                    "cob->process_link_reference_definition>>stopping link definition"
                )
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
                POGGER.debug("BOOOM")
                if (
                    caller_can_handle_requeue
                    and requeue_line_info
                    and requeue_line_info.lines_to_requeue
                ):
                    POGGER.debug("BOOOM-->break")
                    break
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
            else:
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

            new_tokens.extend(adjusted_tokens)

        POGGER.debug("cob-end>>$", parser_state.token_stack)
        POGGER.debug("cob-end>>$", parser_state.token_document)
        POGGER.debug("cob-end>>new_tokens>>$", new_tokens)
        return new_tokens, requeue_line_info

    # pylint: enable=too-many-arguments,too-many-locals,too-many-statements, too-many-branches

    @staticmethod
    def __remove_top_element_from_stack(parser_state, was_forced):
        """
        Once it is decided that we need to remove the top element from the stack,
        make sure to do it uniformly.
        """

        new_tokens = []
        POGGER.debug("cob->top_element->$", parser_state.token_stack[-1])
        POGGER.debug("cob->was_forced->$", was_forced)
        extra_elements = []
        if parser_state.token_stack[-1].is_indented_code_block:
            extra_elements.extend(
                ContainerBlockProcessor.extract_markdown_tokens_back_to_blank_line(
                    parser_state, was_forced
                )
            )

        new_tokens.append(
            parser_state.token_stack[-1].generate_close_markdown_token_from_stack_token(
                was_forced=was_forced
            )
        )
        new_tokens.extend(extra_elements)
        del parser_state.token_stack[-1]
        return new_tokens

    # pylint: disable=too-many-locals, too-many-branches, too-many-statements
    @staticmethod
    def __handle_blank_line(
        parser_state,
        input_line,
        from_main_transform,
        position_marker=None,
        forced_close_until_index=None,
    ):
        """
        Handle the processing of a blank line.
        """

        if not from_main_transform:
            close_only_these_blocks = [ParagraphStackToken]
            do_include_block_quotes = False
        else:
            close_only_these_blocks = None
            do_include_block_quotes = True
        POGGER.debug("hbl>>from_main_transform>>$", from_main_transform)
        POGGER.debug("hbl>>close_only_these_blocks>>$", close_only_these_blocks)
        POGGER.debug("hbl>>do_include_block_quotes>>$", do_include_block_quotes)
        POGGER.debug("hbl>>forced_close_until_index>>$", forced_close_until_index)

        non_whitespace_index, extracted_whitespace = ParserHelper.extract_whitespace(
            input_line, 0
        )

        is_processing_list, in_index = LeafBlockProcessor.check_for_list_in_process(
            parser_state
        )
        POGGER.debug(
            "hbl>>is_processing_list>>$>>in_index>>$>>last_stack>>$",
            is_processing_list,
            in_index,
            parser_state.token_stack[-1],
        )

        requeue_line_info = None
        new_tokens = None
        force_default_handling = False
        if parser_state.token_stack[-1].was_link_definition_started:
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
            force_default_handling = True
        elif parser_state.token_stack[-1].is_code_block:
            stack_bq_count = parser_state.count_of_block_quotes_on_stack()
            if stack_bq_count:
                POGGER.debug("hbl>>code block within block quote")
            else:
                POGGER.debug("hbl>>code block")
                new_tokens = []
        elif parser_state.token_stack[-1].is_html_block:
            POGGER.debug("hbl>>check_blank_html_block_end")
            new_tokens = HtmlHelper.check_blank_html_block_end(parser_state)
        elif (
            is_processing_list
            and parser_state.token_document[-1].is_blank_line
            and parser_state.token_document[-2].is_list_start
        ):
            POGGER.debug("hbl>>double blank in list")
            new_tokens, _ = TokenizedMarkdown.__close_open_blocks(
                parser_state, until_this_index=in_index, include_lists=True
            )
        elif forced_close_until_index:
            POGGER.debug("hbl>>forced_close_until_index")
            new_tokens, _ = TokenizedMarkdown.__close_open_blocks(
                parser_state,
                until_this_index=forced_close_until_index,
                include_lists=True,
                include_block_quotes=True,
            )

        if from_main_transform:
            POGGER.debug("hbl>>__handle_blank_line_in_block_quote")
            TokenizedMarkdown.__handle_blank_line_in_block_quote(parser_state)

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

        POGGER.debug("hbl>>new_tokens>>$", new_tokens)
        assert non_whitespace_index == len(input_line)
        if not (requeue_line_info and requeue_line_info.force_ignore_first_as_lrd):
            new_tokens.append(
                BlankLineMarkdownToken(extracted_whitespace, position_marker)
            )
        POGGER.debug("hbl>>new_tokens>>$", new_tokens)

        return new_tokens, requeue_line_info

    # pylint: enable=too-many-locals, too-many-branches, too-many-statements

    @staticmethod
    def __handle_blank_line_in_block_quote(parser_state):

        stack_index = parser_state.find_last_container_on_stack()
        POGGER.debug(
            "blank>>bq_start>>$",
            parser_state.token_stack[stack_index],
        )
        if stack_index > 0 and parser_state.token_stack[stack_index].is_block_quote:
            parser_state.token_stack[
                stack_index
            ].matching_markdown_token.add_leading_spaces("")


# pylint: enable=too-few-public-methods
