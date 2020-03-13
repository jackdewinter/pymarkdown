"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_emphasis_400():
    """
    Test case 400:  Rule 7: This is not strong emphasis, because the closing delimiter is preceded by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo bar **"""
    expected_tokens = [
        "[para:]",
        "[text:**:]",
        "[text:foo bar :]",
        "[text:**:]",
        "[end-para]",
    ]
    expected_gfm = """<p>**foo bar **</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_401():
    """
    Test case 401:  This is not strong emphasis, because the second ** is preceded by punctuation and followed by an alphanumeric:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**(**foo)"""
    expected_tokens = [
        "[para:]",
        "[text:**:]",
        "[text:(:]",
        "[text:**:]",
        "[text:foo):]",
        "[end-para]",
    ]
    expected_gfm = """<p>**(**foo)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_402():
    """
    Test case 402:  (part 1) The point of this restriction is more easily appreciated with these examples
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*(**foo**)*"""
    expected_tokens = [
        "[para:]",
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


@pytest.mark.gfm
def test_emphasis_403():
    """
    Test case 403:  (part 2) The point of this restriction is more easily appreciated with these examples
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**Gomphocarpus (*Gomphocarpus physocarpus*, syn.
*Asclepias physocarpa*)**"""
    expected_tokens = [
        "[para:\n]",
        "[emphasis:2]",
        "[text:Gomphocarpus (:]",
        "[emphasis:1]",
        "[text:Gomphocarpus physocarpus:]",
        "[end-emphasis::1]",
        "[text:, syn.\n::\n]",
        "[emphasis:1]",
        "[text:Asclepias physocarpa:]",
        "[end-emphasis::1]",
        "[text:):]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>Gomphocarpus (<em>Gomphocarpus physocarpus</em>, syn.
<em>Asclepias physocarpa</em>)</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_404():
    """
    Test case 404:  (part 3) The point of this restriction is more easily appreciated with these examples
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo "*bar*" foo**"""
    expected_tokens = [
        "[para:]",
        "[emphasis:2]",
        "[text:foo &quot;:]",
        "[emphasis:1]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[text:&quot; foo:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo &quot;<em>bar</em>&quot; foo</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_405():
    """
    Test case 405:  Intraword emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo**bar"""
    expected_tokens = [
        "[para:]",
        "[emphasis:2]",
        "[text:foo:]",
        "[end-emphasis::2]",
        "[text:bar:]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo</strong>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
