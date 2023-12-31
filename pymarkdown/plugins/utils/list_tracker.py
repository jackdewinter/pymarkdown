from typing import Dict, List, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.reference_markdown_token import ReferenceMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class ListTracker:
    """
    Class to help rules keep track of lists.
    """

    def __init__(self) -> None:
        self.__list_stack: List[ListStartMarkdownToken] = []
        self.__line_count: Dict[int, int] = {}
        self.__list_start_indices: Dict[int, Dict[MarkdownToken, int]] = {}
        self.__list_end_indices: Dict[int, Dict[MarkdownToken, int]] = {}
        self.__list_adjustments: Dict[int, Dict[MarkdownToken, int]] = {}
        self.__current_list_tokens: Dict[int, MarkdownToken] = {}

    def starting_new_file(self) -> None:
        """
        Called from the `starting_new_file` function of the rule.
        """
        self.__line_count = {}
        self.__list_stack = []
        self.__list_start_indices = {}
        self.__list_end_indices = {}
        self.__list_adjustments = {}
        self.__current_list_tokens = {}

    def next_token(self, token: MarkdownToken) -> None:
        """
        Called from the `next_token` function of the rule.
        """
        if list_stack_length := len(self.__list_stack):
            self.__line_count[list_stack_length] += self.__count_newlines_in_token(
                token
            )

    def register(self, token: MarkdownToken, register_value: int) -> None:
        """
        Register an integer for a given list token at the current level.
        """
        list_level = len(self.__list_stack)
        self.__list_adjustments[list_level][token] = register_value

    def get_registrations(self) -> Dict[MarkdownToken, int]:
        """
        Get any registrations at this level.
        """
        list_level = len(self.__list_stack)
        return self.__list_adjustments[list_level]

    def get_start_stop(self, token: MarkdownToken) -> Tuple[int, int]:
        """
        Get the start and stop positions of the current list item.
        """
        list_level = len(self.__list_stack)
        start_index = self.__list_start_indices[list_level][token]
        end_index = self.__list_end_indices[list_level][token]
        return start_index, end_index

    def list_start(self, token: MarkdownToken) -> None:
        """
        Record the start of a list.
        """
        assert isinstance(token, ListStartMarkdownToken)
        self.__list_stack.append(token)
        list_level = len(self.__list_stack)
        self.__line_count[list_level] = 0

        new_map: Dict[MarkdownToken, int] = {}
        self.__list_start_indices[list_level] = new_map
        new_map[token] = self.__line_count[list_level]

        new_map = {}
        self.__list_end_indices[list_level] = new_map
        self.__current_list_tokens[list_level] = token

        new_map = {}
        self.__list_adjustments[list_level] = new_map

    def new_list_item(self, token: MarkdownToken) -> None:
        """
        Record a new item within the list.
        """
        list_level = len(self.__list_stack)
        assert list_level in self.__list_start_indices
        current_list_token = self.__current_list_tokens[list_level]
        self.__current_list_tokens[list_level] = token

        self.__list_end_indices[list_level][current_list_token] = self.__line_count[
            list_level
        ]
        self.__list_start_indices[list_level][token] = self.__line_count[list_level]

    def list_end(self) -> None:
        """
        Record the end of a list.
        """
        list_level = len(self.__list_stack)
        assert list_level in self.__list_start_indices

        current_list_token = self.__current_list_tokens[list_level]
        self.__list_end_indices[list_level][current_list_token] = self.__line_count[
            list_level
        ]

    def list_end_cleanup(self) -> None:
        """
        Cleanup after any processing of the end of the list.
        """
        list_level = len(self.__list_stack)
        assert list_level in self.__list_start_indices

        del self.__list_start_indices[list_level]
        del self.__list_end_indices[list_level]
        del self.__current_list_tokens[list_level]
        del self.__list_adjustments[list_level]

        del self.__line_count[len(self.__list_stack)]
        del self.__list_stack[-1]

    def __count_newlines_in_token(self, current_token: MarkdownToken) -> int:
        newlines_in_text_token = 0
        if current_token.is_text:
            text_token = cast(TextMarkdownToken, current_token)
            newlines_in_text_token = ParserHelper.count_newlines_in_text(
                text_token.token_text
            )
        elif current_token.is_inline_image or current_token.is_inline_link:
            reference_token = cast(ReferenceMarkdownToken, current_token)
            newlines_in_text_token += ParserHelper.count_newlines_in_text(
                reference_token.text_from_blocks
            )
        elif current_token.is_inline_raw_html:
            raw_html_token = cast(RawHtmlMarkdownToken, current_token)
            newlines_in_text_token += ParserHelper.count_newlines_in_text(
                raw_html_token.raw_tag
            )
        elif current_token.is_inline_code_span:
            code_span_token = cast(InlineCodeSpanMarkdownToken, current_token)
            newlines_in_text_token += ParserHelper.count_newlines_in_texts(
                code_span_token.leading_whitespace,
                code_span_token.span_text,
                code_span_token.trailing_whitespace,
            )
        return newlines_in_text_token
