"""
Module to provide for special tokens that represent exceptional inline elements.
"""

from typing import Optional

from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class SpecialTextMarkdownToken(TextMarkdownToken):
    """
    Class to provide for special tokens that represent exceptional inline elements.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_text: str,
        repeat_count: int,
        preceding_two: Optional[str],
        following_two: Optional[str],
        is_active: bool = True,
        line_number: int = 0,
        column_number: int = 0,
    ):
        (
            self.__repeat_count,
            self.__is_active,
            self.__preceding_two,
            self.__following_two,
        ) = (repeat_count, is_active, preceding_two, following_two)
        TextMarkdownToken.__init__(
            self,
            token_text,
            "",
            "",
            line_number=line_number,
            column_number=column_number,
            is_special=True,
        )

    # pylint: enable=too-many-arguments

    @property
    def is_active(self) -> bool:
        """
        Returns a value indicating whether this special text is still active.
        """
        return self.__is_active

    @property
    def repeat_count(self) -> int:
        """
        Returns the repeat count for the special text element.
        """
        return self.__repeat_count

    @property
    def preceding_two(self) -> Optional[str]:
        """
        Returns the preceding two characters before this token.
        """
        return self.__preceding_two

    @property
    def following_two(self) -> Optional[str]:
        """
        Returns the following two characters before this token.
        """
        return self.__following_two

    def deactivate(self) -> None:
        """
        Mark this special token as deactivated.
        """
        self.__is_active = False

    def adjust_token_text_by_repeat_count(self) -> None:
        """
        Adjust the token's text by the repeat count.
        """
        self._set_token_text(self.token_text[: self.repeat_count])

    def reduce_repeat_count(
        self, emphasis_length: int, adjust_column_number: bool = False
    ) -> None:
        """
        Reduce the repeat count by the specified amount.
        """
        self.__repeat_count -= emphasis_length
        if adjust_column_number:
            self._set_column_number(self.column_number + emphasis_length)

    def show_process_emphasis(self) -> str:
        """
        Independent of the __str__ function, provide extra information.
        """
        return (
            f">>active={self.__is_active},repeat={self.__repeat_count},preceding='{self.__preceding_two}',"
            + f"following='{self.__following_two}':{self}"
        )
