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
from pymarkdown.source_providers import InMemorySourceProvider
from pymarkdown.stack_token import DocumentStackToken, ParagraphStackToken

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class TokenizedMarkdown:
    """
    Class to provide a tokenization of a markdown-encoded string.
    """

    def __init__(self, resource_path=None):
        """
        Initializes a new instance of the TokenizedMarkdown class.
        """

        self.tokenized_document = None
        self.stack = None
        self.source_provider = None

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
            self.tokenized_document = None
            self.stack = []

            InlineProcessor.initialize()
            LinkHelper.initialize()

            LOGGER.debug("\n\n>>>>>>>parse_blocks_pass>>>>>>")
            first_pass_results = self.__parse_blocks_pass()

            LOGGER.debug("\n\n>>>>>>>coalesce_text_blocks>>>>>>")
            coalesced_results = CoalesceProcessor.coalesce_text_blocks(
                first_pass_results
            )

            LOGGER.debug("\n\n>>>>>>>parse_inline>>>>>>")
            final_pass_results = InlineProcessor.parse_inline(coalesced_results)

            LOGGER.debug("\n\n>>>>>>>final_pass_results>>>>>>")
            return final_pass_results
        except Exception as this_exception:
            raise BadTokenizationError() from this_exception

    # pylint: disable=too-many-statements
    def __parse_blocks_pass(self):
        """
        The first pass at the tokens is to deal with blocks.
        """

        self.stack = []
        self.stack.append(DocumentStackToken())

        self.tokenized_document = []
        token_to_use = self.source_provider.get_next_line()
        did_start_close = False
        did_started_close = False
        requeue = []
        ignore_link_definition_start = False
        LOGGER.debug("---%s---", str(token_to_use))
        LOGGER.debug("---")
        line_number = 1
        keep_on_going = True
        while keep_on_going:
            LOGGER.debug("next-line>>%s", str(token_to_use))
            LOGGER.debug("stack>>%s", str(self.stack))
            LOGGER.debug("current_block>>%s", str(self.stack[-1]))
            LOGGER.debug("line_number>>%s", str(line_number))
            LOGGER.debug("---")

            position_marker = PositionMarker(line_number, 0, token_to_use)
            parser_state = ParserState(
                self.stack,
                self.tokenized_document,
                TokenizedMarkdown.__close_open_blocks,
                self.__handle_blank_line,
            )
            if did_start_close:
                LOGGER.debug("\n\ncleanup")

                was_link_definition_started_before_close = False
                if self.stack[-1].was_link_definition_started:
                    was_link_definition_started_before_close = True

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
                LOGGER.debug(
                    ">>>>%s", ParserHelper.make_value_visible(self.tokenized_document)
                )

                if not token_to_use or not token_to_use.strip():
                    LOGGER.debug("call __parse_blocks_pass>>handle_blank_line")
                    (tokens_from_line, requeue_line_info,) = self.__handle_blank_line(
                        parser_state,
                        token_to_use,
                        from_main_transform=True,
                        position_marker=position_marker,
                    )
                else:
                    LOGGER.debug("\n\nnormal lines")
                    (
                        tokens_from_line,
                        _,
                        requeue_line_info,
                    ) = ContainerBlockProcessor.parse_line_for_container_blocks(
                        parser_state,
                        position_marker,
                        ignore_link_definition_start,
                    )

                LOGGER.debug(
                    "<<<<%s", ParserHelper.make_value_visible(self.tokenized_document)
                )

            if keep_on_going:
                line_number, ignore_link_definition_start = TokenizedMarkdown.__xx(
                    line_number, requeue_line_info, requeue
                )

                LOGGER.debug(
                    "---\nbefore>>%s",
                    ParserHelper.make_value_visible(self.tokenized_document),
                )
                LOGGER.debug(
                    "before>>%s", ParserHelper.make_value_visible(tokens_from_line)
                )
                if tokens_from_line:
                    self.tokenized_document.extend(tokens_from_line)
                LOGGER.debug(
                    "after>>%s",
                    ParserHelper.make_value_visible(self.tokenized_document),
                )
                if requeue:
                    LOGGER.debug("requeue>>%s", str(requeue))
                LOGGER.debug("---")

                (
                    token_to_use,
                    did_start_close,
                    did_started_close,
                ) = self.__determine_next_token_process(
                    requeue, did_start_close, did_started_close
                )

        return self.tokenized_document

    # pylint: enable=too-many-statements

    @staticmethod
    def __xx(line_number, requeue_line_info, requeue):

        if requeue_line_info and requeue_line_info.lines_to_requeue:
            number_of_lines_to_requeue = len(requeue_line_info.lines_to_requeue)
            LOGGER.debug("\n\n---lines_to_requeue>>%s", str(number_of_lines_to_requeue))
            line_number -= number_of_lines_to_requeue - 1

            for i in requeue_line_info.lines_to_requeue:
                requeue.insert(0, i)
            ignore_link_definition_start = requeue_line_info.force_ignore_first_as_lrd
        else:
            ignore_link_definition_start = False
            line_number += 1
        LOGGER.debug("line_number>>%s\n---", str(line_number))

        return line_number, ignore_link_definition_start

    def __determine_next_token_process(
        self, requeue, did_start_close, did_started_close
    ):
        """
        For the parse_blocks_pass function, determine the next token to parse.
        """

        token_to_use = None
        if requeue:
            LOGGER.debug(">>Requeues present")
            token_to_use = requeue[0]
            del requeue[0]
            LOGGER.debug(">>Requeue>>%s", str(token_to_use))
            LOGGER.debug(">>Requeues left>>%s", str(requeue))
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

        LOGGER.debug("cob-start>>%s", str(parser_state.token_stack))
        LOGGER.debug(
            "cob-start>>%s",
            ParserHelper.make_value_visible(parser_state.token_document),
        )
        if destination_array:
            LOGGER.debug(
                "cob-destination_array>>%s",
                ParserHelper.make_value_visible(destination_array),
            )
        if only_these_blocks:
            LOGGER.debug("cob-only_these_blocks>>%s", str(only_these_blocks))
        if include_block_quotes:
            LOGGER.debug("cob-include_block_quotes>>%s", str(include_block_quotes))
        if include_lists:
            LOGGER.debug("cob-include_lists>>%s", str(include_lists))
        if until_this_index != -1:
            LOGGER.debug("cob-until_this_index>>%s", str(until_this_index))
        if caller_can_handle_requeue:
            LOGGER.debug(
                "cob-caller_can_handle_requeue>>%s", str(caller_can_handle_requeue)
            )
        if was_forced:
            LOGGER.debug("cob-was_forced>>%s", str(was_forced))
        while not parser_state.token_stack[-1].is_document:

            was_close_forced = was_forced
            LOGGER.debug("cob>>%s", str(parser_state.token_stack))
            if only_these_blocks:
                LOGGER.debug("cob-only-type>>%s", str(only_these_blocks))
                LOGGER.debug(
                    "cob-only-type>>%s", str(type(parser_state.token_stack[-1]))
                )
                # pylint: disable=unidiomatic-typecheck
                if type(parser_state.token_stack[-1]) not in only_these_blocks:
                    LOGGER.debug("cob>>not in only")
                    break
                # pylint: enable=unidiomatic-typecheck
            if not include_block_quotes and parser_state.token_stack[-1].is_block_quote:
                LOGGER.debug("cob>>not block quotes")
                break
            if not include_lists and parser_state.token_stack[-1].is_list:
                LOGGER.debug("cob>>not lists")
                break
            if until_this_index != -1:
                LOGGER.debug(
                    "NOT ME!!!!%s<<%s<<",
                    str(until_this_index),
                    str(len(parser_state.token_stack)),
                )
                if until_this_index >= len(parser_state.token_stack):
                    break
                was_close_forced = True

            if parser_state.token_stack[-1].was_link_definition_started:
                LOGGER.debug(
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
                LOGGER.debug("BOOOM")
                if (
                    caller_can_handle_requeue
                    and requeue_line_info
                    and requeue_line_info.lines_to_requeue
                ):
                    LOGGER.debug("BOOOM-->break")
                    break
                assert not (requeue_line_info and requeue_line_info.lines_to_requeue)
                LOGGER.debug(
                    "cob->process_link_reference_definition>>outer_processed>>%s",
                    str(outer_processed),
                )
                LOGGER.debug(
                    "cob->process_link_reference_definition>>did_complete_lrd>>%s",
                    str(did_complete_lrd),
                )
                LOGGER.debug(
                    "cob->process_link_reference_definition>>adjusted_tokens>>%s",
                    str(adjusted_tokens),
                )
                assert not did_pause_lrd
            else:
                LOGGER.debug(
                    "cob-rem>>%s",
                    ParserHelper.make_value_visible(parser_state.token_document),
                )
                adjusted_tokens = TokenizedMarkdown.__remove_top_element_from_stack(
                    parser_state, was_close_forced
                )
                LOGGER.debug(
                    "cob-rem<<%s",
                    ParserHelper.make_value_visible(parser_state.token_document),
                )
                LOGGER.debug("cob-adj<<%s", str(adjusted_tokens))

            new_tokens.extend(adjusted_tokens)

        LOGGER.debug("cob-end>>%s", str(parser_state.token_stack))
        LOGGER.debug(
            "cob-end>>%s", ParserHelper.make_value_visible(parser_state.token_document)
        )
        LOGGER.debug(
            "cob-end>>new_tokens>>%s", ParserHelper.make_value_visible(new_tokens)
        )
        return new_tokens, requeue_line_info

    # pylint: enable=too-many-arguments,too-many-locals,too-many-statements, too-many-branches

    @staticmethod
    def __remove_top_element_from_stack(parser_state, was_forced):
        """
        Once it is decided that we need to remove the top element from the stack,
        make sure to do it uniformly.
        """

        new_tokens = []
        LOGGER.debug("cob->top_element->%s", str(parser_state.token_stack[-1]))
        LOGGER.debug("cob->was_forced->%s", str(was_forced))
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

        close_only_these_blocks = None
        do_include_block_quotes = True
        if not from_main_transform:
            close_only_these_blocks = [ParagraphStackToken]
            do_include_block_quotes = False
        LOGGER.debug("hbl>>from_main_transform>>%s", str(from_main_transform))
        LOGGER.debug("hbl>>close_only_these_blocks>>%s", str(close_only_these_blocks))
        LOGGER.debug("hbl>>do_include_block_quotes>>%s", str(do_include_block_quotes))
        LOGGER.debug("hbl>>forced_close_until_index>>%s", str(forced_close_until_index))

        non_whitespace_index, extracted_whitespace = ParserHelper.extract_whitespace(
            input_line, 0
        )

        is_processing_list, in_index = LeafBlockProcessor.check_for_list_in_process(
            parser_state
        )
        LOGGER.debug(
            "hbl>>is_processing_list>>%s>>in_index>>%s>>last_stack>>%s",
            str(is_processing_list),
            str(in_index),
            str(parser_state.token_stack[-1]),
        )

        requeue_line_info = None
        new_tokens = None
        force_default_handling = False
        if parser_state.token_stack[-1].was_link_definition_started:
            LOGGER.debug(
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
                LOGGER.debug("hbl>>code block within block quote")
            else:
                LOGGER.debug("hbl>>code block")
                new_tokens = []
        elif parser_state.token_stack[-1].is_html_block:
            LOGGER.debug("hbl>>check_blank_html_block_end")
            new_tokens = HtmlHelper.check_blank_html_block_end(parser_state)
        elif (
            is_processing_list
            and parser_state.token_document[-1].is_blank_line
            and parser_state.token_document[-2].is_list_start
        ):
            LOGGER.debug("hbl>>double blank in list")
            new_tokens, _ = TokenizedMarkdown.__close_open_blocks(
                parser_state, until_this_index=in_index, include_lists=True
            )
        elif forced_close_until_index:
            LOGGER.debug("hbl>>forced_close_until_index")
            new_tokens, _ = TokenizedMarkdown.__close_open_blocks(
                parser_state,
                until_this_index=forced_close_until_index,
                include_lists=True,
                include_block_quotes=True,
            )

        if from_main_transform:
            LOGGER.debug("hbl>>__handle_blank_line_in_block_quote")
            TokenizedMarkdown.__handle_blank_line_in_block_quote(parser_state)

        if force_default_handling or new_tokens is None:
            LOGGER.debug("hbl>>default blank handling-->cob")
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

        LOGGER.debug("hbl>>new_tokens>>%s", str(new_tokens))
        assert non_whitespace_index == len(input_line)
        if not (requeue_line_info and requeue_line_info.force_ignore_first_as_lrd):
            new_tokens.append(
                BlankLineMarkdownToken(extracted_whitespace, position_marker)
            )
        LOGGER.debug("hbl>>new_tokens>>%s", str(new_tokens))

        return new_tokens, requeue_line_info

    # pylint: enable=too-many-locals, too-many-branches, too-many-statements

    @staticmethod
    def __handle_blank_line_in_block_quote(parser_state):

        stack_index = parser_state.find_last_container_on_stack()
        LOGGER.debug(
            "blank>>bq_start>>%s",
            ParserHelper.make_value_visible(parser_state.token_stack[stack_index]),
        )
        if stack_index > 0 and parser_state.token_stack[stack_index].is_block_quote:
            parser_state.token_stack[
                stack_index
            ].matching_markdown_token.add_leading_spaces("")


# pylint: enable=too-few-public-methods
