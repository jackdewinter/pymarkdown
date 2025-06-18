from test.tokens.mock_plugin_modify_context import MockPluginModifyContext

from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken


def test_reference_markdown_token_modify_with_bad_name() -> None:
    """
    Test to make sure that try to change this token with a bad name fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = ListStartMarkdownToken(
        token_name="bob",
        position_marker=PositionMarker(1, 1, "", 1),
        list_start_sequence=")",
        list_start_content="1",
        indent_level=4,
        tabbed_adjust=-1,
        extracted_whitespace="",
        tabbed_whitespace_to_add=None,
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "bad_name", "")

    # Assert
    assert not did_modify
