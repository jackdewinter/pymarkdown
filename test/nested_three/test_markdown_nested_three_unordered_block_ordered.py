"""
Extra tests for three level nesting with un/or.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered() -> None:
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
def test_nested_three_unordered_nl_block_nl_ordered() -> None:
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
def test_nested_three_unordered_nl_block_nl_ordered_wo_bq() -> None:
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
def test_nested_three_unordered_text_nl_block_text_nl_ordered() -> None:
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
def test_nested_three_unordered_text_nl_block_text_nl_ordered_wo_bq() -> None:
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
def test_nested_three_unordered_block_skip_ordered() -> None:
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
def test_nested_three_unordered_nl_block_skip_nl_ordered() -> None:
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
def test_nested_three_unordered_nl_block_skip_nl_ordered_wo_bq() -> None:
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
def test_nested_three_unordered_text_nl_block_skip_text_nl_ordered() -> None:
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
def test_nested_three_unordered_text_nl_block_skip_text_nl_ordered_wo_bq() -> None:
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
def test_nested_three_unordered_max_block_max_ordered_max_x() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    >    1. list
        >       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n        > ]",
        "[olist(1,14):.:1:16:   :      ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_unordered_max_block_max_ordered_max_with_li1() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1. list
   +    >       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item:  ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li>list</li>
</ol>
</blockquote>
</li>
<li>
<blockquote>
<pre><code>  item
</code></pre>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_with_li2() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1. list
        >    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[li(2,14):16:   :1]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li>list</li>
<li>item</li>
</ol>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_with_li3() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1. list
   +    >    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[olist(2,14):.:1:16:   ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li>list</li>
</ol>
</blockquote>
</li>
<li>
<blockquote>
<ol>
<li>item</li>
</ol>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_empty() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   +    >    1.
        >       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n        > ]",
        "[olist(1,14):.:1:16:   :      ]",
        "[BLANK(1,16):]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li>item</li>
</ol>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_empty_with_li1() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1.
   +    >       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :]",
        "[block-quote(1,9):        :        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item:  ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</li>
<li>
<blockquote>
<pre><code>  item
</code></pre>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_empty_with_li2() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1.
        >    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[li(2,14):16:   :1]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li></li>
<li>item</li>
</ol>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_empty_with_li3() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1.
   +    >    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):8:   :]",
        "[block-quote(2,9):        :        > ]",
        "[olist(2,14):.:1:16:   ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</li>
<li>
<blockquote>
<ol>
<li>item</li>
</ol>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_no_bq1() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    1. list
                item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n]",
        "[olist(1,14):.:1:16:   :                \n]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_unordered_max_block_max_ordered_max_no_bq1_with_li1() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1. list
   +            item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:       ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li>list</li>
</ol>
</blockquote>
</li>
<li>
<pre><code>       item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_no_bq1_with_li2() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1. list
             1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > \n]",
        "[olist(1,14):.:1:16:   :             ]",
        "[para(1,17):\n]",
        "[text(1,17):list\n1. item::\n]",
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
1. item</li>
</ol>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_no_bq1_with_li3() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1. list
   +        1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:   ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li>list</li>
</ol>
</blockquote>
</li>
<li>
<pre><code>   1. item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_empty_no_bq1() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >    1.
                item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        ]",
        "[block-quote(1,9):        :        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,13):    :]",
        "[text(2,13):item:    ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>    item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_empty_no_bq1_with_li1() -> (
    None
):
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1.
   +            item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:       ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</li>
<li>
<pre><code>       item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_empty_no_bq1_with_li2() -> (
    None
):
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1.
             1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        ]",
        "[block-quote(1,9):        :        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,13):    :]",
        "[text(2,13):1. item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code> 1. item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_empty_no_bq1_with_li3() -> (
    None
):
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   +    >    1.
   +         1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:    ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</li>
<li>
<pre><code>    1. item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_block_max_ordered_max() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    +    >    1.  list
    +         1.  item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    \a>\a&gt;\a    1.  list\n+         1.  item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    &gt;    1.  list
+         1.  item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_block_max_ordered_max_no_bq1() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    +    >    1.  list
                  item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    \a>\a&gt;\a    1.  list\n              item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    &gt;    1.  list
              item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_plus_one_ordered_max() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +     >    1. list
   +          1. item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:     ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>&gt;    1. list
</code></pre>
</li>
<li>
<pre><code>     1. item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_plus_one_ordered_max_no_bq1() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +     >    1. list
                 item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   :     ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    1. list\n        item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>&gt;    1. list
        item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_plus_one() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    >     1. list
   +          1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[block-quote(1,9):        :        > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:     ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</li>
<li>
<pre><code>     1. item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_block_max_ordered_max_plus_one_no_bq1() -> None:
    """
    Verify that a nesting of unordered list, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   +    >     1. list
                 item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   :        ]",
        "[block-quote(1,9):        :        > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,13):    :]",
        "[text(2,13):item:     ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
<pre><code>     item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_atx_x() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2

## Headline 2

Some Text
"""

    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[olist(2,5):):1:7:]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[atx(5,1):2:0:]",
        "[text(5,4):Headline 2: ]",
        "[end-atx::]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[text(7,1):Some Text:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
</li>
</ul>
<h2>Headline 2</h2>
<p>Some Text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_atx_a() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2

  ## Headline 2

Some Text
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[olist(2,5):):1:7:]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[atx(5,3):2:0:]",
        "[text(5,6):Headline 2: ]",
        "[end-atx::]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[para(7,1):]",
        "[text(7,1):Some Text:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<ul>
<li>
<p>Test List</p>
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
<h2>Headline 2</h2>
</li>
</ul>
<p>Some Text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_text_atx_x() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List

  > 1) Test1
  > 2) Test2

  this is some text

## Headline 2

Some Text
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n\n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,3):  :  > \n  > ]",
        "[olist(3,5):):1:7:]",
        "[para(3,8):]",
        "[text(3,8):Test1:]",
        "[end-para:::True]",
        "[li(4,5):7::2]",
        "[para(4,8):]",
        "[text(4,8):Test2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[para(6,3):]",
        "[text(6,3):this is some text:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[atx(8,1):2:0:]",
        "[text(8,4):Headline 2: ]",
        "[end-atx::]",
        "[BLANK(9,1):]",
        "[para(10,1):]",
        "[text(10,1):Some Text:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<ul>
<li>
<p>Test List</p>
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
<p>this is some text</p>
</li>
</ul>
<h2>Headline 2</h2>
<p>Some Text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_text_atx_a() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List

  > 1) Test1
  > 2) Test2

this is some text

## Headline 2

Some Text
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,3):  :  > \n  > ]",
        "[olist(3,5):):1:7:]",
        "[para(3,8):]",
        "[text(3,8):Test1:]",
        "[end-para:::True]",
        "[li(4,5):7::2]",
        "[para(4,8):]",
        "[text(4,8):Test2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[para(6,1):]",
        "[text(6,1):this is some text:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[atx(8,1):2:0:]",
        "[text(8,4):Headline 2: ]",
        "[end-atx::]",
        "[BLANK(9,1):]",
        "[para(10,1):]",
        "[text(10,1):Some Text:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<ul>
<li>
<p>Test List</p>
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
</li>
</ul>
<p>this is some text</p>
<h2>Headline 2</h2>
<p>Some Text</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_thematic_x() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """# Headline 1

- Test List

  > 1) Test1
  > 2) Test2

-----
"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):Headline 1: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[ulist(3,1):-::2::\n]",
        "[para(3,3):]",
        "[text(3,3):Test List:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[block-quote(5,3):  :  > \n  > ]",
        "[olist(5,5):):1:7:]",
        "[para(5,8):]",
        "[text(5,8):Test1:]",
        "[end-para:::True]",
        "[li(6,5):7::2]",
        "[para(6,8):]",
        "[text(6,8):Test2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[tbreak(8,1):-::-----]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<h1>Headline 1</h1>
<ul>
<li>
<p>Test List</p>
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_thematic_a() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """# Headline 1

- Test List

  > 1) Test1
  > 2) Test2

  -----
"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):Headline 1: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[ulist(3,1):-::2::\n\n  \n]",
        "[para(3,3):]",
        "[text(3,3):Test List:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[block-quote(5,3):  :  > \n  > ]",
        "[olist(5,5):):1:7:]",
        "[para(5,8):]",
        "[text(5,8):Test1:]",
        "[end-para:::True]",
        "[li(6,5):7::2]",
        "[para(6,8):]",
        "[text(6,8):Test2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[tbreak(8,3):-::-----]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<h1>Headline 1</h1>
<ul>
<li>
<p>Test List</p>
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
<hr />
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_x() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2

```text
block
```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[olist(2,5):):1:7:]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[fcode-block(5,1):`:3:text:::::]",
        "[text(6,1):block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
</li>
</ul>
<pre><code class="language-text">block
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_a() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2

  ```text
  block
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[olist(2,5):):1:7:]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[fcode-block(5,3):`:3:text:::::]",
        "[text(6,3):block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>Test List</p>
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
<pre><code class="language-text">block
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_bx() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2
  >
  ```text
  block
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  >]",
        "[olist(2,5):):1:7::]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::True]",
        "[BLANK(4,4):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:text:::::]",
        "[text(6,3):block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
<pre><code class="language-text">block
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_ba() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2
  > abc
  ```text
  block
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > ]",
        "[olist(2,5):):1:7::]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):\n]",
        "[text(3,8):Test2\nabc::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:text:::::]",
        "[text(6,3):block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2
abc</li>
</ol>
</blockquote>
<pre><code class="language-text">block
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_bb() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """
    ####
    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2
  > ___
  ```text
  block
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > ]",
        "[olist(2,5):):1:7:]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[tbreak(4,5):_::___]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:text:::::]",
        "[text(6,3):block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
<hr />
</blockquote>
<pre><code class="language-text">block
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_bc() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2
  > # bob
  ```text
  block
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > ]",
        "[olist(2,5):):1:7::]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[atx(4,5):1:0:]",
        "[text(4,7):bob: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:text:::::]",
        "[text(6,3):block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
<h1>bob</h1>
</blockquote>
<pre><code class="language-text">block
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_bdx() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2
  > # bob
  abc
  ```text
  block
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > ]",
        "[olist(2,5):):1:7::]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[atx(4,5):1:0:]",
        "[text(4,7):bob: ]",
        "[end-atx::]",
        "[end-block-quote:::False]",
        "[para(5,3):]",
        "[text(5,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(6,3):`:3:text:::::]",
        "[text(7,3):block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
<h1>bob</h1>
</blockquote>
abc
<pre><code class="language-text">block
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_bda() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2
  > bob
  abc
  ```text
  block
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > \n]",
        "[olist(2,5):):1:7::\n  ]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):\n\n]",
        "[text(3,8):Test2\nbob\nabc::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(6,3):`:3:text:::::]",
        "[text(7,3):block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2
bob
abc</li>
</ol>
</blockquote>
<pre><code class="language-text">block
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_bdb() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2
  >    bob
  abc
  ```text
  block
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > \n]",
        "[olist(2,5):):1:7::   \n  ]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):\n\n]",
        "[text(3,8):Test2\nbob\nabc::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(6,3):`:3:text:::::]",
        "[text(7,3):block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2
bob
abc</li>
</ol>
</blockquote>
<pre><code class="language-text">block
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_be() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2
  > # bob
  > # robert
  abc
  ```text
  block
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n  \n  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > \n  > ]",
        "[olist(2,5):):1:7::]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[atx(4,5):1:0:]",
        "[text(4,7):bob: ]",
        "[end-atx::]",
        "[atx(5,5):1:0:]",
        "[text(5,7):robert: ]",
        "[end-atx::]",
        "[end-block-quote:::False]",
        "[para(6,3):]",
        "[text(6,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(7,3):`:3:text:::::]",
        "[text(8,3):block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
<h1>bob</h1>
<h1>robert</h1>
</blockquote>
abc
<pre><code class="language-text">block
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_bf() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2
  > # bob
  > # robert
  abc
  # cblock
  block
  # uncblock
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n  \n  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > \n  > ]",
        "[olist(2,5):):1:7::]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[atx(4,5):1:0:]",
        "[text(4,7):bob: ]",
        "[end-atx::]",
        "[atx(5,5):1:0:]",
        "[text(5,7):robert: ]",
        "[end-atx::]",
        "[end-block-quote:::False]",
        "[para(6,3):]",
        "[text(6,3):abc:]",
        "[end-para:::False]",
        "[atx(7,3):1:0:]",
        "[text(7,5):cblock: ]",
        "[end-atx::]",
        "[para(8,3):]",
        "[text(8,3):block:]",
        "[end-para:::False]",
        "[atx(9,3):1:0:]",
        "[text(9,5):uncblock: ]",
        "[end-atx::]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
<h1>bob</h1>
<h1>robert</h1>
</blockquote>
abc
<h1>cblock</h1>
block
<h1>uncblock</h1>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_bg() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > # Test1
  > Test2
  > # bob
  > robert
  # abc
  # cblock
  block
  # uncblock
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n\n\n\n  \n  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > \n  > ]",
        "[atx(2,5):1:0:]",
        "[text(2,7):Test1: ]",
        "[end-atx::]",
        "[para(3,5):]",
        "[text(3,5):Test2:]",
        "[end-para:::False]",
        "[atx(4,5):1:0:]",
        "[text(4,7):bob: ]",
        "[end-atx::]",
        "[para(5,5):]",
        "[text(5,5):robert:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[atx(6,3):1:0:]",
        "[text(6,5):abc: ]",
        "[end-atx::]",
        "[atx(7,3):1:0:]",
        "[text(7,5):cblock: ]",
        "[end-atx::]",
        "[para(8,3):]",
        "[text(8,3):block:]",
        "[end-para:::False]",
        "[atx(9,3):1:0:]",
        "[text(9,5):uncblock: ]",
        "[end-atx::]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<h1>Test1</h1>
<p>Test2</p>
<h1>bob</h1>
<p>robert</p>
</blockquote>
<h1>abc</h1>
<h1>cblock</h1>
block
<h1>uncblock</h1>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_c1() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2
  >
  ```text
  block
  text
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  >]",
        "[olist(2,5):):1:7::]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::True]",
        "[BLANK(4,4):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:text:::::]",
        "[text(6,3):block\ntext:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
<pre><code class="language-text">block
text
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_c2() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > 1) Test1
  > 2) Test2
  ```text
  block
  text
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[olist(2,5):):1:7:]",
        "[para(2,8):]",
        "[text(2,8):Test1:]",
        "[end-para:::True]",
        "[li(3,5):7::2]",
        "[para(3,8):]",
        "[text(3,8):Test2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,3):`:3:text:::::]",
        "[text(5,3):block\ntext:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
<pre><code class="language-text">block
text
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_e1() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > Test1
  > Test2
  >
  ```text
  text
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n\n\n  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  >]",
        "[para(2,5):\n]",
        "[text(2,5):Test1\nTest2::\n]",
        "[end-para:::True]",
        "[BLANK(4,4):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:text:::::]",
        "[text(6,3):text:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<p>Test1
Test2</p>
</blockquote>
<pre><code class="language-text">text
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_fenced_e2() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """- Test List
  > Test1
  > Test2
  ```text
  text
  ```
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n\n  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):Test List:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[para(2,5):\n]",
        "[text(2,5):Test1\nTest2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,3):`:3:text:::::]",
        "[text(5,3):text:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Test List
<blockquote>
<p>Test1
Test2</p>
</blockquote>
<pre><code class="language-text">text
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_html_x() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """# Headline 1

- Test List

  > 1) Test1
  > 2) Test2

<!-- this is html-->
"""

    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):Headline 1: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[ulist(3,1):-::2::\n]",
        "[para(3,3):]",
        "[text(3,3):Test List:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[block-quote(5,3):  :  > \n  > ]",
        "[olist(5,5):):1:7:]",
        "[para(5,8):]",
        "[text(5,8):Test1:]",
        "[end-para:::True]",
        "[li(6,5):7::2]",
        "[para(6,8):]",
        "[text(6,8):Test2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[html-block(8,1)]",
        "[text(8,1):<!-- this is html-->:]",
        "[end-html-block:::False]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<h1>Headline 1</h1>
<ul>
<li>
<p>Test List</p>
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
</li>
</ul>
<!-- this is html-->"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_block_ordered_with_blank_html_a() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    source_markdown = """# Headline 1

- Test List

  > 1) Test1
  > 2) Test2

  <!-- this is html-->
"""

    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):Headline 1: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[ulist(3,1):-::2::\n\n  \n]",
        "[para(3,3):]",
        "[text(3,3):Test List:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[block-quote(5,3):  :  > \n  > ]",
        "[olist(5,5):):1:7:]",
        "[para(5,8):]",
        "[text(5,8):Test1:]",
        "[end-para:::True]",
        "[li(6,5):7::2]",
        "[para(6,8):]",
        "[text(6,8):Test2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[html-block(8,3)]",
        "[text(8,3):<!-- this is html-->:]",
        "[end-html-block:::False]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<h1>Headline 1</h1>
<ul>
<li>
<p>Test List</p>
<blockquote>
<ol>
<li>Test1</li>
<li>Test2</li>
</ol>
</blockquote>
<!-- this is html-->
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
