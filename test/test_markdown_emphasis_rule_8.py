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
def test_emphasis_406():
    """
    Test case 406:  Rule 8: This is not strong emphasis, because the closing delimiter is preceded by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__foo bar __"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:__:]",
        "[text:foo bar :]",
        "[text:__:]",
        "[end-para]",
    ]
    expected_gfm = """<p>__foo bar __</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_407():
    """
    Test case 407:  This is not strong emphasis, because the second __ is preceded by punctuation and followed by an alphanumeric:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__(__foo)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:__:]",
        "[text:(:]",
        "[text:__:]",
        "[text:foo):]",
        "[end-para]",
    ]
    expected_gfm = """<p>__(__foo)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_408():
    """
    Test case 408:  The point of this restriction is more easily appreciated with this example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_(__foo__)_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:(:]",
        "[emphasis:2]",
        "[text:foo:]",
        "[end-emphasis::2]",
        "[text:):]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>(<strong>foo</strong>)</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_409():
    """
    Test case 409:  (part 1) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__foo__bar"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:__:]",
        "[text:foo:]",
        "[text:__:]",
        "[text:bar:]",
        "[end-para]",
    ]
    expected_gfm = """<p>__foo__bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_410():
    """
    Test case 410:  (part 2) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__пристаням__стремятся"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:__:]",
        "[text:пристаням:]",
        "[text:__:]",
        "[text:стремятся:]",
        "[end-para]",
    ]
    expected_gfm = """<p>__пристаням__стремятся</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_411():
    """
    Test case 411:  (part 3) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__foo__bar__baz__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:2]",
        "[text:foo:]",
        "[text:__:]",
        "[text:bar:]",
        "[text:__:]",
        "[text:baz:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo__bar__baz</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_412():
    """
    Test case 412:  This is strong emphasis, even though the closing delimiter is both left- and right-flanking, because it is followed by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__(bar)__."""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:2]",
        "[text:(bar):]",
        "[end-emphasis::2]",
        "[text:.:]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>(bar)</strong>.</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
