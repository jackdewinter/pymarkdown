"""
Module to provide processing for the list blocks.
"""

import string

from pymarkdown.leaf_block_processor import LeafBlockProcessor
from pymarkdown.markdown_token import (
    NewListItemMarkdownToken,
    OrderedListStartMarkdownToken,
    UnorderedListStartMarkdownToken,
)
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.stack_token import OrderedListStackToken, UnorderedListStackToken


class ListBlockProcessor:
    """
    Class to provide processing for the list blocks.
    """

    __ulist_start_characters = "-+*"
    __olist_start_characters = ".)"

    @staticmethod
    # pylint: disable=too-many-arguments
    def is_ulist_start(
        token_stack,
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check=False,
        adj_ws=None,
    ):
        """
        Determine if we have the start of an un-numbered list.
        """

        print("is_ulist_start>>pre>>")
        is_start = False
        after_all_whitespace_index = -1
        if adj_ws is None:
            adj_ws = extracted_whitespace

        if (
            (
                ParserHelper.is_length_less_than_or_equal_to(adj_ws, 3)
                or skip_whitespace_check
            )
            and ParserHelper.is_character_at_index_one_of(
                line_to_parse, start_index, ListBlockProcessor.__ulist_start_characters
            )
            and (
                ParserHelper.is_character_at_index_whitespace(
                    line_to_parse, start_index + 1
                )
                or ((start_index + 1) == len(line_to_parse))
            )
        ):

            print("is_ulist_start>>mid>>")
            after_all_whitespace_index, _ = ParserHelper.extract_whitespace(
                line_to_parse, start_index + 1
            )
            print(
                "after_all_whitespace_index>>"
                + str(after_all_whitespace_index)
                + ">>len>>"
                + str(len(line_to_parse))
            )

            is_break, _ = LeafBlockProcessor.is_thematic_break(
                line_to_parse, start_index, extracted_whitespace
            )
            if not is_break and not (
                token_stack[-1].is_paragraph
                and not token_stack[-2].is_list
                and (after_all_whitespace_index == len(line_to_parse))
            ):
                is_start = True

        print("is_ulist_start>>result>>" + str(is_start))
        return is_start, after_all_whitespace_index
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def is_olist_start(
        token_stack,
        line_to_parse,
        start_index,
        extracted_whitespace,
        skip_whitespace_check=False,
        adj_ws=None,
    ):
        """
        Determine if we have the start of an numbered or ordered list.
        """

        is_start = False
        end_whitespace_index = -1
        index = None
        my_count = None
        if adj_ws is None:
            adj_ws = extracted_whitespace
        if (
            ParserHelper.is_length_less_than_or_equal_to(adj_ws, 3)
            or skip_whitespace_check
        ) and ParserHelper.is_character_at_index_one_of(
            line_to_parse, start_index, string.digits
        ):
            index = start_index
            while ParserHelper.is_character_at_index_one_of(
                line_to_parse, index, string.digits
            ):
                index += 1
            my_count = index - start_index
            olist_index_number = line_to_parse[start_index:index]
            print("olist?" + olist_index_number + "<<count>>" + str(my_count) + "<<")
            print("olist>>" + str(line_to_parse[index]))
            print("index+1>>" + str(index + 1) + ">>len>>" + str(len(line_to_parse)))

            end_whitespace_index, _ = ParserHelper.extract_whitespace(
                line_to_parse, index + 1
            )
            print(
                "end_whitespace_index>>"
                + str(end_whitespace_index)
                + ">>len>>"
                + str(len(line_to_parse))
                + ">>"
                + olist_index_number
            )

            if (
                my_count <= 9
                and ParserHelper.is_character_at_index_one_of(
                    line_to_parse, index, ListBlockProcessor.__olist_start_characters
                )
                and not (
                    token_stack[-1].is_paragraph
                    and not token_stack[-2].is_list
                    and (
                        (end_whitespace_index == len(line_to_parse))
                        or olist_index_number != "1"
                    )
                )
                and (
                    ParserHelper.is_character_at_index_whitespace(
                        line_to_parse, index + 1
                    )
                    or ((index + 1) == len(line_to_parse))
                )
            ):
                is_start = True

        print("is_olist_start>>result>>" + str(is_start))
        return is_start, index, my_count, end_whitespace_index
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __pre_list(
        token_stack,
        line_to_parse,
        start_index,
        extracted_whitespace,
        marker_width,
        stack_bq_count,
        this_bq_count,
        close_open_blocks_fn,
    ):
        """
        Handle the processing of the first part of the list.
        """

        (
            after_marker_ws_index,
            after_marker_whitespace,
        ) = ParserHelper.extract_whitespace(line_to_parse, start_index + 1)
        ws_after_marker = ParserHelper.calculate_length(after_marker_whitespace)
        ws_before_marker = ParserHelper.calculate_length(extracted_whitespace)

        container_level_tokens, stack_bq_count = ListBlockProcessor.handle_list_nesting(
            token_stack, stack_bq_count, this_bq_count, close_open_blocks_fn
        )
        print(
            ">>>>>XX>>"
            + str(after_marker_ws_index)
            + ">>"
            + str(len(line_to_parse))
            + "<<"
        )
        if after_marker_ws_index == len(line_to_parse):
            print("BOOOOOOOM")
            indent_level = 2 + marker_width
            remaining_whitespace = 0
            ws_after_marker = 1
        else:
            indent_level = ws_before_marker + 1 + ws_after_marker + marker_width
            remaining_whitespace = 0
            print(
                "ws_after_marker>>"
                + str(ws_after_marker)
                + "<<es<<"
                + str(len(extracted_whitespace))
                + "<<indent_level<<"
                + str(indent_level)
                + "<<rem<<"
                + str(remaining_whitespace)
                + "<<"
            )
            if ws_after_marker > 4:
                indent_level = indent_level - ws_after_marker + 1
                remaining_whitespace = ws_after_marker - 1
                ws_after_marker = 1
        print(
            "ws_after_marker>>"
            + str(ws_after_marker)
            + "<<indent_level<<"
            + str(indent_level)
            + "<<rem<<"
            + str(remaining_whitespace)
            + "<<"
        )
        return (
            indent_level,
            remaining_whitespace,
            ws_after_marker,
            after_marker_ws_index,
            ws_before_marker,
            container_level_tokens,
            stack_bq_count,
        )
        # pylint: enable=too-many-arguments

    @staticmethod
    def handle_list_nesting(
        token_stack, stack_bq_count, this_bq_count, close_open_blocks_fn
    ):
        """
        Resolve any nesting issues with block quotes.
        """
        print(
            ">>stack_bq_count>>"
            + str(stack_bq_count)
            + ">>this_bq_count>>"
            + str(this_bq_count)
        )
        container_level_tokens = []
        while this_bq_count < stack_bq_count:

            assert not container_level_tokens
            inf = len(token_stack) - 1
            while not token_stack[inf].is_block_quote:
                inf -= 1

            container_level_tokens, _, _ = close_open_blocks_fn(
                until_this_index=inf, include_block_quotes=True, include_lists=True
            )
            print("container_level_tokens>>" + str(container_level_tokens))
            stack_bq_count -= 1
        return container_level_tokens, stack_bq_count

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def __post_list(
        token_stack,
        token_document,
        new_stack,
        new_token,
        line_to_parse,
        remaining_whitespace,
        after_marker_ws_index,
        indent_level,
        current_container_blocks,
        close_open_blocks_fn,
    ):
        """
        Handle the processing of the last part of the list.
        """

        print("new_stack>>" + str(new_stack))

        emit_item = True
        emit_li = True
        did_find, last_list_index = LeafBlockProcessor.check_for_list_in_process(
            token_stack
        )
        if did_find:
            (
                container_level_tokens,
                emit_li,
                emit_item,
            ) = ListBlockProcessor.close_required_lists_after_start(
                token_stack,
                token_document,
                last_list_index,
                close_open_blocks_fn,
                new_stack,
                current_container_blocks,
            )
        else:
            print("NOT list-in-process>>" + str(token_stack[last_list_index]))
            container_level_tokens, _, _ = close_open_blocks_fn()
        print("container_level_tokens>>" + str(container_level_tokens))

        if emit_item or not emit_li:
            token_stack.append(new_stack)
            container_level_tokens.append(new_token)
        else:
            assert emit_li
            container_level_tokens.append(NewListItemMarkdownToken(indent_level))
        line_to_parse = (
            "".rjust(remaining_whitespace, " ") + line_to_parse[after_marker_ws_index:]
        )

        return True, container_level_tokens, line_to_parse
        # pylint: enable=too-many-locals, too-many-arguments

    @staticmethod
    # pylint: disable=too-many-arguments
    def close_required_lists_after_start(
        token_stack,
        token_document,
        last_list_index,
        close_open_blocks_fn,
        new_stack,
        current_container_blocks,
    ):
        """
        After a list start, check to see if any others need closing.
        """
        print("list-in-process>>" + str(token_stack[last_list_index]))
        container_level_tokens, _, _ = close_open_blocks_fn(
            until_this_index=last_list_index + 1
        )
        print("old-stack>>" + str(container_level_tokens) + "<<")

        (
            do_not_emit,
            emit_li,
            extra_tokens,
        ) = ListBlockProcessor.__are_list_starts_equal(
            token_stack,
            token_document,
            last_list_index,
            new_stack,
            current_container_blocks,
            close_open_blocks_fn,
        )
        print("extra_tokens>>" + str(extra_tokens))
        container_level_tokens.extend(extra_tokens)
        emit_item = None
        if do_not_emit:
            emit_item = False
            print("post_list>>don't emit")
        else:
            print("post_list>>close open blocks and emit")
            close_tokens, _, _ = close_open_blocks_fn(
                until_this_index=last_list_index, include_lists=True
            )
            assert close_tokens
            container_level_tokens.extend(close_tokens)
        return container_level_tokens, emit_li, emit_item

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __are_list_starts_equal(
        token_stack,
        token_document,
        last_list_index,
        new_stack,
        current_container_blocks,
        close_open_blocks_fn,
    ):
        """
        Check to see if the list starts are equal, and hence a continuation of
        the current list.
        """

        balancing_tokens = []

        print(
            "ARE-EQUAL>>stack>>"
            + str(token_stack[last_list_index])
            + ">>new>>"
            + str(new_stack)
        )
        if token_stack[last_list_index] == new_stack:
            balancing_tokens, _, _ = close_open_blocks_fn(
                until_this_index=last_list_index, include_block_quotes=True
            )
            return True, True, balancing_tokens

        document_token_index = len(token_document) - 1
        while document_token_index >= 0 and not (
            token_document[document_token_index].is_any_list_token
        ):
            document_token_index -= 1
        assert document_token_index >= 0

        print("ARE-EQUAL>>Last_List_token=" + str(token_document[document_token_index]))
        old_start_index = token_document[document_token_index].indent_level

        old_last_marker_character = token_stack[last_list_index].list_character[-1]
        current_start_index = new_stack.ws_before_marker
        print(
            "old>>"
            + str(token_stack[last_list_index].extra_data)
            + ">>"
            + old_last_marker_character
        )
        print("new>>" + str(new_stack.extra_data) + ">>" + new_stack.list_character[-1])
        if (
            token_stack[last_list_index].type_name == new_stack.type_name
            and old_last_marker_character == new_stack.list_character[-1]
        ):
            print("are_list_starts_equal>>ELIGIBLE!!!")
            print(
                "are_list_starts_equal>>current_start_index>>"
                + str(current_start_index)
                + ">>old_start_index>>"
                + str(old_start_index)
            )
            if current_start_index < old_start_index:

                print("current_container_blocks>>" + str(current_container_blocks))
                if len(current_container_blocks) > 1:
                    print("current_container_blocks-->" + str(token_stack))
                    last_stack_depth = token_stack[-1].ws_before_marker
                    while current_start_index < last_stack_depth:
                        last_stack_index = token_stack.index(token_stack[-1])
                        close_tokens, _, _ = close_open_blocks_fn(
                            until_this_index=last_stack_index, include_lists=True
                        )
                        assert close_tokens
                        balancing_tokens.extend(close_tokens)
                        print("close_tokens>>" + str(close_tokens))
                        last_stack_depth = token_stack[-1].ws_before_marker

                return True, True, balancing_tokens
            return True, False, balancing_tokens
        print("SUBLIST WITH DIFFERENT")
        print("are_list_starts_equal>>ELIGIBLE!!!")
        print(
            "are_list_starts_equal>>current_start_index>>"
            + str(current_start_index)
            + ">>old_start_index>>"
            + str(old_start_index)
        )
        if current_start_index >= old_start_index:
            return True, False, balancing_tokens
        return False, False, balancing_tokens
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def handle_ulist_block(
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
    ):
        """
        Handle the processing of a ulist block.
        """

        end_of_ulist_start_index = -1
        container_level_tokens = []
        if not did_process:
            started_ulist, end_of_ulist_start_index = ListBlockProcessor.is_ulist_start(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                adj_ws=adj_ws,
            )
            if started_ulist:
                print("clt>>ulist-start")

                (
                    indent_level,
                    remaining_whitespace,
                    ws_after_marker,
                    after_marker_ws_index,
                    ws_before_marker,
                    container_level_tokens,
                    stack_bq_count,
                ) = ListBlockProcessor.__pre_list(
                    token_stack,
                    line_to_parse,
                    start_index,
                    extracted_whitespace,
                    0,
                    stack_bq_count,
                    this_bq_count,
                    close_open_blocks_fn,
                )

                print(
                    "total="
                    + str(indent_level)
                    + ";ws-before="
                    + str(ws_before_marker)
                    + ";ws_after="
                    + str(ws_after_marker)
                )
                new_stack = UnorderedListStackToken(
                    indent_level,
                    line_to_parse[start_index],
                    ws_before_marker,
                    ws_after_marker,
                )
                new_token = UnorderedListStartMarkdownToken(
                    line_to_parse[start_index], indent_level, extracted_whitespace
                )

                (
                    no_para_start_if_empty,
                    new_container_level_tokens,
                    line_to_parse,
                ) = ListBlockProcessor.__post_list(
                    token_stack,
                    token_document,
                    new_stack,
                    new_token,
                    line_to_parse,
                    remaining_whitespace,
                    after_marker_ws_index,
                    indent_level,
                    current_container_blocks,
                    close_open_blocks_fn,
                )
                assert new_container_level_tokens
                container_level_tokens.extend(new_container_level_tokens)
                did_process = True
                was_container_start = True

        return (
            did_process,
            was_container_start,
            end_of_ulist_start_index,
            no_para_start_if_empty,
            line_to_parse,
            container_level_tokens,
        )
        # pylint: enable=too-many-locals, too-many-arguments

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def handle_olist_block(
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
    ):
        """
        Handle the processing of a olist block.
        """

        end_of_olist_start_index = -1
        container_level_tokens = []
        if not did_process:
            (
                started_olist,
                index,
                my_count,
                end_of_olist_start_index,
            ) = ListBlockProcessor.is_olist_start(
                token_stack,
                line_to_parse,
                start_index,
                extracted_whitespace,
                adj_ws=adj_ws,
            )
            if started_olist:
                assert not container_level_tokens
                print("clt>>olist-start")

                (
                    indent_level,
                    remaining_whitespace,
                    ws_after_marker,
                    after_marker_ws_index,
                    ws_before_marker,
                    container_level_tokens,
                    stack_bq_count,
                ) = ListBlockProcessor.__pre_list(
                    token_stack,
                    line_to_parse,
                    index,
                    extracted_whitespace,
                    my_count,
                    stack_bq_count,
                    this_bq_count,
                    close_open_blocks_fn,
                )

                print(
                    "total="
                    + str(indent_level)
                    + ";ws-before="
                    + str(ws_before_marker)
                    + ";ws_after="
                    + str(ws_after_marker)
                )

                new_stack = OrderedListStackToken(
                    indent_level,
                    line_to_parse[start_index : index + 1],
                    ws_before_marker,
                    ws_after_marker,
                )
                new_token = OrderedListStartMarkdownToken(
                    line_to_parse[index],
                    line_to_parse[start_index:index],
                    indent_level,
                    extracted_whitespace,
                )

                (
                    no_para_start_if_empty,
                    new_container_level_tokens,
                    line_to_parse,
                ) = ListBlockProcessor.__post_list(
                    token_stack,
                    token_document,
                    new_stack,
                    new_token,
                    line_to_parse,
                    remaining_whitespace,
                    after_marker_ws_index,
                    indent_level,
                    current_container_blocks,
                    close_open_blocks_fn,
                )
                assert new_container_level_tokens
                container_level_tokens.extend(new_container_level_tokens)
                did_process = True
                was_container_start = True
        return (
            did_process,
            was_container_start,
            end_of_olist_start_index,
            no_para_start_if_empty,
            line_to_parse,
            container_level_tokens,
        )
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def list_in_process(
        token_stack,
        token_document,
        line_to_parse,
        start_index,
        extracted_whitespace,
        ind,
        close_open_blocks_fn,
    ):
        """
        Handle the processing of a line where there is a list in process.
        """

        container_level_tokens = []

        print("!!!!!FOUND>>" + str(token_stack[ind]))
        print("!!!!!FOUND>>" + str(token_stack[ind].extra_data))
        requested_list_indent = token_stack[ind].indent_level
        before_ws_length = token_stack[ind].ws_before_marker
        print(
            "!!!!!requested_list_indent>>"
            + str(requested_list_indent)
            + ",before_ws="
            + str(before_ws_length)
        )

        leading_space_length = ParserHelper.calculate_length(extracted_whitespace)

        started_ulist, _ = ListBlockProcessor.is_ulist_start(
            token_stack,
            line_to_parse,
            start_index,
            extracted_whitespace,
            skip_whitespace_check=True,
        )
        started_olist, _, _, _ = ListBlockProcessor.is_olist_start(
            token_stack,
            line_to_parse,
            start_index,
            extracted_whitespace,
            skip_whitespace_check=True,
        )

        allow_list_continue = True
        if leading_space_length >= 4 and (started_ulist or started_olist):
            allow_list_continue = not token_document[-1].is_blank_line

        print(
            "leading_space_length>>"
            + str(leading_space_length)
            + ">>requested_list_indent>>"
            + str(requested_list_indent)
            + ">>is_in_paragraph>>"
            + str(token_stack[-1].is_paragraph)
        )
        if leading_space_length >= requested_list_indent and allow_list_continue:
            line_to_parse = ListBlockProcessor.adjust_line_for_list_in_process(
                line_to_parse, start_index, leading_space_length, requested_list_indent
            )
        else:
            requested_list_indent = requested_list_indent - before_ws_length
            print(
                "leading_space_length>>"
                + str(leading_space_length)
                + ">>adj requested_list_indent>>"
                + str(requested_list_indent)
                + ">>"
                + str(token_stack[-1].is_paragraph)
                + "<<"
            )
            if (
                token_stack[-1].is_paragraph
                and leading_space_length >= requested_list_indent
                and allow_list_continue
            ):
                line_to_parse = ListBlockProcessor.adjust_line_for_list_in_process(
                    line_to_parse,
                    start_index,
                    requested_list_indent,
                    requested_list_indent,
                )
            else:
                container_level_tokens = ListBlockProcessor.check_for_list_closures(
                    line_to_parse,
                    token_stack,
                    token_document,
                    start_index,
                    extracted_whitespace,
                    close_open_blocks_fn,
                    ind,
                )

        return container_level_tokens, line_to_parse
        # pylint: enable=too-many-arguments

    @staticmethod
    def adjust_line_for_list_in_process(
        line_to_parse, start_index, leading_space_length, requested_list_indent
    ):
        """
        Alter the current line to better represent the current level of lists.
        """
        print("enough ws to continue")
        remaining_indent = leading_space_length - requested_list_indent
        line_to_parse = "".rjust(remaining_indent, " ") + line_to_parse[start_index:]
        return line_to_parse

    # pylint: disable=too-many-arguments
    @staticmethod
    def check_for_list_closures(
        line_to_parse,
        token_stack,
        token_document,
        start_index,
        extracted_whitespace,
        close_open_blocks_fn,
        ind,
    ):
        """
        Check to see if the list in progress and the level of lists shown require
        the closing of some of the sublists.
        """
        container_level_tokens = []
        print("ws(naa)>>line_to_parse>>" + line_to_parse + "<<")
        print("ws(naa)>>stack>>" + str(token_stack))
        print("ws(naa)>>tokens>>" + str(token_document))

        is_theme_break, _ = LeafBlockProcessor.is_thematic_break(
            line_to_parse,
            start_index,
            extracted_whitespace,
            skip_whitespace_check=True,
        )
        print("ws(naa)>>is_theme_break>>" + str(is_theme_break))

        if not token_stack[-1].is_paragraph or is_theme_break:
            print("ws (normal and adjusted) not enough to continue")

            container_level_tokens, _, _ = close_open_blocks_fn(
                until_this_index=ind, include_lists=True
            )
        else:
            print("ws (normal and adjusted) continue")
        return container_level_tokens

    # pylint: enable=too-many-arguments
