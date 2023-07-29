"""
Module to provide for an encapsulation of the thematic break element.
"""

from typing import Optional

from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class ThematicBreakMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the thematic break element.
    """

    def __init__(
        self,
        start_character: str,
        extracted_whitespace: Optional[str],
        rest_of_line: str,
        position_marker: PositionMarker,
    ) -> None:
        assert extracted_whitespace is not None
        self.__rest_of_line = rest_of_line
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_thematic_break,
            MarkdownToken.extra_data_separator.join(
                [start_character, extracted_whitespace, self.__rest_of_line]
            ),
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_thematic_break

    # pylint: enable=protected-access

    @property
    def rest_of_line(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__rest_of_line
