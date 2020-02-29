"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_emphasis_457():
    """
    Test case 457:  (part 1) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo ___"""
    expected_tokens = ["[para:]", "[text:foo ___:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_458():
    """
    Test case 458:  (part 2) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo _\\__"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_459():
    """
    Test case 459:  (part 3) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo _*_"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_460():
    """
    Test case 460:  (part 4) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo _____"""
    expected_tokens = ["[para:]", "[text:foo _____:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_461():
    """
    Test case 461:  (part 5) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo __\\___"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_462():
    """
    Test case 462:  (part 6) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo __*__"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_463():
    """
    Test case 463:  (part 7) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__foo_"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_464():
    """
    Test case 464:  (part 1) Note that when delimiters do not match evenly, Rule 12 determines that the excess literal _ characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_foo__"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_465():
    """
    Test case 465:  (part 2) Note that when delimiters do not match evenly, Rule 12 determines that the excess literal _ characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """___foo__"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_466():
    """
    Test case 466:  (part 3) Note that when delimiters do not match evenly, Rule 12 determines that the excess literal _ characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """____foo_"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_467():
    """
    Test case 467:  (part 4) Note that when delimiters do not match evenly, Rule 12 determines that the excess literal _ characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__foo___"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_468():
    """
    Test case 468:  (part 5) Note that when delimiters do not match evenly, Rule 12 determines that the excess literal _ characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_foo____"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
