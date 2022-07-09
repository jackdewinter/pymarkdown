"""
Extra tests for three level nesting with un/or.
"""
from test.utils import act_and_assert

import pytest

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
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:  ]",
        "[BLANK(2,5):]",
        "[ulist(3,6):+::7:     :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
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
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5:  ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[ulist(3,6):+::7:     :       ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
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
def test_nested_three_unordered_max_ordered_max_unordered_max():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    1.    + list
                item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              :                ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_unordered_max_ordered_max_unordered_max_with_li1():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    + list
   +            item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:       ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ul>
<li>list</li>
</ul>
</li>
</ol>
</li>
<li>
<pre><code>       item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_with_li2():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    + list
        1.      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,9):11:        :1]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ul>
<li>list</li>
</ul>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_with_li3():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    + list
              + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[li(2,15):16:              :]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li>list</li>
<li>item</li>
</ul>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_with_li4():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    + list
        1.    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,9):14:        :1]",
        "[ulist(2,15):+::16:              ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li>list</li>
</ul>
</li>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_with_li5():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    + list
   +          + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):+ item:     ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ul>
<li>list</li>
</ul>
</li>
</ol>
</li>
<li>
<pre><code>     + item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_with_li6():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    + list
   +    1.      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[li(2,4):8:   :]",
        "[olist(2,9):.:1:11:        ]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ul>
<li>list</li>
</ul>
</li>
</ol>
</li>
<li>
<ol>
<li>
<pre><code> item
</code></pre>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_with_li7():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    + list
   +    1.    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[li(2,4):8:   :]",
        "[olist(2,9):.:1:14:        ]",
        "[ulist(2,15):+::16:              ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li>list</li>
</ul>
</li>
</ol>
</li>
<li>
<ol>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_empty():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   +    1.    +
                item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              :                ]",
        "[BLANK(1,16):]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li>item</li>
</ul>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_empty_wih_li1():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    +
   +            item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:       ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ul>
<li></li>
</ul>
</li>
</ol>
</li>
<li>
<pre><code>       item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_empty_wih_li2():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    +
        1.      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[li(2,9):11:        :1]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ul>
<li></li>
</ul>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_empty_wih_li3():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    +
              + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[BLANK(1,16):]",
        "[li(2,15):16:              :]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li></li>
<li>item</li>
</ul>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_empty_wih_li4():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    +
        1.    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[li(2,9):14:        :1]",
        "[ulist(2,15):+::16:              ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li></li>
</ul>
</li>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_empty_wih_li5():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    +
   +          + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):+ item:     ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ul>
<li></li>
</ul>
</li>
</ol>
</li>
<li>
<pre><code>     + item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_empty_wih_li6():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    +
   +    1.      item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[li(2,4):8:   :]",
        "[olist(2,9):.:1:11:        ]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ul>
<li></li>
</ul>
</li>
</ol>
</li>
<li>
<ol>
<li>
<pre><code> item
</code></pre>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_empty_wih_li7():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    +
   +    1.    + item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[ulist(1,15):+::16:              ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[li(2,4):8:   :]",
        "[olist(2,9):.:1:14:        ]",
        "[ulist(2,15):+::16:              ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
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
<li></li>
</ul>
</li>
</ol>
</li>
<li>
<ol>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_ordered_max_unordered_max():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    +    1.    + list
                 item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    1.    + list\n             item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    1.    + list
             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_plus_one_unordered_max():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +     1.    + list
                 item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   :     ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):1.    + list\n        item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>1.    + list
        item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_unordered_max_plus_one():
    """
    Verify that a nesting of unordered list, ordered list, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    1.     + list
                 item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:11:        :           ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):+ list\n  item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<pre><code>+ list
  item
</code></pre>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
