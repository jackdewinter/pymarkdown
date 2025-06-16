from test.tokens.mock_plugin_modify_context import MockPluginModifyContext

from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken


def test_atx_heading_markdown_token_modify_with_bad_name() -> None:
    """
    Test to make sure that try to change this token with a bad name fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = AtxHeadingMarkdownToken(
        hash_count=3,
        remove_trailing_count=2,
        extracted_whitespace="",
        position_marker=PositionMarker(1, 1, "", 1),
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "bad_name", "")

    # Assert
    assert not did_modify
    assert original_token.hash_count == 3
    assert original_token.remove_trailing_count == 2
    assert original_token.extracted_whitespace == ""


def test_atx_heading_markdown_token_modify_with_bad_hash_count_value_type() -> None:
    """
    Test to make sure that try to change this token with a bad hash_count value type fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = AtxHeadingMarkdownToken(
        hash_count=3,
        remove_trailing_count=2,
        extracted_whitespace="",
        position_marker=PositionMarker(1, 1, "", 1),
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "hash_count", "fred")

    # Assert
    assert not did_modify
    assert original_token.hash_count == 3
    assert original_token.remove_trailing_count == 2
    assert original_token.extracted_whitespace == ""


def test_atx_heading_markdown_token_modify_with_bad_low_hash_count_value() -> None:
    """
    Test to make sure that try to change this token with a low hash_count value fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = AtxHeadingMarkdownToken(
        hash_count=3,
        remove_trailing_count=2,
        extracted_whitespace="",
        position_marker=PositionMarker(1, 1, "", 1),
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "hash_count", 0)

    # Assert
    assert not did_modify
    assert original_token.hash_count == 3
    assert original_token.remove_trailing_count == 2
    assert original_token.extracted_whitespace == ""


def test_atx_heading_markdown_token_modify_with_bad_high_hash_count_value() -> None:
    """
    Test to make sure that try to change this token with a high hash_count value fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = AtxHeadingMarkdownToken(
        hash_count=3,
        remove_trailing_count=2,
        extracted_whitespace="",
        position_marker=PositionMarker(1, 1, "", 1),
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "hash_count", 7)

    # Assert
    assert not did_modify
    assert original_token.hash_count == 3
    assert original_token.remove_trailing_count == 2
    assert original_token.extracted_whitespace == ""


def test_atx_heading_markdown_token_modify_with_good_high_hash_count_value() -> None:
    """
    Test to make sure that try to change this token with a good hash_count value succeeds.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = AtxHeadingMarkdownToken(
        hash_count=3,
        remove_trailing_count=2,
        extracted_whitespace="",
        position_marker=PositionMarker(1, 1, "", 1),
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "hash_count", 1)

    # Assert
    assert did_modify
    assert original_token.hash_count == 1
    assert original_token.remove_trailing_count == 2
    assert original_token.extracted_whitespace == ""
