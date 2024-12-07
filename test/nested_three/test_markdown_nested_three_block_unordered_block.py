"""
Extra tests.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


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
        "[block-quote(3,5)::> \n>   > ]",
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
        "[block-quote(3,5)::> \n]",
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
        "[block-quote(3,5)::> \n]",
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
        "[ulist(1,3):+::4::  þ]",
        "[block-quote(1,5)::> \n> ]",
        "[para(1,7):\n  ]",
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
        "[ulist(2,3):+::4::\n  þ]",
        "[BLANK(2,4):]",
        "[block-quote(3,5)::> \n> ]",
        "[para(3,7):\n  ]",
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
        "[block-quote(3,5)::> \n]",
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
        "[ulist(2,3):+::4::\n  þ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n> ]",
        "[para(3,7):\n  ]",
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
        "[block-quote(3,5)::> \n]",
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
def test_nested_three_block_max_unordered_max_block_max_with_li():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    > list
   >    +    > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   :]",
        "[block-quote(1,14)::> \n   > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(2,9):13:   :]",
        "[block-quote(2,14)::   > ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
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
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
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
        "[block-quote(1,14)::>\n   >         > ]",
        "[BLANK(1,15):]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
def test_nested_three_block_max_unordered_max_block_max_empty_with_li():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with a list item.

    ISSUE: https://github.com/jackdewinter/pymarkdown/issues/296
    """

    # Arrange
    source_markdown = """   >    +    >
   >    +    > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   :]",
        "[block-quote(1,14)::>]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[li(2,9):13:   :]",
        "[block-quote(2,14)::   > ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
</blockquote>
</li>
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
def test_nested_three_block_max_unordered_max_block_max_no_bq1_with_li():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    > list
        +    > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   :]",
        "[block-quote(1,14)::> \n]",
        "[para(1,16):\n        ]",
        "[text(1,16):list\n+    \a>\a&gt;\a item::\n]",
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
+    &gt; item</p>
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
def test_nested_three_block_max_unordered_max_block_max_empty_no_bq1_with_li():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    >
        +    > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   ]",
        "[block-quote(1,14)::>]",
        "[BLANK(1,15):]",
        "[end-block-quote:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):+    \a>\a&gt;\a item:    ]",
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
<pre><code>    +    &gt; item
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
        "[ulist(1,9):+::13:   :        þ]",
        "[block-quote(1,14)::> \n   > ]",
        "[para(1,16):\n  ]",
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
def test_nested_three_block_max_unordered_max_block_max_no_bq2_with_li():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    > list
   >    +      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   ]",
        "[block-quote(1,14)::> \n   > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(2,9):10:   :]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_block_max_empty_no_bq2_x():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    >
   >           item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   :        ]",
        "[block-quote(1,14)::>]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[para(2,16):  ]",
        "[text(2,16):item:]",
        "[end-para:::True]",
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
def test_nested_three_block_max_unordered_max_block_max_empty_no_bq2_with_li():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.

    ISSUE: https://github.com/jackdewinter/pymarkdown/issues/296
    """

    # Arrange
    source_markdown = """   >    +    >
   >    +      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[block-quote(1,14)::>]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[li(2,9):10:   :]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
</blockquote>
</li>
<li>
<pre><code> item
</code></pre>
</li>
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
def test_nested_three_block_max_unordered_max_block_max_no_bq3_with_li():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    > list
        +      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   :]",
        "[block-quote(1,14)::> \n]",
        "[para(1,16):\n        ]",
        "[text(1,16):list\n+      item::\n]",
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
+      item</p>
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
def test_nested_three_block_max_unordered_max_block_max_empty_no_bq3_with_li():
    """
    Verify that a nesting of block quote, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    >
        +      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   ]",
        "[block-quote(1,14)::>]",
        "[BLANK(1,15):]",
        "[end-block-quote:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):+      item:    ]",
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
<pre><code>    +      item
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


@pytest.mark.gfm
def test_nested_three_block_unordered_block_fenced_empty_with_thematics():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing an empty fenced code block surrounded by thematic blocks.

    Was: test_extra_044jxx
    Refs: bad_fenced_block_in_block_quote_in_list_in_block_quote_empty
    """

    # Arrange
    source_markdown = """> + > -----
>   > ```block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[fcode-block(2,7):`:3:block:::::]",
        "[end-fcode-block:::3:False]",
        "[tbreak(4,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(5,3):4::]",
        "[para(5,5):]",
        "[text(5,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block"></code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_fenced_empty_with_blanks_with_thematics():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing an empty fenced code block surrounded by blank lines and then thematic blocks.

    Was: test_extra_044jxa
    Refs: bad_fenced_block_in_block_quote_in_list_in_block_quote_empty
    """

    # Arrange
    source_markdown = """> + > -----
>   >
>   > ```block
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n]",
        "[block-quote(1,5)::> \n>   >\n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,6):]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,6):]",
        "[tbreak(6,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block"></code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_fenced_with_thematics():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by thematic blocks.

    Was: test_extra_044jax
    Refs: bad_fenced_block_in_block_quote_in_list_in_block_quote
    """

    # Arrange
    source_markdown = """> + > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[fcode-block(2,7):`:3:block:::::]",
        "[text(3,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(5,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(6,3):4::]",
        "[para(6,5):]",
        "[text(6,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_fenced_with_blanks_with_thematics():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by blanks and then thematic blocks.

    Was: test_extra_044jaa
    Refs: bad_fenced_block_in_block_quote_in_list_in_block_quote
    """

    # Arrange
    source_markdown = """> + > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,6):]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,6):]",
        "[tbreak(7,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_fenced_with_text_before_with_thematics():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by text and thematic blocks.

    Was: test_extra_044jbx
    """

    # Arrange
    source_markdown = """> + > -----
>   > def
>   > ```block
>   > abc
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,7):abc:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(6,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>def</p>
<pre><code class="language-block">abc
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_fenced_with_blanks_with_text_before_with_thematics():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by blanks, text, and thematic blocks.

    Was: test_extra_044jba
    """

    # Arrange
    source_markdown = """> + > -----
>   > def
>   >
>   > ```block
>   > abc
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[BLANK(3,6):]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):abc:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(7,6):]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>def</p>
<pre><code class="language-block">abc
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_fenced_with_text_after_with_thematics():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by text and thematic blocks.

    Was: test_extra_044jcx
    """

    # Arrange
    source_markdown = """> + > -----
>   > ```block
>   > abc
>   > ```
>   > def
>   > _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[fcode-block(2,7):`:3:block:::::]",
        "[text(3,7):abc:]",
        "[end-fcode-block:::3:False]",
        "[para(5,7):]",
        "[text(5,7):def:]",
        "[end-para:::False]",
        "[tbreak(6,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block">abc
</code></pre>
<p>def</p>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_fenced_with_blanks_with_text_after_with_thematics():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by blanks, text, and thematic blocks.

    Was: test_extra_044jca
    """

    # Arrange
    source_markdown = """> + > -----
>   >
>   > ```block
>   > abc
>   > ```
>   >
>   > def
>   > _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,6):]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,7):abc:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,6):]",
        "[para(7,7):]",
        "[text(7,7):def:]",
        "[end-para:::False]",
        "[tbreak(8,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block">abc
</code></pre>
<p>def</p>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_fenced_multiline_with_thematics():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a multiline fenced code block surrounded by thematic blocks.

    Was: test_extra_044jd
    """
    # Arrange
    source_markdown = """> + > -----
>   > ```block
>   > abc
>   > def
>   > ```
>   > _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[fcode-block(2,7):`:3:block:::::]",
        "[text(3,7):abc\ndef:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(6,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block">abc
def
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_thematics_around_text_lines():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a thematic blocks around text lines.

    Was: test_extra_044jex
    """
    # Arrange
    source_markdown = """> + > -----
>   > block
>   > abc
>   > un-block
>   > _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):\n\n]",
        "[text(2,7):block\nabc\nun-block::\n\n]",
        "[end-para:::False]",
        "[tbreak(5,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(6,3):4::]",
        "[para(6,5):]",
        "[text(6,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>block
abc
un-block</p>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_thematics_around_blanks_around_text_lines():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a thematic blocks around blanks around text lines.

    Was: test_extra_044k0
    """

    # Arrange
    source_markdown = """> + > -----
>   > 
>   > block
>   > abc
>   > un-block
>   > 
>   > _____
> + more
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,7):]",
        "[para(3,7):\n\n]",
        "[text(3,7):block\nabc\nun-block::\n\n]",
        "[end-para:::True]",
        "[BLANK(6,7):]",
        "[tbreak(7,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):more:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>block
abc
un-block</p>
<hr />
</blockquote>
</li>
<li>more</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_thematics_around_text_lines_with_text_after():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a thematic blocks around text lines.

    Was: test_extra_044jea
    """
    # Arrange
    source_markdown = """> + > -----
>   > block
>   > abc
>   > un-block
>   > _____
>   > more
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):\n\n]",
        "[text(2,7):block\nabc\nun-block::\n\n]",
        "[end-para:::False]",
        "[tbreak(5,7):_::_____]",
        "[para(6,7):]",
        "[text(6,7):more:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>block
abc
un-block</p>
<hr />
<p>more</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_block_drop_block_thematics_around_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    dropping the block quote, with a fenced block surrounded by thematics.

    Was: test_extra_044la0
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_0
    """
    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ\n  \n  \n  \n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(4,5):-::------]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::------]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<blockquote>
<p>block 2
block 3</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_block_drop_block_thematics_around_blanks_around_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    dropping the block quote, with a fenced block surrounded by thematics.

    Was: test_extra_044la1
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_0
    """
    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ\n\n  \n  \n  \n\n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(4,5):-::------]",
        "[BLANK(5,2):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):-::------]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<blockquote>
<p>block 2
block 3</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_list__li_drop_list_thematics_around_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new list with a new list item, dropping that list, and thematics around
    a fenced block surrounded.

    Was: test_extra_044mcu0
    refs: bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_and_thematics
    """
    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):-::-----]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
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
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_list__li_drop_list_thematics_around_blanks_around_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new list with a new list item, dropping that list, and thematics around
    blanks around a fenced block.

    Was: test_extra_044mcu1
    refs: bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_and_thematics
    """
    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):-::-----]",
        "[BLANK(6,6):]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,6):]",
        "[tbreak(11,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(12,3):4::]",
        "[para(12,5):]",
        "[text(12,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
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
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_block_single_line_drop_block_thematics_around_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote with a single line, dropping that block, and thematics around
    a fenced block.

    Was: test_extra_044lde
    """
    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > ]",
        "[para(2,9):]",
        "[text(2,9):block 1:]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(3,7):-::-----]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_block_drop_block_thematics_around_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote, dropping that block, and thematics around a fenced block.

    Was: test_extra_044lddx test_extra_044mcv0
    refs: bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_with_thematics
    """
    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(4,7):-::-----]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_block_drop_block_thematics_around_blanks_around_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote, dropping that block, and thematics around blanks around a fenced block.

    Was: test_extra_044mcv1
    refs: bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_with_thematics
    """
    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(4,7):-::-----]",
        "[BLANK(5,6):]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,6):]",
        "[tbreak(10,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_block_drop_block_with_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote, dropping that block, and a fenced block.

    Was: test_extra_044mcz1
    refs: bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blockx
    """
    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_block_drop_block_with_blanks_around_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote, dropping that block, and a fenced block.

    Was: test_extra_046ca
    refs: bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blockx
    """
    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   >\n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,6):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,6):]",
        "[tbreak(9,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_block_with_extra_single_indent_drop_block_with_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote indented by an extra space, dropping that block, and a fenced block.

    Was: test_extra_044mcz2
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>    ```block
>    A code block
>    ```
>    -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  ]",
        "[ulist(1,5):+::6:  :\n\n  þ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,6):`:3:block:::: :]",
        "[text(5,5):A code block:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
        "[tbreak(7,6):-: :-----]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_block_with_extra_double_indent_drop_block_with_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote indented by an extra space, dropping that block, and a fenced block.

    Was: test_extra_044mcz3
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>   ```block
>   A code block
>   ```
>   -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  ]",
        "[ulist(1,5):+::6:  :\n\n  þ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,5):-::-----]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_block_with_extra_triple_indent_drop_block_with_fenced_code_block():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote indented by an extra space, dropping that block, and a fenced block.

    Was: test_extra_044mcz4
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>  ```block
>  A code block
>  ```
>  -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,4):`:3:block:::: :]",
        "[text(5,3):A code block:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
        "[tbreak(7,4):-: :-----]",
        "[ulist(8,3):+::4:]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_block_drop_block_extra_block_drop_block_fenced():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote indented by an extra space, dropping that block, and a fenced block.

    Was: test_extra_047d0
    refs: bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blocks
    """
    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   > > block 1
>   > > block 2
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(4,7):-::-----]",
        "[block-quote(5,7)::>   > > \n>   > > \n>   > ]",
        "[para(5,9):\n]",
        "[text(5,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(10,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_extra_block_drop_block_extra_block_drop_block_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote indented by an extra space, dropping that block, and a fenced block.

    Was: test_extra_047d1
    refs: bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blocks
    """
    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   > > block 1
>   > > block 2
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(4,7):-::-----]",
        "[block-quote(5,7)::>   > > \n>   > > \n>   >\n>   > ]",
        "[para(5,9):\n]",
        "[text(5,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(7,6):]",
        "[end-block-quote:::True]",
        "[fcode-block(8,7):`:3:block:::::]",
        "[text(9,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(11,6):]",
        "[tbreak(12,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(13,3):4::]",
        "[para(13,5):]",
        "[text(13,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(14,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_block_drop_block_with_fenced():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote indented by an extra space, dropping that block, and a fenced block.

    Was: test_extra_046g0
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_0_without_thematics
    """
    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
>   ```block
>   A code block
>   ```
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ\n  \n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<blockquote>
<p>block 2
block 3</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_block_drop_block_with_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote indented by an extra space, dropping that block, and a fenced block.

    Was: test_extra_046g1
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_0_without_thematics
    """
    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
>
>   ```block
>   A code block
>   ```
>
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> ]",
        "[ulist(1,3):+::4::\n\n\n  \n  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n>]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<blockquote>
<p>block 2
block 3</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_thematics_around_text_and_fenced():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote, dropping that block, and a fenced block.

    Was: test_extra_044fxx
    """
    # Arrange
    source_markdown = """> + > -----
>   > abc
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::False]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(6,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>abc</p>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_thematics_around_text_and_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote, dropping that block, and a fenced block.

    Was: test_extra_044fxx
    """
    # Arrange
    source_markdown = """> + > -----
>   > abc
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[BLANK(3,6):]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(7,6):]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>abc</p>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_thematic_drop_block_and_list_with_text():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote, dropping that block, and a fenced block.

    Was: test_extra_044fa
    """
    # Arrange
    source_markdown = """> + > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[block-quote(1,5)::> ]",
        "[tbreak(1,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(2,3):4::]",
        "[para(2,5):]",
        "[text(2,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_thematic_nl_text_drop_block_and_list_with_text():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote, dropping that block, and a fenced block.

    Was: test_extra_044fa
    """
    # Arrange
    source_markdown = """> + > -----
>   > abc
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n>   > \n> ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>abc</p>
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_thematic_nl_fenced_with_drop_block_li():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote, dropping that block, and a fenced block.

    Was: test_extra_044fc
    """
    # Arrange
    source_markdown = """> + > -----
>   > ```block
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[fcode-block(2,7):`:3:block:::::]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block"></code></pre>
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_fenced_with_drop_right_after():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote, dropping that block, and a fenced block.

    Was: test_extra_044fd
    """
    # Arrange
    source_markdown = """> + > ```block
>   > abc
>   > ```
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n]",
        "[block-quote(1,5)::> \n>   > \n>   > ]",
        "[fcode-block(1,7):`:3:block:::::]",
        "[text(2,7):abc:]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
        "[li(4,3):4::]",
        "[para(4,5):]",
        "[text(4,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<pre><code class="language-block">abc
</code></pre>
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_empty_fenced_with_drop_right_after():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    a new block quote, dropping that block, and a fenced block.

    Was: test_extra_044fe
    """
    # Arrange
    source_markdown = """> + > ```block
>   > ```
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n>   > ]",
        "[fcode-block(1,7):`:3:block:::::]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<pre><code class="language-block"></code></pre>
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_thematics_around_blanks_around_text_drop_block_li_li_extra_block_drop_block_li():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by blanks and then thematic blocks.

    Was: test_extra_044kx
    """
    # Arrange
    source_markdown = """> + > -----
>   > 
>   > block
>   > abc
>   > un-block
>   > 
>   > _____
> + more
>   this is more
> + some
>   > more
> + more
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n  \n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,7):]",
        "[para(3,7):\n\n]",
        "[text(3,7):block\nabc\nun-block::\n\n]",
        "[end-para:::True]",
        "[BLANK(6,7):]",
        "[tbreak(7,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):\n]",
        "[text(8,5):more\nthis is more::\n]",
        "[end-para:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):some:]",
        "[end-para:::True]",
        "[block-quote(11,5)::> \n> ]",
        "[para(11,7):]",
        "[text(11,7):more:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(12,3):4::]",
        "[para(12,5):]",
        "[text(12,5):more:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(13,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>block
abc
un-block</p>
<hr />
</blockquote>
</li>
<li>more
this is more</li>
<li>some
<blockquote>
<p>more</p>
</blockquote>
</li>
<li>more</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_thematics_around_blank_drop_block_li_text():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by blanks and then thematic blocks.

    Was: test_extra_044k1
    """
    # Arrange
    source_markdown = """> + > -----
>   > 
>   > _____
> + more
>   this is more
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n  ]",
        "[block-quote(1,5)::> \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,7):]",
        "[tbreak(3,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(4,3):4::]",
        "[para(4,5):\n]",
        "[text(4,5):more\nthis is more::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<hr />
</blockquote>
</li>
<li>more
this is more</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_thematics_around_blank_drop_block_li_extra_block_text():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by blanks and then thematic blocks.

    Was: test_extra_044k2
    """
    # Arrange
    source_markdown = """> + > -----
>   > 
>   > _____
> + > more
>   > this is more
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,7):]",
        "[tbreak(3,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(4,3):4::]",
        "[block-quote(4,5)::> \n>   > \n]",
        "[para(4,7):\n]",
        "[text(4,7):more\nthis is more::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<hr />
</blockquote>
</li>
<li>
<blockquote>
<p>more
this is more</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_block_drop_block_headings_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by blanks and then thematic blocks.

    Was: test_extra_044lb
    """
    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
>   # xxx
>   ```block
>   A code block
>   ```
>   # xxx
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ\n  \n  \n  \n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[atx(4,5):1:0:]",
        "[text(4,7):xxx: ]",
        "[end-atx::]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[atx(8,5):1:0:]",
        "[text(8,7):xxx: ]",
        "[end-atx::]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<blockquote>
<p>block 2
block 3</p>
</blockquote>
<h1>xxx</h1>
<pre><code class="language-block">A code block
</code></pre>
<h1>xxx</h1>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_block_drop_block_blank_thematics_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by blanks and then thematic blocks.

    Was: test_extra_044lda
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>
>     -----
>     ```block
>     A code block
>     ```
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n\n    \n    \n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n>]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[tbreak(5,7):-::-----]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-ulist:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_extra_block_with_no_space_after_drop_block_thematics_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by blanks and then thematic blocks.

    Was: test_extra_044ldd1
    """
    # Arrange
    source_markdown = """> + > -----
>   > >block 1
>   > >block 2
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > >\n>   > >\n>   > ]",
        "[para(2,8):\n]",
        "[text(2,8):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(4,7):-::-----]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_extra_block_drop_block_thematic_extra_block_drop_block_thematics_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by blanks and then thematic blocks.

    Was: test_extra_044ldf
    """
    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > -----
>   > > block 1
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > ]",
        "[para(2,9):]",
        "[text(2,9):block 1:]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(3,7):-::-----]",
        "[block-quote(4,7)::>   > > \n>   > ]",
        "[para(4,9):]",
        "[text(4,9):block 1:]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(5,7):-::-----]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1</p>
</blockquote>
<hr />
<blockquote>
<p>block 1</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_extra_list_drop_list_thematics_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, block quote,
    containing a fenced code block surrounded by blanks and then thematic blocks.

    Was: test_extra_044ldg
    """
    # Arrange
    source_markdown = """> + > -----
>   > + block 1
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:]",
        "[para(2,9):]",
        "[text(2,9):block 1:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(3,7):-::-----]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>block 1</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
