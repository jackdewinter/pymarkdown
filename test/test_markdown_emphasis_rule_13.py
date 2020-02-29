"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


@pytest.mark.skip
def test_emphasis_469():
    """
    Test case 469:  (part 1) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**foo**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_470():
    """
    Test case 470:  (part 2) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*_foo_*"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_471():
    """
    Test case 471:  (part 3) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__foo__"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_472():
    """
    Test case 472:  (part 4) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_*foo*_"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_473():
    """
    Test case 473:  (part 1) However, strong emphasis within strong emphasis is possible without switching delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """****foo****"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_474():
    """
    Test case 474:  (part 2) However, strong emphasis within strong emphasis is possible without switching delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """____foo____"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_475():
    """
    Test case 475:  Rule 13 can be applied to arbitrarily long sequences of delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """******foo******"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
