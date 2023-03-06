"""
Module to hold the request information to pass on to the handle_* functions.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from pymarkdown.leaf_markdown_token import ParagraphMarkdownToken
from pymarkdown.markdown_token import MarkdownToken


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class InlineRequest:
    """
    Class to hold the request information to pass on to the handle_* functions.
    """

    source_text: str
    next_index: int
    inline_blocks: List[MarkdownToken] = field(default_factory=list)
    remaining_line: Optional[str] = None
    tabified_remaining_line: Optional[str] = None
    current_string_unresolved: Optional[str] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    para_owner: Optional[ParagraphMarkdownToken] = None
    tabified_text: Optional[str] = None


# pylint: enable=too-many-instance-attributes
