"""Module to help with the continuation or stopping of a table block.
"""

import copy
from typing import List, Optional, Tuple, cast

from pymarkdown.container_blocks.container_grab_bag import POGGER
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.leaf_blocks.table_block_parse_helper import TableParseHelper
from pymarkdown.leaf_blocks.table_block_tuple import TableTuple
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import TableBlockStackToken
from pymarkdown.tokens.table_markdown_tokens import (
    TableMarkdownBodyToken,
    TableMarkdownHeaderItemToken,
    TableMarkdownHeaderToken,
    TableMarkdownRowItemToken,
    TableMarkdownRowToken,
    TableMarkdownToken,
)
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken

# pylint: disable=too-few-public-methods


class TableBlockContinuationHelper:
    """Class to help with the continuation or stopping of a table block."""

    # pylint: disable=too-many-arguments
    @staticmethod
    def determine_continue_or_stop(
        parser_state: ParserState,
        position_marker: PositionMarker,
        was_started: bool,
        remaining_line_to_parse: str,
        extracted_whitespace: str,
        unmodified_line_to_parse: str,
        original_stack_depth: int,
        original_document_depth: int,
        end_table_index: int,
        line_to_parse_size: int,
        is_blank_line: bool,
        did_complete_table: bool,
        parsed_table_tuple: Optional[TableTuple],
        lines_to_requeue: List[str],
    ) -> Tuple[bool, bool, List[MarkdownToken]]:
        """
        Determine whether to continue with the processing of the table.
        """
        if did_pause_table := (
            end_table_index >= 0
            and end_table_index == line_to_parse_size
            and not is_blank_line
        ):
            POGGER.debug(">>parse_table>>continuation")
            TableBlockContinuationHelper.__add_line_for_table_continuation(
                parser_state,
                position_marker,
                was_started,
                remaining_line_to_parse,
                extracted_whitespace,
                unmodified_line_to_parse,
                original_stack_depth,
                original_document_depth,
            )
        if not did_pause_table and was_started or did_complete_table:
            return TableBlockContinuationHelper.__stop_table_continuation(
                parser_state,
                did_complete_table,
                parsed_table_tuple,
                lines_to_requeue,
                did_pause_table,
            )

        POGGER.debug(">>parse_table>>other")
        return did_pause_table, False, []

    # pylint: enable=too-many-arguments

    @staticmethod
    def __stop_table_continuation(
        parser_state: ParserState,
        did_complete_table: bool,
        parsed_table_tuple: Optional[TableTuple],
        lines_to_requeue: List[str],
        did_pause_table: bool,
    ) -> Tuple[bool, bool, List[MarkdownToken]]:
        """
        As part of processing a table, stop a continuation.
        """
        POGGER.debug(">>parse_table>>no longer need start")
        if did_complete_table:
            assert parsed_table_tuple, "Table tuple must be defined by now."
            assert (
                parsed_table_tuple.normalized_destination is not None
            ), "normalized_destination must be defined by now."
            ## Different from LRD.
            # did_add_definition = False  # LinkParseHelper.add_link_definition(                parsed_table_tuple.normalized_destination, parsed_table_tuple.link_titles            )
            ## Different from LRD.
            table_stack_token = cast(TableBlockStackToken, parser_state.token_stack[-1])
            assert (
                table_stack_token.extracted_whitespace is not None
            ), "extracted_whitespace must be defined by now."
            extracted_whitespace = table_stack_token.extracted_whitespace

            POGGER.debug(
                "table_stack_token.extracted_whitespace>:$:<",
                table_stack_token.extracted_whitespace,
            )
            POGGER.debug(
                "table_stack_token.continuation_lines>:$:<",
                table_stack_token.continuation_lines,
            )
            POGGER.debug(
                "table_stack_token.unmodified_lines>:$:<",
                table_stack_token.unmodified_lines,
            )
            POGGER.debug("lines_to_requeue>:$:<", lines_to_requeue)

            does_any_line_have_tabs = any(
                ParserHelper.tab_character in ffg
                for ffg in table_stack_token.unmodified_lines
            )
            POGGER.debug("does_any_line_have_tabs>:$:<", does_any_line_have_tabs)

            last_container_index = parser_state.find_last_container_on_stack()
            if does_any_line_have_tabs and last_container_index > 0:
                (
                    extracted_whitespace,
                    parsed_table_tuple,
                ) = TableBlockContinuationHelper.__stop_table_continuation_with_tab(
                    parser_state,
                    table_stack_token,
                    ## Different from LRD.
                    lines_to_requeue,
                    ## Different from LRD.
                    parsed_table_tuple,
                )

            new_tokens: List[MarkdownToken] = (
                TableBlockContinuationHelper.__create_new_tokens(
                    table_stack_token, parsed_table_tuple, extracted_whitespace, False
                )
            )

            del parser_state.token_stack[-1]
            ## Different from LRD.
            TableBlockContinuationHelper.__stop_table_continuation_end(
                parser_state, new_tokens
            )
            ## Different from LRD.
            return did_pause_table, len(lines_to_requeue) > 1, new_tokens

        del parser_state.token_stack[-1]
        return did_pause_table, True, []

    ## Different from LRD.
    @staticmethod
    def __create_new_tokens(
        table_stack_token: TableBlockStackToken,
        parsed_table_tuple: TableTuple,
        extracted_whitespace: str,
        did_add_definition: bool,
    ) -> List[MarkdownToken]:
        _ = (extracted_whitespace, did_add_definition)
        # assert (
        #     parsed_table_tuple.normalized_destination is not None
        # ), "normalized_destination must be defined by now."

        new_tokens: List[MarkdownToken] = []

        ## Different from LRD.
        start_token = TableMarkdownToken(
            position_marker=table_stack_token.start_position_marker,
        )

        start_header_token = TableMarkdownHeaderToken(
            parsed_table_tuple.xyz[0],
            parsed_table_tuple.xyz[1],
            position_marker=table_stack_token.start_position_marker,
        )
        new_tokens.extend((start_token, start_header_token))

        line_number = table_stack_token.start_position_marker.line_number
        column_number = (
            table_stack_token.start_position_marker.index_number
            + table_stack_token.start_position_marker.index_indent
            + 1
        )
        if start_header_token.did_header_row_start_with_separator:
            column_number += 1
        for next_column_index, next_column in enumerate(
            parsed_table_tuple.xyz[0].columns
        ):
            column_number += len(next_column.leading_whitespace)
            start_header_item_token = TableMarkdownHeaderItemToken(
                next_column.leading_whitespace,
                parsed_table_tuple.col_as[next_column_index],
                line_number=line_number,
                column_number=column_number,
            )
            new_tokens.extend(
                (
                    start_header_item_token,
                    TextMarkdownToken(
                        next_column.text,
                        "",
                        line_number=line_number,
                        column_number=column_number,
                    ),
                    start_header_item_token.generate_close_markdown_token_from_markdown_token(
                        next_column.trailing_whitespace, ""
                    ),
                )
            )
            column_number += len(next_column.text) + len(
                next_column.trailing_whitespace
            )
        new_tokens.append(
            start_header_token.generate_close_markdown_token_from_markdown_token("", "")
        )

        if len(parsed_table_tuple.xyz) > 2:
            TableBlockContinuationHelper.__stop_table_continuation_body(
                new_tokens, table_stack_token, parsed_table_tuple
            )

        new_tokens.append(
            start_token.generate_close_markdown_token_from_markdown_token("", "")
        )
        return new_tokens

    ## Different from LRD.

    ## Different from LRD.
    @staticmethod
    def __stop_table_continuation_end(
        parser_state: ParserState, new_tokens: List[MarkdownToken]
    ) -> None:
        if parser_state.token_stack[-1].is_paragraph:
            tokens_from_close, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=(len(parser_state.token_stack) - 1),
            )
            assert len(tokens_from_close) == 1, "Only one token should be returned."
            new_tokens.insert(0, tokens_from_close[0])

    ## Different from LRD.

    ## Different from LRD.
    # pylint: disable=too-many-locals
    @staticmethod
    def __stop_table_continuation_body(
        new_tokens: List[MarkdownToken],
        table_stack_token: TableBlockStackToken,
        parsed_table_tuple: TableTuple,
    ) -> None:
        line_number = table_stack_token.start_position_marker.line_number + 2
        extracted_ws_len = (
            len(table_stack_token.extracted_whitespace)
            if table_stack_token.extracted_whitespace is not None
            else 0
        )
        base_column_number = (
            table_stack_token.start_position_marker.index_number
            + table_stack_token.start_position_marker.index_indent
            + 1
            - extracted_ws_len
        )

        start_body_token = TableMarkdownBodyToken(
            line_number=line_number, column_number=base_column_number
        )
        new_tokens.append(start_body_token)

        for next_row_index in range(2, len(parsed_table_tuple.xyz)):

            next_table_row = parsed_table_tuple.xyz[next_row_index]
            abc = next_table_row.columns[: len(parsed_table_tuple.col_as)]
            abc_after = next_table_row.columns[len(parsed_table_tuple.col_as) :]
            aaa_string = (
                "".join(
                    f"{ii.leading_whitespace}{ii.text}{ii.trailing_whitespace}"
                    for ii in abc_after
                )
                if abc_after
                else ""
            )
            delta = len(parsed_table_tuple.col_as) - len(abc)

            start_row_token = TableMarkdownRowToken(
                next_table_row.extracted_whitespace,
                next_table_row.trailing_whitespace,
                next_table_row.did_start_with_separator,
                delta,
                line_number=line_number,
                column_number=base_column_number,
            )
            new_tokens.append(start_row_token)

            column_number = base_column_number + int(
                next_table_row.did_start_with_separator
            )

            for next_column_index, next_column in enumerate(abc):

                column_number += len(next_column.leading_whitespace)
                start_row_item_token = TableMarkdownRowItemToken(
                    next_column.leading_whitespace,
                    parsed_table_tuple.col_as[next_column_index],
                    line_number=line_number,
                    column_number=column_number,
                )

                new_tokens.extend(
                    (
                        start_row_item_token,
                        TextMarkdownToken(
                            next_column.text,
                            "",
                            line_number=line_number,
                            column_number=column_number,
                        ),
                        start_row_item_token.generate_close_markdown_token_from_markdown_token(
                            next_column.trailing_whitespace, ""
                        ),
                    )
                )
                column_number += len(next_column.text) + len(
                    next_column.trailing_whitespace
                )
            new_tokens.append(
                start_row_token.generate_close_markdown_token_from_markdown_token(
                    aaa_string, ""
                )
            )
            line_number += 1
        new_tokens.append(
            start_body_token.generate_close_markdown_token_from_markdown_token("", "")
        )

    ## Different from LRD.

    # pylint: enable=too-many-locals

    @staticmethod
    def __stop_table_continuation_with_tab(
        parser_state: ParserState,
        table_stack_token: TableBlockStackToken,
        ## Different from LRD.
        lines_to_requeue: List[str],
        ## Different from LRD.
        parsed_table_tuple: TableTuple,
    ) -> Tuple[str, TableTuple]:
        _ = lines_to_requeue

        POGGER.debug(
            "extracted_whitespace>:$:<",
            table_stack_token.extracted_whitespace,
        )
        last_block_quote_index = parser_state.find_last_block_quote_on_stack()
        if last_block_quote_index:
            last_block_quote_token = parser_state.token_stack[last_block_quote_index]
            block_quote_token = cast(
                BlockQuoteMarkdownToken, last_block_quote_token.matching_markdown_token
            )
        else:
            block_quote_token = None
        last_list_index = parser_state.find_last_list_block_on_stack()
        if last_list_index:
            last_list_token = parser_state.token_stack[last_list_index]
            list_token = cast(
                ListStartMarkdownToken, last_list_token.matching_markdown_token
            )
        else:
            list_token = None

        POGGER.debug(
            "table_stack_token.continuation_lines>:$:<",
            table_stack_token.continuation_lines,
        )
        POGGER.debug(
            "table_stack_token.unmodified_lines>:$:<",
            table_stack_token.unmodified_lines,
        )

        if last_block_quote_index > last_list_index:
            assert block_quote_token is not None
            assert block_quote_token.bleading_spaces is not None
            split_container_spaces = block_quote_token.bleading_spaces.split("\n")
        else:
            assert list_token is not None
            assert list_token.leading_spaces is not None
            split_container_spaces = list_token.leading_spaces.split("\n")

        ## Different from LRD.
        assert len(table_stack_token.continuation_lines) > 1
        (
            extracted_whitespace,
            parsed_table_tuple,
        ) = TableBlockContinuationHelper.__stop_table_continuation_with_tab_multiple(
            parser_state,
            table_stack_token,
            block_quote_token,
            last_block_quote_index,
            list_token,
            last_list_index,
            split_container_spaces,
        )
        # if len(table_stack_token.continuation_lines) == 1:
        #     extracted_whitespace = (
        #         TableBlockContinuationHelper.__stop_table_continuation_with_tab_single(
        #             parser_state,
        #             table_stack_token,
        #             last_block_quote_index,
        #             last_list_index,
        #             split_container_spaces
        #         )
        #     )
        # else:
        #     (
        #         extracted_whitespace,
        #         parsed_table_tuple,
        #     ) = TableBlockContinuationHelper.__stop_table_continuation_with_tab_multiple(
        #         parser_state,
        #         table_stack_token,
        #         block_quote_token,
        #         last_block_quote_index,
        #         list_token,
        #         last_list_index,
        #         split_container_spaces
        #     )
        ## Different from LRD.

        return extracted_whitespace, parsed_table_tuple

    ## Different from LRD.
    # @staticmethod
    # def __stop_table_continuation_with_tab_single(
    #     parser_state: ParserState,
    #     table_stack_token: TableBlockStackToken,
    #     last_block_quote_index: int,
    #     last_list_index: int,
    #     split_container_spaces: List[str],
    # ) -> str:
    #     parsed_lines = table_stack_token.continuation_lines[0]
    #     original_lines = table_stack_token.unmodified_lines[0]

    #     current_line_container_spaces = (
    #         split_container_spaces[-2]
    #         if len(split_container_spaces) >= 2
    #         else split_container_spaces[-1]
    #     )
    #     (
    #         extracted_whitespace,
    #         split_tab,
    #         _,
    #     ) = TableBlockContinuationHelper.__find_line_ws(parsed_lines, original_lines, current_line_container_spaces)

    #     if split_tab:
    #         if last_block_quote_index > last_list_index:
    #             TabHelper.adjust_block_quote_indent_for_tab(parser_state)
    #         else:
    #             TabHelper.adjust_block_quote_indent_for_tab(
    #                 parser_state, extracted_whitespace=extracted_whitespace
    #             )
    #     # POGGER.debug(
    #     #     "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
    #     # )
    #     return extracted_whitespace
    ## Different from LRD.

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __stop_table_continuation_with_tab_multiple(
        parser_state: ParserState,
        table_stack_token: TableBlockStackToken,
        block_quote_token: Optional[BlockQuoteMarkdownToken],
        last_block_quote_index: int,
        list_token: Optional[ListStartMarkdownToken],
        last_list_index: int,
        split_container_spaces: List[str],
    ) -> Tuple[str, TableTuple]:
        split_tabs_list: List[bool] = []
        completed_lrd_text: str = ""
        extracted_whitespace = ""
        alt_ws: Optional[str] = None
        for this_line_index, this_line in enumerate(
            table_stack_token.continuation_lines
        ):
            (
                completed_lrd_text,
                extracted_whitespace,
                alt_ws,
            ) = TableBlockContinuationHelper.__stop_table_continuation_with_tab_multiple_loop(
                table_stack_token,
                this_line_index,
                this_line,
                completed_lrd_text,
                extracted_whitespace,
                alt_ws,
                split_tabs_list,
                split_container_spaces,
            )

        POGGER.debug("completed_lrd_text>:$:<", completed_lrd_text)
        assert alt_ws is not None, "This value must be set inside of the for loop."

        (
            did_succeed,
            next_index,
            new_parsed_table_tuple,
        ) = TableParseHelper.parse_table(
            parser_state, completed_lrd_text, 0, alt_ws, True, "", True
        )
        assert (
            did_succeed
        ), "Since this is the stop and there is at least one valid match, this must be true."
        assert (
            len(completed_lrd_text) == next_index
        ), "Index must be at the end of the stirng."
        assert new_parsed_table_tuple is not None, "New tuple must be defined."

        if last_block_quote_index > last_list_index:
            assert block_quote_token is not None
            TableBlockContinuationHelper.__xx_multiple_fix_bleading_spaces(
                block_quote_token, split_tabs_list, table_stack_token
            )
        else:
            assert list_token is not None
            TableBlockContinuationHelper.__xx_multiple_fix_leading_spaces(
                list_token, split_tabs_list, table_stack_token
            )
        return extracted_whitespace, new_parsed_table_tuple

    # pylint: enable=too-many-arguments, too-many-locals

    # # pylint: disable=too-many-arguments
    @staticmethod
    def __stop_table_continuation_with_tab_multiple_loop(
        table_stack_token: TableBlockStackToken,
        this_line_index: int,
        this_line: str,
        completed_lrd_text: str,
        extracted_whitespace: str,
        alt_ws: Optional[str],
        split_tabs_list: List[bool],
        split_container_spaces: List[str],
    ) -> Tuple[str, str, Optional[str]]:
        original_this_line = table_stack_token.unmodified_lines[this_line_index]
        POGGER.debug("this_line_index>:$:<", this_line_index)
        POGGER.debug("this_line>:$:<", this_line)
        POGGER.debug("original_this_line>:$:<", original_this_line)

        spaces_index = (
            len(split_container_spaces)
            - len(table_stack_token.unmodified_lines)
            + this_line_index
        )
        (
            extracted_ws,
            split_tab,
            start_whitespace_index,
        ) = TableBlockContinuationHelper.__find_line_ws(
            this_line, original_this_line, split_container_spaces[spaces_index]
        )

        if completed_lrd_text:
            completed_lrd_text += "\n"
        if this_line_index == 0:
            extracted_whitespace, alt_ws = (
                TableBlockContinuationHelper.__stop_table_continuation_with_tab_multiple_loop_1(
                    extracted_ws,
                    start_whitespace_index,
                    split_container_spaces,
                    spaces_index,
                )
            )
            # x2 = extracted_whitespace[tabified_whitespace_index:]
            # end if
        else:
            completed_lrd_text += extracted_ws
        completed_lrd_text += this_line
        split_tabs_list.append(split_tab)
        return completed_lrd_text, extracted_whitespace, alt_ws

    # # pylint: enable=too-many-arguments

    @staticmethod
    def __stop_table_continuation_with_tab_multiple_loop_1(
        extracted_ws: str,
        start_whitespace_index: int,
        split_container_spaces: List[str],
        spaces_index: int,
    ) -> Tuple[str, str]:
        extracted_whitespace = extracted_ws
        alt_ws = TabHelper.detabify_string(extracted_whitespace, start_whitespace_index)
        assert "\t" in extracted_whitespace
        # if "\t" in extracted_whitespace:
        current_container_spaces = split_container_spaces[spaces_index]
        dccs = TabHelper.detabify_string(current_container_spaces)
        tabified_whitespace_index = 1
        xx = extracted_whitespace[:tabified_whitespace_index]
        detabified_whitespace = TabHelper.detabify_string(xx)
        detabified_length = len(detabified_whitespace)
        while tabified_whitespace_index < (
            len(extracted_whitespace) + 1
        ) and detabified_length < len(dccs):
            xx = extracted_whitespace[:tabified_whitespace_index]
            detabified_whitespace = TabHelper.detabify_string(xx)
            detabified_length = len(detabified_whitespace)
            tabified_whitespace_index += 1

        assert tabified_whitespace_index >= len(
            extracted_whitespace
        ) + 1 or detabified_length >= len(dccs)
        tabified_whitespace_index += 1
        tabified_whitespace_index -= 1
        alt_ws = extracted_whitespace[:tabified_whitespace_index]
        return extracted_whitespace, alt_ws

    @staticmethod
    def __find_line_ws(
        parsed_lines: str, original_lines: str, wsx: str
    ) -> Tuple[str, bool, int]:
        start_text_index = original_lines.find(parsed_lines)
        assert start_text_index != -1, "Index must be found within string."
        # POGGER.debug("start_text_index>:$:<", start_text_index)
        # start_whitespace_index, _ = ParserHelper.extract_spaces_from_end(
        #     original_lines, start_text_index
        # )
        start_whitespace_index = 0
        # POGGER.debug("start_whitespace_index>:$:<", start_whitespace_index)
        tabified_whitespace = original_lines[start_whitespace_index:start_text_index]
        # POGGER.debug("tabified_whitespace>:$:<", tabified_whitespace)

        split_tab = "\t" in tabified_whitespace
        assert split_tab
        # if split_tab:
        tabified_whitespace_index = 1
        detabified_whitespace = ""
        detabified_length = -1
        while tabified_whitespace_index < (
            len(tabified_whitespace) + 1
        ) and detabified_length < len(wsx):
            detabified_whitespace = TabHelper.detabify_string(
                tabified_whitespace[:tabified_whitespace_index]
            )
            detabified_length = len(detabified_whitespace)
            tabified_whitespace_index += 1
        tabified_whitespace_index -= 1
        does_end__with_bq_tab = (
            bool(wsx)
            and wsx[-1] == ">"
            and tabified_whitespace_index < len(tabified_whitespace)
            and tabified_whitespace[tabified_whitespace_index] == "\t"
        )
        split_tab = len(detabified_whitespace) != len(wsx) or does_end__with_bq_tab
        # endif
        if split_tab:
            if not does_end__with_bq_tab:
                tabified_whitespace_index = 0
                while (
                    tabified_whitespace_index < len(wsx)
                    and wsx[tabified_whitespace_index] == " "
                    and tabified_whitespace[tabified_whitespace_index] == " "
                ):
                    tabified_whitespace_index += 1
            tabified_whitespace = tabified_whitespace[tabified_whitespace_index:]
        if not split_tab:
            tabified_whitespace = tabified_whitespace[len(wsx) :]
        extracted_whitespace = tabified_whitespace
        # POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
        # POGGER.debug("split_tab>:$:<", split_tab)
        return extracted_whitespace, split_tab, start_whitespace_index

    @staticmethod
    def __xx_multiple_fix_bleading_spaces(
        block_quote_token: BlockQuoteMarkdownToken,
        split_tabs_list: List[bool],
        table_stack_token: TableBlockStackToken,
    ) -> None:
        POGGER.debug("split_tabs_list>:$:<", split_tabs_list)
        POGGER.debug(
            "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        )
        assert (
            block_quote_token.bleading_spaces is not None
        ), "Bleading spaces must be defined by now."
        leading_spaces: List[str] = []
        for _ in table_stack_token.continuation_lines:
            last_leading_space = block_quote_token.remove_last_bleading_space()
            POGGER.debug("last_leading_space>:$:<", last_leading_space)
            # if last_leading_space[0] == "\n":
            #     last_leading_space = last_leading_space[1:]
            leading_spaces.insert(0, last_leading_space)
        assert len(split_tabs_list) == len(
            leading_spaces
        ), "The two lists must have the same length."
        POGGER.debug("leading_spaces>:$:<", leading_spaces)
        POGGER.debug(
            "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        )
        is_first = not block_quote_token.bleading_spaces
        for prefix_to_add in leading_spaces:
            # if split_tabs_list[0] and prefix_to_add[-1] == " "):
            #   prefix_to_add = prefix_to_add[:-1]
            assert not (split_tabs_list[0] and prefix_to_add[-1] == " ")
            del split_tabs_list[0]
            POGGER.debug(
                "__xx_multiple_fix_leading_spaces>>block_token>>$", block_quote_token
            )
            block_quote_token.add_bleading_spaces(prefix_to_add, is_first)
            POGGER.debug(
                "__xx_multiple_fix_leading_spaces>>block_token>>$", block_quote_token
            )
            is_first = False

    @staticmethod
    def __xx_multiple_fix_leading_spaces(
        list_token: ListStartMarkdownToken,
        split_tabs_list: List[bool],
        table_stack_token: TableBlockStackToken,
    ) -> None:
        POGGER.debug("split_tabs_list>:$:<", split_tabs_list)
        POGGER.debug("list_token.leading_spaces>:$:<", list_token.leading_spaces)
        assert (
            list_token.leading_spaces is not None
        ), "leading spaces must be defined by now."
        leading_spaces: List[str] = []
        for _ in table_stack_token.continuation_lines:
            last_leading_space = list_token.remove_last_leading_space()
            POGGER.debug("last_leading_space>:$:<", last_leading_space)
            assert last_leading_space is not None
            leading_spaces.insert(0, last_leading_space)
        assert len(split_tabs_list) == len(
            leading_spaces
        ), "The two lists must have the same length."
        POGGER.debug("leading_spaces>:$:<", leading_spaces)
        POGGER.debug("list_token.leading_spaces>:$:<", list_token.leading_spaces)
        for current_leading_space_index, prefix_to_add in enumerate(leading_spaces):
            if split_tabs_list[0]:
                current_unmodified_line = table_stack_token.unmodified_lines[
                    current_leading_space_index
                ]
                continuation_start_index = current_unmodified_line.find(
                    table_stack_token.continuation_lines[current_leading_space_index]
                )
                unmodified_line_prefix = current_unmodified_line[
                    :continuation_start_index
                ]

                unmodified_line_prefix_index = 0
                detabified_length = -1
                while unmodified_line_prefix_index < len(
                    unmodified_line_prefix
                ) and detabified_length < len(prefix_to_add):
                    detabified_length = len(
                        TabHelper.detabify_string(
                            unmodified_line_prefix[: unmodified_line_prefix_index + 1]
                        )
                    )
                    unmodified_line_prefix_index += 1

                unmodified_line_prefix_index -= 1
                assert unmodified_line_prefix_index < len(
                    unmodified_line_prefix
                ), "Index must be within the string."
                assert unmodified_line_prefix[unmodified_line_prefix_index] == "\t"
                prefix_to_add = unmodified_line_prefix[:unmodified_line_prefix_index]
            del split_tabs_list[0]
            POGGER.debug(
                "__xx_multiple_fix_bleading_spaces>>block_token>>$", list_token
            )
            list_token.add_leading_spaces(prefix_to_add)
            POGGER.debug(
                "__xx_multiple_fix_bleading_spaces>>block_token>>$", list_token
            )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_line_for_table_continuation(
        parser_state: ParserState,
        position_marker: PositionMarker,
        was_started: bool,
        remaining_line_to_parse: str,
        extracted_whitespace: str,
        unmodified_line_to_parse: str,
        original_stack_depth: int,
        original_document_depth: int,
    ) -> None:
        """
        As part of processing a table, add a line to the continuation.
        """

        line_to_store = remaining_line_to_parse
        if not was_started:
            POGGER.debug(">>parse_table>>marking start")
            new_token = TableBlockStackToken(extracted_whitespace, position_marker)
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

            ## Different from LRD.
            lbqi = parser_state.find_last_block_quote_on_stack()
            new_token.last_block_quote_stack_token = (
                parser_state.token_stack[lbqi] if lbqi else None
            )
            new_token.last_block_quote_markdown_token_index = None
            new_token.copy_of_last_block_quote_markdown_token = None
            if new_token.last_block_quote_stack_token:
                markdown_token = parser_state.token_stack[lbqi].matching_markdown_token
                assert markdown_token is not None
                new_token.last_block_quote_markdown_token_index = (
                    parser_state.token_document.index(markdown_token)
                )
                new_token.copy_of_last_block_quote_markdown_token = cast(
                    BlockQuoteMarkdownToken,
                    copy.deepcopy(
                        parser_state.token_document[
                            new_token.last_block_quote_markdown_token_index
                        ]
                    ),
                )

            new_token.copy_of_token_stack = parser_state.copy_of_token_stack
            ## Different from LRD.

            new_token.x1_token = parser_state.x1_token
            new_token.copy_of_x1_token = parser_state.copy_of_x1_token
            new_token.x1_token_index = parser_state.x1_token_index
        else:
            new_token = cast(TableBlockStackToken, parser_state.token_stack[-1])

        POGGER.debug(">>line_to_store>>add>:$<<", line_to_store)
        POGGER.debug(">>unmodified_line_to_parse>>add>:$<<", unmodified_line_to_parse)
        assert unmodified_line_to_parse.endswith(
            line_to_store
        ), "Unmodified line must end with the processed line."
        new_token.add_continuation_line(line_to_store)
        new_token.add_unmodified_line(unmodified_line_to_parse)

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
