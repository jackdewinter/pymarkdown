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
def test_emphasis_431():
    """
    Test case 431:  (part 1) Any nonempty sequence of inline elements can be the contents of an strongly emphasized span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo [bar](/url)**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo :]",
        "[link:inline:/url:::::bar:False::::]",
        "[text(1,8):bar:]",
        "[end-link:::False]",
        "[end-emphasis(1,18)::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo <a href="/url">bar</a></strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_432():
    """
    Test case 432:  (part 2) Any nonempty sequence of inline elements can be the contents of an strongly emphasized span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo
bar**"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo\nbar::\n]",
        "[end-emphasis(2,4)::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo
bar</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_433():
    """
    Test case 433:  (part 1) In particular, emphasis and strong emphasis can be nested inside strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__foo _bar_ baz__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):foo :]",
        "[emphasis(1,7):1:_]",
        "[text(1,8):bar:]",
        "[end-emphasis(1,11)::1:_:False]",
        "[text(1,12): baz:]",
        "[end-emphasis(1,16)::2:_:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo <em>bar</em> baz</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_434():
    """
    Test case 434:  (part 2) In particular, emphasis and strong emphasis can be nested inside strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__foo __bar__ baz__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):foo :]",
        "[emphasis(1,7):2:_]",
        "[text(1,9):bar:]",
        "[end-emphasis(1,12)::2:_:False]",
        "[text(1,14): baz:]",
        "[end-emphasis(1,18)::2:_:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo <strong>bar</strong> baz</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_435():
    """
    Test case 435:  (part 3) In particular, emphasis and strong emphasis can be nested inside strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """____foo__ bar__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[emphasis(1,3):2:_]",
        "[text(1,5):foo:]",
        "[end-emphasis(1,8)::2:_:False]",
        "[text(1,10): bar:]",
        "[end-emphasis(1,14)::2:_:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong><strong>foo</strong> bar</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_436():
    """
    Test case 436:  (part 4) In particular, emphasis and strong emphasis can be nested inside strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo **bar****"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo :]",
        "[emphasis(1,7):2:*]",
        "[text(1,9):bar:]",
        "[end-emphasis(1,12)::2:*:False]",
        "[end-emphasis(1,14)::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo <strong>bar</strong></strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_437():
    """
    Test case 437:  (part 5) In particular, emphasis and strong emphasis can be nested inside strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo *bar* baz**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo :]",
        "[emphasis(1,7):1:*]",
        "[text(1,8):bar:]",
        "[end-emphasis(1,11)::1:*:False]",
        "[text(1,12): baz:]",
        "[end-emphasis(1,16)::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo <em>bar</em> baz</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_438():
    """
    Test case 438:  (part 6) In particular, emphasis and strong emphasis can be nested inside strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo*bar*baz**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo:]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):bar:]",
        "[end-emphasis(1,10)::1:*:False]",
        "[text(1,11):baz:]",
        "[end-emphasis(1,14)::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo<em>bar</em>baz</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_439():
    """
    Test case 439:  (part 7) In particular, emphasis and strong emphasis can be nested inside strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """***foo* bar**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[emphasis(1,3):1:*]",
        "[text(1,4):foo:]",
        "[end-emphasis(1,7)::1:*:False]",
        "[text(1,8): bar:]",
        "[end-emphasis(1,12)::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong><em>foo</em> bar</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_440():
    """
    Test case 440:  (part 8) In particular, emphasis and strong emphasis can be nested inside strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo *bar***"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo :]",
        "[emphasis(1,7):1:*]",
        "[text(1,8):bar:]",
        "[end-emphasis(1,11)::1:*:False]",
        "[end-emphasis(1,12)::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo <em>bar</em></strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_441():
    """
    Test case 441:  (part 1) Indefinite levels of nesting are possible:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo *bar **baz**
bim* bop**"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo :]",
        "[emphasis(1,7):1:*]",
        "[text(1,8):bar :]",
        "[emphasis(1,12):2:*]",
        "[text(1,14):baz:]",
        "[end-emphasis(1,17)::2:*:False]",
        "[text(1,19):\nbim::\n]",
        "[end-emphasis(2,4)::1:*:False]",
        "[text(2,5): bop:]",
        "[end-emphasis(2,9)::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo <em>bar <strong>baz</strong>
bim</em> bop</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_442():
    """
    Test case 442:  (part 2) Indefinite levels of nesting are possible:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo [*bar*](/url)**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo :]",
        "[link:inline:/url:::::*bar*:False::::]",
        "[emphasis(1,8):1:*]",
        "[text(1,9):bar:]",
        "[end-emphasis(1,12)::1:*:False]",
        "[end-link:::False]",
        "[end-emphasis(1,20)::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo <a href="/url"><em>bar</em></a></strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_443():
    """
    Test case 443:  (part 1) There can be no empty emphasis or strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__ is not an empty emphasis"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):__:]",
        "[text(1,3): is not an empty emphasis:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>__ is not an empty emphasis</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_444():
    """
    Test case 444:  (part 2) There can be no empty emphasis or strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """____ is not an empty strong emphasis"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):____:]",
        "[text(1,5): is not an empty strong emphasis:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>____ is not an empty strong emphasis</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
