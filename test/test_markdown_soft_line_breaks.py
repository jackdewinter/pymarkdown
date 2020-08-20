"""
https://github.github.com/gfm/#soft-line-breaks
"""

import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)


@pytest.mark.gfm
def test_soft_line_breaks_669():
    """
    Test case 669:  A regular line break (not in a code span or HTML tag) that is not preceded by two or more spaces or a backslash is parsed as a softbreak.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo
baz"""
    expected_tokens = ["[para(1,1):\n]", "[text:foo\nbaz::\n]", "[end-para:::True]"]
    expected_gfm = """<p>foo
baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_soft_line_breaks_670():
    """
    Test case 670:  Spaces at the end of the line and beginning of the next line are removed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo\a
 baz""".replace(
        "\a", " "
    )
    expected_tokens = ["[para(1,1):\n ]", "[text:foo\nbaz:: \n]", "[end-para:::True]"]
    expected_gfm = """<p>foo
baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
