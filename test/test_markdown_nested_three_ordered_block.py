"""
Extra tests for three level nesting with un/or.
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_ordered_block_unordered():
    """
    Verify that a nesting of ordered list, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. > + list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,6):+::7::  ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_unordered():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > + list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n   > \n   > ]",
        "[BLANK(2,5):]",
        "[ulist(3,6):+::7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_unordered_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     + list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[end-block-quote:::True]",
        "[ulist(3,6):+::7:     ]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,4):   :   > ]",
        "[para(4,8):  ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_unordered():
    """
    Verify that a nesting of ordered list, text, new line, block quote, text, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > + list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n   > \n   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[ulist(3,6):+::7::  ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_unordered_wo_bq():
    """
    Verify that a nesting of ordered list, text, new line, block quote, text, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     + list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(3,6):+::7:     ]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,4):   :   > ]",
        "[para(4,8):  ]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_nested_three_ordered_block_skip_unordered():
    """
    Verify that a nesting of ordered list, block quote, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. > + list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n]",
        "[ulist(1,6):+::7::       \n]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_unordered():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > + list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n   > \n]",
        "[BLANK(2,5):]",
        "[ulist(3,6):+::7::       \n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_unordered_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     + list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[end-block-quote:::True]",
        "[ulist(3,6):+::7:     :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_unordered():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > + list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n   > \n]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[ulist(3,6):+::7::       \n]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_unordered_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     + list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(3,6):+::7:     :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
</blockquote>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_ordered():
    """
    Verify that a nesting of ordered list, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. > 1. list
   >    item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > ]",
        "[olist(1,6):.:1:8::   ]",
        "[para(1,9):\n]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_ordered():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > 1. list
   >    item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n   > \n   > ]",
        "[BLANK(2,5):]",
        "[olist(3,6):.:1:8::   ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_ordered_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     1. list
   >    item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[end-block-quote:::True]",
        "[olist(3,6):.:1:8:     ]",
        "[para(3,9):]",
        "[text(3,9):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,4):   :   > ]",
        "[para(4,9):   ]",
        "[text(4,9):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_ordered():
    """
    Verify that a nesting of ordered list, text, new line, block quote, text, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > 1. list
   >    item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n   > \n   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[olist(3,6):.:1:8::   ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_ordered_wo_bq():
    """
    Verify that a nesting of ordered list, text, new line, block quote, text, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     1. list
   >    item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,6):.:1:8:     ]",
        "[para(3,9):]",
        "[text(3,9):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(4,4):   :   > ]",
        "[para(4,9):   ]",
        "[text(4,9):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_skip_ordered():
    """
    Verify that a nesting of ordered list, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. > 1. list
        item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n]",
        "[olist(1,6):.:1:8::        \n]",
        "[para(1,9):\n]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_ordered():
    """
    Verify that a nesting of ordered list, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > 1. list
        item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n   > \n]",
        "[BLANK(2,5):]",
        "[olist(3,6):.:1:8::        \n]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_ordered_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     1. list
        item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[end-block-quote:::True]",
        "[olist(3,6):.:1:8:     :        ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_ordered():
    """
    Verify that a nesting of ordered list, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > 1. list
        item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n   > \n]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[olist(3,6):.:1:8::        \n]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_ordered_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     1. list
        item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[olist(3,6):.:1:8:     :        ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
</blockquote>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_x():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. > > list
   > > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_block_x():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > > list
   > > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[block-quote(3,4):   :   > > \n   > > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_block_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     > list
   > > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n     > ]",
        "[BLANK(2,5):]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[block-quote(4,4):   :   > > ]",
        "[para(4,8):]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_block_x():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > > list
   > > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,4):   :   > > \n   > > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_block_wo_bq():
    """
    Verify that a nesting of ordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     > list
   > > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n     > ]",
        "[para(2,6):\n]",
        "[text(2,6):def\nlist::\n]",
        "[end-para:::True]",
        "[block-quote(4,4):   :   > > ]",
        "[para(4,8):]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def
list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_skip_block_x():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. > > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n     > ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_block():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[block-quote(3,4):   :   > > \n     > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_block_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n     > \n     > ]",
        "[BLANK(2,5):]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_block():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,4):   :   > > \n     > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_block_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n     > \n     > ]",
        "[para(2,6):\n\n]",
        "[text(2,6):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_skip():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. > > list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > ]",
        "[para(1,8):\n  ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_block_skip():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > > list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[block-quote(3,4):   :   > > \n   > ]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_block_skip_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     > list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n     > \n   > ]",
        "[BLANK(2,5):]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_block_skip():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > > list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,4):   :   > > \n   > ]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_block_skip_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     > list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n     > \n   > ]",
        "[para(2,6):\n\n  ]",
        "[text(2,6):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_skip_block_skip():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. > > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n]",
        "[para(1,8):\n    ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_ordered_nl_block_skip_nl_block_skip():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n   \n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[block-quote(3,4):   :   > > \n]",
        "[para(3,8):\n    ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_block_skip_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n   \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n     > \n]",
        "[para(2,6):\n\n    ]",
        "[text(2,6):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_block_skip():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n   \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,4):   :   > > \n]",
        "[para(3,8):\n    ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_block_skip_wo_bq():
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n   \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n     > \n]",
        "[para(2,6):\n\n    ]",
        "[text(2,6):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    >    + list
         >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[ulist(1,15):+::16:   :     ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_empty():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   1.    >    +
         >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[ulist(1,15):+::16:   :     ]",
        "[BLANK(1,16):]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    + list
                item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n]",
        "[ulist(1,15):+::16:   :                \n]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_empty_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    +
                item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):item:   ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>   item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_unordered_max():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    1.    >    + list
          >      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    + list\n      \a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    + list
      &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_unordered_max_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    1.    >    + list
                 item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    + list\n             item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    + list
             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_unordered_max():
    """
    Verify that a nesting of ordered list, unordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.     >    + list
          >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    + list\n\a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    + list
&gt;      item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_unordered_max_no_bq1():
    """
    Verify that a nesting of ordered list, unordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.     >    + list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    + list\n       item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    + list
       item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_plus_one():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    >     + list
         >       item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):+ list\n  item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>+ list
  item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_unordered_max_plus_one_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >     + list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):+ list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):item:    ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>+ list
</code></pre>
</blockquote>
<pre><code>    item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_ordered_max():
    """
    Verify that a nesting of ordered list, block quote, ordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    >    1. list
         >       item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[olist(1,15):.:1:17:   :      ]",
        "[para(1,18):\n]",
        "[text(1,18):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_ordered_max_empty():
    """
    Verify that a nesting of ordered list, block quote, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   1.    >    1.
         >       item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[olist(1,15):.:1:17:   :      ]",
        "[BLANK(1,17):]",
        "[para(2,18):]",
        "[text(2,18):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li>item</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_ordered_max_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, ordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    1. list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > \n]",
        "[olist(1,15):.:1:17:   :                 \n]",
        "[para(1,18):\n]",
        "[text(1,18):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_ordered_max_empty_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    1.
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[olist(1,15):.:1:17:   ]",
        "[BLANK(1,17):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):item:    ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>    item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_ordered_max():
    """
    Verify that a nesting of ordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    1.    >    1.  list
          >        item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    1.  list\n      \a>\a&gt;\a        item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    1.  list
      &gt;        item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_ordered_max_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    1.    >    1.  list
                   item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    1.  list\n               item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    1.  list
               item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_ordered_max():
    """
    Verify that a nesting of ordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.     >    1. list
          >       item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    1. list\n\a>\a&gt;\a       item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    1. list
&gt;       item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_ordered_max_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.     >    1. list
                  item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    1. list\n        item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    1. list
        item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_ordered_max_plus_one():
    """
    Verify that a nesting of ordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    >     1. list
         >        item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):1. list\n   item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>1. list
   item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_ordered_max_plus_one_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >     1. list
                  item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):item:     ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
<pre><code>     item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    >    > list
         >    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > \n         >    > ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_empty():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   1.    >    >
         >    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    >\n         >    > ]",
        "[BLANK(1,16):]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    > list
              > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         \n]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > \n]",
        "[para(1,17):\n     ]",
        "[text(1,17):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_empty_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    >
              > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):\a>\a&gt;\a item: ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code> &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_no_bq2():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    > list
         >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > \n         > ]",
        "[para(1,17):\n     ]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_ordered_max_block_max_block_max_empty_no_bq2():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    >
         >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :\n]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    >\n         > ]",
        "[BLANK(1,16):]",
        "[BLANK(1,16):]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
</blockquote>
<pre><code> item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_no_bq3():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    > list
                item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         \n]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > \n]",
        "[para(1,17):\n       ]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_empty_no_bq3():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    >
                item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):item:   ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>   item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_block_max():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    1.    >    > list
          >    > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    \a>\a&gt;\a list\n      \a>\a&gt;\a    \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    &gt; list
      &gt;    &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_block_max_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    1.    >    > list
               > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    \a>\a&gt;\a list\n           \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    &gt; list
           &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_block_max_no_bq2():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    1.    >    > list
          >      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    \a>\a&gt;\a list\n      \a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    &gt; list
      &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_block_max_no_bq3():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    1.    >    > list
                 item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    \a>\a&gt;\a list\n             item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    &gt; list
             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_block_max():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.     >    > list
          >    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    \a>\a&gt;\a list\n\a>\a&gt;\a    \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    &gt; list
&gt;    &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_block_max_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.     >    > list
               > item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    \a>\a&gt;\a list\n     \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    &gt; list
     &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_block_max_no_bq2():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.     >    > list
          >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    \a>\a&gt;\a list\n\a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    &gt; list
&gt;      item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_block_max_no_bq3():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.     >    > list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    \a>\a&gt;\a list\n       item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    &gt; list
       item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_ordered_max_block_max_block_max_plus_one():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    >     > list
         >     > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):\a>\a&gt;\a item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>&gt; list
&gt; item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_plus_one_no_bq1():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >     > list
               > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):\a>\a&gt;\a item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
<pre><code>  &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_plus_one_no_bq2():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >     > list
         >       item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):\a>\a&gt;\a list\n  item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>&gt; list
  item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_plus_one_no_bq3():
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >     > list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):item:    ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
<pre><code>    item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
