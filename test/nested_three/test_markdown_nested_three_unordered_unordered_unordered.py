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
def test_nested_three_unordered_unordered_unordered_nl_list_with_li_drop_list_with_thematics_around_fenced():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    a new line and a new unordered list, a list item, then drop the list, and then
    thematics arounds a fenced block.

    was: test_extra_044mcq0
    refs: bad_fenced_block_in_list_in_list_in_list_with_previous_list_0
    """
    # Arrange
    source_markdown = """+ + + -----
      + list 1
        list 2
      + list 3
      -----
      ```block
      A code block
      ```
      -----
  + another list"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :      \n      \n      \n      \n      ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:      :        ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:      :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(5,7):-::-----]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-ulist:::True]",
        "[li(10,3):4:  :]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_unordered_unordered_nl_list_with_li_drop_list_with_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    a new line and a new unordered list, a list item, then drop the list, and then
    thematics arounds blanks around a fenced block.

    was: test_extra_044mcq1
    refs: bad_fenced_block_in_list_in_list_in_list_with_previous_list_0
    """
    # Arrange
    source_markdown = """+ + + -----
      + list 1
        list 2
      + list 3
      -----

      ```block
      A code block
      ```

      -----
  + another list"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :      \n\n      \n      \n      \n\n      ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:      :        ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:      :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(5,7):-::-----]",
        "[BLANK(6,1):]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,1):]",
        "[tbreak(11,7):-::-----]",
        "[end-ulist:::True]",
        "[li(12,3):4:  :]",
        "[para(12,5):]",
        "[text(12,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_unordered_nl_unordered_drop_list_with_fenced():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    a new line and a new unordered list, a list item, then drop the list, and then
    thematics arounds blanks around a fenced block.

    was: test_extra_047a0
    refs: bad_fenced_block_in_list_in_list_with_previous_inner_listx
    """
    # Arrange
    source_markdown = """+ + list 1
+ + + list 2.1
      list 2.2
    ```block
    A code block
    ```
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,1):2::]",
        "[ulist(2,3):+::4:  :    \n    \n    \n]",
        "[ulist(2,5):+::6:    :      ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2.1\nlist 2.2::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(7,3):4:  :]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>list 1</li>
</ul>
</li>
<li>
<ul>
<li>
<ul>
<li>list 2.1
list 2.2</li>
</ul>
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
def test_nested_three_unordered_unordered_nl_unordered_drop_list_with_blanks_around_fenced():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    a new line and a new unordered list, a list item, then drop the list, and then
    thematics arounds blanks around a fenced block.

    was: test_extra_044b, test_extra_047a1
    refs: bad_fenced_block_in_list_in_list_with_previous_inner_listx
    """
    # Arrange
    source_markdown = """+ + list 1
+ + + list 2.1
      list 2.2

    ```block
    A code block
    ```

  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,1):2::]",
        "[ulist(2,3):+::4:  :    \n    \n    \n\n]",
        "[ulist(2,5):+::6:    :      \n]",
        "[para(2,7):\n]",
        "[text(2,7):list 2.1\nlist 2.2::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
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
<li>list 1</li>
</ul>
</li>
<li>
<ul>
<li>
<ul>
<li>list 2.1
list 2.2</li>
</ul>
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


@pytest.mark.gfm
def test_nested_three_unordered_unordered_nl_li_li_unordered_drop_list_with_thematics_then_fenced():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    a new line and a new unordered list, a list item, then drop the list, and then
    thematics arounds blanks around a fenced block.

    was: test_extra_047g0
    refs: bad_fenced_block_in_list_in_list_with_previous_inner_list_with_thematics
    """
    # Arrange
    source_markdown = """+ + list 1
+ + + list 2.1
      list 2.2
    ----
    ```block
    A code block
    ```
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,1):2::]",
        "[ulist(2,3):+::4:  :    \n    \n    \n    \n]",
        "[ulist(2,5):+::6:    :      ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2.1\nlist 2.2::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::----]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(8,3):4:  :]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>list 1</li>
</ul>
</li>
<li>
<ul>
<li>
<ul>
<li>list 2.1
list 2.2</li>
</ul>
<hr />
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
def test_nested_three_unordered_unordered_nl_li_liunordered_drop_list_with_thematics_then_blanks_around_fenced():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    a new line and a new unordered list, a list item, then drop the list, and then
    thematics arounds blanks around a fenced block.

    was: test_extra_047g1
    refs: bad_fenced_block_in_list_in_list_with_previous_inner_list_with_thematics
    """
    # Arrange
    source_markdown = """+ + list 1
+ + + list 2.1
      list 2.2
    ----

    ```block
    A code block
    ```

  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,1):2::]",
        "[ulist(2,3):+::4:  :    \n\n    \n    \n    \n\n]",
        "[ulist(2,5):+::6:    :      ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2.1\nlist 2.2::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::----]",
        "[BLANK(5,1):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[li(10,3):4:  :]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>list 1</li>
</ul>
</li>
<li>
<ul>
<li>
<ul>
<li>list 2.1
list 2.2</li>
</ul>
<hr />
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


@pytest.mark.gfm
def test_nested_three_unordered_unordered_nl_unordered_drop_list_with_thematics_then_fenced():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    a new line and a new unordered list, a list item, then drop the list, and then
    thematics arounds blanks around a fenced block.

    was: test_extra_047g2
    refs: bad_fenced_block_in_list_in_list2_with_previous_inner_list_with_thematics
    """
    # Arrange
    source_markdown = """+ + list 1
    + list 2.1
      list 2.2
    ----
    ```block
    A code block
    ```
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n    \n    \n    \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:    :      ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2.1\nlist 2.2::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::----]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(8,3):4:  :]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>list 1
<ul>
<li>list 2.1
list 2.2</li>
</ul>
<hr />
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
def test_nested_three_unordered_unordered_nl_unordered_drop_list_with_thematics_then_blanks_around_fenced():
    """
    Verify that a nesting of unordered list, unordered list, unordered list, with
    a new line and a new unordered list, a list item, then drop the list, and then
    thematics arounds blanks around a fenced block.

    was: test_extra_047g3
    refs: bad_fenced_block_in_list_in_list2_with_previous_inner_list_with_thematics
    """
    # Arrange
    source_markdown = """+ + list 1
    + list 2.1
      list 2.2
    ----

    ```block
    A code block
    ```

  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n\n    \n    \n    \n\n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:    :      ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2.1\nlist 2.2::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::----]",
        "[BLANK(5,1):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[li(10,3):4:  :]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2.1
list 2.2</li>
</ul>
<hr />
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
