"""
Module to hold the response from the inline handle_* functions.
"""

from dataclasses import dataclass
from typing import Any, Optional


# pylint: disable=too-many-instance-attributes
@dataclass
class InlineResponse:
    """
    Class to hold the response from the inline handle_* functions.
    """

    new_string: Optional[str] = None
    new_string_unresolved: Optional[str] = None
    new_index: Optional[int] = None
    new_tokens: Any = None
    consume_rest_of_line: bool = False
    original_string: Optional[str] = None
    delta_line_number: int = 0
    delta_column_number: int = 0


# pylint: enable=too-many-instance-attributes
