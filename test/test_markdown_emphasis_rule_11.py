"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_emphasis_445():
    """
    Test case 445:  (part 1) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo ***"""
    expected_tokens = ["[para(1,1):]", "[text:foo :]", "[text:***:]", "[end-para]"]
    expected_gfm = """<p>foo ***</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_446():
    """
    Test case 446:  (part 2) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo *\\**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo :]",
        "[emphasis:1]",
        "[text:*:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo <em>*</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_447():
    """
    Test case 447:  (part 3) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo *_*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo :]",
        "[emphasis:1]",
        "[text:_:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo <em>_</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_448():
    """
    Test case 448:  (part 4) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo *****"""
    expected_tokens = ["[para(1,1):]", "[text:foo :]", "[text:*****:]", "[end-para]"]
    expected_gfm = """<p>foo *****</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_449():
    """
    Test case 449:  (part 5) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo **\\***"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo :]",
        "[emphasis:2]",
        "[text:*:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo <strong>*</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_450():
    """
    Test case 450:  (part 6) Rule 11
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo **_**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo :]",
        "[emphasis:2]",
        "[text:_:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo <strong>_</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_451():
    """
    Test case 451:  (part 1) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:*:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p>*<em>foo</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_452():
    """
    Test case 452:  (part 2) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text:*:]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo</em>*</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_453():
    """
    Test case 453:  (part 3) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """***foo**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:*:]",
        "[emphasis:2]",
        "[text:foo:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p>*<strong>foo</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_454():
    """
    Test case 454:  (part 4) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """****foo*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:***:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p>***<em>foo</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_455():
    """
    Test case 455:  (part 5) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo***"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:2]",
        "[text:foo:]",
        "[end-emphasis::2]",
        "[text:*:]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo</strong>*</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_456():
    """
    Test case 456:  (part 6) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo****"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text:***:]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo</em>***</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
