"""
https://github.github.com/gfm/#soft-line-breaks
"""

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_soft_line_breaks_669():
    """
    Test case 669:  A regular line break (not in a code span or HTML tag) that is not preceded by two or more spaces or a backslash is parsed as a softbreak.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo
baz"""
    expected_tokens = ['[para:\n]', "[text:foo\nbaz::\n]", '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_soft_line_breaks_670():
    """
    Test case 670:  Spaces at the end of the line and beginning of the next line are removed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo\a
 baz""".replace("\a", " ")
    expected_tokens = ['[para:\n ]', "[text:foo\nbaz:: \n]", '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
