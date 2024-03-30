"""
Module to provide for an encapsulation of the html block element.
"""

import logging
from typing import Optional

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)

POGGER = ParserLogger(logging.getLogger(__name__))


class HtmlBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the html block element.
    """

    def __init__(
        self, position_marker: PositionMarker, extracted_whitespace: str
    ) -> None:
        line_number = position_marker.line_number if position_marker else -1
        column_number = (
            position_marker.index_number
            + position_marker.index_indent
            + 1
            - len(extracted_whitespace)
            if position_marker
            else -1
        )
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_html_block,
            "",
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_html_block

    # pylint: enable=protected-access

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            HtmlBlockMarkdownToken,
            HtmlBlockMarkdownToken.__rehydrate_html_block,
            HtmlBlockMarkdownToken.__rehydrate_html_block_end,
        )

    @staticmethod
    def __rehydrate_html_block(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the html block from the token.
        """
        _ = (current_token, previous_token)

        context.block_stack.append(current_token)
        return ""

    @staticmethod
    def __rehydrate_html_block_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the html block from the token.
        """
        _ = (current_token, previous_token, next_token)

        del context.block_stack[-1]
        return ""

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            HtmlBlockMarkdownToken,
            HtmlBlockMarkdownToken.__handle_start_html_block_token,
            HtmlBlockMarkdownToken.__handle_end_html_block_token,
        )

    @staticmethod
    def __handle_start_html_block_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        transform_state.is_in_html_block = True
        token_parts = []
        if (
            not output_html
            and transform_state.transform_stack
            and transform_state.transform_stack[-1].endswith("<li>")
        ):
            token_parts.append(ParserHelper.newline_character)
        else:
            previous_token = transform_state.actual_tokens[
                transform_state.actual_token_index - 1
            ]
            POGGER.debug(">previous_token>$>", previous_token)
            token_parts.append(output_html)
            if (
                not previous_token.is_list_end
                and previous_token.is_paragraph_end
                and not transform_state.is_in_loose_list
                or previous_token.is_list_end
            ):
                token_parts.append(ParserHelper.newline_character)
        return "".join(token_parts)

    @staticmethod
    def __handle_end_html_block_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        transform_state.is_in_html_block = False
        return output_html
