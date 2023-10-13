from test.tokens.mock_plugin_modify_context import MockPluginModifyContext
from test.utils import assert_that_exception_is_raised

from pymarkdown.plugin_manager.bad_plugin_fix_error import BadPluginFixError
from pymarkdown.tokens.markdown_token import MarkdownToken, MarkdownTokenClass


class __NotSupportedToken(MarkdownToken):
    """
    Token that is not supported and for testing purposes only.
    """

    def __init__(self) -> None:
        MarkdownToken.__init__(
            self,
            "unsupported",
            MarkdownTokenClass.SPECIAL,
        )


def test_modify_markdown_token_no_modify_method():
    """
    Test to make sure that try to change this token with a bad name fails.
    """

    # Arrange
    modification_context = MockPluginModifyContext()
    original_token = __NotSupportedToken()

    # Act
    did_modify = original_token.modify_token(
        modification_context, "some_name", "some_value"
    )

    # Assert
    assert not did_modify


def test_modify_markdown_token_not_in_fix_mode():
    """
    Test to make sure that try to change this token while not reporting that we are in fix mode.
    """

    # Arrange
    modification_context = MockPluginModifyContext(in_fix_mode=False)
    original_token = __NotSupportedToken()
    expected_output = "Token 'unsupported' can only be modified in fix mode."

    # Act & Assert
    assert_that_exception_is_raised(
        BadPluginFixError,
        expected_output,
        original_token.modify_token,
        modification_context,
        "some_name",
        "some_value",
    )


def test_modify_markdown_token_not_in_fix_mode_during_line_pass():
    """
    Test to make sure that try to change this token while reporting that we are in fix mode, but not in token fix mode.
    """

    # Arrange
    modification_context = MockPluginModifyContext(
        in_fix_mode=True, is_during_line_pass=True
    )
    original_token = __NotSupportedToken()

    expected_output = (
        "Token 'unsupported' can only be modified during the token pass in fix mode."
    )

    # Act & Assert
    assert_that_exception_is_raised(
        BadPluginFixError,
        expected_output,
        original_token.modify_token,
        modification_context,
        "some_name",
        "some_value",
    )
