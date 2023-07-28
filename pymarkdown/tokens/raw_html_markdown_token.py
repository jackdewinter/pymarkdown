"""
Module to provide for an encapsulation of the inline raw html element.
"""

from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class RawHtmlMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline raw html element.
    """

    def __init__(self, raw_tag: str, line_number: int, column_number: int) -> None:
        self.__raw_tag = raw_tag
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_raw_html,
            self.__raw_tag,
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_raw_html

    # pylint: enable=protected-access

    @property
    def raw_tag(self) -> str:
        """
        Returns the text that is the raw html tag.
        """
        return self.__raw_tag
