"""
Module to provide for an encapsulation of the setext heading element.
"""

from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken


class SetextHeadingMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the setext heading element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        heading_character: str,
        heading_character_count: int,
        extracted_whitespace: str,
        position_marker: PositionMarker,
        para_token: ParagraphMarkdownToken,
    ) -> None:
        (
            self.__heading_character,
            self.__heading_character_count,
            self.__final_whitespace,
            self.__original_line_number,
            self.__original_column_number,
        ) = (
            heading_character,
            heading_character_count,
            "",
            para_token.line_number if para_token else -1,
            para_token.column_number if para_token else -1,
        )

        if self.__heading_character == "=":
            self.__hash_count = 1
        else:
            assert self.__heading_character == "-"
            self.__hash_count = 2

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_setext_heading,
            "",
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
            can_force_close=False,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments
    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_setext_heading

    # pylint: enable=protected-access

    @property
    def final_whitespace(self) -> str:
        """
        Returns any final whitespace at the end of the heading that was removed.
        """
        return self.__final_whitespace

    @property
    def heading_character(self) -> str:
        """
        Returns the character associated with the heading start.
        """
        return self.__heading_character

    @property
    def hash_count(self) -> int:
        """
        Returns the count in equivalence of "Atx Hash" counts.
        """
        return self.__hash_count

    @property
    def heading_character_count(self) -> int:
        """
        Returns the count of characters associated with the heading start.
        """
        return self.__heading_character_count

    @property
    def original_line_number(self) -> int:
        """
        Returns the line number where this element actually started.
        """
        return self.__original_line_number

    @property
    def original_column_number(self) -> int:
        """
        Returns the column number where this element actually started.
        """
        return self.__original_column_number

    def set_final_whitespace(self, whitespace_to_set: str) -> None:
        """
        Set the final whitespace for the paragraph. That is any whitespace at the very
        end of the paragraph, removed to prevent hard lines at the end.
        """

        self.__final_whitespace = whitespace_to_set
        self.__compose_extra_data_field()

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        original_location = (
            f"({self.original_line_number},{self.original_column_number})"
        )
        field_parts = [
            self.__heading_character,
            str(self.__heading_character_count),
            self.extracted_whitespace,
            original_location,
        ]
        if self.final_whitespace:
            field_parts.append(self.final_whitespace)
        self._set_extra_data(MarkdownToken.extra_data_separator.join(field_parts))
