"""
Extra tests for three level nesting with un/or.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_unordered_block_unordered() -> None:
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
def test_nested_three_unordered_nl_block_nl_unordered() -> None:
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
def test_nested_three_unordered_nl_block_nl_unordered_wo_bq() -> None:
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
def test_nested_three_unordered_text_nl_block_text_nl_unordered() -> None:
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
def test_nested_three_unordered_text_nl_block_text_nl_unordered_wo_bq() -> None:
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
def test_nested_three_unordered_block_skip_unordered() -> None:
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
def test_nested_three_unordered_nl_block_skip_nl_unordered() -> None:
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
def test_nested_three_unordered_nl_block_skip_nl_unordered_wo_bq() -> None:
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
def test_nested_three_unordered_text_nl_block_skip_text_nl_unordered() -> None:
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
def test_nested_three_unordered_text_nl_block_skip_text_nl_unordered_wo_bq() -> None:
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
def test_nested_three_unordered_max_block_max_unordered_max_x() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    >    + list
        >      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n        > ]",
        "[ulist(1,14):+::15:   :     ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
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
def test_nested_three_unordered_max_block_max_unordered_max_with_li1() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    + list
   +    >      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[ulist(1,14):+::15:   ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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
<ul>
<li>list</li>
</ul>
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
def test_nested_three_unordered_max_block_max_unordered_max_with_li2() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    + list
        >    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n        > ]",
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
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li>list</li>
<li>item</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_unordered_max_with_li3() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    + list
   +    >    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[ulist(1,14):+::15:   ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[ulist(2,14):+::15:   ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li>list</li>
</ul>
</blockquote>
</li>
<li>
<blockquote>
<ul>
<li>item</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_unordered_max_empty() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   +    >    +
        >      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n        > ]",
        "[ulist(1,14):+::15:   :     ]",
        "[BLANK(1,15):]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li>item</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_unordered_max_empty_with_li1() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    +
   +    >      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
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
<ul>
<li></li>
</ul>
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
def test_nested_three_unordered_max_block_max_unordered_max_empty_with_li2() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    +
        >    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n        > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[li(2,14):15:   :]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li></li>
<li>item</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_unordered_max_empty_with_li3() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    +
   +    >    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[ulist(2,14):+::15:   ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</li>
<li>
<blockquote>
<ul>
<li>item</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_unordered_max_no_bq1() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    + list
               item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n]",
        "[ulist(1,14):+::15:   :               \n]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
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
def test_nested_three_unordered_max_block_max_unordered_max_no_bq1_with_li1() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    + list
   +           item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[ulist(1,14):+::15:   ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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
<ul>
<li>list</li>
</ul>
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
def test_nested_three_unordered_max_block_max_unordered_max_no_bq1_with_li2() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    + list
             + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n]",
        "[ulist(1,14):+::15:   :             ]",
        "[para(1,16):\n]",
        "[text(1,16):list\n+ item::\n]",
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
+ item</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_unordered_max_no_bq1_with_li3() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    + list
   +         + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[ulist(1,14):+::15:   ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):+ item:    ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li>list</li>
</ul>
</blockquote>
</li>
<li>
<pre><code>    + item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_unordered_max_empty_no_bq1() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    +
               item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        ]",
        "[block-quote(1,9):        :        > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,13):    :]",
        "[text(2,13):item:   ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>   item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_unordered_max_empty_no_bq1_with_li1() -> (
    None
):
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    +
   +           item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
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
<ul>
<li></li>
</ul>
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
def test_nested_three_unordered_max_block_max_unordered_max_empty_no_bq1_with_li2() -> (
    None
):
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    +
             + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        ]",
        "[block-quote(1,9):        :        > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,13):    :]",
        "[text(2,13):+ item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code> + item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_unordered_max_empty_no_bq1_with_li3() -> (
    None
):
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    +
   +         + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[ulist(1,14):+::15:   ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):+ item:    ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</li>
<li>
<pre><code>    + item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_block_max_unordered_max() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    +    >    + list
         >      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    \a>\a&gt;\a    + list\n     \a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    &gt;    + list
     &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_block_max_unordered_max_no_bq1() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    +    >    + list
                item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    \a>\a&gt;\a    + list\n            item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    &gt;    + list
            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_plus_one_unordered_max() -> None:
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +     >    + list
         >      item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   :     ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    + list\n\a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>&gt;    + list
&gt;      item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_plus_one_unordered_max_no_bq1() -> None:
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +     >    + list
                item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   :     ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    + list\n       item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>&gt;    + list
       item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_unordered_max_plus_one() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    >     + list
   +          + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):+ list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):+ item:     ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<pre><code>+ list
</code></pre>
</blockquote>
</li>
<li>
<pre><code>     + item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_unordered_max_plus_one_no_bq1() -> None:
    """
    Verify that a nesting of unordered list, block quote, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >     + list
                item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        ]",
        "[block-quote(1,9):        :        > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):+ list:]",
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
<pre><code>+ list
</code></pre>
</blockquote>
<pre><code>    item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
