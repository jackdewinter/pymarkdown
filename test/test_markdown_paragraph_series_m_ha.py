"""
https://github.github.com/gfm/#paragraph
"""
import pytest

from .utils import act_and_assert


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_nl_ha_t():
    """
    Test case:  Ordered list newline atx heading text
    was:        test_list_blocks_256g
    """

    # Arrange
    source_markdown = """1.
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[atx(2,1):1:0:]",
        "[text(2,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_nl_i2_ha_t():
    """
    Test case:  Ordered list newline indent of 2 atx heading text
    was:        test_list_blocks_256gxa
    """

    # Arrange
    source_markdown = """1.
  # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[atx(2,3):1:0:  ]",
        "[text(2,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_nl_i3_ha_t():
    """
    Test case:  Ordered list newline indent of 3 atx heading text
    was:        test_list_blocks_256gxb
    """

    # Arrange
    source_markdown = """1.
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[atx(2,4):1:0:]",
        "[text(2,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h1>foo</h1>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_t_nl_ha_t():
    """
    Test case:  Ordered list text newline atx heading text
    was:        test_list_blocks_256ga
    """

    # Arrange
    source_markdown = """1. abc
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[atx(2,1):1:0:]",
        "[text(2,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_t_nl_i2_ha_t():
    """
    Test case:  Ordered list text newline indent of 2 atx heading text
    was:        test_list_blocks_256gaa
    """

    # Arrange
    source_markdown = """1. abc
  # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[atx(2,3):1:0:  ]",
        "[text(2,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_t_nl_i3_ha_t():
    """
    Test case:  Ordered list text newline indent of 3 atx heading text
    was:        test_list_blocks_256gab
    """

    # Arrange
    source_markdown = """1. abc
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[atx(2,4):1:0:]",
        "[text(2,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<h1>foo</h1>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_ol_nl_ha_t():
    """
    Test case:  Ordered list x2 newline atx heading text
    """

    # Arrange
    source_markdown = """1. 1.
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(2,1):1:0:]",
        "[text(2,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_ol_t_nl_ha_t():
    """
    Test case:  Ordered list x2 text newline atx heading text
    was:        test_list_blocks_256gb
    """

    # Arrange
    source_markdown = """1. 1. abc
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(2,1):1:0:]",
        "[text(2,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_nl_ol_nl_ha_t():
    """
    Test case:  Ordered list newline ordered list new line atx heading text
    """

    # Arrange
    source_markdown = """1.
   1.
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(3,1):1:0:]",
        "[text(3,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_t_nl_ol_nl_ha_t():
    """
    Test case:  Ordered list text newline ordered list new line atx heading text
    """

    # Arrange
    source_markdown = """1. abc
   1.
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n1.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[atx(3,1):1:0:]",
        "[text(3,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ul_t_nl_ul_nl_ha_t():
    """
    Test case:  Unordered list text newline unordered list new line atx heading text
    """

    # Arrange
    source_markdown = """- abc
  -
# foo
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext:::False]",
        "[end-ulist:::True]",
        "[atx(3,1):1:0:]",
        "[text(3,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ul_t_nl_ulb_nl_ha_t():
    """
    Test case:  Unordered list text newline unordered list (b) new line atx heading text
    """

    # Arrange
    source_markdown = """- abc
  *
# foo
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[atx(3,1):1:0:]",
        "[text(3,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
*</li>
</ul>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_nl_ol_t_nl_ha_t():
    """
    Test case:  Ordered list newline ordered list text new line atx heading text
    was:        test_list_blocks_256gc
    """

    # Arrange
    source_markdown = """1.
   1. abc
# foo
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
        "[atx(3,1):1:0:]",
        "[text(3,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_t_nl_ol_t_nl_ha_t():
    """
    Test case:  Ordered list text newline ordered list text new line atx heading text
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
# foo
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
        "[atx(3,1):1:0:]",
        "[text(3,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_nl_ol_nl_i2_ha_t():
    """
    Test case:  Ordered list newline ordered list new line indent of 2 atx heading text
    """

    # Arrange
    source_markdown = """1.
   1.
  # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(3,3):1:0:  ]",
        "[text(3,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_t_nl_ol_nl_i2_ha_t():
    """
    Test case:  Ordered list text newline ordered list new line indent of 2 atx heading text
    """

    # Arrange
    source_markdown = """1. abc
   1.
  # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n1.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[atx(3,3):1:0:  ]",
        "[text(3,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ul_t_nl_ul_nl_i1_ha_t():
    """
    Test case:  Unordered list text newline unordered list new line indent of 2 atx heading text
    """

    # Arrange
    source_markdown = """- abc
  -
 # foo
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext:::False]",
        "[end-ulist:::True]",
        "[atx(3,2):1:0: ]",
        "[text(3,4):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ul_t_nl_ulb_nl_i1_ha_t():
    """
    Test case:  Unordered list text newline unordered list (b) new line indent of 2 atx heading text
    """

    # Arrange
    source_markdown = """- abc
  *
 # foo
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[atx(3,2):1:0: ]",
        "[text(3,4):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
*</li>
</ul>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_nl_ol_t_nl_i2_ha_t():
    """
    Test case:  Ordered list newline ordered list text new line indent of 2 atx heading text
    was:        test_list_blocks_256gd
    """

    # Arrange
    source_markdown = """1.
   1. abc
  # foo
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
        "[atx(3,3):1:0:  ]",
        "[text(3,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_t_nl_ol_t_nl_i2_ha_t():
    """
    Test case:  Ordered list text newline ordered list text new line indent of 2 atx heading text
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
  # foo
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
        "[atx(3,3):1:0:  ]",
        "[text(3,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_nl_ol_nl_i3_ha_t():
    """
    Test case:  Ordered list newline ordered list new line indent of 3 atx heading text
    """

    # Arrange
    source_markdown = """1.
   1.
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[atx(3,4):1:0:]",
        "[text(3,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
<h1>foo</h1>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_t_nl_ol_nl_i3_ha_t():
    """
    Test case:  Ordered list text newline ordered list new line indent of 3 atx heading text
    """

    # Arrange
    source_markdown = """1. abc
   1.
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n1.::\n]",
        "[end-para:::False]",
        "[atx(3,4):1:0:]",
        "[text(3,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
<h1>foo</h1>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ul_t_nl_ul_nl_i2_ha_t():
    """
    Test case:  Unordered list text newline unordered list new line indent of 2 atx heading text
    """

    # Arrange
    source_markdown = """- abc
  -
  # foo
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext:::False]",
        "[atx(3,3):1:0:]",
        "[text(3,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
<h1>foo</h1>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ul_t_nl_ulb_nl_i2_ha_t():
    """
    Test case:  Unordered list text newline unordered list (b) new line indent of 2 atx heading text
    """

    # Arrange
    source_markdown = """- abc
  *
  # foo
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[end-para:::False]",
        "[atx(3,3):1:0:]",
        "[text(3,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
*
<h1>foo</h1>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_nl_ol_t_nl_i3_ha_t():
    """
    Test case:  Ordered list newline ordered list text new line indent of 3 atx heading text
    was:        test_list_blocks_256ge
    """

    # Arrange
    source_markdown = """1.
   1. abc
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[atx(3,4):1:0:]",
        "[text(3,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
<h1>foo</h1>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ha_ol_t_nl_ol_t_nl_i3_ha_t():
    """
    Test case:  Ordered list text newline ordered list text new line indent of 3 atx heading text
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[atx(3,4):1:0:]",
        "[text(3,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
<h1>foo</h1>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
