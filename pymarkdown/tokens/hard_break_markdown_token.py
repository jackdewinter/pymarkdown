"""
Module to provide for an encapsulation of the inline hard line break element.
"""

from pymarkdown.parser_helper import ParserHelper
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


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
