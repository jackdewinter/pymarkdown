"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
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
def test_emphasis_360():
    """
    Test case 360:  Rule 1:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo bar*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1:*]",
        "[text:foo bar:]",
        "[end-emphasis::1:*]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo bar</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_361():
    """
    Test case 361:  This is not emphasis, because the opening * is followed by whitespace, and hence not part of a left-flanking delimiter run:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a * foo bar*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:a :]",
        "[text:*:]",
        "[text: foo bar:]",
        "[text:*:]",
        "[end-para]",
    ]
    expected_gfm = """<p>a * foo bar*</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_362():
    """
    Test case 362:  This is not emphasis, because the opening * is preceded by an alphanumeric and followed by punctuation, and hence not part of a left-flanking delimiter run:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a*"foo"*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:a:]",
        "[text:*:]",
        '[text:\a"\a&quot;\afoo\a"\a&quot;\a:]',
        "[text:*:]",
        "[end-para]",
    ]
    expected_gfm = """<p>a*&quot;foo&quot;*</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_363():
    """
    Test case 363:  Unicode nonbreaking spaces count as whitespace, too:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*\u00A0a\u00A0*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:*:]",
        "[text:\u00A0a\u00A0:]",
        "[text:*:]",
        "[end-para]",
    ]
    expected_gfm = """<p>*\u00A0a\u00A0*</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_364():
    """
    Test case 364:  (part 1) Intraword emphasis with * is permitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo*bar*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo:]",
        "[emphasis:1:*]",
        "[text:bar:]",
        "[end-emphasis::1:*]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo<em>bar</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_365():
    """
    Test case 365:  (part 2) Intraword emphasis with * is permitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """5*6*78"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:5:]",
        "[emphasis:1:*]",
        "[text:6:]",
        "[end-emphasis::1:*]",
        "[text:78:]",
        "[end-para]",
    ]
    expected_gfm = """<p>5<em>6</em>78</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
