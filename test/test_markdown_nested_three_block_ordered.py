"""
Extra tests.
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_block_ordered_unordered():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> 1. + list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[ulist(1,6):+::7:   :     ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_unordered():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    + list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[ulist(3,6):+::7:   :     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
  1.
>    + list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[olist(2,3):.:1:5:  ]",
        "[BLANK(2,5):]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> \n> ]",
        "[ulist(3,6):+::7:   :     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ol>
<li></li>
</ol>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
     + list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):+ list: ]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[icode-block(4,7):    :]",
        "[text(4,7):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code> + list
</code></pre>
<blockquote>
<pre><code> item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    + list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[ulist(3,6):+::7:   :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_unordered():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
>    + list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5:]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[ulist(3,6):+::7:   :     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  1. def
>    + list
>      item"""
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
        "[ulist(3,6):+::7:   :     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ol>
<li>def</li>
</ol>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
     + list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::     \n   ]",
        "[para(2,6):\n\n  ]",
        "[text(2,6):def\n+ list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
+ list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
>    + list
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
        "[ulist(3,6):+::7:   :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_ordered_unordered():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> 1. + list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[olist(1,3):.:1:5:]",
        "[ulist(1,6):+::7:   :       ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_unordered():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    + list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[ulist(3,6):+::7:   :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
  1.
>    + list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[olist(2,3):.:1:5:  ]",
        "[BLANK(2,5):]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> \n]",
        "[ulist(3,6):+::7:   :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ol>
<li></li>
</ol>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
     + list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):+ list\n   item: ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code> + list
   item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_ordered_text_nl_unordered():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
>    + list
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
        "[ulist(3,6):+::7:   :       ]",
        "[para(3,8):\n ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_ordered_text_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  1. def
>    + list
       item"""
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
        "[block-quote(3,1)::> \n]",
        "[ulist(3,6):+::7:   :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ol>
<li>def</li>
</ol>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_ordered_text_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
     + list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::     \n     ]",
        "[para(2,6):\n\n  ]",
        "[text(2,6):def\n+ list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
+ list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
def test_nested_three_block_ordered_block_x():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> 1. > list
>    > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::]",
        "[block-quote(1,6)::> \n>    > ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_block_x():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    > list
>    > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5::\n]",
        "[BLANK(2,5):]",
        "[block-quote(3,4)::> \n>    > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_block_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
  1.
>    > list
>    > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[olist(2,3):.:1:5:  ]",
        "[BLANK(2,5):]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,6)::>    > \n>    > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ol>
<li></li>
</ol>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_block_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
     > list
>    > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):\a>\a&gt;\a list: ]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[block-quote(4,6)::>    > ]",
        "[para(4,8):]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code> &gt; list
</code></pre>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_block_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    > list
     > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5::\n]",
        "[BLANK(2,5):]",
        "[block-quote(3,4)::> \n]",
        "[para(3,8):\n     ]",
        "[text(3,8):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_block_x():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
>    > list
>    > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::\n]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,6)::> \n>    > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_block_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  1. def
>    > list
>    > item"""
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
        "[block-quote(3,1)::> ]",
        "[block-quote(3,6)::>    > \n>    > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ol>
<li>def</li>
</ol>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_block_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
     > list
>    > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::     \n]",
        "[para(2,6):\n]",
        "[text(2,6):def\n\a>\a&gt;\a list::\n]",
        "[end-para:::True]",
        "[block-quote(4,6)::> ]",
        "[para(4,8):]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
&gt; list
<blockquote>
<p>item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_block_no_bq3():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
>    > list
     > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::\n]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,6)::> \n]",
        "[para(3,8):\n     ]",
        "[text(3,8):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_ordered_block():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> 1. > list
     > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::]",
        "[block-quote(1,6)::> \n]",
        "[para(1,8):\n     ]",
        "[text(1,8):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_block():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    > list
     > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5::\n]",
        "[BLANK(2,5):]",
        "[block-quote(3,4)::> \n]",
        "[para(3,8):\n     ]",
        "[text(3,8):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_block_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
  1.
>    > list
     > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[olist(2,3):.:1:5:  ]",
        "[BLANK(2,5):]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,6)::>    > \n]",
        "[para(3,8):\n     ]",
        "[text(3,8):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ol>
<li></li>
</ol>
<blockquote>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_block_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
     > list
     > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):\a>\a&gt;\a list\n \a>\a&gt;\a item: ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code> &gt; list
 &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_ordered_text_nl_block():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
>    > list
     > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::\n]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,6)::> \n]",
        "[para(3,8):\n     ]",
        "[text(3,8):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_ordered_text_nl_block_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  1. def
>    > list
     > item"""
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
        "[block-quote(3,1)::> ]",
        "[block-quote(3,6)::>    > \n]",
        "[para(3,8):\n     ]",
        "[text(3,8):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ol>
<li>def</li>
</ol>
<blockquote>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_ordered_text_nl_block_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
     > list
     > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::     \n     ]",
        "[para(2,6):\n\n]",
        "[text(2,6):def\n\a>\a&gt;\a list\n\a>\a&gt;\a item::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
&gt; list
&gt; item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_ordered_block_skip():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> 1. > list
>       item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::]",
        "[block-quote(1,6)::> \n> ]",
        "[para(1,8):\n      ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_block_skip():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    > list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5::\n]",
        "[BLANK(2,5):]",
        "[block-quote(3,4)::> \n> ]",
        "[para(3,8):\n     ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_block_skip_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
  1.
>    > list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[olist(2,3):.:1:5:  ]",
        "[BLANK(2,5):]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,6)::>    > \n> ]",
        "[para(3,8):\n     ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ol>
<li></li>
</ol>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_block_skip_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
     > list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):\a>\a&gt;\a list: ]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[icode-block(4,7):    :]",
        "[text(4,7):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code> &gt; list
</code></pre>
<blockquote>
<pre><code> item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_ordered_nl_block_skip_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    > list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5::\n]",
        "[BLANK(2,5):]",
        "[block-quote(3,4)::> \n]",
        "[para(3,8):\n       ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_block_skip():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
>    > list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::\n]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,6)::> \n> ]",
        "[para(3,8):\n     ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_block_skip_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  1. def
>    > list
>      item"""
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
        "[block-quote(3,1)::> ]",
        "[block-quote(3,6)::>    > \n> ]",
        "[para(3,8):\n     ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ol>
<li>def</li>
</ol>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_block_skip_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
     > list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::     \n   ]",
        "[para(2,6):\n\n  ]",
        "[text(2,6):def\n\a>\a&gt;\a list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
&gt; list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_ordered_text_nl_block_skip_no_bq3():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
>    > list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::\n]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,6)::> \n]",
        "[para(3,8):\n       ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_ordered_block_skip():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> 1. > list
        item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::]",
        "[block-quote(1,6)::> \n]",
        "[para(1,8):\n        ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_block_skip():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
>    > list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5::\n]",
        "[BLANK(2,5):]",
        "[block-quote(3,4)::> \n]",
        "[para(3,8):\n       ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_block_skip_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
  1.
>    > list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[olist(2,3):.:1:5:  ]",
        "[BLANK(2,5):]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,6)::>    > \n]",
        "[para(3,8):\n       ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ol>
<li></li>
</ol>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_ordered_nl_block_skip_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> 1.
    > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:]",
        "[BLANK(2,5):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):\a>\a&gt;\a list\n  item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>&gt; list
  item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_ordered_text_nl_block_skip():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
>    > list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::\n]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,6)::> \n]",
        "[para(3,8):\n       ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_ordered_text_nl_block_skip_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  1. def
>    > list
       item"""
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
        "[block-quote(3,1)::> ]",
        "[block-quote(3,6)::>    > \n]",
        "[para(3,8):\n       ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ol>
<li>def</li>
</ol>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_ordered_text_nl_block_skip_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> 1. def
     > list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5::     \n     ]",
        "[para(2,6):\n\n  ]",
        "[text(2,6):def\n\a>\a&gt;\a list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ol>
<li>def
&gt; list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_unordered_max():
    """
    Verify that a nesting of block quote, ordered list, unordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    1.    + list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:14:   ]",
        "[ulist(1,15):+::16:         :           ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    1.    + list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n]",
        "[olist(1,9):.:1:14:   ]",
        "[ulist(1,15):+::16:         :                ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_ordered_max_unordered_max():
    """
    Verify that a nesting of block quote, ordered list, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    >    1.    + list
    >            item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    1.    + list\n\a>\a&gt;\a            item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    1.    + list
&gt;            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_ordered_max_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    1.    + list
                 item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    1.    + list\n             item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    1.    + list
             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_plus_one_unordered_max():
    """
    Verify that a nesting of block quote, ordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >     1.    + list
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):1.    + list\n        item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>1.    + list
        item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_plus_one_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     1.    + list
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):1.    + list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:             ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>1.    + list
</code></pre>
</blockquote>
<pre><code>             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_unordered_max_plus_one():
    """
    Verify that a nesting of block quote, ordered list, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    1.     + list
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:11:   :      ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):+ list\n  item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<pre><code>+ list
  item
</code></pre>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_unordered_max_plus_one_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    1.     + list
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:11:   ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):+ list:]",
        "[end-icode-block:::False]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:             ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<pre><code>+ list
</code></pre>
</li>
</ol>
</blockquote>
<pre><code>             item
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


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_block_max():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    1.    > list
   >          > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:14:   :]",
        "[block-quote(1,15)::> \n   >          > ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_block_max_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    1.    > list
              > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:14:   :]",
        "[block-quote(1,15)::> \n]",
        "[para(1,17):\n              ]",
        "[text(1,17):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_block_max_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    1.    > list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:14:   :]",
        "[block-quote(1,15)::> \n   > ]",
        "[para(1,17):\n           ]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_block_max_no_bq3():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    1.    > list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:14:   :]",
        "[block-quote(1,15)::> \n]",
        "[para(1,17):\n                ]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_ordered_max_block_max():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    >    1.    > list
    >    1.    > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    1.    \a>\a&gt;\a list\n\a>\a&gt;\a    1.    \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    1.    &gt; list
&gt;    1.    &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_ordered_max_block_max_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    1.    > list
         1.    > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    1.    \a>\a&gt;\a list\n     1.    \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    1.    &gt; list
     1.    &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_ordered_max_block_max_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    1.    > list
    >    1.      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    1.    \a>\a&gt;\a list\n\a>\a&gt;\a    1.      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    1.    &gt; list
&gt;    1.      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_ordered_max_block_max_no_bq3():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    1.    > list
         1.      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    1.    \a>\a&gt;\a list\n     1.      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    1.    &gt; list
     1.      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_plus_one_block_max():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >     1.    > list
   >           > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):1.    \a>\a&gt;\a list\n      \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>1.    &gt; list
      &gt; item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_plus_one_block_max_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     1.    > list
               > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):1.    \a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a item:           ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>1.    &gt; list
</code></pre>
</blockquote>
<pre><code>           &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_plus_one_block_max_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     1.    > list
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):1.    \a>\a&gt;\a list\n        item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>1.    &gt; list
        item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_plus_one_block_max_no_bq3():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     1.    > list
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):1.    \a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:             ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>1.    &gt; list
</code></pre>
</blockquote>
<pre><code>             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_block_max_plus_one():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    1.     > list
   >           > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > \n]",
        "[olist(1,9):.:1:11:   :      ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):\a>\a&gt;\a list\n\a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<pre><code>&gt; list
&gt; item
</code></pre>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_block_max_plus_one_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    1.     > list
               > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:11:   ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):\a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a item:           ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<pre><code>&gt; list
</code></pre>
</li>
</ol>
</blockquote>
<pre><code>           &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_block_max_plus_one_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    1.     > list
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,9):.:1:11:   :      ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):\a>\a&gt;\a list\n  item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<pre><code>&gt; list
  item
</code></pre>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_ordered_max_block_max_plus_one_no_bq3():
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    1.     > list
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[olist(1,9):.:1:11:   ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):\a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:             ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<pre><code>&gt; list
</code></pre>
</li>
</ol>
</blockquote>
<pre><code>             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
