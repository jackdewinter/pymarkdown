"""
Extra tests for three level nesting with un/or.
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_unordered_block_unordered():
    """
    Verify that a nesting of unordered list, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ > + list
  >   item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[block-quote(1,3):  :  > \n  > ]",
        "[ulist(1,5):+::6::  ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_nl_unordered():
    """
    Verify that a nesting of unordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
  > + list
  >   item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >\n  > \n  > ]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6::  ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_nl_unordered_wo_bq():
    """
    Verify that a nesting of unordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
    + list
  >   item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6:    ]",
        "[para(3,7):]",
        "[text(3,7):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,3):  :  > ]",
        "[para(4,7):  ]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
</blockquote>
<ul>
<li>list</li>
</ul>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_text_nl_unordered():
    """
    Verify that a nesting of unordered list, text, new line, block quote, text, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
  > + list
  >   item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6::  ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_text_nl_unordered_wo_bq():
    """
    Verify that a nesting of unordered list, text, new line, block quote, text, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
    + list
  >   item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6:    ]",
        "[para(3,7):]",
        "[text(3,7):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,3):  :  > ]",
        "[para(4,7):  ]",
        "[text(4,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list</li>
</ul>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_skip_unordered():
    """
    Verify that a nesting of unordered list, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ > + list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[block-quote(1,3):  :  > \n]",
        "[ulist(1,5):+::6::      \n]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_skip_nl_unordered():
    """
    Verify that a nesting of unordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
    + list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6:    :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_skip_nl_unordered_wo_bq():
    """
    Verify that a nesting of unordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
    + list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6:    :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_skip_text_nl_unordered():
    """
    Verify that a nesting of unordered list, text, new line, block quote, text, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
    + list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6:    :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_skip_text_nl_unordered_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
    + list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(3,5):+::6:    :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered():
    """
    Verify that a nesting of unordered list, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ > 1. list
  >    item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[block-quote(1,3):  :  > \n  > ]",
        "[olist(1,5):.:1:7::   ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_nl_ordered():
    """
    Verify that a nesting of unordered list, new line, block quote, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
  > 1. list
  >    item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >\n  > \n  > ]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7::   ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_nl_ordered_wo_bq():
    """
    Verify that a nesting of unordered list, new line, block quote, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
    1. list
  >    item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:    ]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,3):  :  > ]",
        "[para(4,8):   ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
</blockquote>
<ol>
<li>list</li>
</ol>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_text_nl_ordered():
    """
    Verify that a nesting of unordered list, text, new line, block quote, text, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
  > 1. list
  >    item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7::   ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_text_nl_ordered_wo_bq():
    """
    Verify that a nesting of unordered list, text, new line, block quote, text, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
    1. list
  >    item"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:    ]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,3):  :  > ]",
        "[para(4,8):   ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list</li>
</ol>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_skip_ordered():
    """
    Verify that a nesting of unordered list, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ > 1. list
       item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[block-quote(1,3):  :  > \n]",
        "[olist(1,5):.:1:7::       \n]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_skip_nl_ordered():
    """
    Verify that a nesting of unordered list, new line, block quote, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
    1. list
       item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:    :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_nl_block_skip_nl_ordered_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  >
    1. list
       item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[BLANK(1,2):]",
        "[block-quote(2,3):  :  >]",
        "[BLANK(2,4):]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:    :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_skip_text_nl_ordered():
    """
    Verify that a nesting of unordered list, text, new line, block quote, text, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
    1. list
       item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:    :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_text_nl_block_skip_text_nl_ordered_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  > def
    1. list
       item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,5):.:1:7:    :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[block-quote(1,5):  :  > > \n\n]",
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
        "[block-quote(3,3):  :  > > \n\n]",
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
        "[block-quote(2,3):  :  > \n    > \n\n]",
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
        "[block-quote(3,3):  :  > > \n\n]",
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
        "[block-quote(2,3):  :  > \n    > \n\n]",
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
