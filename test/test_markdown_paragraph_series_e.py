"""
https://github.github.com/gfm/#paragraph
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
def test_paragraph_series_e_cs():
    """
    Test case:  Paragraph with code span with newline inside
    was:        test_paragraph_extra_43
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a`code
span`a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[icode-span(1,2):code\a\n\a \aspan:`::]",
        "[text(2,6):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<code>code span</code>a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_e_rh():
    """
    Test case:  Paragraph with raw HTML with newline inside
    was:        test_paragraph_extra_44
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a<raw
html='cool'>a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[raw-html(1,2):raw\nhtml='cool']",
        "[text(2,13):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<raw\nhtml='cool'>a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_e_ua():
    """
    Test case:  Paragraph with URI autolink with newline inside, renders invalid
    was:        test_paragraph_extra_45
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a<http://www.\ngoogle.com>a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a\a<\a&lt;\ahttp://www.\ngoogle.com\a>\a&gt;\aa::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a&lt;http://www.\ngoogle.com&gt;a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_e_ea():
    """
    Test case:  Paragraph with email autolink with newline inside, renders invalid
    was:        test_paragraph_extra_46
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a<foo@bar\n.com>a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a\a<\a&lt;\afoo@bar\n.com\a>\a&gt;\aa::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a&lt;foo@bar\n.com&gt;a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_e_em():
    """
    Test case:  Paragraph with emphasis with newline inside
    was:        test_paragraph_extra_46b
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a*foo\nbar*a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):foo\nbar::\n]",
        "[end-emphasis(2,4)::1:*:False]",
        "[text(2,5):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<em>foo\nbar</em>a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
