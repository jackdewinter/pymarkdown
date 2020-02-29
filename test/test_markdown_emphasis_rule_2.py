"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


@pytest.mark.skip
def test_emphasis_366():
    """
    Test case 366:  Rule 2:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_foo bar_"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_367():
    """
    Test case 367:  This is not emphasis, because the opening _ is followed by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_ foo bar_"""
    expected_tokens = ["[para:]", "[text:_ foo bar_:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_368():
    """
    Test case 368:  This is not emphasis, because the opening _ is preceded by an alphanumeric and followed by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """a_"foo"_"""
    expected_tokens = ["[para:]", "[text:a_&quot;foo&quot;_:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_369():
    """
    Test case 369:  (part 1) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo_bar_"""
    expected_tokens = ["[para:]", "[text:foo_bar_:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_370():
    """
    Test case 370:  (part 2) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """5_6_78"""
    expected_tokens = ["[para:]", "[text:5_6_78:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_371():
    """
    Test case 371:  (part 3) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """пристаням_стремятся_"""
    expected_tokens = ["[para:]", "[text:пристаням_стремятся_:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_372():
    """
    Test case 372:  Here _ does not generate emphasis, because the first delimiter run is right-flanking and the second left-flanking:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """aa_"bb"_cc"""
    expected_tokens = ["[para:]", "[text:aa_&quot;bb&quot;_cc:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_373():
    """
    Test case 373:  This is emphasis, even though the opening delimiter is both left- and right-flanking, because it is preceded by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo-_(bar)_"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
