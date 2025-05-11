"""
Module to provide for an encapsulation of the high level state of the parser.
"""

from __future__ import annotations

import copy
from typing import List, Optional, Tuple, cast

from typing_extensions import Protocol

from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.requeue_line_info import RequeueLineInfo
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import (
    ListStackToken,
    StackToken,
    TableBlockStackToken,
)


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
    ) -> Tuple[List[MarkdownToken], Optional[RequeueLineInfo]]: ...  # pragma: no cover

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
    ) -> Tuple[
        Optional[List[MarkdownToken]], Optional[RequeueLineInfo]
    ]: ...  # pragma: no cover


# pylint: enable=too-few-public-methods


# pylint: disable=too-many-instance-attributes, too-many-public-methods
class ParserState:
    """
    Class to provide for an encapsulation of the high level state of the parser.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_stack: List[StackToken],
        token_document: List[MarkdownToken],
        close_open_blocks_fn: CloseOpenBlocksProtocol,
        handle_blank_line_fn: HandleBlankLineProtocol,
        parse_properties: ParseBlockPassProperties,
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
        self.__x1_token: Optional[ListStartMarkdownToken] = None
        self.__copy_of_x1_token: Optional[ListStartMarkdownToken] = None
        self.__x1_token_index: Optional[int] = -1

        self.__original_stack_depth: int = 0
        self.__original_document_depth: int = 0
        self.__original_line_to_parse: Optional[str] = None
        self.__same_line_container_tokens: Optional[List[MarkdownToken]] = None
        self.nested_list_start: Optional[ListStackToken] = None
        self.copy_of_token_stack: List[StackToken] = []
        self.block_copy: List[Optional[MarkdownToken]] = []
        self.parse_properties = parse_properties

    # pylint: enable=too-many-arguments

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

    @property
    def x1_token(self) -> Optional[ListStartMarkdownToken]:
        """
        TBD
        """
        return self.__x1_token

    @property
    def copy_of_x1_token(self) -> Optional[ListStartMarkdownToken]:
        """
        TBD
        """
        return self.__copy_of_x1_token

    @property
    def x1_token_index(self) -> Optional[int]:
        """
        TBD
        """
        return self.__x1_token_index

    def __abc_part_1(
        self, number_of_lines_to_requeue: int, stack_token: TableBlockStackToken
    ) -> None:
        last_list_index = -1
        last_list_token = stack_token.x1_token
        if last_list_token is None:
            last_list_index = self.find_last_list_block_on_stack()
            if last_list_index > 0:
                last_list_token = self.token_stack[
                    last_list_index
                ].matching_markdown_token

        if last_list_token:
            list_token = cast(ListStartMarkdownToken, last_list_token)
            if last_list_index != -1:
                prev_leading_space_count = -1
            else:
                prev_leading_spaces = cast(
                    ListStartMarkdownToken, stack_token.copy_of_x1_token
                ).leading_spaces
                prev_leading_space_count = (
                    prev_leading_spaces.count("\n") if prev_leading_spaces else -1
                )

            leading_space_count = (
                list_token.leading_spaces.count("\n")
                if list_token.leading_spaces
                else 0
            )
            while (
                number_of_lines_to_requeue > 0
                and leading_space_count > prev_leading_space_count
            ):
                if list_token.leading_spaces:
                    list_token.remove_last_leading_space()
                number_of_lines_to_requeue -= 1
                leading_space_count = (
                    list_token.leading_spaces.count("\n")
                    if list_token.leading_spaces
                    else 0
                )

    def abc(self, requeue_line_info: RequeueLineInfo, stack_token: StackToken) -> None:
        """
        TBD

        need to have common "multi-line" stack token base, not assume TableBlockStackToken
        """
        if requeue_line_info.has_been_abc_ed:
            return
        number_of_lines_to_requeue = len(requeue_line_info.lines_to_requeue)
        self.__abc_part_1(
            number_of_lines_to_requeue, cast(TableBlockStackToken, stack_token)
        )
        last_block_stack_token = cast(
            TableBlockStackToken, stack_token
        ).last_block_quote_stack_token
        if last_block_stack_token is None:
            if (last_block_quote_index := self.find_last_block_quote_on_stack()) > 0:
                last_block_stack_token = self.token_stack[last_block_quote_index]
        if last_block_stack_token:
            assert last_block_stack_token.matching_markdown_token is not None
            # if last_block_stack_token.matching_markdown_token is not None:
            block_quote_token = cast(
                BlockQuoteMarkdownToken, last_block_stack_token.matching_markdown_token
            )
            # endif
            copy_of_block_quote_token = cast(
                TableBlockStackToken, stack_token
            ).copy_of_last_block_quote_markdown_token
            bleading_space_count = (
                copy_of_block_quote_token.bleading_spaces.count("\n")
                if copy_of_block_quote_token
                and copy_of_block_quote_token.bleading_spaces
                else -1
            )
            if isinstance(stack_token, TableBlockStackToken):
                bleading_space_count -= 1
            current_bleading_space_count = (
                block_quote_token.bleading_spaces.count("\n")
                if block_quote_token.bleading_spaces
                else 0
            )
            while (
                number_of_lines_to_requeue > 0
                and current_bleading_space_count > bleading_space_count
            ):
                if block_quote_token.bleading_spaces:
                    block_quote_token.remove_last_bleading_space()
                number_of_lines_to_requeue -= 1
                current_bleading_space_count = (
                    block_quote_token.bleading_spaces.count("\n")
                    if block_quote_token.bleading_spaces
                    else 0
                )
        requeue_line_info.has_been_abc_ed = True

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
            assert (
                markdown_token is not None
            ), "Always start with a container or leaf token, that has a matching markdown token."
            try:
                self.__last_block_quote_markdown_token_index = (
                    self.token_document.index(markdown_token)
                )
                self.__copy_of_last_block_quote_markdown_token = cast(
                    BlockQuoteMarkdownToken,
                    copy.deepcopy(
                        self.token_document[
                            self.__last_block_quote_markdown_token_index
                        ]
                    ),
                )
            except ValueError:
                self.__last_block_quote_markdown_token_index = -1
                self.__copy_of_last_block_quote_markdown_token = None
        x1 = self.find_last_list_block_on_stack()
        self.__x1_token = None
        self.__copy_of_x1_token = None
        self.__x1_token_index = -1
        if not self.token_stack[x1].is_document:
            matching_token = self.token_stack[x1].matching_markdown_token
            assert matching_token is not None
            assert isinstance(matching_token, ListStartMarkdownToken)
            self.__x1_token = matching_token

            self.__copy_of_x1_token = copy.deepcopy(self.__x1_token)
            self.__x1_token_index = self.token_document.index(self.__x1_token)

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


# pylint: enable=too-many-instance-attributes, too-many-public-methods
