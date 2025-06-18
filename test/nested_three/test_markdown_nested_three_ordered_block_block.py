"""
Extra tests for three level nesting with un/or.
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_ordered_block_block_x() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. > > list
   > > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_block_x() -> None:
    """
    Verify that a nesting of ordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > > list
   > > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[block-quote(3,4):   :   > > \n   > > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_block_wo_bq() -> None:
    """
    Verify that a nesting of ordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     > list
   > > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n     > ]",
        "[BLANK(2,5):]",
        "[para(3,8):]",
        "[text(3,8):list:]",
        "[end-para:::True]",
        "[block-quote(4,4):   :   > > ]",
        "[para(4,8):]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_block_x() -> None:
    """
    Verify that a nesting of ordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > > list
   > > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,4):   :   > > \n   > > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_block_wo_bq() -> None:
    """
    Verify that a nesting of ordered list, new line, block quote, new line, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     > list
   > > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n     > ]",
        "[para(2,6):\n]",
        "[text(2,6):def\nlist::\n]",
        "[end-para:::True]",
        "[block-quote(4,4):   :   > > ]",
        "[para(4,8):]",
        "[text(4,8):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def
list</p>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_skip_block_x() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. > > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n     > ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_block() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[block-quote(3,4):   :   > > \n     > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_block_wo_bq() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n     > \n     > ]",
        "[BLANK(2,5):]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_block() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,4):   :   > > \n     > ]",
        "[para(3,8):\n]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_block_wo_bq() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     > list
     > item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n     > \n     > ]",
        "[para(2,6):\n\n]",
        "[text(2,6):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_skip() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. > > list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > ]",
        "[para(1,8):\n  ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_block_skip() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > > list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[block-quote(3,4):   :   > > \n   > ]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_nl_block_skip_wo_bq() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
     > list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >\n     > \n   > ]",
        "[BLANK(2,5):]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_block_skip() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > > list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,4):   :   > > \n   > ]",
        "[para(3,8):\n  ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_text_nl_block_skip_wo_bq() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     > list
   >   item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n     > \n   > ]",
        "[para(2,6):\n\n  ]",
        "[text(2,6):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_skip_block_skip() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. > > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n]",
        "[para(1,8):\n    ]",
        "[text(1,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_block_skip_x() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   >
   > > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n   \n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[block-quote(3,4):   :   > > \n]",
        "[para(3,8):\n    ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_block_skip_1() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n   \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,4):   :   > > \n]",
        "[para(3,8):\n    ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_block_skip_2() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1.
   > def
   > > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n   \n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,4):   :   > > \n]",
        "[para(3,8):\n    ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_block_skip_3() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   >
   > > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n   \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   >]",
        "[BLANK(2,5):]",
        "[block-quote(3,4):   :   > > \n]",
        "[para(3,8):\n    ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_nl_block_skip_nl_block_skip_wo_bq() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n   \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n     > \n]",
        "[para(2,6):\n\n    ]",
        "[text(2,6):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_block_skip() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
   > > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n   \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > ]",
        "[para(2,6):]",
        "[text(2,6):def:]",
        "[end-para:::True]",
        "[block-quote(3,4):   :   > > \n]",
        "[para(3,8):\n    ]",
        "[text(3,8):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def</p>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_text_nl_block_skip_text_nl_block_skip_wo_bq() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote works
    properly.
    """

    # Arrange
    source_markdown = """1. abc
   > def
     > list
       item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n   \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[block-quote(2,4):   :   > \n     > \n]",
        "[para(2,6):\n\n    ]",
        "[text(2,6):def\nlist\nitem::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<blockquote>
<p>def
list
item</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    >    > list
         >    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > \n         >    > ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_with_li() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    > list
   1.    >    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):9:   :1]",
        "[block-quote(2,10):         :         > ]",
        "[block-quote(2,15)::         >    > ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list</p>
</blockquote>
</blockquote>
</li>
<li>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_empty() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   1.    >    >
         >    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    >\n         >    > ]",
        "[BLANK(1,16):]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_empty_with_li() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    >
   1.    >    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):9:   :1]",
        "[block-quote(2,10):         :         > ]",
        "[block-quote(2,15)::         >    > ]",
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</li>
<li>
<blockquote>
<blockquote>
<p>item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    > list
              > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         \n]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > \n]",
        "[para(1,17):\n     ]",
        "[text(1,17):list\n\a>\a&gt;\a item::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
&gt; item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_no_bq1_with_li() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    > list
   1.         > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):\a>\a&gt;\a item:    ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list</p>
</blockquote>
</blockquote>
</li>
<li>
<pre><code>    &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_empty_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    >
              > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):\a>\a&gt;\a item: ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code> &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_empty_no_bq1_with_li() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    >
   1.         > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):\a>\a&gt;\a item:    ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</li>
<li>
<pre><code>    &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_no_bq2() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    > list
         >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > \n         > ]",
        "[para(1,17):\n     ]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_no_bq2_with_li() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    > list
   1.    >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):9:   :1]",
        "[block-quote(2,10):         :         > ]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list</p>
</blockquote>
</blockquote>
</li>
<li>
<blockquote>
<pre><code> item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_empty_no_bq2() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    >
         >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[block-quote(1,15)::         >    >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
</blockquote>
<pre><code> item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_empty_no_bq2_with_li() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    >
         >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[block-quote(1,15)::         >    >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[icode-block(2,16):    :]",
        "[text(2,16):item: ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
</blockquote>
<pre><code> item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_no_bq3() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    > list
                item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         \n]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > \n]",
        "[para(1,17):\n       ]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list
item</p>
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_no_bq3_with_li() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    > list
   1.           item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    > ]",
        "[para(1,17):]",
        "[text(1,17):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):item:      ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>list</p>
</blockquote>
</blockquote>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_empty_no_bq3() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >    >
                item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):item:   ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
<pre><code>   item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_empty_no_bq3_with_li() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   1.    >    >
   1.           item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > ]",
        "[block-quote(1,15)::         >    >]",
        "[BLANK(1,16):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):6:   :1]",
        "[icode-block(2,11):    :]",
        "[text(2,11):item:      ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</li>
<li>
<pre><code>      item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_block_max() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    1.    >    > list
          >    > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    \a>\a&gt;\a list\n      \a>\a&gt;\a    \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    &gt; list
      &gt;    &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_block_max_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    1.    >    > list
               > item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    \a>\a&gt;\a list\n           \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    &gt; list
           &gt; item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_block_max_no_bq2() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    1.    >    > list
          >      item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    \a>\a&gt;\a list\n      \a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    &gt; list
      &gt;      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_plus_one_block_max_block_max_no_bq3() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    1.    >    > list
                 item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):1.    \a>\a&gt;\a    \a>\a&gt;\a list\n             item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.    &gt;    &gt; list
             item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_block_max() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.     >    > list
          >    > item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    \a>\a&gt;\a list\n\a>\a&gt;\a    \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    &gt; list
&gt;    &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_block_max_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.     >    > list
               > item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    \a>\a&gt;\a list\n     \a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    &gt; list
     &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_block_max_no_bq2() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.     >    > list
          >      item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    \a>\a&gt;\a list\n\a>\a&gt;\a      item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    &gt; list
&gt;      item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_plus_one_block_max_no_bq3() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.     >    > list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[icode-block(1,11):    :\n    ]",
        "[text(1,11):\a>\a&gt;\a    \a>\a&gt;\a list\n       item:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>&gt;    &gt; list
       item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_plus_one_x() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   1.    >     > list
         >     > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > \n         > \n]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):\a>\a&gt;\a list\n\a>\a&gt;\a item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>&gt; list
&gt; item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_plus_one_no_bq1() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >     > list
               > item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):\a>\a&gt;\a item:  ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
<pre><code>  &gt; item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_plus_one_no_bq2() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >     > list
         >       item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :]",
        "[block-quote(1,10):         :         > \n         > ]",
        "[icode-block(1,16):    :\n    ]",
        "[text(1,16):\a>\a&gt;\a list\n  item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>&gt; list
  item
</code></pre>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_max_block_max_block_max_plus_one_no_bq3() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   1.    >     > list
                 item"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   :         ]",
        "[block-quote(1,10):         :         > ]",
        "[icode-block(1,16):    :]",
        "[text(1,16):\a>\a&gt;\a list:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,14):    :]",
        "[text(2,14):item:    ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<pre><code>&gt; list
</code></pre>
</blockquote>
<pre><code>    item
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_drop_block_with_fenced() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046t0
    refs: bad_fenced_block_in_block_quote_in_list_with_previous_inner_block
    """
    # Arrange
    source_markdown = """1. > >
   > > block 3
   > > block 3
   > ```block
   > A code block
   > ```
   > --------
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n]",
        "[block-quote(1,6):   :   > >\n   > > \n   > > \n   > ]",
        "[BLANK(1,7):]",
        "[para(2,8):\n]",
        "[text(2,8):block 3\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[fcode-block(4,6):`:3:block:::::]",
        "[text(5,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,6):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>block 3
block 3</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_drop_block_with_blanks_aroundfenced() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046t1
    refs: bad_fenced_block_in_block_quote_in_list_with_previous_inner_block
    """
    # Arrange
    source_markdown = """1. > >
   > > block 3
   > > block 3
   >
   > ```block
   > A code block
   > ```
   >
   > --------
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   >\n   > \n]",
        "[block-quote(1,6):   :   > >\n   > > \n   > > \n   >]",
        "[BLANK(1,7):]",
        "[para(2,8):\n]",
        "[text(2,8):block 3\nblock 3::\n]",
        "[end-para:::True]",
        "[BLANK(4,5):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,6):`:3:block:::::]",
        "[text(6,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,5):]",
        "[tbreak(9,6):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>block 3
block 3</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_nl_extra_block_single_line_drop_block_with_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046s0
    refs: bad_fenced_block_in_block_quote_in_list_with_previous_inner_block_and_para_continue
    """
    # Arrange
    source_markdown = """1. > >
   > > block 3
   > block 3
   > ```block
   > A code block
   > ```
   > --------
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n]",
        "[block-quote(1,6):   :   > >\n   > > \n   > \n   > ]",
        "[BLANK(1,7):]",
        "[para(2,8):\n]",
        "[text(2,8):block 3\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[fcode-block(4,6):`:3:block:::::]",
        "[text(5,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,6):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>block 3
block 3</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_nl_extra_block_single_line_drop_block_with_blanks_around_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046s1
    refs: bad_fenced_block_in_block_quote_in_list_with_previous_inner_block_and_para_continue
    """
    # Arrange
    source_markdown = """1. > >
   > > block 3
   > block 3
   >
   > ```block
   > A code block
   > ```
   >
   > --------
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   >\n   > \n]",
        "[block-quote(1,6):   :   > >\n   > > \n   > \n   >]",
        "[BLANK(1,7):]",
        "[para(2,8):\n]",
        "[text(2,8):block 3\nblock 3::\n]",
        "[end-para:::True]",
        "[BLANK(4,5):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,6):`:3:block:::::]",
        "[text(6,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,5):]",
        "[tbreak(9,6):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>block 3
block 3</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_with_thematics_around_fenced() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046r0
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list
    """
    # Arrange
    source_markdown = """1. > > ----
   > > ```block
   > > A code block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[fcode-block(2,8):`:3:block:::::]",
        "[text(3,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(5,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_with_thematics_around_blanks_around_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046r1
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list
    """
    # Arrange
    source_markdown = """1. > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > >\n   > > \n   > > \n   > > \n   > >\n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[BLANK(2,7):]",
        "[fcode-block(3,8):`:3:block:::::]",
        "[text(4,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,7):]",
        "[tbreak(7,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_with_thematics_around_empty_fenced() -> None:
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046q0
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list_empty
    """
    # Arrange
    source_markdown = """1. > > ----
   > > ```block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[fcode-block(2,8):`:3:block:::::]",
        "[end-fcode-block:::3:False]",
        "[tbreak(4,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<pre><code class="language-block"></code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_with_thematics_around_blanks_around_empty_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046q1
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list_empty
    """
    # Arrange
    source_markdown = """1. > > ----
   > >
   > > ```block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > >\n   > > \n   > > \n   > >\n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[BLANK(2,7):]",
        "[fcode-block(3,8):`:3:block:::::]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,7):]",
        "[tbreak(6,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<pre><code class="language-block"></code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_nl_extra_block_drop_block_with_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046m0
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block
    """
    # Arrange
    source_markdown = """1. > > ----
   > > > inner block 1
   > > > inner block 2
   > > ```block
   > > A code block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,4):   :   > > > \n   > > > \n   > > ]",
        "[para(2,10):\n]",
        "[text(2,10):inner block 1\ninner block 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > > :True]",
        "[fcode-block(4,8):`:3:block:::::]",
        "[text(5,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<blockquote>
<p>inner block 1
inner block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_nl_extra_block_drop_block_with_blanks_around_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046m1
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block
    """
    # Arrange
    source_markdown = """1. > > ----
   > > > inner block 1
   > > > inner block 2
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > >\n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,4):   :   > > > \n   > > > \n   > >]",
        "[para(2,10):\n]",
        "[text(2,10):inner block 1\ninner block 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,7):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,7):]",
        "[tbreak(9,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<blockquote>
<p>inner block 1
inner block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_nl_extra_block_drop_block_with_thematics_around_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046k0
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_with_thematics
    """
    # Arrange
    source_markdown = """1. > > ----
   > > > inner block 1
   > > > inner block 2
   > > ----
   > > ```block
   > > A code block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,4):   :   > > > \n   > > > \n   > > ]",
        "[para(2,10):\n]",
        "[text(2,10):inner block 1\ninner block 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > > :True]",
        "[tbreak(4,8):-::----]",
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<blockquote>
<p>inner block 1
inner block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_nl_extra_block_drop_block_with_thematics_around_blanks_around_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046k1
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_with_thematics
    """
    # Arrange
    source_markdown = """1. > > ----
   > > > inner block 1
   > > > inner block 2
   > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > >\n   > > \n   > > \n   > > \n   > >\n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,4):   :   > > > \n   > > > \n   > > ]",
        "[para(2,10):\n]",
        "[text(2,10):inner block 1\ninner block 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > > :True]",
        "[tbreak(4,8):-::----]",
        "[BLANK(5,7):]",
        "[fcode-block(6,8):`:3:block:::::]",
        "[text(7,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,7):]",
        "[tbreak(10,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<blockquote>
<p>inner block 1
inner block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_nl_extra_list_li_drop_list_with_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046j0
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list
    """
    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > > ```block
   > > A code block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  \n]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9::]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_nl_extra_list_li_drop_list_with_blanks_around_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046j1
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list
    """
    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > >\n   > > \n   > > \n   > > \n   > >\n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  \n\n]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9::]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,7):]",
        "[end-ulist:::True]",
        "[fcode-block(6,8):`:3:block:::::]",
        "[text(7,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,7):]",
        "[tbreak(10,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_nl_extra_list_li_drop_list_with_thematics_around_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046h0
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_with_thematics
    """
    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > > ----
   > > ```block
   > > A code block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9::]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,8):-::----]",
        "[fcode-block(6,8):`:3:block:::::]",
        "[text(7,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
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
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_ordered_block_block_nl_extra_list_li_drop_list_with_thematics_around_blanks_around_fenced() -> (
    None
):
    """
    Verify that a nesting of ordered list, block quote, block quote, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.

    was: test_extra_046h1
    refs: bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_with_thematics
    """
    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > > \n   > >\n   > > \n   > > \n   > > \n   > >\n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9::]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,8):-::----]",
        "[BLANK(6,7):]",
        "[fcode-block(7,8):`:3:block:::::]",
        "[text(8,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,7):]",
        "[tbreak(11,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
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
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
