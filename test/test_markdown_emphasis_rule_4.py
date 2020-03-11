"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_emphasis_380():
    """
    Test case 380:  Rule 4:  This is not emphasis, because the closing _ is preceded by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_foo bar _"""
    expected_tokens = [
        "[para:]",
        "[text:_:]",
        "[text:foo bar :]",
        "[text:_:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_381():
    """
    Test case 381:  This is not emphasis, because the second _ is preceded by punctuation and followed by an alphanumeric:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_(_foo)"""
    expected_tokens = [
        "[para:]",
        "[text:_:]",
        "[text:(:]",
        "[text:_:]",
        "[text:foo):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_382():
    """
    Test case 382:  This is emphasis within emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_(_foo_)_"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_383():
    """
    Test case 383:  (part 1) Intraword emphasis is disallowed for _:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_foo_bar"""
    expected_tokens = [
        "[para:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text:bar:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_384():
    """
    Test case 384:  (part 2) Intraword emphasis is disallowed for _:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_пристаням_стремятся"""
    expected_tokens = [
        "[para:]",
        "[emphasis:1]",
        "[text:пристаням:]",
        "[end-emphasis::1]",
        "[text:стремятся:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_385():
    """
    Test case 385:  (part 3) Intraword emphasis is disallowed for _:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_foo_bar_baz_"""
    expected_tokens = [
        "[para:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text:bar:]",
        "[emphasis:1]",
        "[text:baz:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_386():
    """
    Test case 386:  This is emphasis, even though the closing delimiter is both left- and right-flanking, because it is followed by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_(bar)_."""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
