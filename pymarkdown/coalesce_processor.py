"""
Processing to coalesce a text tokens with a list of tokens.
"""
import logging

from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class CoalesceProcessor:
    """
    Handle the text coalesce processing of the token stream.
    """

    # LOW
    @staticmethod
    def coalesce_text_blocks(first_pass_results):
        """
        Take a pass and combine any two adjacent text blocks into one.
        """
        coalesced_list = []
        coalesced_list.extend(first_pass_results[0:1])
        for coalesce_index in range(1, len(first_pass_results)):
            did_process = False
            POGGER.debug(
                "coalesce_text_blocks>>>>$<<",
                first_pass_results[coalesce_index],
            )
            if coalesced_list[-1].is_text:
                POGGER.debug(">>coalesce_text_blocks>>>>$<<", coalesced_list[-1])
                if first_pass_results[coalesce_index].is_text or (
                    first_pass_results[coalesce_index].is_blank_line
                    and coalesced_list[-2].is_code_block
                ):

                    POGGER.debug("text-text>>$<<", coalesced_list[-2])
                    if coalesced_list[-2].is_indented_code_block:
                        remove_leading_spaces = len(
                            coalesced_list[-2].extracted_whitespace
                        )
                    elif (
                        coalesced_list[-2].is_paragraph
                        or coalesced_list[-2].is_setext_heading
                    ):
                        remove_leading_spaces = -1
                    else:
                        remove_leading_spaces = 0

                    POGGER.debug("remove_leading_spaces>>$", remove_leading_spaces)
                    POGGER.debug("combine1>>$", coalesced_list[-1])
                    POGGER.debug("combine2>>$", first_pass_results[coalesce_index])
                    indented_whitespace = coalesced_list[-1].combine(
                        first_pass_results[coalesce_index], remove_leading_spaces
                    )
                    POGGER.debug("combined>>$", coalesced_list[-1])
                    POGGER.debug("indented_whitespace>>$<<", indented_whitespace)
                    if coalesced_list[-2].is_indented_code_block:
                        coalesced_list[-2].add_indented_whitespace(indented_whitespace)
                    did_process = True
            elif (
                first_pass_results[coalesce_index].is_blank_line
                and coalesced_list[-1].is_code_block
            ):
                POGGER.debug("was>>$", first_pass_results[coalesce_index])
                replacement_token = TextMarkdownToken(
                    "",
                    first_pass_results[coalesce_index].extracted_whitespace,
                    line_number=first_pass_results[coalesce_index].line_number,
                    column_number=first_pass_results[coalesce_index].column_number,
                )
                POGGER.debug("now>>$", replacement_token)
                coalesced_list.append(replacement_token)
                did_process = True
            if not did_process:
                coalesced_list.append(first_pass_results[coalesce_index])

        for coalesce_index in range(1, len(coalesced_list)):
            if coalesced_list[coalesce_index].is_text and (
                coalesced_list[coalesce_index - 1].is_paragraph
                or coalesced_list[coalesce_index - 1].is_setext_heading
            ):
                POGGER.debug("full_paragraph_text>$<", coalesced_list[coalesce_index])
                POGGER.debug(
                    "full_paragraph_text>$<",
                    coalesced_list[coalesce_index].token_text,
                )
                removed_ws = coalesced_list[coalesce_index].remove_final_whitespace()
                POGGER.debug(
                    "full_paragraph_text>$<",
                    coalesced_list[coalesce_index].token_text,
                )
                POGGER.debug(
                    "full_paragraph_text>$>", coalesced_list[coalesce_index - 1]
                )
                coalesced_list[coalesce_index - 1].set_final_whitespace(removed_ws)
                POGGER.debug(
                    "full_paragraph_text>$>", coalesced_list[coalesce_index - 1]
                )

        return coalesced_list


# pylint: enable=too-few-public-methods
