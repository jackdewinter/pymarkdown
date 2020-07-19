"""
https://github.github.com/gfm/#setext-headings
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_setext_headings_050():
    """
    Test case 050:  Simple examples:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo *bar*
=========

Foo *bar*
---------"""
    expected_tokens = [
        "[setext(2,1):=::(1,1)]",
        "[text:Foo :]",
        "[emphasis:1]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[setext(5,1):-::(4,1)]",
        "[text:Foo :]",
        "[emphasis:1]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>Foo <em>bar</em></h1>
<h2>Foo <em>bar</em></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_051():
    """
    Test case 051:  The content of the heading may span more than one line:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo *bar
baz*
===="""
    expected_tokens = [
        "[setext(3,1):=::(1,1)]",
        "[text:Foo :]",
        "[emphasis:1]",
        "[text:bar\nbaz::\n]",
        "[end-emphasis::1]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>Foo <em>bar
baz</em></h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_052():
    """
    Test case 052:  The heading’s raw content is formed by concatenating the lines and removing initial and final whitespace.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  Foo *bar
baz*\t
===="""
    expected_tokens = [
        "[setext(3,1):=:  :(1,3):\t]",
        "[text:Foo :]",
        "[emphasis:1]",
        "[text:bar\nbaz::\n]",
        "[end-emphasis::1]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>Foo <em>bar
baz</em></h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_052a():
    """
    Test case 052a:  Deal with multiple lines that start with whitespace.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  a
  b
  c
==="""
    expected_tokens = [
        "[setext(4,1):=:  :(1,3)]",
        "[text:a\nb\nc::\n  \n  ]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>a
b
c</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_052b():
    """
    Test case 052a:  Deal with multiple lines that start with whitespace.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  a\a\a
  b\a\a
  c
===""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(4,1):=:  :(1,3)]",
        "[text:a::  ]",
        "[hard-break:  ]",
        "[text:\nb::\n  ]",
        "[hard-break:  ]",
        "[text:\nc::\n]",
        "[end-setext::]",
    ]
    expected_gfm = """<h1>a<br />
b<br />
c</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_053():
    """
    Test case 053:  The underlining can be any length:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
-------------------------

Foo
="""
    expected_tokens = [
        "[setext(2,1):-::(1,1)]",
        "[text:Foo:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[setext(5,1):=::(4,1)]",
        "[text:Foo:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>Foo</h2>
<h1>Foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_054():
    """
    Test case 054:  The heading content can be indented up to three spaces, and need not line up with the underlining:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   Foo
---

  Foo
-----

  Foo
  ==="""
    expected_tokens = [
        "[setext(2,1):-:   :(1,4)]",
        "[text:Foo:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[setext(5,1):-:  :(4,3)]",
        "[text:Foo:]",
        "[end-setext::]",
        "[BLANK(6,1):]",
        "[setext(8,3):=:  :(7,3)]",
        "[text:Foo:]",
        "[end-setext:  :]",
    ]
    expected_gfm = """<h2>Foo</h2>
<h2>Foo</h2>
<h1>Foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_055():
    """
    Test case 055:  Four spaces indent is too much:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    Foo
    ---

    Foo
---"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n\n    ]",
        "[text:Foo\n---\n\nFoo:]",
        "[end-icode-block]",
        "[tbreak(5,1):-::---]",
    ]
    expected_gfm = """<pre><code>Foo
---

Foo
</code></pre>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_056():
    """
    Test case 056:  The setext heading underline can be indented up to three spaces, and may have trailing spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
   ----      """
    expected_tokens = [
        "[setext(2,4):-::(1,1)]",
        "[text:Foo:]",
        "[end-setext:   :      ]",
    ]
    expected_gfm = """<h2>Foo</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_057():
    """
    Test case 057:  Four spaces is too much:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
    ---"""
    expected_tokens = ["[para(1,1):\n    ]", "[text:Foo\n---::\n]", "[end-para]"]
    expected_gfm = """<p>Foo
---</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_058():
    """
    Test case 058:  The setext heading underline cannot contain internal spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
= =

Foo
--- -"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text:Foo\n= =::\n]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text:Foo:]",
        "[end-para]",
        "[tbreak(5,1):-::--- -]",
    ]
    expected_gfm = """<p>Foo
= =</p>
<p>Foo</p>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_059():
    """
    Test case 059:  Trailing spaces in the content line do not cause a line break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo\a\a
-----""".replace(
        "\a", " "
    )
    expected_tokens = ["[setext(2,1):-::(1,1):  ]", "[text:Foo:]", "[end-setext::]"]
    expected_gfm = """<h2>Foo</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_060():
    """
    Test case 060:  Nor does a backslash at the end:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo\\
----"""
    expected_tokens = ["[setext(2,1):-::(1,1)]", "[text:Foo\\:]", "[end-setext::]"]
    expected_gfm = """<h2>Foo\\</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_061():
    """
    Test case 061:  Since indicators of block structure take precedence over indicators of inline structure, the following are setext headings:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """`Foo
----
`

<a title="a lot
---
of dashes"/>"""
    expected_tokens = [
        "[setext(2,1):-::(1,1)]",
        "[text:`Foo:]",
        "[end-setext::]",
        "[para(3,1):]",
        "[text:`:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[setext(6,1):-::(5,1)]",
        '[text:\a<\a&lt;\aa title=\a"\a&quot;\aa lot:]',
        "[end-setext::]",
        "[para(7,1):]",
        '[text:of dashes\a"\a&quot;\a/\a>\a&gt;\a:]',
        "[end-para]",
    ]
    expected_gfm = """<h2>`Foo</h2>
<p>`</p>
<h2>&lt;a title=&quot;a lot</h2>
<p>of dashes&quot;/&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_062():
    """
    Test case 062:  (part a) The setext heading underline cannot be a lazy continuation line in a list item or block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> Foo
---"""
    expected_tokens = [
        "[block-quote(1,1):]",
        "[para(1,3):]",
        "[text:Foo:]",
        "[end-para]",
        "[end-block-quote]",
        "[tbreak(2,1):-::---]",
    ]
    expected_gfm = """<blockquote>
<p>Foo</p>
</blockquote>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_063():
    """
    Test case 063:  (part b) The setext heading underline cannot be a lazy continuation line in a list item or block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
bar
==="""
    expected_tokens = [
        "[block-quote(1,1):]",
        "[para(1,3):\n\n]",
        "[text:foo\nbar\n===::\n\n]",
        "[end-para]",
        "[end-block-quote]",
    ]
    expected_gfm = """<blockquote>
<p>foo
bar
===</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_064():
    """
    Test case 064:  (part c) The setext heading underline cannot be a lazy continuation line in a list item or block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- Foo
---"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:Foo:]",
        "[end-para]",
        "[end-ulist]",
        "[tbreak(2,1):-::---]",
    ]
    expected_gfm = """<ul>
<li>Foo</li>
</ul>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_064a():
    """
    Test case 064a:  064 with with other underline
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- Foo
---"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:Foo:]",
        "[end-para]",
        "[end-ulist]",
        "[tbreak(2,1):-::---]",
    ]
    expected_gfm = """<ul>
<li>Foo</li>
</ul>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_065():
    """
    Test case 065:  A blank line is needed between a paragraph and a following setext heading, since otherwise the paragraph becomes part of the heading’s content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
Bar
---"""
    expected_tokens = [
        "[setext(3,1):-::(1,1)]",
        "[text:Foo\nBar::\n]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>Foo
Bar</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_066():
    """
    Test case 066:  A blank line is needed between a paragraph and a following setext heading, since otherwise the paragraph becomes part of the heading’s content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """---
Foo
---
Bar
---
Baz"""
    expected_tokens = [
        "[tbreak(1,1):-::---]",
        "[setext(3,1):-::(2,1)]",
        "[text:Foo:]",
        "[end-setext::]",
        "[setext(5,1):-::(4,1)]",
        "[text:Bar:]",
        "[end-setext::]",
        "[para(6,1):]",
        "[text:Baz:]",
        "[end-para]",
    ]
    expected_gfm = """<hr />
<h2>Foo</h2>
<h2>Bar</h2>
<p>Baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_067():
    """
    Test case 067:  Setext headings cannot be empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """
===="""
    expected_tokens = ["[BLANK(1,1):]", "[para(2,1):]", "[text:====:]", "[end-para]"]
    expected_gfm = """<p>====</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_068():
    """
    Test case 068:  (part a) Setext heading text lines must not be interpretable as block constructs other than paragraphs. So, the line of dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """---
---"""
    expected_tokens = ["[tbreak(1,1):-::---]", "[tbreak(2,1):-::---]"]
    expected_gfm = """<hr />
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_069():
    """
    Test case 069:  (part b) Setext heading text lines must not be interpretable as block constructs other than paragraphs. So, the line of dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo
-----"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
        "[tbreak(2,1):-::-----]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
</ul>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_069a():
    """
    Test case 069a:  069 with other underline
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo
-----"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
        "[tbreak(2,1):-::-----]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
</ul>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_070():
    """
    Test case 070:  (part c) Setext heading text lines must not be interpretable as block constructs other than paragraphs. So, the line of dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    foo
---"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text:foo:]",
        "[end-icode-block]",
        "[tbreak(2,1):-::---]",
    ]
    expected_gfm = """<pre><code>foo
</code></pre>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_071():
    """
    Test case 071:  (part d) Setext heading text lines must not be interpretable as block constructs other than paragraphs. So, the line of dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
-----"""
    expected_tokens = [
        "[block-quote(1,1):]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[end-block-quote]",
        "[tbreak(2,1):-::-----]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
</blockquote>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_072():
    """
    Test case 072:  If you want a heading with > foo as its literal text, you can use backslash escapes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\> foo
------"""
    expected_tokens = [
        "[setext(2,1):-::(1,1)]",
        "[text:\\\b\a>\a&gt;\a foo:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>&gt; foo</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_073():
    """
    Test case 073:  Authors who want interpretation 1 can put a blank line after the first paragraph:
    https://github.github.com/gfm/#example-73
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo

bar
---
baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:Foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[setext(4,1):-::(3,1)]",
        "[text:bar:]",
        "[end-setext::]",
        "[para(5,1):]",
        "[text:baz:]",
        "[end-para]",
    ]
    expected_gfm = """<p>Foo</p>
<h2>bar</h2>
<p>baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_074():
    """
    Test case 074:  Authors who want interpretation 2 can put blank lines around the thematic break,
    https://github.github.com/gfm/#example-74
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
bar

---

baz"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text:Foo\nbar::\n]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
        "[para(6,1):]",
        "[text:baz:]",
        "[end-para]",
    ]
    expected_gfm = """<p>Foo
bar</p>
<hr />
<p>baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_075():
    """
    Test case 075:  or use a thematic break that cannot count as a setext heading underline, such as
    https://github.github.com/gfm/#example-75
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
bar
* * *
baz"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text:Foo\nbar::\n]",
        "[end-para]",
        "[tbreak(3,1):*::* * *]",
        "[para(4,1):]",
        "[text:baz:]",
        "[end-para]",
    ]
    expected_gfm = """<p>Foo
bar</p>
<hr />
<p>baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_076():
    """
    Test case 076:  Authors who want interpretation 3 can use backslash escapes:
    https://github.github.com/gfm/#example-76
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
bar
\\---
baz"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text:Foo\nbar\n\\\b---\nbaz::\n\n\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>Foo
bar
---
baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
