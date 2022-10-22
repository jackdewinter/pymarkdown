"""
https://github.com/jackdewinter/pymarkdown/issues/456
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_block_quotes_with_spaces():
    """
    Test case:  Block quotes preceeded by spaces.
    """

    # Arrange
    source_markdown = """   > block quote"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[para(1,6):]",
        "[text(1,6):block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>block quote</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_block_quotes_with_tabs():
    """
    Test case:  Block quotes preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ > block quote
 >\t> another block quote"""
    expected_tokens = [
        "[block-quote(1,2): : > \n > ]",
        "[para(1,4):]",
        "[text(1,4):block quote:]",
        "[end-para:::True]",
        "[block-quote(2,5):: >  > ]",
        "[para(2,7):]",
        "[text(2,7):another block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>block quote</p>
<blockquote>
<p>another block quote</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_block_quotes_with_tabs_2():
    """
    Test case:  Block quotes preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ > block quote
 >\t> another block quote
 >\t> same block quote"""
    expected_tokens = [
        "[block-quote(1,2): : > \n > ]",
        "[para(1,4):]",
        "[text(1,4):block quote:]",
        "[end-para:::True]",
        "[block-quote(2,5):: >  > \n >  > ]",
        "[para(2,7):\n]",
        "[text(2,7):another block quote\nsame block quote::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>block quote</p>
<blockquote>
<p>another block quote
same block quote</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_block_quotes_with_form_feeds():
    """
    Test case:  Block quotes preceeded by spaces and form feeds (ascii whitespace).
    """

    # Arrange
    source_markdown = """ > block quote
 >\u000C> another block quote"""
    expected_tokens = [
        "[block-quote(1,2): : > \n >]",
        "[para(1,4):\n]",
        "[text(1,4):block quote\n\u000C\a>\a&gt;\a another block quote::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>block quote
\u000C&gt; another block quote</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_ordered_lists_with_spaces():
    """
    Test case:  Ordered lists preceeded by spaces.
    """

    # Arrange
    source_markdown = """   1. list item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):list item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>list item</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_ordered_lists_with_tabs():
    """
    Test case:  Ordered lists preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. list item
 \t1. inner list item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):list item:]",
        "[end-para:::True]",
        "[olist(2,5):.:1:7:    ]",
        "[para(2,8):]",
        "[text(2,8):inner list item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>list item
<ol>
<li>inner list item</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_ordered_lists_with_form_feeds():
    """
    Test case:  Ordered lists preceeded by spaces and form feeds (ascii whitespace).
    """

    # Arrange
    source_markdown = """1. list item
 \u000C1. inner list item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n ]",
        "[text(1,4):list item\n\u000C1. inner list item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>list item
\u000C1. inner list item</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_unordered_lists_with_spaces():
    """
    Test case:  Unordered lists preceeded by spaces.
    """

    # Arrange
    source_markdown = """   + list item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   ]",
        "[para(1,6):]",
        "[text(1,6):list item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>list item</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_unordered_lists_with_tabs():
    """
    Test case:  Unordered lists preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """+ list item
 \t+ inner list item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[para(1,3):]",
        "[text(1,3):list item:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:    ]",
        "[para(2,7):]",
        "[text(2,7):inner list item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>list item
<ul>
<li>inner list item</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_unordered_lists_with_form_feeds():
    """
    Test case:  Unordered lists preceeded by spaces and form feeds (ascii whitespace).
    """

    # Arrange
    source_markdown = """+ list item
 \u000C + inner list item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[para(1,3):\n ]",
        "[text(1,3):list item\n\u000C + inner list item::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>list item
\u000C + inner list item</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces():
    """
    Test case:  Thematic breaks preceeded by spaces.
    """

    # Arrange
    source_markdown = """   * * *"""
    expected_tokens = ["[tbreak(1,4):*:   :* * *]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_thematic_breaks_with_tabs_before():
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t * * *"""
    expected_tokens = [
        "[icode-block(1,5): \t:]",
        "[text(1,5):* * *: ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code> * * *
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_thematic_breaks_with_tabs_before_within():
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """
    # NOTE: thematic break takes precedece: https://github.github.com/gfm/#example-30

    # Arrange
    source_markdown = """- abc
    * * *"""
    expected_tokens = [
        "[icode-block(1,5): \t:]",
        "[text(1,5):* * *: ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<hr />
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_form_feeds_before():
    """
    Test case:  Thematic breaks preceeded by spaces and form feeds.
    """

    # Arrange
    source_markdown = """ \u000C * * *"""
    expected_tokens = [
        "[para(1,2): \u000C ]",
        "[text(1,2):*:]",
        "[text(1,3): :]",
        "[text(1,4):*:]",
        "[text(1,5): :]",
        "[text(1,6):*:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>* * *</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_inside():
    """
    Test case:  Thematic breaks containing spaces and tabs.
    """

    # Arrange
    source_markdown = """* *\t*"""
    expected_tokens = ["[tbreak(1,1):*::* *\t*]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_form_feeds_inside():
    """
    Test case:  Thematic breaks containing spaces and form feeds.
    """

    # Arrange
    source_markdown = """* *\u000C*"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):*:]",
        "[text(1,4):\u000C:]",
        "[text(1,5):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>*\u000C*</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_after():
    """
    Test case:  Thematic breaks followed by spaces.
    """

    # Arrange
    source_markdown = """* * * """
    expected_tokens = ["[tbreak(1,1):*::* * * ]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_after():
    """
    Test case:  Thematic breaks followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """* * *\t"""
    expected_tokens = ["[tbreak(1,1):*::* * *\t]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_form_feeds_after():
    """
    Test case:  Thematic breaks followed by spaces and form feeds.
    """

    # Arrange
    source_markdown = """* * *\u000C"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[ulist(1,3):*::4:  ]",
        "[para(1,5)::\u000C]",
        "[text(1,5):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>*</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_spaces_before():
    """
    Test case:  Atx Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """  # abc"""
    expected_tokens = ["[atx(1,3):1:0:  ]", "[text(1,5):abc: ]", "[end-atx::]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_atx_headings_with_tabs_before():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t # abc"""
    expected_tokens = [
        "[icode-block(1,5): \t:]",
        "[text(1,5):# abc: ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code> # abc
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_within():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \t# abc"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[atx(2,5):1:0:\t]",
        "[text(2,7):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<h1>abc</h1>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_form_feeds_before():
    """
    Test case:  Atx Headings preceeded by spaces and form feeds.
    """

    # Arrange
    source_markdown = """ \u000C # abc"""
    expected_tokens = [
        "[para(1,2): \u000C ]",
        "[text(1,2):# abc:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p># abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_inside():
    """
    Test case:  Atx Headings containing spaces and tabs.
    """

    # Arrange
    source_markdown = """#\tabc"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc:\t]", "[end-atx::]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_inside_2():
    """
    Test case:  Atx Headings containing spaces and tabs.
    """

    # Arrange
    source_markdown = """# abc\tdef"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc\tdef: ]", "[end-atx::]"]
    expected_gfm = """<h1>abc\tdef</h1>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_form_feeds_inside():
    """
    Test case:  Atx Headings containing form feeds.
    """

    # Arrange
    source_markdown = """#\u000Cabc"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):#\u000Cabc:]", "[end-para:::True]"]
    expected_gfm = """<p>#\u000Cabc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_spaces_after():
    """
    Test case:  Atx Headings followed by spaces.
    """

    # Arrange
    source_markdown = """# abc  """
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc: ]", "[end-atx:  :]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_after():
    """
    Test case:  Atx Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """# abc \t"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc: ]", "[end-atx: \t:]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_form_feeds_after():
    """
    Test case:  Atx Headings containing form feeds.
    """

    # Arrange
    source_markdown = """# abc\u000C"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc\u000C: ]", "[end-atx::]"]
    expected_gfm = """<h1>abc\u000C</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_inside_closed():
    """
    Test case:  Atx Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """# abc\tdef #"""
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc\tdef: ]", "[end-atx:: ]"]
    expected_gfm = """<h1>abc\tdef</h1>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_spaces_after_closed():
    """
    Test case:  Atx Headings followed by spaces.
    """

    # Arrange
    source_markdown = """# abc #"""
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc: ]", "[end-atx:: ]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_after_closed():
    """
    Test case:  Atx Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """# abc\t#"""
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc: ]", "[end-atx::\t]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_form_feeds_after_closed():
    """
    Test case:  Atx Headings followed by form feeds.
    """

    # Arrange
    source_markdown = """# abc\u000C#"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc\u000C#: ]", "[end-atx::]"]
    expected_gfm = """<h1>abc\u000C#</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_closed_with_spaces_after():
    """
    Test case:  Atx Headings followed by spaces.
    """

    # Arrange
    source_markdown = """# abc #  """
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc: ]", "[end-atx:  : ]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_closed_with_tabs_after():
    """
    Test case:  Atx Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """# abc #\t"""
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc: ]", "[end-atx:\t: ]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_atx_headings_closed_with_form_feeds_after():
    """
    Test case:  Atx Headings followed by form feeds.
    """

    # Arrange
    source_markdown = """# abc #\u000C"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc #\u000C: ]", "[end-atx::]"]
    expected_gfm = """<h1>abc #\u000C</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_spaces_before():
    """
    Test case:  SetExt Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """abc
  ---"""
    expected_tokens = [
        "[setext(2,3):-:3::(1,1)]",
        "[text(1,1):abc:]",
        "[end-setext:  :]",
    ]
    expected_gfm = """<h2>abc</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_setext_headings_with_tabs_before():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # https://github.github.com/gfm/#example-77 - is not indent block because part of para, not setext or sep due to 4 spaces
    # Arrange
    source_markdown = """abc
\t---"""
    expected_tokens = [
        "[para(1,1):\n\t]",
        "[text(1,1):abc\n---::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
---</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \t---"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,5):-:3::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext:\t:]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        allow_alternate_markdown=False,
    )


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_form_feeds_before():
    """
    Test case:  SetExt Headings preceeded by form feeds.
    """

    # Arrange
    source_markdown = """abc
\u000C---"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc\n\u000C---::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
\u000C---</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_spaces_after():
    """
    Test case:  SetExt Headings followed by spaces.
    """

    # Arrange
    source_markdown = """abc
---  """
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):abc:]",
        "[end-setext::  ]",
    ]
    expected_gfm = """<h2>abc</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_after():
    """
    Test case:  SetExt Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """abc
---\t"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):abc:]",
        "[end-setext::\t]",
    ]
    expected_gfm = """<h2>abc</h2>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_after_within():
    """
    Test case:  SetExt Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  ---\t"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:3::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::\t]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        allow_alternate_markdown=False,
    )


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_form_feeds_after():
    """
    Test case:  SetExt Headings followed by form feeds.
    """

    # Arrange
    source_markdown = """abc
--- \u000C"""
    expected_tokens = [
        "[para(1,1):\n: \u000C]",
        "[text(1,1):abc\n---::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
---</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """    indented block"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):indented block:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>indented block
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_indented_code_with_tabs_before():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """\tindented block"""
    expected_tokens = [
        "[icode-block(1,5):\t:]",
        "[text(1,5):indented block:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>indented block
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_indented_code_with_form_feeds_before():
    """
    Test case:  Indented Code blocks preceeded by form feeds.
    """

    # Arrange
    source_markdown = """\u000C\u000C\u000C\u000Cindented block"""
    expected_tokens = [
        "[para(1,1):\u000C\u000C\u000C\u000C]",
        "[text(1,1):indented block:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>indented block</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """  ```python
abc"""
    expected_tokens = [
        "[fcode-block(1,3):`:3:python::::  :]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_fenced_code_open_with_tabs_before():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t```python
abc"""
    expected_tokens = [
        "[icode-block(1,5): \t:]",
        "[text(1,5):```python:]",
        "[end-icode-block:::False]",
        "[para(2,1):]",
        "[text(2,1):abc:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>```python
</code></pre>
<p>abc</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_form_feeds_before():
    """
    Test case:  Fenced Code blocks preceeded by form feeds.
    """

    # Arrange
    source_markdown = """ \u000C```python
abc"""
    expected_tokens = [
        "[para(1,2): \u000C\n]",
        "[text(1,2):```python\nabc::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>```python
abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_info():
    """
    Test case:  Fenced Code blocks info string followed by spaces.
    """

    # Arrange
    source_markdown = """```  python
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::  ]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_info():
    """
    Test case:  Fenced Code block info string followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """```\tpython
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::\t]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_form_feeds_before_info():
    """
    Test case:  Fenced Code blocks info string followed by form feeds.
    """

    # Arrange
    source_markdown = """```\u000Cpython
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::\u000C]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_after_info():
    """
    Test case:  Fenced Code blocks info string followed by spaces.
    """

    # Arrange
    source_markdown = """```python  
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_after_info():
    """
    Test case:  Fenced Code block info string followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """```python\t
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::\t:::]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_form_feeds_after_language():
    """
    Test case:  Fenced Code blocks info string followed by form feeds.
    """

    # Arrange
    source_markdown = """```python\u000C
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::\u000C:::]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_form_feeds_after_info():
    """
    Test case:  Fenced Code blocks info string followed by form feeds.
    """

    # Arrange
    source_markdown = """```python a\u000C\a
abc""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:: a\u000C :::]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_within():
    """
    Test case:  Fenced Code blocks...
    """

    # Arrange
    source_markdown = """```python
abc\tdef
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::]",
        "[text(2,1):abc\tdef:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc\tdef
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_spaces_before():
    """
    Test case:  Fenced Code blocks closed preceeded by spaces.
    """

    # Arrange
    source_markdown = """```python
abc
  ```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::]",
        "[text(2,1):abc:]",
        "[end-fcode-block:  ::3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_before():
    """
    Test case:  Fenced Code block closed preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """```python
abc
\t```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::]",
        "[text(2,1):abc\n\t```:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
\t```
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_before_x():
    """
    Test case:  Fenced Code block closed preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- ```python
  abc
  \t```"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[fcode-block(1,3):`:3:python:::::]",
        "[text(2,3):abc\n\t```:]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code class="language-python">abc
\t```
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        allow_alternate_markdown=False,
    )


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_form_feeds_before():
    """
    Test case:  Fenced Code blocks closed preceeded by form feeds.
    """

    # Arrange
    source_markdown = """```python
abc
\u000C```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::]",
        "[text(2,1):abc\n\u000C```:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
\u000C```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_spaces_after():
    """
    Test case:  Fenced Code blocks closed followed by spaces.
    """

    # Arrange
    source_markdown = """```python  
abc
``` """
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc:]",
        "[end-fcode-block:: :3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_after():
    """
    Test case:  Fenced Code block closed followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """```python  
abc
```\t"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc\n```\t:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
```\t
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_after_and_before():
    """
    Test case:  Fenced Code block close followed by tabs and preceeded be spaces.
    """

    # Arrange
    source_markdown = """```python  
abc
  ```\t"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc\n  ```\t:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
  ```\t
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_after_and_before_2():
    """
    Test case:  Fenced Code block close followed by tabs and preceeded be spaces.
    """

    # Arrange
    source_markdown = """- ```python  
  abc
  ```\t"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[fcode-block(1,3):`:3:python::  :::]",
        "[text(2,3):abc\n```\t:]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code class="language-python">abc
```\t
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        allow_alternate_markdown=False,
    )


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_form_feeds_after():
    """
    Test case:  Fenced Code blocks closed followed by form feeds.
    """

    # Arrange
    source_markdown = """```python  
abc
```\u000C"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc\n```\u000C:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
```\u000C
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_with_tabs_inside():
    """
    Test case:  Fenced Code block closed followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """```python  
abc\tdef
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc\tdef:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc\tdef
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before():
    """
    Test case:  Html blocks closed followed by spaces.
    """

    # Arrange
    source_markdown = """  <!-- comment"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,3):<!-- comment:  ]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """  <!-- comment"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_html_with_tabs_before():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t<!-- comment"""
    expected_tokens = [
        "[icode-block(1,5): \t:]",
        "[text(1,5):\a<\a&lt;\a!-- comment:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&lt;!-- comment
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_inside():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \t<!-- comment"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\t<!-- comment
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_html_with_form_feeds_before():
    """
    Test case:  HTML blocks followed by form feeds.
    """

    # Arrange
    source_markdown = """ \u000C<!-- comment"""
    expected_tokens = [
        "[para(1,2): \u000C]",
        "[text(1,2):\a<\a&lt;\a!-- comment:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;!-- comment</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_start_6_with_spaces_after():
    """
    Test case:  Html blocks type 6 followed by spaces.
    """

    # Arrange
    source_markdown = """<dialog  """
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog  :]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog  """

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_start_6_with_tabs_after():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """<dialog\t"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog\t:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog\t"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_html_start_6_with_form_feeds_after():
    """
    Test case:  HTML blocks followed by form feeds.
    """

    # Arrange
    source_markdown = """<dialog\u000c"""
    expected_tokens = [
        "[para(1,1)::\u000c]",
        "[text(1,1):\a<\a&lt;\adialog:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;dialog</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_start_7_with_spaces_after():
    """
    Test case:  Html blocks type 7 followed by spaces.
    """

    # Arrange
    source_markdown = """<dialog>  """
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog>  :]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog>  """

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_start_7_with_tabs_after():
    """
    Test case:  HTML block type 7 followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """<dialog>\t"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog>\t:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog>\t"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_html_start_7_with_tabs_within():
    """
    Test case:  HTML block type 7 followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """<dialog>
<something>\t</something>

"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog>\n<something>\t</something>:]",
        "[end-html-block:::False]",
        "[BLANK(3,1):]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<dialog>
<something>\t</something>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_html_start_7_with_form_feeds_after():
    """
    Test case:  HTML blocks type 7 followed by form feeds.
    """

    # Arrange
    source_markdown = """<dialog>\u000c"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog>\u000c:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog>\u000c"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """   [fred]: /url
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,4):True:   :fred:: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_lrd_with_tabs_before():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """\t[fred]: /url
[fred]"""
    expected_tokens = [
        "[icode-block(1,5):\t:]",
        "[text(1,5):[fred]: /url:]",
        "[end-icode-block:::False]",
        "[para(2,1):]",
        "[text(2,1):[:]",
        "[text(2,2):fred:]",
        "[text(2,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>[fred]: /url
</code></pre>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_before():
    """
    Test case:  LRD preceeded by form feeds.
    """

    # Arrange
    source_markdown = """\u000c[fred]: /url
[fred]"""
    expected_tokens = [
        "[para(1,1):\u000c\n]",
        "[text(1,1):[:]",
        "[text(1,2):fred:]",
        "[text(1,6):]:]",
        "[text(1,7):: /url\n::\n]",
        "[text(2,1):[:]",
        "[text(2,2):fred:]",
        "[text(2,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[fred]: /url
[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_label():
    """
    Test case:  LRD link label preceeded by spaces.
    """

    # Arrange
    source_markdown = """[  fred]: /url
[ fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:  fred: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url::::: fred:False::::]",
        "[text(2,2): fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url"> fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_lrd_with_tabs_before_label():
    """
    Test case:  LRD link label preceeded by tabs.
    """

    # Arrange
    source_markdown = """[\t\tfred]: /url
[ fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:\t\tfred: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url::::: fred:False::::]",
        "[text(2,2): fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url"> fred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_before_label():
    """
    Test case:  LRD link label preceeded by form feeds.
    """

    # Arrange
    source_markdown = """[\u000cfred]: /url
[ fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:\u000cfred: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url::::: fred:False::::]",
        "[text(2,2): fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url"> fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_after_label():
    """
    Test case:  LRD link label followed by spaces.
    """

    # Arrange
    source_markdown = """[fred  ]: /url
[fred ]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:fred  : :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred :False::::]",
        "[text(2,2):fred :]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred </a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_lrd_with_tabs_after_label():
    """
    Test case:  LRD link label followwed by tabs.
    """

    # Arrange
    source_markdown = """[fred\t\t]: /url
[fred ]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:fred\t\t: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred :False::::]",
        "[text(2,2):fred :]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred </a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_after_label():
    """
    Test case:  LRD link label followed by form feeds.
    """

    # Arrange
    source_markdown = """[fred\u000c]: /url
[fred ]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:fred\u000c: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred :False::::]",
        "[text(2,2):fred :]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred </a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_in_label():
    """
    Test case:  LRD link label with spaces inside.
    """

    # Arrange
    source_markdown = """[fred  boy]: /url
[fred boy]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred boy:fred  boy: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred boy:False::::]",
        "[text(2,2):fred boy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred boy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_lrd_with_tabs_in_label():
    """
    Test case:  LRD link label followwed by tabs.
    """

    # Arrange
    source_markdown = """[fred\t\tboy]: /url
[fred boy]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred boy:fred\t\tboy: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred boy:False::::]",
        "[text(2,2):fred boy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred boy</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_in_label():
    """
    Test case:  LRD link label followed by form feeds.
    """

    # Arrange
    source_markdown = """[fred\u000c\u000cboy]: /url
[fred boy]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred boy:fred\u000c\u000cboy: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred boy:False::::]",
        "[text(2,2):fred boy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred boy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_destination():
    """
    Test case:  LRD destination preceeded by spaces.
    """

    # Arrange
    source_markdown = """[fred]:  /url
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred::  :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_lrd_with_tabs_before_destination():
    """
    Test case:  LRD destination preceeded by tabs.
    """

    # Arrange
    source_markdown = """[fred]:\t/url
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred::\t:/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_before_destination():
    """
    Test case:  LRD destination preceeded by form feeds.
    """

    # Arrange
    source_markdown = """[fred]:\u000c/url
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred::\u000c:/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_after_destination():
    """
    Test case:  LRD destination followed by spaces.
    """

    # Arrange
    source_markdown = """[fred]: /url  
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:: :/url::  :::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_lrd_with_tabs_after_destination():
    """
    Test case:  LRD destination followed by tabs.
    """

    # Arrange
    source_markdown = """[fred]: /url\t\t
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:: :/url::\t\t:::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_after_destination():
    """
    Test case:  LRD destination followed by form feeds.
    """

    # Arrange
    source_markdown = """[fred]: /url\u000c\u000c
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:: :/url::\u000c\u000c:::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_title():
    """
    Test case:  LRD title preceeded by spaces.
    """

    # Arrange
    source_markdown = """[fred]: /url "title"
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url:: :title:"title":]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_lrd_with_tabs_before_title():
    """
    Test case:  LRD title preceeded by tabs.
    """

    # Arrange
    source_markdown = """[fred]: /url\t"title"
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url::\t:title:"title":]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_before_title():
    """
    Test case:  LRD title preceeded by form feeds.
    """

    # Arrange
    source_markdown = """[fred]: /url\u000c"title"
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url::\u000c:title:"title":]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_after_title():
    """
    Test case:  LRD title followed by spaces.
    """

    # Arrange
    source_markdown = """[fred]: /url "title"   
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url:: :title:"title":   ]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_lrd_with_tabs_after_title():
    """
    Test case:  LRD title followed by tabs.
    """

    # Arrange
    source_markdown = """[fred]: /url "title"\t\t
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url:: :title:"title":\t\t]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_after_title():
    """
    Test case:  LRD title followed by form feeds.
    """

    # Arrange
    source_markdown = """[fred]: /url "title"\u000c\u000c
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url:: :title:"title":\u000c\u000c]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before():
    """
    Test case:  paragraph preceeded by spaces.
    """

    # Arrange
    source_markdown = """  a paragraph"""
    expected_tokens = [
        "[para(1,3):  ]",
        "[text(1,3):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_paragraph_with_tabs_before():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """\ta paragraph"""
    expected_tokens = [
        "[icode-block(1,5):\t:]",
        "[text(1,5):a paragraph:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>a paragraph
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_inside():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """a\tlong\tparagraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a\tlong\tparagraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a\tlong\tparagraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_inside_and_emphasis():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """a\t*long*\tparagraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a\t:]",
        "[emphasis(1,5):1:*]",
        "[text(1,6):long:]",
        "[end-emphasis(1,10)::]",
        "[text(1,11):\tparagraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a\t<em>long</em>\tparagraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_paragraph_with_form_feeds_before():
    """
    Test case:  paragraph preceeded by form feeds.
    """

    # Arrange
    source_markdown = """\u000ca paragraph"""
    expected_tokens = [
        "[para(1,1):\u000c]",
        "[text(1,1):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_and_form_feeds_before():
    """
    Test case:  paragraph preceeded by form feeds.
    """

    # Arrange
    source_markdown = """ \u000ca paragraph"""
    expected_tokens = [
        "[para(1,2): \u000c]",
        "[text(1,2):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_and_form_feeds_before_and_after():
    """
    Test case:  paragraph preceeded by form feeds.
    """

    # Arrange
    source_markdown = """ \u000c a paragraph"""
    expected_tokens = [
        "[para(1,2): \u000c ]",
        "[text(1,2):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_after():
    """
    Test case:  paragraph followed by spaces.
    """

    # Arrange
    source_markdown = """a paragraph  """
    expected_tokens = [
        "[para(1,1)::  ]",
        "[text(1,1):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_after():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """a paragraph\t"""
    expected_tokens = [
        "[para(1,1)::\t]",
        "[text(1,1):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_after_double():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """a paragraph\t
another paragraph\t\t"""
    expected_tokens = [
        "[para(1,1):\n:\t\t]",
        "[text(1,1):a paragraph\nanother paragraph::\t\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph\t
another paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_after_double_only_first():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """a paragraph\t
another paragraph"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a paragraph\nanother paragraph::\t\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph\t
another paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_after_double_only_second():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """a paragraph
another paragraph\t\t"""
    expected_tokens = [
        "[para(1,1):\n:\t\t]",
        "[text(1,1):a paragraph\nanother paragraph::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph
another paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_after_only_middle():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """a paragraph
another paragraph\t\t
yet another paragraph"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):a paragraph\nanother paragraph\nyet another paragraph::\n\t\t\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph
another paragraph\t\t
yet another paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_mixed_and_no_newline():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """before-tab\tafter-tab
before-tab\tafter-tab
before-tab\tafter-tab\tafter-another
a\tbb\tccc\tddd"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):before-tab\tafter-tab\nbefore-tab\tafter-tab\nbefore-tab\tafter-tab\tafter-another\na\tbb\tccc\tddd::\n\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>before-tab\tafter-tab
before-tab\tafter-tab
before-tab\tafter-tab\tafter-another
a\tbb\tccc\tddd</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_mixed_and_newline():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """before-tab\tafter-tab
before-tab\tafter-tab
before-tab\tafter-tab\tafter-another
a\tbb\tccc\tddd
"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):before-tab\tafter-tab\nbefore-tab\tafter-tab\nbefore-tab\tafter-tab\tafter-another\na\tbb\tccc\tddd::\n\n\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<p>before-tab\tafter-tab
before-tab\tafter-tab
before-tab\tafter-tab\tafter-another
a\tbb\tccc\tddd</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_paragraph_with_form_feeds_after():
    """
    Test case:  paragraph followed by form feeds.
    """

    # Arrange
    source_markdown = """a paragraph\u000c"""
    expected_tokens = [
        "[para(1,1)::\u000c]",
        "[text(1,1):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_spaces():
    """
    Test case:  code span with spaces at the front and end
    """

    # Arrange
    source_markdown = """a ` good ` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):good:`: : ]",
        "[text(1,11): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>good</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_0x():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a `\tgood\t` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):\tgood\t:`::]",
        "[text(1,14): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>\tgood\t</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_0a():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a `\tgood` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):\tgood:`::]",
        "[text(1,10): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>\tgood</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_0b():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a `good\t` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):good\t:`::]",
        "[text(1,10): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>good\t</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_0c():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """`\tgood\t`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):\tgood\t:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>\tgood\t</code></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_1():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a `&#09;good&#09;` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,19): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>&amp;#09;good&amp;#09;</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_2():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a &#09;`good`&#09; paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \a&#09;\a\t\a:]",
        "[icode-span(1,8):good:`::]",
        "[text(1,14):\a&#09;\a\t\a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a \t<code>good</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_3():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a &#09;`&#09;good&#09;`&#09; paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \a&#09;\a\t\a:]",
        "[icode-span(1,8):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,24):\a&#09;\a\t\a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a \t<code>&amp;#09;good&amp;#09;</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_code_span_with_tabs_4():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a \t`&#09;good&#09;`\t paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a\t:]",
        "[icode-span(1,5):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,21):\t paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a \t<code>&amp;#09;good&amp;#09;</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_code_span_with_tabs_4a():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a \t`&#09;good&#09;` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \t:]",
        "[icode-span(1,5):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,21): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a \t<code>&amp;#09;good&amp;#09;</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_code_span_with_tabs_4b():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a `&#09;good&#09;`\t paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,19):\t paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>&amp;#09;good&amp;#09;</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_code_span_with_tabs_4c():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """\t`&#09;good&#09;`\t"""
    expected_tokens = [
        "[icode-block(1,5):\t:]",
        "[text(1,5):`\a&\a&amp;\a#09;good\a&\a&amp;\a#09;`\t:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>`&amp;#09;good&amp;#09;`\t
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        allow_alternate_markdown=False,
    )


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_5():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a &#09;`\tgood\t`&#09; paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \a&#09;\a\t\a:]",
        "[icode-span(1,8):\tgood\t:`::]",
        "[text(1,22):\a&#09;\a\t\a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a 	<code>\tgood\t</code>	 paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_5a():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a &#09;`\tgood`&#09; paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \a&#09;\a\t\a:]",
        "[icode-span(1,8):\tgood:`::]",
        "[text(1,18):\a&#09;\a\t\a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a 	<code>\tgood</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_5b():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a &#09;`good\t`&#09; paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \a&#09;\a\t\a:]",
        "[icode-span(1,8):good\t:`::]",
        "[text(1,18):\a&#09;\a\t\a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a 	<code>good\t</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_5c():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """`\tgood\t`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):\tgood\t:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>\tgood\t</code></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_code_span_with_tabs_6():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a\tvery `&#09;good&#09;`xx\t paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a\t:]",
        "[icode-span(1,5):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,21):\t paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>a\tvery <code>&amp;#09;good&amp;#09;</code>xx\t paragraph</p>"""
    )

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_code_spans_with_form_feeds():
    """
    Test case: code span with form feeds at the front and end
    """

    # Arrange
    source_markdown = """a `\u000cgood\u000c` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):\u000cgood\u000c:`::]",
        "[text(1,11): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>\u000cgood\u000c</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_hard_break_with_spaces():
    """
    Test case:  hard_break with spaces
    """

    # Arrange
    source_markdown = """foo   
bar"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo:]",
        "[hard-break(1,4):   :\n]",
        "[text(2,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_hard_break_with_tabs():
    """
    Test case:  hard_break with tabs
    """

    # Arrange
    source_markdown = """foo\t\t
bar"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo\nbar::\t\t\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo\t\t
bar</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )
    # assert False


@pytest.mark.gfm
def test_whitespaces_hard_break_with_form_feeds():
    """
    Test case: hard_break with form feeds
    """

    # Arrange
    source_markdown = """foo\u000c\u000c
bar"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo\u000c\u000c\nbar::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo\u000c\u000c
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_autolink_uri_with_spaces():
    """
    Test case:  autolink_uri with spaces
    """

    # Arrange
    source_markdown = """<http://foo.bar.baz/test?q=hello man&id=22&boolean>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\ahttp://foo.bar.baz/test?q=hello man\a&\a&amp;\aid=22\a&\a&amp;\aboolean\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>&lt;http://foo.bar.baz/test?q=hello man&amp;id=22&amp;boolean&gt;</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_autolink_uri_with_tabs_inside():
    """
    Test case:  autolink_uri with tabs
    """

    # Arrange
    source_markdown = """<http://foo.bar.baz/test?q=hello\tman&id=22&boolean>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\ahttp://foo.bar.baz/test?q=hello\tman\a&\a&amp;\aid=22\a&\a&amp;\aboolean\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>&lt;http://foo.bar.baz/test?q=hello\tman&amp;id=22&amp;boolean&gt;</p>"""
    )

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_autolink_uri_with_tabs_outside():
    """
    Test case:  autolink_uri with tabs
    """

    # Arrange
    source_markdown = """this\tis <http://foo.bar.baz> an\tautolink"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this\tis :]",
        "[uri-autolink(1,12):http://foo.bar.baz]",
        "[text(1,32): an\tautolink:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this\tis <a href="http://foo.bar.baz">http://foo.bar.baz</a> an\tautolink</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_autolink_uri_with_form_feeds():
    """
    Test case: autolink_uri with form feeds
    """

    # Arrange
    source_markdown = """<http://foo.bar.baz/test?q=hello\u000cman&id=22&boolean>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\ahttp://foo.bar.baz/test?q=hello\u000cman\a&\a&amp;\aid=22\a&\a&amp;\aboolean\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;http://foo.bar.baz/test?q=hello\u000cman&amp;id=22&amp;boolean&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_before_label():
    """
    Test case:  inline link label with spaces before
    """

    # Arrange
    source_markdown = """[ fred](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url::::: fred:False::::]",
        "[text(1,2): fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url"> fred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_outside():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """this\tis [fred](/url) a\tlink"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this\tis :]",
        "[link(1,12):inline:/url:::::fred:False::::]",
        "[text(1,13):fred:]",
        "[end-link::]",
        "[text(1,24): a\tlink:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this\tis <a href="/url">fred</a> a\tlink</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink
this\tis [fred](/url) a\tlink
large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink\nthis\tis ::\n]",
        "[link(2,12):inline:/url:::::fred:False::::]",
        "[text(2,13):fred:]",
        "[end-link::]",
        "[text(2,24): a\tlink\nlarge\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink
this\tis <a href="/url">fred</a> a\tlink
large\text</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_no_spaces():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink
this\tis[fred](/url)a\tlink
large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink\nthis\tis::\n]",
        "[link(2,11):inline:/url:::::fred:False::::]",
        "[text(2,12):fred:]",
        "[end-link::]",
        "[text(2,23):a\tlink\nlarge\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink
this\tis<a href="/url">fred</a>a\tlink
large\text</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis [fred](/url) a\tlink a\tlink
large\text large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis ::\n]",
        "[link(2,20):inline:/url:::::fred:False::::]",
        "[text(2,21):fred:]",
        "[end-link::]",
        "[text(2,32): a\tlink a\tlink\nlarge\text large\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis <a href="/url">fred</a> a\tlink a\tlink
large\text large\text</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_first_two():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis [fred](/url) a\tlink a\tlink"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis ::\n]",
        "[link(2,20):inline:/url:::::fred:False::::]",
        "[text(2,21):fred:]",
        "[end-link::]",
        "[text(2,32): a\tlink a\tlink:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis <a href="/url">fred</a> a\tlink a\tlink</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_and_links():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis [fred](/url) a\tlink a\tlink [barney](/url) another\tlink another\tlink
large\text large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis ::\n]",
        "[link(2,20):inline:/url:::::fred:False::::]",
        "[text(2,21):fred:]",
        "[end-link::]",
        "[text(2,32): a\tlink a\tlink :]",
        "[link(2,50):inline:/url:::::barney:False::::]",
        "[text(2,51):barney:]",
        "[end-link::]",
        "[text(2,64): another\tlink another\tlink\nlarge\text large\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis <a href="/url">fred</a> a\tlink a\tlink <a href="/url">barney</a> another\tlink another\tlink
large\text large\text</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_and_links_no_space():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis[fred](/url)a\tlink a\tlink[barney](/url)another\tlink another\tlink
large\text large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis::\n]",
        "[link(2,19):inline:/url:::::fred:False::::]",
        "[text(2,20):fred:]",
        "[end-link::]",
        "[text(2,31):a\tlink a\tlink:]",
        "[link(2,45):inline:/url:::::barney:False::::]",
        "[text(2,46):barney:]",
        "[end-link::]",
        "[text(2,59):another\tlink another\tlink\nlarge\text large\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis<a href="/url">fred</a>a\tlink a\tlink<a href="/url">barney</a>another\tlink another\tlink
large\text large\text</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_and_links_no_word_just_space():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis[fred](/url) [barney](/url)another\tlink another\tlink
large\text large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis::\n]",
        "[link(2,19):inline:/url:::::fred:False::::]",
        "[text(2,20):fred:]",
        "[end-link::]",
        "[text(2,31): :]",
        "[link(2,32):inline:/url:::::barney:False::::]",
        "[text(2,33):barney:]",
        "[end-link::]",
        "[text(2,46):another\tlink another\tlink\nlarge\text large\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis<a href="/url">fred</a> <a href="/url">barney</a>another\tlink another\tlink
large\text large\text</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_and_links_no_word_just_tab():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink an\tlink
this\tis this\tis[fred](/url)\t[barney](/url)another\tlink another\tlink
large\text large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink an\tlink\nthis\tis this\tis::\n]",
        "[link(2,19):inline:/url:::::fred:False::::]",
        "[text(2,20):fred:]",
        "[end-link::]",
        "[text(2,31):\t:]",
        "[link(2,33):inline:/url:::::barney:False::::]",
        "[text(2,34):barney:]",
        "[end-link::]",
        "[text(2,47):another\tlink another\tlink\nlarge\text large\text::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink an\tlink
this\tis this\tis<a href="/url">fred</a>\t<a href="/url">barney</a>another\tlink another\tlink
large\text large\text</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_duplicate_outside_and_links_more_links():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink [wilma](/url) an\tlink
this\tis this\tis[fred](/url)a\tlink a\tlink[barney](/url)another\tlink another\tlink
large\text[betty](/url)large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink :]",
        "[link(1,10):inline:/url:::::wilma:False::::]",
        "[text(1,11):wilma:]",
        "[end-link::]",
        "[text(1,23): an\tlink\nthis\tis this\tis::\n]",
        "[link(2,19):inline:/url:::::fred:False::::]",
        "[text(2,20):fred:]",
        "[end-link::]",
        "[text(2,31):a\tlink a\tlink:]",
        "[link(2,45):inline:/url:::::barney:False::::]",
        "[text(2,46):barney:]",
        "[end-link::]",
        "[text(2,59):another\tlink another\tlink\nlarge\text::\n]",
        "[link(3,12):inline:/url:::::betty:False::::]",
        "[text(3,13):betty:]",
        "[end-link::]",
        "[text(3,25):large\text:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink <a href="/url">wilma</a> an\tlink
this\tis this\tis<a href="/url">fred</a>a\tlink a\tlink<a href="/url">barney</a>another\tlink another\tlink
large\text<a href="/url">betty</a>large\text</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_more_links_and_middle_surrounding_spaces():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink [wilma](/url) an\tlink
this\tis this\tis[fred](/url) a\tlink a\tlink [barney](/url)another\tlink another\tlink
large\text[betty](/url)large\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink :]",
        "[link(1,10):inline:/url:::::wilma:False::::]",
        "[text(1,11):wilma:]",
        "[end-link::]",
        "[text(1,23): an\tlink\nthis\tis this\tis::\n]",
        "[link(2,19):inline:/url:::::fred:False::::]",
        "[text(2,20):fred:]",
        "[end-link::]",
        "[text(2,31): a\tlink a\tlink :]",
        "[link(2,50):inline:/url:::::barney:False::::]",
        "[text(2,51):barney:]",
        "[end-link::]",
        "[text(2,64):another\tlink another\tlink\nlarge\text::\n]",
        "[link(3,12):inline:/url:::::betty:False::::]",
        "[text(3,13):betty:]",
        "[end-link::]",
        "[text(3,25):large\text:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink <a href="/url">wilma</a> an\tlink
this\tis this\tis<a href="/url">fred</a> a\tlink a\tlink <a href="/url">barney</a>another\tlink another\tlink
large\text<a href="/url">betty</a>large\text</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_more_links_and_middle_surrounding_tabs():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink\t[wilma](/url)\tan\tlink
this\tis this\tis\t[fred](/url)\ta\tlink a\tlink\t[barney](/url)\tanother\tlink another\tlink
large\text\t[betty](/url)\tlarge\text"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):an\tlink\t:]",
        "[link(1,13):inline:/url:::::wilma:False::::]",
        "[text(1,14):wilma:]",
        "[end-link::]",
        "[text(1,26):\tan\tlink\nthis\tis this\tis\t::\n]",
        "[link(2,21):inline:/url:::::fred:False::::]",
        "[text(2,22):fred:]",
        "[end-link::]",
        "[text(2,33):\ta\tlink a\tlink\t:]",
        "[link(2,57):inline:/url:::::barney:False::::]",
        "[text(2,58):barney:]",
        "[end-link::]",
        "[text(2,71):\tanother\tlink another\tlink\nlarge\text\t::\n]",
        "[link(3,13):inline:/url:::::betty:False::::]",
        "[text(3,14):betty:]",
        "[end-link::]",
        "[text(3,26):\tlarge\text:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink\t<a href="/url">wilma</a>\tan\tlink
this\tis this\tis\t<a href="/url">fred</a>\ta\tlink a\tlink\t<a href="/url">barney</a>\tanother\tlink another\tlink
large\text\t<a href="/url">betty</a>\tlarge\text</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_more_links_and_ending_with_spaces():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink\t[wilma](/url)\tan\tlink
this\tis this\tis\t[fred](/url)\ta\tlink a\tlink\t[barney](/url)\tanother\tlink another\tlink
large\text\t[betty](/url)  """
    expected_tokens = [
        "[para(1,1):\n\n:  ]",
        "[text(1,1):an\tlink\t:]",
        "[link(1,13):inline:/url:::::wilma:False::::]",
        "[text(1,14):wilma:]",
        "[end-link::]",
        "[text(1,26):\tan\tlink\nthis\tis this\tis\t::\n]",
        "[link(2,21):inline:/url:::::fred:False::::]",
        "[text(2,22):fred:]",
        "[end-link::]",
        "[text(2,33):\ta\tlink a\tlink\t:]",
        "[link(2,57):inline:/url:::::barney:False::::]",
        "[text(2,58):barney:]",
        "[end-link::]",
        "[text(2,71):\tanother\tlink another\tlink\nlarge\text\t::\n]",
        "[link(3,13):inline:/url:::::betty:False::::]",
        "[text(3,14):betty:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink\t<a href="/url">wilma</a>\tan\tlink
this\tis this\tis\t<a href="/url">fred</a>\ta\tlink a\tlink\t<a href="/url">barney</a>\tanother\tlink another\tlink
large\text\t<a href="/url">betty</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_large_outside_with_more_links_and_ending_with_tabs():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """an\tlink\t[wilma](/url)\tan\tlink
this\tis this\tis\t[fred](/url)\ta\tlink a\tlink\t[barney](/url)\tanother\tlink another\tlink
large\text\t[betty](/url)\t\t"""
    expected_tokens = [
        "[para(1,1):\n\n:\t\t]",
        "[text(1,1):an\tlink\t:]",
        "[link(1,13):inline:/url:::::wilma:False::::]",
        "[text(1,14):wilma:]",
        "[end-link::]",
        "[text(1,26):\tan\tlink\nthis\tis this\tis\t::\n]",
        "[link(2,21):inline:/url:::::fred:False::::]",
        "[text(2,22):fred:]",
        "[end-link::]",
        "[text(2,33):\ta\tlink a\tlink\t:]",
        "[link(2,57):inline:/url:::::barney:False::::]",
        "[text(2,58):barney:]",
        "[end-link::]",
        "[text(2,71):\tanother\tlink another\tlink\nlarge\text\t::\n]",
        "[link(3,13):inline:/url:::::betty:False::::]",
        "[text(3,14):betty:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an\tlink\t<a href="/url">wilma</a>\tan\tlink
this\tis this\tis\t<a href="/url">fred</a>\ta\tlink a\tlink\t<a href="/url">barney</a>\tanother\tlink another\tlink
large\text\t<a href="/url">betty</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_before_label():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """[\tfred](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::\tfred:False::::]",
        "[text(1,2):\tfred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">\tfred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_before_label():
    """
    Test case:  inline link label with form feeds before
    """

    # Arrange
    source_markdown = """[\u000cfred](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::\u000cfred:False::::]",
        "[text(1,2):\u000cfred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">\u000cfred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_spaces_before_label():
    """
    Test case:  shortcut link label with spaces before
    """

    # Arrange
    source_markdown = """[  fred]

[ fred]: /url
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::  fred:False::::]",
        "[text(1,2):  fred:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred: fred: :/url:::::]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url">  fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_tabs_before_label():
    """
    Test case:  shortcut link label with tabs before
    """

    # Arrange
    source_markdown = """[\t\tfred]

[ fred]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::\t\tfred:False::::]",
        "[text(1,2):\t\tfred:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred: fred: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">\t\tfred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_form_feeds_before_label():
    """
    Test case:  shortcut link label with form feeds before
    """

    # Arrange
    source_markdown = """[\u000c\u000cfred]

[ fred]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::\u000c\u000cfred:False::::]",
        "[text(1,2):\u000c\u000cfred:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred: fred: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">\u000c\u000cfred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_in_label():
    """
    Test case:  inline link label with spaces in
    """

    # Arrange
    source_markdown = """[fred  boy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred  boy:False::::]",
        "[text(1,2):fred  boy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred  boy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_in_label():
    """
    Test case:  inline link label with tabs in
    """

    # Arrange
    source_markdown = """[fred\t\tboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t\tboy:False::::]",
        "[text(1,2):fred\t\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\t\tboy</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_in_label():
    """
    Test case:  inline link label with form feeds in
    """

    # Arrange
    source_markdown = """[fred\u000c\u000cboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\u000c\u000cboy:False::::]",
        "[text(1,2):fred\u000c\u000cboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\u000c\u000cboy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_spaces_in_label():
    """
    Test case:  shortcut link label with spaces in
    """

    # Arrange
    source_markdown = """[fred  boy]

[fred boy]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred  boy:False::::]",
        "[text(1,2):fred  boy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred boy:: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred  boy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_tabs_in_label():
    """
    Test case:  shortcut link label with tabs in
    """

    # Arrange
    source_markdown = """[fred\t\tboy]

[fred boy]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred\t\tboy:False::::]",
        "[text(1,2):fred\t\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred boy:: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred\t\tboy</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_form_feeds_in_label():
    """
    Test case:  shortcut link label with form feeds in
    """

    # Arrange
    source_markdown = """[fred\u000c\u000cboy]

[fred boy]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred\u000c\u000cboy:False::::]",
        "[text(1,2):fred\u000c\u000cboy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred boy:: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred\u000c\u000cboy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_after_label():
    """
    Test case:  inline link label with after before
    """

    # Arrange
    source_markdown = """[fred ](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred :False::::]",
        "[text(1,2):fred :]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred </a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_after_label():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t\t](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t\t:False::::]",
        "[text(1,2):fred\t\t:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\t\t</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_after_label():
    """
    Test case:  inline link label with form feeds after
    """

    # Arrange
    source_markdown = """[fred\u000c\u000c](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\u000c\u000c:False::::]",
        "[text(1,2):fred\u000c\u000c:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\u000c\u000c</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_spaces_after_label():
    """
    Test case:  shortcut link label with spaces after
    """

    # Arrange
    source_markdown = """[fred  ]

[fred ]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred  :False::::]",
        "[text(1,2):fred  :]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred:fred : :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred  </a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_tabs_after_label():
    """
    Test case:  shortcut link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t\t]

[fred ]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred\t\t:False::::]",
        "[text(1,2):fred\t\t:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred:fred : :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred\t\t</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_shortcut_link_with_form_feeds_after_label():
    """
    Test case:  shortcut link label with form feeds after
    """

    # Arrange
    source_markdown = """[fred\u000c\u000c]

[fred ]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::fred\u000c\u000c:False::::]",
        "[text(1,2):fred\u000c\u000c:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred:fred : :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred\u000c\u000c</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_and_references():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t&amp;\tboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t&amp;\tboy:False::::]",
        "[text(1,2):fred\t\a&amp;\a\a&\a&amp;\a\a\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\t&amp;\tboy</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_inline_link_with_tabs_and_code_span():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t`bob`\tboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t&amp;\tboy:False::::]",
        "[text(1,2):fred\t\a&amp;\a\a&\a&amp;\a\a\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\t<code>bob</code>\tboy</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_and_emphasis():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t*bob\tthe*\tboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t*bob\tthe*\tboy:False::::]",
        "[text(1,2):fred\t:]",
        "[emphasis(1,9):1:*]",
        "[text(1,10):bob\tthe:]",
        "[end-emphasis(1,20)::]",
        "[text(1,21):\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred\t<em>bob\tthe</em>\tboy</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_and_image():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """[fred\t![bob\tboy](/url)\tboy](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred\t![bob\tboy](/url)\tboy:False::::]",
        "[text(1,2):fred\t:]",
        "[image(1,9):inline:/url::bob\tboy::::bob\tboy:False::::]",
        "[text(1,27):\tboy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="/url">fred\t<img src="/url" alt="bob\tboy" />\tboy</a></p>"""
    )

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_inside_of_tabs():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """this\tshould\t[fred\tboy](/url)\tbe\tbad\tmarkdown"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this\tshould\t:]",
        "[link(1,17):inline:/url:::::fred\tboy:False::::]",
        "[text(1,18):fred\tboy:]",
        "[end-link::]",
        "[text(1,35):\tbe\tbad\tmarkdown:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>this\tshould\t<a href="/url">fred\tboy</a>\tbe\tbad\tmarkdown</p>"""
    )

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_and_newlines():
    """
    Test case:  inline link label with tabs after
    """

    # Arrange
    source_markdown = """should\t[fred\t
\tboy](/url)\tpass"""
    expected_tokens = [
        "[para(1,1):\n\t]",
        "[text(1,1):should\t:]",
        "[link(1,9):inline:/url:::::fred\t\nboy:False::::]",
        "[text(1,10):fred\nboy::\t\n]",
        "[end-link::]",
        "[text(2,12):\tpass:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>should\t<a href="/url">fred\t
boy</a>\tpass</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_before_destination():
    """
    Test case:  inline link label with spaces before the destination
    """

    # Arrange
    source_markdown = """[fred](  /url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False::  ::]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_before_destination():
    """
    Test case:  inline link label with tabs before the destination
    """

    # Arrange
    source_markdown = """[fred](\t\t/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False::\t\t::]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_before_destination():
    """
    Test case:  inline link label with form feeds before the destination
    """

    # Arrange
    source_markdown = """[fred](\u000c\u000c/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False::\u000c\u000c::]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_after_destination():
    """
    Test case:  inline link label with spaces after the destination
    """

    # Arrange
    source_markdown = """[fred](/url  )"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False:::  :]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_after_destination():
    """
    Test case:  inline link label with tabs after the destination
    """

    # Arrange
    source_markdown = """[fred](/url\t\t)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False:::\t\t:]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_after_destination():
    """
    Test case:  inline link label with form feeds after the destination
    """

    # Arrange
    source_markdown = """[fred](/url\u000c\u000c)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::fred:False:::\u000c\u000c:]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_before_title():
    """
    Test case:  inline link label with spaces before the title
    """

    # Arrange
    source_markdown = """[fred](/url  'title')"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:'::  :]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_before_title():
    """
    Test case:  inline link label with tabs before the title
    """

    # Arrange
    source_markdown = """[fred](/url\t\t'title')"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:'::\t\t:]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_before_title():
    """
    Test case:  inline link label with form feeds before the title
    """

    # Arrange
    source_markdown = """[fred](/url\u000c\u000c'title')"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:'::\u000c\u000c:]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_spaces_after_title():
    """
    Test case:  inline link label with spaces after the title
    """

    # Arrange
    source_markdown = """[fred](/url 'title'  )"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:':: :  ]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_after_title():
    """
    Test case:  inline link label with tabs after the title
    """

    # Arrange
    source_markdown = """[fred](/url 'title'\t\t)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:':: :\t\t]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_whitespaces_inline_link_with_form_feeds_after_title():
    """
    Test case:  inline link label with form feeds after the title
    """

    # Arrange
    source_markdown = """[fred](/url 'title'\u000c\u000c)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::fred:False:':: :\u000c\u000c]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_full_link_with_tabs_in_reference():
    """
    Test case:  inline link label with tabs before the title
    """

    # Arrange
    source_markdown = """[foo][\t\tbar]

[ bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/url:title:::\t\tbar:foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar: bar: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        allow_alternate_markdown=False,
        show_debug=True,
    )


@pytest.mark.gfm
def test_whitespaces_emphasis_1x():
    """
    Test case:  open left is followed by whitespace
    """

    # Arrange
    source_markdown = """* *"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[ulist(1,3):*::4:  ]",
        "[BLANK(1,4):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1xa():
    """
    Test case:  open left is followed by whitespace
    """

    # Arrange
    source_markdown = """** **"""
    expected_tokens = ["[tbreak(1,1):*::** **]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1a():
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """*\u00a0*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[text(1,2):\u00a0:]",
        "[text(1,3):*:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*\u00a0*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1ax():
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """**\u00a0**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):**:]",
        "[text(1,3):\u00a0:]",
        "[text(1,4):**:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>**\u00a0**</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1b():
    """
    Test case:  open left is followed by whitespace
    """

    # Arrange
    source_markdown = """_ _"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):_:]",
        "[text(1,2): :]",
        "[text(1,3):_:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>_ _</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1bx():
    """
    Test case:  open left is followed by whitespace
    """

    # Arrange
    source_markdown = """__ __"""
    expected_tokens = ["[tbreak(1,1):_::__ __]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1c():
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """_\u00a0_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):_:]",
        "[text(1,2):\u00a0:]",
        "[text(1,3):_:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>_\u00a0_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1cx():
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """__\u00a0__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):__:]",
        "[text(1,3):\u00a0:]",
        "[text(1,4):__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>__\u00a0__</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1d():
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """*\u2000*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[text(1,2):\u2000:]",
        "[text(1,3):*:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*\u2000*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1dx():
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """**\u2000**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):**:]",
        "[text(1,3):\u2000:]",
        "[text(1,4):**:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>**\u2000**</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1e():
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """_\u2000_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):_:]",
        "[text(1,2):\u2000:]",
        "[text(1,3):_:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>_\u2000_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1ex():
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """__\u2000__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):__:]",
        "[text(1,3):\u2000:]",
        "[text(1,4):__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>__\u2000__</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_2x():
    """
    Test case:  open left is not followed by unicode whitespace or punctuation
    """

    # Arrange
    source_markdown = """_a_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):a:]",
        "[end-emphasis(1,3)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>a</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_2xx():
    """
    Test case:  open left is not followed by unicode whitespace or punctuation
    """

    # Arrange
    source_markdown = """__a__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):a:]",
        "[end-emphasis(1,4)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>a</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_2a():
    """
    Test case:  open left is not followed by unicode whitespace or punctuation
    """

    # Arrange
    source_markdown = """*a*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):a:]",
        "[end-emphasis(1,3)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>a</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_2ax():
    """
    Test case:  open left is not followed by unicode whitespace or punctuation
    """

    # Arrange
    source_markdown = """**a**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):a:]",
        "[end-emphasis(1,4)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>a</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3x():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """*.foo.*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):.foo.:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>.foo.</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3xx():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """**.foo.**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>.foo.</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3a():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """*\u007efoo\u007e*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):~foo~:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>~foo~</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3ax():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """**\u007efoo\u007e**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):~foo~:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>~foo~</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3b():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """_.foo._"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):.foo.:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>.foo.</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3bx():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """__.foo.__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>.foo.</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3c():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """_\u007efoo\u007e_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):~foo~:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>~foo~</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3cx():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """__\u007efoo\u007e__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):~foo~:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>~foo~</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3d():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line Pc
    """

    # Arrange
    source_markdown = """*\u203ffoo\u203f*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):\u203ffoo\u203f:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>\u203ffoo\u203f</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3dx():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line Pc
    """

    # Arrange
    source_markdown = """**\u203ffoo\u203f**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):\u203ffoo\u203f:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>\u203ffoo\u203f</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3e():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line Pc
    """

    # Arrange
    source_markdown = """_\u203ffoo\u203f_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):\u203ffoo\u203f:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>\u203ffoo\u203f</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3ex():
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """__\u203ffoo\u203f__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):\u203ffoo\u203f:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>\u203ffoo\u203f</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4x():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """ *.foo.* """
    expected_tokens = [
        "[para(1,2): : ]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>.foo.</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4xa():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """ **.foo.** """
    expected_tokens = [
        "[para(1,2): : ]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>.foo.</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4a():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u00a0*.foo.*\u00a0"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u00a0:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):\u00a0:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u00a0<em>.foo.</em>\u00a0</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4ax():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u00a0**.foo.**\u00a0"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u00a0:]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):\u00a0:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u00a0<strong>.foo.</strong>\u00a0</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4b():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """ _.foo._ """
    expected_tokens = [
        "[para(1,2): : ]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>.foo.</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4bx():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """ __.foo.__ """
    expected_tokens = [
        "[para(1,2): : ]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>.foo.</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4c():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u00a0_.foo._\u00a0"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u00a0:]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):\u00a0:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u00a0<em>.foo.</em>\u00a0</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4cx():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u00a0__.foo.__\u00a0"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u00a0:]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):\u00a0:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u00a0<strong>.foo.</strong>\u00a0</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4d():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u2000*.foo.*\u2000"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u2000:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):\u2000:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u2000<em>.foo.</em>\u2000</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4dx():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u2000**.foo.**\u2000"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u2000:]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):\u2000:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u2000<strong>.foo.</strong>\u2000</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4e():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u2000_.foo._\u2000"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u2000:]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):\u2000:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u2000<em>.foo.</em>\u2000</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4ex():
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u2000__.foo.__\u2000"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u2000:]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):\u2000:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u2000<strong>.foo.</strong>\u2000</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5x():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """.*.foo.*."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):.:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>.<em>.foo.</em>.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5xx():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """.**.foo.**."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):.:]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>.<strong>.foo.</strong>.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5a():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u007e*.foo.*\u007e"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):~:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):~:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>~<em>.foo.</em>~</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5ax():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u007e**.foo.**\u007e"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):~:]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):~:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>~<strong>.foo.</strong>~</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5b():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """._.foo._."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):.:]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>.<em>.foo.</em>.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5bx():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """.__.foo.__."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):.:]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>.<strong>.foo.</strong>.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5c():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u007e_.foo._\u007e"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):~:]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):~:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>~<em>.foo.</em>~</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5cx():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u007e__.foo.__\u007e"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):~:]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):~:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>~<strong>.foo.</strong>~</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5d():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u203f*.foo.*\u203f"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):‿:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):‿:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u203f<em>.foo.</em>\u203f</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5dx():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u203f**.foo.**\u203f"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):‿:]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):‿:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u203f<strong>.foo.</strong>\u203f</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5e():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u203f_.foo._\u203f"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):‿:]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):‿:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u203f<em>.foo.</em>\u203f</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5ex():
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u203f__.foo.__\u203f"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):‿:]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):‿:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u203f<strong>.foo.</strong>\u203f</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6x():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a*.foo.*.a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):*:]",
        "[text(1,3):.foo.:]",
        "[text(1,8):*:]",
        "[text(1,9):.a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a*.foo.*.a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6xx():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a**.foo.**.a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):**:]",
        "[text(1,4):.foo.:]",
        "[text(1,9):**:]",
        "[text(1,11):.a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a**.foo.**.a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6a():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a*\u007efoo\u007e*a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):*:]",
        "[text(1,3):~foo~:]",
        "[text(1,8):*:]",
        "[text(1,9):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a*~foo~*a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6ax():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a**\u007efoo\u007e**a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):**:]",
        "[text(1,4):~foo~:]",
        "[text(1,9):**:]",
        "[text(1,11):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a**~foo~**a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6b():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a_.foo._.a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):_:]",
        "[text(1,3):.foo.:]",
        "[text(1,8):_:]",
        "[text(1,9):.a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a_.foo._.a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6bx():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a__.foo.__.a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):__:]",
        "[text(1,4):.foo.:]",
        "[text(1,9):__:]",
        "[text(1,11):.a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a__.foo.__.a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6c():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a_\u007efoo\u007e_a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):_:]",
        "[text(1,3):~foo~:]",
        "[text(1,8):_:]",
        "[text(1,9):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a_~foo~_a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6cx():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a__\u007efoo\u007e__a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):__:]",
        "[text(1,4):~foo~:]",
        "[text(1,9):__:]",
        "[text(1,11):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a__~foo~__a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6d():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a*\u203ffoo\u203f*a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):*:]",
        "[text(1,3):‿foo‿:]",
        "[text(1,8):*:]",
        "[text(1,9):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a*\u203ffoo\u203f*a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6dx():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a**\u203ffoo\u203f**a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):**:]",
        "[text(1,4):‿foo‿:]",
        "[text(1,9):**:]",
        "[text(1,11):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a**\u203ffoo\u203f**a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6e():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a_\u203ffoo\u203f_a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):_:]",
        "[text(1,3):‿foo‿:]",
        "[text(1,8):_:]",
        "[text(1,9):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a_\u203ffoo\u203f_a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6ex():
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a__\u203ffoo\u203f__a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):__:]",
        "[text(1,4):‿foo‿:]",
        "[text(1,9):__:]",
        "[text(1,11):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a__\u203ffoo\u203f__a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
