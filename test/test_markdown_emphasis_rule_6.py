"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


@pytest.mark.skip
def test_emphasis_391():
    """
    Test case 391:  Rule 6:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__foo bar__"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_392():
    """
    Test case 392:  This is not strong emphasis, because the opening delimiter is followed by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__ foo bar__"""
    expected_tokens = ["[para:]", "[text:__ foo bar__:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_393():
    """
    Test case 393:  A newline counts as whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__
foo bar__"""
    expected_tokens = ["[para:\n]", "[text:__\nfoo bar__::\n]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_394():
    """
    Test case 394:  This is not strong emphasis, because the opening __ is preceded by an alphanumeric and followed by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """a__"foo"__"""
    expected_tokens = ["[para:]", "[text:a__&quot;foo&quot;__:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_395():
    """
    Test case 395:  (part 1) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo__bar__"""
    expected_tokens = ["[para:]", "[text:foo__bar__:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_396():
    """
    Test case 396:  (part 2) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """5__6__78"""
    expected_tokens = ["[para:]", "[text:5__6__78:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_397():
    """
    Test case 397:  (part 3) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """пристаням__стремятся__"""
    expected_tokens = ["[para:]", "[text:пристаням__стремятся__:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_398():
    """
    Test case 398:  (part 4) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__foo, __bar__, baz__"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_399():
    """
    Test case 399:  This is strong emphasis, even though the opening delimiter is both left- and right-flanking, because it is preceded by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo-__(bar)__"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
