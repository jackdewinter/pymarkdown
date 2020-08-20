"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)


@pytest.mark.gfm
def test_emphasis_469():
    """
    Test case 469:  (part 1) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:2:*]",
        "[text:foo:]",
        "[end-emphasis::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_470():
    """
    Test case 470:  (part 2) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*_foo_*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1:*]",
        "[emphasis:1:_]",
        "[text:foo:]",
        "[end-emphasis::1:_:False]",
        "[end-emphasis::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em><em>foo</em></em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_471():
    """
    Test case 471:  (part 3) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__foo__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:2:_]",
        "[text:foo:]",
        "[end-emphasis::2:_:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_472():
    """
    Test case 472:  (part 4) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_*foo*_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1:_]",
        "[emphasis:1:*]",
        "[text:foo:]",
        "[end-emphasis::1:*:False]",
        "[end-emphasis::1:_:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em><em>foo</em></em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_473():
    """
    Test case 473:  (part 1) However, strong emphasis within strong emphasis is possible without switching delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """****foo****"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:2:*]",
        "[emphasis:2:*]",
        "[text:foo:]",
        "[end-emphasis::2:*:False]",
        "[end-emphasis::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong><strong>foo</strong></strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_474():
    """
    Test case 474:  (part 2) However, strong emphasis within strong emphasis is possible without switching delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """____foo____"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:2:_]",
        "[emphasis:2:_]",
        "[text:foo:]",
        "[end-emphasis::2:_:False]",
        "[end-emphasis::2:_:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong><strong>foo</strong></strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_475():
    """
    Test case 475:  Rule 13 can be applied to arbitrarily long sequences of delimiters:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """******foo******"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:2:*]",
        "[emphasis:2:*]",
        "[emphasis:2:*]",
        "[text:foo:]",
        "[end-emphasis::2:*:False]",
        "[end-emphasis::2:*:False]",
        "[end-emphasis::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong><strong><strong>foo</strong></strong></strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
