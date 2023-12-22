from test.tokens.mock_plugin_modify_context import MockPluginModifyContext

from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.markdown_token import EndMarkdownToken
from pymarkdown.tokens.new_list_item_markdown_token import NewListItemMarkdownToken


def test_fenced_code_block_markdown_token_modify_with_bad_name():
    """
    Test to make sure that try to change this token with a bad name fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    start_token = NewListItemMarkdownToken(
        indent_level=4,
        position_marker=PositionMarker(1, 1, 1),
        extracted_whitespace="",
        list_start_content="1",
    )
    original_token = EndMarkdownToken(
        type_name="bob",
        extracted_whitespace="",
        extra_end_data=None,
        start_markdown_token=start_token,
        was_forced=False,
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "bad_name", "")

    # Assert
    assert not did_modify
