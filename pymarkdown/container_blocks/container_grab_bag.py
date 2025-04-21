"""
Class to provide a "grab bag" for commonly used properties for the Container Block Processor.
"""

import logging
from typing import Any, List, Optional, Tuple

from typing_extensions import Protocol

from pymarkdown.block_quotes.block_quote_data import BlockQuoteData
from pymarkdown.container_blocks.container_indices import ContainerIndices
from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.requeue_line_info import RequeueLineInfo
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.stack_token import StackToken

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class ParseForContainerBlocksProtocol(Protocol):
    """
    Protocol to do further parsing for container blocks.
    """

    # pylint: disable=too-many-arguments
    def __call__(
        self,
        parser_state: ParserState,
        position_marker: PositionMarker,
        ignore_link_definition_start: bool,
        ignore_table_start: bool,
        parser_properties: ParseBlockPassProperties,
        container_start_bq_count: int,
        container_depth: int,
        adjusted_block_index: Optional[int],
        initial_block_quote_count: Optional[int],
        original_line: Optional[str],
    ) -> Tuple[
        List[MarkdownToken],
        Optional[str],
        Optional[int],
        Optional[RequeueLineInfo],
        bool,
        bool,
    ]: ...  # pragma: no cover

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
class ContainerGrabBag:
    """
    Class to provide for a grab bag of values instead of passing
    them around one by one.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        parser_state: ParserState,
        container_depth: int,
        initial_block_quote_count: Optional[int],
        adjusted_block_index: Optional[int],
        container_start_bq_count: int,
        parser_properties: ParseBlockPassProperties,
        ignore_link_definition_start: bool,
        ignore_table_start: bool,
        original_line: str,
        recurse_fn: ParseForContainerBlocksProtocol,
    ) -> None:
        # Functions
        self.__recurse_fn = recurse_fn

        # Booleans
        self.__did_blank: bool = False
        self.__was_paragraph_continuation: bool = False
        self.__do_skip_containers_before_leaf_blocks: bool = False
        self.__was_indent_already_processed: bool = False
        self.__do_force_leaf_token_parse: bool = False
        self.__did_indent_processing: bool = False
        self.__have_pre_processed_indent: bool = False
        self.__can_continue: bool = False
        self.__do_force_list_continuation = False

        # Integers
        self.__indent_used_by_container: int = -1
        self.__indent_already_processed: int = -1
        self.__last_block_quote_index: int = -1
        self.__last_list_start_index: int = -1
        self.__start_index: int = -1

        # Optional integers
        self.__removed_chars_at_start_of_line: Optional[int] = None

        # Strings
        self.__adj_line_to_parse: str = ""
        self.__line_to_parse: str = ""

        # Optional strings
        self.__weird_adjusted_text: Optional[str] = None
        self.__indent_used_by_list: Optional[str] = None
        self.__text_removed_by_container: Optional[str] = None
        self.__extracted_whitespace: Optional[str] = None
        self.__adj_ws: Optional[str] = None
        self.__bogus: Optional[str] = None

        # Others
        self.__block_quote_data = BlockQuoteData(-1, -1)
        self.__end_container_indices = ContainerIndices(-1, -1, -1)
        self.__requeue_line_info: Optional[RequeueLineInfo] = None
        self.__current_container_blocks: List[StackToken] = []
        self.__leaf_tokens: List[MarkdownToken] = []
        self.__container_level_tokens: List[MarkdownToken] = []

        # Read only values
        self.__container_depth = container_depth
        self.__initial_block_quote_count = initial_block_quote_count
        self.__adjusted_block_index = adjusted_block_index
        self.__container_start_bq_count = container_start_bq_count
        self.__parser_properties = parser_properties
        self.__do_ignore_link_definition_start = ignore_link_definition_start
        self.__do_ignore_table_start = ignore_table_start
        self.__original_line = original_line
        self.__is_para_continue = (
            bool(
                parser_state
                and parser_state.token_stack
                and len(parser_state.token_stack) >= 2
                and parser_state.token_stack[-1].is_paragraph
            )
            and not parser_state.token_document[-1].is_blank_line
        )
        self.__log_initial_values()

    def __log_initial_values(self) -> None:
        # Booleans
        self.__log_read_write_value("did_blank", self.__did_blank)
        self.__log_read_write_value(
            "was_paragraph_continuation", self.__was_paragraph_continuation
        )
        self.__log_read_write_value(
            "do_skip_containers_before_leaf_blocks",
            self.__do_skip_containers_before_leaf_blocks,
        )
        self.__log_read_write_value(
            "was_indent_already_processed", self.__was_indent_already_processed
        )
        self.__log_read_write_value(
            "do_force_leaf_token_parse", self.__do_force_leaf_token_parse
        )
        self.__log_read_write_value(
            "did_indent_processing", self.__did_indent_processing
        )
        self.__log_read_write_value(
            "have_pre_processed_indent", self.__have_pre_processed_indent
        )
        self.__log_read_write_value("can_continue", self.__can_continue)
        self.__log_read_write_value(
            "do_force_list_continuation", self.__do_force_list_continuation
        )

        # Integers
        self.__log_read_write_value(
            "indent_used_by_container", self.__indent_used_by_container
        )
        self.__log_read_write_value(
            "indent_already_processed", self.__indent_already_processed
        )
        self.__log_read_write_value(
            "last_block_quote_index", self.__last_block_quote_index
        )
        self.__log_read_write_value(
            "last_list_start_index", self.__last_list_start_index
        )
        self.__log_read_write_value("start_index", self.__start_index)

        # Optional integers
        self.__log_read_write_value(
            "removed_chars_at_start_of_line", self.__removed_chars_at_start_of_line
        )

        # Strings
        self.__log_read_write_value("adj_line_to_parse", self.__adj_line_to_parse)
        self.__log_read_write_value("line_to_parse", self.__line_to_parse)

        # Optional strings
        self.__log_read_write_value("weird_adjusted_text", self.__weird_adjusted_text)
        self.__log_read_write_value("indent_used_by_list", self.__indent_used_by_list)
        self.__log_read_write_value(
            "text_removed_by_container", self.__text_removed_by_container
        )
        self.__log_read_write_value("extracted_whitespace", self.__extracted_whitespace)
        self.__log_read_write_value("adj_ws", self.__adj_ws)
        self.__log_read_write_value("bogus", self.__bogus)

        # Others
        self.__log_read_write_value("block_quote_data", self.__block_quote_data)
        self.__log_read_write_value(
            "end_container_indices", self.__end_container_indices
        )
        self.__log_read_write_value("requeue_line_info", self.__requeue_line_info)
        self.__log_read_write_value("leaf_tokens", self.__leaf_tokens)
        self.__log_read_write_value(
            "container_level_tokens", self.__container_level_tokens
        )

        # Read only values
        self.__log_read_only_value("container_depth", self.__container_depth)
        self.__log_read_only_value(
            "initial_block_quote_count", self.__initial_block_quote_count
        )
        self.__log_read_only_value("adjusted_block_index", self.__adjusted_block_index)
        self.__log_read_only_value(
            "container_start_bq_count", self.__container_start_bq_count
        )
        self.__log_read_only_value("parser_properties", self.__parser_properties)
        self.__log_read_only_value(
            "do_ignore_link_definition_start", self.__do_ignore_link_definition_start
        )
        self.__log_read_only_value(
            "do_ignore_table_start", self.__do_ignore_table_start
        )
        self.__log_read_only_value("original_line", self.__original_line)
        self.__log_read_only_value("is_para_continue", self.__is_para_continue)

    @staticmethod
    def __log_read_only_value(value_name: str, value_object: Any) -> None:
        POGGER.debug("CGB(ReadOnly): '$'=:$:", value_name, value_object)

    @staticmethod
    def __log_read_write_value(value_name: str, value_object: Any) -> None:
        POGGER.debug("CGB(ReadWrite): '$'=:$:", value_name, value_object)

    # pylint: enable=too-many-arguments
    @property
    def is_para_continue(self) -> bool:
        """
        Xxx
        """
        return self.__is_para_continue

    @property
    def original_line(self) -> str:
        """
        Get the original line that was passed to be processed.
        """
        return self.__original_line

    @property
    def container_depth(self) -> int:
        """
        Get the container depth of this pass through the line.
        """
        return self.__container_depth

    @property
    def initial_block_quote_count(self) -> Optional[int]:
        """
        Get any initial block quote informatin.
        """
        return self.__initial_block_quote_count

    @property
    def adjusted_block_index(self) -> Optional[int]:
        """
        Index of the block start.
        """
        return self.__adjusted_block_index

    @property
    def container_start_bq_count(self) -> Optional[int]:
        """
        Xxx
        """
        return self.__container_start_bq_count

    @property
    def parser_properties(self) -> ParseBlockPassProperties:
        """
        Xxx
        """
        return self.__parser_properties

    @property
    def do_ignore_link_definition_start(self) -> bool:
        """
        Xxx
        """
        return self.__do_ignore_link_definition_start

    @property
    def do_ignore_table_start(self) -> bool:
        """
        Xxx
        """
        return self.__do_ignore_table_start

    @property
    def do_force_list_continuation(self) -> bool:
        """
        Xxx
        """
        return self.__do_force_list_continuation

    @do_force_list_continuation.setter
    def do_force_list_continuation(self, value: bool) -> None:
        """
        xxx
        """
        if value != self.__do_force_list_continuation:
            self.__log_read_write_value("do_force_list_continuation", value)
        self.__do_force_list_continuation = value

    @property
    def did_blank(self) -> bool:
        """
        Xxx
        """
        return self.__did_blank

    @did_blank.setter
    def did_blank(self, value: bool) -> None:
        """
        xxx
        """
        if value != self.__did_blank:
            self.__log_read_write_value("did_blank", value)
            self.__did_blank = value

    @property
    def was_paragraph_continuation(self) -> bool:
        """
        Xxx
        """
        return self.__was_paragraph_continuation

    @was_paragraph_continuation.setter
    def was_paragraph_continuation(self, value: bool) -> None:
        """
        xxx
        """
        if value != self.__was_paragraph_continuation:
            self.__log_read_write_value("was_paragraph_continuation", value)
            self.__was_paragraph_continuation = value

    @property
    def do_skip_containers_before_leaf_blocks(self) -> bool:
        """
        Xxx
        """
        return self.__do_skip_containers_before_leaf_blocks

    @do_skip_containers_before_leaf_blocks.setter
    def do_skip_containers_before_leaf_blocks(self, value: bool) -> None:
        """
        xxx
        """
        if value != self.__do_skip_containers_before_leaf_blocks:
            self.__log_read_write_value("do_skip_containers_before_leaf_blocks", value)
            self.__do_skip_containers_before_leaf_blocks = value

    @property
    def was_indent_already_processed(self) -> bool:
        """
        Xxx
        """
        return self.__was_indent_already_processed

    @was_indent_already_processed.setter
    def was_indent_already_processed(self, value: bool) -> None:
        """
        xxx
        """
        if value != self.__was_indent_already_processed:
            self.__log_read_write_value("was_indent_already_processed", value)
            self.__was_indent_already_processed = value

    @property
    def do_force_leaf_token_parse(self) -> bool:
        """
        Xxx
        """
        return self.__do_force_leaf_token_parse

    @do_force_leaf_token_parse.setter
    def do_force_leaf_token_parse(self, value: bool) -> None:
        """
        xxx
        """
        if value != self.__do_force_leaf_token_parse:
            self.__log_read_write_value("do_force_leaf_token_parse", value)
            self.__do_force_leaf_token_parse = value

    @property
    def did_indent_processing(self) -> bool:
        """
        Xxx
        """
        return self.__did_indent_processing

    @did_indent_processing.setter
    def did_indent_processing(self, value: bool) -> None:
        """
        xxx
        """
        if value != self.__did_indent_processing:
            self.__log_read_write_value("did_indent_processing", value)
            self.__did_indent_processing = value

    @property
    def have_pre_processed_indent(self) -> bool:
        """
        Xxx
        """
        return self.__have_pre_processed_indent

    @have_pre_processed_indent.setter
    def have_pre_processed_indent(self, value: bool) -> None:
        """
        xxx
        """
        if value != self.__have_pre_processed_indent:
            self.__log_read_write_value("have_pre_processed_indent", value)
            self.__have_pre_processed_indent = value

    @property
    def can_continue(self) -> bool:
        """
        Xxx
        """
        return self.__can_continue

    @can_continue.setter
    def can_continue(self, value: bool) -> None:
        """
        xxx
        """
        if value != self.__can_continue:
            self.__log_read_write_value("can_continue", value)
            self.__can_continue = value

    @property
    def indent_used_by_container(self) -> int:
        """
        Xxx
        """
        return self.__indent_used_by_container

    @indent_used_by_container.setter
    def indent_used_by_container(self, value: int) -> None:
        """
        xxx
        """
        if value != self.__indent_used_by_container:
            self.__log_read_write_value("indent_used_by_container", value)
            self.__indent_used_by_container = value

    @property
    def indent_already_processed(self) -> int:
        """
        Xxx
        """
        return self.__indent_already_processed

    @indent_already_processed.setter
    def indent_already_processed(self, value: int) -> None:
        """
        xxx
        """
        if value != self.__indent_already_processed:
            self.__log_read_write_value("indent_already_processed", value)
            self.__indent_already_processed = value

    @property
    def last_block_quote_index(self) -> int:
        """
        Xxx
        """
        return self.__last_block_quote_index

    @last_block_quote_index.setter
    def last_block_quote_index(self, value: int) -> None:
        """
        xxx
        """
        if value != self.__last_block_quote_index:
            self.__log_read_write_value("last_block_quote_index", value)
            self.__last_block_quote_index = value

    @property
    def last_list_start_index(self) -> int:
        """
        Xxx
        """
        return self.__last_list_start_index

    @last_list_start_index.setter
    def last_list_start_index(self, value: int) -> None:
        """
        xxx
        """
        if value != self.__last_list_start_index:
            self.__log_read_write_value("last_list_start_index", value)
            self.__last_list_start_index = value

    @property
    def start_index(self) -> int:
        """
        Xxx
        """
        return self.__start_index

    @start_index.setter
    def start_index(self, value: int) -> None:
        """
        xxx
        """
        if value != self.__start_index:
            self.__log_read_write_value("start_index", value)
            self.__start_index = value

    @property
    def line_to_parse(self) -> str:
        """
        Xxx
        """
        return self.__line_to_parse

    @line_to_parse.setter
    def line_to_parse(self, value: str) -> None:
        """
        xxx
        """
        if value != self.__line_to_parse:
            self.__log_read_write_value("line_to_parse", value)
            self.__line_to_parse = value

    @property
    def adj_line_to_parse(self) -> str:
        """
        Xxx
        """
        return self.__adj_line_to_parse

    @adj_line_to_parse.setter
    def adj_line_to_parse(self, value: str) -> None:
        """
        xxx
        """
        if value != self.__adj_line_to_parse:
            self.__log_read_write_value("adj_line_to_parse", value)
            self.__adj_line_to_parse = value

    @property
    def weird_adjusted_text(self) -> Optional[str]:
        """
        Xxx
        """
        return self.__weird_adjusted_text

    @weird_adjusted_text.setter
    def weird_adjusted_text(self, value: Optional[str]) -> None:
        """
        xxx
        """
        if value != self.__weird_adjusted_text:
            self.__log_read_write_value("weird_adjusted_text", value)
            self.__weird_adjusted_text = value

    @property
    def indent_used_by_list(self) -> Optional[str]:
        """
        Xxx
        """
        return self.__indent_used_by_list

    @indent_used_by_list.setter
    def indent_used_by_list(self, value: Optional[str]) -> None:
        """
        xxx
        """
        if value != self.__indent_used_by_list:
            self.__log_read_write_value("indent_used_by_list", value)
            self.__indent_used_by_list = value

    @property
    def text_removed_by_container(self) -> Optional[str]:
        """
        Xxx
        """
        return self.__text_removed_by_container

    @text_removed_by_container.setter
    def text_removed_by_container(self, value: Optional[str]) -> None:
        """
        xxx
        """
        if value != self.__text_removed_by_container:
            self.__log_read_write_value("text_removed_by_container", value)
            self.__text_removed_by_container = value

    @property
    def extracted_whitespace(self) -> Optional[str]:
        """
        Xxx
        """
        return self.__extracted_whitespace

    @extracted_whitespace.setter
    def extracted_whitespace(self, value: Optional[str]) -> None:
        """
        xxx
        """
        if value != self.__extracted_whitespace:
            self.__log_read_write_value("extracted_whitespace", value)
            self.__extracted_whitespace = value

    @property
    def adj_ws(self) -> Optional[str]:
        """
        Xxx
        """
        return self.__adj_ws

    @adj_ws.setter
    def adj_ws(self, value: Optional[str]) -> None:
        """
        xxx
        """
        if value != self.__adj_ws:
            self.__log_read_write_value("adj_ws", value)
            self.__adj_ws = value

    @property
    def bogus(self) -> Optional[str]:
        """
        Xxx
        """
        return self.__bogus

    @bogus.setter
    def bogus(self, value: Optional[str]) -> None:
        """
        xxx
        """
        if value != self.__bogus:
            self.__log_read_write_value("bogus", value)
            self.__bogus = value

    @property
    def removed_chars_at_start_of_line(self) -> Optional[int]:
        """
        Xxx
        """
        return self.__removed_chars_at_start_of_line

    @removed_chars_at_start_of_line.setter
    def removed_chars_at_start_of_line(self, value: Optional[int]) -> None:
        """
        xxx
        """
        if value != self.__removed_chars_at_start_of_line:
            self.__log_read_write_value("removed_chars_at_start_of_line", value)
            self.__removed_chars_at_start_of_line = value

    @property
    def block_quote_data(self) -> BlockQuoteData:
        """
        Xxx
        """
        return self.__block_quote_data

    @block_quote_data.setter
    def block_quote_data(self, value: BlockQuoteData) -> None:
        """
        xxx
        """
        if value != self.__block_quote_data:
            self.__log_read_write_value("block_quote_data", value)
            self.__block_quote_data = value

    @property
    def end_container_indices(self) -> ContainerIndices:
        """
        Xxx
        """
        return self.__end_container_indices

    @end_container_indices.setter
    def end_container_indices(self, value: ContainerIndices) -> None:
        """
        xxx
        """
        if value != self.__end_container_indices:
            self.__log_read_write_value("end_container_indices", value)
            self.__end_container_indices = value

    @property
    def requeue_line_info(self) -> Optional[RequeueLineInfo]:
        """
        Xxx
        """
        return self.__requeue_line_info

    @requeue_line_info.setter
    def requeue_line_info(self, value: RequeueLineInfo) -> None:
        """
        xxx
        """
        if value != self.__requeue_line_info:
            self.__log_read_write_value("requeue_line_info", value)
            self.__requeue_line_info = value

    @property
    def current_container_blocks(self) -> List[StackToken]:
        """
        Xxx
        """
        return self.__current_container_blocks

    @current_container_blocks.setter
    def current_container_blocks(self, value: List[StackToken]) -> None:
        """
        xxx
        """
        if value != self.__current_container_blocks:
            self.__log_read_write_value("current_container_blocks", value)
            self.__current_container_blocks = value

    def get_recurse_fn(
        self,
    ) -> ParseForContainerBlocksProtocol:
        """
        xxx
        """
        return self.__recurse_fn

    def is_leaf_tokens_empty(self) -> bool:
        """
        xxx
        """
        return not self.__leaf_tokens

    def extend_leaf_tokens(self, tokens_to_append: List[MarkdownToken]) -> None:
        """
        xxx
        """
        self.__leaf_tokens.extend(tokens_to_append)
        self.__log_read_write_value("leaf_tokens", self.__leaf_tokens)

    def clear_container_tokens(self) -> None:
        """
        xxx
        """
        self.__container_level_tokens.clear()
        self.__log_read_write_value(
            "container_level_tokens", self.__container_level_tokens
        )

    def extend_container_tokens(self, tokens_to_append: List[MarkdownToken]) -> None:
        """
        xxx
        """
        self.__container_level_tokens.extend(tokens_to_append)
        self.__log_read_write_value(
            "container_level_tokens", self.__container_level_tokens
        )

    def extend_container_tokens_with_leaf_tokens(self) -> None:
        """
        xxx
        """
        self.extend_container_tokens(self.__leaf_tokens)
        self.__leaf_tokens.clear()

    @property
    def container_tokens(self) -> List[MarkdownToken]:
        """
        Xxx
        """
        return self.__container_level_tokens

    @property
    def leaf_tokens(self) -> List[MarkdownToken]:
        """
        Xxx
        """
        return self.__leaf_tokens


# pylint: enable=too-many-public-methods
# pylint: enable=too-many-instance-attributes
