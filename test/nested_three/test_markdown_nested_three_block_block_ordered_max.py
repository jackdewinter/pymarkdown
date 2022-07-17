"""
Extra tests.
"""
from test.utils import act_and_assert

import pytest


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   :      ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
@pytest.mark.skip
def test_nested_three_block_max_block_max_ordered_max_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   :   ]",
        "[para(1,17):\n   ]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > ]",
        "[olist(1,14):.:1:16:   :   ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :   ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :\n]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    >    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
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
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list</li>
<li>item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_with_li_and_nl():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    >    1. item
                again"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > \n]",
        "[olist(1,14):.:1:16:   :                ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[li(2,14):16:   :1]",
        "[para(2,17):\n]",
        "[text(2,17):item\nagain::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list</li>
<li>item
again</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_with_li_and_nl_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    >    1. item
             again"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > \n]",
        "[olist(1,14):.:1:16:   :             ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[li(2,14):16:   :1]",
        "[para(2,17):\n]",
        "[text(2,17):item\nagain::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list</li>
<li>item
again</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_with_li_and_nl_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    >    1. item
        again"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > \n]",
        "[olist(1,14):.:1:16:   :        ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[li(2,14):16:   :1]",
        "[para(2,17):\n]",
        "[text(2,17):item\nagain::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list</li>
<li>item
again</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_with_li_and_nl_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    >    1. item
   again"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > \n]",
        "[olist(1,14):.:1:16:   :   ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[li(2,14):16:   :1]",
        "[para(2,17):\n]",
        "[text(2,17):item\nagain::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list</li>
<li>item
again</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_with_li_and_nl_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    >    1. item
again"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > \n]",
        "[olist(1,14):.:1:16:   :\n]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[li(2,14):16:   :1]",
        "[para(2,17):\n]",
        "[text(2,17):item\nagain::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list</li>
<li>item
again</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   :      ]",
        "[BLANK(1,16):]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_drop_ordered_x():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   :   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[para(2,14):   ]",
        "[text(2,14):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_drop_ordered_no_item_indent():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    > item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[end-olist:::False]",
        "[BLANK(1,16):]",
        "[para(2,11):]",
        "[text(2,11):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
<p>item</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[para(2,9):   ]",
        "[text(2,9):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<p>item</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1.
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >    1.
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    >    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[li(2,14):16:   :1]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
<li>item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_with_li_and_nl():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    >    1. item
                list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > \n]",
        "[olist(1,14):.:1:16:   :                ]",
        "[BLANK(1,16):]",
        "[li(2,14):16:   :1]",
        "[para(2,17):\n]",
        "[text(2,17):item\nlist::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
<li>item
list</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_with_li_and_nl_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    >    1. item
             list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > \n]",
        "[olist(1,14):.:1:16:   :             ]",
        "[BLANK(1,16):]",
        "[li(2,14):16:   :1]",
        "[para(2,17):\n]",
        "[text(2,17):item\nlist::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
<li>item
list</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_with_li_and_nl_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    >    1. item
        list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > \n]",
        "[olist(1,14):.:1:16:   :        ]",
        "[BLANK(1,16):]",
        "[li(2,14):16:   :1]",
        "[para(2,17):\n]",
        "[text(2,17):item\nlist::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
<li>item
list</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_with_li_and_nl_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    >    1. item
   list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > \n]",
        "[olist(1,14):.:1:16:   :   ]",
        "[BLANK(1,16):]",
        "[li(2,14):16:   :1]",
        "[para(2,17):\n]",
        "[text(2,17):item\nlist::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
<li>item
list</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_with_li_and_nl_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, and
    no text on the first line, with
    the maximum number of spaces allowed works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    >    1. item
list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > \n]",
        "[olist(1,14):.:1:16:   :\n]",
        "[BLANK(1,16):]",
        "[li(2,14):16:   :1]",
        "[para(2,17):\n]",
        "[text(2,17):item\nlist::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
<li>item
list</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :        ]",
        "[para(1,17):\n]",
        "[text(1,17):list\n\a>\a&gt;\a       item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
&gt;       item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :        ]",
        "[para(1,17):\n]",
        "[text(1,17):list\n\a>\a&gt;\a    item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
&gt;    item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :        ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :   ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq1_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :\n]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq1_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        >    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :        ]",
        "[para(1,17):\n]",
        "[text(1,17):list\n\a>\a&gt;\a    1. item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
&gt;    1. item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq1_with_li_and_nl():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        >    1. item
                another"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n\n]",
        "[olist(1,14):.:1:16:   :        \n                ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n\a>\a&gt;\a    1. item\nanother::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
&gt;    1. item
another</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq1_with_li_and_nl_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        >    1. item
             another"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n\n]",
        "[olist(1,14):.:1:16:   :        \n             ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n\a>\a&gt;\a    1. item\nanother::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
&gt;    1. item
another</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq1_with_li_and_nl_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        >    1. item
        another"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n\n]",
        "[olist(1,14):.:1:16:   :        \n        ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n\a>\a&gt;\a    1. item\nanother::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
&gt;    1. item
another</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq1_with_li_and_nl_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        >    1. item
   another"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n\n]",
        "[olist(1,14):.:1:16:   :        \n   ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n\a>\a&gt;\a    1. item\nanother::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
&gt;    1. item
another</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq1_with_li_and_nl_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        >    1. item
   another"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n\n]",
        "[olist(1,14):.:1:16:   :        \n   ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n\a>\a&gt;\a    1. item\nanother::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
&gt;    1. item
another</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
        >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a       item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    &gt;       item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
        >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a    item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    &gt;    item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
        item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
        >    1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a    1. item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    &gt;    1. item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1_with_li_and_nl():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
        >    1. item
                list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :\n    ]",
        "[text(2,5):\a>\a&gt;\a    1. item\n            list:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    &gt;    1. item
            list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1_with_li_and_nl_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
        >    1. item
             list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :\n    ]",
        "[text(2,5):\a>\a&gt;\a    1. item\n         list:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    &gt;    1. item
         list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1_with_li_and_nl_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
        >    1. item
        list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :\n    ]",
        "[text(2,5):\a>\a&gt;\a    1. item\n    list:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    &gt;    1. item
    list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1_with_li_and_nl_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
        >    1. item
   list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a    1. item:    ]",
        "[end-icode-block:::False]",
        "[para(3,4):   ]",
        "[text(3,4):list:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    &gt;    1. item
</code></pre>
<p>list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq1_with_li_and_nl_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
        >    1. item
list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a    1. item:    ]",
        "[end-icode-block:::False]",
        "[para(3,1):]",
        "[text(3,1):list:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    &gt;    1. item
</code></pre>
<p>list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > ]",
        "[olist(1,14):.:1:16:   :           ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >         item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > ]",
        "[olist(1,14):.:1:16:   :        ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > ]",
        "[olist(1,14):.:1:16:   :   ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :   ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq2_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :\n]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq2_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >         1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > ]",
        "[olist(1,14):.:1:16:   :        ]",
        "[para(1,17):\n]",
        "[text(1,17):list\n1. item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq2_with_li_and_nl():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >         1. item
                redux"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > \n]",
        "[olist(1,14):.:1:16:   :        \n                ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n1. item\nredux::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item
redux</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq2_with_li_and_nl_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >         1. item
             redux"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > \n]",
        "[olist(1,14):.:1:16:   :        \n             ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n1. item\nredux::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item
redux</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq2_with_li_and_nl_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >         1. item
        redux"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > \n]",
        "[olist(1,14):.:1:16:   :        \n        ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n1. item\nredux::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item
redux</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq2_with_li_and_nl_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >         1. item
   redux"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > \n]",
        "[olist(1,14):.:1:16:   :        \n   ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n1. item\nredux::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item
redux</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq2_with_li_and_nl_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   >         1. item
redux"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   > \n]",
        "[olist(1,14):.:1:16:   :        \n\n]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n1. item\nredux::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item
redux</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:       ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>       item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >         item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:    ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>    item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[para(2,9):   ]",
        "[text(2,9):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<p>item</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >         1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:    ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>    1. item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2_with_li_and_nl():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >         1. item
                list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:    ]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):list:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>    1. item
</code></pre>
</blockquote>
<pre><code>            list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2_with_li_and_nl_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >         1. item
             list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:    ]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):list:         ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>    1. item
</code></pre>
</blockquote>
<pre><code>         list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2_with_li_and_nl_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >         1. item
        list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:    ]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):list:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>    1. item
</code></pre>
</blockquote>
<pre><code>    list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2_with_li_and_nl_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >         1. item
   list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:    ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(3,4):   ]",
        "[text(3,4):list:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>    1. item
</code></pre>
</blockquote>
<p>list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq2_with_li_and_nl_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
   >         1. item
list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):1. item:    ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(3,1):]",
        "[text(3,1):list:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
<pre><code>    1. item
</code></pre>
</blockquote>
<p>list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :                ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :             ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
        item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :        ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :   ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq3_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :\n]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
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
def test_nested_three_block_max_block_max_ordered_max_no_bq3_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
             1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n]",
        "[olist(1,14):.:1:16:   :             ]",
        "[para(1,17):\n]",
        "[text(1,17):list\n1. item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq3_with_li_and_nl():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
             1. item
                redux"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n\n]",
        "[olist(1,14):.:1:16:   :             \n                ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n1. item\nredux::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item
redux</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq3_with_li_and_nl_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
             1. item
             redux"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n\n]",
        "[olist(1,14):.:1:16:   :             \n             ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n1. item\nredux::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item
redux</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq3_with_li_and_nl_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
             1. item
        redux"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n\n]",
        "[olist(1,14):.:1:16:   :             \n        ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n1. item\nredux::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item
redux</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq3_with_li_and_nl_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
             1. item
   redux"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n\n]",
        "[olist(1,14):.:1:16:   :             \n   ]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n1. item\nredux::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item
redux</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_no_bq3_with_li_and_nl_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1. list
             1. item
redux"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n\n]",
        "[olist(1,14):.:1:16:   :             \n\n]",
        "[para(1,17):\n\n]",
        "[text(1,17):list\n1. item\nredux::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
1. item
redux</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>         item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
        item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>    item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >    1.
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3_with_li():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
             1. item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):1. item:         ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>         1. item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3_with_li_and_nl():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
             1. item
                list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :\n    ]",
        "[text(2,5):1. item\n            list:         ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>         1. item
            list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3_with_li_and_nl_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
             1. item
             list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :\n    ]",
        "[text(2,5):1. item\n         list:         ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>         1. item
         list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3_with_li_and_nl_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
             1. item
        list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :\n    ]",
        "[text(2,5):1. item\n    list:         ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>         1. item
    list
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3_with_li_and_nl_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
             1. item
   list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):1. item:         ]",
        "[end-icode-block:::False]",
        "[para(3,4):   ]",
        "[text(3,4):list:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>         1. item
</code></pre>
<p>list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_empty_no_bq3_with_li_and_nl_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces allowed works properly, and no text on the first line,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    >    1.
             1. item
list"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[olist(1,14):.:1:16:   ]",
        "[BLANK(1,16):]",
        "[end-olist:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):1. item:         ]",
        "[end-icode-block:::False]",
        "[para(3,1):]",
        "[text(3,1):list:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li></li>
</ol>
</blockquote>
</blockquote>
<pre><code>         1. item
</code></pre>
<p>list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    >    >       item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n\a>\a&gt;\a    \a>\a&gt;\a       item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
&gt;    &gt;       item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    >    >    item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n\a>\a&gt;\a    \a>\a&gt;\a    item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
&gt;    &gt;    item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    >    item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n\a>\a&gt;\a    item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
&gt;    item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\nitem:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly.
    """

    # Arrange
    source_markdown = """    >    >    1. list
item"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
</code></pre>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
         >       item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n     \a>\a&gt;\a       item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
     &gt;       item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
         >    item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n     \a>\a&gt;\a    item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
     &gt;    item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
         item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n     item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
     item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\nitem:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq1_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
item"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
</code></pre>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    >            item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n\a>\a&gt;\a            item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
&gt;            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    >         item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n\a>\a&gt;\a         item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
&gt;         item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    >    item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n\a>\a&gt;\a    item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
&gt;    item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\nitem:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq2_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
item"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
</code></pre>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
                 item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n             item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
              item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n          item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
          item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
         item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\n     item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
     item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
    item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list\nitem:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_block_max_ordered_max_no_bq3_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the first) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    >    1. list
item"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):\a>\a&gt;\a    \a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    &gt;    1. list
</code></pre>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   >     >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    1. list\n\a>\a&gt;\a       item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
&gt;       item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   >     >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    1. list\n\a>\a&gt;\a    item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
&gt;    item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   >     item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    1. list\nitem:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    1. list
         >       item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a       item:     ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<pre><code>     &gt;       item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    1. list
         >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a    item:     ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<pre><code>     &gt;    item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    1. list
         item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:     ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<pre><code>     item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq1_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     >    1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    1. list\n        item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
        item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   >          item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    1. list\n     item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
     item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   >     item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):\a>\a&gt;\a    1. list\nitem:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq2_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:             ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<pre><code>             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
              item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:          ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<pre><code>          item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
         item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:     ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<pre><code>     item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_plus_one_ordered_max_no_bq3_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the second) allowed works properly.
    """

    # Arrange
    source_markdown = """   >     >    1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):\a>\a&gt;\a    1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;    1. list
</code></pre>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   >    >        item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):1. list\n   item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
   item
</code></pre>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   >    >     item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):1. list\nitem:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
item
</code></pre>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,9):   ]",
        "[text(2,9):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
<p>item</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly.
    """

    # Arrange
    source_markdown = """   >    >     1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq1():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
        >        item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a        item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<pre><code>    &gt;        item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq1_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
        >     item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):\a>\a&gt;\a     item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<pre><code>    &gt;     item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq1_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
        item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<pre><code>    item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq1_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq1_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq2():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   >             item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:        ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
<pre><code>        item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq2_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   >          item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,10):    :]",
        "[text(2,10):item:     ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
<pre><code>     item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq2_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,9):   ]",
        "[text(2,9):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
<p>item</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq2_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq2_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq3():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
                 item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:             ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<pre><code>             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq3_drop_ordered():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
              item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:          ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<pre><code>          item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq3_drop_ordered_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
        item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<pre><code>    item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq3_drop_ordered_block_block():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,4):   ]",
        "[text(2,4):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_block_max_ordered_max_plus_one_no_bq3_drop_ordered_block_block_all():
    """
    Verify that a nesting of block quote, block quote, ordered list, with
    the maximum number of spaces (plus one for the third) allowed works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    >     1. list
item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):1. list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):item:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1. list
</code></pre>
</blockquote>
</blockquote>
<p>item</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
