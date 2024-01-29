"""
Extra tests.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_block_ordered_ordered():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> 1. 1. list
>       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[olist(1,6):.:1:8:   :      ]",
        "[para(1,9):\n]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_ordered():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    1. list
>       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[olist(3,6):.:1:8:   :      ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
  1.
>    1. list
>       item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[olist(2,3):.:1:5:  ]",
        "[BLANK(2,5):]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> \n> ]",
        "[olist(3,6):.:1:8:   :      ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ol>
<li></li>
</ol>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
     1. list
>       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list: ]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[icode-block(4,7):    :]",
        "[text(4,7):item:  ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code> 1. list
</code></pre>
<blockquote>
<pre><code>  item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    1. list
        item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[olist(3,6):.:1:8:   :        ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_ordered_x():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
>    1. list
>       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5:]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[olist(3,6):.:1:8:   :      ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  1. def
>    1. list
>       item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(2,3):.:1:5:  ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> \n> ]",
        "[olist(3,6):.:1:8:   :      ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ol>
<li>def</li>
</ol>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
     1. list
>       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::     \n   ]",
        "[para(2,6):\n\n   ]",
        "[text(2,6):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
1. list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
>    1. list
        item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5:]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[olist(3,6):.:1:8:   :        ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_ordered_ordered():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> 1. 1. list
        item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[olist(1,3):.:1:5:]",
        "[olist(1,6):.:1:8:   :        ]",
        "[para(1,9):\n]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_ordered():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    1. list
        item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[olist(3,6):.:1:8:   :        ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
  1.
>    1. list
        item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[olist(2,3):.:1:5:  ]",
        "[BLANK(2,5):]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> \n]",
        "[olist(3,6):.:1:8:   :        ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ol>
<li></li>
</ol>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
     1. list
        item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):1. list\n    item: ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code> 1. list
    item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    1.    1. list
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         :            ]",
        "[para(1,18):\n]",
        "[text(1,18):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_with_li1():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1. list
   >    1.       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(2,9):11:   :1]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list</li>
</ol>
</li>
<li>
<pre><code>  item
</code></pre>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_with_li2():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1. list
   >          1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[li(2,15):17:         :1]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list</li>
<li>item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_with_li3():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1. list
   >    1.    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(2,9):14:   :1]",
        "[olist(2,15):.:1:17:         ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list</li>
</ol>
</li>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_empty():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   >    1.    1.
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         :            ]",
        "[BLANK(1,17):]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_empty_with_li1():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1.
   >    1.       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         ]",
        "[BLANK(1,17):]",
        "[end-olist:::True]",
        "[li(2,9):11:   :1]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li></li>
</ol>
</li>
<li>
<pre><code>  item
</code></pre>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_empty_with_li2():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1.
   >          1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         ]",
        "[BLANK(1,17):]",
        "[li(2,15):17:         :1]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li></li>
<li>item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_empty_with_li3():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1.
   >    1.    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         ]",
        "[BLANK(1,17):]",
        "[end-olist:::True]",
        "[li(2,9):14:   :1]",
        "[olist(2,15):.:1:17:         ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li></li>
</ol>
</li>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    1.    1. list
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         :                 ]",
        "[para(1,18):\n]",
        "[text(1,18):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_no_bq1_with_li1():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1. list
        1.       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         :        ]",
        "[para(1,18):\n]",
        "[text(1,18):list\n1.       item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
1.       item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_no_bq1_with_li2():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1. list
              1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         :              ]",
        "[para(1,18):\n]",
        "[text(1,18):list\n1. item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
1. item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_no_bq1_with_li3():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1. list
        1.    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         :        ]",
        "[para(1,18):\n]",
        "[text(1,18):list\n1.    1. item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
1.    1. item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_empty_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    1.    1.
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         ]",
        "[BLANK(1,17):]",
        "[end-olist:::False]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:             ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
</blockquote>
<pre><code>             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_empty_no_bq1_with_li1():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1.
        1.       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         ]",
        "[BLANK(1,17):]",
        "[end-olist:::False]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):1.       item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
</blockquote>
<pre><code>    1.       item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_empty_no_bq1_with_li2():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1.
              1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         ]",
        "[BLANK(1,17):]",
        "[end-olist:::False]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):1. item:          ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
</blockquote>
<pre><code>          1. item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_empty_no_bq1_with_li3():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    1.    1.
        1.    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[olist(1,15):.:1:17:         ]",
        "[BLANK(1,17):]",
        "[end-olist:::False]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):1.    1. item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
</blockquote>
<pre><code>    1.    1. item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_ordered_max_ordered_max():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    >    1.    1.  list
    >              item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    1.    1.  list\n\a>\a&gt;\a              item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    1.    1.  list
&gt;              item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_ordered_max_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    1.    1.  list
                   item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    1.    1.  list\n               item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    1.    1.  list
               item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_plus_one_ordered_max():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >     1.    1. list
   >              item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):1.    1. list\n         item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>1.    1. list
         item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_plus_one_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     1.    1. list
                  item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):1.    1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:              ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>1.    1. list
</code></pre>
</blockquote>
<pre><code>              item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_plus_one():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    1.     1. list
   >              item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:11:   :      ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):1. list\n   item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<pre><code>1. list
   item
</code></pre>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_ordered_max_plus_one_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, ordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    1.     1. list
                  item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:11:   ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):1. list:]",
        "[end-icode-block:::False]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:              ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<pre><code>1. list
</code></pre>
</li>
</ol>
</blockquote>
<pre><code>              item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
