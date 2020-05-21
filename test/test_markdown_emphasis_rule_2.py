"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_emphasis_366():
    """
    Test case 366:  Rule 2:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_foo bar_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo bar:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo bar</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_367():
    """
    Test case 367:  This is not emphasis, because the opening _ is followed by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_ foo bar_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:_:]",
        "[text: foo bar:]",
        "[text:_:]",
        "[end-para]",
    ]
    expected_gfm = """<p>_ foo bar_</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_368():
    """
    Test case 368:  This is not emphasis, because the opening _ is preceded by an alphanumeric and followed by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a_"foo"_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:a:]",
        "[text:_:]",
        "[text:&quot;foo&quot;:]",
        "[text:_:]",
        "[end-para]",
    ]
    expected_gfm = """<p>a_&quot;foo&quot;_</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_369():
    """
    Test case 369:  (part 1) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo_bar_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo:]",
        "[text:_:]",
        "[text:bar:]",
        "[text:_:]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo_bar_</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_370():
    """
    Test case 370:  (part 2) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """5_6_78"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:5:]",
        "[text:_:]",
        "[text:6:]",
        "[text:_:]",
        "[text:78:]",
        "[end-para]",
    ]
    expected_gfm = """<p>5_6_78</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_371():
    """
    Test case 371:  (part 3) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """пристаням_стремятся_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:пристаням:]",
        "[text:_:]",
        "[text:стремятся:]",
        "[text:_:]",
        "[end-para]",
    ]
    expected_gfm = """<p>пристаням_стремятся_</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_372():
    """
    Test case 372:  Here _ does not generate emphasis, because the first delimiter run is right-flanking and the second left-flanking:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """aa_"bb"_cc"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:aa:]",
        "[text:_:]",
        "[text:&quot;bb&quot;:]",
        "[text:_:]",
        "[text:cc:]",
        "[end-para]",
    ]
    expected_gfm = """<p>aa_&quot;bb&quot;_cc</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_373():
    """
    Test case 373:  This is emphasis, even though the opening delimiter is both left- and right-flanking, because it is preceded by punctuation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo-_(bar)_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo-:]",
        "[emphasis:1]",
        "[text:(bar):]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo-<em>(bar)</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
