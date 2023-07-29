"""
Module to provide for an encapsulation of the html block element.
"""

from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class HtmlBlockMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the html block element.
    """

    def __init__(
        self, position_marker: PositionMarker, extracted_whitespace: str
    ) -> None:
        assert position_marker
        line_number, column_number = position_marker.line_number, (
            position_marker.index_number
            + position_marker.index_indent
            + 1
            - len(extracted_whitespace)
        )
        # else:
        #     line_number, column_number = -1, -1

        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_html_block,
            "",
            line_number=line_number,
            column_number=column_number,
            extracted_whitespace=extracted_whitespace,
            requires_end_token=True,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_html_block

    # pylint: enable=protected-access
