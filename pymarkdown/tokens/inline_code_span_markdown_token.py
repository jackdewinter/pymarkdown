"""
Module to provide for an encapsulation of the inline code span element.
"""

from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


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
