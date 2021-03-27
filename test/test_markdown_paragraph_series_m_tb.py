"""
https://github.github.com/gfm/#paragraph
"""
import pytest

from .utils import act_and_assert


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_nl_tb():
    """
    Test case:  Ordered list newline thematic break
    was:        test_list_blocks_256fx
    """

    # Arrange
    source_markdown = """1.
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[tbreak(2,1):-::---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_nl_i2_tb():
    """
    Test case:  Ordered list new line indent of 2 thematic break
    was:        test_list_blocks_256fxa
    """

    # Arrange
    source_markdown = """1.
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[tbreak(2,3):-:  :---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_nl_i3_tb():
    """
    Test case:  Ordered list new line indent of 3 thematic break
    Test case:  Ordered list thematic break on next line after an indent of 3
    was:        test_list_blocks_256fxb
    """

    # Arrange
    source_markdown = """1.
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[tbreak(2,4):-::---]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_t_nl_tb():
    """
    Test case:  Ordered list text new line thematic break
    was:        test_list_blocks_256fa
    """

    # Arrange
    source_markdown = """1. abc
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(2,1):-::---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_t_nl_i2_tb():
    """
    Test case:  Ordered list text newline indent of 2 thematic break
    was:        test_list_blocks_256faa
    """

    # Arrange
    source_markdown = """1. abc
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(2,3):-:  :---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_t_nl_i3_tb():
    """
    Test case:  Ordered list text newline indent of 2 thematic break
    was:        test_list_blocks_256fab
    """

    # Arrange
    source_markdown = """1. abc
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[setext(2,4):-:3::(1,4)]",
        "[text(1,4):abc:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>abc</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_ol_nl_tb():
    """
    Test case:  Ordered list x2 new line thematic break
    """

    # Arrange
    source_markdown = """1. 1.
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(2,1):-::---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_ol_t_nl_tb():
    """
    Test case:  Ordered list x2 text new line thematic break
    was:        test_list_blocks_256fb
    """

    # Arrange
    source_markdown = """1. 1. abc
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(2,1):-::---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_nl_ol_nl_tb():
    """
    Test case:  Ordered list newline ordered list new line thematic break
    """

    # Arrange
    source_markdown = """1.
   1.
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_t_nl_ol_nl_tb():
    """
    Test case:  Ordered list text newline ordered list new line thematic break
    """

    # Arrange
    source_markdown = """1. abc
   1.
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n1.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ul_t_nl_ul_nl_tb():
    """
    Test case:  Unordered list text newline unordered list new line thematic break
    """

    # Arrange
    source_markdown = """- abc
  -
---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[end-ulist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ul_t_nl_ulb_nl_tb():
    """
    Test case:  Unordered list text newline unordered list (b) new line thematic break
    """

    # Arrange
    source_markdown = """- abc
  *
---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
*</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ul_t_nl_ul_t_nl_ulb_nl_tb():
    """
    Test case:  Unordered list text newline unordered list (b) new line thematic break
    """

    # Arrange
    source_markdown = """- abc
- def
  *
---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):\n]",
        "[text(2,3):def\n::\n]",
        "[text(3,1):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li>abc</li>
<li>def
*</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ul_t_nl_ul_t_nl_i3_ulb_nl_tb():
    """
    Test case:  Unordered list text newline unordered list (b) new line thematic break
    """

    # Arrange
    source_markdown = """- abc
- def
  *
---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):\n]",
        "[text(2,3):def\n::\n]",
        "[text(3,1):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li>abc</li>
<li>def
*</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ul_t_nl_i3_ul_t_nl_ulb_nl_tb():
    """
    Test case:  Unordered list text newline unordered list (b) new line thematic break
    """

    # Arrange
    source_markdown = """- abc
  - def
  *
---
"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[ulist(3,3):*::4:  ]",
        "[BLANK(3,4):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def</li>
</ul>
<ul>
<li></li>
</ul>
</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_nl_ol_t_nl_tb():
    """
    Test case:  Ordered list newline ordered list text new line thematic break
    was:        test_list_blocks_256fc
    """

    # Arrange
    source_markdown = """1.
   1. abc
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_t_nl_ol_t_nl_tb():
    """
    Test case:  Ordered list text newline ordered list text new line thematic break
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_nl_ol_nl_i2_tb():
    """
    Test case:  Ordered list newline ordered list new line indent of 2 thematic break
    """

    # Arrange
    source_markdown = """1.
   1.
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,3):-:  :---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_t_nl_ol_nl_i2_tb():
    """
    Test case:  Ordered list text newline ordered list new line indent of 2 thematic break
    """

    # Arrange
    source_markdown = """1. abc
   1.
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n1.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,3):-:  :---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ul_t_nl_ul_nl_i1_tb():
    """
    Test case:  Unordered list text newline unordered list new line indent of 1 thematic break
    """

    # Arrange
    source_markdown = """- abc
  -
 ---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[end-ulist:::True]",
        "[tbreak(3,2):-: :---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ul_t_nl_ulb_nl_i1_tb():
    """
    Test case:  Unordered list text newline unordered list (b) new line indent of 1 thematic break
    """

    # Arrange
    source_markdown = """- abc
  *
 ---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(3,2):-: :---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
*</li>
</ul>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_nl_ol_t_nl_i2_tb():
    """
    Test case:  Ordered list newline ordered list text new line indent of 2 thematic break
    was:        test_list_blocks_256fd
    """

    # Arrange
    source_markdown = """1.
   1. abc
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,3):-:  :---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_t_nl_ol_t_nl_i2_tb():
    """
    Test case:  Ordered list text newline ordered list text new line indent of 2 thematic break
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,3):-:  :---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_nl_ol_t_nl_i3_tb():
    """
    Test case:  Ordered list newline ordered list text new line indent of 3 thematic break
    was:        test_list_blocks_256fe
    """

    # Arrange
    source_markdown = """1.
   1. abc
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,4):-::---]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_t_nl_ol_t_nl_i3_tb():
    """
    Test case:  Ordered list text newline ordered list text new line indent of 3 thematic break
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,4):-::---]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_nl_ol_nl_i3_tb():
    """
    Test case:  Ordered list newline ordered list new line indent of 3 thematic break
    """

    # Arrange
    source_markdown = """1.
   1.
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[tbreak(3,4):-::---]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ol_t_nl_ol_nl_i3_tb():
    """
    Test case:  Ordered list text newline ordered list new line indent of 3 thematic break
    """

    # Arrange
    source_markdown = """1. abc
   1.
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[setext(3,4):-:3::(1,4)]",
        "[text(1,4):abc\n1.::\n]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>abc
1.</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ul_t_nl_ul_nl_i2_tb():
    """
    Test case:  Unordered list text newline unordered list new line indent of 3 thematic break
    """

    # Arrange
    source_markdown = """- abc
  -
  ---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[tbreak(3,3):-::---]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
<hr />
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_tb_ul_t_nl_ulb_nl_i2_tb():
    """
    Test case:  Unordered list text newline unordered list (b) new line indent of 3 thematic break
    """

    # Arrange
    source_markdown = """- abc
  *
  ---
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[setext(3,3):-:3::(1,3)]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc
*</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
