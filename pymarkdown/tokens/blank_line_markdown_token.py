"""
Module to provide for an encapsulation of the blank line element.
"""

from typing import Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


class BlankLineMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the blank line element.
    """

    def __init__(
        self,
        extracted_whitespace: str,
        position_marker: Optional[PositionMarker],
        column_delta: int = 0,
    ) -> None:
        line_number = position_marker.line_number if position_marker else 0
        column_number = (
            position_marker.index_number
            + position_marker.index_indent
            + 1
            - column_delta
            if position_marker
            else 0
        )
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_blank_line,
            extracted_whitespace,
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_blank_line

    # pylint: enable=protected-access

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            BlankLineMarkdownToken, BlankLineMarkdownToken.__rehydrate_blank_line, None
        )

    @staticmethod
    def __rehydrate_blank_line(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the blank line from the token.
        """
        # if (
        #     self.context.block_stack
        #     and self.context.block_stack[-1].is_fenced_code_block
        #     and (previous_token and previous_token.is_text)
        # ):
        #     extra_newline_after_text_token = ParserHelper.newline_character
        # else:
        _ = previous_token, context
        extra_newline_after_text_token = ""

        current_blank_token = cast(BlankLineMarkdownToken, current_token)
        return f"{extra_newline_after_text_token}{current_blank_token.extracted_whitespace}{ParserHelper.newline_character}"

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            BlankLineMarkdownToken,
            BlankLineMarkdownToken.__handle_blank_line_token,
            None,
        )

    @staticmethod
    def __handle_blank_line_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        if transform_state.is_in_html_block:
            output_html = f"{output_html}{ParserHelper.newline_character}"
        return output_html
