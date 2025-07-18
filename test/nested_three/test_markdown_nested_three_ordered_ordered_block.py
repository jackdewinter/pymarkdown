"""
Extra tests for three level nesting with un/un.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_ordered_ordered_block_x() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. 1. > list
      > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :]",
        "[block-quote(1,7):      :      > \n      > ]",
        "[para(1,9):\n]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_ordered_nl_block_x() -> None:
    """
    Verify that a nesting of ordered list, new line, ordered list, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   1.
      > list
      > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :\n]",
        "[BLANK(2,6):]",
        "[block-quote(3,7):      :      > \n      > ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_ordered_text_nl_block_x() -> None:
    """
    Verify that a nesting of ordered list, text, new line, ordered list, text, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
      > list
      > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[block-quote(3,7):      :      > \n      > ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_ordered_block_skip() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. 1. > list
        item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :      \n]",
        "[block-quote(1,7):      :      > \n]",
        "[para(1,9):\n  ]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_ordered_nl_block_skip() -> None:
    """
    Verify that a nesting of ordered list, new line, ordered list, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   1.
      > list
        item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :\n      \n]",
        "[BLANK(2,6):]",
        "[block-quote(3,7):      :      > \n]",
        "[para(3,9):\n  ]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_ordered_text_nl_block_skip() -> None:
    """
    Verify that a nesting of ordered list, text, new line, ordered list, text, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
      > list
        item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n      \n]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[block-quote(3,7):      :      > \n]",
        "[para(3,9):\n  ]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    1.    > list
               > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         :]",
        "[block-quote(1,16):               :               > \n               > ]",
        "[para(1,18):\n]",
        "[text(1,18):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_with_li1() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    > list
   1.          > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[block-quote(1,16):               :               > ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):\a>\a&gt;\a item:     ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
</ol>
</li>
<li>
<pre><code>     &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_with_li2() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    > list
         1.    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         :]",
        "[block-quote(1,16):               :               > ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(2,10):15:         :1]",
        "[block-quote(2,16):               :               > ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_with_li3() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    > list
   1.    1.    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[block-quote(1,16):               :               > ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[li(2,4):9:   :1]",
        "[olist(2,10):.:1:15:         ]",
        "[block-quote(2,16):               :               > ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
</ol>
</li>
<li>
<ol>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_empty() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   1.    1.    >
               > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         :]",
        "[block-quote(1,16):               :               >\n               > ]",
        "[BLANK(1,17):]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_empty_with_li1() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    >
   1.          > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[block-quote(1,16):               :               >]",
        "[BLANK(1,17):]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):\a>\a&gt;\a item:     ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
</blockquote>
</li>
</ol>
</li>
<li>
<pre><code>     &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_empty_with_li2() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    >
         1.    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         :]",
        "[block-quote(1,16):               :               >]",
        "[BLANK(1,17):]",
        "[end-block-quote:::True]",
        "[li(2,10):15:         :1]",
        "[block-quote(2,16):               :               > ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
</blockquote>
</li>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_empty_with_li3() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    >
   1.    1.    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[block-quote(1,16):               :               >]",
        "[BLANK(1,17):]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[li(2,4):9:   :1]",
        "[olist(2,10):.:1:15:         ]",
        "[block-quote(2,16):               :               > ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
</blockquote>
</li>
</ol>
</li>
<li>
<ol>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    1.    > list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         :               \n]",
        "[block-quote(1,16):               :               > \n]",
        "[para(1,18):\n  ]",
        "[text(1,18):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_no_bq1_with_li1() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    1.    > list
   1.            item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[block-quote(1,16):               :               > ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):item:       ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
</ol>
</li>
<li>
<pre><code>       item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_no_bq1_with_li2() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    1.    > list
         1.      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[block-quote(1,16):               :               > ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(2,10):12:         :1]",
        "[icode-block(2,17):    :]",
        "[text(2,17):item: ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_no_bq1_with_li3() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    1.    > list
   1.    1.      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[block-quote(1,16):               :               > ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[li(2,4):9:   :1]",
        "[olist(2,10):.:1:12:         ]",
        "[icode-block(2,17):    :]",
        "[text(2,17):item: ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
</ol>
</li>
<li>
<ol>
<li>
<pre><code> item
</code></pre>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_empty_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly, with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    1.    >
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         :               ]",
        "[block-quote(1,16):               :               >]",
        "[BLANK(1,17):]",
        "[end-block-quote:::False]",
        "[para(2,18):  ]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
</blockquote>
item</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_empty_no_bq1_with_li1() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly, with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    >
   1.          > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[block-quote(1,16):               :               >]",
        "[BLANK(1,17):]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):\a>\a&gt;\a item:     ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
</blockquote>
</li>
</ol>
</li>
<li>
<pre><code>     &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_empty_no_bq1_with_li2() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly, with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    >
         1.    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         :]",
        "[block-quote(1,16):               :               >]",
        "[BLANK(1,17):]",
        "[end-block-quote:::True]",
        "[li(2,10):15:         :1]",
        "[block-quote(2,16):               :               > ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
</blockquote>
</li>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_empty_no_bq1_with_li3() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly, with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    >
   1.    1.    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[block-quote(1,16):               :               >]",
        "[BLANK(1,17):]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[li(2,4):9:   :1]",
        "[olist(2,10):.:1:15:         ]",
        "[block-quote(2,16):               :               > ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<blockquote>
</blockquote>
</li>
</ol>
</li>
<li>
<ol>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_ordered_max_block_max() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    1.    1.    > list
                > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    1.    \a>\a&gt;\a list\n            \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    1.    &gt; list
            &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_ordered_max_block_max_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    1.    1.    > list
                  item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    1.    \a>\a&gt;\a list\n              item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    1.    &gt; list
              item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_plus_one_block_max() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.     1.    > list
                > item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):1.    \a>\a&gt;\a list\n      \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>1.    &gt; list
      &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_plus_one_block_max_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.     1.    > list
                  item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):1.    \a>\a&gt;\a list\n        item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>1.    &gt; list
        item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_plus_one() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    1.     > list
                > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:12:         :            ]",
        "[icode-block(1,17):    :\n    ]",
        "[text(1,17):\a>\a&gt;\a list\n\a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<pre><code>&gt; list
&gt; item
</code></pre>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_block_max_plus_one_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, ordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    1.     > list
                  item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:12:         :            ]",
        "[icode-block(1,17):    :\n    ]",
        "[text(1,17):\a>\a&gt;\a list\n  item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<pre><code>&gt; list
  item
</code></pre>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
