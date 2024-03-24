"""
Module to help with the parsing of inline elements at the end of the line.
"""

import logging
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.tab_helper import TabHelper
from pymarkdown.inline.inline_backslash_helper import InlineBackslashHelper
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.inline.inline_response import InlineResponse
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.hard_break_markdown_token import HardBreakMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class InlineLineEndHelper:
    """
    Class to help with the parsing of inline elements at the end of the line.
    """

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_line_end(
        remaining_line: str,
        tabified_remaining_line: Optional[str],
        end_string: Optional[str],
        current_string: str,
        inline_blocks: List[MarkdownToken],
        is_setext: bool,
        line_number: int,
        column_number: int,
        coalesced_stack: List[MarkdownToken],
        tabified_text: Optional[str],
        inline_request: InlineRequest,
    ) -> Tuple[
        str, Optional[str], List[MarkdownToken], str, Optional[str], str, Optional[str]
    ]:
        """
        Handle the inline case of having the end of line character encountered.
        """
        new_tokens: List[MarkdownToken] = []

        # POGGER.debug(">>current_string>>$>>", current_string)
        # POGGER.debug(">>end_string>>$>>", end_string)
        # POGGER.debug(">>remaining_line>>$>>", remaining_line)
        # POGGER.debug(">>tabified_remaining_line>>$>>", tabified_remaining_line)
        (
            removed_end_whitespace,
            remaining_line,
        ) = InlineLineEndHelper.__setup_for_select_line_ending(
            tabified_remaining_line, is_setext, remaining_line
        )
        # POGGER.debug(">>line_to_use>>$>>", line_to_use)
        # POGGER.debug(">>current_string>>$>>", current_string)

        (
            current_string,
            whitespace_to_add,
            append_to_current_string,
            end_string,
            remaining_line,
            tabified_remaining_line,
        ) = InlineLineEndHelper.__select_line_ending(
            new_tokens,
            line_number,
            column_number + len(remaining_line),
            current_string,
            removed_end_whitespace,
            end_string,
            remaining_line,
            inline_blocks,
            is_setext,
            tabified_text,
            inline_request,
            tabified_remaining_line,
        )

        InlineLineEndHelper.__handle_line_end_adjust_block_quote(coalesced_stack)

        return (
            append_to_current_string,
            whitespace_to_add,
            new_tokens,
            remaining_line,
            end_string,
            current_string,
            tabified_remaining_line,
        )

    # pylint: enable=too-many-arguments
    @staticmethod
    def __setup_for_select_line_ending(
        tabified_remaining_line: Optional[str], is_setext: bool, remaining_line: str
    ) -> Tuple[str, str]:
        line_to_use = (
            tabified_remaining_line
            if tabified_remaining_line and is_setext
            else remaining_line
        )
        _, last_non_whitespace_index = ParserHelper.collect_backwards_while_character(
            line_to_use, -1, " "
        )
        removed_end_whitespace = line_to_use[last_non_whitespace_index:]
        remaining_line = line_to_use[:last_non_whitespace_index]
        return removed_end_whitespace, remaining_line

    @staticmethod
    def __handle_line_end_adjust_block_quote(
        coalesced_stack: List[MarkdownToken],
    ) -> None:
        if coalesced_stack and coalesced_stack[-1].is_block_quote_start:
            block_quote_token = cast(BlockQuoteMarkdownToken, coalesced_stack[-1])
            block_quote_token.leading_text_index += 1

    @staticmethod
    def __is_proper_hard_break(
        current_string: str, removed_end_whitespace_size: int
    ) -> bool:
        POGGER.debug("__is_proper_hard_break>>current_string>>$>>", current_string)
        POGGER.debug("removed_end_whitespace_size>>$>>", removed_end_whitespace_size)

        current_string_size = len(current_string)
        if (
            removed_end_whitespace_size == 0
            and current_string_size
            and current_string[current_string_size - 1]
            == InlineBackslashHelper.backslash_character
        ):
            POGGER.debug(">>$<<", current_string)
            modified_current_string = current_string[:-1]
            is_proper_hard_break = modified_current_string[-2:] != "\\\b"
            POGGER.debug(">>$<<", is_proper_hard_break)
        else:
            is_proper_hard_break = False

        POGGER.debug("__is_proper_hard_break>>$>>", is_proper_hard_break)
        return is_proper_hard_break

    @staticmethod
    def __select_line_end_hard_break(
        new_tokens: List[MarkdownToken],
        line_number: int,
        adj_hard_column: int,
        current_string: str,
    ) -> Tuple[str, Optional[str], str]:
        POGGER.debug(">>proper hard break")
        new_tokens.append(
            HardBreakMarkdownToken(
                InlineBackslashHelper.backslash_character,
                line_number,
                adj_hard_column - 1,
            )
        )
        current_string, whitespace_to_add = current_string[:-1], None
        append_to_current_string = ""
        return current_string, whitespace_to_add, append_to_current_string

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def __select_line_ending(
        new_tokens: List[MarkdownToken],
        line_number: int,
        adj_hard_column: int,
        current_string: str,
        removed_end_whitespace: str,
        end_string: Optional[str],
        remaining_line: str,
        inline_blocks: List[MarkdownToken],
        is_setext: bool,
        tabified_text: Optional[str],
        inline_request: InlineRequest,
        tabified_remaining_line: Optional[str],
    ) -> Tuple[str, Optional[str], str, Optional[str], str, Optional[str]]:
        # POGGER.debug(">>removed_end_whitespace>:$:<", removed_end_whitespace)
        # POGGER.debug(">>tabified_text>:$:<", tabified_text)
        # POGGER.debug(
        #     ">>inline_request.tabified_text>:$:<", inline_request.tabified_text
        # )
        # POGGER.debug(
        #     ">>inline_request.tabified_remaining_line>:$:<",
        #     inline_request.tabified_remaining_line,
        # )
        append_to_current_string = ParserHelper.newline_character
        whitespace_to_add: Optional[str] = None

        removed_end_whitespace_size = len(removed_end_whitespace)
        # POGGER.debug(
        #     ">>len(r_e_w)>>$>>rem>>$>>",
        #     removed_end_whitespace_size,
        #     remaining_line,
        # )

        is_proper_end = not tabified_text or (
            tabified_remaining_line and tabified_remaining_line.endswith("  ")
        )

        if InlineLineEndHelper.__is_proper_hard_break(
            current_string, removed_end_whitespace_size
        ):
            current_string, whitespace_to_add, append_to_current_string = (
                InlineLineEndHelper.__select_line_end_hard_break(
                    new_tokens, line_number, adj_hard_column, current_string
                )
            )
        elif removed_end_whitespace_size >= 2 and is_proper_end:
            POGGER.debug(">>whitespace hard break")
            new_tokens.append(
                HardBreakMarkdownToken(
                    removed_end_whitespace, line_number, adj_hard_column
                )
            )
            whitespace_to_add = None
            append_to_current_string = ""

            if tabified_remaining_line is not None:
                number_collected_characters, start_index = (
                    ParserHelper.collect_backwards_while_character_verified(
                        tabified_remaining_line, len(tabified_remaining_line), " "
                    )
                )
                assert number_collected_characters >= 2
                tabified_remaining_line = tabified_remaining_line[:start_index]
        else:
            POGGER.debug(">>normal end")
            # POGGER.debug("current_string>:$:<", current_string)
            # POGGER.debug("removed_end_whitespace>:$:<", removed_end_whitespace)
            # POGGER.debug("end_string>:$:<", end_string)
            # POGGER.debug("remaining_line>:$:<", remaining_line)
            (
                end_string,
                remaining_line,
            ) = InlineLineEndHelper.__select_line_ending_normal(
                is_setext,
                inline_blocks,
                current_string,
                removed_end_whitespace,
                inline_request.tabified_remaining_line,
                end_string,
                remaining_line,
            )

        # POGGER.debug(
        #     "<<append_to_current_string<<$<<",
        #     append_to_current_string,
        # )
        # POGGER.debug(
        #     "<<whitespace_to_add<<$<<",
        #     whitespace_to_add,
        # )
        # POGGER.debug("<<remaining_line<<$<<", remaining_line)
        # POGGER.debug("<<end_string<<$<<", end_string)
        # POGGER.debug("<<current_string<<$<<", current_string)
        return (
            current_string,
            whitespace_to_add,
            append_to_current_string,
            end_string,
            remaining_line,
            tabified_remaining_line,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    # pylint: disable=too-many-arguments
    @staticmethod
    def __select_line_ending_normal(
        is_setext: bool,
        inline_blocks: List[MarkdownToken],
        current_string: str,
        removed_end_whitespace: str,
        tabified_remaining_line: Optional[str],
        end_string: Optional[str],
        remaining_line: str,
    ) -> Tuple[str, str]:
        # POGGER.debug("<<is_setext<<$<<", is_setext)
        # POGGER.debug("<<inline_blocks<<$<<", inline_blocks)
        # POGGER.debug("<<current_string<<$<<", current_string)
        POGGER.debug("<<remaining_line<<$<<", remaining_line)
        POGGER.debug("<<end_string<<$<<", end_string)
        POGGER.debug("<<removed_end_whitespace<<$<<", removed_end_whitespace)
        if (
            is_setext
            and inline_blocks
            and inline_blocks[-1].is_inline_hard_break
            and not current_string
        ):
            new_index, ex_ws = ParserHelper.extract_spaces(remaining_line, 0)
            # POGGER.debug("<<new_index<<$<<", new_index)
            # POGGER.debug("<<ex_ws<<$<<", ex_ws)
            end_string = (
                f"{ex_ws}{ParserHelper.whitespace_split_character}" if new_index else ""
            )
            remaining_line = remaining_line[new_index:]
        if not is_setext and tabified_remaining_line and removed_end_whitespace:
            POGGER.debug("<<tabified_remaining_line>:$:<", tabified_remaining_line)
            POGGER.debug("<<removed_end_whitespace>:$:<", removed_end_whitespace)
            adj_original, _ = TabHelper.find_detabify_string_ex(
                tabified_remaining_line, removed_end_whitespace
            )
            POGGER.debug("<<adj_original<<$<<", adj_original)
            assert adj_original is not None
            removed_end_whitespace = adj_original

        POGGER.debug("<<end_string<<$<<", end_string)
        end_string = (
            f"{removed_end_whitespace}{ParserHelper.newline_character}"
            if end_string is None
            else f"{end_string}{removed_end_whitespace}{ParserHelper.newline_character}"
        )
        POGGER.debug("<<end_string<<$<<", end_string)
        return end_string, remaining_line

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def process_inline_new_line(
        source_text: str,
        next_index: int,
        inline_response: InlineResponse,
        remaining_line: str,
        end_string: Optional[str],
        current_string: str,
        inline_blocks: List[MarkdownToken],
        is_setext: bool,
        line_number: int,
        column_number: int,
        coalesced_stack: List[MarkdownToken],
        whitespace_to_recombine: Optional[str],
        para_owner: Optional[ParagraphMarkdownToken],
        tabified_text: Optional[str],
        inline_request: InlineRequest,
        tabified_remaining_line: Optional[str],
    ) -> Tuple[Optional[str], str, Optional[str], str, bool, Optional[str]]:
        """
        Process a new line character.
        """
        assert source_text[next_index] == ParserHelper.newline_character
        # POGGER.debug("end_string>:$:<", end_string)
        # POGGER.debug("remaining_line>:$:<", remaining_line)
        # POGGER.debug("tabified_remaining_line>:$:<", tabified_remaining_line)
        # POGGER.debug("tabified_text>:$:<", tabified_text)
        # POGGER.debug(
        #     "inline_request.tabified_remaining_line>:$:<",
        #     inline_request.tabified_remaining_line,
        # )
        (
            inline_response.new_string,
            whitespace_to_add,
            inline_response.new_tokens,
            remaining_line,
            end_string,
            current_string,
            tabified_remaining_line,
        ) = InlineLineEndHelper.__handle_line_end(
            remaining_line,
            tabified_remaining_line,
            end_string,
            current_string,
            inline_blocks,
            is_setext,
            line_number,
            column_number,
            coalesced_stack,
            tabified_text,
            inline_request,
        )
        inline_response.new_index = next_index + 1
        # POGGER.debug("end_string>:$:<", end_string)
        # POGGER.debug("remaining_line>:$:<", remaining_line)
        # POGGER.debug(
        #     "handle_line_end>>new_tokens>>$<<",
        #     inline_response.new_tokens,
        # )

        if not inline_response.new_tokens:
            # POGGER.debug("ws")
            end_string = InlineLineEndHelper.__add_recombined_whitespace(
                bool(whitespace_to_recombine),
                source_text,
                inline_response,
                end_string,
                is_setext,
            )
            # POGGER.debug(
            #     "3<<end_string<<$<<",
            #     end_string,
            # )
            # POGGER.debug("ws>$<", end_string)
        # POGGER.debug(
        #     "handle_line_end>>$<<", source_text[inline_response.new_index :]
        # )
        # POGGER.debug(
        #     "end_string(after)>>$<<",
        #     end_string,
        # )
        # POGGER.debug(">>line_number>>$<<", line_number)
        # POGGER.debug(">>column_number>>$<<", column_number)
        if para_owner:
            # POGGER.debug(">>para_owner.rehydrate_index>>$<<", para_owner.rehydrate_index)
            para_owner.rehydrate_index += 1
            # POGGER.debug(">>para_owner.rehydrate_index>>$<<", para_owner.rehydrate_index)

        if tabified_remaining_line and end_string and len(end_string) > 1:
            assert end_string is not None
            tabified_remaining_line = InlineLineEndHelper.__clean_up_new_line(
                end_string, is_setext, tabified_remaining_line
            )

        return (
            whitespace_to_add,
            remaining_line,
            end_string,
            current_string,
            True,
            tabified_remaining_line,
        )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def __clean_up_new_line(
        end_string: str, is_setext: bool, tabified_remaining_line: str
    ) -> str:
        POGGER.debug("end_string>$<", end_string)
        POGGER.debug("tabified_remaining_line>$<", tabified_remaining_line)
        assert end_string[-1] in ["\n", ParserHelper.whitespace_split_character]
        if end_string[-1] == ParserHelper.whitespace_split_character:
            newline_index = end_string.rfind("\n")
            assert newline_index != -1
            end_suffix = end_string[:newline_index]
        else:
            end_suffix = end_string[:-1]
        POGGER.debug("end_suffix>$<", end_suffix)
        newline_index = end_suffix.rfind("\n")
        if is_setext:
            special_index = end_suffix.rfind(ParserHelper.whitespace_split_character)
            if special_index != -1 or newline_index != -1:
                max_index = max(special_index, newline_index)
                end_suffix = end_suffix[max_index + 1 :]
            else:
                assert special_index == -1
                assert newline_index != 1
                end_suffix = end_suffix[newline_index + 1 :]
        elif newline_index != -1:
            end_suffix = end_suffix[newline_index + 1 :]

        POGGER.debug("tabified_remaining_line>$<", tabified_remaining_line)
        POGGER.debug("end_suffix>$<", end_suffix)
        assert tabified_remaining_line.endswith(end_suffix)
        if end_suffix:
            tabified_remaining_line = tabified_remaining_line[: -(len(end_suffix))]
        POGGER.debug("tabified_remaining_line>$<", tabified_remaining_line)
        return tabified_remaining_line

    @staticmethod
    def __add_recombined_whitespace(
        did_recombine: bool,
        source_text: str,
        inline_response: InlineResponse,
        end_string: Optional[str],
        is_setext: bool,
    ) -> Optional[str]:
        POGGER.debug("__arw>>did_recombine>>$>>", did_recombine)
        POGGER.debug(
            "__arw>>end_string>>$>>",
            end_string,
        )
        if did_recombine:
            POGGER.debug(
                "__arw>>source_text>>$>>",
                source_text,
            )
            assert inline_response.new_index is not None
            new_index, extracted_whitespace = ParserHelper.extract_spaces(
                source_text, inline_response.new_index
            )
            POGGER.debug("__arw>>$>>", source_text[: inline_response.new_index])
            POGGER.debug("__arw>>$>>", source_text[inline_response.new_index :])
            POGGER.debug(
                "__arw>>extracted_whitespace>>$>>",
                extracted_whitespace,
            )
            if extracted_whitespace:
                inline_response.new_index = new_index
                assert end_string is not None
                assert is_setext
                end_string = f"{end_string}{extracted_whitespace}{ParserHelper.whitespace_split_character}"
                POGGER.debug(
                    "__arw>>end_string>>$>>",
                    end_string,
                )
        return end_string


# pylint: enable=too-few-public-methods
