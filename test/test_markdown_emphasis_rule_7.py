"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_emphasis_400():
    """
    Test case 400:  Rule 7: This is not strong emphasis, because the closing delimiter is preceded by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**foo bar **"""
    expected_tokens = [
        "[para:]",
        "[text:**:]",
        "[text:foo bar :]",
        "[text:**:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_401():
    """
    Test case 401:  This is not strong emphasis, because the second ** is preceded by punctuation and followed by an alphanumeric:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**(**foo)"""
    expected_tokens = [
        "[para:]",
        "[text:**:]",
        "[text:(:]",
        "[text:**:]",
        "[text:foo):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_402():
    """
    Test case 402:  (part 1) The point of this restriction is more easily appreciated with these examples
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*(**foo**)*"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_403():
    """
    Test case 403:  (part 2) The point of this restriction is more easily appreciated with these examples
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**Gomphocarpus (*Gomphocarpus physocarpus*, syn.
*Asclepias physocarpa*)**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_404():
    """
    Test case 404:  (part 3) The point of this restriction is more easily appreciated with these examples
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**foo "*bar*" foo**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_405():
    """
    Test case 405:  Intraword emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**foo**bar"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
