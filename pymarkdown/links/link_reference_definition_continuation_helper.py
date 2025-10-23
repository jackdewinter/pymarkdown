"""
Module to helper with determining whether to continue with the link reference definitions.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.links.link_parse_helper import LinkParseHelper
from pymarkdown.links.link_reference_definition_parse_helper import (
    LinkReferenceDefinitionParseHelper,
)
from pymarkdown.links.link_reference_tuple import LinkReferenceDefinitionTuple
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.link_reference_definition_markdown_token import (
    LinkReferenceDefinitionMarkdownToken,
)
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import LinkDefinitionStackToken

POGGER = ParserLogger(logging.getLogger(__name__))

# pylint: disable=too-few-public-methods


class LinkReferenceDefinitionContinuationHelper:
    """
    Class to helper with determining whether to continue with the link reference definitions.
    """

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
        end_lrd_index: int,
        line_to_parse_size: int,
        is_blank_line: bool,
        did_complete_lrd: bool,
        parsed_lrd_tuple: Optional[LinkReferenceDefinitionTuple],
        lines_to_requeue: List[str],
    ) -> Tuple[bool, bool, List[MarkdownToken]]:
        """
        Determine whether to continue with the processing of the LRD.
        """
        if did_pause_lrd := (
            end_lrd_index >= 0
            and end_lrd_index == line_to_parse_size
            and not is_blank_line
        ):
            POGGER.debug(">>parse_link_reference_definition>>continuation")
            LinkReferenceDefinitionContinuationHelper.__add_line_for_lrd_continuation(
                parser_state,
                position_marker,
                was_started,
                remaining_line_to_parse,
                extracted_whitespace,
                unmodified_line_to_parse,
                original_stack_depth,
                original_document_depth,
            )
        if not did_pause_lrd and was_started or did_complete_lrd:
            return LinkReferenceDefinitionContinuationHelper.__stop_lrd_continuation(
                parser_state,
                did_complete_lrd,
                parsed_lrd_tuple,
                lines_to_requeue,
                did_pause_lrd,
            )

        POGGER.debug(">>parse_link_reference_definition>>other")
        return did_pause_lrd, False, []

    # pylint: enable=too-many-arguments

    @staticmethod
    def __stop_lrd_continuation(
        parser_state: ParserState,
        did_complete_lrd: bool,
        parsed_lrd_tuple: Optional[LinkReferenceDefinitionTuple],
        lines_to_requeue: List[str],
        did_pause_lrd: bool,
    ) -> Tuple[bool, bool, List[MarkdownToken]]:
        """
        As part of processing a link reference definition, stop a continuation.
        """
        POGGER.debug(">>parse_link_reference_definition>>no longer need start")
        if did_complete_lrd:
            assert parsed_lrd_tuple, "LRd tuple must be defined by now."
            assert (
                parsed_lrd_tuple.normalized_destination is not None
            ), "normalized_destination must be defined by now."
            did_add_definition = LinkParseHelper.add_link_definition(
                parsed_lrd_tuple.normalized_destination, parsed_lrd_tuple.link_titles
            )
            link_def_token = cast(
                LinkDefinitionStackToken, parser_state.token_stack[-1]
            )
            assert (
                link_def_token.extracted_whitespace is not None
            ), "extracted_whitespace must be defined by now."
            extracted_whitespace = link_def_token.extracted_whitespace

            POGGER.debug(
                "link_def_token.extracted_whitespace>:$:<",
                link_def_token.extracted_whitespace,
            )
            POGGER.debug(
                "link_def_token.continuation_lines>:$:<",
                link_def_token.continuation_lines,
            )
            POGGER.debug(
                "link_def_token.unmodified_lines>:$:<", link_def_token.unmodified_lines
            )
            POGGER.debug("lines_to_requeue>:$:<", lines_to_requeue)

            does_any_line_have_tabs = any(
                ParserHelper.tab_character in ffg
                for ffg in link_def_token.unmodified_lines
            )
            POGGER.debug("does_any_line_have_tabs>:$:<", does_any_line_have_tabs)

            last_container_index = parser_state.find_last_container_on_stack()
            if does_any_line_have_tabs and last_container_index > 0:
                (
                    extracted_whitespace,
                    parsed_lrd_tuple,
                ) = LinkReferenceDefinitionContinuationHelper.__stop_lrd_continuation_with_tab(
                    parser_state,
                    link_def_token,
                    parsed_lrd_tuple,
                )

            new_tokens: List[MarkdownToken] = (
                LinkReferenceDefinitionContinuationHelper.__create_new_tokens(
                    link_def_token,
                    parsed_lrd_tuple,
                    extracted_whitespace,
                    did_add_definition,
                )
            )
            del parser_state.token_stack[-1]
            return did_pause_lrd, len(lines_to_requeue) > 1, new_tokens

        del parser_state.token_stack[-1]
        return did_pause_lrd, True, []

    @staticmethod
    def __create_new_tokens(
        link_def_token: LinkDefinitionStackToken,
        parsed_lrd_tuple: LinkReferenceDefinitionTuple,
        extracted_whitespace: str,
        did_add_definition: bool,
    ) -> List[MarkdownToken]:
        assert (
            parsed_lrd_tuple.normalized_destination is not None
        ), "normalized_destination must be defined by now."
        new_tokens: List[MarkdownToken] = [
            LinkReferenceDefinitionMarkdownToken(
                did_add_definition,
                extracted_whitespace,
                parsed_lrd_tuple.normalized_destination,
                parsed_lrd_tuple.link_titles,
                parsed_lrd_tuple.link_info,
                position_marker=link_def_token.start_position_marker,
            )
        ]
        POGGER.debug(">>link_info>>$", parsed_lrd_tuple.link_info)
        POGGER.debug(">>new_tokens>>$", new_tokens)
        return new_tokens

    @staticmethod
    def __stop_lrd_continuation_with_tab(
        parser_state: ParserState,
        link_def_token: LinkDefinitionStackToken,
        parsed_lrd_tuple: LinkReferenceDefinitionTuple,
    ) -> Tuple[str, LinkReferenceDefinitionTuple]:
        POGGER.debug(
            "extracted_whitespace>:$:<",
            link_def_token.extracted_whitespace,
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
            "link_def_token.continuation_lines>:$:<", link_def_token.continuation_lines
        )
        POGGER.debug(
            "link_def_token.unmodified_lines>:$:<", link_def_token.unmodified_lines
        )

        if last_block_quote_index > last_list_index:
            assert block_quote_token is not None
            assert block_quote_token.bleading_spaces is not None
            split_container_spaces = block_quote_token.bleading_spaces.split("\n")
        else:
            assert list_token is not None
            assert list_token.leading_spaces is not None
            split_container_spaces = list_token.leading_spaces.split("\n")

        if len(link_def_token.continuation_lines) == 1:
            extracted_whitespace = LinkReferenceDefinitionContinuationHelper.__stop_lrd_continuation_with_tab_single(
                parser_state,
                link_def_token,
                last_block_quote_index,
                last_list_index,
                split_container_spaces,
            )
        else:
            (
                extracted_whitespace,
                parsed_lrd_tuple,
            ) = LinkReferenceDefinitionContinuationHelper.__stop_lrd_continuation_with_tab_multiple(
                parser_state,
                link_def_token,
                block_quote_token,
                last_block_quote_index,
                list_token,
                last_list_index,
                split_container_spaces,
            )

        return extracted_whitespace, parsed_lrd_tuple

    @staticmethod
    def __stop_lrd_continuation_with_tab_single(
        parser_state: ParserState,
        link_def_token: LinkDefinitionStackToken,
        last_block_quote_index: int,
        last_list_index: int,
        split_container_spaces: List[str],
    ) -> str:
        parsed_line = link_def_token.continuation_lines[0]
        original_line = link_def_token.unmodified_lines[0]

        current_line_container_spaces = (
            split_container_spaces[-2]
            if len(split_container_spaces) >= 2
            else split_container_spaces[-1]
        )
        (
            extracted_whitespace,
            split_tab,
            _,
        ) = LinkReferenceDefinitionContinuationHelper.__find_line_ws(
            parsed_line, original_line, current_line_container_spaces
        )

        if split_tab:
            if last_block_quote_index > last_list_index:
                TabHelper.adjust_block_quote_indent_for_tab(parser_state)
            else:
                TabHelper.adjust_block_quote_indent_for_tab(
                    parser_state, extracted_whitespace=extracted_whitespace
                )
        # POGGER.debug(
        #     "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        # )
        return extracted_whitespace

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __stop_lrd_continuation_with_tab_multiple(
        parser_state: ParserState,
        link_def_token: LinkDefinitionStackToken,
        block_quote_token: Optional[BlockQuoteMarkdownToken],
        last_block_quote_index: int,
        list_token: Optional[ListStartMarkdownToken],
        last_list_index: int,
        split_container_spaces: List[str],
    ) -> Tuple[str, LinkReferenceDefinitionTuple]:
        split_tabs_list: List[bool] = []
        completed_lrd_text: str = ""
        extracted_whitespace = ""
        alt_ws: Optional[str] = None
        for this_line_index, this_line in enumerate(link_def_token.continuation_lines):
            (
                completed_lrd_text,
                extracted_whitespace,
                alt_ws,
            ) = LinkReferenceDefinitionContinuationHelper.__stop_lrd_continuation_with_tab_multiple_loop(
                link_def_token,
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
            new_parsed_lrd_tuple,
        ) = LinkReferenceDefinitionParseHelper.parse_link_reference_definition(
            parser_state, completed_lrd_text, 0, "", True, "", True
        )
        assert (
            did_succeed
        ), "Since this is the stop and there is at least one valid match, this must be true."
        assert (
            len(completed_lrd_text) == next_index
        ), "Index must be at the end of the stirng."
        assert new_parsed_lrd_tuple is not None, "New tuple must be defined."

        if last_block_quote_index > last_list_index:
            assert block_quote_token is not None
            LinkReferenceDefinitionContinuationHelper.__xx_multiple_fix_bleading_spaces(
                block_quote_token, split_tabs_list, link_def_token
            )
        else:
            assert list_token is not None
            LinkReferenceDefinitionContinuationHelper.__xx_multiple_fix_leading_spaces(
                list_token, split_tabs_list, link_def_token
            )
        return extracted_whitespace, new_parsed_lrd_tuple

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __stop_lrd_continuation_with_tab_multiple_loop(
        link_def_token: LinkDefinitionStackToken,
        this_line_index: int,
        this_line: str,
        completed_lrd_text: str,
        extracted_whitespace: str,
        alt_ws: Optional[str],
        split_tabs_list: List[bool],
        split_container_spaces: List[str],
    ) -> Tuple[str, str, Optional[str]]:
        original_this_line = link_def_token.unmodified_lines[this_line_index]
        POGGER.debug("this_line_index>:$:<", this_line_index)
        POGGER.debug("this_line>:$:<", this_line)
        POGGER.debug("original_this_line>:$:<", original_this_line)

        spaces_index = (
            len(split_container_spaces)
            - len(link_def_token.unmodified_lines)
            + this_line_index
        )
        (
            extracted_ws,
            split_tab,
            start_whitespace_index,
        ) = LinkReferenceDefinitionContinuationHelper.__find_line_ws(
            this_line, original_this_line, split_container_spaces[spaces_index]
        )

        if completed_lrd_text:
            completed_lrd_text += "\n"
        if this_line_index == 0:
            extracted_whitespace = extracted_ws
            alt_ws = TabHelper.detabify_string(
                extracted_whitespace, start_whitespace_index
            )
        else:
            completed_lrd_text += extracted_ws
        completed_lrd_text += this_line
        split_tabs_list.append(split_tab)
        return completed_lrd_text, extracted_whitespace, alt_ws

    # pylint: enable=too-many-arguments

    @staticmethod
    def __find_line_ws(
        parsed_lines: str, original_lines: str, wsx: str
    ) -> Tuple[str, bool, int]:
        start_text_index = original_lines.find(parsed_lines)
        assert start_text_index != -1, "Index must be found within string."
        # POGGER.debug("start_text_index>:$:<", start_text_index)
        start_whitespace_index = 0
        # POGGER.debug("start_whitespace_index>:$:<", start_whitespace_index)
        tabified_whitespace = original_lines[start_whitespace_index:start_text_index]
        # POGGER.debug("tabified_whitespace>:$:<", tabified_whitespace)

        split_tab = "\t" in tabified_whitespace
        if split_tab:
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
        link_def_token: LinkDefinitionStackToken,
    ) -> None:
        POGGER.debug("split_tabs_list>:$:<", split_tabs_list)
        POGGER.debug(
            "block_quote_token.leading_spaces>:$:<", block_quote_token.bleading_spaces
        )
        assert (
            block_quote_token.bleading_spaces is not None
        ), "Bleading spaces must be defined by now."
        leading_spaces: List[str] = []
        for _ in link_def_token.continuation_lines:
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
                "__xx_multiple_fix_bleading_spaces>>block_token>>$", block_quote_token
            )
            block_quote_token.add_bleading_spaces(prefix_to_add, is_first)
            POGGER.debug(
                "__xx_multiple_fix_bleading_spaces>>block_token>>$", block_quote_token
            )
            is_first = False

    @staticmethod
    def __xx_multiple_fix_leading_spaces(
        list_token: ListStartMarkdownToken,
        split_tabs_list: List[bool],
        link_def_token: LinkDefinitionStackToken,
    ) -> None:
        POGGER.debug("split_tabs_list>:$:<", split_tabs_list)
        POGGER.debug("list_token.leading_spaces>:$:<", list_token.leading_spaces)
        assert (
            list_token.leading_spaces is not None
        ), "leading spaces must be defined by now."
        leading_spaces: List[str] = []
        for _ in link_def_token.continuation_lines:
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
                current_unmodified_line = link_def_token.unmodified_lines[
                    current_leading_space_index
                ]
                continuation_start_index = current_unmodified_line.find(
                    link_def_token.continuation_lines[current_leading_space_index]
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
    def __add_line_for_lrd_continuation(
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
        As part of processing a link reference definition, add a line to the continuation.
        """

        line_to_store = remaining_line_to_parse
        if not was_started:
            POGGER.debug(">>parse_link_reference_definition>>marking start")
            new_token = LinkDefinitionStackToken(extracted_whitespace, position_marker)
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
            new_token.copy_of_token_stack = parser_state.copy_of_token_stack

            new_token.x1_token = parser_state.x1_token
            new_token.copy_of_x1_token = parser_state.copy_of_x1_token
            new_token.x1_token_index = parser_state.x1_token_index
        else:
            new_token = cast(LinkDefinitionStackToken, parser_state.token_stack[-1])

        POGGER.debug(">>line_to_store>>add>:$<<", line_to_store)
        POGGER.debug(">>unmodified_line_to_parse>>add>:$<<", unmodified_line_to_parse)
        assert unmodified_line_to_parse.endswith(
            line_to_store
        ), "Unmodified line must end with the processed line."
        new_token.add_continuation_line(line_to_store)
        new_token.add_unmodified_line(unmodified_line_to_parse)

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
