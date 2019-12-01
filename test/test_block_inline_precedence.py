"""
https://github.github.com/gfm/#precedence
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_block_inline_precedence_012():
    """
    Test case 012:  Indicators of block structure always take precedence over indicators of inline structure.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- `one
- two`"""
    expected_tokens = ["[para:]", "[text:- `one:]", "[text:- two`:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when lists are implemented
    # TODO Expect this to fail when inline code blocks implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
