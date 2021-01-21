"""
https://github.github.com/gfm/#hard-line-breaks
"""

import pytest

from .utils import act_and_assert


@pytest.mark.gfm
def test_hard_line_breaks_654():
    """
    Test case 654:  A line break (not in a code span or HTML tag) that is preceded by two or more spaces and does not occur at the end of a block is parsed as a hard line break (rendered in HTML as a <br /> tag):
    """

    # Arrange
    source_markdown = """foo\a\a
baz""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo:]",
        "[hard-break(1,4):  ]",
        "[text(2,1):\nbaz::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_655x():
    """
    Test case 655:  For a more visible alternative, a backslash before the line ending may be used instead of two spaces:
    """

    # Arrange
    source_markdown = """foo\\
baz"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo:]",
        "[hard-break(1,4):\\]",
        "[text(2,1):\nbaz::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_655a():
    """
    Test case 655a:  variation with two backslashes at end
    """

    # Arrange
    source_markdown = """foo\\\\
baz"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo\\\b\\\nbaz::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo\\
baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_656():
    """
    Test case 656:  More than two spaces can be used:
    """

    # Arrange
    source_markdown = """foo\a\a\a\a\a\a\a
baz""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo:]",
        "[hard-break(1,4):       ]",
        "[text(2,1):\nbaz::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_657():
    """
    Test case 657:  (part 1) Leading spaces at the beginning of the next line are ignored:
    """

    # Arrange
    source_markdown = """foo\a\a
     bar""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n     ]",
        "[text(1,1):foo:]",
        "[hard-break(1,4):  ]",
        "[text(2,6):\nbar::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_658():
    """
    Test case 658:  (part 2) Leading spaces at the beginning of the next line are ignored:
    """

    # Arrange
    source_markdown = """foo\\
     bar"""
    expected_tokens = [
        "[para(1,1):\n     ]",
        "[text(1,1):foo:]",
        "[hard-break(1,4):\\]",
        "[text(2,6):\nbar::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_659():
    """
    Test case 659:  (part 1) Line breaks can occur inside emphasis, links, and other constructs that allow inline content:
    """

    # Arrange
    source_markdown = """*foo\a\a
bar*""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo:]",
        "[hard-break(1,5):  ]",
        "[text(2,1):\nbar::\n]",
        "[end-emphasis(2,4):::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo<br />
bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_660():
    """
    Test case 660:  (part 2) Line breaks can occur inside emphasis, links, and other constructs that allow inline content:
    """

    # Arrange
    source_markdown = """*foo\\
bar*""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo:]",
        "[hard-break(1,5):\\]",
        "[text(2,1):\nbar::\n]",
        "[end-emphasis(2,4):::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo<br />
bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_661():
    """
    Test case 661:  (part 1) Line breaks do not occur inside code spans
    """

    # Arrange
    source_markdown = """`code\a\a
span`""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[icode-span(1,1):code  \a\n\a \aspan:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>code   span</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_662():
    """
    Test case 662:  (part 2) Line breaks do not occur inside code spans
    """

    # Arrange
    source_markdown = """`code\\
span`"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[icode-span(1,1):code\\\a\n\a \aspan:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>code\\ span</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_663():
    """
    Test case 663:  (part 1) or HTML tags:
    """

    # Arrange
    source_markdown = """<a href="foo\a\a
bar">""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        '[raw-html(1,1):a href="foo  \nbar"]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="foo\a\a
bar"></p>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_664():
    """
    Test case 664:  (part 2) or HTML tags:
    """

    # Arrange
    source_markdown = """<a href="foo\\
bar">"""
    expected_tokens = [
        "[para(1,1):\n]",
        '[raw-html(1,1):a href="foo\\\nbar"]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="foo\\
bar"></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_665():
    """
    Test case 665:  (part 1) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    source_markdown = """foo\\"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):foo\\:]", "[end-para:::True]"]
    expected_gfm = """<p>foo\\</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_665a():
    """
    Test case 665a:  variation of 665 with a space before hb character
    """

    # Arrange
    source_markdown = """foo \\"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):foo \\:]", "[end-para:::True]"]
    expected_gfm = """<p>foo \\</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_666():
    """
    Test case 666:  (part 2) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    source_markdown = """foo  """
    expected_tokens = ["[para(1,1)::  ]", "[text(1,1):foo:]", "[end-para:::True]"]
    expected_gfm = """<p>foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_667():
    """
    Test case 667:  (part 3) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    source_markdown = """### foo\\"""
    expected_tokens = ["[atx(1,1):3:0:]", "[text(1,5):foo\\: ]", "[end-atx:::False]"]
    expected_gfm = """<h3>foo\\</h3>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_668():
    """
    Test case 668:  (part 4) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    source_markdown = """### foo  """
    expected_tokens = ["[atx(1,1):3:0:]", "[text(1,5):foo: ]", "[end-atx:  ::False]"]
    expected_gfm = """<h3>foo</h3>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
