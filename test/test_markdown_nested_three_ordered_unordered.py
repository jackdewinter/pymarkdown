"""
Extra tests for three level nesting with un/un.
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines

@pytest.mark.gfm
def test_nested_three_ordered_unordered_unordered():
    """
    Verify that a nesting of ordered list, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. + + list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[ulist(1,4):+::5:   ]",
        "[ulist(1,6):+::7:     :       ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_ordered_nl_unordered_nl_unordered():
    """
    Verify that a nesting of ordered list, new line, unordered list, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   +
     + list
       item"""
    expected_tokens = ['[olist(1,1):.:1:3:]', '[BLANK(1,3):]', '[ulist(2,4):+::5:   ]', '[BLANK(2,5):]', '[ulist(3,6):+::7:     :       ]', '[para(3,8):\n]', '[text(3,8):list\nitem::\n]', '[end-para:::True]', '[end-ulist:::True]', '[end-ulist:::True]', '[end-olist:::True]']
    expected_gfm = """<ol>
<li>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_ordered_text_nl_unordered_text_nl_unordered():
    """
    Verify that a nesting of ordered list, text, new line, unordered list, text, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   + def
     + list
       item"""
    expected_tokens = ['[olist(1,1):.:1:3:]', '[para(1,4):]', '[text(1,4):abc:]', '[end-para:::True]', '[ulist(2,4):+::5:   ]', '[para(2,6):]', '[text(2,6):def:]', '[end-para:::True]', '[ulist(3,6):+::7:     :       ]', '[para(3,8):\n]', '[text(3,8):list\nitem::\n]', '[end-para:::True]', '[end-ulist:::True]', '[end-ulist:::True]', '[end-olist:::True]']
    expected_gfm = """<ol>
<li>abc
<ul>
<li>def
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_ordered_unordered_ordered():
    """
    Verify that a nesting of ordered list, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. + 1. list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[ulist(1,4):+::5:   ]",
        "[olist(1,6):.:1:8:     :]",
        "[para(1,9):\n       ]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_ordered_nl_unordered_nl_ordered():
    """
    Verify that a nesting of ordered list, new line, unordered list, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   +
     1. list
        item"""
    expected_tokens = ['[olist(1,1):.:1:3:]', '[BLANK(1,3):]', '[ulist(2,4):+::5:   ]', '[BLANK(2,5):]', '[olist(3,6):.:1:8:     :        ]', '[para(3,9):\n]', '[text(3,9):list\nitem::\n]', '[end-para:::True]', '[end-olist:::True]', '[end-ulist:::True]', '[end-olist:::True]']
    expected_gfm = """<ol>
<li>
<ul>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_ordered_text_nl_unordered_text_nl_ordered():
    """
    Verify that a nesting of ordered list, text, new line, unordered list, text, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   + def
     1. list
        item"""
    expected_tokens = ['[olist(1,1):.:1:3:]', '[para(1,4):]', '[text(1,4):abc:]', '[end-para:::True]', '[ulist(2,4):+::5:   ]', '[para(2,6):]', '[text(2,6):def:]', '[end-para:::True]', '[olist(3,6):.:1:8:     :        ]', '[para(3,9):\n]', '[text(3,9):list\nitem::\n]', '[end-para:::True]', '[end-olist:::True]', '[end-ulist:::True]', '[end-olist:::True]']
    expected_gfm = """<ol>
<li>abc
<ul>
<li>def
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_ordered_unordered_block():
    """
    Verify that a nesting of ordered list, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. + > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[ulist(1,4):+::5:   :]",
        "[block-quote(1,6):     :     > \n     > ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_ordered_nl_unordered_nl_block():
    """
    Verify that a nesting of ordered list, new list, unordered list, new list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   +
     > list
     > item"""
    expected_tokens = ['[olist(1,1):.:1:3:]', '[BLANK(1,3):]', '[ulist(2,4):+::5:   :\n]', '[BLANK(2,5):]', '[block-quote(3,6):     :     > \n     > ]', '[para(3,8):\n]', '[text(3,8):list\nitem::\n]', '[end-para:::True]', '[end-block-quote:::True]', '[end-ulist:::True]', '[end-olist:::True]']
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_ordered_text_nl_unordered_text_nl_block():
    """
    Verify that a nesting of ordered list, text, new list, unordered list, text, new list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   + def
     > list
     > item"""
    expected_tokens = ['[olist(1,1):.:1:3:]', '[para(1,4):]', '[text(1,4):abc:]', '[end-para:::True]', '[ulist(2,4):+::5:   :\n]', '[para(2,6):]', '[text(2,6):def:]', '[end-para:::True]', '[block-quote(3,6):     :     > \n     > ]', '[para(3,8):\n]', '[text(3,8):list\nitem::\n]', '[end-para:::True]', '[end-block-quote:::True]', '[end-ulist:::True]', '[end-olist:::True]']
    expected_gfm = """<ol>
<li>abc
<ul>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_ordered_unordered_block_skip():
    """
    Verify that a nesting of ordered list, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. + > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[ulist(1,4):+::5:   :     \n]",
        "[block-quote(1,6):     :     > \n\n]",
        "[para(1,8):\n  ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_ordered_nl_unordered_nl_block_skip():
    """
    Verify that a nesting of ordered list, new line, unordered list, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   +
     > list
       item"""
    expected_tokens = ['[olist(1,1):.:1:3:]', '[BLANK(1,3):]', '[ulist(2,4):+::5:   :\n     \n]', '[BLANK(2,5):]', '[block-quote(3,6):     :     > \n\n]', '[para(3,8):\n  ]', '[text(3,8):list\nitem::\n]', '[end-para:::True]', '[end-block-quote:::True]', '[end-ulist:::True]', '[end-olist:::True]']
    expected_gfm = """<ol>
<li>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
