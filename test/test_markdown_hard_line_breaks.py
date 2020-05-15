"""
https://github.github.com/gfm/#hard-line-breaks
"""

import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_hard_line_breaks_654():
    """
    Test case 654:  A line break (not in a code span or HTML tag) that is preceded by two or more spaces and does not occur at the end of a block is parsed as a hard line break (rendered in HTML as a <br /> tag):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo\a\a
baz""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para:\n]",
        "[text:foo:]",
        "[hard-break:  ]",
        "[text:\nbaz::\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo<br />
baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_655():
    """
    Test case 655:  For a more visible alternative, a backslash before the line ending may be used instead of two spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo\\
baz"""
    expected_tokens = [
        "[para:\n]",
        "[text:foo:]",
        "[hard-break:\\]",
        "[text:\nbaz:]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo<br />
baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_656():
    """
    Test case 656:  More than two spaces can be used:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo\a\a\a\a\a\a\a
baz""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para:\n]",
        "[text:foo:]",
        "[hard-break:       ]",
        "[text:\nbaz::\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo<br />
baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_657():
    """
    Test case 657:  (part 1) Leading spaces at the beginning of the next line are ignored:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo\a\a
     bar""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para:\n     ]",
        "[text:foo:]",
        "[hard-break:  ]",
        "[text:\nbar::\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo<br />
bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_658():
    """
    Test case 658:  (part 2) Leading spaces at the beginning of the next line are ignored:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo\\
     bar"""
    expected_tokens = [
        "[para:\n     ]",
        "[text:foo:]",
        "[hard-break:\\]",
        "[text:\nbar:]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo<br />
bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_659():
    """
    Test case 659:  (part 1) Line breaks can occur inside emphasis, links, and other constructs that allow inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo\a\a
bar*""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para:\n]",
        "[emphasis:1]",
        "[text:foo:]",
        "[hard-break:  ]",
        "[text:\nbar::\n]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo<br />
bar</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_660():
    """
    Test case 660:  (part 2) Line breaks can occur inside emphasis, links, and other constructs that allow inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo\\
bar*""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para:\n]",
        "[emphasis:1]",
        "[text:foo:]",
        "[hard-break:\\]",
        "[text:\nbar:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo<br />
bar</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_661():
    """
    Test case 661:  (part 1) Line breaks do not occur inside code spans
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """`code\a\a
span`""".replace(
        "\a", " "
    )
    expected_tokens = ["[para:\n]", "[icode-span:code   span]", "[end-para]"]
    expected_gfm = """<p><code>code   span</code></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_662():
    """
    Test case 662:  (part 2) Line breaks do not occur inside code spans
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """`code\\
span`"""
    expected_tokens = ["[para:\n]", "[icode-span:code\\ span]", "[end-para]"]
    expected_gfm = """<p><code>code\\ span</code></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_663():
    """
    Test case 663:  (part 1) or HTML tags:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a href="foo\a\a
bar">""".replace(
        "\a", " "
    )
    expected_tokens = ["[para:\n]", '[raw-html:a href="foo  \nbar"]', "[end-para]"]
    expected_gfm = """<p><a href="foo\a\a
bar"></p>""".replace(
        "\a", " "
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_664():
    """
    Test case 664:  (part 2) or HTML tags:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a href="foo\\
bar">"""
    expected_tokens = ["[para:\n]", '[raw-html:a href="foo\\\nbar"]', "[end-para]"]
    expected_gfm = """<p><a href="foo\\
bar"></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_665():
    """
    Test case 665:  (part 1) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo\\"""
    expected_tokens = ["[para:]", "[text:foo\\:]", "[end-para]"]
    expected_gfm = """<p>foo\\</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_665a():
    """
    Test case 665a:  variation of 665 with a space before hb character
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo \\"""
    expected_tokens = ["[para:]", "[text:foo \\:]", "[end-para]"]
    expected_gfm = """<p>foo \\</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_666():
    """
    Test case 666:  (part 2) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo  """
    expected_tokens = ["[para::  ]", "[text:foo:]", "[end-para]"]
    expected_gfm = """<p>foo</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_667():
    """
    Test case 667:  (part 3) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """### foo\\"""
    expected_tokens = ["[atx:3:0:]", "[text:foo\\: ]", "[end-atx::]"]
    expected_gfm = """<h3>foo\\</h3>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_hard_line_breaks_668():
    """
    Test case 668:  (part 4) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """### foo  """
    expected_tokens = ["[atx:3:0:]", "[text:foo: ]", "[end-atx:  :]"]
    expected_gfm = """<h3>foo</h3>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
