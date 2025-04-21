"""
Tests for the ContainerGrabBag class.
"""

from pymarkdown.container_blocks.container_grab_bag import ContainerGrabBag


def test_initial_do_force_leaf_token_parse():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    initial_value = container_grab_bag.do_force_leaf_token_parse

    # Assert
    assert not initial_value


def test_change_do_force_leaf_token_parse_set_different():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.do_force_leaf_token_parse = True
    new_value = container_grab_bag.do_force_leaf_token_parse

    # Assert
    assert new_value


def test_change_do_force_leaf_token_parse_set_same():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.do_force_leaf_token_parse = False
    new_value = container_grab_bag.do_force_leaf_token_parse

    # Assert
    assert not new_value


def test_initial_did_indent_processing():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    initial_value = container_grab_bag.did_indent_processing

    # Assert
    assert not initial_value


def test_change_did_indent_processing_set_different():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.did_indent_processing = True
    new_value = container_grab_bag.did_indent_processing

    # Assert
    assert new_value


def test_change_did_indent_processing_set_same():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.did_indent_processing = False
    new_value = container_grab_bag.did_indent_processing

    # Assert
    assert not new_value


def test_initial_indent_used_by_container():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    initial_value = container_grab_bag.indent_used_by_container

    # Assert
    assert initial_value == -1


def test_change_indent_used_by_container_set_different():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.indent_used_by_container = 0
    new_value = container_grab_bag.indent_used_by_container

    # Assert
    assert new_value == 0


def test_change_indent_used_by_container_set_same():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.indent_used_by_container = -1
    new_value = container_grab_bag.indent_used_by_container

    # Assert
    assert new_value == -1


def test_initial_indent_already_processed():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    initial_value = container_grab_bag.indent_already_processed

    # Assert
    assert initial_value == -1


def test_change_indent_already_processed_set_different():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.indent_already_processed = 0
    new_value = container_grab_bag.indent_already_processed

    # Assert
    assert new_value == 0


def test_change_indent_already_processed_set_same():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.indent_already_processed = -1
    new_value = container_grab_bag.indent_already_processed

    # Assert
    assert new_value == -1


def test_initial_weird_adjusted_text():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    initial_value = container_grab_bag.weird_adjusted_text

    # Assert
    assert initial_value is None


def test_change_weird_adjusted_text_set_different():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.weird_adjusted_text = "text"
    new_value = container_grab_bag.weird_adjusted_text

    # Assert
    assert new_value is not None


def test_change_weird_adjusted_text_set_same():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.weird_adjusted_text = None
    new_value = container_grab_bag.weird_adjusted_text

    # Assert
    assert new_value is None


def test_initial_adj_line_to_parse():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    initial_value = container_grab_bag.adj_line_to_parse

    # Assert
    assert initial_value == ""


def test_change_adj_line_to_parse_set_different():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.adj_line_to_parse = "text"
    new_value = container_grab_bag.adj_line_to_parse

    # Assert
    assert new_value == "text"


def test_change_adj_line_to_parse_set_same():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.adj_line_to_parse = ""
    new_value = container_grab_bag.adj_line_to_parse

    # Assert
    assert not new_value


def test_initial_last_list_start_index():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    initial_value = container_grab_bag.last_list_start_index

    # Assert
    assert initial_value == -1


def test_change_last_list_start_index_set_different():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.last_list_start_index = 0
    new_value = container_grab_bag.last_list_start_index

    # Assert
    assert new_value == 0


def test_change_last_list_start_index_set_same():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.last_list_start_index = -1
    new_value = container_grab_bag.last_list_start_index

    # Assert
    assert new_value == -1


def test_initial_last_block_quote_index():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    initial_value = container_grab_bag.last_block_quote_index

    # Assert
    assert initial_value == -1


def test_change_last_block_quote_index_set_different():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.last_block_quote_index = 0
    new_value = container_grab_bag.last_block_quote_index

    # Assert
    assert new_value == 0


def test_change_last_block_quote_index_set_same():
    """
    xxx
    """

    # Arrange
    container_grab_bag = ContainerGrabBag(
        None, None, None, None, None, None, None, None, None, None
    )

    # Act
    container_grab_bag.last_block_quote_index = -1
    new_value = container_grab_bag.last_block_quote_index

    # Assert
    assert new_value == -1
