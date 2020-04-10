"""
Module to provide processing for the container blocks.
"""
from pymarkdown.block_quote_processor import BlockQuoteProcessor
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.link_reference_definition_helper import LinkReferenceDefinitionHelper
from pymarkdown.list_block_processor import ListBlockProcessor
from pymarkdown.markdown_token import TextMarkdownToken
from pymarkdown.parser_helper import ParserHelper


# pylint: disable=too-few-public-methods
class ContainerIndices:
    """
    Class to provide for encapsulation on a group of container indices.
    """

    def __init__(self, ulist_index, olist_index, block_index):
        self.ulist_index = ulist_index
        self.olist_index = olist_index
        self.block_index = block_index


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class RequeueLineInfo:
    """
    Class to provide an container for lines that need to be requeued.
    """

    def __init__(self):
        self.lines_to_requeue = []
        self.force_ignore_first_as_lrd = None


# pylint: enable=too-few-public-methods


class ContainerBlockProcessor:
    """
    Class to provide processing for the container blocks.
    """

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_for_container_blocks(
        token_stack,
        token_document,
        line_to_parse,
        extracted_whitespace,
        foobar,
        init_bq,
    ):
        """
        Perform some calculations that will be needed for parsing the container blocks.
        """

        this_bq_count = 0
        if init_bq is not None:
            this_bq_count = init_bq

        current_container_blocks = []
        for ind in token_stack:
            if ind.is_list:
                current_container_blocks.append(ind)

        adj_ws = ContainerBlockProcessor.__calculate_adjusted_whitespace(
            token_stack,
            token_document,
            current_container_blocks,
            line_to_parse,
            extracted_whitespace,
            foobar=foobar,
        )

        stack_bq_count = BlockQuoteProcessor.count_of_block_quotes_on_stack(token_stack)

        return current_container_blocks, adj_ws, stack_bq_count, this_bq_count

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __calculate_adjusted_whitespace(
        token_stack,
        token_document,
        current_container_blocks,
        line_to_parse,
        extracted_whitespace,
        foobar=None,
    ):
        """
        Based on the last container on the stack, determine what the adjusted whitespace is.
        """

        adj_ws = extracted_whitespace
        stack_index = len(token_stack) - 1
        while stack_index >= 0 and not token_stack[stack_index].is_list:
            stack_index -= 1
        if stack_index < 0:
            print("PLFCB>>No Started lists")
            assert len(current_container_blocks) == 0
            if foobar is None:
                print("PLFCB>>No Started Block Quote")
            else:
                print("PLFCB>>Started Block Quote")
                adj_ws = extracted_whitespace[foobar:]
        else:
            assert len(current_container_blocks) >= 1
            print("PLFCB>>Started list-last stack>>" + str(token_stack[stack_index]))
            token_index = len(token_document) - 1

            while token_index >= 0 and not (
                token_document[token_index].is_any_list_token
            ):
                token_index -= 1
            print("PLFCB>>Started list-last token>>" + str(token_document[token_index]))
            assert token_index >= 0

            old_start_index = token_document[token_index].indent_level

            ws_len = ParserHelper.calculate_length(extracted_whitespace)
            print(
                "old_start_index>>" + str(old_start_index) + ">>ws_len>>" + str(ws_len)
            )
            if ws_len >= old_start_index:
                print("RELINE:" + line_to_parse + ":")
                adj_ws = extracted_whitespace[old_start_index:]
            else:
                print("DOWNGRADE")
        return adj_ws

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def __handle_nested_container_blocks(
        token_stack,
        token_document,
        container_depth,
        this_bq_count,
        stack_bq_count,
        no_para_start_if_empty,
        line_to_parse,
        end_container_indices,
        leaf_tokens,
        container_level_tokens,
        was_container_start,
        close_open_blocks_fn,
        handle_blank_line_fn,
    ):
        """
        Handle the processing of nested container blocks, as they can contain
        themselves and get somewhat messy.
        """

        if was_container_start and line_to_parse:
            assert container_depth < 10
            nested_container_starts = ContainerBlockProcessor.__get_nested_container_starts(
                token_stack, line_to_parse, end_container_indices,
            )

            print("check next container_start>stack>>" + str(token_stack))
            print("check next container_start>leaf_tokens>>" + str(leaf_tokens))
            print(
                "check next container_start>container_level_tokens>>"
                + str(container_level_tokens)
            )

            adj_line_to_parse = line_to_parse

            print("check next container_start>pre>>" + str(adj_line_to_parse) + "<<")
            active_container_index = max(
                end_container_indices.ulist_index,
                end_container_indices.olist_index,
                end_container_indices.block_index,
            )
            print(
                "check next container_start>max>>"
                + str(active_container_index)
                + ">>bq>>"
                + str(end_container_indices.block_index)
            )
            print(
                "^^"
                + adj_line_to_parse[0 : end_container_indices.block_index]
                + "^^"
                + adj_line_to_parse[end_container_indices.block_index :]
                + "^^"
            )
            if (
                end_container_indices.block_index != -1
                and not nested_container_starts.ulist_index
                and not nested_container_starts.olist_index
            ):  # and active_container_index == end_container_indices.block_index:
                adj_line_to_parse = adj_line_to_parse[
                    end_container_indices.block_index :
                ]

            print(
                "check next container_start>mid>>stack_bq_count>>"
                + str(stack_bq_count)
                + "<<this_bq_count<<"
                + str(this_bq_count)
            )
            adj_line_to_parse = "".rjust(active_container_index) + adj_line_to_parse
            print("check next container_start>post<<" + str(adj_line_to_parse) + "<<")

            print("leaf_tokens>>" + str(leaf_tokens))
            if leaf_tokens:
                token_document.extend(leaf_tokens)
                leaf_tokens = []
            if container_level_tokens:
                token_document.extend(container_level_tokens)
                container_level_tokens = []

            print("check next container_start>stack>>" + str(token_stack))
            print(
                "check next container_start>tokenized_document>>" + str(token_document)
            )

            if (
                nested_container_starts.ulist_index
                or nested_container_starts.olist_index
                or nested_container_starts.block_index
            ):
                line_to_parse = ContainerBlockProcessor.__look_for_container_blocks(
                    adj_line_to_parse,
                    end_container_indices.block_index,
                    token_stack,
                    token_document,
                    container_depth,
                    this_bq_count,
                    close_open_blocks_fn,
                    handle_blank_line_fn,
                )
            no_para_start_if_empty = True
        return (
            line_to_parse,
            leaf_tokens,
            container_level_tokens,
            no_para_start_if_empty,
        )
        # pylint: enable=too-many-locals, too-many-arguments

    @staticmethod
    def __get_nested_container_starts(
        token_stack, line_to_parse, end_container_indices,
    ):

        print("check next container_start>")
        nested_ulist_start, _ = ListBlockProcessor.is_ulist_start(
            token_stack, line_to_parse, 0, ""
        )
        nested_olist_start, _, _, _ = ListBlockProcessor.is_olist_start(
            token_stack, line_to_parse, 0, ""
        )
        nested_block_start = BlockQuoteProcessor.is_block_quote_start(
            line_to_parse, 0, ""
        )
        print(
            "check next container_start>ulist>"
            + str(nested_ulist_start)
            + ">index>"
            + str(end_container_indices.ulist_index)
        )
        print(
            "check next container_start>olist>"
            + str(nested_olist_start)
            + ">index>"
            + str(end_container_indices.olist_index)
        )
        print(
            "check next container_start>bquote>"
            + str(nested_block_start)
            + ">index>"
            + str(end_container_indices.block_index)
        )
        return ContainerIndices(
            nested_ulist_start, nested_olist_start, nested_block_start
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __look_for_container_blocks(
        adj_line_to_parse,
        end_of_bquote_start_index,
        token_stack,
        token_document,
        container_depth,
        this_bq_count,
        close_open_blocks_fn,
        handle_blank_line_fn,
    ):
        """
        Look for container blocks that we can use.
        """
        print("check next container_start>recursing")
        print("check next container_start>>" + adj_line_to_parse + "\n")

        adj_block = None
        if end_of_bquote_start_index != -1:
            adj_block = end_of_bquote_start_index

        print("adj_line_to_parse>>>" + str(adj_line_to_parse) + "<<<")
        (
            _,
            line_to_parse,
            requeue_line_info,
        ) = ContainerBlockProcessor.parse_line_for_container_blocks(
            token_stack,
            token_document,
            close_open_blocks_fn,
            handle_blank_line_fn,
            adj_line_to_parse,
            False,
            container_depth=container_depth + 1,
            foobar=adj_block,
            init_bq=this_bq_count,
        )
        assert not requeue_line_info or not requeue_line_info.lines_to_requeue
        # TODO will need to deal with force_ignore_first_as_lrd

        print("\ncheck next container_start>recursed")
        print("check next container_start>stack>>" + str(token_stack))
        print("check next container_start>tokenized_document>>" + str(token_document))
        print("check next container_start>line_parse>>" + str(line_to_parse))
        return line_to_parse

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    @staticmethod
    def parse_line_for_container_blocks(
        token_stack,
        token_document,
        close_open_blocks_fn,
        handle_blank_line_fn,
        line_to_parse,
        ignore_link_definition_start,
        container_depth=0,
        foobar=None,
        init_bq=None,
    ):
        """
        Parse the line, taking care to handle any container blocks before deciding
        whether or not to pass the (remaining parts of the) line to the leaf block
        processor.
        """

        print("Line:" + line_to_parse + ":")
        no_para_start_if_empty = False

        start_index, extracted_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, 0
        )

        (
            current_container_blocks,
            adj_ws,
            stack_bq_count,
            this_bq_count,
        ) = ContainerBlockProcessor.__calculate_for_container_blocks(
            token_stack,
            token_document,
            line_to_parse,
            extracted_whitespace,
            foobar,
            init_bq,
        )

        end_container_indices = ContainerIndices(-1, -1, -1)
        (
            did_process,
            was_container_start,
            end_container_indices.block_index,
            this_bq_count,
            stack_bq_count,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
        ) = BlockQuoteProcessor.handle_block_quote_block(
            token_stack,
            line_to_parse,
            start_index,
            extracted_whitespace,
            adj_ws,
            this_bq_count,
            stack_bq_count,
            close_open_blocks_fn,
            handle_blank_line_fn,
        )

        (
            did_process,
            was_container_start,
            end_container_indices.ulist_index,
            no_para_start_if_empty,
            line_to_parse,
            resultant_tokens,
        ) = ListBlockProcessor.handle_ulist_block(
            token_stack,
            token_document,
            did_process,
            was_container_start,
            no_para_start_if_empty,
            line_to_parse,
            start_index,
            extracted_whitespace,
            adj_ws,
            stack_bq_count,
            this_bq_count,
            current_container_blocks,
            close_open_blocks_fn,
        )
        container_level_tokens.extend(resultant_tokens)

        (
            did_process,
            was_container_start,
            end_container_indices.olist_index,
            no_para_start_if_empty,
            line_to_parse,
            resultant_tokens,
        ) = ListBlockProcessor.handle_olist_block(
            token_stack,
            token_document,
            did_process,
            was_container_start,
            no_para_start_if_empty,
            line_to_parse,
            start_index,
            extracted_whitespace,
            adj_ws,
            stack_bq_count,
            this_bq_count,
            current_container_blocks,
            close_open_blocks_fn,
        )
        container_level_tokens.extend(resultant_tokens)

        (
            line_to_parse,
            leaf_tokens,
            container_level_tokens,
            no_para_start_if_empty,
        ) = ContainerBlockProcessor.__handle_nested_container_blocks(
            token_stack,
            token_document,
            container_depth,
            this_bq_count,
            stack_bq_count,
            no_para_start_if_empty,
            line_to_parse,
            end_container_indices,
            leaf_tokens,
            container_level_tokens,
            was_container_start,
            close_open_blocks_fn,
            handle_blank_line_fn,
        )

        if container_depth:
            assert not leaf_tokens
            print(">>>>>>>>" + line_to_parse + "<<<<<<<<<<")
            return container_level_tokens, line_to_parse, None

        (
            did_process,
            line_to_parse,
            container_level_tokens,
        ) = ContainerBlockProcessor.__process_list_in_progress(
            did_process,
            token_stack,
            token_document,
            line_to_parse,
            start_index,
            container_level_tokens,
            extracted_whitespace,
            close_open_blocks_fn,
        )
        ContainerBlockProcessor.__process_lazy_lines(
            leaf_tokens,
            token_stack,
            this_bq_count,
            stack_bq_count,
            line_to_parse,
            extracted_whitespace,
            did_process,
            container_level_tokens,
            close_open_blocks_fn,
        )
        leaf_tokens, requeue_line_info = ContainerBlockProcessor.__process_leaf_tokens(
            token_stack,
            leaf_tokens,
            token_document,
            line_to_parse,
            this_bq_count,
            no_para_start_if_empty,
            ignore_link_definition_start,
            close_open_blocks_fn,
        )

        container_level_tokens.extend(leaf_tokens)
        print(
            "clt-end>>"
            + str(len(container_level_tokens))
            + ">>"
            + str(container_level_tokens)
            + "<<"
        )
        return container_level_tokens, line_to_parse, requeue_line_info
        # pylint: enable=too-many-locals
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_list_in_progress(
        did_process,
        token_stack,
        token_document,
        line_to_parse,
        start_index,
        container_level_tokens,
        extracted_whitespace,
        close_open_blocks_fn,
    ):
        if not did_process:
            is_list_in_process, ind = LeafBlockProcessor.check_for_list_in_process(
                token_stack
            )
            if is_list_in_process:
                assert not container_level_tokens
                print("clt>>list-in-progress")
                (
                    container_level_tokens,
                    line_to_parse,
                ) = ListBlockProcessor.list_in_process(
                    token_stack,
                    token_document,
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    ind,
                    close_open_blocks_fn,
                )
                did_process = True

        if did_process:
            print(
                "clt-before-lead>>"
                + str(len(container_level_tokens))
                + ">>"
                + str(container_level_tokens)
            )
        return did_process, line_to_parse, container_level_tokens

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_lazy_lines(
        leaf_tokens,
        token_stack,
        this_bq_count,
        stack_bq_count,
        line_to_parse,
        extracted_whitespace,
        did_process,
        container_level_tokens,
        close_open_blocks_fn,
    ):

        print("LINE-lazy>" + line_to_parse)
        if not leaf_tokens:
            print("clt>>lazy-check")
            lazy_tokens = BlockQuoteProcessor.check_for_lazy_handling(
                token_stack,
                this_bq_count,
                stack_bq_count,
                line_to_parse,
                extracted_whitespace,
                close_open_blocks_fn,
            )
            if lazy_tokens:
                print("clt>>lazy-found")
                container_level_tokens.extend(lazy_tokens)
                did_process = True

        if did_process:
            print(
                "clt-after-leaf>>"
                + str(len(container_level_tokens))
                + ">>"
                + str(container_level_tokens)
            )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_leaf_tokens(
        token_stack,
        leaf_tokens,
        token_document,
        line_to_parse,
        this_bq_count,
        no_para_start_if_empty,
        ignore_link_definition_start,
        close_open_blocks_fn,
    ):
        requeue_line_info = RequeueLineInfo()
        if not leaf_tokens:
            print("parsing leaf>>")
            (
                leaf_tokens,
                requeue_line_info,
            ) = ContainerBlockProcessor.__parse_line_for_leaf_blocks(
                token_stack,
                token_document,
                line_to_parse,
                0,
                this_bq_count,
                no_para_start_if_empty,
                ignore_link_definition_start,
                close_open_blocks_fn,
            )
            print("parsed leaf>>" + str(leaf_tokens))
            print("parsed leaf>>" + str(len(leaf_tokens)))
            print(
                "parsed leaf>>lines_to_requeue>>"
                + str(requeue_line_info.lines_to_requeue)
                + ">"
                + str(len(requeue_line_info.lines_to_requeue))
            )
            print(
                "parsed leaf>>requeue_line_info.force_ignore_first_as_lrd>>"
                + str(requeue_line_info.force_ignore_first_as_lrd)
                + ">"
            )
        return leaf_tokens, requeue_line_info
        # pylint: enable=too-many-arguments

    @staticmethod
    def __close_indented_block_if_indent_not_there(
        token_stack, extracted_whitespace, token_document
    ):

        pre_tokens = []
        if token_stack[
            -1
        ].is_indented_code_block and ParserHelper.is_length_less_than_or_equal_to(
            extracted_whitespace, 3
        ):
            pre_tokens.append(token_stack[-1].generate_close_token())
            del token_stack[-1]
            pre_tokens.extend(
                ContainerBlockProcessor.extract_markdown_tokens_back_to_blank_line(
                    token_document
                )
            )
        return pre_tokens

    # pylint: disable=too-many-arguments
    @staticmethod
    def handle_fenced_code_block(
        outer_processed,
        token_stack,
        line_to_parse,
        start_index,
        extracted_whitespace,
        new_tokens,
        close_open_blocks_fn,
    ):
        """
        Take care of the processing for fenced code blocks.
        """
        if not token_stack[-1].was_link_definition_started:
            fenced_tokens = LeafBlockProcessor.parse_fenced_code_block(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                close_open_blocks_fn,
            )
            outer_processed = False
            if fenced_tokens:
                new_tokens.extend(fenced_tokens)
                outer_processed = True
            elif token_stack[-1].is_fenced_code_block:
                new_tokens.append(
                    TextMarkdownToken(line_to_parse[start_index:], extracted_whitespace)
                )
                outer_processed = True
        return outer_processed

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def handle_html_block(
        outer_processed,
        token_stack,
        line_to_parse,
        start_index,
        extracted_whitespace,
        new_tokens,
        close_open_blocks_fn,
    ):
        """
        Take care of the processing for html blocks.
        """
        if not outer_processed and not token_stack[-1].is_html_block:
            html_tokens = HtmlHelper.parse_html_block(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                close_open_blocks_fn,
            )
            new_tokens.extend(html_tokens)
        if token_stack[-1].is_html_block:
            html_tokens = HtmlHelper.check_normal_html_block_end(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                close_open_blocks_fn,
            )
            assert html_tokens
            new_tokens.extend(html_tokens)
            outer_processed = True
        return outer_processed

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, unused-argument
    @staticmethod
    def handle_link_reference_definition(
        outer_processed,
        token_stack,
        line_to_parse,
        start_index,
        extracted_whitespace,
        original_line_to_parse,
        ignore_link_definition_start,
    ):
        """
        Take care of the processing for link reference definitions.
        """
        # did_complete_lrd = False
        # did_pause_lrd = False

        lines_to_requeue = []
        force_ignore_first_as_lrd = None

        if not outer_processed and not ignore_link_definition_start:
            print(
                "plflb-process_link_reference_definition>>outer_processed>>"
                + line_to_parse[start_index:]
            )
            (
                outer_processed,
                _,  # did_complete_lrd,
                _,  # did_pause_lrd,
                lines_to_requeue,
                force_ignore_first_as_lrd,
            ) = LinkReferenceDefinitionHelper.process_link_reference_definition(
                token_stack,
                line_to_parse,
                start_index,
                original_line_to_parse,
                extracted_whitespace,
            )
            if lines_to_requeue:
                outer_processed = True
            print(
                "plflb-process_link_reference_definition>>outer_processed>>"
                + str(outer_processed)
                # + ">did_complete_lrd>"
                # + str(did_complete_lrd)
                # + "<did_pause_lrd<"
                # + str(did_pause_lrd)
                + "<lines_to_requeue<"
                + str(lines_to_requeue)
                + "<"
                + str(len(lines_to_requeue))
            )
        return outer_processed, lines_to_requeue, force_ignore_first_as_lrd

    # pylint: enable=too-many-arguments, unused-argument

    # pylint: disable=too-many-arguments
    @staticmethod
    def __parse_line_for_leaf_blocks(
        token_stack,
        token_document,
        line_to_parse,
        start_index,
        this_bq_count,
        no_para_start_if_empty,
        ignore_link_definition_start,
        close_open_blocks_fn,
    ):
        """
        Parse the contents of a line for a leaf block.
        """

        print("Leaf Line:" + line_to_parse.replace("\t", "\\t") + ":")
        new_tokens = []

        requeue_line_info = RequeueLineInfo()
        original_line_to_parse = line_to_parse[start_index:]
        start_index, extracted_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, start_index
        )

        pre_tokens = ContainerBlockProcessor.__close_indented_block_if_indent_not_there(
            token_stack, extracted_whitespace, token_document
        )

        outer_processed = False
        outer_processed = ContainerBlockProcessor.handle_fenced_code_block(
            outer_processed,
            token_stack,
            line_to_parse,
            start_index,
            extracted_whitespace,
            new_tokens,
            close_open_blocks_fn,
        )

        (
            outer_processed,
            requeue_line_info.lines_to_requeue,
            requeue_line_info.force_ignore_first_as_lrd,
        ) = ContainerBlockProcessor.handle_link_reference_definition(
            outer_processed,
            token_stack,
            line_to_parse,
            start_index,
            extracted_whitespace,
            original_line_to_parse,
            ignore_link_definition_start,
        )

        outer_processed = ContainerBlockProcessor.handle_html_block(
            outer_processed,
            token_stack,
            line_to_parse,
            start_index,
            extracted_whitespace,
            new_tokens,
            close_open_blocks_fn,
        )

        if not outer_processed:
            assert not new_tokens
            new_tokens = LeafBlockProcessor.parse_atx_headings(
                line_to_parse, start_index, extracted_whitespace, close_open_blocks_fn
            )
            if not new_tokens:
                new_tokens = LeafBlockProcessor.parse_indented_code_block(
                    token_stack, line_to_parse, start_index, extracted_whitespace
                )
            if not new_tokens:
                stack_bq_count = BlockQuoteProcessor.count_of_block_quotes_on_stack(
                    token_stack
                )
                new_tokens = LeafBlockProcessor.parse_setext_headings(
                    token_stack,
                    token_document,
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    this_bq_count,
                    stack_bq_count,
                )
            if not new_tokens:
                stack_bq_count = BlockQuoteProcessor.count_of_block_quotes_on_stack(
                    token_stack
                )
                new_tokens = LeafBlockProcessor.parse_thematic_break(
                    token_stack,
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    this_bq_count,
                    close_open_blocks_fn,
                    stack_bq_count,
                )
            if not new_tokens:
                stack_bq_count = BlockQuoteProcessor.count_of_block_quotes_on_stack(
                    token_stack
                )
                new_tokens = LeafBlockProcessor.parse_paragraph(
                    token_stack,
                    token_document,
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    this_bq_count,
                    no_para_start_if_empty,
                    stack_bq_count,
                    close_open_blocks_fn,
                )

        # assert new_tokens or did_complete_lrd or did_pause_lrd or lines_to_requeue
        print(">>leaf--adding>>" + str(new_tokens))
        pre_tokens.extend(new_tokens)
        return pre_tokens, requeue_line_info

    # pylint: enable=too-many-arguments

    @staticmethod
    def extract_markdown_tokens_back_to_blank_line(token_document):
        """
        Extract tokens going back to the last blank line token.
        """

        pre_tokens = []
        while token_document[-1].is_blank_line:
            last_element = token_document[-1]
            pre_tokens.append(last_element)
            del token_document[-1]
        return pre_tokens
