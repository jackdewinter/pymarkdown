"""
Module to provide a tokenization of a markdown-encoded string.
"""
import os

from pymarkdown.block_quote_processor import BlockQuoteProcessor
from pymarkdown.coalesce_processor import CoalesceProcessor
from pymarkdown.container_block_processor import ContainerBlockProcessor
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.inline_helper import InlineHelper
from pymarkdown.inline_processor import InlineProcessor
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.link_helper import LinkHelper
from pymarkdown.link_reference_definition_helper import LinkReferenceDefinitionHelper
from pymarkdown.markdown_token import BlankLineMarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.source_providers import InMemorySourceProvider
from pymarkdown.stack_token import DocumentStackToken, ParagraphStackToken


# pylint: disable=too-few-public-methods
class TokenizedMarkdown:
    """
    Class to provide a tokenization of a markdown-encoded string.
    """

    def __init__(self):
        """
        Initializes a new instance of the TokenizedMarkdown class.
        """
        self.tokenized_document = None
        self.stack = []
        self.resource_path = os.path.join(os.path.split(__file__)[0], "resources")
        self.source_provider = None

    def transform(self, your_text_string):
        """
        Transform a markdown-encoded string into an array of tokens.
        """
        InlineHelper.initialize(self.resource_path)
        InlineProcessor.initialize()
        LinkHelper.initialize()
        self.source_provider = InMemorySourceProvider(your_text_string)

        print("\n\n>>>>>>>parse_blocks_pass>>>>>>")
        first_pass_results = self.__parse_blocks_pass()

        print("\n\n>>>>>>>coalesce_text_blocks>>>>>>")
        coalesced_results = CoalesceProcessor.coalesce_text_blocks(first_pass_results)

        print("\n\n>>>>>>>parse_inline>>>>>>")
        final_pass_results = InlineProcessor.parse_inline(coalesced_results)

        print("\n\n>>>>>>>final_pass_results>>>>>>")
        return final_pass_results

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
        print("---" + str(token_to_use) + "---")
        print("---")
        while True:
            print("next-line>>" + str(token_to_use))
            print("stack>>" + str(self.stack))
            print("current_block>>" + str(self.stack[-1]))
            print("---")

            if did_start_close:
                print("\n\ncleanup")
                did_started_close = True
                (
                    _,
                    lines_to_requeue,
                    force_ignore_first_as_lrd,
                ) = self.__close_open_blocks(
                    self.tokenized_document,
                    include_block_quotes=True,
                    include_lists=True,
                    caller_can_handle_requeue=True,
                )
                if not lines_to_requeue:
                    break

                did_start_close = False
                tokens_from_line = None
                print(
                    "\n\n\n\n\n\n\n\n\n\n>>lines_to_requeue>>" + str(lines_to_requeue)
                )
            else:
                if not token_to_use or not token_to_use.strip():
                    print("\n\nblank line")
                    (
                        tokens_from_line,
                        lines_to_requeue,
                        force_ignore_first_as_lrd,
                    ) = self.__handle_blank_line(token_to_use, from_main_transform=True)
                else:
                    print("\n\nnormal lines")
                    (
                        tokens_from_line,
                        _,
                        requeue_line_info,
                    ) = ContainerBlockProcessor.parse_line_for_container_blocks(
                        self.stack,
                        self.tokenized_document,
                        self.__close_open_blocks,
                        self.__handle_blank_line,
                        token_to_use,
                        ignore_link_definition_start,
                    )
                    lines_to_requeue = requeue_line_info.lines_to_requeue
                    force_ignore_first_as_lrd = (
                        requeue_line_info.force_ignore_first_as_lrd
                    )

            if lines_to_requeue:
                for i in lines_to_requeue:
                    requeue.insert(0, i)
                ignore_link_definition_start = force_ignore_first_as_lrd
            else:
                ignore_link_definition_start = False

            print("---\nbefore>>" + str(self.tokenized_document))
            print("before>>" + str(tokens_from_line))
            if tokens_from_line:
                self.tokenized_document.extend(tokens_from_line)
            print("after>>" + str(self.tokenized_document))
            if requeue:
                print("requeue>>" + str(requeue))
            print("---")

            (
                token_to_use,
                did_start_close,
                did_started_close,
            ) = self.__determine_next_token_process(
                requeue, did_start_close, did_started_close
            )

        return self.tokenized_document

    def __determine_next_token_process(
        self, requeue, did_start_close, did_started_close
    ):
        """
        For the parse_blocks_pass function, determine the next token to parse.
        """

        token_to_use = None
        if requeue:
            print(">>Requeues present")
            token_to_use = requeue[0]
            del requeue[0]
            print(">>Requeue>>" + str(token_to_use))
            print(">>Requeues left>>" + str(requeue))
        elif did_started_close:
            did_start_close = True
        else:
            token_to_use = self.source_provider.get_next_line()
            if token_to_use is None:
                did_start_close = True

        return token_to_use, did_start_close, did_started_close

    # pylint: disable=too-many-arguments
    def __close_open_blocks(
        self,
        destination_array=None,
        only_these_blocks=None,
        include_block_quotes=False,
        include_lists=False,
        until_this_index=-1,
        caller_can_handle_requeue=False,
    ):
        """
        Close any open blocks that are currently on the stack.
        """

        new_tokens = []
        lines_to_requeue = []
        force_ignore_first_as_lrd = False
        if destination_array:
            new_tokens = destination_array

        while not self.stack[-1].is_document:
            print("cob>>" + str(self.stack))
            if only_these_blocks:
                print("cob-only-type>>" + str(only_these_blocks))
                print("cob-only-type>>" + str(type(self.stack[-1])))
                # pylint: disable=unidiomatic-typecheck
                if type(self.stack[-1]) not in only_these_blocks:
                    print("cob>>not in only")
                    break
                # pylint: enable=unidiomatic-typecheck
            if not include_block_quotes and self.stack[-1].is_block_quote:
                print("cob>>not block quotes")
                break
            if not include_lists and self.stack[-1].is_list:
                print("cob>>not lists")
                break
            if until_this_index != -1:
                print(
                    "NOT ME!!!!"
                    + str(until_this_index)
                    + "<<"
                    + str(len(self.stack))
                    + "<<"
                )
                if until_this_index >= len(self.stack):
                    break

            if self.stack[-1].was_link_definition_started:
                print(
                    "cob->process_link_reference_definition>>stopping link definition"
                )
                (
                    outer_processed,
                    did_complete_lrd,
                    did_pause_lrd,
                    lines_to_requeue,
                    force_ignore_first_as_lrd,
                ) = LinkReferenceDefinitionHelper.process_link_reference_definition(
                    self.stack, "", 0, "", ""
                )
                if caller_can_handle_requeue and lines_to_requeue:
                    break
                assert not lines_to_requeue
                print(
                    "cob->process_link_reference_definition>>outer_processed>>"
                    + str(outer_processed)
                    + ">did_complete_lrd>"
                    + str(did_complete_lrd)
                    + "<"
                )
                assert not did_pause_lrd
            else:
                adjusted_tokens = self.__remove_top_element_from_stack()
                new_tokens.extend(adjusted_tokens)
        return new_tokens, lines_to_requeue, force_ignore_first_as_lrd
        # pylint: enable=too-many-arguments

    def __remove_top_element_from_stack(self):
        """
        Once it is decided that we need to remove the top element from the stack,
        make sure to do it uniformly.
        """

        new_tokens = []
        print("cob->te->" + str(self.stack[-1]))
        extra_elements = []
        if self.stack[-1].is_indented_code_block:
            extra_elements.extend(
                ContainerBlockProcessor.extract_markdown_tokens_back_to_blank_line(
                    self.tokenized_document
                )
            )

        new_tokens.append(self.stack[-1].generate_close_token())
        new_tokens.extend(extra_elements)
        del self.stack[-1]
        return new_tokens

    def __handle_blank_line(self, input_line, from_main_transform):
        """
        Handle the processing of a blank line.
        """

        if (
            self.stack[-1].is_paragraph
            and len(self.stack) >= 2
            and self.stack[-2].is_list
        ):
            from_main_transform = False
        elif self.stack[-1].is_list:
            from_main_transform = False

        close_only_these_blocks = None
        do_include_block_quotes = True
        if not from_main_transform:
            close_only_these_blocks = [ParagraphStackToken]
            do_include_block_quotes = False
        print("from_main_transform>>" + str(from_main_transform))
        print("close_only_these_blocks>>" + str(close_only_these_blocks))
        print("do_include_block_quotes>>" + str(do_include_block_quotes))

        non_whitespace_index, extracted_whitespace = ParserHelper.extract_whitespace(
            input_line, 0
        )

        is_processing_list, in_index = LeafBlockProcessor.check_for_list_in_process(
            self.stack
        )
        print(
            "is_processing_list>>"
            + str(is_processing_list)
            + ">>in_index>>"
            + str(in_index)
            + ">>last_stack>>"
            + str(self.stack[-1])
        )

        lines_to_requeue = []
        force_ignore_first_as_lrd = None
        new_tokens = None
        if self.stack[-1].was_link_definition_started:
            print("process_link_reference_definition>>stopping link definition")
            (
                _,
                _,
                did_pause_lrd,
                lines_to_requeue,
                force_ignore_first_as_lrd,
            ) = LinkReferenceDefinitionHelper.process_link_reference_definition(
                self.stack, "", 0, "", ""
            )
            assert not did_pause_lrd
        elif self.stack[-1].is_code_block:
            stack_bq_count = BlockQuoteProcessor.count_of_block_quotes_on_stack(
                self.stack
            )
            if stack_bq_count:
                print("hbl>>code block within block quote")
            else:
                print("hbl>>code block")
                new_tokens = []
        elif self.stack[-1].is_html_block:
            new_tokens = HtmlHelper.check_blank_html_block_end(
                self.stack, self.__close_open_blocks
            )
        elif (
            is_processing_list
            and self.tokenized_document[-1].is_blank_line
            and self.tokenized_document[-2].is_list_start
        ):
            print("double blank in list")
            new_tokens, _, _ = self.__close_open_blocks(
                until_this_index=in_index, include_lists=True
            )

        if new_tokens is None:
            new_tokens, _, _ = self.__close_open_blocks(
                only_these_blocks=close_only_these_blocks,
                include_block_quotes=do_include_block_quotes,
            )

        print("new_tokens>>" + str(new_tokens))
        assert non_whitespace_index == len(input_line)
        new_tokens.append(BlankLineMarkdownToken(extracted_whitespace))
        return new_tokens, lines_to_requeue, force_ignore_first_as_lrd


# pylint: enable=too-few-public-methods
