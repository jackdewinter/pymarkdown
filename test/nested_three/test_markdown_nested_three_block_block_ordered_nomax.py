"""
Extra tests.
"""
from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_block_block_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
> >    item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > ]",
        "[olist(1,5):.:1:7::   ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
> > item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > ]",
        "[olist(1,5):.:1:7::]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_ordered_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> ]",
        "[olist(1,5):.:1:7::]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_ordered_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[olist(1,5):.:1:7::\n]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
> >    item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n> > ]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::   ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
> > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n> > ]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n> ]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
> >    item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,8):   ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list</li>
</ol>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
> > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,5):]",
        "[text(4,5):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list</li>
</ol>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
> >    item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  ]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,8):   ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list</li>
</ol>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
> > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  ]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,5):]",
        "[text(4,5):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list</li>
</ol>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
> >    item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::]",
        "[block-quote(4,3)::> > ]",
        "[para(4,8):   ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
> > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::]",
        "[block-quote(4,3)::> > ]",
        "[para(4,5):]",
        "[text(4,5):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[para(4,3):]",
        "[text(4,3):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<blockquote>
<p>item</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_ordered_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::False]",
        "[para(4,1):]",
        "[text(4,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
> >    item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::   ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
> > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
> >    item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,8):   ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list</li>
</ol>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
> > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,5):]",
        "[text(4,5):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list</li>
</ol>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
> >    item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  ]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,8):   ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list</li>
</ol>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
> > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  ]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,5):]",
        "[text(4,5):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list</li>
</ol>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
> >    item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n> > ]",
        "[para(2,5):\n    \n   ]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
> > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n> > ]",
        "[para(2,5):\n    \n]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n> ]",
        "[para(2,5):\n    \n]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_ordered_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n    \n]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
  >    item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n  > ]",
        "[olist(1,5):.:1:7::   ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
  > item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n  > ]",
        "[olist(1,5):.:1:7::]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_ordered_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[olist(1,5):.:1:7::  ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_ordered_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[olist(1,5):.:1:7::\n]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
  >    item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n  > ]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::   ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
  > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n  > ]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
  >    item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n  > ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::   ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
  > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n  > ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
  >    item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n  > ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :   ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
  > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n  > ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
  >    item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,3):  :  > ]",
        "[para(4,8):   ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<blockquote>
<p>item</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
  > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,3):  :  > ]",
        "[para(4,5):]",
        "[text(4,5):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<blockquote>
<p>item</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::False]",
        "[para(4,3):  ]",
        "[text(4,3):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_ordered_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::False]",
        "[para(4,1):]",
        "[text(4,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
  >    item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::   ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
  > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
  >    item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n  > ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::   ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
  > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n  > ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
  >    item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n  > ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :   ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
  > item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n  > ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
  >    item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n  > ]",
        "[para(2,5):\n    \n   ]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
  > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n  > ]",
        "[para(2,5):\n    \n]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n    \n  ]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_ordered_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n    \n]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_skip_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> ]",
        "[olist(1,5):.:1:7::     ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_skip_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
>   item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> ]",
        "[olist(1,5):.:1:7::  ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_skip_ordered_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> ]",
        "[olist(1,5):.:1:7::]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_skip_ordered_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[olist(1,5):.:1:7::\n]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n> ]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
>   item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n> ]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n> ]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
>   item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
>   item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
>   item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :  ]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
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
<blockquote>
</blockquote>
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
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
>   item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[para(4,5):  ]",
        "[text(4,5):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<blockquote>
<p>item</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[para(4,3):]",
        "[text(4,3):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<blockquote>
<p>item</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_ordered_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::False]",
        "[para(4,1):]",
        "[text(4,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
>   item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
>   item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :     ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
>   item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :  ]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n> ]",
        "[para(2,5):\n    \n     ]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
>   item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n> ]",
        "[para(2,5):\n    \n  ]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
> item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n> ]",
        "[para(2,5):\n    \n]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_ordered_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n    \n]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_skip_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[olist(1,5):.:1:7::       ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_skip_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > 1. list
    item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[olist(1,5):.:1:7::    ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > 1. list
    item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::    ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
    item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::    ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
    item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :    ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):1. list\n   item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
   item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
    item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):1. list\nitem:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::False]",
        "[para(4,3):  ]",
        "[text(4,3):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_ordered_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):1. list:]",
        "[end-icode-block:::False]",
        "[para(4,1):]",
        "[text(4,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>1. list
</code></pre>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
    item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::    ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
    item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::    ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > 1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n  > \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7::\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
    item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :    ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:  :\n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n    \n       ]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
    item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n    \n    ]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
  item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n    \n  ]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_ordered_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    1. list
item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n    \n]",
        "[text(2,5):def\n1. list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
1. list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
