"""
Extra tests for three level nesting with un/un.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


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
def test_nested_three_unordered_max_unordered_max_block_max_empty_no_bq1_x():
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
        "[ulist(1,9):+::13:        :             ]",
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


@pytest.mark.gfm
def test_nested_three_unordered_unordered_block_nl_extra_block_drop_block_thematics_around_fenced():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    a new line, extra block quote, drop that block quote, and then thematics
    around a fenced code block.

    was: test_extra_044lc
    refs: bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_and_thematics
    """
    # Arrange
    source_markdown = """+ + > -----
    > > block 1
    > > block 2
    > -----
    > ```block
    > A code block
    > ```
    > -----
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n\n\n\n\n\n\n]",
        "[block-quote(1,5):    :    > \n    > \n    > \n    > \n    > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,5):    :    > > \n    > > \n    > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::    > :True]",
        "[tbreak(4,7):-::-----]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(9,3):4:  :]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_unordered_nl_block_drop_block_fenced():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    drop that block quote, and then a fenced code block.

    was: test_extra_044mcr0
    refs: bad_fenced_block_in_list_in_list_with_previous_inner_block
    """

    # Arrange
    source_markdown = """+ + list 1
    > block 2.1
    > block 2.2
    ```block
    A code block
    ```
  + another list"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n\n    \n    \n    ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5):    :    > \n    > ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2.1\nblock 2.2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(7,3):4:  :]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>list 1
<blockquote>
<p>block 2.1
block 2.2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_unordered_nl_block_drop_block_with_blanks_around_fenced():
    """
    Verify that a nesting of unordered list, unordered list, block quote, with
    drop that block quote, and then blanks around a fenced code block.

    was: test_extra_044mcr1
    refs: bad_fenced_block_in_list_in_list_with_previous_inner_block
    """
    # Arrange
    source_markdown = """+ + list 1
    > block 2.1
    > block 2.2

    ```block
    A code block
    ```

  + another list"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n\n\n    \n    \n    \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5):    :    > \n    > \n]",
        "[para(2,7):\n]",
        "[text(2,7):block 2.1\nblock 2.2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[li(9,3):4:  :]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<p>list 1</p>
<blockquote>
<p>block 2.1
block 2.2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>
<p>another list</p>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
