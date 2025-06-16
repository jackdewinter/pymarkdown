"""
Extra tests for three level nesting with un/or.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_unordered_ordered_ordered() -> None:
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
def test_nested_three_unordered_nl_ordered_nl_ordered() -> None:
    """
    Verify that a nesting of unordered list, new line, ordered list, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+
  1.
     1. list
        item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5:  ]",
        "[BLANK(2,5):]",
        "[olist(3,6):.:1:8:     :        ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
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
def test_nested_three_unordered_text_nl_ordered_text_nl_ordered() -> None:
    """
    Verify that a nesting of unordered list, text, new line, ordered list, text, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """+ abc
  1. def
     1. list
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
        "[olist(3,6):.:1:8:     :        ]",
        "[para(3,9):\n]",
        "[text(3,9):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
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
def test_nested_three_unordered_max_ordered_max_ordered_max() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    1.    1. list
                 item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              :                 ]",
        "[para(1,18):\n]",
        "[text(1,18):list\nitem::\n]",
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
def test_nested_three_unordered_max_ordered_max_ordered_max_with_li1() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1. list
   +             item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:        ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ol>
<li>list</li>
</ol>
</li>
</ol>
</li>
<li>
<pre><code>        item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_with_li2() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1. list
        1.       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(2,9):11:        :1]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ol>
<li>list</li>
</ol>
</li>
<li>
<pre><code>  item
</code></pre>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_with_li3() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1. list
              1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[li(2,15):17:              :1]",
        "[para(2,18):]",
        "[text(2,18):item:]",
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
<li>list</li>
<li>item</li>
</ol>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_with_li4() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1. list
        1.    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(2,9):14:        :1]",
        "[olist(2,15):.:1:17:              ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
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
<li>list</li>
</ol>
</li>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_with_li5() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1. list
   +          1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:     ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ol>
<li>list</li>
</ol>
</li>
</ol>
</li>
<li>
<pre><code>     1. item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_with_li6() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1. list
   +    1.       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):8:   :]",
        "[olist(2,9):.:1:11:        ]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ol>
<li>list</li>
</ol>
</li>
</ol>
</li>
<li>
<ol>
<li>
<pre><code>  item
</code></pre>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_with_li7() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1. list
   +    1.    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[para(1,18):]",
        "[text(1,18):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):8:   :]",
        "[olist(2,9):.:1:14:        ]",
        "[olist(2,15):.:1:17:              ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
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
<li>list</li>
</ol>
</li>
</ol>
</li>
<li>
<ol>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_empty() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   +    1.    1.
                 item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              :                 ]",
        "[BLANK(1,17):]",
        "[para(2,18):]",
        "[text(2,18):item:]",
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
<li>item</li>
</ol>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_empty_with_li1() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1.
   +             item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[BLANK(1,17):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:        ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
</li>
<li>
<pre><code>        item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_empty_with_li2() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1.
        1.       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[BLANK(1,17):]",
        "[end-olist:::True]",
        "[li(2,9):11:        :1]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ol>
<li></li>
</ol>
</li>
<li>
<pre><code>  item
</code></pre>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_empty_with_li3() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1.
              1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[BLANK(1,17):]",
        "[li(2,15):17:              :1]",
        "[para(2,18):]",
        "[text(2,18):item:]",
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
<li></li>
<li>item</li>
</ol>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_empty_with_li4() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1.
        1.    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[BLANK(1,17):]",
        "[end-olist:::True]",
        "[li(2,9):14:        :1]",
        "[olist(2,15):.:1:17:              ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
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
<li></li>
</ol>
</li>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_empty_with_li5() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1.
   +          1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[BLANK(1,17):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):5:   :]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:     ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
</li>
<li>
<pre><code>     1. item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_empty_with_li6() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1.
   +    1.       item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[BLANK(1,17):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):8:   :]",
        "[olist(2,9):.:1:11:        ]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
</li>
<li>
<ol>
<li>
<pre><code>  item
</code></pre>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_empty_with_li7() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   +    1.    1.
   +    1.    1. item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:14:        ]",
        "[olist(1,15):.:1:17:              ]",
        "[BLANK(1,17):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):8:   :]",
        "[olist(2,9):.:1:14:        ]",
        "[olist(2,15):.:1:17:              ]",
        "[para(2,18):]",
        "[text(2,18):item:]",
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
<li></li>
</ol>
</li>
</ol>
</li>
<li>
<ol>
<li>
<ol>
<li>item</li>
</ol>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_plus_one_ordered_max_ordered_max() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    +    1.    1.  list
                   item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):+    1.    1.  list\n               item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>+    1.    1.  list
               item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_plus_one_ordered_max() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +     1.    1. list
                  item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   :     ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):1.    1. list\n         item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>1.    1. list
         item
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_unordered_max_ordered_max_ordered_max_plus_one() -> None:
    """
    Verify that a nesting of unordered list, ordered list, ordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   +    1.     1. list
                  item"""
    expected_tokens = [
        "[ulist(1,4):+::8:   ]",
        "[olist(1,9):.:1:11:        :           ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):1. list\n   item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<pre><code>1. list
   item
</code></pre>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
