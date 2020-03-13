"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
@pytest.mark.skip
def test_emphasis_431():
    """
    Test case 431:  (part 1) Any nonempty sequence of inline elements can be the contents of an strongly emphasized span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo [bar](/url)**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]
    expected_gfm = """<p><strong>foo <a href="/url">bar</a></strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:\n]",
        "[emphasis:2]",
        "[text:foo\nbar::\n]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo
bar</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[emphasis:2]",
        "[text:foo :]",
        "[emphasis:1]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[text: baz:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo <em>bar</em> baz</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[emphasis:2]",
        "[text:foo :]",
        "[emphasis:2]",
        "[text:bar:]",
        "[end-emphasis::2]",
        "[text: baz:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo <strong>bar</strong> baz</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[emphasis:2]",
        "[emphasis:2]",
        "[text:foo:]",
        "[end-emphasis::2]",
        "[text: bar:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong><strong>foo</strong> bar</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[emphasis:2]",
        "[text:foo :]",
        "[emphasis:2]",
        "[text:bar:]",
        "[end-emphasis::2]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo <strong>bar</strong></strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[emphasis:2]",
        "[text:foo :]",
        "[emphasis:1]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[text: baz:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo <em>bar</em> baz</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[emphasis:2]",
        "[text:foo:]",
        "[emphasis:1]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[text:baz:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo<em>bar</em>baz</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[emphasis:2]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text: bar:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong><em>foo</em> bar</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[emphasis:2]",
        "[text:foo :]",
        "[emphasis:1]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo <em>bar</em></strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:\n]",
        "[emphasis:2]",
        "[text:foo :]",
        "[emphasis:1]",
        "[text:bar :]",
        "[emphasis:2]",
        "[text:baz:]",
        "[end-emphasis::2]",
        "[text:\nbim::\n]",
        "[end-emphasis::1]",
        "[text: bop:]",
        "[end-emphasis::2]",
        "[end-para]",
    ]
    expected_gfm = """<p><strong>foo <em>bar <strong>baz</strong>
bim</em> bop</strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
@pytest.mark.skip
def test_emphasis_442():
    """
    Test case 442:  (part 2) Indefinite levels of nesting are possible:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**foo [*bar*](/url)**"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]
    expected_gfm = """<p><strong>foo <a href="/url"><em>bar</em></a></strong></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[text:__:]",
        "[text: is not an empty emphasis:]",
        "[end-para]",
    ]
    expected_gfm = """<p>__ is not an empty emphasis</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[text:____:]",
        "[text: is not an empty strong emphasis:]",
        "[end-para]",
    ]
    expected_gfm = """<p>____ is not an empty strong emphasis</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
