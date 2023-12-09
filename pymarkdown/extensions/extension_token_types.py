"""
Module to contain lists of the available extension token types.
"""


from typing import List

from pymarkdown.extensions.front_matter_markdown_token import FrontMatterMarkdownToken
from pymarkdown.extensions.pragma_token import PragmaToken
from pymarkdown.extensions.task_list_items import TaskListToken


# pylint: disable=too-few-public-methods
class ExtensionTokenTypes:
    """
    Class to contain lists of the available token types.
    """

    __TOKEN_TYPES: List[type] = [FrontMatterMarkdownToken, PragmaToken, TaskListToken]

    @staticmethod
    def get_token_types() -> List[type]:
        """
        Get a list of all available extension token types.
        """
        return ExtensionTokenTypes.__TOKEN_TYPES


# pylint: enable=too-few-public-methods
