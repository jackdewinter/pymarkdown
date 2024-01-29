"""
Module containing extra information for a link reference.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LinkReferenceInfo:
    """
    Class containing extra information for a link reference.
    """

    collected_destination: Optional[str]
    line_destination_whitespace: Optional[str]
    inline_raw_link: Optional[str]
    line_title_whitespace: Optional[str]
    inline_raw_title: Optional[str]
    end_whitespace: Optional[str]
