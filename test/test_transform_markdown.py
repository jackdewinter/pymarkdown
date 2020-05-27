"""
Test the top level transform functions.
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

# pylint: disable=relative-beyond-top-level
from .utils import assert_if_lists_different


def test_transform_with_debug_on():
    """
    Copy of test case 012 to test with debug logging.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- `one
- two`"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:`one:]",
        "[end-para]",
        "[li(2,1):2]",
        "[para(2,3):]",
        "[text:two`:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown, show_debug=True)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_transform_with_debug_off():
    """
    Copy of test case 012 to test with debug logging off.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- `one
- two`"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:`one:]",
        "[end-para]",
        "[li(2,1):2]",
        "[para(2,3):]",
        "[text:two`:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown, show_debug=False)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


# pylint: enable=relative-beyond-top-level
