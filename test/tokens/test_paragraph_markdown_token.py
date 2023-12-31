from test.tokens.mock_plugin_modify_context import MockPluginModifyContext

from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken


def test_paragraph_markdown_token_modify_with_bad_name():
    """
    Test to make sure that try to change this token with a bad name fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = ParagraphMarkdownToken(
        extracted_whitespace="", position_marker=PositionMarker(0, 0, "")
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "bad_name", "")

    # Assert
    assert not did_modify
