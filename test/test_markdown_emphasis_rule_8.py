"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_emphasis_406():
    """
    Test case 406:  Rule 8: This is not strong emphasis, because the closing delimiter is preceded by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__foo bar __"""
    expected_tokens = ["[para:]", "[text:__foo bar __:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_407():
    """
    Test case 407:  This is not strong emphasis, because the second __ is preceded by punctuation and followed by an alphanumeric:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__(__foo)"""
    expected_tokens = ["[para:]", "[text:__(__foo):]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_408():
    """
    Test case 408:  The point of this restriction is more easily appreciated with this example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_(__foo__)_"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_409():
    """
    Test case 409:  (part 1) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__foo__bar"""
    expected_tokens = ["[para:]", "[text:__foo__bar:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_410():
    """
    Test case 410:  (part 2) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__пристаням__стремятся"""
    expected_tokens = ["[para:]", "[text:__пристаням__стремятся:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_411():
    """
    Test case 411:  (part 3) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__foo__bar__baz__"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_412():
    """
    Test case 412:  This is strong emphasis, even though the closing delimiter is both left- and right-flanking, because it is followed by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__(bar)__."""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
