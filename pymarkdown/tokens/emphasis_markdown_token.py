"""
Module to provide for an encapsulation of the inline emphasis element.
"""

from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class EmphasisMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline emphasis element.
    """

    def __init__(
        self,
        emphasis_length: int,
        emphasis_character: str,
        line_number: int = 0,
        column_number: int = 0,
    ) -> None:
        self.__emphasis_length, self.__emphasis_character = (
            emphasis_length,
            emphasis_character,
        )
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_emphasis,
            MarkdownToken.extra_data_separator.join(
                [str(emphasis_length), emphasis_character]
            ),
            line_number=line_number,
            column_number=column_number,
            requires_end_token=True,
            can_force_close=False,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_emphasis

    # pylint: enable=protected-access

    @property
    def emphasis_length(self) -> int:
        """
        Returns the length of the current emphasis text.
        """
        return self.__emphasis_length

    @property
    def emphasis_character(self) -> str:
        """
        Returns the character used for the current emphasis text.
        """
        return self.__emphasis_character
