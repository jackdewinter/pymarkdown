"""
Module to hold the token to fix and how to fix it.
"""

from dataclasses import dataclass
from typing import Union

from pymarkdown.tokens.markdown_token import MarkdownToken


@dataclass(frozen=True)
class FixTokenRecord:
    """
    Class to hold the token to fix and how to fix it.
    """

    token_to_fix: MarkdownToken
    plugin_id: str
    plugin_action: str
    field_name: str
    field_value: Union[str, int]
