"""
https://github.github.com/gfm/#hard-line-breaks
"""

from test.utils import act_and_assert

import pytest


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_hard_line_breaks_654() -> None:
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
        "[hard-break(1,4):  :\n]",
        "[text(2,1):baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_655x() -> None:
    """
    Test case 655:  For a more visible alternative, a backslash before the line ending may be used instead of two spaces:
    """

    # Arrange
    source_markdown = """foo\\
baz"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo:]",
        "[hard-break(1,4):\\:\n]",
        "[text(2,1):baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_655a() -> None:
    """
    Test case 655a:  variation of 655 with two backslashes at end
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
def test_hard_line_breaks_656() -> None:
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
        "[hard-break(1,4):       :\n]",
        "[text(2,1):baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_657() -> None:
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
        "[hard-break(1,4):  :\n]",
        "[text(2,6):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_658() -> None:
    """
    Test case 658:  (part 2) Leading spaces at the beginning of the next line are ignored:
    """

    # Arrange
    source_markdown = """foo\\
     bar"""
    expected_tokens = [
        "[para(1,1):\n     ]",
        "[text(1,1):foo:]",
        "[hard-break(1,4):\\:\n]",
        "[text(2,6):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_659() -> None:
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
        "[hard-break(1,5):  :\n]",
        "[text(2,1):bar:]",
        "[end-emphasis(2,4)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo<br />
bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_660() -> None:
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
        "[hard-break(1,5):\\:\n]",
        "[text(2,1):bar:]",
        "[end-emphasis(2,4)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo<br />
bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_661() -> None:
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
def test_hard_line_breaks_662() -> None:
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
def test_hard_line_breaks_663() -> None:
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
def test_hard_line_breaks_664() -> None:
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
def test_hard_line_breaks_665() -> None:
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
def test_hard_line_breaks_665a() -> None:
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
def test_hard_line_breaks_666() -> None:
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
def test_hard_line_breaks_667() -> None:
    """
    Test case 667:  (part 3) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    source_markdown = """### foo\\"""
    expected_tokens = ["[atx(1,1):3:0:]", "[text(1,5):foo\\: ]", "[end-atx::]"]
    expected_gfm = """<h3>foo\\</h3>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_668() -> None:
    """
    Test case 668:  (part 4) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    source_markdown = """### foo  """
    expected_tokens = ["[atx(1,1):3:0:]", "[text(1,5):foo: ]", "[end-atx:  :]"]
    expected_gfm = """<h3>foo</h3>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_01x() -> None:
    """
    Test case extra 01x:  Hard line breaks at start of line
    """

    # Arrange
    source_markdown = """\a\a
This is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):  ]",
        "[para(2,1):]",
        "[text(2,1):This is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_01a() -> None:
    """
    Test case extra 01x:  Hard line breaks at start of line
    """

    # Arrange
    source_markdown = """\\
This is new."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[hard-break(1,1):\\:\n]",
        "[text(2,1):This is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><br />
This is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_02x() -> None:
    """
    Test case extra 02x:  Hard line breaks as the only whitespace on the line
    """

    # Arrange
    source_markdown = """abc
\a\a
This is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):  ]",
        "[para(3,1):]",
        "[text(3,1):This is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc</p>
<p>This is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_02a() -> None:
    """
    Test case extra 02a:  Hard line breaks at start of blank line
    """

    # Arrange
    source_markdown = """abc
\\
This is new."""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):abc\n::\n]",
        "[hard-break(2,1):\\:\n]",
        "[text(3,1):This is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
<br />
This is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_03x() -> None:
    """
    Test case extra 03x:  Hard line break followed by text
    """

    # Arrange
    source_markdown = """abc\\
This is new."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):\\:\n]",
        "[text(2,1):This is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
This is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_03a() -> None:
    """
    Test case extra 03a:  Hard line break followed by backslash escaped
    """

    # Arrange
    source_markdown = """abc\\
\\\\This is new."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):\\:\n]",
        "[text(2,1):\\\b\\This is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
\\This is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_03b() -> None:
    """
    Test case extra 03b:  Hard line break followed by entity
    """

    # Arrange
    source_markdown = """abc\\
&copy; This is new."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):\\:\n]",
        "[text(2,1):\a&copy;\a©\a This is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
© This is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_03c() -> None:
    """
    Test case extra 03c:  Hard line break followed by code span
    """

    # Arrange
    source_markdown = """abc\\
`This` is new."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):\\:\n]",
        "[icode-span(2,1):This:`::]",
        "[text(2,7): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<code>This</code> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_03d() -> None:
    """
    Test case extra 03d:  Hard line break followed by emphasis
    """

    # Arrange
    source_markdown = """abc\\
*This* is new."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):\\:\n]",
        "[emphasis(2,1):1:*]",
        "[text(2,2):This:]",
        "[end-emphasis(2,6)::]",
        "[text(2,7): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<em>This</em> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_03e() -> None:
    """
    Test case extra 03e:  Hard line break followed by link
    """

    # Arrange
    source_markdown = """abc\\
[This](foo.com) is new."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):\\:\n]",
        "[link(2,1):inline:foo.com:::::This:False::::]",
        "[text(2,2):This:]",
        "[end-link::]",
        "[text(2,16): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<a href="foo.com">This</a> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_03f() -> None:
    """
    Test case extra 03f:  Hard line break followed by link
    """

    # Arrange
    source_markdown = """abc\\
![This](foo.com) is new."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):\\:\n]",
        "[image(2,1):inline:foo.com::This::::This:False::::]",
        "[text(2,17): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<img src="foo.com" alt="This" /> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_03g() -> None:
    """
    Test case extra 03g:  Hard line break followed by autolink
    """

    # Arrange
    source_markdown = """abc\\
<http://this.com> is new."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):\\:\n]",
        "[uri-autolink(2,1):http://this.com]",
        "[text(2,18): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<a href="http://this.com">http://this.com</a> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_03h() -> None:
    """
    Test case extra 03h:  Hard line break followed by autolink
    """

    # Arrange
    source_markdown = """abc\\
<this> is new."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):\\:\n]",
        "[raw-html(2,1):this]",
        "[text(2,7): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<this> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_03i() -> None:
    """
    Test case extra 03i:  Hard line break followed by hard line break
    """

    # Arrange
    source_markdown = """abc\\
\\
this is new."""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):\\:\n]",
        "[hard-break(2,1):\\:\n]",
        "[text(3,1):this is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<br />
this is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_04x() -> None:
    """
    Test case extra 04:  Hard line break followed by text
    """

    # Arrange
    source_markdown = """abc\a\a
This is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):  :\n]",
        "[text(2,1):This is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
This is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_04xa() -> None:
    """
    Test case extra 04xa:  Hard line break followed by whitespace and text
    """

    # Arrange
    source_markdown = """abc\a\a
  This is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n  ]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):  :\n]",
        "[text(2,3):This is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
This is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_04a() -> None:
    """
    Test case extra 04a:  Hard line break followed by backslash escaped
    """

    # Arrange
    source_markdown = """abc\a\a
\\\\This is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):  :\n]",
        "[text(2,1):\\\b\\This is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
\\This is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_04b() -> None:
    """
    Test case extra 04b:  Hard line break followed by entity
    """

    # Arrange
    source_markdown = """abc\a\a
&copy; This is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):  :\n]",
        "[text(2,1):\a&copy;\a©\a This is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
© This is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_04c() -> None:
    """
    Test case extra 04c:  Hard line break followed by code span
    """

    # Arrange
    source_markdown = """abc\a\a
`This` is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):  :\n]",
        "[icode-span(2,1):This:`::]",
        "[text(2,7): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<code>This</code> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_04d() -> None:
    """
    Test case extra 04d:  Hard line break followed by emphasis
    """

    # Arrange
    source_markdown = """abc\a\a
*This* is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):  :\n]",
        "[emphasis(2,1):1:*]",
        "[text(2,2):This:]",
        "[end-emphasis(2,6)::]",
        "[text(2,7): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<em>This</em> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_04e() -> None:
    """
    Test case extra 04e:  Hard line break followed by link
    """

    # Arrange
    source_markdown = """abc\a\a
[This](foo.com) is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):  :\n]",
        "[link(2,1):inline:foo.com:::::This:False::::]",
        "[text(2,2):This:]",
        "[end-link::]",
        "[text(2,16): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<a href="foo.com">This</a> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_04f() -> None:
    """
    Test case extra 04f:  Hard line break followed by link
    """

    # Arrange
    source_markdown = """abc\a\a
![This](foo.com) is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):  :\n]",
        "[image(2,1):inline:foo.com::This::::This:False::::]",
        "[text(2,17): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<img src="foo.com" alt="This" /> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_04g() -> None:
    """
    Test case extra 04g:  Hard line break followed by autolink
    """

    # Arrange
    source_markdown = """abc\a\a
<http://this.com> is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):  :\n]",
        "[uri-autolink(2,1):http://this.com]",
        "[text(2,18): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<a href="http://this.com">http://this.com</a> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_04h() -> None:
    """
    Test case extra 04h:  Hard line break followed by autolink
    """

    # Arrange
    source_markdown = """abc\a\a
<this> is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):  :\n]",
        "[raw-html(2,1):this]",
        "[text(2,7): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<this> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_04i() -> None:
    """
    Test case extra 04i:  Hard line break followed by hard line break
    """

    # Arrange
    source_markdown = """abc\a\a
\a\a
this is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1)::  ]",
        "[text(1,1):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):  ]",
        "[para(3,1):]",
        "[text(3,1):this is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc</p>
<p>this is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_05x() -> None:
    """
    Test case extra 05:  Hard line break followed by space and emphasis
    """

    # Arrange
    source_markdown = """abc\a\a
   *this* is new.""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):  :\n]",
        "[emphasis(2,4):1:*]",
        "[text(2,5):this:]",
        "[end-emphasis(2,9)::]",
        "[text(2,10): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<em>this</em> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_hard_line_breaks_extra_05a() -> None:
    """
    Test case extra 05a:  Hard line break followed by space and emphasis
    """

    # Arrange
    source_markdown = """abc\\
   *this* is new."""
    expected_tokens = [
        "[para(1,1):\n   ]",
        "[text(1,1):abc:]",
        "[hard-break(1,4):\\:\n]",
        "[emphasis(2,4):1:*]",
        "[text(2,5):this:]",
        "[end-emphasis(2,9)::]",
        "[text(2,10): is new.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc<br />
<em>this</em> is new.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
