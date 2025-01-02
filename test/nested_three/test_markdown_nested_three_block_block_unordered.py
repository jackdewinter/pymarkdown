"""
Extra tests.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_block_block_unordered():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > + list
> >   item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > ]",
        "[ulist(1,5):+::6::  ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_unordered():
    """
    Verify that a nesting of block quote, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > + list
> >   item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n> > ]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6::  ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > + list
> >   item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6:]",
        "[para(3,7):]",
        "[text(3,7):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,7):  ]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ul>
<li>list</li>
</ul>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   + list
> >   item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6:  ]",
        "[para(3,7):]",
        "[text(3,7):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,7):  ]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ul>
<li>list</li>
</ul>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    + list
> >   item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):+ list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::]",
        "[block-quote(4,3)::> > ]",
        "[para(4,7):  ]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>+ list
</code></pre>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_unordered():
    """
    Verify that a nesting of block quote, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > + list
> >   item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6::  ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > + list
> >   item"""
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
        "[ulist(3,5):+::6:]",
        "[para(3,7):]",
        "[text(3,7):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,7):  ]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list</li>
</ul>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   + list
> >   item"""
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
        "[ulist(3,5):+::6:  ]",
        "[para(3,7):]",
        "[text(3,7):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,1)::> > ]",
        "[para(4,7):  ]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list</li>
</ul>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_text_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    + list
> >   item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n> > ]",
        "[para(2,5):\n    \n  ]",
        "[text(2,5):def\n+ list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
+ list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_unordered():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > + list
  >   item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n  > ]",
        "[ulist(1,5):+::6::  ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_unordered():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > + list
  >   item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n  > ]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6::  ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > + list
  >   item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n  > ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6::  ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   + list
  >   item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n  > ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6:  :  ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    + list
  >   item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):+ list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,3):  :  > ]",
        "[para(4,7):  ]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>+ list
</code></pre>
<blockquote>
<p>item</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_unordered():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > + list
  >   item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6::  ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > + list
  >   item"""
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
        "[ulist(3,5):+::6::  ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   + list
  >   item"""
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
        "[ulist(3,5):+::6:  :  ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_text_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    + list
  >   item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n  > ]",
        "[para(2,5):\n    \n  ]",
        "[text(2,5):def\n+ list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
+ list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_skip_unordered():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> ]",
        "[ulist(1,5):+::6::    ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_unordered():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n> ]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6::    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6::    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6:  :    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_block_skip_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
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
<blockquote>
</blockquote>
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
def test_nested_three_block_text_nl_block_skip_text_nl_unordered():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6::    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > + list
>     item"""
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
        "[ulist(3,5):+::6::    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   + list
>     item"""
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
        "[ulist(3,5):+::6:  :    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_block_skip_text_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n> ]",
        "[para(2,5):\n    \n    ]",
        "[text(2,5):def\n+ list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
+ list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_block_skip_unordered():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> > + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[ulist(1,5):+::6::      ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_unordered():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
> > + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >\n> > \n]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6::      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
  > + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n  > \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6::      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_block_skip_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> >
    + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):+ list\n  item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>+ list
  item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_unordered():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
> > + list
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
        "[ulist(3,5):+::6::      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
  > + list
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
        "[ulist(3,5):+::6::      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   + list
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
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_block_skip_text_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> > def
    + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n    \n      ]",
        "[text(2,5):def\n+ list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
+ list
item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    + list
   >    >      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[ulist(1,14):+::15:   :     ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_with_li():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces allowed works properly, with a new list item.
    """

    # Arrange
    source_markdown = """   >    >    + list
   >    >    + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[ulist(1,14):+::15:   ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[li(2,14):15:   :]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list</li>
<li>item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_empty():
    """
    Verify that a nesting of block quote, block quote, unordered list,
    and no text on the first line, with the maximum number of spaces
    allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    +
   >    >      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[ulist(1,14):+::15:   :     ]",
        "[BLANK(1,15):]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_empty_with_li():
    """
    Verify that a nesting of block quote, block quote, unordered list,
    and no text on the first line, with the maximum number of spaces
    allowed works properly, with a new list item.
    """

    # Arrange
    source_markdown = """   >    >    +
   >    >    + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[li(2,14):15:   :]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li></li>
<li>item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    + list
        >      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[ulist(1,14):+::15:   :        ]",
        "[para(1,16):\n]",
        "[text(1,16):list\n\a>\a&gt;\a      item::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
&gt;      item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_no_bq1_with_li():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a new list item.
    """

    # Arrange
    source_markdown = """   >    >    + list
        >    + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[ulist(1,14):+::15:   :        ]",
        "[para(1,16):\n]",
        "[text(1,16):list\n\a>\a&gt;\a    + item::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
&gt;    + item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_empty_no_bq1():
    """
    Verify that a nesting of block quote, block quote, unordered list,
    and no text on the first line, with the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    +
        >      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a      item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</blockquote>
<pre><code>    &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_empty_no_bq1_with_li():
    """
    Verify that a nesting of block quote, block quote, unordered list,
    and no text on the first line, with the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a new list item.
    """

    # Arrange
    source_markdown = """   >    >    +
        >    + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a    + item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</blockquote>
<pre><code>    &gt;    + item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    + list
   >           item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > ]",
        "[ulist(1,14):+::15:   :          ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_no_bq2_with_li():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a new list item.
    """

    # Arrange
    source_markdown = """   >    >    + list
   >         + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > ]",
        "[ulist(1,14):+::15:   :        ]",
        "[para(1,16):\n]",
        "[text(1,16):list\n+ item::\n]",  # text should be split
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
+ item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
    # assert False


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_empty_no_bq2():
    """
    Verify that a nesting of block quote, block quote, unordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    +
   >           item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:      ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>      item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_empty_no_bq2_with_li():
    """
    Verify that a nesting of block quote, block quote, unordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a new list item.
    """

    # Arrange
    source_markdown = """   >    >    +
   >         + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):+ item:    ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>    + item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    + list
               item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[ulist(1,14):+::15:   :               ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_no_bq3_with_li():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a new list item.
    """

    # Arrange
    source_markdown = """   >    >    + list
             + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[ulist(1,14):+::15:   :             ]",
        "[para(1,16):\n]",
        "[text(1,16):list\n+ item::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>list
+ item</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_empty_no_bq3():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    +
               item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:           ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</blockquote>
<pre><code>           item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_empty_no_bq3_with_li():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a new list item.
    """

    # Arrange
    source_markdown = """   >    >    +
             + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):+ item:         ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</blockquote>
<pre><code>         + item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_unordered_max():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly.
    """

    # Arrange
    source_markdown = """    >    >    + list
    >    >      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    + list\n\a>\a&gt;\a    \a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    + list
&gt;    &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    + list
         >      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    + list\n     \a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    + list
     &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_unordered_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    + list
    >           item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    + list\n\a>\a&gt;\a           item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    + list
&gt;           item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_unordered_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    + list
                item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    + list\n            item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    + list
            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_unordered_max():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    + list
   >     >      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    + list\n\a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    + list
&gt;      item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    + list
         >      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    + list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a      item:     ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    + list
</code></pre>
</blockquote>
<pre><code>     &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_unordered_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    + list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    + list\n       item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    + list
       item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_unordered_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    + list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    + list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    + list
</code></pre>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_plus_one():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >     + list
   >    >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):+ list\n  item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>+ list
  item
</code></pre>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_plus_one_with_li():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with list item.
    """

    # Arrange
    source_markdown = """   >    >     + list
   >    >     + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):+ list\n+ item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>+ list
+ item
</code></pre>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_plus_one_no_bq1():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     + list
        >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):+ list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a       item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>+ list
</code></pre>
</blockquote>
</blockquote>
<pre><code>    &gt;       item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_plus_one_no_bq2():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     + list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):+ list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:       ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>+ list
</code></pre>
</blockquote>
<pre><code>       item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_unordered_max_plus_one_no_bq3():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     + list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):+ list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>+ list
</code></pre>
</blockquote>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_drop_list_after_new_list_and_text_with_thematic_and_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lx
    refs: bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_list_with_thematics
    """

    # Arrange
    source_markdown = """> > + block 3
> >   block 3
> > + block 3
> > --------
> > ```block
> > A code block
> > ```
> > --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
        "[ulist(1,5):+::6::  \n]",
        "[para(1,7):\n]",
        "[text(1,7):block 3\nblock 3::\n]",
        "[end-para:::True]",
        "[li(3,5):6::]",
        "[para(3,7):]",
        "[text(3,7):block 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
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
<ul>
<li>block 3
block 3</li>
<li>block 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_drop_list_after_new_list_and_text_with_thematic_and_fenced_with_blanks():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block surrounded by blanks.

    refs: bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_list_with_thematics
    """

    # Arrange
    source_markdown = """> > + block 3
> >   block 3
> > + block 3
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
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> >\n> > \n> > \n> > \n> >\n> > \n]",
        "[ulist(1,5):+::6::  \n]",
        "[para(1,7):\n]",
        "[text(1,7):block 3\nblock 3::\n]",
        "[end-para:::True]",
        "[li(3,5):6::]",
        "[para(3,7):]",
        "[text(3,7):block 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
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
<ul>
<li>block 3
block 3</li>
<li>block 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_nl_extra_block_drop_block_with_thematics_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044mcx0, test_extra_047e0, test_extra_047h0
    refs: bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_with_thematics
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >   --------
> >   ```block
> >   A code block
> >   ```
> >   --------"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::\n\n  þ\n  \n  \n  \n  ]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[tbreak(4,7):-::--------]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::--------]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
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
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_nl_extra_block_drop_block_with_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block surrounded by blanks.

    was: test_extra_044mcx1, test_extra_047h1
    refs: bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_with_thematics
    """
    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >   --------
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   --------"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> >\n> > \n> > \n> > \n> >\n> > ]",
        "[ulist(1,5):+::6::\n\n  þ\n\n  \n  \n  \n\n  ]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[tbreak(4,7):-::--------]",
        "[BLANK(5,4):]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,4):]",
        "[tbreak(10,7):-::--------]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
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
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_nl_extra_block_drop_block_with_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_046v0
    refs: bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block
    """
    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >   ```block
> >   A code block
> >   ```
> >   --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::\n\n  þ\n  \n  \n  ]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):-::--------]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
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
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_nl_extra_block_drop_block_with_blanks_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_046v1
    refs: bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block
    """
    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> >\n> > ]",
        "[ulist(1,5):+::6::\n\n\n  \n  \n  \n\n  ]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> >]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,4):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,4):]",
        "[tbreak(9,7):-::--------]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
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
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_nl_extra_list_li_drop_list_with_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_046u0
    refs: bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  ]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):_::______]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
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
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_nl_extra_list_li_drop_list_with_blanks_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_046u0
    refs: bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> >\n> > \n> > \n> > \n> >\n> > ]",
        "[ulist(1,5):+::6::  \n  \n\n  ]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n\n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,4):]",
        "[end-ulist:::True]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,4):]",
        "[tbreak(10,7):_::______]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
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
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_block_drop_block_blanks_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_045a
    """
    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >
> >  ```block
> >   A code block
> >   ```
> >
> >  --------
> >
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> >\n> > \n> >\n]",
        "[ulist(1,5):+::6::\n\n\n ]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> >]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,4):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,6):`:3:block:::: :]",
        "[text(6,5):A code block:\a \a\x03\a ]",
        "[end-fcode-block:  ::3:False]",
        "[BLANK(8,4):]",
        "[tbreak(9,6):-: :--------]",
        "[BLANK(10,4):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block"> A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_block_drop_block_blanks_with_trailing_space_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_045x
    """
    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >\a
> >  ```block
> >   A code block
> >   ```
> >\a
> >  --------
> >\a
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
        "[ulist(1,5):+::6::\n\n\n ]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,5):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,6):`:3:block:::: :]",
        "[text(6,5):A code block:\a \a\x03\a ]",
        "[end-fcode-block:  ::3:False]",
        "[BLANK(8,5):]",
        "[tbreak(9,6):-: :--------]",
        "[BLANK(10,5):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block"> A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_list_li_drop_list_thematics_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lex1
    refs: bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_and_thematics
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >   ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  \n  ]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):_::______]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):_::______]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
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
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_list_li_drop_list_thematics_around_blanks_and_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lex1a
    refs: bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_and_thematics
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >   ______
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> >\n> > \n> > \n> > \n> >\n> > ]",
        "[ulist(1,5):+::6::\n  \n  \n  \n\n  ]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):_::______]",
        "[BLANK(6,4):]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,4):]",
        "[tbreak(11,7):_::______]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
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
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_list_li_double_drop_with_single_indent_fenced_then_thematics():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lex2
    refs: bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_and_thematics
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >  ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
        "[ulist(1,5):+::6:]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[tbreak(5,6):_: :______]",
        "[fcode-block(6,7):`:3:block::::  :]",
        "[text(7,5):A code block:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[tbreak(9,7):_:  :______]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_list_li_double_drop_fenced_then_thematics_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lex3
    refs: bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_and_thematics
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> > ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
        "[ulist(1,5):+::6:]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[tbreak(5,5):_::______]",
        "[fcode-block(6,7):`:3:block::::  :]",
        "[text(7,5):A code block:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[tbreak(9,7):_:  :______]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_list_li_double_drop_fenced_then_headings_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lex3a
    refs: bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_and_thematics
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> > # head 1
> >   ```block
> >   A code block
> >   ```
> >   # head 2
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
        "[ulist(1,5):+::6:]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[atx(5,5):1:0:]",
        "[text(5,7):head 1: ]",
        "[end-atx::]",
        "[fcode-block(6,7):`:3:block::::  :]",
        "[text(7,5):A code block:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[atx(9,7):1:0:  ]",
        "[text(9,9):head 2: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
<h1>head 1</h1>
<pre><code class="language-block">A code block
</code></pre>
<h1>head 2</h1>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_list_li_double_drop_fenced_then_htmls_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lex3b
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> > <!-- html 1 -->
> >   ```block
> >   A code block
> >   ```
> >   <!-- html 2 -->
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
        "[ulist(1,5):+::6:]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[html-block(5,5)]",
        "[text(5,5):<!-- html 1 -->:]",
        "[end-html-block:::False]",
        "[fcode-block(6,7):`:3:block::::  :]",
        "[text(7,5):A code block:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[html-block(9,5)]",
        "[text(9,7):<!-- html 2 -->:  ]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
<!-- html 1 -->
<pre><code class="language-block">A code block
</code></pre>
  <!-- html 2 -->
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_list_li_thematics_first_with_single_indent_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lex4
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >    ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  \n  ]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n   ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,8):_: :______]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):_::______]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
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
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_list_li_thematics_first_with_double_indent_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lex5x
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >     ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  ]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n    \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[tbreak(5,9):_::______]",
        "[end-ulist:::True]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):_::______]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3
<hr />
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_list_thematics_first_with_double_indent_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lex5a
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >     ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  ]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n    \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::False]",
        "[tbreak(4,9):_::______]",
        "[end-ulist:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):_::______]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2
<hr />
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_extra_list_single_line_thematics_first_with_double_indent_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lex5b
    """
    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  ]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n  ]",
        "[para(2,9):]",
        "[text(2,9):list 1:]",
        "[end-para:::False]",
        "[tbreak(3,9):_::______]",
        "[end-ulist:::True]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):_::______]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
<hr />
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_block_unordered_thematics_around_fenced():
    """
    Verify that a nesting of block quote, block quote, unordered list, with
    a new list item, then dropping the list and continuing with a thematic block
    and a fenced code block.

    was: test_extra_044lex5c
    """
    # Arrange
    source_markdown = """> > + ______
> >     ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  \n  \n  ]",
        "[tbreak(1,7):_::______]",
        "[tbreak(2,9):_:  :______]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(6,7):_::______]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
