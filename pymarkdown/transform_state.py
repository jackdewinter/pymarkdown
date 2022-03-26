"""
Module that contains the state of transformation of TransformToGfm.
"""

from typing import List, Optional

from pymarkdown.markdown_token import MarkdownToken


# pylint: disable=too-many-instance-attributes
class TransformState:
    """
    Class that contains the state of transformation of TransformToGfm.
    """

    def __init__(self, actual_tokens: List[MarkdownToken]) -> None:
        """
        Initializes a new instance of the TransformState class.
        """
        (
            self.__is_in_code_block,
            self.__is_in_fenced_code_block,
            self.__is_in_html_block,
            self.__is_in_loose_list,
            self.__actual_tokens,
            self.__actual_token_index,
        ) = (False, False, False, True, actual_tokens, 0)
        self.__add_trailing_text: Optional[str] = None
        self.__add_leading_text: Optional[str] = None
        self.__next_token: Optional[MarkdownToken] = None
        self.__transform_stack: List[str] = []
        self.__last_token: Optional[MarkdownToken] = None

    @property
    def is_in_code_block(self) -> bool:
        """
        Whether the generator is currently inside of a code block.
        """
        return self.__is_in_code_block

    @is_in_code_block.setter
    def is_in_code_block(self, value: bool) -> None:
        """
        Set whether the generator is currently inside of a code block.
        """
        self.__is_in_code_block = value

    @property
    def is_in_fenced_code_block(self) -> bool:
        """
        Whether the generator is currently inside of a fenced code block.
        """
        return self.__is_in_fenced_code_block

    @is_in_fenced_code_block.setter
    def is_in_fenced_code_block(self, value: bool) -> None:
        """
        Set whether the generator is currently inside of a fenced code block.
        """
        self.__is_in_fenced_code_block = value

    @property
    def is_in_html_block(self) -> bool:
        """
        Whether the generator is currently inside of a HTML block.
        """
        return self.__is_in_html_block

    @is_in_html_block.setter
    def is_in_html_block(self, value: bool) -> None:
        """
        Set whether the generator is currently inside of a HTML block.
        """
        self.__is_in_html_block = value

    @property
    def is_in_loose_list(self) -> bool:
        """
        Whether the generator is currently inside of a loose list.
        """
        return self.__is_in_loose_list

    @is_in_loose_list.setter
    def is_in_loose_list(self, value: bool) -> None:
        """
        Set whether the generator is currently inside of a loose list.
        """
        self.__is_in_loose_list = value

    @property
    def transform_stack(self) -> List[str]:
        """
        Stack used to keep track of scope within the generator.
        """
        return self.__transform_stack

    @property
    def add_trailing_text(self) -> Optional[str]:
        """
        Keep track of trailing text.
        """
        return self.__add_trailing_text

    @add_trailing_text.setter
    def add_trailing_text(self, value: Optional[str]) -> None:
        """
        Set trailing text to keep track of.
        """
        self.__add_trailing_text = value

    @property
    def add_leading_text(self) -> Optional[str]:
        """
        Keep track of leading text.
        """
        return self.__add_leading_text

    @add_leading_text.setter
    def add_leading_text(self, value: Optional[str]) -> None:
        """
        Set leading text to keep track of.
        """
        self.__add_leading_text = value

    @property
    def next_token(self) -> Optional[MarkdownToken]:
        """
        Next token to process.
        """
        return self.__next_token

    @next_token.setter
    def next_token(self, value: Optional[MarkdownToken]) -> None:
        """
        Sets the next token to process.
        """
        self.__next_token = value

    @property
    def last_token(self) -> Optional[MarkdownToken]:
        """
        Last token to process.
        """
        return self.__last_token

    @last_token.setter
    def last_token(self, value: Optional[MarkdownToken]) -> None:
        """
        Sets the last token to process.
        """
        self.__last_token = value

    @property
    def actual_tokens(self) -> List[MarkdownToken]:
        """
        Actual tokens to use to generate the HTML with.
        """
        return self.__actual_tokens

    @property
    def actual_token_index(self) -> int:
        """
        Index into the actual token list.
        """
        return self.__actual_token_index

    @actual_token_index.setter
    def actual_token_index(self, value: int) -> None:
        """
        Sets the new index into the actual token list.
        """
        self.__actual_token_index = value


# pylint: enable=too-many-instance-attributes
