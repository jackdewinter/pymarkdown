"""
Extra tests for three level nesting with un/un.
"""

from test.utils import act_and_assert

import pytest


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_nested_three_ordered_ordered_ordered() -> None:
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
def test_nested_three_ordered_nl_ordered_nl_ordered() -> None:
    """
    Verify that a nesting of ordered list, new line, ordered list, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1.
   1.
      1. list
         item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[olist(3,7):.:1:9:      :         ]",
        "[para(3,10):\n]",
        "[text(3,10):list\nitem::\n]",
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
def test_nested_three_ordered_text_nl_ordered_text_nl_ordered() -> None:
    """
    Verify that a nesting of ordered list, text, new line, ordered list, text, new line, ordered list works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
      1. list
         item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[olist(3,7):.:1:9:      :         ]",
        "[para(3,10):\n]",
        "[text(3,10):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    1.    1. list
                  item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               :                  ]",
        "[para(1,19):\n]",
        "[text(1,19):list\nitem::\n]",
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
def test_nested_three_ordered_max_ordered_max_ordered_max_with_li1() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1. list
   1.             item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[para(1,19):]",
        "[text(1,19):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):item:        ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_with_li2() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1. list
         1.       item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[para(1,19):]",
        "[text(1,19):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(2,10):12:         :1]",
        "[icode-block(2,17):    :]",
        "[text(2,17):item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_with_li3() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1. list
               1. item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[para(1,19):]",
        "[text(1,19):list:]",
        "[end-para:::True]",
        "[li(2,16):18:               :1]",
        "[para(2,19):]",
        "[text(2,19):item:]",
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
<li>list</li>
<li>item</li>
</ol>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_with_li4() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1. list
         1.    1. item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[para(1,19):]",
        "[text(1,19):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(2,10):15:         :1]",
        "[olist(2,16):.:1:18:               ]",
        "[para(2,19):]",
        "[text(2,19):item:]",
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_with_li5() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1. list
   1.          1. item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[para(1,19):]",
        "[text(1,19):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):1. item:     ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_with_li6() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1. list
   1.    1.       item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[para(1,19):]",
        "[text(1,19):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):9:   :1]",
        "[olist(2,10):.:1:12:         ]",
        "[icode-block(2,17):    :]",
        "[text(2,17):item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_with_li7() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1. list
   1.    1.    1. item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[para(1,19):]",
        "[text(1,19):list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):9:   :1]",
        "[olist(2,10):.:1:15:         ]",
        "[olist(2,16):.:1:18:               ]",
        "[para(2,19):]",
        "[text(2,19):item:]",
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_empty() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   1.    1.    1.
                  item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               :                  ]",
        "[BLANK(1,18):]",
        "[para(2,19):]",
        "[text(2,19):item:]",
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
<li>item</li>
</ol>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_empty_with_li1() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1.
   1.             item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[BLANK(1,18):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):item:        ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_empty_with_li2() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1.
         1.       item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[BLANK(1,18):]",
        "[end-olist:::True]",
        "[li(2,10):12:         :1]",
        "[icode-block(2,17):    :]",
        "[text(2,17):item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_empty_with_li3() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1.
               1. item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[BLANK(1,18):]",
        "[li(2,16):18:               :1]",
        "[para(2,19):]",
        "[text(2,19):item:]",
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
<li></li>
<li>item</li>
</ol>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_empty_with_li4() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1.
         1.    1. item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[BLANK(1,18):]",
        "[end-olist:::True]",
        "[li(2,10):15:         :1]",
        "[olist(2,16):.:1:18:               ]",
        "[para(2,19):]",
        "[text(2,19):item:]",
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_empty_with_li5() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1.
   1.          1. item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[BLANK(1,18):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):1. item:     ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_empty_with_li6() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1.
   1.    1.       item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[BLANK(1,18):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):9:   :1]",
        "[olist(2,10):.:1:12:         ]",
        "[icode-block(2,17):    :]",
        "[text(2,17):item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_empty_with_li7() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    1.    1.
   1.    1.    1. item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:15:         ]",
        "[olist(1,16):.:1:18:               ]",
        "[BLANK(1,18):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[li(2,4):9:   :1]",
        "[olist(2,10):.:1:15:         ]",
        "[olist(2,16):.:1:18:               ]",
        "[para(2,19):]",
        "[text(2,19):item:]",
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
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_ordered_max_ordered_max() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    1.    1.    1.  list
                    item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    1.    1.  list\n                item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    1.    1.  list
                item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_plus_one_ordered_max() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.     1.    1. list
                   item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):1.    1. list\n         item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>1.    1. list
         item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_ordered_max_ordered_max_plus_one() -> None:
    """
    Verify that a nesting of ordered list, ordered list, ordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    1.     1. list
                   item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[olist(1,10):.:1:12:         :            ]",
        "[icode-block(1,17):    :\n    ]",
        "[text(1,17):1. list\n   item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<pre><code>1. list
   item
</code></pre>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
