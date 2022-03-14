"""
Module to hold the request information to pass on to the handle_* functions.
"""

from dataclasses import dataclass
from typing import Any, Optional


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class InlineRequest:
    """
    Class to hold the request information to pass on to the handle_* functions.
    """

    source_text: str
    next_index: int
    inline_blocks: Optional[Any] = None
    remaining_line: Optional[Any] = None
    current_string_unresolved: Optional[Any] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    para_owner: Optional[Any] = None


# pylint: enable=too-many-instance-attributes
