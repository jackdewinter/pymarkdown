"""
Module to provide for an encapsulation of the high level state of the parser.
"""
from __future__ import annotations

import copy
from typing import List, Optional, Tuple, cast

from typing_extensions import Protocol

from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.requeue_line_info import RequeueLineInfo
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import ListStackToken, StackToken


# pylint: disable=too-few-public-methods
class CloseOpenBlocksProtocol(Protocol):
    """
    Protocol to provide typing for the close open blocks function.
    """

    # pylint: disable=too-many-arguments
    def __call__(
        self,
        parser_state: ParserState,
        destination_array: Optional[List[MarkdownToken]] = None,
        only_these_blocks: Optional[List[type]] = None,
        include_block_quotes: bool = False,
        include_lists: bool = False,
        until_this_index: int = -1,
        caller_can_handle_requeue: bool = False,
        requeue_reset: bool = False,
        was_forced: bool = False,
    ) -> Tuple[List[MarkdownToken], Optional[RequeueLineInfo]]:
        ...  # pragma: no cover

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class HandleBlankLineProtocol(Protocol):
    """
    Protocol to provide typing for the blank line function.
    """

    def __call__(
        self,
        parser_state: ParserState,
        input_line: str,
        from_main_transform: bool,
        position_marker: Optional[PositionMarker] = None,
    ) -> Tuple[Optional[List[MarkdownToken]], Optional[RequeueLineInfo]]:
        ...  # pragma: no cover


# pylint: enable=too-few-public-methods


# pylint: disable=too-many-instance-attributes
class ParserState:
    """
    Class to provide for an encapsulation of the high level state of the parser.
    """

    def __init__(
        self,
        token_stack: List[StackToken],
        token_document: List[MarkdownToken],
        close_open_blocks_fn: CloseOpenBlocksProtocol,
        handle_blank_line_fn: HandleBlankLineProtocol,
    ) -> None:
        (
            self.__token_stack,
            self.__token_document,
            self.__close_open_blocks_fn,
            self.__handle_blank_line_fn,
        ) = (token_stack, token_document, close_open_blocks_fn, handle_blank_line_fn)

        self.__no_para_start_if_empty: bool = False
        self.__last_block_quote_stack_token: Optional[StackToken] = None
        self.__last_block_quote_markdown_token_index: Optional[int] = None
        self.__copy_of_last_block_quote_markdown_token: Optional[
            BlockQuoteMarkdownToken
        ] = None
        self.__original_stack_depth: int = 0
        self.__original_document_depth: int = 0
        self.__original_line_to_parse: Optional[str] = None
        self.__same_line_container_tokens: Optional[List[MarkdownToken]] = None
        self.nested_list_start: Optional[ListStackToken] = None
        self.copy_of_token_stack: List[StackToken] = []
        self.block_copy: List[Optional[MarkdownToken]] = []

    @property
    def token_stack(self) -> List[StackToken]:
        """
        Stack array containing the currently active stack tokens.
        """
        return self.__token_stack

    @property
    def token_document(self) -> List[MarkdownToken]:
        """
        Document array containing any Markdown tokens.
        """
        return self.__token_document

    @property
    def close_open_blocks_fn(self) -> CloseOpenBlocksProtocol:
        """
        Function to handle the closing of blocks.
        """
        return self.__close_open_blocks_fn

    @property
    def handle_blank_line_fn(self) -> HandleBlankLineProtocol:
        """
        Function to handle blank lines.
        """
        return self.__handle_blank_line_fn

    @property
    def same_line_container_tokens(self) -> Optional[List[MarkdownToken]]:
        """
        State of the container tokens at the start of the leaf processing.
        """
        return self.__same_line_container_tokens

    @property
    def last_block_quote_stack_token(self) -> Optional[StackToken]:
        """
        Last block quote token.
        """
        return self.__last_block_quote_stack_token

    @property
    def last_block_quote_markdown_token_index(self) -> Optional[int]:
        """
        Index of the last block quote token.
        """
        return self.__last_block_quote_markdown_token_index

    @property
    def copy_of_last_block_quote_markdown_token(
        self,
    ) -> Optional[BlockQuoteMarkdownToken]:
        """
        Copy of the last block quote markdown token, before any changes.
        """
        return self.__copy_of_last_block_quote_markdown_token

    @property
    def original_line_to_parse(self) -> Optional[str]:
        """
        Line to parse, before any processing occurs.
        """
        return self.__original_line_to_parse

    @property
    def original_stack_depth(self) -> int:
        """
        Length of the token_stack array at the start of the line.
        """
        return self.__original_stack_depth

    @property
    def original_document_depth(self) -> int:
        """
        Length of the token_document array at the start of the line.
        """
        return self.__original_document_depth

    @property
    def no_para_start_if_empty(self) -> bool:
        """
        Whether to start a paragraph if the owning list item was empty.
        """
        return self.__no_para_start_if_empty

    def find_last_block_quote_on_stack(self) -> int:
        """
        Finds the index of the last block quote on the stack (from the end).
        If no block quotes are found, 0 is returned.
        """
        last_stack_index = len(self.token_stack) - 1
        while (
            not self.token_stack[last_stack_index].is_document
            and not self.token_stack[last_stack_index].is_block_quote
        ):
            last_stack_index -= 1
        return last_stack_index

    def find_last_list_block_on_stack(self) -> int:
        """
        Finds the index of the last list block on the stack (from the end).
        If no block quotes are found, 0 is returned.
        """
        last_stack_index = len(self.token_stack) - 1
        while (
            not self.token_stack[last_stack_index].is_document
            and not self.token_stack[last_stack_index].is_list
        ):
            last_stack_index -= 1
        return last_stack_index

    def find_last_container_on_stack(self) -> int:
        """
        Finds the index of the last container on the stack (from the end).
        If no container tokens are found, 0 is returned.
        """
        last_stack_index = len(self.token_stack) - 1
        while not self.token_stack[last_stack_index].is_document and not (
            self.token_stack[last_stack_index].is_block_quote
            or self.token_stack[last_stack_index].is_list
        ):
            last_stack_index -= 1
        return last_stack_index

    def count_of_block_quotes_on_stack(self) -> int:
        """
        Helper method to count the number of block quotes currently on the stack.
        """

        return sum(
            bool(next_item_on_stack.is_block_quote)
            for next_item_on_stack in self.token_stack
        )

    def mark_start_information(self, position_marker: PositionMarker) -> None:
        """
        Mark the start of processing this line of information.  A lot of
        this information is to allow a requeue to occur, if needed.
        """
        (
            self.__original_line_to_parse,
            self.__original_stack_depth,
            self.__original_document_depth,
            self.__no_para_start_if_empty,
        ) = (
            position_marker.text_to_parse[:],
            len(self.token_stack),
            len(self.token_document),
            False,
        )

        last_stack_index = self.find_last_block_quote_on_stack()

        (
            self.__last_block_quote_stack_token,
            self.__last_block_quote_markdown_token_index,
        ) = (None, None)
        self.__copy_of_last_block_quote_markdown_token = None
        if not self.token_stack[last_stack_index].is_document:
            self.__last_block_quote_stack_token = self.token_stack[last_stack_index]
            markdown_token = self.token_stack[last_stack_index].matching_markdown_token
            assert markdown_token is not None
            self.__last_block_quote_markdown_token_index = self.token_document.index(
                markdown_token
            )
            self.__copy_of_last_block_quote_markdown_token = cast(
                BlockQuoteMarkdownToken,
                copy.deepcopy(
                    self.token_document[self.__last_block_quote_markdown_token_index]
                ),
            )

    def mark_for_leaf_processing(
        self, container_level_tokens: List[MarkdownToken]
    ) -> None:
        """
        Set things up for leaf processing.
        """
        self.__same_line_container_tokens = container_level_tokens

    def clear_after_leaf_processing(self) -> None:
        """
        Reset things after leaf processing.
        """
        self.__same_line_container_tokens = None

    def set_no_para_start_if_empty(self) -> None:
        """
        Set the member variable to true.
        """
        self.__no_para_start_if_empty = True


# pylint: enable=too-many-instance-attributes
