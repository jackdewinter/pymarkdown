"""
Extra tests.
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> + + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :    ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6:  :    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
  +
>   + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> \n> ]",
        "[ulist(3,5):+::6:  :    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ul>
<li></li>
</ul>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
    + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):+ list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[icode-block(4,7):    :]",
        "[text(4,7):item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>+ list
</code></pre>
<blockquote>
<pre><code>item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6:  :    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  + def
>   + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> \n> ]",
        "[ulist(3,5):+::6:  :    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ul>
<li>def</li>
</ul>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
    + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::    \n  ]",
        "[para(2,5):\n\n  ]",
        "[text(2,5):def\n+ list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
+ list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_unordered_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> + + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :      ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
  +
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> \n]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ul>
<li></li>
</ul>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
    + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):+ list\n  item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>+ list
  item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_unordered_text_nl_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_unordered_text_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  + def
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> \n]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ul>
<li>def</li>
</ul>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_unordered_text_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
    + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::    \n    ]",
        "[para(2,5):\n\n  ]",
        "[text(2,5):def\n+ list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
+ list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_ordered():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> + 1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[olist(1,5):.:1:7:  :     ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_ordered():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7:  :     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
  +
>   1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> \n> ]",
        "[olist(3,5):.:1:7:  :     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ul>
<li></li>
</ul>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
    1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[icode-block(4,7):    :]",
        "[text(4,7):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>1. list
</code></pre>
<blockquote>
<pre><code> item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7:  :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_ordered():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7:  :     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  + def
>   1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> \n> ]",
        "[olist(3,5):.:1:7:  :     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ul>
<li>def</li>
</ul>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
    1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::    \n  ]",
        "[para(2,5):\n\n   ]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
1. list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7:  :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_unordered_ordered():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> + 1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[ulist(1,3):+::4:]",
        "[olist(1,5):.:1:7:  :       ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_ordered():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7:  :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
  +
>   1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> \n]",
        "[olist(3,5):.:1:7:  :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ul>
<li></li>
</ul>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
    1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):1. list\n   item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>1. list
   item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_x():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> + > list
>   > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n>   > ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_block_x():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   > list
>   > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4::\n]",
        "[BLANK(2,4):]",
        "[block-quote(3,3)::> \n>   > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_block_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote works
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
def test_nested_three_block_nl_unordered_nl_block_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
    > list
>   > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[block-quote(4,5)::>   > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>&gt; list
</code></pre>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_block_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4::\n]",
        "[BLANK(2,4):]",
        "[block-quote(3,3)::> \n]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_block_x():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   > list
>   > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::\n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n>   > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_block_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  + def
>   > list
>   > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
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
<p>abc</p>
</blockquote>
<ul>
<li>def</li>
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
def test_nested_three_block_text_nl_unordered_text_nl_block_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
    > list
>   > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::    \n]",
        "[para(2,5):\n]",
        "[text(2,5):def\n\a>\a&gt;\a list::\n]",
        "[end-para:::True]",
        "[block-quote(4,5)::> ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
&gt; list
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_block_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::\n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_unordered_block():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> + > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n]",
        "[para(1,7):\n    ]",
        "[text(1,7):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_block():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4::\n]",
        "[BLANK(2,4):]",
        "[block-quote(3,3)::> \n]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_block_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
  +
>   > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,5)::>   > \n]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\n\a>\a&gt;\a item::\n]",
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
&gt; item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_block_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
    > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):\a>\a&gt;\a list\n\a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>&gt; list
&gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_unordered_text_nl_block():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::\n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_unordered_text_nl_block_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  + def
>   > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,5)::>   > \n]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ul>
<li>def</li>
</ul>
<blockquote>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_unordered_text_nl_block_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
    > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::    \n    ]",
        "[para(2,5):\n\n]",
        "[text(2,5):def\n\a>\a&gt;\a list\n\a>\a&gt;\a item::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
&gt; list
&gt; item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_skip():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> + > list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n> ]",
        "[para(1,7):\n    ]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_block_skip():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   > list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4::\n]",
        "[BLANK(2,4):]",
        "[block-quote(3,3)::> \n> ]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_block_skip_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
  +
>   > list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,5)::>   > \n> ]",
        "[para(3,7):\n    ]",
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
def test_nested_three_block_nl_unordered_nl_block_skip_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
    > list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[icode-block(4,7):    :]",
        "[text(4,7):item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>&gt; list
</code></pre>
<blockquote>
<pre><code>item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_block_skip_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4::\n]",
        "[BLANK(2,4):]",
        "[block-quote(3,3)::> \n]",
        "[para(3,7):\n      ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_block_skip():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   > list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::\n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n> ]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_block_skip_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  + def
>   > list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,5)::>   > \n> ]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ul>
<li>def</li>
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
def test_nested_three_block_text_nl_unordered_text_nl_block_skip_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
    > list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::    \n  ]",
        "[para(2,5):\n\n  ]",
        "[text(2,5):def\n\a>\a&gt;\a list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
&gt; list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_block_skip_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::\n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n]",
        "[para(3,7):\n      ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_unordered_block_skip():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> + > list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n]",
        "[para(1,7):\n       ]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_block_skip():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4::\n]",
        "[BLANK(2,4):]",
        "[block-quote(3,3)::> \n]",
        "[para(3,7):\n      ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_block_skip_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
  +
>   > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,5)::>   > \n]",
        "[para(3,7):\n      ]",
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
def test_nested_three_block_skip_nl_unordered_nl_block_skip_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
    > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):\a>\a&gt;\a list\n  item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>&gt; list
  item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_unordered_text_nl_block_skip():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::\n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n]",
        "[para(3,7):\n      ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_unordered_text_nl_block_skip_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  + def
>   > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,5)::>   > \n]",
        "[para(3,7):\n      ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ul>
<li>def</li>
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
def test_nested_three_block_skip_text_nl_unordered_text_nl_block_skip_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
    > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::    \n    ]",
        "[para(2,5):\n\n  ]",
        "[text(2,5):def\n\a>\a&gt;\a list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
&gt; list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    +    + list
   >           item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        :          ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_empty():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   >    +    +
   >           item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        :          ]",
        "[BLANK(1,15):]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    + list
               item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        :               ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_empty_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    +
               item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        ]",
        "[BLANK(1,15):]",
        "[end-ulist:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:           ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>
</blockquote>
<pre><code>           item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_unordered_max_unordered_max():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    >    +    + list
    >           item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    +    + list\n\a>\a&gt;\a           item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    +    + list
&gt;           item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_unordered_max_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    +    + list
                item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    +    + list\n            item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    +    + list
            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_plus_one_unordered_max():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >     +    + list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):+    + list\n       item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>+    + list
       item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_plus_one_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     +    + list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):+    + list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>+    + list
</code></pre>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_plus_one():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    +     + list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::10:   :     ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):+ list\n  item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<pre><code>+ list
  item
</code></pre>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_plus_one_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +     + list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::10:   ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):+ list:]",
        "[end-icode-block:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<pre><code>+ list
</code></pre>
</li>
</ul>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_ordered_max():
    """
    Verify that a nesting of block quote, unordered list, ordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    +    1. list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[olist(1,14):.:1:16:        :           ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_ordered_max_empty():
    """
    Verify that a nesting of block quote, unordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   >    +    1.
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[olist(1,14):.:1:16:        :           ]",
        "[BLANK(1,16):]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, ordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    1. list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n]",
        "[ulist(1,9):+::13:   ]",
        "[olist(1,14):.:1:16:        :                ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_ordered_max_empty_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    1.
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   ]",
        "[olist(1,14):.:1:16:        ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ol>
<li></li>
</ol>
</li>
</ul>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_unordered_max_ordered_max():
    """
    Verify that a nesting of block quote, unordered list, ordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    >    +    1.  list
    >             item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    +    1.  list\n\a>\a&gt;\a             item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    +    1.  list
&gt;             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_unordered_max_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, ordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    +    1.  list
                  item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    +    1.  list\n              item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    +    1.  list
              item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_plus_one_ordered_max():
    """
    Verify that a nesting of block quote, unordered list, ordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >     +    1. list
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):+    1. list\n        item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>+    1. list
        item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_plus_one_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, ordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     +    1. list
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):+    1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:             ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>+    1. list
</code></pre>
</blockquote>
<pre><code>             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_ordered_max_plus_one():
    """
    Verify that a nesting of block quote, unordered list, ordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    +     1. list
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::10:   :     ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):1. list\n   item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<pre><code>1. list
   item
</code></pre>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_ordered_max_plus_one_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, ordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +     1. list
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::10:   ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:             ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<pre><code>1. list
</code></pre>
</li>
</ul>
</blockquote>
<pre><code>             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_block_max():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    +    > list
   >         > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   :]",
        "[block-quote(1,14)::> \n   >         > ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_max_unordered_max_block_max_empty():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   >    +    >
   >         > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   :]",
        "[block-quote(1,14)::> \n   >         > ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_block_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    > list
             > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   :]",
        "[block-quote(1,14)::> \n]",
        "[para(1,16):\n             ]",
        "[text(1,16):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_block_max_empty_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    >
             > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   ]",
        "[block-quote(1,14)::>]",
        "[BLANK(1,15):]",
        "[end-block-quote:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a item:         ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
</blockquote>
</li>
</ul>
</blockquote>
<pre><code>         &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_block_max_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    > list
   >           item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   :]",
        "[block-quote(1,14)::> \n   > ]",
        "[para(1,16):\n          ]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_max_unordered_max_block_max_empty_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    >
   >           item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   :\n]",
        "[block-quote(1,14)::>\n   > ]",
        "[BLANK(1,15):]",
        "[BLANK(1,15):]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:      ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
</blockquote>
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_block_max_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    > list
               item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   :]",
        "[block-quote(1,14)::> \n]",
        "[para(1,16):\n               ]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_block_max_empty_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    >
               item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   ]",
        "[block-quote(1,14)::>]",
        "[BLANK(1,15):]",
        "[end-block-quote:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:           ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
</blockquote>
</li>
</ul>
</blockquote>
<pre><code>           item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_unordered_max_block_max():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    >    +    > list
    >         > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    +    \a>\a&gt;\a list\n\a>\a&gt;\a         \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    +    &gt; list
&gt;         &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_unordered_max_block_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    +    > list
              > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    +    \a>\a&gt;\a list\n          \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    +    &gt; list
          &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_unordered_max_block_max_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    +    > list
    >           item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    +    \a>\a&gt;\a list\n\a>\a&gt;\a           item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    +    &gt; list
&gt;           item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_unordered_max_block_max_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    +    > list
                item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    +    \a>\a&gt;\a list\n            item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    +    &gt; list
            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_plus_one_block_max():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >     +    > list
   >          > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):+    \a>\a&gt;\a list\n     \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>+    &gt; list
     &gt; item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_plus_one_block_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     +    > list
              > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):+    \a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a item:          ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>+    &gt; list
</code></pre>
</blockquote>
<pre><code>          &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_plus_one_block_max_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     +    > list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):+    \a>\a&gt;\a list\n       item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>+    &gt; list
       item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_plus_one_block_max_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     +    > list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):+    \a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>+    &gt; list
</code></pre>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_block_max_plus_one():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    +     > list
   >          > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > \n]",
        "[ulist(1,9):+::10:   :     ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):\a>\a&gt;\a list\n\a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<pre><code>&gt; list
&gt; item
</code></pre>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_block_max_plus_one_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +     > list
              > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::10:   ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):\a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a item:          ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<pre><code>&gt; list
</code></pre>
</li>
</ul>
</blockquote>
<pre><code>          &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_block_max_plus_one_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +     > list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::10:   :     ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):\a>\a&gt;\a list\n  item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<pre><code>&gt; list
  item
</code></pre>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_block_max_plus_one_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +     > list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::10:   ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):\a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<pre><code>&gt; list
</code></pre>
</li>
</ul>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
