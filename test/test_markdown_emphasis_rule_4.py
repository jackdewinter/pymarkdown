"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_emphasis_380():
    """
    Test case 380:  Rule 4:  This is not emphasis, because the closing _ is preceded by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_foo bar _"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:_:]",
        "[text:foo bar :]",
        "[text:_:]",
        "[end-para]",
    ]
    expected_gfm = """<p>_foo bar _</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_381():
    """
    Test case 381:  This is not emphasis, because the second _ is preceded by punctuation and followed by an alphanumeric:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_(_foo)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:_:]",
        "[text:(:]",
        "[text:_:]",
        "[text:foo):]",
        "[end-para]",
    ]
    expected_gfm = """<p>_(_foo)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_382():
    """
    Test case 382:  This is emphasis within emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_(_foo_)_"""
    expected_tokens = [
        "[para(1,1):]",
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
def test_emphasis_383():
    """
    Test case 383:  (part 1) Intraword emphasis is disallowed for _:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_foo_bar"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:_:]",
        "[text:foo:]",
        "[text:_:]",
        "[text:bar:]",
        "[end-para]",
    ]
    expected_gfm = """<p>_foo_bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_384():
    """
    Test case 384:  (part 2) Intraword emphasis is disallowed for _:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_пристаням_стремятся"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:_:]",
        "[text:пристаням:]",
        "[text:_:]",
        "[text:стремятся:]",
        "[end-para]",
    ]
    expected_gfm = """<p>_пристаням_стремятся</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_385():
    """
    Test case 385:  (part 3) Intraword emphasis is disallowed for _:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_foo_bar_baz_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo:]",
        "[text:_:]",
        "[text:bar:]",
        "[text:_:]",
        "[text:baz:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo_bar_baz</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_386():
    """
    Test case 386:  This is emphasis, even though the closing delimiter is both left- and right-flanking, because it is followed by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_(bar)_."""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:(bar):]",
        "[end-emphasis::1]",
        "[text:.:]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>(bar)</em>.</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
