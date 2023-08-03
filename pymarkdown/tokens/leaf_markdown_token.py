"""
Module to provide for a leaf element that can be added to markdown parsing stream.
"""
from typing import Optional

from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.markdown_token import MarkdownToken, MarkdownTokenClass


class LeafMarkdownToken(MarkdownToken):
    """
    Class to provide for a leaf element that can be added to markdown parsing stream.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_name: str,
        extra_data: Optional[str],
        line_number: int = 0,
        column_number: int = 0,
        position_marker: Optional[PositionMarker] = None,
        extracted_whitespace: str = "",
        is_extension: bool = False,
        requires_end_token: bool = False,
        can_force_close: bool = True,
    ) -> None:
        self.__extracted_whitespace = extracted_whitespace
        MarkdownToken.__init__(
            self,
            token_name,
            MarkdownTokenClass.LEAF_BLOCK,
            extra_data,
            line_number=line_number,
            column_number=column_number,
            position_marker=position_marker,
            is_extension=is_extension,
            requires_end_token=requires_end_token,
            can_force_close=can_force_close,
        )

    # pylint: enable=too-many-arguments

    @property
    def extracted_whitespace(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace
