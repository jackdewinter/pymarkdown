"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_emphasis_445():
    """
    Test case 445:  (part 1) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo ***"""
    expected_tokens = ["[para:]", "[text:foo ***:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_446():
    """
    Test case 446:  (part 2) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo *\\**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_447():
    """
    Test case 447:  (part 3) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo *_*"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_448():
    """
    Test case 448:  (part 4) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo *****"""
    expected_tokens = ["[para:]", "[text:foo *****:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_449():
    """
    Test case 449:  (part 5) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo **\\***"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_450():
    """
    Test case 450:  (part 6) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo **_**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_451():
    """
    Test case 451:  (part 1) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**foo*"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_452():
    """
    Test case 452:  (part 2) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_453():
    """
    Test case 453:  (part 3) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """***foo**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_454():
    """
    Test case 454:  (part 4) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """****foo*"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_455():
    """
    Test case 455:  (part 5) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**foo***"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_456():
    """
    Test case 456:  (part 6) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo****"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
