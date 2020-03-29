"""
Module to provide processing for the container blocks.
"""
from pymarkdown.block_quote_processor import BlockQuoteProcessor
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.link_helper import LinkHelper
from pymarkdown.list_block_processor import ListBlockProcessor
from pymarkdown.markdown_token import TextMarkdownToken
from pymarkdown.parser_helper import ParserHelper


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
            stack_index = stack_index - 1
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
                token_index = token_index - 1
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
        line_to_parse,
        end_of_ulist_start_index,
        end_of_olist_start_index,
        end_of_bquote_start_index,
        leaf_tokens,
        container_level_tokens,
        close_open_blocks_fn,
        handle_blank_line_fn,
    ):
        """
        Handle the processing of nested container blocks, as they can contain
        themselves and get somewhat messy.
        """

        assert container_depth < 10
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
            + str(end_of_ulist_start_index)
        )
        print(
            "check next container_start>olist>"
            + str(nested_olist_start)
            + ">index>"
            + str(end_of_olist_start_index)
        )
        print(
            "check next container_start>bquote>"
            + str(nested_block_start)
            + ">index>"
            + str(end_of_bquote_start_index)
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
            end_of_ulist_start_index,
            end_of_olist_start_index,
            end_of_bquote_start_index,
        )
        print(
            "check next container_start>max>>"
            + str(active_container_index)
            + ">>bq>>"
            + str(end_of_bquote_start_index)
        )
        print(
            "^^"
            + adj_line_to_parse[0:end_of_bquote_start_index]
            + "^^"
            + adj_line_to_parse[end_of_bquote_start_index:]
            + "^^"
        )
        if (
            end_of_bquote_start_index != -1
            and not nested_ulist_start
            and not nested_olist_start
        ):  # and active_container_index == end_of_bquote_start_index:
            adj_line_to_parse = adj_line_to_parse[end_of_bquote_start_index:]

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
        print("check next container_start>tokenized_document>>" + str(token_document))

        if nested_ulist_start or nested_olist_start or nested_block_start:
            print("check next container_start>recursing")
            print("check next container_start>>" + adj_line_to_parse + "\n")

            adj_block = None
            if end_of_bquote_start_index != -1:
                adj_block = end_of_bquote_start_index

            print("adj_line_to_parse>>>" + str(adj_line_to_parse) + "<<<")
            (
                _,
                line_to_parse,
                lines_to_requeue,
                _,
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
            assert not lines_to_requeue
            # TODO will need to deal with force_ignore_first_as_lrd

            print("\ncheck next container_start>recursed")
            print("check next container_start>stack>>" + str(token_stack))
            print(
                "check next container_start>tokenized_document>>" + str(token_document)
            )
            print("check next container_start>line_parse>>" + str(line_to_parse))
        return line_to_parse, leaf_tokens, container_level_tokens
        # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-statements
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

        end_of_olist_start_index = -1
        end_of_ulist_start_index = -1

        print("LINE-pre-block-start>" + line_to_parse)
        (
            did_process,
            was_container_start,
            end_of_bquote_start_index,
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

        print("LINE-pre-ulist>" + line_to_parse)
        (
            did_process,
            was_container_start,
            end_of_ulist_start_index,
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

        print("LINE-pre-olist>" + line_to_parse)
        (
            did_process,
            was_container_start,
            end_of_olist_start_index,
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

        print(
            "LINE-another_container_start>did_start>>"
            + str(was_container_start)
            + ">>"
            + line_to_parse
        )
        if was_container_start and line_to_parse:
            (
                line_to_parse,
                leaf_tokens,
                container_level_tokens,
            ) = ContainerBlockProcessor.__handle_nested_container_blocks(
                token_stack,
                token_document,
                container_depth,
                this_bq_count,
                stack_bq_count,
                line_to_parse,
                end_of_ulist_start_index,
                end_of_olist_start_index,
                end_of_bquote_start_index,
                leaf_tokens,
                container_level_tokens,
                close_open_blocks_fn,
                handle_blank_line_fn,
            )
            no_para_start_if_empty = True

        if container_depth:
            assert not leaf_tokens
            print(">>>>>>>>" + line_to_parse + "<<<<<<<<<<")
            return container_level_tokens, line_to_parse, None, None

        print("LINE-list-in-progress>" + line_to_parse)

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

        lines_to_requeue = []
        force_ignore_first_as_lrd = None
        if not leaf_tokens:
            print("parsing leaf>>")
            (
                leaf_tokens,
                lines_to_requeue,
                force_ignore_first_as_lrd,
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
                + str(lines_to_requeue)
                + ">"
                + str(len(lines_to_requeue))
            )
            print(
                "parsed leaf>>force_ignore_first_as_lrd>>"
                + str(force_ignore_first_as_lrd)
                + ">"
            )

        container_level_tokens.extend(leaf_tokens)
        print(
            "clt-end>>"
            + str(len(container_level_tokens))
            + ">>"
            + str(container_level_tokens)
            + "<<"
        )
        return (
            container_level_tokens,
            line_to_parse,
            lines_to_requeue,
            force_ignore_first_as_lrd,
        )
        # pylint: enable=too-many-locals
        # pylint: enable=too-many-arguments
        # pylint: enable=too-many-statements

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
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

        print("Leaf Line:" + line_to_parse + ":")
        new_tokens = []
        pre_tokens = []
        lines_to_requeue = []
        force_ignore_first_as_lrd = None
        original_line_to_parse = line_to_parse[start_index:]
        start_index, extracted_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, start_index
        )

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

        outer_processed = False
        fenced_tokens = None

        if not token_stack[-1].was_link_definition_started:
            fenced_tokens = LeafBlockProcessor.parse_fenced_code_block(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                close_open_blocks_fn,
            )
            if fenced_tokens:
                new_tokens.extend(fenced_tokens)
                outer_processed = True
            elif token_stack[-1].is_fenced_code_block:
                new_tokens.append(
                    TextMarkdownToken(line_to_parse[start_index:], extracted_whitespace)
                )
                outer_processed = True

        did_complete_lrd = False
        did_pause_lrd = False
        if not outer_processed and not ignore_link_definition_start:
            print(
                "plflb-process_link_reference_definition>>outer_processed>>"
                + line_to_parse[start_index:]
            )
            (
                outer_processed,
                did_complete_lrd,
                did_pause_lrd,
                lines_to_requeue,
                force_ignore_first_as_lrd,
            ) = LinkHelper.process_link_reference_definition(
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
                + ">did_complete_lrd>"
                + str(did_complete_lrd)
                + "<did_pause_lrd<"
                + str(did_pause_lrd)
                + "<lines_to_requeue<"
                + str(lines_to_requeue)
                + "<"
                + str(len(lines_to_requeue))
            )

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

        assert new_tokens or did_complete_lrd or did_pause_lrd or lines_to_requeue
        print(">>leaf--adding>>" + str(new_tokens))
        pre_tokens.extend(new_tokens)
        return pre_tokens, lines_to_requeue, force_ignore_first_as_lrd

    # pylint: enable=too-many-locals
    # pylint: enable=too-many-arguments
    # pylint: enable=too-many-branches
    # pylint: enable=too-many-statements

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
