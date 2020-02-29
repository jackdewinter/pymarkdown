"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_emphasis_374():
    """
    Test case 374:  Rule 3:  This is not emphasis, because the closing delimiter does not match the opening delimiter:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_foo*"""
    expected_tokens = ["[para:]", "[text:_foo*:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_375():
    """
    Test case 375:  This is not emphasis, because the closing * is preceded by whitespace
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo bar *"""
    expected_tokens = ["[para:]", "[text:*foo bar *:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_376():
    """
    Test case 376:  A newline also counts as whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo bar
*"""
    expected_tokens = ["[para:\n]", "[text:*foo bar\n*::\n]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_377():
    """
    Test case 377:  This is not emphasis, because the second * is preceded by punctuation and followed by an alphanumeric (hence it is not part of a right-flanking delimiter run:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*(*foo)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_378():
    """
    Test case 378:  The point of this restriction is more easily appreciated with this example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*(*foo*)*"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_379():
    """
    Test case 379:  Intraword emphasis with * is allowed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo*bar"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
