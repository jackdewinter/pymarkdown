"""
Extra tests.
"""
from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_block_block_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> > > list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n> > > ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > > list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[block-quote(3,1)::> > > \n> > > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_block_no_bq1():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > > list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n  > > ]",
        "[BLANK(2,4):]",
        "[para(3,7):]",
        "[text(3,7):list:]",
        "[end-para:::True]",
        "[block-quote(4,1)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_block_no_bq2():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   > list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n>   > ]",
        "[BLANK(2,4):]",
        "[para(3,7):]",
        "[text(3,7):list:]",
        "[end-para:::True]",
        "[block-quote(4,1)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_block_no_bq3():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    > list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::]",
        "[block-quote(4,3)::]",
        "[block-quote(4,5)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>&gt; list
</code></pre>
<blockquote>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_block_no_bq4():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> >   list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > ]",
        "[BLANK(2,4):]",
        "[para(3,7):  ]",
        "[text(3,7):list:]",
        "[end-para:::True]",
        "[block-quote(4,1)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_block_no_bq5():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  >   list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[para(3,7):  ]",
        "[text(3,7):list:]",
        "[end-para:::True]",
        "[block-quote(4,1)::]",
        "[block-quote(4,3)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<p>list</p>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_block_no_bq6():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>     list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[icode-block(3,7):    :]",
        "[text(3,7):list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::]",
        "[block-quote(4,3)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<pre><code>list
</code></pre>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_block_no_bq7():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
      list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):list:  ]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::]",
        "[block-quote(4,3)::]",
        "[block-quote(4,5)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>  list
</code></pre>
<blockquote>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > > list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,1)::> > > \n> > > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_block_no_bq1():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > > list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n  > > ]",
        "[para(2,5):\n]",
        "[text(2,5):def\nlist::\n]",
        "[end-para:::True]",
        "[block-quote(4,1)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_block_no_bq2():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   > list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n>   > ]",
        "[para(2,5):\n]",
        "[text(2,5):def\nlist::\n]",
        "[end-para:::True]",
        "[block-quote(4,1)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_block_no_bq3():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    > list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n    ]",
        "[text(2,5):def\n\a>\a&gt;\a list::\n]",
        "[end-para:::True]",
        "[block-quote(4,1)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
&gt; list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_block_no_bq4():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> >   list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > ]",
        "[para(2,5):\n  ]",
        "[text(2,5):def\nlist::\n]",
        "[end-para:::True]",
        "[block-quote(4,1)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_block_no_bq5():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  >   list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n  > ]",
        "[para(2,5):\n  ]",
        "[text(2,5):def\nlist::\n]",
        "[end-para:::True]",
        "[block-quote(4,1)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_block_no_bq6():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>     list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):\n    ]",
        "[text(2,5):def\nlist::\n]",
        "[end-para:::True]",
        "[block-quote(4,1)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_block_no_bq7():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
      list
> > > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n      ]",
        "[text(2,5):def\nlist::\n]",
        "[end-para:::True]",
        "[block-quote(4,1)::> > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> > > list
  > > item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n  > > ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > > list
  > > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[block-quote(3,1)::> > > \n  > > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > > list
  > > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,1)::> > > \n  > > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_skip_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> > > list
>   > item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n>   > ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > > list
>   > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[block-quote(3,1)::> > > \n>   > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > > list
>   > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,1)::> > > \n>   > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_skip_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> > > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n]",
        "[para(1,7):\n    ]",
        "[text(1,7):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[block-quote(3,1)::> > > \n]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_block():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,1)::> > > \n]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> > > list
> >   item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n> > ]",
        "[para(1,7):\n  ]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > > list
> >   item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[block-quote(3,1)::> > > \n> > ]",
        "[para(3,7):\n  ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > > list
> >   item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,1)::> > > \n> > ]",
        "[para(3,7):\n  ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_skip_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> > > list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n> ]",
        "[para(1,7):\n    ]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > > list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[block-quote(3,1)::> > > \n> ]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > > list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,1)::> > > \n> ]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> > > list
  >   item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n  > ]",
        "[para(1,7):\n  ]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > > list
  >   item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[block-quote(3,1)::> > > \n  > ]",
        "[para(3,7):\n  ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > > list
  >   item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,1)::> > > \n  > ]",
        "[para(3,7):\n  ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_skip_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> > > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n]",
        "[para(1,7):\n      ]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[block-quote(3,1)::> > > \n]",
        "[para(3,7):\n      ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_block_skip():
    """
    Verify that a nesting of block quote, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > > list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,1)::> > > \n]",
        "[para(3,7):\n      ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    >    > list
   >    >    > list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    > \n   >    >    > ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nlist::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
list</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_empty():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   >    >    >
   >    >    > list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    >\n   >    >    > ]",
        "[BLANK(1,15):]",
        "[para(2,16):]",
        "[text(2,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    > list
        >    > list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    > \n]",
        "[para(1,16):\n        ]",
        "[text(1,16):list\n\a>\a&gt;\a    \a>\a&gt;\a list::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
&gt;    &gt; list</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_empty_no_bq1():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    >
        >    > list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a    \a>\a&gt;\a list:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</blockquote>
<pre><code>    &gt;    &gt; list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    > list
   >         > list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    > \n   > ]",
        "[para(1,16):\n        ]",
        "[text(1,16):list\n\a>\a&gt;\a list::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
&gt; list</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_empty_no_bq2():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    >
   >         > list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):\a>\a&gt;\a list:    ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>    &gt; list
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    > list
             > list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    > \n]",
        "[para(1,16):\n             ]",
        "[text(1,16):list\n\a>\a&gt;\a list::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
&gt; list</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_empty_no_bq3():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    >
             > list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a list:         ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</blockquote>
<pre><code>         &gt; list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_no_bq4():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    > list
   >    >      list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    > \n   >    > ]",
        "[para(1,16):\n     ]",
        "[text(1,16):list\nlist::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
list</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_empty_no_bq4():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    >
   >    >      list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[block-quote(1,14)::   >    >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[icode-block(2,15):    :]",
        "[text(2,15):list: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
</blockquote>
<pre><code> list
</code></pre>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_no_bq5():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    > list
        >      list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    > \n]",
        "[para(1,16):\n        ]",
        "[text(1,16):list\n\a>\a&gt;\a      list::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
&gt;      list</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_empty_no_bq5():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    >
        >      list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a      list:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</blockquote>
<pre><code>    &gt;      list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_no_bq6():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    > list
   >           list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    > \n   > ]",
        "[para(1,16):\n          ]",
        "[text(1,16):list\nlist::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
list</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_empty_no_bq6():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    >
   >           list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):list:      ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>      list
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_no_bq7():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    > list
               list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    > \n]",
        "[para(1,16):\n               ]",
        "[text(1,16):list\nlist::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>list
list</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_empty_no_bq7():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    >
               list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[block-quote(1,14)::   >    >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):list:           ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</blockquote>
<pre><code>           list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_block_max():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    >    >    > list
    >    >    > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    \a>\a&gt;\a list\n\a>\a&gt;\a    \a>\a&gt;\a    \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    &gt; list
&gt;    &gt;    &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_block_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    > list
         >    > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    \a>\a&gt;\a list\n     \a>\a&gt;\a    \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    &gt; list
     &gt;    &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_block_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    > list
    >         > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    \a>\a&gt;\a list\n\a>\a&gt;\a         \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    &gt; list
&gt;         &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_block_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    > list
              > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    \a>\a&gt;\a list\n          \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    &gt; list
          &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_block_max_no_bq4():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    > list
    >    >      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    \a>\a&gt;\a list\n\a>\a&gt;\a    \a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    &gt; list
&gt;    &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_block_max_no_bq5():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    > list
         >      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    \a>\a&gt;\a list\n     \a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    &gt; list
     &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_block_max_no_bq6():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    > list
    >           item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    \a>\a&gt;\a list\n\a>\a&gt;\a           item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    &gt; list
&gt;           item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_block_max_no_bq7():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    > list
                item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    \a>\a&gt;\a list\n            item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    &gt; list
            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_block_max():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    > list
   >     >    > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list\n\a>\a&gt;\a    \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    &gt; list
&gt;    &gt; item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_block_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    > list
         >    > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a    \a>\a&gt;\a item:     ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    &gt; list
</code></pre>
</blockquote>
<pre><code>     &gt;    &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_block_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    > list
   >          > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list\n     \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    &gt; list
     &gt; item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_block_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    > list
              > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a item:          ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    &gt; list
</code></pre>
</blockquote>
<pre><code>          &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_block_max_no_bq4():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    > list
   >     >      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list\n\a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    &gt; list
&gt;      item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_block_max_no_bq5():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    > list
         >      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a      item:     ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    &gt; list
</code></pre>
</blockquote>
<pre><code>     &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_block_max_no_bq6():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    > list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list\n       item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    &gt; list
       item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_block_max_no_bq7():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    > list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    &gt; list
</code></pre>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_plus_one():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >     > list
   >    >     > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):\a>\a&gt;\a list\n\a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>&gt; list
&gt; item
</code></pre>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_plus_one_no_bq1():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     > list
        >     > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):\a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a     \a>\a&gt;\a item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
</blockquote>
<pre><code>    &gt;     &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_plus_one_no_bq2():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     > list
   >          > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):\a>\a&gt;\a item:     ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
<pre><code>     &gt; item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_plus_one_no_bq3():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     > list
              > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):\a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a item:          ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
</blockquote>
<pre><code>          &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_plus_one_no_bq4():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     > list
   >    >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):\a>\a&gt;\a list\n  item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>&gt; list
  item
</code></pre>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_plus_one_no_bq5():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     > list
        >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):\a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a       item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
</blockquote>
<pre><code>    &gt;       item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_plus_one_no_bq6():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     > list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:       ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
<pre><code>       item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_block_max_plus_one_no_bq7():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     > list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):\a>\a&gt;\a list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
