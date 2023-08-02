"""
Module to provide for an inline element that can be added to markdown parsing stream.
"""
import logging
from typing import Optional

from pymarkdown.parser_logger import ParserLogger
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.markdown_token import MarkdownToken, MarkdownTokenClass

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-many-arguments
class InlineMarkdownToken(MarkdownToken):
    """
    Class to provide for a leaf element that can be added to markdown parsing stream.
    """

    def __init__(
        self,
        token_name: str,
        extra_data: Optional[str],
        line_number: int = 0,
        column_number: int = 0,
        position_marker: Optional[PositionMarker] = None,
        requires_end_token: bool = False,
        can_force_close: bool = True,
        is_special: bool = False,
    ):
        MarkdownToken.__init__(
            self,
            token_name,
            MarkdownTokenClass.INLINE_BLOCK,
            extra_data,
            line_number=line_number,
            column_number=column_number,
            position_marker=position_marker,
            can_force_close=can_force_close,
            requires_end_token=requires_end_token,
            is_special=is_special,
        )


# pylint: enable=too-many-arguments
