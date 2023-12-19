from test.tokens.mock_plugin_modify_context import MockPluginModifyContext

from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.thematic_break_markdown_token import ThematicBreakMarkdownToken


def test_text_markdown_token_modify_with_bad_name():
    """
    Test to make sure that try to change this token with a bad name fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = ThematicBreakMarkdownToken(
        start_character="*",
        extracted_whitespace="",
        rest_of_line="***",
        position_marker=PositionMarker(1, 1, 1),
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "bad_name", "")

    # Assert
    assert not did_modify
