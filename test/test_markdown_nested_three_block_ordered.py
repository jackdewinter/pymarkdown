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
def test_nested_three_block_text_nl_ordered_text_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
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
@pytest.mark.skip
def test_nested_three_block_skip_nl_ordered_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
  1.
     1. list
        item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[olist(2,3):.:1:5:  ]",
        "[BLANK(2,5):]",
        "[end-olist:::True]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):1. list\n    item: ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>"""

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
def test_nested_three_block_nl_ordered_nl_block_no_bq1():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
  +
>   > list
>   > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,5)::>   > \n>   > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ul>
<li></li>
</ul>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
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
