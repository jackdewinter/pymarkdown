"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different, assert_token_consistency


@pytest.mark.skip
def test_strikethrough_491():
    """
    Test case 491:  Strikethrough text is any text wrapped in two tildes (~).
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """~~Hi~~ Hello, world!"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)


def test_strikethrough_492():
    """
    Test case 492:  As with regular emphasis delimiters, a new paragraph will cause strikethrough parsing to cease:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """This ~~has a

new paragraph~~."""
    expected_tokens = [
        "[para(1,1):]",
        "[text:This ~~has a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:new paragraph~~.:]",
        "[end-para:::True]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)
