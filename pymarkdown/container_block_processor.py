"""
Module to provide processing for the container blocks.
"""
import copy
import logging

from pymarkdown.block_quote_processor import BlockQuoteProcessor
from pymarkdown.html_helper import HtmlHelper
from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.link_reference_definition_helper import LinkReferenceDefinitionHelper
from pymarkdown.list_block_processor import ListBlockProcessor
from pymarkdown.parser_helper import ParserHelper, PositionMarker

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
# pylint: disable=too-many-lines
class ContainerIndices:
    """
    Class to provide for encapsulation on a group of container indices.
    """

    def __init__(self, ulist_index, olist_index, block_index):
        self.ulist_index = ulist_index
        self.olist_index = olist_index
        self.block_index = block_index

    def __str__(self):
        return (
            "{ContainerIndices:ulist_index:"
            + str(self.ulist_index)
            + ";olist_index:"
            + str(self.olist_index)
            + ";block_index:"
            + str(self.block_index)
            + "}"
        )


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

    @staticmethod
    def extract_markdown_tokens_back_to_blank_line(parser_state, was_forced):
        """
        Extract tokens going back to the last blank line token.
        """

        pre_tokens = []
        while parser_state.token_document[-1].is_blank_line:
            last_element = parser_state.token_document[-1]
            if was_forced:
                pre_tokens.insert(0, last_element)
            else:
                pre_tokens.append(last_element)
            del parser_state.token_document[-1]
        return pre_tokens

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-branches
    @staticmethod
    def parse_line_for_container_blocks(
        parser_state,
        position_marker,
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
        # TODO work on removing this
        line_to_parse = position_marker.text_to_parse
        if container_depth == 0:
            parser_state.original_line_to_parse = position_marker.text_to_parse[:]

        original_stack_depth = len(parser_state.token_stack)
        original_document_depth = len(parser_state.token_document)
        LOGGER.debug("Line:%s:", position_marker.text_to_parse)
        LOGGER.debug("Stack Depth:%s:", str(original_stack_depth))
        LOGGER.debug("Document Depth:%s:", str(original_document_depth))
        no_para_start_if_empty = False

        last_stack_index = len(parser_state.token_stack) - 1
        while not parser_state.token_stack[last_stack_index].is_document:
            if parser_state.token_stack[last_stack_index].is_block_quote:
                break
            last_stack_index -= 1

        last_block_quote_stack_token = None
        last_block_quote_markdown_token_index = None
        copy_of_last_block_quote_markdown_token = None
        if not parser_state.token_stack[last_stack_index].is_document:
            last_block_quote_stack_token = parser_state.token_stack[last_stack_index]
            last_block_quote_markdown_token_index = parser_state.token_document.index(
                parser_state.token_stack[last_stack_index].matching_markdown_token
            )
            copy_of_last_block_quote_markdown_token = copy.deepcopy(
                parser_state.token_document[last_block_quote_markdown_token_index]
            )
        LOGGER.debug(
            "Last Block Quote:%s:",
            ParserHelper.make_value_visible(last_block_quote_stack_token),
        )
        LOGGER.debug("Last Block Quote:%s:", str(last_block_quote_markdown_token_index))
        LOGGER.debug(
            "Last Block Quote:%s:",
            ParserHelper.make_value_visible(copy_of_last_block_quote_markdown_token),
        )
        parser_state.last_block_quote_stack_token = last_block_quote_stack_token
        parser_state.last_block_quote_markdown_token_index = (
            last_block_quote_markdown_token_index
        )
        parser_state.copy_of_last_block_quote_markdown_token = (
            copy_of_last_block_quote_markdown_token
        )

        start_index, extracted_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, 0
        )

        (
            current_container_blocks,
            adj_ws,
            stack_bq_count,
            this_bq_count,
        ) = ContainerBlockProcessor.__calculate_for_container_blocks(
            parser_state,
            line_to_parse,
            extracted_whitespace,
            foobar,
            init_bq,
        )

        end_container_indices = ContainerIndices(-1, -1, -1)

        LOGGER.debug(
            ">>__get_block_start_index>>%s>>",
            ParserHelper.make_whitespace_visible(line_to_parse),
        )
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
            removed_chars_at_start,
            did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            lines_to_requeue,
            force_ignore_first_as_lrd,
        ) = ContainerBlockProcessor.__get_block_start_index(
            position_marker,
            parser_state,
            extracted_whitespace,
            adj_ws,
            this_bq_count,
            stack_bq_count,
            start_index,
        )
        if lines_to_requeue:
            requeue_line_info = RequeueLineInfo()
            requeue_line_info.lines_to_requeue = lines_to_requeue
            requeue_line_info.force_ignore_first_as_lrd = force_ignore_first_as_lrd
            return None, None, requeue_line_info

        LOGGER.debug(">>did_blank>>%s", did_blank)
        LOGGER.debug(">>avoid_block_starts>>%s", str(avoid_block_starts))
        if did_blank:
            container_level_tokens.extend(leaf_tokens)
            return container_level_tokens, line_to_parse, RequeueLineInfo()

        LOGGER.debug(
            ">>__get_list_start_index>>%s>>",
            ParserHelper.make_whitespace_visible(line_to_parse.replace),
        )
        (
            did_process,
            was_container_start,
            end_container_indices.ulist_index,
            no_para_start_if_empty,
            line_to_parse,
            removed_chars_at_start,
            lines_to_requeue,
            force_ignore_first_as_lrd,
        ) = ContainerBlockProcessor.__get_list_start_index(
            position_marker,
            line_to_parse,
            start_index,
            True,
            parser_state,
            did_process,
            was_container_start,
            no_para_start_if_empty,
            extracted_whitespace,
            adj_ws,
            stack_bq_count,
            this_bq_count,
            removed_chars_at_start,
            current_container_blocks,
            container_level_tokens,
        )
        if lines_to_requeue:
            requeue_line_info = RequeueLineInfo()
            requeue_line_info.lines_to_requeue = lines_to_requeue
            requeue_line_info.force_ignore_first_as_lrd = force_ignore_first_as_lrd
            return None, None, requeue_line_info

        LOGGER.debug(
            ">>__get_list_start_index>>%s>>",
            ParserHelper.make_whitespace_visible(line_to_parse),
        )
        (
            did_process,
            was_container_start,
            end_container_indices.olist_index,
            no_para_start_if_empty,
            line_to_parse,
            removed_chars_at_start,
            lines_to_requeue,
            force_ignore_first_as_lrd,
        ) = ContainerBlockProcessor.__get_list_start_index(
            position_marker,
            line_to_parse,
            start_index,
            False,
            parser_state,
            did_process,
            was_container_start,
            no_para_start_if_empty,
            extracted_whitespace,
            adj_ws,
            stack_bq_count,
            this_bq_count,
            removed_chars_at_start,
            current_container_blocks,
            container_level_tokens,
        )
        if lines_to_requeue:
            requeue_line_info = RequeueLineInfo()
            requeue_line_info.lines_to_requeue = lines_to_requeue
            requeue_line_info.force_ignore_first_as_lrd = force_ignore_first_as_lrd
            return None, None, requeue_line_info
        LOGGER.debug(
            ">>__get_list_start_index>>%s>>",
            ParserHelper.make_whitespace_visible(line_to_parse),
        )

        LOGGER.debug("last_block_quote_index>>%s", str(last_block_quote_index))

        LOGGER.debug("olist_index>>%s", str(end_container_indices.olist_index))
        LOGGER.debug("ulist_index>>%s", str(end_container_indices.ulist_index))
        LOGGER.debug("block_index>>%s", str(end_container_indices.block_index))

        last_list_start_index = 0
        if end_container_indices.block_index != -1:
            assert last_block_quote_index in (
                end_container_indices.block_index - 1,
                end_container_indices.block_index,
            )
        elif end_container_indices.olist_index != -1:
            last_list_start_index = end_container_indices.olist_index
        elif end_container_indices.ulist_index != -1:
            last_list_start_index = end_container_indices.ulist_index

        if not parser_state.token_stack[-1].is_fenced_code_block:
            new_position_marker = PositionMarker(
                position_marker.line_number, start_index, line_to_parse
            )
            LOGGER.debug(
                "__handle_nested_container_blocks>>%s>>",
                ParserHelper.make_whitespace_visible(line_to_parse),
            )
            (
                line_to_parse,
                leaf_tokens,
                container_level_tokens,
                no_para_start_if_empty,
            ) = ContainerBlockProcessor.__handle_nested_container_blocks(
                parser_state,
                container_depth,
                this_bq_count,
                stack_bq_count,
                no_para_start_if_empty,
                new_position_marker,
                end_container_indices,
                leaf_tokens,
                container_level_tokens,
                was_container_start,
                avoid_block_starts,
            )
            LOGGER.debug(
                "text>>%s>>", ParserHelper.make_whitespace_visible(line_to_parse)
            )

        LOGGER.debug("olist->container_level_tokens->%s", str(container_level_tokens))
        LOGGER.debug("removed_chars_at_start>>>%s", str(removed_chars_at_start))

        if container_depth:
            assert not leaf_tokens
            LOGGER.debug(">>>>>>>>%s<<<<<<<<<<", line_to_parse)
            return container_level_tokens, line_to_parse, None

        LOGGER.debug(
            ">>__process_list_in_progress>>%s>>",
            ParserHelper.make_whitespace_visible(line_to_parse),
        )
        (
            did_process,
            line_to_parse,
            container_level_tokens,
            used_indent,
        ) = ContainerBlockProcessor.__process_list_in_progress(
            parser_state,
            did_process,
            line_to_parse,
            start_index,
            container_level_tokens,
            extracted_whitespace,
        )
        LOGGER.debug(
            ">>__process_list_in_progress>>%s>>",
            ParserHelper.make_whitespace_visible(line_to_parse),
        )
        ContainerBlockProcessor.__process_lazy_lines(
            parser_state,
            leaf_tokens,
            this_bq_count,
            stack_bq_count,
            line_to_parse,
            did_process,
            container_level_tokens,
        )
        LOGGER.debug("text>>%s>>", ParserHelper.make_whitespace_visible(line_to_parse))
        LOGGER.debug("container_level_tokens>>%s>>", str(container_level_tokens))

        # TODO refactor to make indent unnecessary?
        calculated_indent = len(parser_state.original_line_to_parse) - len(
            line_to_parse
        )
        LOGGER.debug(">>indent>>%s", str(calculated_indent))

        force_it = False
        if (
            used_indent
            and parser_state.token_stack[-1].is_paragraph
            and parser_state.token_stack[-2].is_block_quote
        ):
            assert text_removed_by_container is None
            text_removed_by_container = used_indent
            force_it = True

        newer_position_marker = PositionMarker(
            position_marker.line_number,
            start_index,
            line_to_parse,
            index_indent=calculated_indent,
        )
        parser_state.same_line_container_tokens = container_level_tokens
        leaf_tokens, requeue_line_info = ContainerBlockProcessor.__process_leaf_tokens(
            parser_state,
            leaf_tokens,
            newer_position_marker,
            this_bq_count,
            removed_chars_at_start,
            no_para_start_if_empty,
            ignore_link_definition_start,
            last_block_quote_index,
            last_list_start_index,
            text_removed_by_container,
            force_it,
            original_stack_depth,
            original_document_depth,
        )
        parser_state.same_line_container_tokens = None

        container_level_tokens.extend(leaf_tokens)
        LOGGER.debug(
            "clt-end>>%s>>%s<<",
            str(len(container_level_tokens)),
            ParserHelper.make_value_visible(container_level_tokens),
        )
        return container_level_tokens, line_to_parse, requeue_line_info
        # pylint: enable=too-many-locals
        # pylint: enable=too-many-arguments
        # pylint: enable=too-many-statements
        # pylint: enable=too-many-branches

    @staticmethod
    # pylint: disable=too-many-locals, too-many-arguments
    def __get_block_start_index(
        position_marker,
        parser_state,
        extracted_whitespace,
        adj_ws,
        this_bq_count,
        stack_bq_count,
        start_index,
    ):
        new_position_marker = PositionMarker(
            position_marker.line_number, start_index, position_marker.text_to_parse
        )
        (
            did_process,
            was_container_start,
            block_index,
            this_bq_count,
            stack_bq_count,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            removed_chars_at_start,
            did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            lines_to_requeue,
            force_ignore_first_as_lrd,
        ) = BlockQuoteProcessor.handle_block_quote_block(
            parser_state,
            new_position_marker,
            extracted_whitespace,
            adj_ws,
            this_bq_count,
            stack_bq_count,
        )
        LOGGER.debug("text>>:%s:>>", line_to_parse)
        LOGGER.debug(">>container_level_tokens>>%s", str(container_level_tokens))
        return (
            did_process,
            was_container_start,
            block_index,
            this_bq_count,
            stack_bq_count,
            line_to_parse,
            start_index,
            leaf_tokens,
            container_level_tokens,
            removed_chars_at_start,
            did_blank,
            last_block_quote_index,
            text_removed_by_container,
            avoid_block_starts,
            lines_to_requeue,
            force_ignore_first_as_lrd,
        )

    # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def __get_list_start_index(
        position_marker,
        line_to_parse,
        start_index,
        is_ulist,
        parser_state,
        did_process,
        was_container_start,
        no_para_start_if_empty,
        extracted_whitespace,
        adj_ws,
        stack_bq_count,
        this_bq_count,
        removed_chars_at_start,
        current_container_blocks,
        container_level_tokens,
    ):

        # TODO refactor so it doesn't need this!
        new_position_marker = PositionMarker(
            position_marker.line_number, start_index, line_to_parse
        )

        LOGGER.debug(
            "pre-list>>#%s#%s#%s#",
            str(position_marker.index_number),
            str(position_marker.index_indent),
            ParserHelper.make_value_visible(position_marker.text_to_parse),
        )
        LOGGER.debug(
            "pre-list>>#%s#%s#%s#",
            str(new_position_marker.index_number),
            str(new_position_marker.index_indent),
            ParserHelper.make_value_visible(new_position_marker.text_to_parse),
        )
        (
            did_process,
            was_container_start,
            new_list_index,
            no_para_start_if_empty,
            line_to_parse,
            resultant_tokens,
            removed_chars_at_start,
            lines_to_requeue,
            force_ignore_first_as_lrd,
        ) = ListBlockProcessor.handle_list_block(
            is_ulist,
            parser_state,
            did_process,
            was_container_start,
            no_para_start_if_empty,
            new_position_marker,
            extracted_whitespace,
            adj_ws,
            stack_bq_count,
            this_bq_count,
            removed_chars_at_start,
            current_container_blocks,
        )
        if lines_to_requeue:
            return (
                None,
                None,
                None,
                None,
                None,
                None,
                lines_to_requeue,
                force_ignore_first_as_lrd,
            )
        container_level_tokens.extend(resultant_tokens)
        LOGGER.debug(
            "post-ulist>>#%s#%s#%s#",
            str(position_marker.index_number),
            str(position_marker.index_indent),
            ParserHelper.make_value_visible(position_marker.text_to_parse),
        )
        LOGGER.debug(
            "post-ulist>>#%s#%s#%s#",
            str(new_position_marker.index_number),
            str(new_position_marker.index_indent),
            ParserHelper.make_value_visible(new_position_marker.text_to_parse),
        )
        LOGGER.debug("text>>%s>>", line_to_parse)

        return (
            did_process,
            was_container_start,
            new_list_index,
            no_para_start_if_empty,
            line_to_parse,
            removed_chars_at_start,
            None,
            None,
        )

    # pylint: enable=too-many-locals, too-many-arguments

    @staticmethod
    def __calculate_for_container_blocks(
        parser_state,
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
        for ind in parser_state.token_stack:
            if ind.is_list:
                current_container_blocks.append(ind)

        adj_ws = ContainerBlockProcessor.__calculate_adjusted_whitespace(
            parser_state,
            current_container_blocks,
            line_to_parse,
            extracted_whitespace,
            foobar=foobar,
        )

        stack_bq_count = BlockQuoteProcessor.count_of_block_quotes_on_stack(
            parser_state
        )

        return current_container_blocks, adj_ws, stack_bq_count, this_bq_count

    @staticmethod
    def __calculate_adjusted_whitespace(
        parser_state,
        current_container_blocks,
        line_to_parse,
        extracted_whitespace,
        foobar=None,
    ):
        """
        Based on the last container on the stack, determine what the adjusted whitespace is.
        """

        adj_ws = extracted_whitespace
        stack_index = len(parser_state.token_stack) - 1
        while stack_index >= 0 and not parser_state.token_stack[stack_index].is_list:
            stack_index -= 1
        if stack_index < 0:
            LOGGER.debug("PLFCB>>No Started lists")
            assert len(current_container_blocks) == 0
            if foobar is None:
                LOGGER.debug("PLFCB>>No Started Block Quote")
            else:
                LOGGER.debug("PLFCB>>Started Block Quote")
                adj_ws = extracted_whitespace[foobar:]
        else:
            assert len(current_container_blocks) >= 1
            LOGGER.debug(
                "PLFCB>>Started list-last stack>>%s",
                str(parser_state.token_stack[stack_index]),
            )
            token_index = len(parser_state.token_document) - 1

            while token_index >= 0 and not (
                parser_state.token_document[token_index].is_any_list_token
            ):
                token_index -= 1
            LOGGER.debug(
                "PLFCB>>Started list-last token>>%s",
                str(parser_state.token_document[token_index]),
            )
            assert token_index >= 0

            old_start_index = parser_state.token_document[token_index].indent_level

            ws_len = ParserHelper.calculate_length(extracted_whitespace)
            LOGGER.debug(
                "old_start_index>>%s>>ws_len>>%s", str(old_start_index), str(ws_len)
            )
            if ws_len >= old_start_index:
                LOGGER.debug("RELINE:%s:", line_to_parse)
                adj_ws = extracted_whitespace[old_start_index:]
            else:
                LOGGER.debug("DOWNGRADE")
        return adj_ws

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_nested_container_blocks(
        parser_state,
        container_depth,
        this_bq_count,
        stack_bq_count,
        no_para_start_if_empty,
        position_marker,
        end_container_indices,
        leaf_tokens,
        container_level_tokens,
        was_container_start,
        avoid_block_starts,
    ):
        """
        Handle the processing of nested container blocks, as they can contain
        themselves and get somewhat messy.
        """
        adjusted_text_to_parse = position_marker.text_to_parse
        if was_container_start and position_marker.text_to_parse:
            assert container_depth < 10
            LOGGER.debug(
                "__handle_nested_container_blocks>stack>>:%s:<<",
                str(position_marker.text_to_parse),
            )
            LOGGER.debug(
                "__handle_nested_container_blocks>end_container_indices>>:%s:<<",
                str(end_container_indices),
            )
            nested_container_starts = (
                ContainerBlockProcessor.__get_nested_container_starts(
                    parser_state,
                    position_marker.text_to_parse,
                    end_container_indices,
                    avoid_block_starts,
                )
            )
            LOGGER.debug(
                "__handle_nested_container_blocks>nested_container_starts>>:%s:<<",
                str(nested_container_starts),
            )
            LOGGER.debug(
                "__handle_nested_container_blocks>end_container_indices>>:%s:<<",
                str(end_container_indices),
            )

            LOGGER.debug(
                "check next container_start>stack>>%s", str(parser_state.token_stack)
            )
            LOGGER.debug("check next container_start>leaf_tokens>>%s", str(leaf_tokens))
            LOGGER.debug(
                "check next container_start>container_level_tokens>>%s",
                str(container_level_tokens),
            )

            adj_line_to_parse = position_marker.text_to_parse

            LOGGER.debug("check next container_start>pre>>%s<<", str(adj_line_to_parse))
            active_container_index = max(
                end_container_indices.ulist_index,
                end_container_indices.olist_index,
                end_container_indices.block_index,
            )
            LOGGER.debug(
                "check next container_start>max>>%s>>bq>>%s",
                str(active_container_index),
                str(end_container_indices.block_index),
            )
            LOGGER.debug(
                "^^%s^^%s^^",
                adj_line_to_parse[0 : end_container_indices.block_index],
                adj_line_to_parse[end_container_indices.block_index :],
            )
            if (
                end_container_indices.block_index != -1
                and not nested_container_starts.ulist_index
                and not nested_container_starts.olist_index
            ):
                assert active_container_index == end_container_indices.block_index
                adj_line_to_parse = adj_line_to_parse[
                    end_container_indices.block_index :
                ]

            LOGGER.debug(
                "check next container_start>mid>>stack_bq_count>>%s<<this_bq_count<<%s",
                str(stack_bq_count),
                str(this_bq_count),
            )
            adj_line_to_parse = (
                ParserHelper.repeat_string(
                    ParserHelper.space_character, active_container_index
                )
                + adj_line_to_parse
            )
            LOGGER.debug(
                "check next container_start>post<<%s<<", str(adj_line_to_parse)
            )

            LOGGER.debug("leaf_tokens>>%s", str(leaf_tokens))
            assert not leaf_tokens
            if container_level_tokens:
                parser_state.token_document.extend(container_level_tokens)
                container_level_tokens = []

            LOGGER.debug(
                "check next container_start>stack>>%s", str(parser_state.token_stack)
            )
            LOGGER.debug(
                "check next container_start>tokenized_document>>%s",
                ParserHelper.make_value_visible(parser_state.token_document),
            )

            if (
                nested_container_starts.ulist_index
                or nested_container_starts.olist_index
                or nested_container_starts.block_index
            ):
                adjusted_text_to_parse = (
                    ContainerBlockProcessor.__look_for_container_blocks(
                        parser_state,
                        adj_line_to_parse,
                        end_container_indices.block_index,
                        container_depth,
                        this_bq_count,
                        position_marker,
                    )
                )
            no_para_start_if_empty = True
        return (
            adjusted_text_to_parse,
            leaf_tokens,
            container_level_tokens,
            no_para_start_if_empty,
        )

    # pylint: enable=too-many-arguments

    @staticmethod
    def __get_nested_container_starts(
        parser_state,
        line_to_parse,
        end_container_indices,
        avoid_block_starts,
    ):

        LOGGER.debug("check next container_start>")

        after_ws_index, ex_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, 0
        )

        nested_ulist_start, _, _, _ = ListBlockProcessor.is_ulist_start(
            parser_state, line_to_parse, after_ws_index, ex_whitespace, False
        )
        nested_olist_start, _, _, _ = ListBlockProcessor.is_olist_start(
            parser_state, line_to_parse, after_ws_index, ex_whitespace, False
        )
        if avoid_block_starts:
            LOGGER.debug("avoiding next block container start")
            nested_block_start = False
        else:
            nested_block_start = BlockQuoteProcessor.is_block_quote_start(
                line_to_parse, after_ws_index, ex_whitespace
            )
        LOGGER.debug(
            "check next container_start>ulist>%s>index>%s",
            str(nested_ulist_start),
            str(end_container_indices.ulist_index),
        )
        LOGGER.debug(
            "check next container_start>olist>%s>index>%s",
            str(nested_olist_start),
            str(end_container_indices.olist_index),
        )
        LOGGER.debug(
            "check next container_start>bquote>%s>index>%s",
            str(nested_block_start),
            str(end_container_indices.block_index),
        )
        return ContainerIndices(
            nested_ulist_start, nested_olist_start, nested_block_start
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __look_for_container_blocks(
        parser_state,
        adj_line_to_parse,
        end_of_bquote_start_index,
        container_depth,
        this_bq_count,
        position_marker,
    ):
        """
        Look for container blocks that we can use.
        """
        LOGGER.debug("check next container_start>recursing")
        LOGGER.debug("check next container_start>>%s\n", adj_line_to_parse)

        adj_block = None
        if end_of_bquote_start_index != -1:
            adj_block = end_of_bquote_start_index

        LOGGER.debug("adj_line_to_parse>>>%s<<<", str(adj_line_to_parse))

        position_marker = PositionMarker(
            position_marker.line_number, -1, adj_line_to_parse
        )
        (
            produced_inner_tokens,
            line_to_parse,
            requeue_line_info,
        ) = ContainerBlockProcessor.parse_line_for_container_blocks(
            parser_state,
            position_marker,
            False,
            container_depth=container_depth + 1,
            foobar=adj_block,
            init_bq=this_bq_count,
        )
        assert not requeue_line_info or not requeue_line_info.lines_to_requeue
        # TODO will need to deal with force_ignore_first_as_lrd

        LOGGER.debug("\ncheck next container_start>recursed")
        LOGGER.debug(
            "check next container_start>stack>>%s", str(parser_state.token_stack)
        )
        LOGGER.debug(
            "check next container_start>tokenized_document>>%s",
            str(parser_state.token_document),
        )
        LOGGER.debug("check next container_start>line_parse>>%s", str(line_to_parse))

        parser_state.token_document.extend(produced_inner_tokens)
        return line_to_parse

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_list_in_progress(
        parser_state,
        did_process,
        line_to_parse,
        start_index,
        container_level_tokens,
        extracted_whitespace,
    ):
        used_indent = None
        if not did_process:
            is_list_in_process, ind = LeafBlockProcessor.check_for_list_in_process(
                parser_state
            )
            if is_list_in_process:
                assert not container_level_tokens
                LOGGER.debug("clt>>list-in-progress")
                LOGGER.debug("clt>>line_to_parse>>:%s:>>", str(line_to_parse))
                (
                    container_level_tokens,
                    line_to_parse,
                    used_indent,
                ) = ListBlockProcessor.list_in_process(
                    parser_state,
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    ind,
                )
                LOGGER.debug("clt>>line_to_parse>>:%s:>>", str(line_to_parse))
                LOGGER.debug("clt>>used_indent>>:%s:>>", str(used_indent))
                did_process = True

        if did_process:
            LOGGER.debug(
                "clt-before-lead>>%s>>%s",
                str(len(container_level_tokens)),
                str(container_level_tokens),
            )
        return did_process, line_to_parse, container_level_tokens, used_indent

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __process_lazy_lines(
        parser_state,
        leaf_tokens,
        this_bq_count,
        stack_bq_count,
        line_to_parse,
        did_process,
        container_level_tokens,
    ):

        LOGGER.debug("LINE-lazy>%s", line_to_parse)
        assert not leaf_tokens
        LOGGER.debug("clt>>lazy-check")

        LOGGER.debug("__process_lazy_lines>>ltp>%s", str(line_to_parse))
        after_ws_index, ex_whitespace = ParserHelper.extract_whitespace(
            line_to_parse, 0
        )
        remaining_line = line_to_parse[after_ws_index:]
        LOGGER.debug("__process_lazy_lines>>mod->ltp>%s<", str(remaining_line))
        LOGGER.debug("__process_lazy_lines>>mod->ews>%s<", str(ex_whitespace))

        lazy_tokens = BlockQuoteProcessor.check_for_lazy_handling(
            parser_state,
            this_bq_count,
            stack_bq_count,
            remaining_line,
            ex_whitespace,
        )
        if lazy_tokens:
            LOGGER.debug("clt>>lazy-found")
            container_level_tokens.extend(lazy_tokens)
            did_process = True

        if did_process:
            LOGGER.debug(
                "clt-after-leaf>>%s>>%s",
                str(len(container_level_tokens)),
                str(container_level_tokens),
            )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __process_leaf_tokens(
        parser_state,
        leaf_tokens,
        xposition_marker,
        this_bq_count,
        removed_chars_at_start,
        no_para_start_if_empty,
        ignore_link_definition_start,
        last_block_quote_index,
        last_list_start_index,
        text_removed_by_container,
        force_it,
        original_stack_depth,
        original_document_depth,
    ):
        assert not leaf_tokens
        LOGGER.debug("parsing leaf>>")
        position_marker = PositionMarker(
            xposition_marker.line_number,
            0,
            xposition_marker.text_to_parse,
            index_indent=xposition_marker.index_indent,
        )
        (
            leaf_tokens,
            requeue_line_info,
        ) = ContainerBlockProcessor.__parse_line_for_leaf_blocks(
            parser_state,
            position_marker,
            this_bq_count,
            removed_chars_at_start,
            no_para_start_if_empty,
            ignore_link_definition_start,
            last_block_quote_index,
            last_list_start_index,
            text_removed_by_container,
            force_it,
            original_stack_depth,
            original_document_depth,
        )
        LOGGER.debug("parsed leaf>>%s", ParserHelper.make_value_visible(leaf_tokens))
        LOGGER.debug("parsed leaf>>%s", str(len(leaf_tokens)))
        LOGGER.debug(
            "parsed leaf>>lines_to_requeue>>%s>%s",
            str(requeue_line_info.lines_to_requeue),
            str(len(requeue_line_info.lines_to_requeue)),
        )
        LOGGER.debug(
            "parsed leaf>>requeue_line_info.force_ignore_first_as_lrd>>%s>",
            str(requeue_line_info.force_ignore_first_as_lrd),
        )
        return leaf_tokens, requeue_line_info

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __close_indented_block_if_indent_not_there(parser_state, extracted_whitespace):

        LOGGER.debug(
            "__close_indented_block_if_indent_not_there>>%s>",
            str(parser_state.token_stack[-1]),
        )
        LOGGER.debug(
            "__close_indented_block_if_indent_not_there>>%s>",
            str(extracted_whitespace),
        )
        pre_tokens = []
        if parser_state.token_stack[
            -1
        ].is_indented_code_block and ParserHelper.is_length_less_than_or_equal_to(
            extracted_whitespace, 3
        ):
            pre_tokens.append(
                parser_state.token_stack[
                    -1
                ].generate_close_markdown_token_from_stack_token()
            )
            del parser_state.token_stack[-1]

            extracted_blank_line_tokens = (
                ContainerBlockProcessor.extract_markdown_tokens_back_to_blank_line(
                    parser_state, False
                )
            )
            extracted_blank_line_tokens.reverse()
            pre_tokens.extend(extracted_blank_line_tokens)
        LOGGER.debug(
            "__close_indented_block_if_indent_not_there>>pre_tokens>%s>",
            str(pre_tokens),
        )
        return pre_tokens

    @staticmethod
    def __handle_fenced_code_block(
        parser_state,
        outer_processed,
        position_marker,
        extracted_whitespace,
        new_tokens,
    ):
        """
        Take care of the processing for fenced code blocks.
        """
        if not parser_state.token_stack[-1].was_link_definition_started:
            (
                fenced_tokens,
                extracted_whitespace,
            ) = LeafBlockProcessor.parse_fenced_code_block(
                parser_state,
                position_marker,
                extracted_whitespace,
            )
            outer_processed = False
            if fenced_tokens:
                new_tokens.extend(fenced_tokens)
                outer_processed = True
            elif parser_state.token_stack[-1].is_fenced_code_block:
                new_tokens.append(
                    TextMarkdownToken(
                        position_marker.text_to_parse[position_marker.index_number :],
                        extracted_whitespace,
                        position_marker=position_marker,
                    )
                )
                outer_processed = True
        return outer_processed

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_html_block(
        parser_state,
        outer_processed,
        position_marker,
        extracted_whitespace,
        new_tokens,
    ):
        """
        Take care of the processing for html blocks.
        """

        LOGGER.debug(">>position_marker>>ttp>>%s>>", position_marker.text_to_parse)
        LOGGER.debug(">>position_marker>>in>>%s>>", str(position_marker.index_number))
        LOGGER.debug(">>position_marker>>ln>>%s>>", str(position_marker.line_number))
        if not outer_processed and not parser_state.token_stack[-1].is_html_block:
            LOGGER.debug(">>html started?>>")
            old_top_of_stack = parser_state.token_stack[-1]
            html_tokens = HtmlHelper.parse_html_block(
                parser_state,
                position_marker,
                extracted_whitespace,
            )
            if html_tokens:
                LOGGER.debug(">>html started>>")
                LeafBlockProcessor.correct_for_leaf_block_start_in_list(
                    parser_state,
                    position_marker.index_indent,
                    old_top_of_stack,
                    html_tokens,
                )
            else:
                LOGGER.debug(">>html not started>>")
            new_tokens.extend(html_tokens)
        if parser_state.token_stack[-1].is_html_block:
            LOGGER.debug(">>html continued>>")
            html_tokens = HtmlHelper.check_normal_html_block_end(
                parser_state,
                position_marker.text_to_parse,
                position_marker.index_number,
                extracted_whitespace,
                position_marker,
            )
            assert html_tokens
            new_tokens.extend(html_tokens)
            outer_processed = True

        return outer_processed

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_link_reference_definition(
        parser_state,
        outer_processed,
        position_marker,
        extracted_whitespace,
        remaining_line_to_parse,
        ignore_link_definition_start,
        pre_tokens,
        original_stack_depth,
        original_document_depth,
    ):
        """
        Take care of the processing for link reference definitions.
        """
        lines_to_requeue = []
        new_tokens = []
        force_ignore_first_as_lrd = None

        LOGGER.debug(
            "handle_link_reference_definition>>pre_tokens>>%s<<",
            str(pre_tokens),
        )

        if not outer_processed and not ignore_link_definition_start:
            LOGGER.debug(
                "plflb-process_link_reference_definition>>outer_processed>>%s",
                position_marker.text_to_parse[position_marker.index_number :],
            )
            (
                outer_processed,
                _,  # did_complete_lrd,
                _,  # did_pause_lrd,
                lines_to_requeue,
                force_ignore_first_as_lrd,
                new_tokens,
            ) = LinkReferenceDefinitionHelper.process_link_reference_definition(
                parser_state,
                position_marker,
                remaining_line_to_parse,
                extracted_whitespace,
                parser_state.original_line_to_parse,
                original_stack_depth,
                original_document_depth,
            )
            if lines_to_requeue:
                outer_processed = True
            LOGGER.debug(
                "plflb-process_link_reference_definition>>outer_processed>>%s<lines_to_requeue<%s<%s",
                str(outer_processed),
                str(lines_to_requeue),
                str(len(lines_to_requeue)),
            )

        LOGGER.debug(
            "handle_link_reference_definition>>pre_tokens>>%s<<",
            ParserHelper.make_value_visible(pre_tokens),
        )
        pre_tokens.extend(new_tokens)
        LOGGER.debug(
            "handle_link_reference_definition>>pre_tokens>>%s<<",
            ParserHelper.make_value_visible(pre_tokens),
        )
        return outer_processed, lines_to_requeue, force_ignore_first_as_lrd

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments,too-many-locals
    @staticmethod
    def __parse_line_for_leaf_blocks(
        parser_state,
        xposition_marker,
        this_bq_count,
        removed_chars_at_start,
        no_para_start_if_empty,
        ignore_link_definition_start,
        last_block_quote_index,
        last_list_start_index,
        text_removed_by_container,
        force_it,
        original_stack_depth,
        original_document_depth,
    ):
        """
        Parse the contents of a line for a leaf block.
        """
        LOGGER.debug(
            "Leaf Line:%s:",
            ParserHelper.make_value_visible(xposition_marker.text_to_parse),
        )
        new_tokens = []

        requeue_line_info = RequeueLineInfo()
        # TODO rename to avoid collision with parameter
        remaining_line_to_parse = xposition_marker.text_to_parse[
            xposition_marker.index_number :
        ]
        (new_index_number, extracted_whitespace,) = ParserHelper.extract_whitespace(
            xposition_marker.text_to_parse, xposition_marker.index_number
        )
        position_marker = PositionMarker(
            xposition_marker.line_number,
            new_index_number,
            xposition_marker.text_to_parse,
            index_indent=xposition_marker.index_indent,
        )

        LOGGER.debug(
            "__close_indented_block_if_indent_not_there",
        )
        pre_tokens = ContainerBlockProcessor.__close_indented_block_if_indent_not_there(
            parser_state, extracted_whitespace
        )

        outer_processed = False
        outer_processed = ContainerBlockProcessor.__handle_fenced_code_block(
            parser_state,
            outer_processed,
            position_marker,
            extracted_whitespace,
            new_tokens,
        )

        (
            outer_processed,
            requeue_line_info.lines_to_requeue,
            requeue_line_info.force_ignore_first_as_lrd,
        ) = ContainerBlockProcessor.__handle_link_reference_definition(
            parser_state,
            outer_processed,
            position_marker,
            extracted_whitespace,
            remaining_line_to_parse,
            ignore_link_definition_start,
            pre_tokens,
            original_stack_depth,
            original_document_depth,
        )

        outer_processed = ContainerBlockProcessor.__handle_html_block(
            parser_state,
            outer_processed,
            position_marker,
            extracted_whitespace,
            new_tokens,
        )

        if not outer_processed:
            assert not new_tokens
            new_tokens = LeafBlockProcessor.parse_atx_headings(
                parser_state, position_marker, extracted_whitespace
            )
            if not new_tokens:
                new_tokens = LeafBlockProcessor.parse_indented_code_block(
                    parser_state,
                    position_marker,
                    extracted_whitespace,
                    removed_chars_at_start,
                    last_block_quote_index,
                    last_list_start_index,
                )
            if not new_tokens:
                stack_bq_count = BlockQuoteProcessor.count_of_block_quotes_on_stack(
                    parser_state
                )
                new_tokens = LeafBlockProcessor.parse_setext_headings(
                    parser_state,
                    position_marker,
                    extracted_whitespace,
                    this_bq_count,
                    stack_bq_count,
                )
            if not new_tokens:
                stack_bq_count = BlockQuoteProcessor.count_of_block_quotes_on_stack(
                    parser_state
                )
                new_tokens = LeafBlockProcessor.parse_thematic_break(
                    parser_state,
                    position_marker,
                    extracted_whitespace,
                    this_bq_count,
                    stack_bq_count,
                )
            if not new_tokens:
                stack_bq_count = BlockQuoteProcessor.count_of_block_quotes_on_stack(
                    parser_state
                )
                new_tokens = LeafBlockProcessor.parse_paragraph(
                    parser_state,
                    position_marker,
                    extracted_whitespace,
                    this_bq_count,
                    no_para_start_if_empty,
                    stack_bq_count,
                    text_removed_by_container,
                    force_it,
                )

        # assert new_tokens or did_complete_lrd or did_pause_lrd or lines_to_requeue
        LOGGER.debug(">>leaf--adding>>%s", ParserHelper.make_value_visible(new_tokens))
        pre_tokens.extend(new_tokens)
        LOGGER.debug(">>leaf--added>>%s", ParserHelper.make_value_visible(pre_tokens))
        return pre_tokens, requeue_line_info

    # pylint: enable=too-many-arguments, too-many-locals
