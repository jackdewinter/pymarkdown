"""
Extra tests for three level nesting with un/un.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


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
