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


@pytest.mark.gfm
def test_nested_three_block_block_block_nl_extra_block_drop_block_thematics_around_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new block quote, drop that block, and thematics around a fenced.

    was: test_extra_044ma
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_with_thematics
    """
    # Arrange
    source_markdown = """> > >
> > > > fourth block 1
> > > > fourth block 2
> > > --------
> > > ```block
> > > A code block
> > > ```
> > > --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >\n> > > \n> > > \n> > > \n> > > \n]",
        "[BLANK(1,6):]",
        "[block-quote(2,1)::> > > > \n> > > > \n> > > ]",
        "[para(2,9):\n]",
        "[text(2,9):fourth block 1\nfourth block 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > > :True]",
        "[tbreak(4,7):-::--------]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<blockquote>
<p>fourth block 1
fourth block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_block_nl_extra_list_li_drop_list_thematics_around_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new list, a list item, drop that list, and thematics around a fenced.

    was: test_extra_044mcy0
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_list_with_thematics
    """
    # Arrange
    source_markdown = """> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > > --------
> > > ```block
> > > A code block
> > > ```
> > > --------"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >\n> > > \n> > > \n> > > \n> > > \n> > > \n> > > \n> > > \n> > > ]",
        "[BLANK(1,6):]",
        "[ulist(2,7):+::8::  \n]",
        "[para(2,9):\n]",
        "[text(2,9):inner list 1\ninner list 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):inner list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):-::--------]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<ul>
<li>inner list 1
inner list 2</li>
<li>inner list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_block_nl_extra_list_li_drop_list_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new list, a list item, drop that list, and thematics around blanks around a fenced.

    was: test_extra_044mcy1
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_list_with_thematics
    """
    # Arrange
    source_markdown = """> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > > --------
> > >
> > > ```block
> > > A code block
> > > ```
> > >
> > > --------"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >\n> > > \n> > > \n> > > \n> > > \n> > >\n> > > \n> > > \n> > > \n> > >\n> > > ]",
        "[BLANK(1,6):]",
        "[ulist(2,7):+::8::  \n]",
        "[para(2,9):\n]",
        "[text(2,9):inner list 1\ninner list 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):inner list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):-::--------]",
        "[BLANK(6,6):]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,6):]",
        "[tbreak(11,7):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<ul>
<li>inner list 1
inner list 2</li>
<li>inner list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_nl_block_drop_double_block_with_setext_then_thematics_around_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new list, a list item, drop that list, and thematics around blanks around a fenced.

    was: test_extra_047f3
    refs: bad_fenced_block_in_block_quote_with_previous_inner_blocks_with_setext
    """
    # Arrange
    source_markdown = """> > inner block
> > > innermost block
> > > innermost block
> > inner block
>
> This is text and no blank line.
> ---
> ```block
> A code block
> ```
> ---
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n>\n]",
        "[block-quote(1,3)::> > ]",
        "[para(1,5):]",
        "[text(1,5):inner block:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > > \n> > > \n> > \n>]",
        "[para(2,7):\n\n]",
        "[text(2,7):innermost block\ninnermost block\ninner block::\n\n]",
        "[end-para:::True]",
        "[BLANK(5,2):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[setext(7,3):-:3::(6,3)]",
        "[text(6,3):This is text and no blank line.:]",
        "[end-setext::]",
        "[fcode-block(8,3):`:3:block:::::]",
        "[text(9,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(11,3):-::---]",
        "[para(12,2):]",
        "[text(12,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(13,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block</p>
<blockquote>
<p>innermost block
innermost block
inner block</p>
</blockquote>
</blockquote>
<h2>This is text and no blank line.</h2>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_nl_block_drop_block_with_thematic_then_text_then_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new list, a list item, drop that list, and thematics around blanks around a fenced.

    was: test_extra_047f6x
    refs: bad_fenced_block_in_block_quote_with_previous_inner_blocks
    """
    # Arrange
    source_markdown = """> > inner block
> > > innermost block
> > > innermost block
> > _____
> > inner block
> ```block
> A code block
> ```
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n]",
        "[block-quote(1,3)::> > \n> > \n> ]",
        "[para(1,5):]",
        "[text(1,5):inner block:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > > \n> > > \n> > ]",
        "[para(2,7):\n]",
        "[text(2,7):innermost block\ninnermost block::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[tbreak(4,5):_::_____]",
        "[para(5,5):]",
        "[text(5,5):inner block:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[para(9,2):]",
        "[text(9,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block</p>
<blockquote>
<p>innermost block
innermost block</p>
</blockquote>
<hr />
<p>inner block</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_nl_block_drop_block_with_thematic_then_text_then_blanks_aroundfenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new list, a list item, drop that list, and thematics around blanks around a fenced.

    was: test_extra_047f6d
    refs: bad_fenced_block_in_block_quote_with_previous_inner_blocks
    """
    # Arrange
    source_markdown = """> > inner block
> > > innermost block
> > > innermost block
> > _____
> > inner block
>
> ```block
> A code block
> ```
>
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n>\n]",
        "[block-quote(1,3)::> > \n> > \n>]",
        "[para(1,5):]",
        "[text(1,5):inner block:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > > \n> > > \n> > ]",
        "[para(2,7):\n]",
        "[text(2,7):innermost block\ninnermost block::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[tbreak(4,5):_::_____]",
        "[para(5,5):]",
        "[text(5,5):inner block:]",
        "[end-para:::True]",
        "[BLANK(6,2):]",
        "[end-block-quote:::True]",
        "[fcode-block(7,3):`:3:block:::::]",
        "[text(8,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,2):]",
        "[para(11,2):]",
        "[text(11,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block</p>
<blockquote>
<p>innermost block
innermost block</p>
</blockquote>
<hr />
<p>inner block</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_nl_block_drop_block_with_text_then_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new list, a list item, drop that list, and thematics around blanks around a fenced.

    was: test_extra_047f6a
    """
    # Arrange
    source_markdown = """> > inner block
> > > innermost block
> > > innermost block
> > inner block
> > ```block
> > A code block
> > ```
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::>\n]",
        "[block-quote(1,3)::> > \n> > \n> > ]",
        "[para(1,5):]",
        "[text(1,5):inner block:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > > \n> > > \n> > \n> > ]",
        "[para(2,7):\n\n]",
        "[text(2,7):innermost block\ninnermost block\ninner block::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
        "[para(8,2):]",
        "[text(8,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block</p>
<blockquote>
<p>innermost block
innermost block
inner block</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
</blockquote>
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_nl_block_drop_block_with_thematics_around_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new list, a list item, drop that list, and thematics around blanks around a fenced.

    was: test_extra_047f6b
    refs: bad_fenced_block_in_block_quote_with_previous_inner_blocks_with_thematics
    """
    # Arrange
    source_markdown = """> > inner block
> > > innermost block
> > > innermost block
> > inner block
> ___
> ```block
> A code block
> ```
> ___
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n]",
        "[block-quote(1,3)::> > ]",
        "[para(1,5):]",
        "[text(1,5):inner block:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > > \n> > > \n> > \n> ]",
        "[para(2,7):\n\n]",
        "[text(2,7):innermost block\ninnermost block\ninner block::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-block-quote:::True]",
        "[tbreak(5,3):_::___]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,3):_::___]",
        "[para(10,2):]",
        "[text(10,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block</p>
<blockquote>
<p>innermost block
innermost block
inner block</p>
</blockquote>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_nl_block_drop_block_with_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new list, a list item, drop that list, and thematics around blanks around a fenced.

    was: test_extra_047f6c
    refs: bad_fenced_block_in_block_quote_with_previous_inner_blocks_with_thematics
    """
    # Arrange
    source_markdown = """> > inner block
> > > innermost block
> > > innermost block
> > inner block
> ___
>
> ```block
> A code block
> ```
>
> ___
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n> \n>\n> \n>\n]",
        "[block-quote(1,3)::> > ]",
        "[para(1,5):]",
        "[text(1,5):inner block:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > > \n> > > \n> > \n> ]",
        "[para(2,7):\n\n]",
        "[text(2,7):innermost block\ninnermost block\ninner block::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-block-quote:::True]",
        "[tbreak(5,3):_::___]",
        "[BLANK(6,2):]",
        "[fcode-block(7,3):`:3:block:::::]",
        "[text(8,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,2):]",
        "[tbreak(11,3):_::___]",
        "[para(12,2):]",
        "[text(12,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(13,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block</p>
<blockquote>
<p>innermost block
innermost block
inner block</p>
</blockquote>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_block_drop_block_thematics_around_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new block quote, drop that block, and thematics around a fenced.

    was: test_extra_044x
    refs: bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_block_with_thematics
    """
    # Arrange
    source_markdown = """> > > block 3
> > > block 3
> > > block 3
> > --------
> > ```block
> > A code block
> > ```
> > --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n]",
        "[block-quote(1,5)::> > > \n> > > \n> > > \n> > ]",
        "[para(1,7):\n\n]",
        "[text(1,7):block 3\nblock 3\nblock 3::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[tbreak(4,5):-::--------]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>block 3
block 3
block 3</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_block_drop_block_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new block quote, drop that block, and thematics around a fenced.

    was: test_extra_044a
    refs: bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_block_with_thematics
    """
    # Arrange
    source_markdown = """> > > block 3
> > > block 3
> > > block 3
> > --------
> >
> > ```block
> > A code block
> > ```
> >
> > --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> >\n> > \n> > \n> > \n> >\n> > \n]",
        "[block-quote(1,5)::> > > \n> > > \n> > > \n> > ]",
        "[para(1,7):\n\n]",
        "[text(1,7):block 3\nblock 3\nblock 3::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[tbreak(4,5):-::--------]",
        "[BLANK(5,4):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,4):]",
        "[tbreak(10,5):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>block 3
block 3
block 3</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_block_thematics_around_text_and_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new block quote, drop that block, and thematics around a fenced.

    was: test_extra_044gx
    """
    # Arrange
    source_markdown = """> > > -----
> > > abc
> > > ```block
> > > A code block
> > > ```
> > > -----
> > another list
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[block-quote(1,5)::> > > \n> > > \n> > > \n> > > \n> > > \n> > > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::False]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(6,7):-::-----]",
        "[end-block-quote:::True]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<hr />
<p>abc</p>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
<p>another list</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_block_thematics_around_text_and_blanks_around_fenced():
    """
    Verify that a nesting of block quote, block quote, block quote, with
    a new block quote, drop that block, and thematics around a fenced.

    was: test_extra_044ga
    """
    # Arrange
    source_markdown = """> > > -----
> > > abc
> > > 
> > > ```block
> > > A code block
> > > ```
> > > 
> > > -----
> > another list
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[block-quote(1,5)::> > > \n> > > \n> > > \n> > > \n> > > \n> > > \n> > > \n> > > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[BLANK(3,7):]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(7,7):]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<hr />
<p>abc</p>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
<p>another list</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
