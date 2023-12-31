from test.tokens.mock_plugin_modify_context import MockPluginModifyContext

from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken


def test_raw_html_markdown_token_modify_with_bad_name():
    """
    Test to make sure that try to change this token with a bad name fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = RawHtmlMarkdownToken(raw_tag="", line_number=0, column_number=0)

    # Act
    did_modify = original_token.modify_token(modification_context, "bad_name", "")

    # Assert
    assert not did_modify
