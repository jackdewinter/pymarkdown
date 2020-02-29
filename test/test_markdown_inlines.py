"""
https://github.github.com/gfm/#inlines
"""

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_inlines_307():
    """
    Test case 307:  Thus, for example, in
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`hi`lo`"""
    expected_tokens = ["[para:]", "[icode-span:hi]", "[text:lo`:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
