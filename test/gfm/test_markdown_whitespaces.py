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
@pytest.mark.skip
def test_whitespaces_block_quotes_with_tabs():
    """
    Test case:  Block quotes preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ > block quote
 >\t> another block quote"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):\\\b\\this is a fun day: ]",
        "[end-atx::]",
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
@pytest.mark.skip
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
\u000C+ inner list item</li>
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
def test_whitespaces_thematic_breaks_with_tabs_before():
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t * * *"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):* * *: ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code> * * *
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
    expected_tokens = ["[tbreak(1,1):*::* * *]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
    expected_tokens = ["[tbreak(1,1):*::* * *   ]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
def test_whitespaces_atx_headings_with_tabs_before():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t # abc"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):# abc: ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code> # abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,5):abc:   ]", "[end-atx::]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc: ]", "[end-atx:   :]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc: ]", "[end-atx::   ]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc: ]", "[end-atx: : ]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
def test_whitespaces_setext_headings_with_tabs_before():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """abc
\t---"""
    expected_tokens = [
        "[para(1,1):\n    ]",
        "[text(1,1):abc\n---::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
---</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[end-setext:: ]",
    ]
    expected_gfm = """<h2>abc</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
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
--- \u000C</p>"""

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
def test_whitespaces_indented_code_with_tabs_before():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """\tindented block"""
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
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t```python
abc"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[end-fcode-block:::True]",
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
        "[fcode-block(1,1):`:3:python::::: ]",
        "[text(2,1):abc:]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[end-fcode-block:::True]",
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
        "[end-fcode-block:::True]",
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
        "[fcode-block(1,1):`:3:python::   :::]",
        "[text(2,1):abc:]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_fenced_code_open_with_form_feeds_after_info():
    """
    Test case:  Fenced Code blocks info string followed by form feeds.
    """

    # Arrange
    source_markdown = """```python\u000C
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python\u000C:::::]",
        "[text(2,1):abc:]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[end-fcode-block:  :3:False]",
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
        "[text(2,1):abc\n    ```:]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
    ```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
\u000C```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
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
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
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
        "[text(2,1):abc:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
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
        "[text(2,1):abc:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
```\u000C
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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


def test_whitespaces_html_with_tabs_before():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t<!-- comment"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):\a<\a&lt;\a!-- comment:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&lt;!-- comment
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[text(1,1):<dialog :]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog """

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[text(1,1):<dialog>    :]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog>    """

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
def test_whitespaces_lrd_with_tabs_before():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """\t[fred]: /url
[fred]"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
def test_whitespaces_lrd_with_tabs_before_label():
    """
    Test case:  LRD link label preceeded by tabs.
    """

    # Arrange
    source_markdown = """[\t\tfred]: /url
[ fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:       fred: :/url:::::]",
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
def test_whitespaces_lrd_with_tabs_after_label():
    """
    Test case:  LRD link label followwed by tabs.
    """

    # Arrange
    source_markdown = """[fred\t\t]: /url
[fred ]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:fred       : :/url:::::]",
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
def test_whitespaces_lrd_with_tabs_in_label():
    """
    Test case:  LRD link label followwed by tabs.
    """

    # Arrange
    source_markdown = """[fred\t\tboy]: /url
[fred boy]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred boy:fred       boy: :/url:::::]",
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
def test_whitespaces_lrd_with_tabs_before_destination():
    """
    Test case:  LRD destination preceeded by tabs.
    """

    # Arrange
    source_markdown = """[fred]:\t/url
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:: :/url:::::]",
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
def test_whitespaces_lrd_with_tabs_after_destination():
    """
    Test case:  LRD destination followed by tabs.
    """

    # Arrange
    source_markdown = """[fred]: /url\t\t
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:: :/url::        :::]",
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
def test_whitespaces_lrd_with_tabs_before_title():
    """
    Test case:  LRD title preceeded by tabs.
    """

    # Arrange
    source_markdown = """[fred]: /url\t"title"
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url::    :title:"title":]',
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
def test_whitespaces_lrd_with_tabs_after_title():
    """
    Test case:  LRD title followed by tabs.
    """

    # Arrange
    source_markdown = """[fred]: /url "title"\t\t
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url:: :title:"title":        ]',
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
def test_whitespaces_paragraph_with_tabs_paragraph():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """\ta paragraph"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):a paragraph:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>a paragraph
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[para(1,1):: ]",
        "[text(1,1):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
@pytest.mark.skip
def test_whitespaces_code_span_with_tabs():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a `\tgood\t` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):good   :`: : ]",
        "[text(1,14): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>good</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
@pytest.mark.skip
def test_whitespaces_hard_break_with_tabs():
    """
    Test case:  hard_break with tabs
    """

    # Arrange
    source_markdown = """foo\t\t
bar"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo:]",
        "[hard-break(1,4):     :\n]",
        "[text(2,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo		
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
def test_whitespaces_autolink_uri_with_tabs():
    """
    Test case:  autolink_uri with tabs
    """

    # Arrange
    source_markdown = """<http://foo.bar.baz/test?q=hello\tman&id=22&boolean>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\ahttp://foo.bar.baz/test?q=hello    man\a&\a&amp;\aid=22\a&\a&amp;\aboolean\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;http://foo.bar.baz/test?q=hello    man&amp;id=22&amp;boolean&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_inline_link_with_tabs_before_label():
    """
    Test case:  inline link label with tabs before
    """

    # Arrange
    source_markdown = """[\tfred](/url)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:::::   fred:False::::]",
        "[text(1,2):   fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">   fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[link(1,1):shortcut:/url:::::       fred:False::::]",
        "[text(1,2):       fred:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred: fred: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">       fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[link(1,1):inline:/url:::::fred       boy:False::::]",
        "[text(1,2):fred       boy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred       boy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[link(1,1):shortcut:/url:::::fred       boy:False::::]",
        "[text(1,2):fred       boy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred boy:: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred       boy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[link(1,1):inline:/url:::::fred       :False::::]",
        "[text(1,2):fred       :]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred       </a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[link(1,1):shortcut:/url:::::fred       :False::::]",
        "[text(1,2):fred       :]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::fred:fred : :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">fred       </a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[link(1,1):inline:/url:::::fred:False::     ::]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[link(1,1):inline:/url:::::fred:False:::     :]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[link(1,1):inline:/url:title::::fred:False:'::     :]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[link(1,1):inline:/url:title::::fred:False:':: :     ]",
        "[text(1,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
