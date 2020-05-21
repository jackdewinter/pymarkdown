"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_emphasis_387():
    """
    Test case 387:  Rule 5:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo bar**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:2]",
        "[text:foo bar:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo bar</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_388():
    """
    Test case 388:  This is not strong emphasis, because the opening delimiter is followed by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """** foo bar**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:**:]",
        "[text: foo bar:]",
        "[text:**:]",
        "[end-para]",
    ]
    expected_gfm = """<p>** foo bar**</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_389():
    """
    Test case 389:  This is not strong emphasis, because the opening ** is preceded by an alphanumeric and followed by punctuation, and hence not part of a left-flanking delimiter run:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a**"foo"**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:a:]",
        "[text:**:]",
        "[text:&quot;foo&quot;:]",
        "[text:**:]",
        "[end-para]",
    ]
    expected_gfm = """<p>a**&quot;foo&quot;**</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_390():
    """
    Test case 390:  Intraword strong emphasis with ** is permitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo**bar**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo:]",
        "[emphasis:2]",
        "[text:bar:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo<strong>bar</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
