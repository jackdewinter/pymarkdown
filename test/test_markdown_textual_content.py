"""
https://github.github.com/gfm/#textual-content
"""

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_textual_content_671():
    """
    Test case 671:  (part 1) Any characters not given an interpretation by the above rules will be parsed as plain textual content.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """hello $.;'there"""
    expected_tokens = ["[para:]", "[text:hello $.;'there:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_textual_content_672():
    """
    Test case 672:  (part 2) Any characters not given an interpretation by the above rules will be parsed as plain textual content.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo χρῆν"""
    expected_tokens = ["[para:]", "[text:Foo χρῆν:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_textual_content_673():
    """
    Test case 673:  Internal spaces are preserved verbatim:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Multiple     spaces"""
    expected_tokens = ["[para:]", "[text:Multiple     spaces:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
