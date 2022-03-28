"""
Module to contain information on link titles.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LinkReferenceTitles:
    """
    Class to contain information on link titles.
    """

    inline_link: Optional[str]
    inline_title: Optional[str]
