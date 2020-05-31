"""
https://github.github.com/gfm/#textual-content
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
def test_textual_content_671():
    """
    Test case 671:  (part 1) Any characters not given an interpretation by the above rules will be parsed as plain textual content.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """hello $.;'there"""
    expected_tokens = ["[para(1,1):]", "[text:hello $.;'there:]", "[end-para]"]
    expected_gfm = """<p>hello $.;'there</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_textual_content_672():
    """
    Test case 672:  (part 2) Any characters not given an interpretation by the above rules will be parsed as plain textual content.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo χρῆν"""
    expected_tokens = ["[para(1,1):]", "[text:Foo χρῆν:]", "[end-para]"]
    expected_gfm = """<p>Foo χρῆν</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_textual_content_673():
    """
    Test case 673:  Internal spaces are preserved verbatim:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Multiple     spaces"""
    expected_tokens = ["[para(1,1):]", "[text:Multiple     spaces:]", "[end-para]"]
    expected_gfm = """<p>Multiple     spaces</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
