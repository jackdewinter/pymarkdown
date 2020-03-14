"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_emphasis_457():
    """
    Test case 457:  (part 1) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo ___"""
    expected_tokens = ["[para:]", "[text:foo :]", "[text:___:]", "[end-para]"]
    expected_gfm = """<p>foo ___</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_458():
    """
    Test case 458:  (part 2) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo _\\__"""
    expected_tokens = [
        "[para:]",
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
def test_emphasis_459():
    """
    Test case 459:  (part 3) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo _*_"""
    expected_tokens = [
        "[para:]",
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
def test_emphasis_460():
    """
    Test case 460:  (part 4) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo _____"""
    expected_tokens = ["[para:]", "[text:foo :]", "[text:_____:]", "[end-para]"]
    expected_gfm = """<p>foo _____</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_461():
    """
    Test case 461:  (part 5) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo __\\___"""
    expected_tokens = [
        "[para:]",
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
def test_emphasis_462():
    """
    Test case 462:  (part 6) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo __*__"""
    expected_tokens = [
        "[para:]",
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
def test_emphasis_463():
    """
    Test case 463:  (part 7) Rule 12
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__foo_"""
    expected_tokens = [
        "[para:]",
        "[text:_:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p>_<em>foo</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_464():
    """
    Test case 464:  (part 1) Note that when delimiters do not match evenly, Rule 12 determines that the excess literal _ characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_foo__"""
    expected_tokens = [
        "[para:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text:_:]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo</em>_</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_465():
    """
    Test case 465:  (part 2) Note that when delimiters do not match evenly, Rule 12 determines that the excess literal _ characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """___foo__"""
    expected_tokens = [
        "[para:]",
        "[text:_:]",
        "[emphasis:2]",
        "[text:foo:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p>_<strong>foo</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_466():
    """
    Test case 466:  (part 3) Note that when delimiters do not match evenly, Rule 12 determines that the excess literal _ characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """____foo_"""
    expected_tokens = [
        "[para:]",
        "[text:___:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p>___<em>foo</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_467():
    """
    Test case 467:  (part 4) Note that when delimiters do not match evenly, Rule 12 determines that the excess literal _ characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__foo___"""
    expected_tokens = [
        "[para:]",
        "[emphasis:2]",
        "[text:foo:]",
        "[end-emphasis::2]",
        "[text:_:]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo</strong>_</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_emphasis_468():
    """
    Test case 468:  (part 5) Note that when delimiters do not match evenly, Rule 12 determines that the excess literal _ characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_foo____"""
    expected_tokens = [
        "[para:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text:___:]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo</em>___</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
