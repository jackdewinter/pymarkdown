"""
https://github.github.com/gfm/#setext-headings
"""
from test.utils import act_and_assert

import pytest


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_setext_headings_050():
    """
    Test case 050:  Simple examples:
    """

    # Arrange
    source_markdown = """Foo *bar*
=========

Foo *bar*
---------"""
    expected_tokens = [
        "[setext(2,1):=:9::(1,1)]",
        "[text(1,1):Foo :]",
        "[emphasis(1,5):1:*]",
        "[text(1,6):bar:]",
        "[end-emphasis(1,9)::]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[setext(5,1):-:9::(4,1)]",
        "[text(4,1):Foo :]",
        "[emphasis(4,5):1:*]",
        "[text(4,6):bar:]",
        "[end-emphasis(4,9)::]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>Foo <em>bar</em></h1>
<h2>Foo <em>bar</em></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_051():
    """
    Test case 051:  The content of the heading may span more than one line:
    """

    # Arrange
    source_markdown = """Foo *bar
baz*
===="""
    expected_tokens = [
        "[setext(3,1):=:4::(1,1)]",
        "[text(1,1):Foo :]",
        "[emphasis(1,5):1:*]",
        "[text(1,6):bar\nbaz::\n]",
        "[end-emphasis(2,4)::]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>Foo <em>bar
baz</em></h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_052xx():
    """
    Test case 052:  The heading’s raw content is formed by concatenating the lines
                    and removing initial and final whitespace.
    """

    # Arrange
    source_markdown = """  Foo *bar
baz*\t
===="""
    expected_tokens = [
        "[setext(3,1):=:4:  :(1,3):\t]",
        "[text(1,3):Foo :]",
        "[emphasis(1,7):1:*]",
        "[text(1,8):bar\nbaz::\n]",
        "[end-emphasis(2,4)::]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>Foo <em>bar
baz</em></h1>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        allow_alternate_markdown=False,
        show_debug=False,
    )


@pytest.mark.gfm
def test_setext_headings_052xa():
    """
    Test case 052:  The heading’s raw content is formed by concatenating the lines
                    and removing initial and final whitespace.
    """

    # Arrange
    source_markdown = """  Foo *bar
baz*\a\a
====""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):=:4:  :(1,3):  ]",
        "[text(1,3):Foo :]",
        "[emphasis(1,7):1:*]",
        "[text(1,8):bar\nbaz::\n]",
        "[end-emphasis(2,4)::]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>Foo <em>bar
baz</em></h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_052a():
    """
    Test case 052a:  variation of 52 to deal with multiple lines that start with whitespace.
    """

    # Arrange
    source_markdown = """  a
  b
  c
==="""
    expected_tokens = [
        "[setext(4,1):=:3:  :(1,3)]",
        "[text(1,3):a\nb\nc::\n  \x02\n  \x02]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>a
b
c</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_052b():
    """
    Test case 052b:  variation of 52a with extra trailing spaces
    """

    # Arrange
    source_markdown = """  a\a
  b\a
  c
===""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(4,1):=:3:  :(1,3)]",
        "[text(1,3):a\nb\nc:: \n  \x02 \n  \x02]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>a
b
c</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_052c():
    """
    Test case 052c:  variation of 52 with more trailing spaces
    """

    # Arrange
    source_markdown = """  a\a
  b\a\a
  c
===""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(4,1):=:3:  :(1,3)]",
        "[text(1,3):a\nb:: \n  \x02]",
        "[hard-break(2,4):  :\n]",
        "[text(3,3):c::  \x02]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>a
b<br />
c</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_052d():
    """
    Test case 052d:  variation of 52 with inline emphasis
    """

    # Arrange
    source_markdown = """  a\a
  *b*\a
  c
===""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(4,1):=:3:  :(1,3)]",
        "[text(1,3):a\n:: \n  \x02]",
        "[emphasis(2,3):1:*]",
        "[text(2,4):b:]",
        "[end-emphasis(2,5)::]",
        "[text(2,6):\nc:: \n  \x02]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>a
<em>b</em>
c</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_052ex():
    """
    Test case 052e:  variation of 52 with inline emphasis and trailing space
    """

    # Arrange
    source_markdown = """  a\a
  *b*\a\a
  c
===""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(4,1):=:3:  :(1,3)]",
        "[text(1,3):a\n:: \n  \x02]",
        "[emphasis(2,3):1:*]",
        "[text(2,4):b:]",
        "[end-emphasis(2,5)::]",
        "[hard-break(2,6):  :\n]",
        "[text(3,3):c::  \x02]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>a
<em>b</em><br />
c</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_052ea():
    """
    Test case 052ea:  variation of 52e with more
    """

    # Arrange
    source_markdown = """  a\a
  *b*\a\a
  a\a
  *b*\a\a
  c
===""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(6,1):=:3:  :(1,3)]",
        "[text(1,3):a\n:: \n  \x02]",
        "[emphasis(2,3):1:*]",
        "[text(2,4):b:]",
        "[end-emphasis(2,5)::]",
        "[hard-break(2,6):  :\n]",
        "[text(3,3):a\n::  \x02 \n  \x02]",
        "[emphasis(4,3):1:*]",
        "[text(4,4):b:]",
        "[end-emphasis(4,5)::]",
        "[hard-break(4,6):  :\n]",
        "[text(5,3):c::  \x02]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>a
<em>b</em><br />
a
<em>b</em><br />
c</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_052eb():
    """
    Test case 052eb:  variation of 52e with even more
    """

    # Arrange
    source_markdown = """ a\a
 *b*\a\a
  a\a
  *b*\a\a
   a\a
   *b*\a\a
c
===""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(8,1):=:3: :(1,2)]",
        "[text(1,2):a\n:: \n \x02]",
        "[emphasis(2,2):1:*]",
        "[text(2,3):b:]",
        "[end-emphasis(2,4)::]",
        "[hard-break(2,5):  :\n]",
        "[text(3,3):a\n::  \x02 \n  \x02]",
        "[emphasis(4,3):1:*]",
        "[text(4,4):b:]",
        "[end-emphasis(4,5)::]",
        "[hard-break(4,6):  :\n]",
        "[text(5,4):a\n::   \x02 \n   \x02]",
        "[emphasis(6,4):1:*]",
        "[text(6,5):b:]",
        "[end-emphasis(6,6)::]",
        "[hard-break(6,7):  :\n]",
        "[text(7,1):c:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>a
<em>b</em><br />
a
<em>b</em><br />
a
<em>b</em><br />
c</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_052f():
    """
    Test case 052f:  variation of 52f with more
    """

    # Arrange
    source_markdown = """  a\a
   *b*\a\a
 c
===""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(4,1):=:3:  :(1,3)]",
        "[text(1,3):a\n:: \n   \x02]",
        "[emphasis(2,4):1:*]",
        "[text(2,5):b:]",
        "[end-emphasis(2,6)::]",
        "[hard-break(2,7):  :\n]",
        "[text(3,2):c:: \x02]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>a
<em>b</em><br />
c</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_053():
    """
    Test case 053:  The underlining can be any length:
    """

    # Arrange
    source_markdown = """Foo
-------------------------

Foo
="""
    expected_tokens = [
        "[setext(2,1):-:25::(1,1)]",
        "[text(1,1):Foo:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[setext(5,1):=:1::(4,1)]",
        "[text(4,1):Foo:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>Foo</h2>
<h1>Foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_054():
    """
    Test case 054:  The heading content can be indented up to three spaces, and need not line up with the underlining:
    """

    # Arrange
    source_markdown = """   Foo
---

  Foo
-----

  Foo
  ==="""
    expected_tokens = [
        "[setext(2,1):-:3:   :(1,4)]",
        "[text(1,4):Foo:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[setext(5,1):-:5:  :(4,3)]",
        "[text(4,3):Foo:]",
        "[end-setext::]",
        "[BLANK(6,1):]",
        "[setext(8,3):=:3:  :(7,3)]",
        "[text(7,3):Foo:]",
        "[end-setext:  :]",
    ]
    expected_gfm = """<h2>Foo</h2>
<h2>Foo</h2>
<h1>Foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_055():
    """
    Test case 055:  Four spaces indent is too much:
    """

    # Arrange
    source_markdown = """    Foo
    ---

    Foo
---"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n\n    ]",
        "[text(1,5):Foo\n---\n\x03\nFoo:]",
        "[end-icode-block:::False]",
        "[tbreak(5,1):-::---]",
    ]
    expected_gfm = """<pre><code>Foo
---

Foo
</code></pre>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_056():
    """
    Test case 056:  The setext heading underline can be indented up to three spaces, and may have trailing spaces:
    """

    # Arrange
    source_markdown = """Foo
   ----      """
    expected_tokens = [
        "[setext(2,4):-:4::(1,1)]",
        "[text(1,1):Foo:]",
        "[end-setext:   :      ]",
    ]
    expected_gfm = """<h2>Foo</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_057():
    """
    Test case 057:  Four spaces is too much:
    """

    # Arrange
    source_markdown = """Foo
    ---"""
    expected_tokens = [
        "[para(1,1):\n    ]",
        "[text(1,1):Foo\n---::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo
---</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_058():
    """
    Test case 058:  The setext heading underline cannot contain internal spaces:
    """

    # Arrange
    source_markdown = """Foo
= =

Foo
--- -"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):Foo\n= =::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):Foo:]",
        "[end-para:::False]",
        "[tbreak(5,1):-::--- -]",
    ]
    expected_gfm = """<p>Foo
= =</p>
<p>Foo</p>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_059():
    """
    Test case 059:  Trailing spaces in the content line do not cause a line break:
    """

    # Arrange
    source_markdown = """Foo\a\a
-----""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(2,1):-:5::(1,1):  ]",
        "[text(1,1):Foo:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>Foo</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_060():
    """
    Test case 060:  Nor does a backslash at the end:
    """

    # Arrange
    source_markdown = """Foo\\
----"""
    expected_tokens = [
        "[setext(2,1):-:4::(1,1)]",
        "[text(1,1):Foo\\:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>Foo\\</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_061():
    """
    Test case 061:  Since indicators of block structure take precedence over indicators
                    of inline structure, the following are setext headings:
    """

    # Arrange
    source_markdown = """`Foo
----
`

<a title="a lot
---
of dashes"/>"""
    expected_tokens = [
        "[setext(2,1):-:4::(1,1)]",
        "[text(1,1):`Foo:]",
        "[end-setext::]",
        "[para(3,1):]",
        "[text(3,1):`:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[setext(6,1):-:3::(5,1)]",
        '[text(5,1):\a<\a&lt;\aa title=\a"\a&quot;\aa lot:]',
        "[end-setext::]",
        "[para(7,1):]",
        '[text(7,1):of dashes\a"\a&quot;\a/\a>\a&gt;\a:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<h2>`Foo</h2>
<p>`</p>
<h2>&lt;a title=&quot;a lot</h2>
<p>of dashes&quot;/&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_062():
    """
    Test case 062:  (part a) The setext heading underline cannot be a lazy continuation
                    line in a list item or block quote:
    """

    # Arrange
    source_markdown = """> Foo
---"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):Foo:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(2,1):-::---]",
    ]
    expected_gfm = """<blockquote>
<p>Foo</p>
</blockquote>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_063():
    """
    Test case 063:  (part b) The setext heading underline cannot be a lazy continuation
    line in a list item or block quote:
    """

    # Arrange
    source_markdown = """> foo
bar
==="""
    expected_tokens = [
        "[block-quote(1,1)::> \n\n]",
        "[para(1,3):\n\n]",
        "[text(1,3):foo\nbar\n===::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo
bar
===</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_064():
    """
    Test case 064:  (part c) The setext heading underline cannot be a lazy continuation
                    line in a list item or block quote:
    """

    # Arrange
    source_markdown = """- Foo
---"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):Foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(2,1):-::---]",
    ]
    expected_gfm = """<ul>
<li>Foo</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_064a():
    """
    Test case 064a:  variation of 64 other underline
    """

    # Arrange
    source_markdown = """- Foo
==="""

    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n]",
        "[text(1,3):Foo\n===::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Foo
===</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_064b():
    """
    Test case 064a:  variation of 64 other underline
    """

    # Arrange
    source_markdown = """- Foo
 ==="""

    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n ]",
        "[text(1,3):Foo\n===::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Foo
===</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_064ba():
    """
    Test case 064a:  variation of 64 other underline
    """

    # Arrange
    source_markdown = """1. Foo
 ==="""

    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n ]",
        "[text(1,4):Foo\n===::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Foo
===</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_064c():
    """
    Test case 064a:  variation of 64 other underline
    """

    # Arrange
    source_markdown = """- Foo
  ==="""

    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):=:3::(1,3)]",
        "[text(1,3):Foo:]",
        "[end-setext::]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h1>Foo</h1>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_065():
    """
    Test case 065:  A blank line is needed between a paragraph and a following
                    setext heading, since otherwise the paragraph becomes part
                    of the heading’s content:
    """

    # Arrange
    source_markdown = """Foo
Bar
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):Foo\nBar::\n]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>Foo
Bar</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_066():
    """
    Test case 066:  A blank line is needed between a paragraph and a following
                    setext heading, since otherwise the paragraph becomes part
                    of the heading’s content:
    """

    # Arrange
    source_markdown = """---
Foo
---
Bar
---
Baz"""
    expected_tokens = [
        "[tbreak(1,1):-::---]",
        "[setext(3,1):-:3::(2,1)]",
        "[text(2,1):Foo:]",
        "[end-setext::]",
        "[setext(5,1):-:3::(4,1)]",
        "[text(4,1):Bar:]",
        "[end-setext::]",
        "[para(6,1):]",
        "[text(6,1):Baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<hr />
<h2>Foo</h2>
<h2>Bar</h2>
<p>Baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_067():
    """
    Test case 067:  Setext headings cannot be empty:
    """

    # Arrange
    source_markdown = """
===="""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[para(2,1):]",
        "[text(2,1):====:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>====</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_068():
    """
    Test case 068:  (part a) Setext heading text lines must not be interpretable
                    as block constructs other than paragraphs. So, the line of
                    dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    source_markdown = """---
---"""
    expected_tokens = ["[tbreak(1,1):-::---]", "[tbreak(2,1):-::---]"]
    expected_gfm = """<hr />
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_069():
    """
    Test case 069:  (part b) Setext heading text lines must not be interpretable
                    as block constructs other than paragraphs. So, the line of
                    dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    source_markdown = """- foo
-----"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(2,1):-::-----]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_069a():
    """
    Test case 069a: variation of 069 with other underline
    """

    # Arrange
    source_markdown = """- foo
====="""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n]",
        "[text(1,3):foo\n=====::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo
=====</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_070():
    """
    Test case 070:  (part c) Setext heading text lines must not be interpretable
                    as block constructs other than paragraphs. So, the line of
                    dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    source_markdown = """    foo
---"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):foo:]",
        "[end-icode-block:::False]",
        "[tbreak(2,1):-::---]",
    ]
    expected_gfm = """<pre><code>foo
</code></pre>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_071():
    """
    Test case 071:  (part d) Setext heading text lines must not be interpretable
                    as block constructs other than paragraphs. So, the line of
                    dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    source_markdown = """> foo
-----"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(2,1):-::-----]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
</blockquote>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_072():
    """
    Test case 072:  If you want a heading with > foo as its literal text, you can use backslash escapes:
    """

    # Arrange
    source_markdown = """\\> foo
------"""
    expected_tokens = [
        "[setext(2,1):-:6::(1,1)]",
        "[text(1,1):\\\b\a>\a&gt;\a foo:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>&gt; foo</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_073():
    """
    Test case 073:  Authors who want interpretation 1 can put a blank line after the first paragraph:
    https://github.github.com/gfm/#example-73
    """

    # Arrange
    source_markdown = """Foo

bar
---
baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[setext(4,1):-:3::(3,1)]",
        "[text(3,1):bar:]",
        "[end-setext::]",
        "[para(5,1):]",
        "[text(5,1):baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo</p>
<h2>bar</h2>
<p>baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_074():
    """
    Test case 074:  Authors who want interpretation 2 can put blank lines around the thematic break,
    https://github.github.com/gfm/#example-74
    """

    # Arrange
    source_markdown = """Foo
bar

---

baz"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):Foo\nbar::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
        "[para(6,1):]",
        "[text(6,1):baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo
bar</p>
<hr />
<p>baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_075():
    """
    Test case 075:  or use a thematic break that cannot count as a setext heading underline, such as
    https://github.github.com/gfm/#example-75
    """

    # Arrange
    source_markdown = """Foo
bar
* * *
baz"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):Foo\nbar::\n]",
        "[end-para:::False]",
        "[tbreak(3,1):*::* * *]",
        "[para(4,1):]",
        "[text(4,1):baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo
bar</p>
<hr />
<p>baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_076():
    """
    Test case 076:  Authors who want interpretation 3 can use backslash escapes:
    https://github.github.com/gfm/#example-76
    """

    # Arrange
    source_markdown = """Foo
bar
\\---
baz"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):Foo\nbar\n\\\b---\nbaz::\n\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo
bar
---
baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
