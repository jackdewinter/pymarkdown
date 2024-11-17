"""
Extra tests for three level nesting with un/or.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered():
    """
    Verify that a nesting of ordered list, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. > + list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,6):+::7::  ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_unordered():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > + list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n   > \n   > ]",
        "[BLANK(2,5):]",
        "[ulist(3,6):+::7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_unordered_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     + list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[end-block-quote:::True]",
        "[ulist(3,6):+::7:     ]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,4):   :   > ]",
        "[para(4,8):  ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
</blockquote>
<ul>
<li>list</li>
</ul>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_unordered():
    """
    Verify that a nesting of ordered list, text, new line, block quote, text, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > + list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n   > \n   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[ulist(3,6):+::7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_unordered_wo_bq():
    """
    Verify that a nesting of ordered list, text, new line, block quote, text, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     + list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(3,6):+::7:     ]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,4):   :   > ]",
        "[para(4,8):  ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list</li>
</ul>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_skip_unordered():
    """
    Verify that a nesting of ordered list, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. > + list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n]",
        "[ulist(1,6):+::7::       \n]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_unordered():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > + list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n   > \n]",
        "[BLANK(2,5):]",
        "[ulist(3,6):+::7::       \n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_unordered_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     + list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[end-block-quote:::True]",
        "[ulist(3,6):+::7:     :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_unordered():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > + list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n   > \n]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[ulist(3,6):+::7::       \n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_unordered_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     + list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(3,6):+::7:     :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    >    + list
         >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[ulist(1,15):+::16:   :     ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_with_li1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    + list
   1.    >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):9:   :1]",
        "[block-quote(2,10):         :         > ]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list</li>
</ul>
</blockquote>
</li>
<li>
<blockquote>
<pre><code> item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_with_li2():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    + list
         >    + item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[ulist(1,15):+::16:   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[li(2,15):16:   :]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list</li>
<li>item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_with_li3():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    + list
   1.    >    + item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):9:   :1]",
        "[block-quote(2,10):         :         > ]",
        "[ulist(2,15):+::16:   ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list</li>
</ul>
</blockquote>
</li>
<li>
<blockquote>
<ul>
<li>item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_empty():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   1.    >    +
         >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[ulist(1,15):+::16:   :     ]",
        "[BLANK(1,16):]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_empty_li1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    +
   1.    >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):9:   :1]",
        "[block-quote(2,10):         :         > ]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</li>
<li>
<blockquote>
<pre><code> item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_empty_li2():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    +
         >    + item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[ulist(1,15):+::16:   ]",
        "[BLANK(1,16):]",
        "[li(2,15):16:   :]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li></li>
<li>item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_empty_li3():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.

    was: test_extra_027x
    """

    # Arrange
    source_markdown = """   1.    >    +
   1.    >    + item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):9:   :1]",
        "[block-quote(2,10):         :         > ]",
        "[ulist(2,15):+::16:   ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</li>
<li>
<blockquote>
<ul>
<li>item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    + list
                item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n]",
        "[ulist(1,15):+::16:   :                \n]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_no_bq1_with_li1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    + list
   1.           item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):item:      ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list</li>
</ul>
</blockquote>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_no_bq1_with_li2():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    + list
              + item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n]",
        "[ulist(1,15):+::16:   :              ]",
        "[para(1,17):\n]",
        "[text(1,17):list\n+ item::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
+ item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_no_bq1_with_li3():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    + list
   1.         + item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):+ item:    ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list</li>
</ul>
</blockquote>
</li>
<li>
<pre><code>    + item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_empty_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    +
                item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):item:   ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>   item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_empty_no_bq1_with_li1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    +
   1.           item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):item:      ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_empty_no_bq1_with_li2():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    +
              + item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):+ item: ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code> + item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_empty_no_bq1_with_li3():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    +
   1.         + item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):+ item:    ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</li>
<li>
<pre><code>    + item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_unordered_max():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    1.    >    + list
          >      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    + list\n      \a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    + list
      &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_unordered_max_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    1.    >    + list
                 item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    + list\n             item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    + list
             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_unordered_max():
    """
    Verify that a nesting of ordered list, unordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.     >    + list
          >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    + list\n\a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    + list
&gt;      item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_unordered_max_no_bq1():
    """
    Verify that a nesting of ordered list, unordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.     >    + list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    + list\n       item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    + list
       item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_plus_one():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    >     + list
         >       item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):+ list\n  item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>+ list
  item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_plus_one_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >     + list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):+ list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):item:    ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>+ list
</code></pre>
</blockquote>
<pre><code>    item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_nl_extra_block_drop_block_fenced():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    and extra block quote, drop the block quote, and a fenced block.

    was: test_extra_044mcw0, test_extra_044mx1
    refs: bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block
    """
    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   >   ```block
   >   A code block
   >   ```
   >   ----"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::\n\n  þ\n  \n  \n  ]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[fcode-block(4,8):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_nl_extra_block_drop_block_blanks_around_fenced():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    and extra block quote, drop the block quote, and blanks around a fenced block.

    was: test_extra_044mcw1
    refs: bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block
    """
    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   ----"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   >\n   > ]",
        "[ulist(1,6):+::7::\n\n\n  \n  \n  \n\n  ]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n   >]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,5):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,5):]",
        "[tbreak(9,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_thematics_around_fenced():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    thematics around a fenced block.

    was: test_extra_044mx2
    refs: bad_fenced_block_in_list_in_block_quote_in_list
    """

    # Arrange
    source_markdown = """1. > + ----
   >   ```block
   >   A code block
   >   ```
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::  \n  \n  \n  ]",
        "[tbreak(1,8):-::----]",
        "[fcode-block(2,8):`:3:block:::::]",
        "[text(3,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(5,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_extra_block_drop_block_with_headings_around_fenced():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    thematics around a fenced block.

    was: test_extra_044mcw2
    refs: bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_4
    """
    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   >   # header 1
   >   ```block
   >   A code block
   >   ```
   >   # header 2
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::\n\n  þ\n  \n  \n  \n  ]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[atx(4,8):1:0:]",
        "[text(4,10):header 1: ]",
        "[end-atx::]",
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[atx(8,8):1:0:]",
        "[text(8,10):header 2: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<h1>header 1</h1>
<pre><code class="language-block">A code block
</code></pre>
<h1>header 2</h1>
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_extra_list_li_drop_list_with_fenced():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    thematics around a fenced block.

    was: test_extra_046p0
    refs: bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list
    """
    # Arrange
    source_markdown = """1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >   ```block
   >   A code block
   >   ```
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::  \n  \n  ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9:  :    \n  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9:  :]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_extra_list_li_drop_list_with_blanks_around_fenced():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    thematics around a fenced block.

    was: test_extra_046p1
    refs: bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list
    """
    # Arrange
    source_markdown = """1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   >\n   > \n   > \n   > \n   >\n   > ]",
        "[ulist(1,6):+::7::  \n  \n\n  ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9:  :    \n\n  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9:  :]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,5):]",
        "[end-ulist:::True]",
        "[fcode-block(6,8):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,5):]",
        "[tbreak(10,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_extra_list_li_drop_list_with_thematics_around_fenced():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    thematics around a fenced block.

    was: test_extra_046n0
    refs: bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_with_thematics
    """
    # Arrange
    source_markdown = """1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >   ----
   >   ```block
   >   A code block
   >   ```
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::  \n  \n  \n  ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9:  :    \n  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9:  :]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,8):-::----]",
        "[fcode-block(6,8):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_extra_list_li_drop_list_with_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    thematics around a fenced block.

    was: test_extra_046n0
    refs: bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_with_thematics
    """
    # Arrange
    source_markdown = """1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >   ----
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   >\n   > \n   > \n   > \n   >\n   > ]",
        "[ulist(1,6):+::7::\n  \n  \n  \n\n  ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9:  :    \n  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9:  :]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,8):-::----]",
        "[BLANK(6,5):]",
        "[fcode-block(7,8):`:3:block:::::]",
        "[text(8,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,5):]",
        "[tbreak(11,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_li_with_empty_prefix_extra_block_drop_block_headings_around_text():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.

    Note: In commonmark java 0.13.0 and commonmark.js 0.28.1, both
    report that the `A code block` should be in a paragraph, hinting
    that it is loose.  There are no blank lines, hence, cannot be loose.

    was: test_extra_044mx30
    """
    # Arrange
    source_markdown = """1. > + ----
       first list item    
     + next list item    
   >   > block 1
   >   > block 2
   >   # header
   >   A code block
   >   # header
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,6):+::7:]",
        "[tbreak(1,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,8):    :]",
        "[text(2,8):first list item    :]",
        "[end-icode-block:::True]",
        "[ulist(3,6):+::7:     ]",
        "[para(3,8)::    ]",
        "[text(3,8):next list item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,4):   :   > \n   > \n   > \n   > \n]",
        "[block-quote(4,8)::   >   > \n   >   > \n   > ]",
        "[para(4,10):\n]",
        "[text(4,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[atx(6,8):1:0:  ]",
        "[text(6,10):header: ]",
        "[end-atx::]",
        "[para(7,8):  ]",
        "[text(7,8):A code block:]",
        "[end-para:::False]",
        "[atx(8,8):1:0:  ]",
        "[text(8,10):header: ]",
        "[end-atx::]",
        "[tbreak(9,8):-:  :----]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
</li>
</ul>
</blockquote>
<pre><code>first list item    
</code></pre>
<ul>
<li>next list item</li>
</ul>
<blockquote>
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<h1>header</h1>
A code block
<h1>header</h1>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_extra_block_drop_block_headings_around_text():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.

    was: test_extra_044mx31
    """
    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   >   # header
   >   A code block
   >   # header
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::\n\n  þ\n  \n  \n  ]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[atx(4,8):1:0:]",
        "[text(4,10):header: ]",
        "[end-atx::]",
        "[para(5,8):]",
        "[text(5,8):A code block:]",
        "[end-para:::False]",
        "[atx(6,8):1:0:]",
        "[text(6,10):header: ]",
        "[end-atx::]",
        "[tbreak(7,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<h1>header</h1>
A code block
<h1>header</h1>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_thematics_around_headings_around_text():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.

    was: test_extra_044mx4
    """
    # Arrange
    source_markdown = """1. > + ----
   >   # header
   >   A code block
   >   # header
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::  \n  \n  \n  ]",
        "[tbreak(1,8):-::----]",
        "[atx(2,8):1:0:]",
        "[text(2,10):header: ]",
        "[end-atx::]",
        "[para(3,8):]",
        "[text(3,8):A code block:]",
        "[end-para:::False]",
        "[atx(4,8):1:0:]",
        "[text(4,10):header: ]",
        "[end-atx::]",
        "[tbreak(5,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<h1>header</h1>
A code block
<h1>header</h1>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_extra_block_drop_block_thematics_around_text():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.

    was: test_extra_044mx50
    """
    # Arrange
    source_markdown = """1. > + _____
   >   > block 1
   >   > block 2
   >   _____
   >   A code block
   >   _____
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::\n\n  þ\n  \n  ]",
        "[tbreak(1,8):_::_____]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[tbreak(4,8):_::_____]",
        "[para(5,8):]",
        "[text(5,8):A code block:]",
        "[end-para:::False]",
        "[tbreak(6,8):_::_____]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<hr />
A code block
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered_extra_block_drop_block_html_around_text():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.

    was: test_extra_044mx60
    """
    # Arrange
    source_markdown = """1. > + _____
   >   > block 1
   >   > block 2
   >   <!--
   >   A code block
   >   -->
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::\n\n  þ\n  \n  ]",
        "[tbreak(1,8):_::_____]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[html-block(4,8)]",
        "[text(4,8):<!--\nA code block\n-->:]",
        "[end-html-block:::False]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<!--
A code block
-->
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
