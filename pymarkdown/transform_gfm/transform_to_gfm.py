"""
Module to provide for a transformation from markdown tokens to html for GFM.
"""
import logging
from typing import List

from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.transform_gfm.transform_to_gfm_token_handlers import (
    TransformToGfmTokenHandlers,
)
from pymarkdown.transform_state import TransformState

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
        assert transform_state.next_token is None
        assert not transform_state.is_in_fenced_code_block

        for next_token in transform_state.actual_tokens:
            output_html = self.__token_handlers.apply_transformation(
                transform_state,
                actual_tokens,
                actual_tokens_size,
                next_token,
                output_html,
            )

            POGGER.debug("======")
            POGGER.debug(
                "add_trailing_text-->$<--",
                transform_state.add_trailing_text,
            )
            POGGER.debug("add_leading_text -->$<--", transform_state.add_leading_text)
            POGGER.debug("output_html    -->$<--", output_html)

            if transform_state.add_trailing_text:
                output_html = self.__apply_trailing_text(output_html, transform_state)
                POGGER.debug("output_html    -->$<--", output_html)

            if transform_state.add_leading_text:
                output_html = self.__apply_leading_text(output_html, transform_state)
                POGGER.debug("output_html    -->$<--", output_html)

            POGGER.debug("------")
            POGGER.debug("next_token     -->$<--", next_token)
            POGGER.debug("output_html    -->$<--", output_html)
            POGGER.debug("transform_stack-->$<--", transform_state.transform_stack)

            transform_state.last_token = next_token
            transform_state.actual_token_index += 1
        if output_html and output_html[-1] == ParserHelper.newline_character:
            output_html = output_html[:-1]
        POGGER.debug("output_html    -->$<--", output_html)
        return output_html

    @classmethod
    def __apply_trailing_text(
        cls, output_html: str, transform_state: TransformState
    ) -> str:
        """
        Apply any trailing text to the output.
        """
        POGGER.debug("__apply_trailing_text>:$:<", output_html)
        stack_text = transform_state.transform_stack.pop()
        trailing_part = [stack_text]
        for next_token_to_test in TransformToGfm.add_trailing_text_tokens:
            if output_html.startswith(next_token_to_test):
                trailing_part.append(ParserHelper.newline_character)
                break

        POGGER.debug("trailing_part>:$:<", trailing_part)
        if trailing_part[-1].endswith("<li>") and output_html.startswith(
            "<blockquote>"
        ):
            trailing_part.append(ParserHelper.newline_character)
        trailing_part.append(output_html)
        POGGER.debug("trailing_part>:$:<", trailing_part)
        if output_html.endswith("</ul>") or output_html.endswith("</ol>"):
            trailing_part.append(ParserHelper.newline_character)
        assert transform_state.add_trailing_text is not None
        trailing_part.append(transform_state.add_trailing_text)
        combined_text = "".join(trailing_part)
        POGGER.debug("__apply_trailing_text>:$:<", combined_text)
        return combined_text

    @classmethod
    def __apply_leading_text(
        cls, output_html: str, transform_state: TransformState
    ) -> str:
        """
        Apply any leading text to the output.
        """

        output_html = (
            f"{output_html}{ParserHelper.newline_character}{transform_state.add_leading_text}"
            if output_html and output_html[-1] != ParserHelper.newline_character
            else f"{output_html}{transform_state.add_leading_text}"
        )
        transform_state.transform_stack.append(output_html)
        return ""


# pylint: enable=too-few-public-methods
