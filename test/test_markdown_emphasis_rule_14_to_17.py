"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


@pytest.mark.skip
def test_emphasis_476():
    """
    Test case 476:  (part 1) Rule 14
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """***foo***"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_477():
    """
    Test case 477:  (part 2) Rule 14
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_____foo_____"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_478():
    """
    Test case 478:  (part 1) Rule 15
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo _bar* baz_"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_479():
    """
    Test case 479:  (part 2) Rule 15
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo __bar *baz bim__ bam*"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_480():
    """
    Test case 480:  (part 1) Rule 16
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**foo **bar baz**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_481():
    """
    Test case 481:  (part 2) Rule 16
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo *bar baz*"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_482():
    """
    Test case 482:  (part 1) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*[bar*](/url)"""
    expected_tokens = ["[para:]", "[text:*[bar*](/url):]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_483():
    """
    Test case 483:  (part 2) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_foo [bar_](/url)"""
    expected_tokens = ["[para:]", "[text:_foo [bar_](/url):]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_484():
    """
    Test case 484:  (part 3) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*<img src="foo" title="*"/>"""
    expected_tokens = [
        "[para:]",
        "[text:*:]",
        '[raw-html:img src="foo" title="*"/]',
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_485():
    """
    Test case 485:  (part 4) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**<a href="**">"""
    expected_tokens = ["[para:]", "[text:**:]", '[raw-html:a href="**"]', "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_emphasis_486():
    """
    Test case 486:  (part 5) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__<a href="__">"""
    expected_tokens = ["[para:]", "[text:__:]", '[raw-html:a href="__"]', "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_487():
    """
    Test case 487:  (part 6) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*a `*`*"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_488():
    """
    Test case 488:  (part 7) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """_a `_`_"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_489():
    """
    Test case 489:  (part 8) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """**a<http://foo.bar/?q=**>"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_emphasis_490():
    """
    Test case 490:  (part 9) Rule 17
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """__a<http://foo.bar/?q=__>"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
