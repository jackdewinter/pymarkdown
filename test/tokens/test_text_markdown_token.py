from test.tokens.mock_plugin_modify_context import MockPluginModifyContext

from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


def test_text_markdown_token_modify_with_bad_name():
    """
    Test to make sure that try to change this token with a bad name fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = TextMarkdownToken(
        token_text="bob",
        extracted_whitespace="",
        line_number=1,
        column_number=1,
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "bad_name", "")

    # Assert
    assert not did_modify
