"""
https://github.github.com/gfm/#setext-headings
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_setext_headings_050():
    """
    Test case 050:  Simple examples:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo *bar*
=========

Foo *bar*
---------"""
    expected_tokens = [
        "[setext:=:]",
        "[text:Foo *bar*:]",
        "[end-setext::]",
        "[BLANK:]",
        "[setext:-:]",
        "[text:Foo *bar*:]",
        "[end-setext::]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when inline emphasis implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_051():
    """
    Test case 051:  The content of the header may span more than one line:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo *bar
baz*
===="""
    expected_tokens = [
        "[setext:=:]",
        "[text:Foo *bar\nbaz*:]",
        "[end-setext::]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_052():
    """
    Test case 052:  The heading’s raw content is formed by concatenating the lines and removing initial and final whitespace.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  Foo *bar
baz*\t
===="""
    expected_tokens = [
        "[setext:=:  ]",
        "[text:Foo *bar\nbaz*    :]",
        "[end-setext::]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when inline emphasis implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_053():
    """
    Test case 053:  The underlining can be any length:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
-------------------------

Foo
="""
    expected_tokens = [
        "[setext:-:]",
        "[text:Foo:]",
        "[end-setext::]",
        "[BLANK:]",
        "[setext:=:]",
        "[text:Foo:]",
        "[end-setext::]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_054():
    """
    Test case 054:  The heading content can be indented up to three spaces, and need not line up with the underlining:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """   Foo
---

  Foo
-----

  Foo
  ==="""
    expected_tokens = [
        "[setext:-:   ]",
        "[text:Foo:]",
        "[end-setext::]",
        "[BLANK:]",
        "[setext:-:  ]",
        "[text:Foo:]",
        "[end-setext::]",
        "[BLANK:]",
        "[setext:=:  ]",
        "[text:Foo:]",
        "[end-setext:  :]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_055():
    """
    Test case 055:  Four spaces indent is too much:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    Foo
    ---

    Foo
---"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:Foo\n    ---:]",
        "[BLANK:]",
        "[text:Foo:    ]",
        "[end-icode-block]",
        "[tbreak:-::---]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_056():
    """
    Test case 056:  The setext heading underline can be indented up to three spaces, and may have trailing spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
   ----      """
    expected_tokens = ["[setext:-:]", "[text:Foo:]", "[end-setext:   :      ]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_057():
    """
    Test case 057:  Four spaces is too much:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
    ---"""
    expected_tokens = ["[para:]", "[text:Foo\n    ---:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_058():
    """
    Test case 058:  The setext heading underline cannot contain internal spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
= =

Foo
--- -"""
    expected_tokens = [
        "[para:]",
        "[text:Foo\n= =:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:Foo:]",
        "[end-para]",
        "[tbreak:-::--- -]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


# pylint: disable=trailing-whitespace
def test_setext_headings_059():
    """
    Test case 059:  Trailing spaces in the content line do not cause a line break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo  
-----"""
    expected_tokens = ["[setext:-:]", "[text:Foo  :]", "[end-setext::]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_060():
    """
    Test case 060:  Nor does a backslash at the end:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo\
----"""
    expected_tokens = ["[para:]", "[text:Foo----:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_061():
    """
    Test case 061:  Since indicators of block structure take precedence over indicators of inline structure, the following are setext headings:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`Foo
----
`

<a title="a lot
---
of dashes"/>"""
    expected_tokens = [
        "[setext:-:]",
        "[text:`Foo:]",
        "[end-setext::]",
        "[para:]",
        "[text:`:]",
        "[end-para]",
        "[BLANK:]",
        "[setext:-:]",
        "[text:&lt;a title=&quot;a lot:]",
        "[end-setext::]",
        "[para:]",
        "[text:of dashes&quot;/&gt;:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_062():
    """
    Test case 062:  (part a) The setext heading underline cannot be a lazy continuation line in a list item or block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> Foo
---"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:Foo:]",
        "[end-para]",
        "[end-block-quote]",
        "[tbreak:-::---]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_063():
    """
    Test case 063:  (part b) The setext heading underline cannot be a lazy continuation line in a list item or block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> foo
bar
==="""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:foo\nbar:]",
        "[end-para]",
        "[end-block-quote]",
        "[para:]",
        "[text:===:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_064():
    """
    Test case 064:  (part c) The setext heading underline cannot be a lazy continuation line in a list item or block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- Foo
---"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:Foo:]",
        "[end-para]",
        "[end-ulist]",
        "[tbreak:-::---]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_064a():
    """
    Test case 064a:  064 with with other underline
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- Foo
---"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:Foo:]",
        "[end-para]",
        "[end-ulist]",
        "[tbreak:-::---]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_065():
    """
    Test case 065:  A blank line is needed between a paragraph and a following setext heading, since otherwise the paragraph becomes part of the heading’s content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
Bar
---"""
    expected_tokens = ["[setext:-:]", "[text:Foo\nBar:]", "[end-setext::]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_066():
    """
    Test case 066:  A blank line is needed between a paragraph and a following setext heading, since otherwise the paragraph becomes part of the heading’s content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """---
Foo
---
Bar
---
Baz"""
    expected_tokens = [
        "[tbreak:-::---]",
        "[setext:-:]",
        "[text:Foo:]",
        "[end-setext::]",
        "[setext:-:]",
        "[text:Bar:]",
        "[end-setext::]",
        "[para:]",
        "[text:Baz:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_067():
    """
    Test case 067:  Setext headings cannot be empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """
===="""
    expected_tokens = ["[BLANK:]", "[para:]", "[text:====:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_068():
    """
    Test case 068:  (part a) Setext heading text lines must not be interpretable as block constructs other than paragraphs. So, the line of dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """---
---"""
    expected_tokens = ["[tbreak:-::---]", "[tbreak:-::---]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_069():
    """
    Test case 069:  (part b) Setext heading text lines must not be interpretable as block constructs other than paragraphs. So, the line of dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
-----"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
        "[tbreak:-::-----]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_069a():
    """
    Test case 069a:  069 with other underline
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
-----"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
        "[tbreak:-::-----]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_070():
    """
    Test case 070:  (part c) Setext heading text lines must not be interpretable as block constructs other than paragraphs. So, the line of dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    foo
---"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[tbreak:-::---]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_071():
    """
    Test case 071:  (part d) Setext heading text lines must not be interpretable as block constructs other than paragraphs. So, the line of dashes in these examples gets interpreted as a thematic break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> foo
-----"""
    expected_tokens = [
        "[block-quote:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-block-quote]",
        "[tbreak:-::-----]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_072():
    """
    Test case 072:  If you want a heading with > foo as its literal text, you can use backslash escapes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """\\> foo
------"""
    expected_tokens = ["[setext:-:]", "[text:&gt; foo:]", "[end-setext::]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_073():
    """
    Test case 073:  Authors who want interpretation 1 can put a blank line after the first paragraph:
    https://github.github.com/gfm/#example-73
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo

bar
---
baz"""
    expected_tokens = [
        "[para:]",
        "[text:Foo:]",
        "[end-para]",
        "[BLANK:]",
        "[setext:-:]",
        "[text:bar:]",
        "[end-setext::]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_074():
    """
    Test case 074:  Authors who want interpretation 2 can put blank lines around the thematic break,
    https://github.github.com/gfm/#example-74
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
bar

---

baz"""
    expected_tokens = [
        "[para:]",
        "[text:Foo\nbar:]",
        "[end-para]",
        "[BLANK:]",
        "[tbreak:-::---]",
        "[BLANK:]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_075():
    """
    Test case 075:  or use a thematic break that cannot count as a setext heading underline, such as
    https://github.github.com/gfm/#example-75
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
bar
* * *
baz"""
    expected_tokens = [
        "[para:]",
        "[text:Foo\nbar:]",
        "[end-para]",
        "[tbreak:*::* * *]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_setext_headings_076():
    """
    Test case 076:  Authors who want interpretation 3 can use backslash escapes:
    https://github.github.com/gfm/#example-76
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
bar
\\---
baz"""
    expected_tokens = [
        "[para:]",
        "[text:Foo\nbar\n---\nbaz:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
