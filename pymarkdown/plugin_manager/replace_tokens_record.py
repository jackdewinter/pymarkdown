"""
Module to keep track of a request made by a plugin rule.
"""

from dataclasses import dataclass
from typing import List

from pymarkdown.tokens.markdown_token import MarkdownToken


@dataclass
class ReplaceTokensRecord:
    """
    Record to keep track of a request made by a plugin rule.
    """

    plugin_id: str
    start_token: MarkdownToken
    end_token: MarkdownToken
    replacement_tokens: List[MarkdownToken]
