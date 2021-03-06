"""
Processing to coalesce a text tokens with a list of tokens.
"""
import logging

from pymarkdown.parser_helper import ParserHelper

LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class CoalesceProcessor:
    """
    Handle the text coalesce processing of the token stream.
    """

    @staticmethod
    def coalesce_text_blocks(first_pass_results):
        """
        Take a pass and combine any two adjacent text blocks into one.
        """
        coalesced_list = []
        coalesced_list.extend(first_pass_results[0:1])
        for coalesce_index in range(1, len(first_pass_results)):
            did_process = False
            LOGGER.debug(
                "coalesce_text_blocks>>>>%s<<",
                ParserHelper.make_value_visible(first_pass_results[coalesce_index]),
            )
            if coalesced_list[-1].is_text:
                LOGGER.debug(
                    ">>coalesce_text_blocks>>>>%s<<",
                    ParserHelper.make_value_visible(coalesced_list[-1]),
                )
                if first_pass_results[coalesce_index].is_text or (
                    first_pass_results[coalesce_index].is_blank_line
                    and coalesced_list[-2].is_code_block
                ):

                    LOGGER.debug("text-text>>%s<<", str(coalesced_list[-2]))
                    remove_leading_spaces = 0
                    if coalesced_list[-2].is_indented_code_block:
                        remove_leading_spaces = len(
                            coalesced_list[-2].extracted_whitespace
                        )
                    elif (
                        coalesced_list[-2].is_paragraph
                        or coalesced_list[-2].is_setext_heading
                    ):
                        remove_leading_spaces = -1

                    LOGGER.debug(
                        "remove_leading_spaces>>%s", str(remove_leading_spaces)
                    )
                    LOGGER.debug(
                        "combine1>>%s",
                        ParserHelper.make_value_visible(coalesced_list[-1]),
                    )
                    LOGGER.debug(
                        "combine2>>%s",
                        ParserHelper.make_value_visible(
                            first_pass_results[coalesce_index]
                        ),
                    )
                    indented_whitespace = coalesced_list[-1].combine(
                        first_pass_results[coalesce_index], remove_leading_spaces
                    )
                    LOGGER.debug(
                        "combined>>%s",
                        ParserHelper.make_value_visible(coalesced_list[-1]),
                    )
                    LOGGER.debug(
                        "indented_whitespace>>%s<<",
                        ParserHelper.make_value_visible(indented_whitespace),
                    )
                    if coalesced_list[-2].is_indented_code_block:
                        coalesced_list[-2].add_indented_whitespace(indented_whitespace)
                    did_process = True
            if not did_process:
                coalesced_list.append(first_pass_results[coalesce_index])

        for coalesce_index in range(1, len(coalesced_list)):
            if coalesced_list[coalesce_index].is_text and (
                coalesced_list[coalesce_index - 1].is_paragraph
                or coalesced_list[coalesce_index - 1].is_setext_heading
            ):
                LOGGER.debug(
                    "full_paragraph_text>%s<",
                    ParserHelper.make_value_visible(coalesced_list[coalesce_index]),
                )
                LOGGER.debug(
                    "full_paragraph_text>%s>%s<",
                    str(len(coalesced_list[coalesce_index].token_text)),
                    ParserHelper.make_value_visible(
                        coalesced_list[coalesce_index].token_text
                    ),
                )
                removed_ws = coalesced_list[coalesce_index].remove_final_whitespace()
                LOGGER.debug(
                    "full_paragraph_text>%s>%s<",
                    str(len(coalesced_list[coalesce_index].token_text)),
                    ParserHelper.make_value_visible(
                        coalesced_list[coalesce_index].token_text
                    ),
                )
                LOGGER.debug(
                    "full_paragraph_text>%s>", str(coalesced_list[coalesce_index - 1])
                )
                coalesced_list[coalesce_index - 1].set_final_whitespace(removed_ws)
                LOGGER.debug(
                    "full_paragraph_text>%s>", str(coalesced_list[coalesce_index - 1])
                )

        return coalesced_list


# pylint: enable=too-few-public-methods
