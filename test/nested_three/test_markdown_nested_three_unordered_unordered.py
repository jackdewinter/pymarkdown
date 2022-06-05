"""
Extra tests for three level nesting with un/un.
"""
from test.utils import act_and_assert

import pytest

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
def test_nested_three_unordered_nl_unordered_nl_unordered():
    """
    Verify that a nesting of unordered list, new line, unordered list, new line, unordered list works.
    properly.
    """

    # Arrange
    source_markdown = """+
  +
    + list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6:    :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
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
def test_nested_three_unordered_text_nl_unordered_text_nl_unordered():
    """
    Verify that a nesting of unordered list, text, new line, unordered list, tex, new line, unordered list works.
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  + def
    + list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6:    :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
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
def test_nested_three_unordered_nl_unordered_nl_ordered():
    """
    Verify that a nesting of unordered list, new line, unordered list, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  +
    1. list
       item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[olist(3,5):.:1:7:    :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
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
def test_nested_three_unordered_text_nl_unordered_text_nl_ordered():
    """
    Verify that a nesting of unordered list, text, new line, unordered list, text, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  + def
    1. list
       item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[olist(3,5):.:1:7:    :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
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
def test_nested_three_unordered_nl_unordered_nl_block():
    """
    Verify that a nesting of unordered list, new line, unordered list, new line,
    block quote works properly.
    """

    # Arrange
    source_markdown = """+
  +
    > list
    > item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:  :\n]",
        "[BLANK(2,4):]",
        "[block-quote(3,5):    :    > \n    > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
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
def test_nested_three_unordered_text_nl_unordered_text_nl_block():
    """
    Verify that a nesting of unordered list, text, new line, unordered list, text, new line,
    block quote works properly.
    """

    # Arrange
    source_markdown = """+ abc
  + def
    > list
    > item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:  :\n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,5):    :    > \n    > ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
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
        "[block-quote(1,5):    :    > \n]",
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
def test_nested_three_unordered_nl_unordered_nl_block_skip():
    """
    Verify that a nesting of unordered list, new line, unordered list, new line, block quote
    with a skipped block quote character works properly.
    """

    # Arrange
    source_markdown = """+
  +
    > list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:  :\n    \n]",
        "[BLANK(2,4):]",
        "[block-quote(3,5):    :    > \n]",
        "[para(3,7):\n  ]",
        "[text(3,7):list\nitem::\n]",
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
def test_nested_three_unordered_text_nl_unordered_text_nl_block_skip():
    """
    Verify that a nesting of unordered list, text, newline, unordered list, text, new line, block quote
    with a skipped block quote character works properly.
    """

    # Arrange
    source_markdown = """+ abc
  + def
    > list
      item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:  :\n    \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[block-quote(3,5):    :    > \n]",
        "[para(3,7):\n  ]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
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
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    +    + list
               item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             :               ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
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
def test_nested_three_unordered_max_unordered_max_unordered_max_with_li1():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    + list
   +           item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:      ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>list</li>
</ul>
</li>
</ul>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_with_li2():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    + list
        +      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,9):10:        :]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>list</li>
</ul>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_with_li3():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    + list
             + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[li(2,14):15:             :]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
<li>list</li>
<li>item</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_with_li4():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    + list
        +    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,9):13:        :]",
        "[ulist(2,14):+::15:             ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
<li>list</li>
</ul>
</li>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_with_li5():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    + list
   +         + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):+ item:    ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>list</li>
</ul>
</li>
</ul>
</li>
<li>
<pre><code>    + item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_with_li6():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    + list
   +    +      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::10:        ]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>list</li>
</ul>
</li>
</ul>
</li>
<li>
<ul>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_with_li7():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    + list
   +    +    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::13:        ]",
        "[ulist(2,14):+::15:             ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
<li>list</li>
</ul>
</li>
</ul>
</li>
<li>
<ul>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_empty():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly.
    """

    # Arrange
    source_markdown = """   +    +    +
               item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             :               ]",
        "[BLANK(1,15):]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
<li>item</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_empty_with_li1():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    +
   +           item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:      ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_empty_with_li2():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    +
        +      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[li(2,9):10:        :]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_empty_with_li3():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    +
             + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[BLANK(1,15):]",
        "[li(2,14):15:             :]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
<li></li>
<li>item</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_empty_with_li4():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    +
        +    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[li(2,9):13:        :]",
        "[ulist(2,14):+::15:             ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
<li></li>
</ul>
</li>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_empty_with_li5():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    +
   +         + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):+ item:    ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>
</li>
<li>
<pre><code>    + item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_empty_with_li6():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    +
   +    +      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::10:        ]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>
</li>
<li>
<ul>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_empty_with_li7():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line,
    works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    +
   +    +    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[ulist(1,14):+::15:             ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::13:        ]",
        "[ulist(2,14):+::15:             ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
<li></li>
</ul>
</li>
</ul>
</li>
<li>
<ul>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_unordered_max_unordered_max():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    +    +    + list
                item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    +    + list\n            item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    +    + list
            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_plus_one_unordered_max():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +     +    + list
                item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   :     ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):+    + list\n       item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>+    + list
       item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_unordered_max_plus_one():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    +     + list
                item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::10:        :          ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):+ list\n  item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<pre><code>+ list
  item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    +    1. list
                item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             :                ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_unordered_max_unordered_max_ordered_max_with_li1():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1. list
   +            item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:       ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ol>
<li>list</li>
</ol>
</li>
</ul>
</li>
<li>
<pre><code>       item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_with_li2():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1. list
        +       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(2,9):10:        :]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item:  ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ol>
<li>list</li>
</ol>
</li>
<li>
<pre><code>  item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_with_li3():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1. list
             1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[li(2,14):16:             :1]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li>list</li>
<li>item</li>
</ol>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_with_li4():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1. list
        +    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(2,9):13:        :]",
        "[olist(2,14):.:1:16:             ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li>list</li>
</ol>
</li>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_with_li5():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1. list
   +         1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:    ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ol>
<li>list</li>
</ol>
</li>
</ul>
</li>
<li>
<pre><code>    1. item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_with_li6():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1. list
   +    +       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::10:        ]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item:  ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ol>
<li>list</li>
</ol>
</li>
</ul>
</li>
<li>
<ul>
<li>
<pre><code>  item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_with_li7():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1. list
   +    +    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::13:        ]",
        "[olist(2,14):.:1:16:             ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li>list</li>
</ol>
</li>
</ul>
</li>
<li>
<ul>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_empty():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   +    +    1.
                item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             :                ]",
        "[BLANK(1,16):]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li>item</li>
</ol>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_empty_with_li1():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1.
   +            item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:       ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ol>
<li></li>
</ol>
</li>
</ul>
</li>
<li>
<pre><code>       item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_empty_with_li2():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1.
        +       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[li(2,9):10:        :]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item:  ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ol>
<li></li>
</ol>
</li>
<li>
<pre><code>  item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_empty_with_li3():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1.
             1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[BLANK(1,16):]",
        "[li(2,14):16:             :1]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li></li>
<li>item</li>
</ol>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_empty_with_li4():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1.
        +    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[li(2,9):13:        :]",
        "[olist(2,14):.:1:16:             ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li></li>
</ol>
</li>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_empty_with_li5():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1.
   +         1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:    ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ol>
<li></li>
</ol>
</li>
</ul>
</li>
<li>
<pre><code>    1. item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_empty_with_li6():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1.
   +    +       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::10:        ]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item:  ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ol>
<li></li>
</ol>
</li>
</ul>
</li>
<li>
<ul>
<li>
<pre><code>  item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_empty_with_li7():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    1.
   +    +    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[olist(1,14):.:1:16:             ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::13:        ]",
        "[olist(2,14):.:1:16:             ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li></li>
</ol>
</li>
</ul>
</li>
<li>
<ul>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_unordered_max_ordered_max():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    +    +    1.  list
                  item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    +    1.  list\n              item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    +    1.  list
              item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_plus_one_ordered_max():
    """
    Verify that a nesting of unordered list, unordered list, ordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +     +    1. list
                 item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   :     ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):+    1. list\n        item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>+    1. list
        item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_ordered_max_plus_one():
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    +     1. list
                 item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::10:        :          ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):1. list\n   item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<pre><code>1. list
   item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    +    > list
             > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        :]",
        "[block-quote(1,14):             :             > \n             > ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
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
def test_nested_three_unordered_max_unordered_max_block_max_with_li1():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    > list
   +         > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[block-quote(1,14):             :             > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):\a>\a&gt;\a item:    ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
</ul>
</li>
<li>
<pre><code>    &gt; item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_with_li2():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    > list
        +    > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        :]",
        "[block-quote(1,14):             :             > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(2,9):13:        :]",
        "[block-quote(2,14):             :             > ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
<p>list</p>
</blockquote>
</li>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_with_li3():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    > list
   +    +    > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[block-quote(1,14):             :             > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::13:        ]",
        "[block-quote(2,14):             :             > ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
<p>list</p>
</blockquote>
</li>
</ul>
</li>
<li>
<ul>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_empty():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   +    +    >
             > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        :]",
        "[block-quote(1,14):             :             >\n             > ]",
        "[BLANK(1,15):]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
<p>item</p>
</blockquote>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_empty_with_li1():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   +    +    >
   +         > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[block-quote(1,14):             :             >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):\a>\a&gt;\a item:    ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
</blockquote>
</li>
</ul>
</li>
<li>
<pre><code>    &gt; item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_empty_with_li2():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   +    +    >
        +    > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        :]",
        "[block-quote(1,14):             :             >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[li(2,9):13:        :]",
        "[block-quote(2,14):             :             > ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
</blockquote>
</li>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_empty_with_li3():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   +    +    >
   +    +    > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[block-quote(1,14):             :             >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::13:        ]",
        "[block-quote(2,14):             :             > ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
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
</blockquote>
</li>
</ul>
</li>
<li>
<ul>
<li>
<blockquote>
<p>item</p>
</blockquote>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_no_bq1():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, with no block quote
    characters on the second line.
    """

    # Arrange
    source_markdown = """   +    +    > list
               item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        :             \n]",
        "[block-quote(1,14):             :             > \n]",
        "[para(1,16):\n  ]",
        "[text(1,16):list\nitem::\n]",
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
def test_nested_three_unordered_max_unordered_max_block_max_no_bq1_with_li1():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, with no block quote
    characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    > list
   +           item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[block-quote(1,14):             :             > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:      ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
</ul>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_no_bq1_with_li2():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, with no block quote
    characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    > list
        +      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[block-quote(1,14):             :             > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(2,9):10:        :]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_no_bq1_with_li3():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, with no block quote
    characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    > list
   +    +      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[block-quote(1,14):             :             > ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::10:        ]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
</ul>
</li>
<li>
<ul>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_empty_no_bq1():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, and no text on the
    first line, with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    +    >
               item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        :             \n]",
        "[block-quote(1,14):             :             >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::False]",
        "[para(2,16):  ]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
</blockquote>
item</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_empty_no_bq1_with_li1():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, and no text on the
    first line, with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    >
   +           item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[block-quote(1,14):             :             >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:      ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
</blockquote>
</li>
</ul>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_empty_no_bq1_with_li2():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, and no text on the
    first line, with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    >
        +      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[block-quote(1,14):             :             >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[li(2,9):10:        :]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
</blockquote>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_empty_no_bq1_with_li3():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces allowed, works properly, and no text on the
    first line, with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    +    >
   +    +      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::13:        ]",
        "[block-quote(1,14):             :             >]",
        "[BLANK(1,15):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[li(2,4):8:   :]",
        "[ulist(2,9):+::10:        ]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
</blockquote>
</li>
</ul>
</li>
<li>
<ul>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_unordered_max_block_max():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    +    +    > list
              > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    +    \a>\a&gt;\a list\n          \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    +    &gt; list
          &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_unordered_max_block_max_no_bq1():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    +    +    > list
                item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    +    \a>\a&gt;\a list\n            item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    +    &gt; list
            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_plus_one_block_max():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +     +    > list
              > item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   :     ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):+    \a>\a&gt;\a list\n     \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>+    &gt; list
     &gt; item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_plus_one_block_max_no_bq1():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +     +    > list
                item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   :     ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):+    \a>\a&gt;\a list\n       item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>+    &gt; list
       item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_plus_one():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    +     > list
              > item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::10:        :          ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):\a>\a&gt;\a list\n\a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<pre><code>&gt; list
&gt; item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_unordered_max_block_max_plus_one_no_bq1():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    +     > list
                item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[ulist(1,9):+::10:        :          ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):\a>\a&gt;\a list\n  item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<pre><code>&gt; list
  item
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
