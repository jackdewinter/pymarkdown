from test.tokens.mock_plugin_modify_context import MockPluginModifyContext

from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.fenced_code_block_markdown_token import (
    FencedCodeBlockMarkdownToken,
)


def test_fenced_code_block_markdown_token_modify_with_bad_name() -> None:
    """
    Test to make sure that try to change this token with a bad name fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = FencedCodeBlockMarkdownToken(
        fence_character="~",
        fence_count=3,
        extracted_text="python",
        pre_extracted_text="bob",
        text_after_extracted_text="",
        pre_text_after_extracted_text="",
        extracted_whitespace="",
        extracted_whitespace_before_info_string=" ",
        position_marker=PositionMarker(1, 1, "", 1),
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "bad_name", "")

    # Assert
    assert not did_modify
