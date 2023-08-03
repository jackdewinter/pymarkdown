"""
Module to provide an encapsulation of the location within the Markdown document.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PositionMarker:
    """
    Class to provide an encapsulation of the location within the Markdown document.
    """

    line_number: int
    index_number: int
    text_to_parse: str
    index_indent: int = 0
