"""
Module to provide for an encapsulation of the blank line element.
"""

from typing import Optional

from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class BlankLineMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the blank line element.
    """

    def __init__(
        self,
        extracted_whitespace: str,
        position_marker: Optional[PositionMarker],
        column_delta: int = 0,
    ) -> None:
        assert position_marker
        line_number, column_number = position_marker.line_number, (
            position_marker.index_number
            + position_marker.index_indent
            + 1
            - column_delta
        )
        # else:
        #     line_number, column_number = 0, 0

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_blank_line,
            extracted_whitespace,
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_blank_line

    # pylint: enable=protected-access
