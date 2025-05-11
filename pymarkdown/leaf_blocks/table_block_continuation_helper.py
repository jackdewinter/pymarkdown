"""Module to help with the continuation or stopping of a table block.
"""

import copy
from typing import List, Optional, Tuple, cast

from pymarkdown.container_blocks.container_grab_bag import POGGER
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.leaf_blocks.table_block_tuple import TableTuple
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
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

    # pylint: disable=too-many-arguments, too-many-locals
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
        process_mode: int,
    ) -> Tuple[bool, bool, List[MarkdownToken], bool]:
        """
        Determine whether to continue with the processing of the table.
        """
        # TODO leave in until testing of tables with tabs is complete.
        _ = (process_mode, extracted_whitespace)

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
        return did_pause_table, False, [], False

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __stop_table_continuation(
        parser_state: ParserState,
        did_complete_table: bool,
        parsed_table_tuple: Optional[TableTuple],
        lines_to_requeue: List[str],
        did_pause_table: bool,
    ) -> Tuple[bool, bool, List[MarkdownToken], bool]:
        """
        As part of processing a table, stop a continuation.
        """
        POGGER.debug(">>parse_table>>no longer need start")
        if did_complete_table:
            assert parsed_table_tuple, "Table tuple must be defined by now."
            assert (
                parsed_table_tuple.normalized_destination is not None
            ), "normalized_destination must be defined by now."
            # TODO remove nd from parsed_table_tuple
            # did_add_definition = False  # LinkParseHelper.add_link_definition(                parsed_table_tuple.normalized_destination, parsed_table_tuple.link_titles            )
            table_stack_token = cast(TableBlockStackToken, parser_state.token_stack[-1])
            # assert (
            #     link_def_token.extracted_whitespace is not None
            # ), "extracted_whitespace must be defined by now."
            # extracted_whitespace = link_def_token.extracted_whitespace

            # POGGER.debug(
            #     "link_def_token.extracted_whitespace>:$:<",
            #     link_def_token.extracted_whitespace,
            # )
            # POGGER.debug(
            #     "link_def_token.continuation_lines>:$:<",
            #     link_def_token.continuation_lines,
            # )
            # POGGER.debug(
            #     "link_def_token.unmodified_lines>:$:<", link_def_token.unmodified_lines
            # )
            POGGER.debug("lines_to_requeue>:$:<", lines_to_requeue)

            does_any_line_have_tabs = any(
                ParserHelper.tab_character in ffg
                for ffg in table_stack_token.unmodified_lines
            )
            POGGER.debug("does_any_line_have_tabs>:$:<", does_any_line_have_tabs)

            # last_container_index = parser_state.find_last_container_on_stack()
            # if does_any_line_have_tabs and last_container_index > 0:
            #     (
            #         extracted_whitespace,
            #         parsed_table_tuple,
            #     ) = TableBlockContinuationHelper.__stop_table_continuation_with_tab(
            #         parser_state,
            #         table_stack_token,
            #         last_container_index,
            #         lines_to_requeue,
            #         process_mode,
            #         extracted_whitespace,
            #         parsed_table_tuple,
            #     )

            assert (
                parsed_table_tuple.normalized_destination is not None
            ), "normalized_destination must be defined by now."
            new_tokens: List[MarkdownToken] = []

            start_token = TableMarkdownToken(
                position_marker=table_stack_token.start_position_marker,
            )

            start_header_token = TableMarkdownHeaderToken(
                parsed_table_tuple.xyz[0],
                parsed_table_tuple.xyz[1],
                position_marker=table_stack_token.start_position_marker,
            )
            new_tokens.extend((start_token, start_header_token))

            for next_column_index, next_column in enumerate(
                parsed_table_tuple.xyz[0].columns
            ):
                start_header_item_token = TableMarkdownHeaderItemToken(
                    next_column.leading_whitespace,
                    parsed_table_tuple.col_as[next_column_index],
                    position_marker=table_stack_token.start_position_marker,
                )
                new_tokens.extend(
                    (
                        start_header_item_token,
                        TextMarkdownToken(
                            next_column.text,
                            "",
                            position_marker=table_stack_token.start_position_marker,
                        ),
                        start_header_item_token.generate_close_markdown_token_from_markdown_token(
                            next_column.trailing_whitespace, ""
                        ),
                    )
                )
            new_tokens.append(
                start_header_token.generate_close_markdown_token_from_markdown_token(
                    "", ""
                )
            )

            if len(parsed_table_tuple.xyz) > 2:
                TableBlockContinuationHelper.__stop_table_continuation_body(
                    new_tokens, table_stack_token, parsed_table_tuple
                )

            new_tokens.append(
                start_token.generate_close_markdown_token_from_markdown_token("", "")
            )

            # POGGER.debug(">>link_info>>$", parsed_table_tuple.link_info)
            # assert parsed_table_tuple.link_info.line_destination_whitespace is not None
            # POGGER.debug(
            #     ">>line_destination_whitespace>>$",
            #     ParserHelper.make_whitespace_visible(
            #         parsed_table_tuple.link_info.line_destination_whitespace
            #     ),
            # )
            TableBlockContinuationHelper.__stop_table_continuation_end(
                parser_state, new_tokens
            )
            return did_pause_table, len(lines_to_requeue) > 1, new_tokens, False

        del parser_state.token_stack[-1]
        return did_pause_table, True, [], True

    @staticmethod
    def __stop_table_continuation_end(
        parser_state: ParserState, new_tokens: List[MarkdownToken]
    ) -> None:
        POGGER.debug(">>new_tokens>>$", new_tokens)
        del parser_state.token_stack[-1]
        if parser_state.token_stack[-1].is_paragraph:
            tokens_from_close, _ = parser_state.close_open_blocks_fn(
                parser_state,
                until_this_index=(len(parser_state.token_stack) - 1),
            )
            assert len(tokens_from_close) == 1, "Only one token should be returned."
            new_tokens.insert(0, tokens_from_close[0])

    # pylint: disable=too-many-locals
    @staticmethod
    def __stop_table_continuation_body(
        new_tokens: List[MarkdownToken],
        table_stack_token: TableBlockStackToken,
        parsed_table_tuple: TableTuple,
    ) -> None:
        start_body_token = TableMarkdownBodyToken(
            position_marker=table_stack_token.start_position_marker
        )
        new_tokens.append(start_body_token)

        for next_row_index in range(2, len(parsed_table_tuple.xyz)):
            x = parsed_table_tuple.xyz[next_row_index]

            abc = x.columns[: len(parsed_table_tuple.col_as)]
            if abc_after := x.columns[len(parsed_table_tuple.col_as) :]:
                aaa: List[str] = []
                for ii in abc_after:
                    aaa.extend((ii.leading_whitespace, ii.text, ii.trailing_whitespace))
                aaa_string = "".join(aaa)
            else:
                aaa_string = ""
            delta = len(parsed_table_tuple.col_as) - len(abc)

            start_row_token = TableMarkdownRowToken(
                x.extracted_whitespace,
                x.trailing_whitespace,
                x.did_start_with_separator,
                delta,
                position_marker=table_stack_token.start_position_marker,
            )
            new_tokens.append(start_row_token)

            for next_column_index, next_column in enumerate(abc):
                start_row_item_token = TableMarkdownRowItemToken(
                    next_column.leading_whitespace,
                    parsed_table_tuple.col_as[next_column_index],
                    position_marker=table_stack_token.start_position_marker,
                )

                new_tokens.extend(
                    (
                        start_row_item_token,
                        TextMarkdownToken(
                            next_column.text,
                            "",
                            position_marker=table_stack_token.start_position_marker,
                        ),
                        start_row_item_token.generate_close_markdown_token_from_markdown_token(
                            next_column.trailing_whitespace, ""
                        ),
                    )
                )
            new_tokens.append(
                start_row_token.generate_close_markdown_token_from_markdown_token(
                    aaa_string, ""
                )
            )
        new_tokens.append(
            start_body_token.generate_close_markdown_token_from_markdown_token("", "")
        )

    # pylint: enable=too-many-locals

    # @staticmethod
    # def __stop_table_continuation_with_tab(
    #     parser_state: ParserState,
    #     table_stack_token: TableBlockStackToken,
    #     last_container_index: int,
    #     lines_to_requeue: List[str],
    #     process_mode: int,
    #     extracted_whitespace: str,
    #     parsed_table_tuple: TableTuple,
    # ) -> Tuple[str, TableTuple]:
    #     assert False
    #     POGGER.debug(
    #         "extracted_whitespace>:$:<",
    #         table_stack_token.extracted_whitespace,
    #     )
    #     assert parser_state.token_stack[
    #         last_container_index
    #     ].is_block_quote, "Container must be a block quote."
    #     last_block_quote_index = parser_state.find_last_block_quote_on_stack()
    #     last_block_quote_token = parser_state.token_stack[last_block_quote_index]
    #     block_quote_token = cast(
    #         BlockQuoteMarkdownToken, last_block_quote_token.matching_markdown_token
    #     )

    #     POGGER.debug(
    #         "table_stack_token.continuation_lines>:$:<", table_stack_token.continuation_lines
    #     )
    #     POGGER.debug(
    #         "table_stack_token.unmodified_lines>:$:<", table_stack_token.unmodified_lines
    #     )

    #     if len(table_stack_token.continuation_lines) == 1:
    #         extracted_whitespace = TableBlockContinuationHelper.__stop_table_continuation_with_tab_single(
    #             parser_state,
    #             table_stack_token,
    #             process_mode,
    #             block_quote_token,
    #             lines_to_requeue,
    #         )
    #     else:
    #         (
    #             extracted_whitespace,
    #             parsed_table_tuple,
    #         ) = TableBlockContinuationHelper.__stop_table_continuation_with_tab_multiple(
    #             parser_state, extracted_whitespace, table_stack_token, block_quote_token
    #         )

    #     return extracted_whitespace, parsed_table_tuple

    # @staticmethod
    # def __stop_table_continuation_with_tab_single(
    #     parser_state: ParserState,
    #     table_stack_token: TableBlockStackToken,
    #     process_mode: int,
    #     block_quote_token: BlockQuoteMarkdownToken,
    #     lines_to_requeue: List[str],
    # ) -> str:
    #     parsed_lines = table_stack_token.continuation_lines[0]
    #     original_lines = table_stack_token.unmodified_lines[0]

    #     (
    #         extracted_whitespace,
    #         split_tab,
    #         _,
    #     ) = TableBlockContinuationHelper.__find_line_ws(
    #         parsed_lines, original_lines
    #     )

    #     POGGER.debug("process_mode>:$:<", process_mode)
    #     POGGER.debug(
    #         "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
    #     )
    #     if process_mode == 1:
    #         block_quote_token.remove_last_bleading_space()
    #     else:
    #         for _ in lines_to_requeue:
    #             block_quote_token.remove_last_bleading_space()

    #     if split_tab:
    #         TabHelper.adjust_block_quote_indent_for_tab(parser_state)
    #     POGGER.debug(
    #         "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
    #     )
    #     return extracted_whitespace

    # @staticmethod
    # def __stop_table_continuation_with_tab_multiple(
    #     parser_state: ParserState,
    #     extracted_whitespace: str,
    #     table_stack_token: TableBlockStackToken,
    #     block_quote_token: BlockQuoteMarkdownToken,
    # ) -> Tuple[str, TableTuple]:
    #     assert False
    #     split_tabs_list: List[bool] = []
    #     completed_table_text: str = ""
    #     alt_ws: Optional[str] = None
    #     for this_line_index, this_line in enumerate(table_stack_token.continuation_lines):
    #         (
    #             completed_table_text,
    #             extracted_whitespace,
    #             alt_ws,
    #         ) = TableBlockContinuationHelper.__stop_table_continuation_with_tab_multiple_loop(
    #             table_stack_token,
    #             this_line_index,
    #             this_line,
    #             completed_table_text,
    #             extracted_whitespace,
    #             alt_ws,
    #             split_tabs_list,
    #         )

    #     POGGER.debug("completed_table_text>:$:<", completed_table_text)
    #     assert alt_ws is not None, "This value must be set inside of the for loop."

    #     (
    #         did_succeed,
    #         next_index,
    #         new_parsed_table_tuple,
    #     ) = TableParseHelper.parse_table(
    #         parser_state, completed_table_text, 0, alt_ws, True, ""
    #     )
    #     assert (
    #         did_succeed
    #     ), "Since this is the stop and there is at least one valid match, this must be true."
    #     assert (
    #         len(completed_table_text) == next_index
    #     ), "Index must be at the end of the stirng."
    #     assert new_parsed_table_tuple is not None, "New tuple must be defined."

    #     TableBlockContinuationHelper.__xx_multiple_fix_leading_spaces(
    #         block_quote_token, split_tabs_list, table_stack_token
    #     )
    #     return extracted_whitespace, new_parsed_table_tuple

    # # pylint: disable=too-many-arguments
    # @staticmethod
    # def __stop_table_continuation_with_tab_multiple_loop(
    #     table_stack_token: TableBlockStackToken,
    #     this_line_index: int,
    #     this_line: str,
    #     completed_table_text: str,
    #     extracted_whitespace: str,
    #     alt_ws: Optional[str],
    #     split_tabs_list: List[bool],
    # ) -> Tuple[str, str, Optional[str]]:
    #     assert False
    #     original_this_line = table_stack_token.unmodified_lines[this_line_index]
    #     POGGER.debug("this_line_index>:$:<", this_line_index)
    #     POGGER.debug("this_line>:$:<", this_line)
    #     POGGER.debug("original_this_line>:$:<", original_this_line)

    #     (
    #         extracted_ws,
    #         split_tab,
    #         start_whitespace_index,
    #     ) = TableBlockContinuationHelper.__find_line_ws(
    #         this_line, original_this_line
    #     )

    #     if completed_table_text:
    #         completed_table_text += "\n"
    #     if this_line_index == 0:
    #         extracted_whitespace = extracted_ws
    #         alt_ws = TabHelper.detabify_string(
    #             extracted_whitespace, start_whitespace_index
    #         )
    #     else:
    #         completed_table_text += extracted_ws
    #     completed_table_text += this_line
    #     split_tabs_list.append(split_tab)
    #     return completed_table_text, extracted_whitespace, alt_ws

    # # pylint: enable=too-many-arguments

    # @staticmethod
    # def __find_line_ws(parsed_lines: str, original_lines: str) -> Tuple[str, bool, int]:
    #     start_text_index = original_lines.find(parsed_lines)
    #     assert start_text_index != -1, "Index must be found within string."
    #     POGGER.debug("start_text_index>:$:<", start_text_index)
    #     start_whitespace_index, _ = ParserHelper.extract_spaces_from_end(
    #         original_lines, start_text_index
    #     )
    #     POGGER.debug("start_whitespace_index>:$:<", start_whitespace_index)
    #     tabified_whitespace = original_lines[start_whitespace_index:start_text_index]
    #     POGGER.debug("tabified_whitespace>:$:<", tabified_whitespace)
    #     split_tab = bool(tabified_whitespace and tabified_whitespace[0] == "\t")
    #     if not split_tab:
    #         tabified_whitespace = tabified_whitespace[1:]
    #         start_whitespace_index += 1
    #     extracted_whitespace = tabified_whitespace
    #     POGGER.debug("extracted_whitespace>:$:<", extracted_whitespace)
    #     POGGER.debug("split_tab>:$:<", split_tab)
    #     return extracted_whitespace, split_tab, start_whitespace_index

    # @staticmethod
    # def __xx_multiple_fix_leading_spaces(
    #     block_quote_token: BlockQuoteMarkdownToken,
    #     split_tabs_list: List[bool],
    #     table_stack_token: TableBlockStackToken,
    # ) -> None:
    #     POGGER.debug("split_tabs_list>:$:<", split_tabs_list)
    #     POGGER.debug(
    #         "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
    #     )
    #     assert (
    #         block_quote_token.bleading_spaces is not None
    #     ), "Bleading spaces must be defined by now."
    #     leading_spaces: List[str] = []
    #     for _ in table_stack_token.continuation_lines:
    #         last_leading_space = block_quote_token.remove_last_bleading_space()
    #         POGGER.debug("last_leading_space>:$:<", last_leading_space)
    #         # if last_leading_space[0] == "\n":
    #         #     last_leading_space = last_leading_space[1:]
    #         leading_spaces.append(last_leading_space)
    #     assert len(split_tabs_list) == len(
    #         leading_spaces
    #     ), "The two lists must have the same length."
    #     POGGER.debug("leading_spaces>:$:<", leading_spaces)
    #     POGGER.debug(
    #         "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
    #     )
    #     is_first = not block_quote_token.bleading_spaces
    #     for prefix_to_add in leading_spaces:
    #         if split_tabs_list[0]:
    #             prefix_to_add = prefix_to_add[:-1]
    #         del split_tabs_list[0]
    #         POGGER.debug(
    #             "__xx_multiple_fix_leading_spaces>>block_token>>$", block_quote_token
    #         )
    #         block_quote_token.add_bleading_spaces(prefix_to_add, is_first)
    #         POGGER.debug(
    #             "__xx_multiple_fix_leading_spaces>>block_token>>$", block_quote_token
    #         )
    #         is_first = False

    # pylint: disable=too-many-arguments
    @staticmethod
    def __add_line_for_table_continuation(
        parser_state: ParserState,
        position_marker: PositionMarker,
        was_started: bool,
        remaining_line_to_parse: str,
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
            new_token = TableBlockStackToken(position_marker)
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
