from test.tokens.mock_plugin_modify_context import MockPluginModifyContext

from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken


def test_block_quote_markdown_token_modify_with_bad_name():
    """
    Test to make sure that try to change this token with a bad name fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = BlockQuoteMarkdownToken(
        position_marker=PositionMarker(1, 1, 1),
        extracted_whitespace="",
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "bad_name", "")

    # Assert
    assert not did_modify
