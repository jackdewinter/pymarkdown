"""
Module to provide for a transformation from markdown tokens to html for GFM.
"""

import logging
from typing import List

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.html_items import FormatOnlyNewLineHtmlItem, HtmlItems
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_gfm.transform_to_gfm_token_handlers import (
    TransformToGfmTokenHandlers,
)

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class TransformToGfm:
    """
    Class to provide for a transformation from markdown tokens to html for GFM.
    """

    add_trailing_text_tokens = [
        "<hr />",
        "<p>",
        "<h1>",
        "<h2>",
        "<h3>",
        "<h4>",
        "<h5>",
        "<h6>",
        "<pre>",
        "<ul>",
        "<ol>",
        '<ol start="',
    ]

    def __init__(self) -> None:
        """
        Initialize an instance of the TransformToGfm class.
        """
        self.__token_handlers = TransformToGfmTokenHandlers()

    def transform(self, actual_tokens: List[MarkdownToken]) -> str:
        """
        Transform the tokens into html.
        """
        POGGER.debug("\n\n---\n")
        transform_state, output_html, actual_tokens_size = (
            TransformState(actual_tokens),
            "",
            len(actual_tokens),
        )

        # This is the easiest way to finish covering the missing items.
        assert (
            transform_state.next_token is None
            and not transform_state.is_in_fenced_code_block
        ), "Initial state must be set properly."

        output_parts: List[HtmlItems] = []

        for next_token in transform_state.actual_tokens:
            output_html = self.__token_handlers.apply_transformation(
                transform_state,
                actual_tokens,
                actual_tokens_size,
                next_token,
                output_html,
                output_parts,
            )

            POGGER.debug("======")
            POGGER.debug(
                "add_trailing_text-->$<--",
                transform_state.add_trailing_text,
            )
            POGGER.debug("add_leading_text -->$<--", transform_state.add_leading_text)
            POGGER.debug("output_html    -->$<--", output_html)

            if transform_state.add_trailing_text:
                output_html = self.__apply_trailing_text(
                    output_html, transform_state, output_parts
                )
                POGGER.debug("output_html    -->$<--", output_html)

            if transform_state.add_leading_text:
                output_html = self.__apply_leading_text(
                    output_html, transform_state, output_parts
                )
                POGGER.debug("output_html    -->$<--", output_html)

            POGGER.debug("------")
            POGGER.debug("next_token     -->$<--", next_token)
            POGGER.debug("output_html    -->$<--", output_html)
            POGGER.debug("transform_stack-->$<--", transform_state.transform_stack)
            POGGER.debug(
                "transform_stack_two-->$<--", transform_state.transform_stack_two
            )

            transform_state.last_token = next_token
            transform_state.actual_token_index += 1
        if output_html and output_html[-1] == ParserHelper.newline_character:
            output_html = output_html[:-1]
        POGGER.debug("output_html    -->$<--", output_html)

        combined_output_parts = "".join([x.get_raw_html_text() for x in output_parts])
        if (
            combined_output_parts
            and combined_output_parts[-1] == ParserHelper.newline_character
        ):
            combined_output_parts = combined_output_parts[:-1]

        assert output_html == combined_output_parts

        return output_html

    @classmethod
    def __apply_trailing_text(
        cls, output_html: str, transform_state: TransformState, abc: List[HtmlItems]
    ) -> str:
        """
        Apply any trailing text to the output.
        """
        POGGER.debug("__apply_trailing_text>:$:<", output_html)

        g = "".join(i.get_raw_html_text() for i in transform_state.add_trailing_parts)
        assert g == transform_state.add_trailing_text

        trailing_part = [transform_state.transform_stack.pop()]
        stack_elements = transform_state.transform_stack_two.pop()

        for next_token_to_test in TransformToGfm.add_trailing_text_tokens:
            if output_html.startswith(next_token_to_test):
                trailing_part.append(ParserHelper.newline_character)
                stack_elements.append(FormatOnlyNewLineHtmlItem())
                break

        POGGER.debug("trailing_part>:$:<", trailing_part)
        if trailing_part[-1].endswith("<li>") and output_html.startswith(
            "<blockquote>"
        ):
            trailing_part.append(ParserHelper.newline_character)
            stack_elements.append(FormatOnlyNewLineHtmlItem())

        trailing_part.append(output_html)
        stack_elements.extend(abc)

        POGGER.debug("trailing_part>:$:<", trailing_part)
        if output_html.endswith("</ul>") or output_html.endswith("</ol>"):
            trailing_part.append(ParserHelper.newline_character)
            stack_elements.append(FormatOnlyNewLineHtmlItem())
        trailing_part.append(transform_state.add_trailing_text)
        stack_elements.extend(transform_state.add_trailing_parts)

        combined_text = "".join(trailing_part)
        POGGER.debug("__apply_trailing_text>:$:<", combined_text)
        abc.clear()
        abc.extend(stack_elements)
        return combined_text

    @classmethod
    def __apply_leading_text(
        cls, output_html: str, transform_state: TransformState, abc: List[HtmlItems]
    ) -> str:
        """
        Apply any leading text to the output.
        """

        g = "".join(i.get_raw_html_text() for i in transform_state.add_leading_parts)
        assert g == transform_state.add_leading_text

        if output_html and output_html[-1] != ParserHelper.newline_character:
            abc.append(FormatOnlyNewLineHtmlItem())
            output_html = f"{output_html}{ParserHelper.newline_character}{transform_state.add_leading_text}"
        else:
            output_html = f"{output_html}{transform_state.add_leading_text}"

        abc.extend(transform_state.add_leading_parts)
        transform_state.transform_stack.append(output_html)
        transform_state.transform_stack_two.append(abc[:])

        abc.clear()
        return ""


# pylint: enable=too-few-public-methods
