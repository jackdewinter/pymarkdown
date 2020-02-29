"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


@pytest.mark.skip
def test_emphasis_360():
    """
    Test case 360:  Rule 1:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo bar*"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_361():
    """
    Test case 361:  This is not emphasis, because the opening * is followed by whitespace, and hence not part of a left-flanking delimiter run:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """a * foo bar*"""
    expected_tokens = ["[para:]", "[text:a * foo bar*:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_362():
    """
    Test case 362:  This is not emphasis, because the opening * is preceded by an alphanumeric and followed by punctuation, and hence not part of a left-flanking delimiter run:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """a*"foo"*"""
    expected_tokens = ["[para:]", "[text:a*&quot;foo&quot;*:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_363():
    """
    Test case 363:  Unicode nonbreaking spaces count as whitespace, too:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*\u00A0a\u00A0*"""
    expected_tokens = ["[para:]", "[text:*\u00A0a\u00A0*:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_364():
    """
    Test case 364:  (part 1) Intraword emphasis with * is permitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo*bar*"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_365():
    """
    Test case 365:  (part 2) Intraword emphasis with * is permitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """5*6*78"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
