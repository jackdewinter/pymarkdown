"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_emphasis_374():
    """
    Test case 374:  Rule 3:  This is not emphasis, because the closing delimiter does not match the opening delimiter:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_foo*"""
    expected_tokens = ["[para:]", "[text:_:]", "[text:foo:]", "[text:*:]", "[end-para]"]
    expected_gfm = """<p>_foo*</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_375():
    """
    Test case 375:  This is not emphasis, because the closing * is preceded by whitespace
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo bar *"""
    expected_tokens = [
        "[para:]",
        "[text:*:]",
        "[text:foo bar :]",
        "[text:*:]",
        "[end-para]",
    ]
    expected_gfm = """<p>*foo bar *</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_376():
    """
    Test case 376:  A newline also counts as whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo bar
*"""
    expected_tokens = [
        "[para:\n]",
        "[text:*:]",
        "[text:foo bar\n::\n]",
        "[text:*:]",
        "[end-para]",
    ]
    expected_gfm = """<p>*foo bar
*</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_377():
    """
    Test case 377:  This is not emphasis, because the second * is preceded by punctuation and followed by an alphanumeric (hence it is not part of a right-flanking delimiter run:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*(*foo)"""
    expected_tokens = [
        "[para:]",
        "[text:*:]",
        "[text:(:]",
        "[text:*:]",
        "[text:foo):]",
        "[end-para]",
    ]
    expected_gfm = """<p>*(*foo)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_378():
    """
    Test case 378:  The point of this restriction is more easily appreciated with this example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*(*foo*)*"""
    expected_tokens = [
        "[para:]",
        "[emphasis:1]",
        "[text:(:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text:):]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>(<em>foo</em>)</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_379():
    """
    Test case 379:  Intraword emphasis with * is allowed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo*bar"""
    expected_tokens = [
        "[para:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text:bar:]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo</em>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
