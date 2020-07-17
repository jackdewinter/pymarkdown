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
def test_emphasis_413():
    """
    Test case 413:  (part 1) Any nonempty sequence of inline elements can be the contents of an emphasized span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo [bar](/url)*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo :]",
        "[link:inline:/url:::::bar]",
        "[text:bar:]",
        "[end-link::]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo <a href="/url">bar</a></em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_414():
    """
    Test case 414:  (part 2) Any nonempty sequence of inline elements can be the contents of an emphasized span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo
bar*"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[emphasis:1]",
        "[text:foo\nbar::\n]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo
bar</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_415():
    """
    Test case 415:  (part 1) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_foo __bar__ baz_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo :]",
        "[emphasis:2]",
        "[text:bar:]",
        "[end-emphasis::2]",
        "[text: baz:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo <strong>bar</strong> baz</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_416():
    """
    Test case 416:  (part 2) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """_foo _bar_ baz_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo :]",
        "[emphasis:1]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[text: baz:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo <em>bar</em> baz</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_417():
    """
    Test case 417:  (part 3) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """__foo_ bar_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text: bar:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em><em>foo</em> bar</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_418():
    """
    Test case 418:  (part 4) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo *bar**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo :]",
        "[emphasis:1]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo <em>bar</em></em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_419():
    """
    Test case 419:  (part 5) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo **bar** baz*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo :]",
        "[emphasis:2]",
        "[text:bar:]",
        "[end-emphasis::2]",
        "[text: baz:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo <strong>bar</strong> baz</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_420():
    """
    Test case 420:  (part 6) In particular, emphasis and strong emphasis can be nested inside emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo**bar**baz*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo:]",
        "[emphasis:2]",
        "[text:bar:]",
        "[end-emphasis::2]",
        "[text:baz:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo<strong>bar</strong>baz</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_421():
    """
    Test case 421:  For the same reason, we don’t get two consecutive emphasis sections in this example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo**bar*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo:]",
        "[text:**:]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo**bar</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_422():
    """
    Test case 422:  (part 1) The same condition ensures that the following cases are all strong emphasis nested inside emphasis, even when the interior spaces are omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """***foo** bar*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[emphasis:2]",
        "[text:foo:]",
        "[end-emphasis::2]",
        "[text: bar:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em><strong>foo</strong> bar</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_423():
    """
    Test case 423:  (part 2) The same condition ensures that the following cases are all strong emphasis nested inside emphasis, even when the interior spaces are omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo **bar***"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo :]",
        "[emphasis:2]",
        "[text:bar:]",
        "[end-emphasis::2]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo <strong>bar</strong></em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_424():
    """
    Test case 424:  (part 3) The same condition ensures that the following cases are all strong emphasis nested inside emphasis, even when the interior spaces are omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo**bar***"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo:]",
        "[emphasis:2]",
        "[text:bar:]",
        "[end-emphasis::2]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo<strong>bar</strong></em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_425():
    """
    Test case 425:  (part 1) When the lengths of the interior closing and opening delimiter runs are both multiples of 3, though, they can match to create emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo***bar***baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo:]",
        "[emphasis:1]",
        "[emphasis:2]",
        "[text:bar:]",
        "[end-emphasis::2]",
        "[end-emphasis::1]",
        "[text:baz:]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo<em><strong>bar</strong></em>baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_426():
    """
    Test case 426:  (part 2) When the lengths of the interior closing and opening delimiter runs are both multiples of 3, though, they can match to create emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo******bar*********baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo:]",
        "[emphasis:2]",
        "[emphasis:2]",
        "[emphasis:2]",
        "[text:bar:]",
        "[end-emphasis::2]",
        "[end-emphasis::2]",
        "[end-emphasis::2]",
        "[text:***:]",
        "[text:baz:]",
        "[end-para]",
    ]
    expected_gfm = (
        """<p>foo<strong><strong><strong>bar</strong></strong></strong>***baz</p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_427():
    """
    Test case 427:  (part 1) When the lengths of the interior closing and opening delimiter runs are both multiples of 3, though, they can match to create emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo **bar *baz* bim** bop*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo :]",
        "[emphasis:2]",
        "[text:bar :]",
        "[emphasis:1]",
        "[text:baz:]",
        "[end-emphasis::1]",
        "[text: bim:]",
        "[end-emphasis::2]",
        "[text: bop:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo <strong>bar <em>baz</em> bim</strong> bop</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_428():
    """
    Test case 428:  (part 2) When the lengths of the interior closing and opening delimiter runs are both multiples of 3, though, they can match to create emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo [*bar*](/url)*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis:1]",
        "[text:foo :]",
        "[link:inline:/url:::::*bar*]",
        "[emphasis:1]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[end-link::]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo <a href="/url"><em>bar</em></a></em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_429():
    """
    Test case 429:  (part 1) There can be no empty emphasis or strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """** is not an empty emphasis"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:**:]",
        "[text: is not an empty emphasis:]",
        "[end-para]",
    ]
    expected_gfm = """<p>** is not an empty emphasis</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_emphasis_430():
    """
    Test case 430:  (part 2) There can be no empty emphasis or strong emphasis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """**** is not an empty strong emphasis"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:****:]",
        "[text: is not an empty strong emphasis:]",
        "[end-para]",
    ]
    expected_gfm = """<p>**** is not an empty strong emphasis</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
