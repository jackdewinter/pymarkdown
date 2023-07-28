"""
Module to provide for an encapsulation of the inline uri autolink element.
"""

from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class UriAutolinkMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the inline uri autolink element.
    """

    def __init__(
        self, autolink_text: str, line_number: int, column_number: int
    ) -> None:
        self.__autolink_text = autolink_text
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_inline_uri_autolink,
            self.__autolink_text,
            line_number=line_number,
            column_number=column_number,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_uri_autolink

    # pylint: enable=protected-access

    @property
    def autolink_text(self) -> str:
        """
        Returns the text that is the autolink.
        """
        return self.__autolink_text
