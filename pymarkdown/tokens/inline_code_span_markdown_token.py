"""
Module to provide for an encapsulation of the inline code span element.
"""

from typing import Callable, Optional, cast

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)


class InlineCodeSpanMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline code span element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        span_text: str,
        extracted_start_backticks: str,
        leading_whitespace: str,
        trailing_whitespace: str,
        line_number: int,
        column_number: int,
    ) -> None:
        (
            self.__span_text,
            self.__extracted_start_backticks,
            self.__leading_whitespace,
            self.__trailing_whitespace,
        ) = (
            span_text,
            extracted_start_backticks,
            leading_whitespace,
            trailing_whitespace,
        )
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_code_span,
            MarkdownToken.extra_data_separator.join(
                [
                    self.__span_text,
                    self.__extracted_start_backticks,
                    self.__leading_whitespace,
                    self.__trailing_whitespace,
                ]
            ),
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_code_span

    # pylint: enable=protected-access

    # pylint: enable=too-many-arguments
    @property
    def span_text(self) -> str:
        """
        Returns the text that is within the span.
        """
        return self.__span_text

    @property
    def extracted_start_backticks(self) -> str:
        """
        Returns the backticks that started the code span.
        """
        return self.__extracted_start_backticks

    @property
    def leading_whitespace(self) -> str:
        """
        Returns the whitespace at the start of the code span.
        """
        return self.__leading_whitespace

    @property
    def trailing_whitespace(self) -> str:
        """
        Returns the whitespace at the end of the code span.
        """
        return self.__trailing_whitespace

    def register_for_markdown_transform(
        self,
        registration_function: Callable[
            [
                type,
                Callable[
                    [MarkdownTransformContext, MarkdownToken, Optional[MarkdownToken]],
                    str,
                ],
                Optional[
                    Callable[
                        [
                            MarkdownTransformContext,
                            MarkdownToken,
                            Optional[MarkdownToken],
                            Optional[MarkdownToken],
                        ],
                        str,
                    ]
                ],
            ],
            None,
        ],
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            InlineCodeSpanMarkdownToken,
            InlineCodeSpanMarkdownToken.__rehydrate_inline_code_span,
            None,
        )

    @staticmethod
    def __rehydrate_inline_code_span(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the code span data from the token.
        """
        _ = previous_token

        if context.block_stack[-1].is_inline_link:
            return ""

        current_inline_token = cast(InlineCodeSpanMarkdownToken, current_token)
        span_text = ParserHelper.remove_all_from_text(current_inline_token.span_text)
        leading_whitespace = ParserHelper.remove_all_from_text(
            current_inline_token.leading_whitespace
        )
        trailing_whitespace = ParserHelper.remove_all_from_text(
            current_inline_token.trailing_whitespace
        )

        if context.block_stack[-1].is_paragraph:
            block_paragraph_token = cast(
                ParagraphMarkdownToken, context.block_stack[-1]
            )
            (
                leading_whitespace,
                block_paragraph_token.rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                leading_whitespace,
                block_paragraph_token.extracted_whitespace,
                block_paragraph_token.rehydrate_index,
            )
            (
                span_text,
                block_paragraph_token.rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                span_text,
                block_paragraph_token.extracted_whitespace,
                block_paragraph_token.rehydrate_index,
            )
            (
                trailing_whitespace,
                block_paragraph_token.rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                trailing_whitespace,
                block_paragraph_token.extracted_whitespace,
                block_paragraph_token.rehydrate_index,
            )

        return "".join(
            [
                current_inline_token.extracted_start_backticks,
                leading_whitespace,
                span_text,
                trailing_whitespace,
                current_inline_token.extracted_start_backticks,
            ]
        )
