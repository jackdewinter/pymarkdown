"""
Tests for the ContainerGrabBag class.
"""

from typing import List, Optional, Tuple, cast

from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag
from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.extension_manager.extension_manager import ExtensionManager
from pymarkdown.extension_manager.parser_extension import ParserExtension
from pymarkdown.general.parser_state import ParserState
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.requeue_line_info import RequeueLineInfo
from pymarkdown.tokens.markdown_token import MarkdownToken


class Bob:

    class Reober:
        def is_front_matter_enabled(self) -> bool:
            return False

        def is_linter_pragmas_enabled(self) -> bool:
            return False

        def is_disallow_raw_html_enabled(self) -> bool:
            return False

        def is_task_list_items_enabled(self) -> bool:
            return False

        def is_strike_through_enabled(self) -> bool:
            return False

        def is_extended_autolinks_enabled(self) -> bool:
            return False

        def is_tables_enabled(self) -> bool:
            return False

        def get_extension_instance(self, extension_id: str) -> ParserExtension:
            return cast(ParserExtension, None)

    parse_block_pass_properties = ParseBlockPassProperties(
        cast(ExtensionManager, Reober())
    )

    def __init__(self) -> None:
        self.parser_state = ParserState(
            [],
            [],
            Bob.close_open_blocks,
            Bob.blank_line_function,
            Bob.parse_block_pass_properties,
        )

    @staticmethod
    def blank_line_function(
        parser_state: ParserState,
        input_line: str,
        from_main_transform: bool,
        position_marker: Optional[PositionMarker] = None,
    ) -> Tuple[Optional[List[MarkdownToken]], Optional[RequeueLineInfo]]:
        return None, None

    @staticmethod
    def close_open_blocks(  # noqa: C901
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
        return [], None

    def recurse_function(
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
    ]:
        return [], None, None, None, False, False


def test_initial_do_force_leaf_token_parse() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    initial_value = container_grab_bag.do_force_leaf_token_parse

    # Assert
    assert not initial_value


def test_change_do_force_leaf_token_parse_set_different() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.do_force_leaf_token_parse = True
    new_value = container_grab_bag.do_force_leaf_token_parse

    # Assert
    assert new_value


def test_change_do_force_leaf_token_parse_set_same() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.do_force_leaf_token_parse = False
    new_value = container_grab_bag.do_force_leaf_token_parse

    # Assert
    assert not new_value


def test_initial_did_indent_processing() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    initial_value = container_grab_bag.did_indent_processing

    # Assert
    assert not initial_value


def test_change_did_indent_processing_set_different() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.did_indent_processing = True
    new_value = container_grab_bag.did_indent_processing

    # Assert
    assert new_value


def test_change_did_indent_processing_set_same() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.did_indent_processing = False
    new_value = container_grab_bag.did_indent_processing

    # Assert
    assert not new_value


def test_initial_indent_used_by_container() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    initial_value = container_grab_bag.indent_used_by_container

    # Assert
    assert initial_value == -1


def test_change_indent_used_by_container_set_different() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.indent_used_by_container = 0
    new_value = container_grab_bag.indent_used_by_container

    # Assert
    assert new_value == 0


def test_change_indent_used_by_container_set_same() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.indent_used_by_container = -1
    new_value = container_grab_bag.indent_used_by_container

    # Assert
    assert new_value == -1


def test_initial_indent_already_processed() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    initial_value = container_grab_bag.indent_already_processed

    # Assert
    assert initial_value == -1


def test_change_indent_already_processed_set_different() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.indent_already_processed = 0
    new_value = container_grab_bag.indent_already_processed

    # Assert
    assert new_value == 0


def test_change_indent_already_processed_set_same() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.indent_already_processed = -1
    new_value = container_grab_bag.indent_already_processed

    # Assert
    assert new_value == -1


def test_initial_weird_adjusted_text() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    initial_value = container_grab_bag.weird_adjusted_text

    # Assert
    assert initial_value is None


def test_change_weird_adjusted_text_set_different() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.weird_adjusted_text = "text"
    new_value = container_grab_bag.weird_adjusted_text

    # Assert
    assert new_value is not None


def test_change_weird_adjusted_text_set_same() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.weird_adjusted_text = None
    new_value = container_grab_bag.weird_adjusted_text

    # Assert
    assert new_value is None


def test_initial_adj_line_to_parse() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    initial_value = container_grab_bag.adj_line_to_parse

    # Assert
    assert initial_value == ""


def test_change_adj_line_to_parse_set_different() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.adj_line_to_parse = "text"
    new_value = container_grab_bag.adj_line_to_parse

    # Assert
    assert new_value == "text"


def test_change_adj_line_to_parse_set_same() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.adj_line_to_parse = ""
    new_value = container_grab_bag.adj_line_to_parse

    # Assert
    assert not new_value


def test_initial_last_list_start_index() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    initial_value = container_grab_bag.last_list_start_index

    # Assert
    assert initial_value == -1


def test_change_last_list_start_index_set_different() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.last_list_start_index = 0
    new_value = container_grab_bag.last_list_start_index

    # Assert
    assert new_value == 0


def test_change_last_list_start_index_set_same() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.last_list_start_index = -1
    new_value = container_grab_bag.last_list_start_index

    # Assert
    assert new_value == -1


def test_initial_last_block_quote_index() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    initial_value = container_grab_bag.last_block_quote_index

    # Assert
    assert initial_value == -1


def test_change_last_block_quote_index_set_different() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.last_block_quote_index = 0
    new_value = container_grab_bag.last_block_quote_index

    # Assert
    assert new_value == 0


def test_change_last_block_quote_index_set_same() -> None:
    """
    xxx
    """

    # Arrange
    bob = Bob()
    container_grab_bag = ContainerGrabBag(
        bob.parser_state,
        0,
        None,
        None,
        0,
        bob.parse_block_pass_properties,
        False,
        False,
        "",
        bob.recurse_function,
    )

    # Act
    container_grab_bag.last_block_quote_index = -1
    new_value = container_grab_bag.last_block_quote_index

    # Assert
    assert new_value == -1
