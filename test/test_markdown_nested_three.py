"""
Extra tests.
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_unordered_unordered_unordered():
    """
    Verify that a nesting of unordered list, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ + + list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :      ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
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
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_unordered_ordered():
    """
    Verify that a nesting of unordered list, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ + 1. list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[olist(1,5):.:1:7:    :]",
        "[para(1,8):\n      ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
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
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_unordered_block():
    """
    Verify that a nesting of unordered list, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """+ + > list
    > item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :]",
        "[block-quote(1,5):    :    > \n    > ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
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
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_unordered_block_skip():
    """
    Verify that a nesting of unordered list, unordered list, block quote
    with a skipped block quote character works properly.
    """

    # Arrange
    source_markdown = """+ + > list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n]",
        "[block-quote(1,5):    :    > \n\n]",
        "[para(1,7):\n  ]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
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
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


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
def test_nested_three_ordered_ordered_unordered():
    """
    Verify that a nesting of ordered list, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. 1. + list
        item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[ulist(1,7):+::8:      :        ]",
        "[para(1,9):\n]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_ordered_ordered():
    """
    Verify that a nesting of ordered list, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. 1. 1. list
         item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[olist(1,7):.:1:9:      :         ]",
        "[para(1,10):\n]",
        "[text(1,10):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_ordered_block_x():
    """
    Verify that a nesting of ordered list, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. 1. > list
      > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :]",
        "[block-quote(1,7):      :      > \n      > ]",
        "[para(1,9):\n]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_ordered_block_skip():
    """
    Verify that a nesting of ordered list, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. 1. > list
        item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :      \n]",
        "[block-quote(1,7):      :      > \n\n]",
        "[para(1,9):\n  ]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


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
def test_nested_three_ordered_block_skip_block():
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


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
        "[block-quote(1,6):   :   > > \n\n]",
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
def test_nested_three_block_unordered_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> + + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :    ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_skip_unordered_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> + + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :      \n]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_unordered_ordered():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> + 1. list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[olist(1,5):.:1:7:  :     ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_skip_unordered_ordered():
    """
    Verify that a nesting of block quote, unordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> + 1. list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[ulist(1,3):+::4:]",
        "[olist(1,5):.:1:7:  :       \n]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_x():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> + > list
>   > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n>   > ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_unordered_block():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> + > list
    > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n    > ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_block_skip():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> + > list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n> ]",
        "[para(1,7):\n     ]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_unordered_block_skip():
    """
    Verify that a nesting of block quote, unordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> + > list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::    \n]",
        "[block-quote(1,5)::> \n\n]",
        "[para(1,7):\n   ]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_ordered_unordered():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> 1. + list
>      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[ulist(1,6):+::7:   :     ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_skip_ordered_unordered():
    """
    Verify that a nesting of block quote, ordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> 1. + list
       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[olist(1,3):.:1:5:]",
        "[ulist(1,6):+::7:   :       \n]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_ordered_ordered():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> 1. 1. list
>       item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[olist(1,6):.:1:8:   :      ]",
        "[para(1,9):\n]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_skip_ordered_ordered():
    """
    Verify that a nesting of block quote, ordered list, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """> 1. 1. list
        item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[olist(1,3):.:1:5:]",
        "[olist(1,6):.:1:8:   :        \n]",
        "[para(1,9):\n]",
        "[text(1,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<ol>
<li>list
item</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_ordered_block_x():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> 1. > list
>    > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::]",
        "[block-quote(1,6)::> \n>    > ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_nested_three_block_skip_ordered_block():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> 1. > list
     > item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::]",
        "[block-quote(1,6)::> \n     > ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_ordered_block_skip():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> 1. > list
>       item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::]",
        "[block-quote(1,6)::> \n> ]",
        "[para(1,8):\n      ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_ordered_block_skip():
    """
    Verify that a nesting of block quote, ordered list, block quote works
    properly.
    """

    # Arrange
    source_markdown = """> 1. > list
        item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::     \n]",
        "[block-quote(1,6)::> \n\n]",
        "[para(1,8):\n   ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
        "[ulist(1,5):+::6::      \n]",
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
        "[olist(1,5):.:1:7::       \n]",
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
