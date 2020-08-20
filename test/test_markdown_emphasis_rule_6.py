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
def test_emphasis_391():
    """
    Test case 391:  Rule 6:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__foo bar__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:2:_]",
        "[text:foo bar:]",
        "[end-emphasis::2:_:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo bar</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_392():
    """
    Test case 392:  This is not strong emphasis, because the opening delimiter is followed by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__ foo bar__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:__:]",
        "[text: foo bar:]",
        "[text:__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>__ foo bar__</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_393():
    """
    Test case 393:  A newline counts as whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__
foo bar__"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text:__:]",
        "[text:\nfoo bar::\n]",
        "[text:__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>__
foo bar__</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_394():
    """
    Test case 394:  This is not strong emphasis, because the opening __ is preceded by an alphanumeric and followed by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a__"foo"__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:a:]",
        "[text:__:]",
        '[text:\a"\a&quot;\afoo\a"\a&quot;\a:]',
        "[text:__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a__&quot;foo&quot;__</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_395():
    """
    Test case 395:  (part 1) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo__bar__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo:]",
        "[text:__:]",
        "[text:bar:]",
        "[text:__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo__bar__</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_396():
    """
    Test case 396:  (part 2) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """5__6__78"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:5:]",
        "[text:__:]",
        "[text:6:]",
        "[text:__:]",
        "[text:78:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>5__6__78</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_397():
    """
    Test case 397:  (part 3) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """пристаням__стремятся__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:пристаням:]",
        "[text:__:]",
        "[text:стремятся:]",
        "[text:__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>пристаням__стремятся__</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_398():
    """
    Test case 398:  (part 4) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__foo, __bar__, baz__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:2:_]",
        "[text:foo, :]",
        "[emphasis:2:_]",
        "[text:bar:]",
        "[end-emphasis::2:_:False]",
        "[text:, baz:]",
        "[end-emphasis::2:_:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo, <strong>bar</strong>, baz</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_399():
    """
    Test case 399:  This is strong emphasis, even though the opening delimiter is both left- and right-flanking, because it is preceded by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo-__(bar)__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo-:]",
        "[emphasis:2:_]",
        "[text:(bar):]",
        "[end-emphasis::2:_:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo-<strong>(bar)</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
