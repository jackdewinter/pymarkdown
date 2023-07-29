"""
Module to provide for an encapsulation of the ordered list start element.
"""

from typing import Optional

from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class OrderedListStartMarkdownToken(ListStartMarkdownToken):
    """
    Class to provide for an encapsulation of the ordered list start element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        list_start_sequence: str,
        list_start_content: str,
        indent_level: int,
        tabbed_adjust: int,
        extracted_whitespace: str,
        tabbed_whitespace_to_add: Optional[str],
        position_marker: PositionMarker,
    ) -> None:
        ListStartMarkdownToken.__init__(
            self,
            MarkdownToken._token_ordered_list_start,
            position_marker,
            list_start_sequence,
            list_start_content,
            indent_level,
            tabbed_adjust,
            extracted_whitespace,
            tabbed_whitespace_to_add,
        )

    # pylint: enable=too-many-arguments
    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_ordered_list_start

    # pylint: enable=protected-access
