from test.tokens.mock_plugin_modify_context import MockPluginModifyContext

from pymarkdown.links.link_helper_properties import LinkHelperProperties
from pymarkdown.tokens.link_start_markdown_token import LinkStartMarkdownToken


def test_reference_markdown_token_modify_with_bad_name() -> None:
    """
    Test to make sure that try to change this token with a bad name fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    lhp = LinkHelperProperties()

    lhp.ex_label = "c"
    lhp.label_type = "inline"
    lhp.before_link_whitespace = " "
    lhp.inline_link = "b"
    lhp.pre_inline_link = "b"
    lhp.before_title_whitespace = " "
    lhp.bounding_character = "<"
    lhp.inline_title = "a"
    lhp.pre_inline_title = "a"
    lhp.after_title_whitespace = " "
    lhp.did_use_angle_start = False

    original_token = LinkStartMarkdownToken(
        text_from_blocks="raw",
        line_number=1,
        column_number=1,
        lhp=lhp,
    )

    # Act
    did_modify = original_token.modify_token(modification_context, "bad_name", "")

    # Assert
    assert not did_modify
