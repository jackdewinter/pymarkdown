"""
Processing to coalesce a text tokens with a list of tokens.
"""
import logging
from typing import List, cast

from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_markdown_token import (
    IndentedCodeBlockMarkdownToken,
    ParagraphMarkdownToken,
)
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class CoalesceProcessor:
    """
    Handle the text coalesce processing of the token stream.
    """

    @staticmethod
    def coalesce_text_blocks(
        first_pass_results: List[MarkdownToken],
    ) -> List[MarkdownToken]:
        """
        Take a pass and combine any two adjacent text blocks into one.
        """
        coalesced_list = [first_pass_results[0]]
        # POGGER.debug("coalesced_list:$:", coalesced_list)
        for coalesce_index in range(1, len(first_pass_results)):
            POGGER.debug(
                "coalesce_text_blocks>>>>$<<",
                first_pass_results[coalesce_index],
            )
            if coalesced_list[-1].is_text:
                # POGGER.debug("__coalesce_with_previous")
                did_process = CoalesceProcessor.__coalesce_with_previous(
                    first_pass_results, coalesced_list, coalesce_index
                )
            else:
                did_process = (
                    first_pass_results[coalesce_index].is_blank_line
                    and coalesced_list[-1].is_code_block
                )
                if did_process:
                    # POGGER.debug("__coalesce_with_blank_line")
                    CoalesceProcessor.__coalesce_with_blank_line(
                        first_pass_results, coalesced_list, coalesce_index
                    )
            if not did_process:
                coalesced_list.append(first_pass_results[coalesce_index])
                # POGGER.debug("coalesced_list:$:", coalesced_list)

        # POGGER.debug("--Final--coalesced_list:$:", coalesced_list)
        CoalesceProcessor.__calculate_final_whitespaces(coalesced_list)
        # POGGER.debug("coalesced_list:$:", coalesced_list)

        return coalesced_list

    @staticmethod
    def __calculate_final_whitespaces(coalesced_list: List[MarkdownToken]) -> None:
        for coalesce_index in range(1, len(coalesced_list)):
            if coalesced_list[coalesce_index].is_text and (
                coalesced_list[coalesce_index - 1].is_paragraph
                or coalesced_list[coalesce_index - 1].is_setext_heading
            ):
                text_token = cast(TextMarkdownToken, coalesced_list[coalesce_index])
                POGGER.debug("full_paragraph_text>$<", text_token)
                POGGER.debug(
                    "full_paragraph_text>$<",
                    text_token.token_text,
                )
                # POGGER.debug("text_token.tabified_text=:$:", text_token.tabified_text)
                # POGGER.debug("text_token.token_text=:$:", text_token.token_text)
                removed_ws = text_token.remove_final_whitespace()
                POGGER.debug(
                    "full_paragraph_text>$<",
                    text_token.token_text,
                )

                paragraph_or_setext_token = cast(
                    ParagraphMarkdownToken, coalesced_list[coalesce_index - 1]
                )
                POGGER.debug("full_paragraph_text>$>", paragraph_or_setext_token)
                paragraph_or_setext_token.set_final_whitespace(removed_ws)
                POGGER.debug("full_paragraph_text>$>", paragraph_or_setext_token)

    @staticmethod
    def __coalesce_with_previous(
        first_pass_results: List[MarkdownToken],
        coalesced_list: List[MarkdownToken],
        coalesce_index: int,
    ) -> bool:

        POGGER.debug(">>coalesce_text_blocks>>>>$<<", coalesced_list[-1])
        if first_pass_results[coalesce_index].is_text or (
            first_pass_results[coalesce_index].is_blank_line
            and coalesced_list[-2].is_code_block
        ):

            POGGER.debug("text-text>>$<<", coalesced_list[-2])
            if coalesced_list[-2].is_indented_code_block:
                indented_token = cast(
                    IndentedCodeBlockMarkdownToken, coalesced_list[-2]
                )
                remove_leading_spaces = len(indented_token.extracted_whitespace)
            elif (
                coalesced_list[-2].is_paragraph or coalesced_list[-2].is_setext_heading
            ):
                remove_leading_spaces = -1
            else:
                remove_leading_spaces = 0

            text_token = cast(TextMarkdownToken, coalesced_list[-1])
            POGGER.debug("remove_leading_spaces>>$", remove_leading_spaces)
            POGGER.debug("combine1>>$", text_token)
            POGGER.debug("combine2>>$", first_pass_results[coalesce_index])
            indented_whitespace = text_token.combine(
                first_pass_results[coalesce_index], remove_leading_spaces
            )
            POGGER.debug("combined>>$", text_token)
            POGGER.debug("indented_whitespace>>$<<", indented_whitespace)
            if coalesced_list[-2].is_indented_code_block:
                indented_token = cast(
                    IndentedCodeBlockMarkdownToken, coalesced_list[-2]
                )
                indented_token.add_indented_whitespace(indented_whitespace)
            return True
        return False

    @staticmethod
    def __coalesce_with_blank_line(
        first_pass_results: List[MarkdownToken],
        coalesced_list: List[MarkdownToken],
        coalesce_index: int,
    ) -> None:

        POGGER.debug("was>>$", first_pass_results[coalesce_index])
        text_token = cast(TextMarkdownToken, first_pass_results[coalesce_index])
        replacement_token = TextMarkdownToken(
            "",
            text_token.extracted_whitespace,
            line_number=text_token.line_number,
            column_number=text_token.column_number,
        )
        POGGER.debug("now>>$", replacement_token)
        coalesced_list.append(replacement_token)


# pylint: enable=too-few-public-methods
