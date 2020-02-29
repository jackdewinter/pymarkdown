"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


@pytest.mark.skip
def test_emphasis_387():
    """
    Test case 387:  Rule 5:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**foo bar**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_388():
    """
    Test case 388:  This is not strong emphasis, because the opening delimiter is followed by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """** foo bar**"""
    expected_tokens = ["[para:]", "[text:** foo bar**:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_389():
    """
    Test case 389:  This is not strong emphasis, because the opening ** is preceded by an alphanumeric and followed by punctuation, and hence not part of a left-flanking delimiter run:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """a**"foo"**"""
    expected_tokens = ["[para:]", "[text:a**&quot;foo&quot;**:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_390():
    """
    Test case 390:  Intraword strong emphasis with ** is permitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo**bar**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
