"""
Extra tests for three level nesting with un/or.
"""
from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_unordered_block_block_x():
    """
    Verify that a nesting of unordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ > > list
  > > item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[block-quote(1,3):  :]",
        "[block-quote(1,5):  :  > > \n  > > ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_nl_block_x():
    """
    Verify that a nesting of unordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
  > > list
  > > item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >]",
        "[BLANK(2,4):]",
        "[block-quote(3,3):  :  > > \n  > > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_nl_block_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
    > list
  > > item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >\n    > ]",
        "[BLANK(2,4):]",
        "[para(3,7):]",
        "[text(3,7):list:]",
        "[end-para:::True]",
        "[block-quote(4,3):  :  > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<p>list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_text_nl_block_x():
    """
    Verify that a nesting of unordered list, text, new line, block quote, text, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
  > > list
  > > item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,3):  :  > > \n  > > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_text_nl_block_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
    > list
  > > item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n    > ]",
        "[para(2,5):\n]",
        "[text(2,5):def\nlist::\n]",
        "[end-para:::True]",
        "[block-quote(4,3):  :  > > ]",
        "[para(4,7):]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def
list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_skip_block_x():
    """
    Verify that a nesting of unordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ > > list
    > item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[block-quote(1,3):  :]",
        "[block-quote(1,5):  :  > > \n    > ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_skip_nl_block_x():
    """
    Verify that a nesting of unordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
  > > list
    > item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >]",
        "[BLANK(2,4):]",
        "[block-quote(3,3):  :  > > \n    > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_skip_nl_block_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
    > list
    > item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >\n    > \n    > ]",
        "[BLANK(2,4):]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_skip_text_nl_block_x():
    """
    Verify that a nesting of unordered list, text, new line, block quote, text, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
  > > list
    > item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,3):  :  > > \n    > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_skip_text_nl_block_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
    > list
    > item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n    > \n    > ]",
        "[para(2,5):\n\n]",
        "[text(2,5):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_block_skip():
    """
    Verify that a nesting of unordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ > > list
  >   item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[block-quote(1,3):  :]",
        "[block-quote(1,5):  :  > > \n  > ]",
        "[para(1,7):\n  ]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_nl_block_skip():
    """
    Verify that a nesting of unordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
  > > list
  >   item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >]",
        "[BLANK(2,4):]",
        "[block-quote(3,3):  :  > > \n  > ]",
        "[para(3,7):\n  ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_nl_block_skip_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
    > list
  >   item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >\n    > \n  > ]",
        "[BLANK(2,4):]",
        "[para(3,7):\n  ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_text_nl_block_skip():
    """
    Verify that a nesting of unordered list, text, new line, block quote, text, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
  > > list
  >   item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,3):  :  > > \n  > ]",
        "[para(3,7):\n  ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_text_nl_block_skip_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
    > list
  >   item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n    > \n  > ]",
        "[para(2,5):\n\n  ]",
        "[text(2,5):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_skip_block_skip():
    """
    Verify that a nesting of unordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ > > list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n]",
        "[block-quote(1,3):  :]",
        "[block-quote(1,5):  :  > > \n]",
        "[para(1,7):\n    ]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_skip_nl_block_skip():
    """
    Verify that a nesting of unordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
  > > list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n  \n]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >]",
        "[BLANK(2,4):]",
        "[block-quote(3,3):  :  > > \n]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_skip_nl_block_skip_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
    > list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n  \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n    > \n]",
        "[para(2,5):\n\n    ]",
        "[text(2,5):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_skip_text_nl_block_skip():
    """
    Verify that a nesting of unordered list, text, new line, block quote, text, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
  > > list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n  \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,3):  :  > > \n]",
        "[para(3,7):\n    ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_skip_text_nl_block_skip_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
    > list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n  \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n    > \n]",
        "[para(2,5):\n\n    ]",
        "[text(2,5):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    >    > list
        >    > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    > \n        >    > ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_with_li():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    > list
   +    >    > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[block-quote(2,14)::        >    > ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list</p>
</blockquote>
</blockquote>
</li>
<li>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_empty():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   +    >    >
        >    > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    >\n        >    > ]",
        "[BLANK(1,15):]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_empty_with_li():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    >
   +    >    > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[block-quote(2,14)::        >    > ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</li>
<li>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_no_bq1():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    > list
             > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        \n]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    > \n]",
        "[para(1,16):\n     ]",
        "[text(1,16):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_no_bq1_with_li():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    > list
   +    >    > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[block-quote(2,14)::        >    > ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list</p>
</blockquote>
</blockquote>
</li>
<li>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_empty_no_bq1():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    >
             > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        ]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,13):    :]",
        "[text(2,13):\a>\a&gt;\a item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code> &gt; item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_empty_no_bq1_with_li():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    >
   +    >    > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[block-quote(2,14)::        >    > ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</li>
<li>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_no_bq2():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    > list
        >      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    > \n        > ]",
        "[para(1,16):\n     ]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_no_bq2_with_li():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    > list
   +    >      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list</p>
</blockquote>
</blockquote>
</li>
<li>
<blockquote>
<pre><code> item
</code></pre>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_empty_no_bq2():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    >
        >      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > \n        > ]",
        "[block-quote(1,14)::        >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
</blockquote>
<pre><code> item
</code></pre>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_empty_no_bq2_with_li():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    >
   +    >      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</li>
<li>
<blockquote>
<pre><code> item
</code></pre>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_no_bq3():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    > list
               item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        \n]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    > \n]",
        "[para(1,16):\n       ]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_no_bq3_with_li():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    > list
   +           item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:      ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>list</p>
</blockquote>
</blockquote>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_empty_no_bq3():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    >
               item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        ]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,13):    :]",
        "[text(2,13):item:   ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>   item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_empty_no_bq3_with_li():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    >
   +           item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[block-quote(1,14)::        >    >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:      ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_block_max_block_max():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    +    >    > list
    +    >    > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    \a>\a&gt;\a    \a>\a&gt;\a list\n+    \a>\a&gt;\a    \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    &gt;    &gt; list
+    &gt;    &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_block_max_block_max_no_bq1():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    +    >    > list
              > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    \a>\a&gt;\a    \a>\a&gt;\a list\n          \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    &gt;    &gt; list
          &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_block_max_block_max_no_bq2():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    +    >    > list
    +    >      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    \a>\a&gt;\a    \a>\a&gt;\a list\n+    \a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    &gt;    &gt; list
+    &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_block_max_block_max_no_bq3():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    +    >    > list
    +           item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    \a>\a&gt;\a    \a>\a&gt;\a list\n+           item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    &gt;    &gt; list
+           item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_plus_one_block_max():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +     >    > list
   +     >    > item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):\a>\a&gt;\a    \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>&gt;    &gt; list
</code></pre>
</li>
<li>
<pre><code>&gt;    &gt; item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_plus_one_block_max_no_bq1():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +     >    > list
              > item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   :     ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list\n     \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>&gt;    &gt; list
     &gt; item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_plus_one_block_max_no_bq2():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +     >    > list
   +     >      item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):\a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>&gt;    &gt; list
</code></pre>
</li>
<li>
<pre><code>&gt;      item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_plus_one_block_max_no_bq3():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +     >    > list
   +            item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    \a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:       ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>&gt;    &gt; list
</code></pre>
</li>
<li>
<pre><code>       item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_plus_one_x():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    >     > list
        >     > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > \n        > \n]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):\a>\a&gt;\a list\n\a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<pre><code>&gt; list
&gt; item
</code></pre>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_plus_one_no_bq1():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >     > list
              > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        ]",
        "[block-quote(1,9):        :        > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,13):    :]",
        "[text(2,13):\a>\a&gt;\a item:  ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
<pre><code>  &gt; item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_plus_one_no_bq2():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >     > list
        >       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > \n        > ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):\a>\a&gt;\a list\n  item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<pre><code>&gt; list
  item
</code></pre>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_block_max_plus_one_no_bq3():
    """
    Verify that a nesting of unordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >     > list
                item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        ]",
        "[block-quote(1,9):        :        > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,13):    :]",
        "[text(2,13):item:    ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
<pre><code>    item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
