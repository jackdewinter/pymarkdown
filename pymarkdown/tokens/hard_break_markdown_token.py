"""
Module to provide for an encapsulation of the inline hard line break element.
"""

from typing import Callable, Optional, cast

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
)


class HardBreakMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline hard line break element.
    """

    def __init__(self, line_end: str, line_number: int, column_number: int) -> None:
        self.__line_end = line_end
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_hard_break,
            MarkdownToken.extra_data_separator.join(
                [
                    self.__line_end,
                    ParserHelper.newline_character,
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
        return MarkdownToken._token_inline_hard_break

    # pylint: enable=protected-access

    @property
    def line_end(self) -> str:
        """
        Returns the text at the end of the line.
        """
        return self.__line_end

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
            HardBreakMarkdownToken, HardBreakMarkdownToken.__rehydrate_hard_break, None
        )

    @staticmethod
    def __rehydrate_hard_break(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the hard break text from the token.
        """
        _ = previous_token

        current_hard_break_token = cast(HardBreakMarkdownToken, current_token)
        leading_whitespace = (
            f"{current_hard_break_token.line_end}{ParserHelper.newline_character}"
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

        return "" if context.block_stack[-1].is_inline_link else leading_whitespace
