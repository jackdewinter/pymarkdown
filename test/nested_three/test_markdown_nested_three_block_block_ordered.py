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
def test_nested_three_block_max_block_max_ordered_max():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   :      ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    >    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[li(2,14):16:   :1]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list</li>
<li>item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   :      ]",
        "[BLANK(1,16):]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    >    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[li(2,14):16:   :1]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
<li>item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :        ]",
        "[para(1,17):\n]",
        "[text(1,17):list\n\a>\a&gt;\a       item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
&gt;       item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq1_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        >    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :        ]",
        "[para(1,17):\n]",
        "[text(1,17):list\n\a>\a&gt;\a    1. item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
&gt;    1. item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
        >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a       item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    &gt;       item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
        >    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a    1. item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    &gt;    1. item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > ]",
        "[olist(1,14):.:1:16:   :           ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq2_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >         1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > ]",
        "[olist(1,14):.:1:16:   :        ]",
        "[para(1,17):\n]",
        "[text(1,17):list\n1. item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:       ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>       item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >         1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:    ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>    1. item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :                ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq3_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
             1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :             ]",
        "[para(1,17):\n]",
        "[text(1,17):list\n1. item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
             1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):1. item:         ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>         1. item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    >    >       item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n\a>\a&gt;\a    \a>\a&gt;\a       item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
&gt;    &gt;       item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
         >       item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n     \a>\a&gt;\a       item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
     &gt;       item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    >            item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n\a>\a&gt;\a            item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
&gt;            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
                 item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n             item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   >     >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    1. list\n\a>\a&gt;\a       item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
&gt;       item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    1. list
         >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a       item:     ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<pre><code>     &gt;       item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    1. list\n        item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
        item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:             ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<pre><code>             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   >    >        item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):1. list\n   item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
   item
</code></pre>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
        >        item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a        item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<pre><code>    &gt;        item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:        ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
<pre><code>        item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:             ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<pre><code>             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
