"""
https://github.github.com/gfm/#paragraph
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_nl_i4_t_ib():
    """
    Test case:  Indent of 3 ordered list newline indent of 4 text (indented block)
    was:        test_list_blocks_256ix
    """

    # Arrange
    source_markdown = """   1.
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[icode-block(2,5):    :]",
        "[text(2,5):foo:]",
        "[end-icode-block:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_nl_i7_t_all_ib():
    """
    Test case:  Indent of 3 ordered list newline indent of 7 text (indented block)
    """

    # Arrange
    source_markdown = """1.
       foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[BLANK(1,3):]",
        "[icode-block(2,8):    :]",
        "[text(2,8):foo:]",
        "[end-icode-block:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>foo
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_nl_i5_t_ib():
    """
    Test case:  Indent of 3 ordered list newline indent of 5 text (indented block)
    was:        test_list_blocks_256ixa
    """

    # Arrange
    source_markdown = """   1.
     foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[icode-block(2,5):    :]",
        "[text(2,5):foo: ]",
        "[end-icode-block:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<pre><code> foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_nl_i6_t_fb():
    """
    Test case:  Indent of 3 ordered list newline indent of 6 text (indented block)
    was:        test_list_blocks_256ixb
    """

    # Arrange
    source_markdown = """   1.
      foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      \n]",
        "[BLANK(1,6):]",
        "[para(2,7):]",
        "[text(2,7):foo:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_t_nl_i4_t_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 4 text (indented block)
    was:        test_list_blocks_256ia
    """

    # Arrange
    source_markdown = """   1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :\n]",
        "[para(1,7):\n    ]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_t_nl_i10_t_all_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """   1. abc
          foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      \n]",
        "[para(1,7):\n    ]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_t_nl_nl_i10_t_all_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """   1. abc

          foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :\n      \n]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,11):    :]",
        "[text(3,11):foo:]",
        "[end-icode-block:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<p>abc</p>
<pre><code>foo
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_t_nl_i5_t_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 5 text (indented block)
    was:        test_list_blocks_256iaa
    """

    # Arrange
    source_markdown = """   1. abc
     foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :\n]",
        "[para(1,7):\n     ]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_t_nl_i6_t_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 6 text (indented block)
    was:        test_list_blocks_256iab
    """

    # Arrange
    source_markdown = """   1. abc
      foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      \n]",
        "[para(1,7):\n]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_ol_ol_nl_i4_t_ib():
    """
    Test case:  Ordered list x2 newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """1. 1.
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[para(2,5): ]",
        "[text(2,5):foo:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
foo</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_ol_ol_nl_i10_t_all_ib():
    """
    Test case:  Ordered list x2 newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """1. 1.
          foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :      \n]",
        "[BLANK(1,6):]",
        "[icode-block(2,11):    :]",
        "[text(2,11):foo:]",
        "[end-icode-block:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<pre><code>foo
</code></pre>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_ol_ol_t_nl_i4_t_ib():
    """
    Test case:  Ordered list x2 text newline indent of 4 text (indented block)
    was:        test_list_blocks_256ib
    """

    # Arrange
    source_markdown = """1. 1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :\n]",
        "[para(1,7):\n    ]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_ol_ol_t_nl_i4_t_all_ib():
    """
    Test case:  Ordered list x2 text newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """1. 1. abc
          foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :      \n]",
        "[para(1,7):\n    ]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_ol_ol_t_nl_nl_i4_t_all_ib():
    """
    Test case:  Ordered list x2 text newline newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """1. 1. abc

          foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :\n      \n]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,11):    :]",
        "[text(3,11):foo:]",
        "[end-icode-block:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<p>abc</p>
<pre><code>foo
</code></pre>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_ol_nl_i3_ol_nl_i4_t_ib():
    """
    Test case:  Ordered list newline indent of 3 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """1.
   1.
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[para(3,5): ]",
        "[text(3,5):foo:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
foo</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_ol_t_nl_i3_ol_nl_i4_t_ib():
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """1. abc
   1.
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n]",
        "[para(1,4):\n\n ]",
        "[text(1,4):abc\n1.\nfoo::\n\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
foo</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_ul_t_nl_i2_ul_nl_i4_t_ib():
    """
    Test case:  Unordered list text newline indent of 2 unordered list newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """- abc
  -
    foo
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[para(3,5):  ]",
        "[text(3,5):foo:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_ul_t_nl_i2_ulb_nl_i4_t_ib():
    """
    Test case:  Unordered list text newline indent of 2 unordered list (b) newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """- abc
  *
    foo
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n]",
        "[para(1,3):\n\n  ]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[text(2,2):\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
*
foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_ol_nl_i3_ol_t_nl_i4_t_ib():
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline indent of 4 text (indented block)
    was:        test_list_blocks_256ic
    """

    # Arrange
    source_markdown = """1.
   1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :\n]",
        "[para(2,7):\n    ]",
        "[text(2,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_ol_t_nl_i3_ol_t_nl_i4_t_ib():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n]",
        "[para(2,7):\n    ]",
        "[text(2,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_nl_i5_ol_nl_i4_t_ib():
    """
    Test case:  Indent of 3 ordered list newline indent of 5 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """   1.
      1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[olist(2,7):.:1:9:      :\n]",
        "[para(2,10):\n    ]",
        "[text(2,10):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_t_nl_i5_ol_nl_i4_t_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 5 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """   1. abc
      1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[olist(2,7):.:1:9:      :\n]",
        "[para(2,10):\n    ]",
        "[text(2,10):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_nl_i5_ol_t_nl_i4__t_ib():
    """
    Test case:  Indent of 3 ordered list newline indent of 5 ordered list text newline indent of 4 text (indented block)
    was:        test_list_blocks_256id
    """

    # Arrange
    source_markdown = """   1.
      1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[olist(2,7):.:1:9:      :\n]",
        "[para(2,10):\n    ]",
        "[text(2,10):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i3_ol_t_nl_i5_ol_t_nl_i4_t_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 5 ordered list
                text newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """   1. abc
      1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[olist(2,7):.:1:9:      :\n]",
        "[para(2,10):\n    ]",
        "[text(2,10):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i1_ol_nl_i4_ol_nl_i4_t_ib():
    """
    Test case:  Indent of 1 ordered list newline indent of 4 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """ 1. abc
    1.
    foo
"""
    expected_tokens = [
        "[olist(1,2):.:1:4: :    \n    \n]",
        "[para(1,5):\n\n]",
        "[text(1,5):abc\n1.\nfoo::\n\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
foo</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i2_ul_nl_i4_ul_nl_i4_t_ib():
    """
    Test case:  Indent of 2 unordered list newline indent of 4 unordered list newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """  - abc
    -
    foo
"""
    expected_tokens = [
        "[ulist(1,3):-::4:  :    \n    \n]",
        "[setext(2,5):-:1::(1,5)]",
        "[text(1,5):abc:]",
        "[end-setext::]",
        "[para(3,5):]",
        "[text(3,5):foo:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i2_ul_nl_i4_ulb_nl_i4_t_ib():
    """
    Test case:  Indent of 2 unordered list newline indent of 4 unordered list
                (b) newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """  - abc
    *
    foo
"""
    expected_tokens = [
        "[ulist(1,3):-::4:  :    \n    \n]",
        "[para(1,5):\n\n]",
        "[text(1,5):abc\n::\n]",
        "[text(2,1):*:]",
        "[text(2,2):\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
*
foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i1_ol_t_nl_i4_ol_nl_i4_t_ib():
    """
    Test case:  Indent of 1 ordered list text newline indent of 4 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """ 1. abc
    1.
    foo
"""
    expected_tokens = [
        "[olist(1,2):.:1:4: :    \n    \n]",
        "[para(1,5):\n\n]",
        "[text(1,5):abc\n1.\nfoo::\n\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
foo</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i2_ul_t_nl_i4_ul_nl_i4_t_ib():
    """
    Test case:  Indent of 2 unordered list text newline indent of 4 unordered
                list newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """  - abc
    -
    foo
"""
    expected_tokens = [
        "[ulist(1,3):-::4:  :    \n    \n]",
        "[setext(2,5):-:1::(1,5)]",
        "[text(1,5):abc:]",
        "[end-setext::]",
        "[para(3,5):]",
        "[text(3,5):foo:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i2_ul_t_nl_i4_ulb_nl_i4_t_ib():
    """
    Test case:  Indent of 2 unordered list text newline indent of 4 unordered
                list (b) newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """  - abc
    *
    foo
"""
    expected_tokens = [
        "[ulist(1,3):-::4:  :    \n    \n]",
        "[para(1,5):\n\n]",
        "[text(1,5):abc\n::\n]",
        "[text(2,1):*:]",
        "[text(2,2):\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
*
foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i1_ol_nl_i4_ol_t_nl_i4_t_ib():
    """
    Test case:  Indent of 1 ordered list newline indent of 4 ordered list text newline indent of 4 text (indented block)
    """

    # Arrange
    source_markdown = """ 1.
    1. def
    foo
"""
    expected_tokens = [
        "[olist(1,2):.:1:4: ]",
        "[BLANK(1,4):]",
        "[olist(2,5):.:1:7:    :\n]",
        "[para(2,8):\n    ]",
        "[text(2,8):def\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ib_i1_ol_t_nl_i4_ol_t_nl_i4_t_ib():
    """
    Test case:  Indent of 1 ordered list text newline indent of 4 ordered list text
                newline indent of 4 text (indented block)
    was:        test_list_blocks_256ie
    """

    # Arrange
    source_markdown = """ 1. abc
    1. def
    foo
"""
    expected_tokens = [
        "[olist(1,2):.:1:4: ]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[olist(2,5):.:1:7:    :\n]",
        "[para(2,8):\n    ]",
        "[text(2,8):def\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
