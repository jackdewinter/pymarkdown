"""
https://github.github.com/gfm/#paragraph
"""
from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_nl_t_nl_hs():
    """
    Test case:  Ordered list newline text new line setext heading
    was:        test_list_blocks_256hx
    """

    # Arrange
    source_markdown = """1.
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[setext(3,1):-:3::(2,1)]",
        "[text(2,1):foo:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<h2>foo</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_nl_t_nl_all_hs():
    """
    Test case:  Ordered list newline text new line setext heading
    """

    # Arrange
    source_markdown = """1.
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n]",
        "[BLANK(1,3):]",
        "[setext(3,4):-:3::(2,4)]",
        "[text(2,4):foo:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>foo</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_nl_i2_t_nl_hs():
    """
    Test case:  Ordered list newline indent of 2 text new line setext heading
    was:        test_list_blocks_256hxa
    """

    # Arrange
    source_markdown = """1.
  foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[setext(3,1):-:3:  :(2,3)]",
        "[text(2,3):foo:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<h2>foo</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_nl_i3_t_nl_hs():
    """
    Test case:  Ordered list newline indent of 3 text new line setext heading
    was:        test_list_blocks_256hxb
    """

    # Arrange
    source_markdown = """1.
   foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[para(2,4):]",
        "[text(2,4):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list newline indent of 3 text new line indent of 3 setext heading
    was:        test_list_blocks_256hxc
    """

    # Arrange
    source_markdown = """1.
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n]",
        "[BLANK(1,3):]",
        "[setext(3,4):-:3::(2,4)]",
        "[text(2,4):foo:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>foo</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_t_nl_t_nl_hs():
    """
    Test case:  Ordered list text newline text new line setext heading
    was:        test_list_blocks_256ha
    """

    # Arrange
    source_markdown = """1. abc
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n]",
        "[text(1,4):abc\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_t_nl_t_nl_all_hs():
    """
    Test case:  Ordered list text newline text new line setext heading
    """

    # Arrange
    source_markdown = """1. abc
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n]",
        "[setext(3,4):-:3::(1,4)]",
        "[text(1,4):abc\nfoo::\n]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>abc
foo</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_t_nl_i2_t_nl_hs():
    """
    Test case:  Ordered list text newline indent of 2 text new line setext heading
    was:        test_list_blocks_256haa
    """

    # Arrange
    source_markdown = """1. abc
  foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n  ]",
        "[text(1,4):abc\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_t_nl_i3_t_nl_hs():
    """
    Test case:  Ordered list text newline indent of 3 text new line setext heading
    was:        test_list_blocks_256hab
    """

    # Arrange
    source_markdown = """1. abc
   foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_t_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list text newline indent of 3 text new line indent of 3 setext heading
    was:        test_list_blocks_256hac
    """

    # Arrange
    source_markdown = """1. abc
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n]",
        "[setext(3,4):-:3::(1,4)]",
        "[text(1,4):abc\nfoo::\n]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>abc
foo</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_ol_nl_t_nl_hs():
    """
    Test case:  Ordered list x2 text newline new line setext heading
    """

    # Arrange
    source_markdown = """1. 1.
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[setext(3,1):-:3::(2,1)]",
        "[text(2,1):foo:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<h2>foo</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_ol_nl_t_nl_all_hs():
    """
    Test case:  Ordered list x2 text newline new line setext heading
    """

    # Arrange
    source_markdown = """1. 1.
      foo
      ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :      \n      \n]",
        "[BLANK(1,6):]",
        "[setext(3,7):-:3::(2,7)]",
        "[text(2,7):foo:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<h2>foo</h2>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_ol_t_nl_t_nl_hs():
    """
    Test case:  Ordered list x2 text newline text new line setext heading
    was:        test_list_blocks_256hb
    """

    # Arrange
    source_markdown = """1. 1. abc
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :]",
        "[para(1,7):\n]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_ol_t_nl_t_nl_all_hs():
    """
    Test case:  Ordered list x2 text newline text new line setext heading
    """

    # Arrange
    source_markdown = """1. 1. abc
      foo
      ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :      \n      \n]",
        "[setext(3,7):-:3::(1,7)]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<h2>abc
foo</h2>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_nl_i3_ol_nl_t_nl_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list new line text newline setext heading
    """

    # Arrange
    source_markdown = """1.
   1.
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[setext(4,1):-:3::(3,1)]",
        "[text(3,1):foo:]",
        "[end-setext::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<h2>foo</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_t_nl_i3_ol_nl_t_nl_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list new line text newline setext heading
    """

    # Arrange
    source_markdown = """1. abc
   1.
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[para(1,4):\n\n]",
        "[text(1,4):abc\n1.\nfoo::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
foo</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ul_t_nl_i2_ul_nl_t_nl_hs():
    """
    Test case:  Unordered list text newline indent of 2 unordered list new line text newline setext heading
    """

    # Arrange
    source_markdown = """- abc
  -
foo
---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[end-ulist:::True]",
        "[setext(4,1):-:3::(3,1)]",
        "[text(3,1):foo:]",
        "[end-setext::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>
<h2>foo</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ul_t_nl_i2_ulb_nl_t_nl_hs():
    """
    Test case:  Unordered list text newline indent of 2 unordered list (b) new line text newline setext heading
    """

    # Arrange
    source_markdown = """- abc
  *
foo
---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n]",
        "[para(1,3):\n\n]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[text(2,2):\nfoo::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
*
foo</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_nl_i3_ol_t_nl_t_nl_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list text new line text newline setext heading
    """

    # Arrange
    source_markdown = """1.
   1. def
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_t_nl_i3_ol_t_nl_t_nl_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text new line text newline setext heading
    was:        test_list_blocks_256hc
    """

    # Arrange
    source_markdown = """1. abc
   1. def
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_nl_i3_ol_nl_i2_t_nl_i2_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list new line indent of
                2 text newline indent of 2 setext heading
    """

    # Arrange
    source_markdown = """1.
   1.
  foo
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[setext(4,3):-:3:  :(3,3)]",
        "[text(3,3):foo:]",
        "[end-setext:  :]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<h2>foo</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_t_nl_i3_ol_nl_i2_t_nl_i2_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list new line indent
                of 2 text newline indent of 2 setext heading
    """

    # Arrange
    source_markdown = """1. abc
   1.
  foo
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[para(1,4):\n\n  ]",
        "[text(1,4):abc\n1.\nfoo::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(4,3):-:  :---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
foo</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ul_t_nl_i2_ul_nl_i1_t_nl_i1_hs():
    """
    Test case:  Unordered list text newline indent of 2 unordered list new line
                indent of 1 text newline indent of 1 setext heading
    """

    # Arrange
    source_markdown = """- abc
  -
 foo
 ---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[end-ulist:::True]",
        "[setext(4,2):-:3: :(3,2)]",
        "[text(3,2):foo:]",
        "[end-setext: :]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>
<h2>foo</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ul_t_nl_i2_ulb_nl_i1_t_nl_i1_hs():
    """
    Test case:  Unordered list text newline indent of 2 unordered list (b) new
                line indent of 1 text newline indent of 1 setext heading
    """

    # Arrange
    source_markdown = """- abc
  *
 foo
 ---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n]",
        "[para(1,3):\n\n ]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[text(2,2):\nfoo::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,2):-: :---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
*
foo</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_nl_i3_ol_t_nl_i2_t_nl_i2_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list text new line indent
                of 2 text newline indent of 2 setext heading
    """

    # Arrange
    source_markdown = """1.
   1. def
  foo
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n  ]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(4,3):-:  :---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_t_nl_i3_ol_t_nl_i2_t_nl_i2_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text new line
                indent of 2 text newline indent of 2 setext heading
    was:        test_list_blocks_256hd
    """

    # Arrange
    source_markdown = """1. abc
   1. def
  foo
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n  ]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(4,3):-:  :---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_nl_i3_ol_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list new line indent
                of 3 text newline indent of 3 setext heading
    """

    # Arrange
    source_markdown = """1.
   1.
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[setext(4,4):-:3::(3,4)]",
        "[text(3,4):foo:]",
        "[end-setext::]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
<h2>foo</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_t_nl_i3_ol_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list new line indent
                of 3 text newline indent of 3 setext heading
    """

    # Arrange
    source_markdown = """1. abc
   1.
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n]",
        "[setext(4,4):-:3::(1,4)]",
        "[text(1,4):abc\n1.\nfoo::\n\n]",
        "[end-setext::]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>abc
1.
foo</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ul_t_nl_i2_ul_nl_i2_t_nl_i2_hs():
    """
    Test case:  Unordered list text newline indent of 2 unordered list new line
                indent of 2 text newline indent of 2 setext heading
    """

    # Arrange
    source_markdown = """- abc
  -
  foo
  ---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[setext(4,3):-:3::(3,3)]",
        "[text(3,3):foo:]",
        "[end-setext::]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
<h2>foo</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ul_t_nl_i2_ulb_nl_i2_t_nl_i2_hs():
    """
    Test case:  Unordered list text newline indent of 2 unordered list (b) new line
                indent of 2 text newline indent of 2 setext heading
    """

    # Arrange
    source_markdown = """- abc
  *
  foo
  ---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n]",
        "[setext(4,3):-:3::(1,3)]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[text(2,2):\nfoo::\n]",
        "[end-setext::]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc
*
foo</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_nl_i3_ol_t_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list text new line indent
                of 3 text newline indent of 3 setext heading
    """

    # Arrange
    source_markdown = """1.
   1. def
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n   ]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(4,4):-::---]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def
foo</li>
</ol>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hs_ol_t_nl_i3_ol_t_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text new line
                indent of 3 text newline indent of 3 setext heading
    was:        test_list_blocks_256he
    """

    # Arrange
    source_markdown = """1. abc
   1. def
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n   ]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(4,4):-::---]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo</li>
</ol>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
