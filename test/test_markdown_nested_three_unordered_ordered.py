"""
Extra tests for three level nesting with un/or.
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines

@pytest.mark.gfm
def test_nested_three_unordered_ordered_unordered():
    """
    Verify that a nesting of unordered list, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ 1. + list
       item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[olist(1,3):.:1:5:  ]",
        "[ulist(1,6):+::7:     :       ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_unordered_nl_ordered_nl_unordered():
    """
    Verify that a nesting of unordered list, new line, ordered list, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  1.
     + list
       item"""
    expected_tokens = ['[ulist(1,1):+::2:]', '[BLANK(1,2):]', '[olist(2,3):.:1:5:  ]', '[BLANK(2,5):]', '[ulist(3,6):+::7:     :       ]', '[para(3,8):\n]', '[text(3,8):list\nitem::\n]', '[end-para:::True]', '[end-ulist:::True]', '[end-olist:::True]', '[end-ulist:::True]']
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_unordered_text_nl_ordered_text_nl_unordered():
    """
    Verify that a nesting of unordered list, text, new line, ordered list, text, new line, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  1. def
     + list
       item"""
    expected_tokens = ['[ulist(1,1):+::2:]', '[para(1,3):]', '[text(1,3):abc:]', '[end-para:::True]', '[olist(2,3):.:1:5:  ]', '[para(2,6):]', '[text(2,6):def:]', '[end-para:::True]', '[ulist(3,6):+::7:     :       ]', '[para(3,8):\n]', '[text(3,8):list\nitem::\n]','[end-para:::True]', '[end-ulist:::True]', '[end-olist:::True]', '[end-ulist:::True]']
    expected_gfm = """<ul>
<li>abc
<ol>
<li>def
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_unordered_ordered_ordered():
    """
    Verify that a nesting of unordered list, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ 1. 1. list
        item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[olist(1,3):.:1:5:  ]",
        "[olist(1,6):.:1:8:     :        ]",
        "[para(1,9):\n]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_unordered_nl_ordered_nl_ordered():
    """
    Verify that a nesting of unordered list, new line, ordered list, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  1.
     1. list
        item"""
    expected_tokens = ['[ulist(1,1):+::2:]', '[BLANK(1,2):]', '[olist(2,3):.:1:5:  ]', '[BLANK(2,5):]', '[olist(3,6):.:1:8:     :        ]', '[para(3,9):\n]', '[text(3,9):list\nitem::\n]', '[end-para:::True]', '[end-olist:::True]', '[end-olist:::True]', '[end-ulist:::True]']
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_unordered_text_nl_ordered_text_nl_ordered():
    """
    Verify that a nesting of unordered list, text, new line, ordered list, text, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  1. def
     1. list
        item"""
    expected_tokens = ['[ulist(1,1):+::2:]', '[para(1,3):]', '[text(1,3):abc:]', '[end-para:::True]', '[olist(2,3):.:1:5:  ]', '[para(2,6):]', '[text(2,6):def:]', '[end-para:::True]', '[olist(3,6):.:1:8:     :        ]', '[para(3,9):\n]', '[text(3,9):list\nitem::\n]', '[end-para:::True]', '[end-olist:::True]', '[end-olist:::True]', '[end-ulist:::True]']
    expected_gfm = """<ul>
<li>abc
<ol>
<li>def
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_unordered_ordered_block():
    """
    Verify that a nesting of unordered list, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ 1. > list
     > item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[olist(1,3):.:1:5:  :]",
        "[block-quote(1,6):     :     > \n     > ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_unordered_nl_ordered_nl_block():
    """
    Verify that a nesting of unordered list, new line, ordered list, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+
  1.
     > list
     > item"""
    expected_tokens = ['[ulist(1,1):+::2:]', '[BLANK(1,2):]', '[olist(2,3):.:1:5:  :\n]', '[BLANK(2,5):]', '[block-quote(3,6):     :     > \n     > ]', '[para(3,8):\n]', '[text(3,8):list\nitem::\n]', '[end-para:::True]', '[end-block-quote:::True]', '[end-olist:::True]', '[end-ulist:::True]']
    expected_gfm = """<ul>
<li>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_unordered_text_nl_ordered_text_nl_block():
    """
    Verify that a nesting of unordered list, text, new line, ordered list, text, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  1. def
     > list
     > item"""
    expected_tokens = ['[ulist(1,1):+::2:]', '[para(1,3):]', '[text(1,3):abc:]', '[end-para:::True]', '[olist(2,3):.:1:5:  :\n]', '[para(2,6):]', '[text(2,6):def:]', '[end-para:::True]', '[block-quote(3,6):     :     > \n     > ]', '[para(3,8):\n]', '[text(3,8):list\nitem::\n]', '[end-para:::True]', '[end-block-quote:::True]', '[end-olist:::True]', '[end-ulist:::True]']
    expected_gfm = """<ul>
<li>abc
<ol>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_unordered_ordered_block_skip():
    """
    Verify that a nesting of unordered list, ordered list, block quote with
    a skipped block quote character works properly.
    """

    # Arrange
    source_markdown = """+ 1. > list
       item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[olist(1,3):.:1:5:  :     \n]",
        "[block-quote(1,6):     :     > \n\n]",
        "[para(1,8):\n  ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_unordered_nl_ordered_nl_block_skip():
    """
    Verify that a nesting of unordered list, new line, ordered list, new line, block quote with
    a skipped block quote character works properly.
    """

    # Arrange
    source_markdown = """+
  1.
     > list
       item"""
    expected_tokens = ['[ulist(1,1):+::2:]', '[BLANK(1,2):]', '[olist(2,3):.:1:5:  :\n     \n]', '[BLANK(2,5):]', '[block-quote(3,6):     :     > \n\n]', '[para(3,8):\n  ]', '[text(3,8):list\nitem::\n]', '[end-para:::True]', '[end-block-quote:::True]', '[end-olist:::True]', '[end-ulist:::True]']
    expected_gfm = """<ul>
<li>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)

@pytest.mark.gfm
def test_nested_three_unordered_text_nl_ordered_text_nl_block_skip():
    """
    Verify that a nesting of unordered list, text, new line, ordered list, text, new line, block quote with
    a skipped block quote character works properly.
    """

    # Arrange
    source_markdown = """+ abc
  1. def
     > list
       item"""
    expected_tokens = ['[ulist(1,1):+::2:]', '[para(1,3):]', '[text(1,3):abc:]', '[end-para:::True]', '[olist(2,3):.:1:5:  :\n     \n]', '[para(2,6):]', '[text(2,6):def:]', '[end-para:::True]', '[block-quote(3,6):     :     > \n\n]', '[para(3,8):\n  ]', '[text(3,8):list\nitem::\n]', '[end-para:::True]', '[end-block-quote:::True]', '[end-olist:::True]', '[end-ulist:::True]']
    expected_gfm = """<ul>
<li>abc
<ol>
<li>def
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
