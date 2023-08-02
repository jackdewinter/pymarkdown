"""
Module to provide for a container element that can be added to markdown parsing stream.
"""
import logging
from typing import Optional

from pymarkdown.parser_logger import ParserLogger
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.markdown_token import MarkdownToken, MarkdownTokenClass

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-many-arguments
class ContainerMarkdownToken(MarkdownToken):
    """
    Class to provide for a container element that can be added to markdown parsing stream.
    """

    def __init__(
        self,
        token_name: str,
        extra_data: str,
        line_number: int = 0,
        column_number: int = 0,
        position_marker: Optional[PositionMarker] = None,
    ) -> None:
        MarkdownToken.__init__(
            self,
            token_name,
            MarkdownTokenClass.CONTAINER_BLOCK,
            extra_data,
            line_number=line_number,
            column_number=column_number,
            position_marker=position_marker,
            requires_end_token=True,
        )


# pylint: enable=too-many-arguments
